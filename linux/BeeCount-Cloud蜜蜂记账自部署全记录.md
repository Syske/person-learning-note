# BeeCount-Cloud(蜜蜂记账)自部署全记录

> 背景：使用开源记账 App **BeeCount（蜜蜂记账）**，数据从随手记迁移（CSV/xlsx 分类整理），
> 自部署其配套的 BeeCount-Cloud（同步云端 + Web 报表）。
> 本文记录：数据准备 → 部署 → 镜像拉取难题（国内环境）→ 配置修复（数据卷持久化）。

## 一、整体架构

```
BeeCount App（手机）  ←→  http://192.168.0.103:8869  (BeeCount-Cloud 容器, CasaOS 管理)
                                  │
              /DATA/AppData/beecount-cloud/data  (SQLite beecount.db, 持久卷)
```

- 镜像：`sunxiao0721/beecount-cloud:latest`（Docker Hub）
- 端口：`8869 → 8080`
- 数据：SQLite（`/data/beecount.db`）+ 附件
- 健康检查：`GET /healthz → {"status":"ok"}`
- 初始管理员：镜像首次启动生成于 `data/.initial_admin_password`（`owner@example.com`）

## 二、数据准备（随手记 → BeeCount 分类映射）

### 1. 分类体系

BeeCount 分类包 `categories.yaml` 结构：一级分类（`level: 1`）+ 二级分类（`level: 2`，带 `parent_name`），
`kind` 区分 expense/income/transfer。

### 2. 旧数据分类映射

随手记导出的 xlsx 是通用分类（餐饮/早午晚餐、交通/公共交通…），需映射到 BeeCount 体系：

- **备注细分**：餐饮按备注"早餐/午餐/晚餐"拆到对应二级分类
- **组合兜底**：每个（旧一级,旧二级）组合配一个映射函数，如 交通/私家车费用 → 交通/加油、汽车/汽车保养…
- **关键词规则** + 全局兜底（支出→购物/日用百货，收入→红包/节日红包）
- 映射脚本可重复执行（`dry` 预览 / `write` 写回），目标分类通过 yaml 校验

### 3. 生成 BeeCount 兼容 CSV（关键！）

BeeCount 原生导出格式（注意列名差异）：

```
类型,分类,二级分类,金额,币种,账户,转出账户,转入账户,备注,时间,标签,附件
支出,餐饮,晚餐,15.00,CNY,支付宝,,,晚餐,2026-08-04 18:28:52,,
```

> ⚠️ **导入报错 `null check operator used on a null value` 的根因**：
> - 列名不匹配：xlsx 用"转出**账号**"，BeeCount 模板是"转出**账户**"
> - xlsx 空单元格 = `null`，而 CSV 空字段 = 空字符串。Flutter 解析器对 null 做 `!` 解包直接崩溃
> - 结论：**用 CSV 导入**（UTF-8 with BOM），空值输出为空字符串，金额两位小数

```python
# 生成 CSV 要点
csv.writer(f)  # open('xxx.csv','w',encoding='utf-8-sig')  # BOM 与 BeeCount 一致
w.writerow([t, c, s, f"{float(amt):.2f}", cur, acc, '', '', note, tm, '', ''])
```

## 三、部署（CasaOS）

用户通过 **CasaOS** 部署（compose 由 CasaOS 生成，位于
`/var/lib/casaos/apps/<project>/docker-compose.yml`）：

```yaml
services:
  beecount-cloud:
    image: sunxiao0721/beecount-cloud:latest
    ports: ["8869:8080"]
    restart: unless-stopped
    volumes:
      - type: bind
        source: /DATA/AppData/beecount-cloud/data   # 持久路径（见第五节迁移）
        target: /data
    environment:
      - TZ=Asia/Shanghai
```

也可以用官方 docker-compose（`8869:8080`、`./data:/data`、`JWT_SECRET` 必填）。

## 四、镜像拉取难题（国内网络）

### 问题：Docker Hub 拉取一直失败/卡住

```bash
# dockerd 日志
journalctl -u docker | grep -iE 'pull|error'
# 现象：
# registry-1.docker.io  → context deadline exceeded（被墙）
# 1ms.run 加速器        → TLS handshake timeout / unexpected EOF
# DaoCloud 加速器       → denied: this image is not in the allowlist（白名单拒绝）
```

### 镜像加速器实测（manifest 可用性）

```bash
# 测试加速器能否取到镜像 manifest
curl -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
  "$mirror/v2/sunxiao0721/beecount-cloud/manifests/latest"
# docker.1panel.live → 200 ✅ 可用
# docker.xuanyuan.me → 429（限流）
# docker.m.daocloud.io → 401（白名单外镜像被拒）
```

但免费加速器 **blob 下载严重限速**（36~697 B/s），大镜像几乎不可用。

### 解决方案：SSH 反向隧道 + 本机 Clash 出海

利用 Windows 本机（105）的 Clash 代理，把 103 的流量转发到 105 的 Clash 出海：

```
103:127.0.0.1:17897  ←SSH反向隧道→  105:127.0.0.1:7897 (Clash)
```

**为什么不用 allow-lan？** Windows 防火墙（公用配置 BlockInbound）阻止局域网访问 7897，
且开 allow-lan 有安全风险。SSH 隧道是 105 **主动出站**（SSH 22 放行），天然穿透防火墙。

**隧道实现（paramiko 反向端口转发）：**

