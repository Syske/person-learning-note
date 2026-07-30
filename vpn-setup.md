# VPN 配置说明

## 环境

- 系统: Arch Linux / KDE Plasma (Wayland)
- VPN 协议: Cisco AnyConnect (通过 OpenConnect)
- VPN 分组: sslvpn-corp

## 安装

```bash
sudo pacman -S openconnect expect
```

## 使用

### 连接 VPN

```bash
cool-vpn <密码> <二次验证码>
```

### 断开 VPN

`Ctrl + C` 终止即可。

## 脚本位置

- `~/net-workspace/cool-vpn` — VPN 一键连接脚本
- `/usr/local/bin/cool-vpn` — 脚本软链接

## Chrome 工作配置

由于 Chrome 命名空间沙箱与 VPN 网络接口冲突，需要使用独立配置启动：

```bash
google-chrome-stable --disable-namespace-sandbox --user-data-dir=$HOME/.config/chrome-work
```

或通过桌面快捷方式 **Chrome (工作)** 启动。

## Clash 代理

- 日常上网: 开启 Clash (TUN 模式)
- 上班连 VPN: 关闭 Clash，开启 VPN
- 不同时使用两者，避免路由冲突

## 死机问题修复记录

死机原因: 卸载 ROCm/AMD GPU 用户态包后，kwin_wayland 无法打开 DRM 设备，显示冻结。

优化内容:

- 移除孤包、旧驱动
- 安装 `vulkan-radeon` 驱动
- Cisco VPN 替换为 OpenConnect
- 系统代理配置清理
