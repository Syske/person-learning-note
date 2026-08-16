# 国内Docker拉取镜像实战：加速器对比与SSH隧道出海

> 背景：国内服务器拉取 Docker Hub 镜像（`sunxiao0721/beecount-cloud`，501MB）反复失败。
> 本文总结：加速器可用性对比、免费加速器限速问题、**SSH 反向隧道 + 本机代理出海**的完整方案，
> 以及 CasaOS 部署时**数据卷误放 /tmp 的风险与迁移**。

## 一、问题现象

```bash
# dockerd 拉取日志
journalctl -u docker | grep -iE 'pull|error'

# 典型错误：
# 1. Docker Hub 直连（被墙）
Get "https://registry-1.docker.io/v2/": context deadline exceeded
# 2. 1ms.run 加速器不稳定
net/http: TLS handshake timeout / unexpected EOF
# 3. DaoCloud 白名单拒绝
denied: this image is not in the allowlist
```

## 二、加速器可用性测试

```bash
# 测试加速器能否取到镜像 manifest（最关键的一步）
for m in "https://docker.1panel.live" "https://docker.xuanyuan.me" \
         "https://hub.rat.dev" "https://dockerpull.org" \
         "https://docker.1ms.run" "https://docker.m.daocloud.io"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -m 8 \
    -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
    "$m/v2/sunxiao0721/beecount-cloud/manifests/latest")
  echo "$m -> HTTP:$code"
done
```

实测结果（2026-08）：

| 加速器 | manifest | blob 下载速度 | 结论 |
|---|---|---|---|
| docker.1panel.live | 200 ✅ | 36~101 KB/s | 慢但可用 |
| docker.xuanyuan.me | 429 | 245 B/s | 限流不可用 |
| hub.rat.dev | 302 | 471 B/s | 不可用 |
| dockerpull.org | 000 | - | 不可用 |
| docker.1ms.run | 401 | 697 B/s | 不稳定 |
| docker.m.daocloud.io | 401 | - | **白名单外镜像拒绝** |

> ⚠️ **关键结论**：免费加速器即使 manifest 可达，blob（镜像层）下载普遍限速到
> **几十 B/s ~ 几百 KB/s**，大镜像实际不可用。1panel.live 是最可用的，但 501MB 镜像
> 需要数小时且中途易断。

## 三、解决方案：SSH 反向隧道 + 本机 Clash 出海

### 思路

利用 Windows 本机（105）已运行的 Clash 代理，把 103 的流量转发给 Clash 出海：

```
103:127.0.0.1:17897  ←—SSH反向隧道—→  105:127.0.0.1:7897 (Clash)  → Docker Hub
```

**为什么不用 allow-lan 直接暴露 7897？**
- Windows 防火墙（公用配置 BlockInbound）会阻止局域网访问 7897
- 开启 allow-lan 等于把代理暴露给局域网所有设备，有安全风险
- SSH 隧道是 105 **主动出站**（SSH 22 放行），天然穿透防火墙，且只服务 103 一个目标

### 隧道实现（paramiko 反向端口转发）

```python
import paramiko, socket, threading

cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cli.connect('192.168.0.103', 22, username='syske', password='***')
transport = cli.get_transport()
transport.request_port_forward('127.0.0.1', 17897)   # 在 103 上监听 17897

def pump(src, sink):          # 双向拷贝
    try:
        while True:
            data = src.recv(65536)
            if not data: break
            sink.sendall(data)
    except Exception: pass
    finally:
        try: sink.close()
        except Exception: pass

while True:
    chan = transport.accept(10)                       # 等待 103 上的新连接
    if chan is not None:
        dst = socket.create_connection(('127.0.0.1', 7897))  # 转发到本机 Clash
        threading.Thread(target=pump, args=(chan, dst), daemon=True).start()
        threading.Thread(target=pump, args=(dst, chan), daemon=True).start()
```

### 使用方式

