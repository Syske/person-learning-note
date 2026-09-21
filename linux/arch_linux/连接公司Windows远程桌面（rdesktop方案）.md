# 连接公司 Windows 远程桌面（rdesktop 方案）

> 归档时间：2026-09-21
> 目标：10.0.0.1（公司内网 Windows），域账号 syske
> 结论：**FreeRDP 3（Remmina/xfreerdp3）与该服务器协议不兼容，改用 rdesktop（NLA）正常**

---

## 一、快速使用

```bash
rdp-company        # 或开始菜单「公司Windows远程桌面」
```

- 密码 + 二次验证在登录界面输入
- 退出全屏：**Ctrl+Alt+Enter**
- 已配置：全屏（1920x1200）、32 位色、剪贴板互通、局域网优化

脚本（~/.local/bin/rdp-company）：
```bash
#!/bin/bash
rdesktop 10.0.0.1 -u syske -a 32 -f -r clipboard:PRIMARYCLIPBOARD -x lan
```

## 二、排查过程（FreeRDP 兼容坑）

### 现象
Remmina 连接报「无法连接」。

### 诊断链
1. `ping` 通、`nc` 测 3389 通、RDP 协商握手正常（X.224 Connection Confirm）
2. Remmina 日志：
   ```
   rdp_client_connect_license: securityFlags=SEC_ENCRYPT, missing required flag SEC_LICENSE_PKT
   CONNECTION_STATE_LICENSING status STATE_RUN_FAILED
   ```
3. xfreerdp3 测试各安全层：
   - `/sec:rdp`（标准加密）→ license 错误（服务器不返回 SEC_LICENSE_PKT）
   - `/sec:nla`（强制 NLA）→ **Protocol Security Negotiation Failure**
   - `+old-license` 参数 → 无效
4. **rdesktop 1.9 走 NLA 成功**（"Connecting to server using NLA..." + "Connection established using plain RDP"）

### 根因
该 Windows 服务器的 RDP 协议协商与 **FreeRDP 3 不兼容**（标准加密的 license 流程 + NLA 协商都失败），老牌 rdesktop 兼容正常。客户端兼容问题，与账号/网络无关。

### 其他尝试
- Remmina security 值：0（RDP）/1（TLS）/2（NLA）都试过，license 错误依旧
- 装 freerdp（3.31）→ xfreerdp3（二进制名 `xfreerdp3`，FreeRDP3 参数有变化：`/cert:ignore`、`/sec:` 语法不同）

## 三、注意事项

1. rdesktop 1.9 已停止维护（2023），功能有限（无 TLS 强加密、无现代性能优化），但 NLA 认证可用
2. 分辨率问题：最初 `-g 1600x900` 窗口操作异常 → 改 **全屏 `-f`** 正常
3. 二次验证（动态码）在 Windows 登录界面输入，rdesktop 只负责第一层认证
4. 445 端口关闭（SMB 被挡）、22 开放——该公司机器常规配置