```python
import paramiko, socket, threading

cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cli.connect('192.168.0.103', 22, username='syske', password='***')

transport = cli.get_transport()
transport.request_port_forward('127.0.0.1', 17897)  # 在 103 上监听

def pump(src, sink):   # 双向拷贝
    while True:
        data = src.recv(65536)
        if not data: break
        sink.sendall(data)

while True:
    chan = transport.accept(10)   # 103 上的新连接
    if chan:
        dst = socket.create_connection(('127.0.0.1', 7897))  # 转发到 105 的 Clash
        threading.Thread(target=pump, args=(chan, dst), daemon=True).start()
        threading.Thread(target=pump, args=(dst, chan), daemon=True).start()
```

**使用：**

```bash
# 103 上用隧道拉镜像（后台执行）
nohup docker pull docker.1panel.live/sunxiao0721/beecount-cloud:latest &
# 或走隧道直接访问 Docker Hub（curl 验证：HTTP 401 为正常可达）
curl -x http://127.0.0.1:17897 https://registry-1.docker.io/v2/
```

**开机自启（Windows 注册表 Run 键，pythonw 无窗口）：**

```python
import winreg, shutil
pw = shutil.which('pythonw')
cmd = '"%s" "C:/Users/syske/clash_forward.py"' % pw
k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
    r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_WRITE)
winreg.SetValueEx(k, "ClashForwardTunnel", 0, winreg.REG_SZ, cmd)
```

### 隧道对 103 网络的影响（结论）

- **不影响**：隧道只监听 `127.0.0.1:17897`，103 正常流量（Web/DNS/SSH/Docker mirror）全走自身路由（网关 192.168.0.1）与本地 dnsmasq，无任何代理环境变量
- **本机不开隧道**：103 不会断外网；仅失去"经代理访问被墙站点（Docker Hub 直连等）"的能力

## 五、配置修复：数据卷持久化

### 问题：CasaOS 默认把数据卷放在 /tmp

```bash
docker inspect <容器> --format '{{range .Mounts}}{{.Source}}->{{.Destination}}{{end}}'
# /tmp/casaos-compose-app-2779781215/data->/data   ← 危险！/tmp 非持久目录
```

### 修复：迁移到 /DATA/AppData 并重建

```bash
# 1. 停止容器
docker stop <容器>
# 2. 迁移数据
mkdir -p /DATA/AppData/beecount-cloud/data
cp -a /tmp/casaos-compose-app-2779781215/data/. /DATA/AppData/beecount-cloud/data/
# 3. 修改 CasaOS compose 卷路径
sed -i 's|/tmp/casaos-compose-app-2779781215/data|/DATA/AppData/beecount-cloud/data|' \
  /var/lib/casaos/apps/<project>/docker-compose.yml
# 4. 重建
cd /var/lib/casaos/apps/<project> && docker compose up -d
# 5. 清理旧目录 + 验证
rm -rf /tmp/casaos-compose-app-2779781215
curl http://<ip>:8869/healthz   # {"status":"ok"}
```

![Beecount健康检查](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/61102ff6-05a8-4024-aa29-e5037143766d.jpg)

> 📸 **待补充 GUI 截图**：Web 端 Dashboard 报表（见文末截图清单）

> 容器会自动生成 `.jwt_secret`、`.initial_admin_password` 于数据目录，**迁移时务必带上隐藏文件**（`cp -a dir/. dest/`）。

## 六、部署后清单

- [ ] `http://192.168.0.103:8869` 可访问，`/healthz` 返回 ok
- [ ] 首次登录用 `.initial_admin_password` 中的凭据，**登录后修改密码**
- [ ] 数据卷在持久路径（`/DATA/AppData/beecount-cloud/data`），`restart: unless-stopped`
- [ ] App 设置服务器地址指向自建实例，导入 `count-data_导入BeeCount.csv`

> 📸 **待补充 GUI 截图**：App 服务器地址 + CSV 导入界面（见文末截图清单）
- [ ] Web 端 Dashboard 查看报表（月度趋势/分类占比/热力图/Top 排行）

## 七、开源记账软件横向对比（调研）

| 软件 | 类型 | 亮点 | 适合 |
|---|---|---|---|
| BeeCount | 移动 App + 自托管云 | iOS/Android/Web、实时同步、图表全、中文好 | 手机记账 + 私有部署 |
| Firefly III | 自托管 Web | 功能最全、多币种/账单/API、中文好 | 功能党 |
| Actual Budget | 自托管 Web | UI 现代、预算/报表出色、轻量 | 重 UI |
| GnuCash | 桌面 | 复式记账专业级 | 学记账原理 |
| beancount + Fava | 纯文本 | 文本记账 + git 版本控制 + Web 报表 | 极客/数据控 |
| Cashew | 手机 App | 开源、现代 UI、订阅追踪 | 手机记账 |

## 附: 需要手动补充的 GUI 截图

1. **Web 端 Dashboard 报表**:浏览器打开 `http://192.168.0.103:8869` 登录后
   - 截取:首页 Dashboard(月度趋势 / 分类占比 / 热力图)
   - 命名:`beecount-dashboard.png` → 替换文中 `> 📸 待补充 GUI 截图` 占位
2. **App 服务器地址设置**:BeeCount App → 设置 → 服务器地址
   - 命名:`beecount-app-server.png`
3. **App CSV 导入界面**:App → 导入 → 选择 `count-data_导入BeeCount.csv`
   - 命名:`beecount-app-import.png`
4. **CasaOS 应用卡片**(可选):CasaOS 界面中 beecount-cloud 应用图标
