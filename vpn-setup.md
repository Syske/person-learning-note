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

## 脚本

### cool-vpn

一键连接 VPN，自动填入密码和二次验证码。

位置: `~/net-workspace/cool-vpn` → `/usr/local/bin/cool-vpn`

内容:

```bash
#!/bin/bash
VPN_SERVER="vpn.beisen-inc.com"
VPN_GROUP="sslvpn-corp"
USERNAME="<域账号>"
PASSWORD="$1"
OTP_CODE="$2"

if [ -z "$PASSWORD" ] || [ -z "$OTP_CODE" ]; then
  echo "用法: $0 <VPN密码> <二次验证码>"
  echo "示例: $0 mypassword 123456"
  exit 1
fi

expect << EOF
set timeout -1
spawn sudo openconnect --protocol=anyconnect --user=\$USERNAME --authgroup=\$VPN_GROUP \$VPN_SERVER
expect -re {[Pp]ass(word|W)[:：]?}
send "\$PASSWORD\r"
sleep 3
send "\$OTP_CODE\r"
expect eof
EOF
```

### cool-chrome

启动独立配置的 Chrome，绕过命名空间沙箱以支持 VPN 内网访问。

位置: `~/net-workspace/cool-chrome`

内容:

```bash
#!/bin/bash
exec google-chrome-stable --disable-namespace-sandbox --user-data-dir="$HOME/.config/chrome-work" "$@"
```

Chrome 配置目录: `~/.config/chrome-work`

## Clash 代理

- 日常上网: 开启 Clash (TUN 模式)
- 上班连 VPN: 关闭 Clash，开启 VPN
- 不同时使用两者，避免路由冲突