```bash
# 103 上验证隧道（HTTP 401 = registry 可达，正常）
curl -x http://127.0.0.1:17897 https://registry-1.docker.io/v2/

# 经加速器拉取（1panel.live 最可用）
nohup docker pull docker.1panel.live/sunxiao0721/beecount-cloud:latest > /tmp/pull.log 2>&1 &

# 拉取完成后 tag 回原镜像名
docker tag docker.1panel.live/sunxiao0721/beecount-cloud:latest sunxiao0721/beecount-cloud:latest
```

> 若需要让 `docker pull` 直接走代理，可在 daemon 配置代理后重启 dockerd
> （`/etc/systemd/system/docker.service.d/http-proxy.conf` 或 daemon.json `proxies` 字段），
> 注意**重启 dockerd 会重启全部容器**（有 restart policy 的会自动恢复）。

### 隧道开机自启（Windows）

```python
import winreg, shutil
pw = shutil.which('pythonw')          # pythonw 无窗口后台运行
cmd = '"%s" "C:/Users/syske/clash_forward.py"' % pw
k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
    r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_WRITE)
winreg.SetValueEx(k, "ClashForwardTunnel", 0, winreg.REG_SZ, cmd)
winreg.CloseKey(k)
```

### 隧道对服务器网络的影响

- **零影响**：隧道只监听 `127.0.0.1:17897`，服务器正常流量（Web/DNS/SSH/镜像加速器）
  全走自身路由与本地 DNS，无任何代理环境变量
- 本机关机/不开隧道：服务器**不会断外网**，仅失去"经代理访问被墙站点"的能力

## 四、数据卷持久化：/tmp 的坑（CasaOS）

### 问题

CasaOS 生成的 compose 默认把 bind 卷放在 `/tmp/casaos-compose-app-<id>/data`：

```bash
docker inspect <容器> --format '{{range .Mounts}}{{.Source}}->{{.Destination}}{{end}}'
# /tmp/casaos-compose-app-2779781215/data->/data   ← 危险！
```

`/tmp` 语义上是临时目录（systemd-tmpfiles 会清理 10 天前的文件），数据库放这里极易丢失。

### 迁移步骤

```bash
# 1. 停止容器
docker stop <容器>
# 2. 迁移数据（cp -a dir/. dest/ 保留隐藏文件！如 .jwt_secret / .initial_admin_password）
mkdir -p /DATA/AppData/beecount-cloud/data
cp -a /tmp/casaos-compose-app-2779781215/data/. /DATA/AppData/beecount-cloud/data/
# 3. 修改 CasaOS compose 卷路径
sed -i 's|/tmp/casaos-compose-app-2779781215/data|/DATA/AppData/beecount-cloud/data|' \
  /var/lib/casaos/apps/<project>/docker-compose.yml
# 4. 重建并验证
cd /var/lib/casaos/apps/<project> && docker compose up -d
docker inspect <容器> --format '{{range .Mounts}}{{.Source}}->{{.Destination}}{{end}}'
# /DATA/AppData/beecount-cloud/data->/data   ✅
# 5. 清理旧目录
rm -rf /tmp/casaos-compose-app-2779781215
```

> 💡 CasaOS 管理的 compose 在 `/var/lib/casaos/apps/<随机project名>/docker-compose.yml`，
> 容器 label `com.docker.compose.project.config_files` 可查到确切路径。
> 挂载路径、端口等改动直接改 compose 后 `docker compose up -d` 即可重建。

## 五、经验总结

1. **免费镜像加速器普遍对 blob 限速**，manifest 可达 ≠ 能下完；大镜像优先考虑代理方案
2. **allow-lan 暴露代理有安全风险**，SSH 反向隧道是更优雅的局域网内"借道出海"方案
3. **数据卷位置是部署必修课**：CasaOS 默认 /tmp 卷务必迁移到持久路径，且用 `cp -a dir/. dest/` 保留隐藏文件
4. `docker inspect` 是排查容器配置的瑞士军刀：Mounts / Config.Env / Labels / RestartPolicy 全都能查
