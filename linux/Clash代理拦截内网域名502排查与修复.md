# Clash代理拦截内网域名导致502的排查与修复

> 背景：局域网内服务域名 `http://syske.local` 在浏览器访问报 **502 Bad Gateway**，
> 但服务端（Nginx Proxy Manager + 上游服务）一切正常。

## 一、问题现象

- 浏览器访问 `http://syske.local` 提示 502
- 服务端 curl 测试全部 200（连续 15 次）

## 二、排查过程

### 1. 先确认服务端是否正常

```bash
# 服务器本机带 Host 头测试
curl -H 'Host: syske.local' http://127.0.0.1      # HTTP:200
# NPM 代理配置：syske.local -> http://192.168.0.103:83
grep -E 'server_name|proxy_pass' proxy_host/2.conf
# server_name syske.local;
# proxy_pass http://192.168.0.103:83;
# 连续 15 次全部 200，服务器端无问题
```

### 2. 复现"浏览器路径"——代理差异

关键测试：客户端（Windows）分别用**直连**和**走 Clash 代理**访问：

```bash
# 直连（不走代理）：正常
curl --noproxy '*' http://syske.local        # HTTP:200 25ms

# 走 Clash 代理（模拟浏览器）：502！
curl -x http://127.0.0.1:7897 http://syske.local   # HTTP:502 2.7ms
```

![直连vs代理对比](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/b1a17930-0aff-498f-8e97-2b7a951981dc.jpg)

### 3. 根因定位

Windows 系统代理（Clash Verge）的**代理绕过列表**只有 IP 网段：

```
localhost;127.*;192.168.*;10.*;172.16~31.*;<local>
```

`syske.local` 是**域名**，不匹配任何 IP 网段 → 浏览器把请求发给 Clash 代理 →
Clash 按规则转发到外网代理节点 → 节点无法访问内网 → **502**。

## 三、解决方案（双层持久化）

### 1. 立即生效：修改 Windows 系统代理绕过列表

```python
import winreg, ctypes
k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
    r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
    0, winreg.KEY_READ | winreg.KEY_WRITE)
cur, _ = winreg.QueryValueEx(k, "ProxyOverride")
cur = cur.rstrip(';') + ";*.syske.local;*.syske.dev"
winreg.SetValueEx(k, "ProxyOverride", 0, winreg.REG_SZ, cur)

# 刷新 WinINET 让浏览器立即感知
internet_set_option = ctypes.windll.Wininet.InternetSetOptionW
internet_set_option(0, 39, 0, 0)   # INTERNET_OPTION_SETTINGS_CHANGED
internet_set_option(0, 37, 0, 0)   # INTERNET_OPTION_REFRESH
```

> 📸 **待补充 GUI 截图**：Clash Verge 系统代理设置界面（见文末截图清单）

> 注意：`reg add` 在 UNC 路径/特殊字符下易语法错误，用 Python `winreg` 更可靠。

### 2. 持久生效：修改 Clash Verge 配置

Clash Verge 每次应用系统代理时会**覆盖**注册表（`use_default_bypass: true`），
必须改它的配置文件（位于 `%APPDATA%\io.github.clash-verge-rev.clash-verge-rev\`）：

```yaml
# verge.yaml
system_proxy_bypass:
  - localhost
  - 127.*
  - 192.168.*
  - 10.*
  - 172.16.* ~ 172.31.*
  - <local>
  - '*.syske.local'
  - '*.syske.dev'
use_default_bypass: false   # 改用自定义列表
```

同时修改 `clash-verge.yaml`、`config.yaml`、`profiles/Merge.yaml` 三个文件保持一致。

### 3. 重启浏览器生效

浏览器有连接池缓存，需 **Ctrl+F5 或重启浏览器**。

## 四、验证

```bash
# 直连 200（保持不变）
curl --noproxy '*' http://syske.local     # HTTP:200
# 浏览器刷新后正常访问
```

## 五、经验总结

1. **内网域名 502 优先怀疑代理**：本机开着系统代理/Clash 时，内网域名不匹配绕过列表会被转发到外网节点
2. **绕过列表匹配的是域名/网段**：IP 段规则不覆盖域名，内网域名需显式加 `*.xxx.local`
3. **Clash Verge 三层配置**：`verge.yaml`（应用设置）→ `config.yaml`（生成的运行配置）→ `profiles/Merge.yaml`（merge 扩展），持久修改要改模板/Merge，否则下次启动被覆盖
4. **浏览器行为 vs curl**：curl 默认不读系统代理（除非 `-x` 或环境变量），排查时用 `-x http://127.0.0.1:<端口>` 模拟浏览器路径

## 附: 需要手动补充的 GUI 截图

1. **Clash Verge → 设置 → 系统代理** 界面
   - 截取区域:显示"代理绕过"列表或 allow-lan 开关的区域
   - 命名:`clash-verge-bypass.png` → 替换文中 `> 📸 待补充 GUI 截图` 占位
2. **Windows 系统代理设置**(可选):`设置 → 网络 → 代理`,显示手动代理 127.0.0.1:7897 + 绕过列表
