# Arch Linux 新机优化与故障排查（华硕 ExpertBook P3455）

> 归档时间：2026-09-21　最后更新：2026-10-09（新增第 13 节「登录卡顿诊断」，并修正 2.4 的结论）
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
13. [登录卡顿诊断：71 秒黑屏（2026-10-09）](#13-登录卡顿诊断71-秒黑屏2026-10-09)

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

> ⚠️ **2026-10-09 修正**：这三层修复**并不稳定**。同机在 9/21 只花 3 秒，10/9 又回到 32.9 秒（`dev-tpm0.device`）。`systemd.mask=tpm2.target` 只挡住了 `tpm2.target` 这个 target，挡不住 udev 触发的 `dev-tpm0.device` 作业，设备阶段照样被固件 PTT 初始化拖住。治本要在 BIOS 里**禁用 TPM Device**（ASUS：Security → TPM Device → Disable）。详见第 13 节。

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

---

## 13. 登录卡顿诊断：71 秒黑屏（2026-10-09）

### 13.1 症状与定位思路

**症状**：开机输入密码后黑屏/卡死约 **71 秒** 才出桌面。

**定位关键**：不要盯着「登录」本身量，要量**认证成功 → 桌面就绪**这一段。用 `kwin_wayland` 打日志的时刻当锚点（它比 `plasmashell` 早，能定位是 compositor 还是 shell 的问题）：

```bash
journalctl -b -o short-iso | grep -E 'Auth.*successful|Starting KDE Wayland Compositor|No backend specified|plasmashell\['
```

本机两个启动的对比：

| 环节 | 9/21（正常） | 10/9（卡顿） |
|---|---|---|
| 认证成功 → 桌面就绪 | 3s | **71s** |
| kwin 启动耗时 | 0s | **38s** |
| userspace 总耗时 | 2.9s | **34.2s** |

**结论**：慢的不是登录，是 `kwin_wayland` 在 DRM 后端初始化阶段卡了 38 秒。

### 13.2 根因：NVMe 位于 VMD 下，MSI-X 中断不上报

时间线（注意两次 I/O 超时和 kwin 卡顿的对应关系）：

```
10:48:07  认证成功
10:48:08  Starting KDE Wayland Compositor...
10:48:18  ← 之后 28 秒 journal 完全静默（kwin 卡住）
10:48:46  nvme I/O tag timeout  +  kwin "No backend specified"   ← 同一秒
10:48:56  plasma-ksplash.service: start operation timed out
10:49:11  kwin_wayland: Failed to delay sleep: Method call timed out
10:49:18  plasmashell 终于起来
```

kwin 解锁的那一秒**恰好**是一次 NVMe I/O 超时 —— 它是被磁盘 IO 阻塞的。

内核持续刷 `nvme0: I/O tag XXX (cid Y) QID N timeout, completion polled`，本次启动累计 **91 次**，空闲期约每 1~2 分钟一次，成对出现时间隔恰好 30 秒（对应 NVMe `io_timeout` 默认值）。

**决定性证据**（中断计数对照实验）：

```bash
grep nvme /proc/interrupts    # nvme0q0~q16，16 个 CPU 列全是 0
# 连续 dd 800MB (O_DIRECT) 前后 diff /proc/interrupts，无任何设备计数增长
# 对照组：同一时刻 iwlwifi 中断计数正常（19 万+），说明 /proc/interrupts 本身有效
```

NVMe 的完成中断没有被统计/送达，内核只能靠超时后轮询兜底回收 —— 这正是 `completion polled` 的成因。本机 SSD 挂在 **Intel VMD** 后面（ACPI 节点 `RstVmdE` / `RstVmdV`，`vmd 0000:00:0e.0: PCI host bridge to bus 10000:e0`），MSI-X 在 VMD 下丢失是该问题的高发场景。

> 说明：机制层面尚未 100% 证实（也不排除 VMD 路径下的中断计数异常），但**现象本身已实测确认**。

**与负载无关，是关键结论**。70 秒采样窗口内系统近零 I/O（仅 8KB 写入），仍出现了一次超时：

```bash
# 采样各进程 /proc/*/io 增量，找出真正在读盘的进程
for p in /proc/[0-9]*; do awk '/^(read_bytes|write_bytes):/{print}' $p/io 2>/dev/null; done > b.txt
sleep 70
# ... 再采一次 a.txt，对比差值
```

结论：**空闲时也会零星卡顿，负载只是把零星卡顿放大成连续阻塞**。kwin 启动时恰好有一串密集 I/O，于是被 30 秒超时正面命中，就卡住了 38 秒。

> ⚠️ **教训：别用全盘扫描去排查全盘扫描类问题**。本次 `pacman -Qkk` 全量校验跑了 50 分钟、读了 3.5GB，本身就制造了大量超时 —— 排查期间的 45 次超时里有一半是自己造成的。要区分「故障导致 IO」还是「IO 导致故障」，必须先看**空闲基线**。

**SSD 硬件已排除嫌疑**（`nvme-cli` 实测）：

| 指标 | 值 | 判读 |
|---|---|---|
| 型号 | WD PC SN5000S SDEQNSJ-512G-1102 (fw 34430100) | — |
| `critical_warning` / `media_errors` | 0 / 0 | 健康 |
| `percentage_used` / 通电时长 | 0% / **6 小时** | 几乎全新 |
| 错误日志 64 条 | 全部 `Successful Completion`，`error_count=0` | 空条目，无真实错误 |
| **`unsafe_shutdowns`** | **30** | ⚠️ 6 小时的盘被强制断电 30 次 |

盘没坏，**所以 30 秒 I/O 超时不是硬件故障**，而是 VMD/MSI-X 层的软件问题；30 次强制断电很可能让控制器长期处在异常状态。后续可尝试：升级 SSD 固件、关 APST（`nvme_core.default_ps=0`，代价是略增功耗）、或向上游报 VMD 的 bug。

### 13.3 附带发现：系统目录属主被损坏（非正常关机所致）

pacman 自己和 systemd 都报了警：

```
[ALPM] warning: directory permissions differ on /usr/, filesystem: 775  package: 755
[systemd-tmpfiles] Detected unsafe path transition / (owned by syske) → /var (owned by root)
```

EFI 分区同次开机报 `FAT-fs (nvme0n1p1): Volume was not properly unmounted.`

> ⚠️ **排查时踩过的坑：`find -perm` 统计会严重高估损坏范围。**
> 第一次扫出「45428 个 group/other 可写条目」，看起来是灾难性损坏。但用
> `bsdtar -tvf /var/cache/pacman/pkg/<pkg>.pkg.tar.zst` 核对后才发现：
> 那些**绝大多数是符号链接** —— Linux 上符号链接的模式位恒为 `lrwxrwxrwx`（777）且无实际意义。
> 更危险的是 `chmod go-w` **会跟随符号链接去改目标文件**的权限，好在执行前发现避免了。
>
> 同理 `/usr/sbin`、`/usr/lib64` 显示 777 也只是因为它们是 symlink，**不需要修**。
>
> 判定原则：**权限是否异常，以包归档和 pacman 数据库为准，不要以 `find` 的模式位为准。**

修正后的真实损坏范围（已修复）：

```bash
# 定点修复，只有 4 个系统路径需要动
sudo chown root:root / /usr /usr/share
sudo chmod 755        / /usr /usr/share
sudo chown -R root:root /usr/share/icons /usr/share/applications
```

验证（`0 altered files` 即完全一致）：

```bash
pacman -Qkk <pkg>
```

| 包 | 结果 |
|---|---|
| bash / plasma-workspace / qt6-base / fcitx5 | 0 altered files |
| systemd | 1 altered：`/var/log/journal` GID 差异 |

`/var/log/journal` 是 `root:systemd-journal 2755`（journald 运行时创建的 setgid 目录），**属正常，非损坏**，忽略。

**EFI 分区 dirty bit 修复**（必须先卸载）：

```bash
sudo umount /boot
sudo fsck.fat -a /dev/nvme0n1p1    # 输出 *** Filesystem was changed ***
sudo mount /boot
```

> 修复后**不要**用挂载态去验证 dirty bit —— 内核在挂载期间会再次置位，必然误报"未修复"。以 `fsck` 输出为准。

**不要动 `/opt`**：`/opt/apps`（494 个条目，小鱼易连 / 企业微信）、`/opt/Obsidian`、`/opt/idea-oss` 等属主是 `syske`/`root` 且带 775/664，那是**用户自己安装的应用数据**，不是损坏。`chown -R /opt` 会破坏它们的写权限。

### 13.4 次要问题

- **TPM 等待 32.9s 回归**：见 2.4 的修正说明，`systemd.mask=` 不够，需 BIOS 禁用 TPM Device。
- **i915 GSC 绑定超时**：`GT1: GSC proxy component didn't bind within the expected timeout`，与 kwin 启动慢同源（都卡在等硬件就绪）。
- **登录时连续 3 次密码错误**，每次约 2s，白等 8s —— 排查卡顿时别把这部分算进去。
- **内核版本错位**：运行 7.2.6 但已装 7.2.9 + systemd 262，重启后才生效，测性能前务必先重启。

### 13.5 本次处理结果与后续

**已完成**

- [x] `/`、`/usr`、`/usr/share`、`/usr/share/icons`、`/usr/share/applications` 属主/权限修复，`pacman -Qkk` 验证 0 altered
- [x] EFI 分区 `/dev/nvme0n1p1` dirty bit 修复（卸载后 `fsck.fat -a`）
- [x] 安装 `nvme-cli`、`dosfstools`，确认 SSD 硬件健康
- [x] 确认 NVMe 挂在 Intel VMD 下，MSI-X 中断不上报为软件层问题

**待重启验证（关键）**

当前运行的是 7.2.6 内核 + systemd 261，但已安装 **7.2.9 + systemd 262**。重启后重测：

```bash
systemd-analyze
journalctl -b -o short-iso | grep -E 'Auth.*successful|Starting KDE Wayland Compositor|plasmashell\['
journalctl -b -k | grep -c 'I/O tag'     # 应显著下降
systemctl is-enabled tpm2.target          # masked-runtime
```

**若重启后仍慢**，按此顺序处理：

1. **BIOS 禁用 TPM Device**（ASUS：Security → TPM Device → Disable）—— 治本，消除 32 秒等待
2. **NVMe**：升级 WD SN5000S 固件（当前 `34430100`），或加内核参数 `nvme_core.default_ps=0` 关闭 APST 后对比
3. 若 I/O timeout 仍复现，考虑 `linux-lts` 内核对照测试，或向上游报 VMD MSI-X 问题

**操作建议**：这台盘通电 6 小时却已被强制断电 30 次（`unsafe_shutdowns: 30`）。务必用 `reboot` 正常重启，别直接断电；长期看考虑给内目录开启自动安全关机。

### 13.6 排查这类问题的通用手法

```bash
# 1. 先切分「登录前 / 登录后」两段，别只看开机总时长
systemd-analyze                      # userspace 总耗时
systemd-analyze blame | head -20     # 谁在等，看时间戳是否整齐
systemd-analyze critical-chain graphical.target   # 看 critical-chain 末端那个 30s 空洞

# 2. journal 里找「静默空洞」——卡住时不会有任何日志
journalctl -b -o short-iso | awk '$1>="T1" && $1<="T2"'

# 3. 硬件就绪类卡顿：数中断是否为 0（比看错误日志更直接）
grep -E '<你的设备>' /proc/interrupts

# 4. 判断文件权限是否异常，以包归档为准，不要只看 find 的模式位
bsdtar -tvf /var/cache/pacman/pkg/<pkg>-*.pkg.tar.zst | head    # 归档里的应有权限
pacman -Qo <文件>                                                # 归属哪个包
pacman -Qkk <pkg>                                                # 0 altered = 完全一致
stat -c '%F' <路径>                                              # 先看是不是符号链接
```

**五条避坑经验**

1. **符号链接的模式位恒为 777 且无意义**。用 `find -perm` 统计损坏范围会严重高估，且 `chmod` 会跟随链接改到目标文件上。判定前先 `stat -c '%F'` 确认类型。
2. **别把用户数据当损坏**。`/opt` 下自装的应用（属主 `syske`、775/664）是正常状态，`chown -R /opt` 反而破坏它。
3. **"看起来像故障"的现象要先排除误报**。`pacman -Qkk` 报的 `/var/log/journal` GID 差异就是 journald 的正常 setgid 目录，不是问题。
4. **排查动作本身会污染数据**。全盘校验/扫描会产生与故障同signature 的日志，必须先取空闲基线再下结论。
5. **改权限前先确认脚本带上了 root**。本次误用 `sh`（非 `sudo bash`）跑修复脚本，好在上千条 `Operation not permitted` 全部失败，等于没执行 —— **权限不足的批量失败反而是安全网**，反倒是"半成功"最危险。

**经验**：「卡顿」类问题的定位锚点选**带时间戳的关键字**（如 `No backend specified`、`Starting KDE Wayland Compositor`），比看总耗时有效得多；静默的 28 秒往往比刷屏的日志更能说明问题。
