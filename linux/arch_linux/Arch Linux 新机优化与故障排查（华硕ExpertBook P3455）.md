# Arch Linux 新机优化与故障排查（华硕 ExpertBook P3455）

> 归档时间：2026-09-21
> 环境：Arch Linux（滚动版）/ KDE Plasma 6.7.5（Wayland）/ 华硕 ExpertBook P3455 / Intel Core Ultra 200H + Intel iGPU / 30G 内存
> 相关历史笔记：[输入法配置（Fcitx5 + Rime 雾凇拼音）](./Arch%20Linux%20输入法配置（Fcitx5%20%2B%20Rime%20雾凇拼音）.md)、[磁盘空间清理与优化](./Arch%20Linux%20磁盘空间清理与优化.md)

---

## 目录

1. [中文输入法（fcitx5 + Rime 雾凇）](#1-中文输入法fcitx5--rime-雾凇)
2. [启动优化：63s → 12.5s](#2-启动优化63s--125s)
3. [声卡无输出（SOF 固件缺失）](#3-声卡无输出sof-固件缺失)
4. [时区 / 语言 / 时间同步](#4-时区--语言--时间同步)
5. [钉钉投屏（Wayland 架构变化）](#5-钉钉投屏wayland-架构变化)
6. [AUR 实战经验（避坑合集）](#6-aur-实战经验避坑合集)
7. [系统清理（KDE 自带应用）](#7-系统清理kde-自带应用)
8. [应用故障排查（Chrome / Clash）](#8-应用故障排查chrome--clash)
9. [Java 后端开发环境](#9-java-后端开发环境)
10. [性能与电源优化清单](#10-性能与电源优化清单)
11. [Git 双身份（按目录自动切换）](#11-git-双身份按目录自动切换)
12. [关键配置与命令速查](#12-关键配置与命令速查)

---

## 1. 中文输入法（fcitx5 + Rime 雾凇）

### 1.1 本次部署流程

基础配置见[历史笔记](。本次采用 plum 方式安装雾凇（比 AUR 包更可控、便于更新）：

```bash
sudo pacman -S fcitx5 fcitx5-rime librime git
# 环境变量（全局）
sudo tee /etc/environment.d/im.conf <<'EOF'
GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS=@im=fcitx
SDL_IM_MODULE=fcitx
EOF
# 开机自启
mkdir -p ~/.config/autostart
cp /usr/share/applications/org.fcitx.Fcitx5.desktop ~/.config/autostart/
# KWin 虚拟键盘（Wayland 原生 text-input 通道）
kwriteconfig6 --file kwinrc --group Wayland --key InputMethod org.fcitx.Fcitx5.desktop
# plum 安装雾凇
git clone --depth=1 https://github.com/rime/plum.git ~/plum
cd ~/plum && rime_dir="$HOME/.local/share/fcitx5/rime" bash rime-install iDvel/rime-ice
```

### 1.2 关键坑：fcitx5 退出时会用内存配置覆盖 profile 文件

**现象**：手动改了 `~/.config/fcitx5/profile` 添加 Rime，重启 fcitx5 后 Rime 消失。

**根因**：fcitx5 在运行中持有配置，`pkill` 退出时把内存中的旧配置**写回文件**，覆盖外部修改。

**解决**：先 `pkill fcitx5` 停进程 → **再改** profile → 再启动。

### 1.3 语法模型（wanxiang 401MB）导致登录卡顿 43 秒 → 已移除

**现象**：登录认证后 fcitx5 要 43 秒才就绪，桌面整体卡顿。

**根因**：Rime 万象语法模型（`wanxiang-lts-zh-hans.gram`，401MB）每次登录时被加载/部署，与 plasmashell 竞争 IO。

**解决**（可逆，需要时重装）：
```bash
rm ~/.local/share/fcitx5/rime/wanxiang-lts-zh-hans.gram
rm ~/.local/share/fcitx5/rime/rime_ice.custom.yaml   # 该文件只是 grammar 补丁
fcitx5-remote -r   # 重新部署
```
移除后登录 3 秒内输入法就绪，词库（17 个方案）不受影响。重装语法模型命令：`cd ~/plum && rime_dir="$HOME/.local/share/fcitx5/rime" bash rime-install iDvel/rime-ice:others/recipes/grammar:schema=rime_ice`

---

## 2. 启动优化：63s → 12.5s

### 2.1 症状

开机 `systemd-analyze` 显示 userspace 63 秒；且**每次重启时间波动**（16s / 46s / 63s 反复横跳）。

### 2.2 根因：TPM 设备等待（Intel PTT 固件初始化慢）

- `systemd-analyze blame` 显示 `dev-tpm0.device` 等待 **31.9s**（连带 ttyS0-3、configfs、fuse 等 device unit 全部 31s——整个 udev 设备阶段被拖住）
- 根因链：系统内置 `tpm_crb` 驱动（`modules.builtin` 里有它，**无法 blacklist**）→ 固件 TPM（Intel PTT，ACPI 节点 `MSFT0101`）**每次开机初始化速度波动**（快 2s、慢 32s）→ systemd 的 `tpm2.target` 等 TPM 设备就绪 → 干等 32s
- 第一次尝试 `modprobe tpm_crb` + mkinitcpio MODULES 无效：tpm_crb 是 **built-in**（initramfs 里根本没有该 .ko，也无需打包）

### 2.3 修复链（三层，缺一不可）

```bash
# ① 主系统：屏蔽 tpm2.target（无 LUKS 加密盘时可安全屏蔽）
sudo systemctl mask tpm2.target

# ② initramfs：initrd 里的 systemd 看不到 /etc 的 mask，需内核参数（对 initrd + 主系统都生效）
sudo sed -i 's/^GRUB_CMDLINE_LINUX=""/GRUB_CMDLINE_LINUX="systemd.mask=tpm2.target"/' /etc/default/grub
sudo grub-mkconfig -o /boot/grub/grub.cfg

# ③ GRUB 倒计时 5s → 1s
sudo sed -i 's/^GRUB_TIMEOUT=5/GRUB_TIMEOUT=1/' /etc/default/grub
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

> 注意：`systemd.mask=` 内核参数是 initrd 阶段的关键，只 mask 主系统（`/etc/systemd/system/tpm2.target → /dev/null`）时 initrd 里的 systemd 依然会等 TPM 31s。

### 2.4 结果

| 阶段 | 优化前 | 优化后 |
|---|---|---|
| 固件 + GRUB | 7.6s | 7.7s |
| initrd（TPM 卡点） | 31.2s | **1.6s** |
| userspace | 63s | **2.9s** |
| **总计** | **103s** | **12.5s** |

剩余 6s 固件自检只能通过 BIOS（开机按 F2 → Boot → **Fast Boot** 开启）再省 4-5s。

---

## 3. 声卡无输出（SOF 固件缺失）

**症状**：`pactl info` 的 Default Sink 是 `auto_null`（无真实输出设备），没声音。

**根因**：Core Ultra 200H（Arrow Lake）的 HD Audio 走 SOF（Sound Open Firmware），但 `sof-firmware` 未安装，内核报 `SOF firmware and/or topology file not found`。

**解决**：
```bash
sudo pacman -S sof-firmware   # 装完需重启，声卡才被探测
```

---

## 4. 时区 / 语言 / 时间同步

```bash
# 时区（中国）
sudo timedatectl set-timezone Asia/Shanghai
# 网络时间同步
sudo timedatectl set-ntp true
# 生成中文 locale
sudo sed -i 's/^#zh_CN.UTF-8/zh_CN.UTF-8/' /etc/locale.gen && sudo locale-gen
sudo localectl set-locale LANG=zh_CN.UTF-8
```

**坑**：本机最初 `LANG=C.UTF-8` 且无 zh locale；KDE 时钟显示不对是系统时区为 UTC 导致，与字体无关。

---

## 5. 钉钉投屏（Wayland 架构变化）

### 5.1 结论：钉钉 Linux 在 Wayland 下投屏目前无解

- 旧版钉钉（≤7.x）用 **X11 XShm API** 抓屏 → 社区 hook（`yatli/dingtalk-wayland-screencast`、`cagedbird043/dingtalk-wayland-screenshare`，均通过 LD_PRELOAD 拦截 XShm 并从 Portal/PipeWire 注入帧）可以救
- **钉钉 8.2.8 的投屏组件 `libscreencast.so` 改用 DRM/GBM 直连抓屏**（实测库内无 XShm 符号，只有 drm/gbm）→ hook 拦不到；Wayland 下 DRM master 被 KWin 占用 → 点投屏按钮无反应
- 钉钉网页版（`im.dingtalk.com`）**已官方停用**（"系统维护中"是永久引导页，阿里云社区确认）；`meeting.dingtalk.com` 只有"加入会议"入口没有发起功能

### 5.2 兜底方案：X11 会话

```bash
# Plasma 6.7+ X11 会话是独立包（原 plasma-workspace-x11 已改名）
sudo pacman -S plasma-x11-session
```
登录界面（SDDM）选择 **Plasma (X11)** 会话 → 普通钉钉投屏正常。输入法环境变量/自启已全局配置，X11 下同样可用。

> 若不想注销切会话，可考虑换腾讯会议（wemeet 新版原生支持 Wayland 投屏）——前提是团队接受。

---

## 6. AUR 实战经验（避坑合集）

### 6.1 pacman 事务中止机制（重要）

**`pacman -Rns pkg1 pkg2 ...` 只要有一个包不存在，整个事务直接中止，一个都不卸**（不跳过）。批量卸载/安装前务必逐个 `pacman -Q <pkg>` 确认存在。

### 6.2 paru-bin 与 libalpm 版本不匹配

预编译 AUR helper（paru-bin 等）链接特定版本 libalpm，与本机 pacman 的 `libalpm.so.16` 不匹配会报 `libalpm.so.15: cannot open shared object file`。解决：**不用 AUR helper**，直接 `git clone AUR 包 → makepkg → sudo pacman -U` 手动流程（已验证可靠）。

### 6.3 gtk2 已从官方仓库下架

`dingtalk-bin` 的 PKGBUILD 依赖 gtk2（已移除），需本地修改 PKGBUILD 去掉 gtk2 再构建（钉钉是 Electron 应用，运行时不需要 gtk2）。

### 6.4 makepkg 构建时依赖安装的 sudo 问题

`makepkg -s` 会自动调 sudo 装依赖，在非交互环境会卡住。正确做法：**先手动 `sudo pacman -S` 装齐 depends，再用不带 `-s` 的 `makepkg --noconfirm`**。

### 6.5 mycli 依赖在官方仓库有缺口 → 用 pipx

`mycli` 的 AUR depends（python-clickdc 等）在官方仓库缺失。改用 **pipx 隔离安装**：
```bash
sudo pacman -S python-pipx
PIP_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple" pipx install mycli
```

### 6.6 IDEA 下载架构错误 + 代理加速

- JetBrains 多架构发布后，文件名区分架构：`idea-2026.2.3.tar.gz`（x86_64）vs `idea-2026.2.3-aarch64.tar.gz`（ARM）。本机是 x86_64，下 aarch64 会**解压出来也无法运行**
- 大文件走代理下载（Clash）：`curl -L -x http://127.0.0.1:7897 -C - -o file "url"`

---

## 7. 系统清理（KDE 自带应用）

- KDE 自带大量应用（几十个小游戏、教育软件、PIM 套件、媒体工具）对办公机无用
- 卸载用 `sudo pacman -Rns <包列表>`，注意：
  - 先检查 `Required By`，确认没有核心包依赖要卸的包
  - 分组卸载，每组后验证核心组件（plasma-workspace/kwin/dolphin/konsole/fcitx5）完好
  - `pacman -Rns` 会递归清理不再被依赖的依赖库，结束时 `pacman -Qdt` 应为 0 孤儿
- 保留的系统组件：dolphin/konsole/kate/ark/gwenview/discover/okular/spectacle/systemsettings/kmix/ksystemlog/kcalc 等
- `v4l-utils` 被 ffmpeg/gstreamer 依赖，**不能卸**（会破坏媒体栈）

---

## 8. 应用故障排查（Chrome / Clash）

### 8.1 Chrome "打不开" = 僵尸实例

**现象**：点图标没反应。**真相**：Chrome 进程还活着（PID 在），但窗口"僵尸化"（看不见点不动），新实例只转发请求给旧实例。

**解决**：
```bash
pkill -x chrome        # 注意用 -x 精确匹配，pkill -f 会误杀命令行含该串的进程（包括执行命令的 shell！）
rm -f ~/.config/google-chrome/Singleton*
nohup google-chrome-stable &
```

### 8.2 Clash Verge 启动慢 + 弹更新提示

**根因**：`verge.yaml` 里 `auto_check_update: true`，每次启动都去 GitHub 静默下载新版（Silent updater），代理未起时直连很慢。

**解决**：`~/.local/share/io.github.clash-verge-rev.clash-verge-rev/verge.yaml` 改 `auto_check_update: false`，需要升级时在设置里手动检查更新。

---

## 9. Java 后端开发环境

```bash
sudo pacman -S jdk8-openjdk maven        # 公司要求 JDK8
# 固化 JAVA_HOME（/etc/environment.d/java.conf）
echo 'JAVA_HOME=/usr/lib/jvm/java-8-openjdk' | sudo tee /etc/environment.d/java.conf
# IDEA Community（手动 AUR 或 GitHub release 解压到 /opt，/usr/local/bin/idea -> bin/idea.sh）
# mycli 见 6.5
```
- `archlinux-java status` 确认默认 JDK（本机唯一 JDK8，默认）
- Maven 跑在 JDK8 上：`mvn -version` 显示 Java 1.8.0_504

---

## 10. 性能与电源优化清单

```bash
# A. TLP 电源管理（笔记本续航 +20-30%）
sudo pacman -S tlp && sudo systemctl enable --now tlp

# B. swappiness 60→10（内存 30G，减少 swap 写 SSD）
sudo sysctl -w vm.swappiness=10
echo 'vm.swappiness=10' | sudo tee /etc/sysctl.d/99-swappiness.conf

# C. ufw 防火墙（默认：拒绝入站/允许出站）
sudo pacman -S ufw && sudo systemctl enable --now ufw && sudo ufw enable

# D. pacman 缓存定时清理（paccache 保留最近 3 版）
sudo systemctl enable --now paccache.timer

# E. journald 日志限 200M
echo 'SystemMaxUse=200M' | sudo tee -a /etc/systemd/journald.conf
sudo systemctl restart systemd-journald

# F. baloo 索引排除大目录（~/.config/baloofilerc）
# [Excluded Folders] 下写 /home/syske/Downloads=true 等，改后 balooctl6 enable 重启索引
```

---

## 11. Git 双身份（按目录自动切换）

公司电脑默认公司身份，个别私人仓库自动用私人身份（`includeIf` 按目录匹配，**仅在 git 仓库内生效**）：

```bash
# 全局 = 公司
git config --global user.name "syske"
git config --global user.email "syske@company.com"

# 私人身份文件
cat > ~/.gitconfig-personal <<'EOF'
[user]
    name = syske
    email = 715448004@qq.com
EOF

# 按目录匹配私人仓库（每个仓库一条）
git config --global --add includeIf."gitdir:~/workspace/ai-system/".path ~/.gitconfig-personal
git config --global --add includeIf."gitdir:~/workspace/person-learning-note/".path ~/.gitconfig-personal
```

验证（必须在仓库内）：`cd ~/workspace/ai-system && git config user.name` → syske。

---

## 12. 关键配置与命令速查

| 用途 | 路径/命令 |
|---|---|
| 输入法环境变量 | `/etc/environment.d/im.conf` |
| JAVA_HOME | `/etc/environment.d/java.conf` |
| KWin 虚拟键盘 | `kreadconfig6 --file kwinrc --group Wayland --key InputMethod` |
| 输入法自启 | `~/.config/autostart/org.fcitx.Fcitx5.desktop` |
| 启动耗时诊断 | `systemd-analyze` / `systemd-analyze blame` / `systemd-analyze critical-chain graphical.target` |
| 登录时刻 | `journalctl -b \| grep -E 'sddm.*Authentication\|fcitx5.*Starting'`；`ps -o lstart= -p <pid>` |
| 卸载前依赖检查 | `pacman -Qi <pkg> \| grep 'Required By'` |
| 孤儿包检查 | `pacman -Qdt` |
| Clash 配置目录 | `~/.local/share/io.github.clash-verge-rev.clash-verge-rev/` |
| SSH 代理（GitHub 加速可选） | `~/.ssh/config`: `Host github.com` → `ProxyCommand nc -X connect -x 127.0.0.1:7897 %h %p` |
