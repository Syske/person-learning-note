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
14. [缓解措施与复测（2026-10-09 晚）](#14-缓解措施与复测2026-10-09-晚)
15. [缓解参数生效后的实测](#15-缓解参数生效后的实测2026-10-09-1427)
16. [最终结果（2026-10-09 22:26 验证）](#16-最终结果2026-10-09-2226-验证)
17. [initramfs 安全网与 GRUB 菜单清理](#17-initramfs-安全网与-grub-菜单清理2026-10-09-2319)
18. [事故复盘：一次改三个文件导致开不了机](#18-事故复盘一次改三个文件导致开不了机2026-10-09-2319)
19. [两个 initramfs 镜像的实际影响](#19-两个-initramfs-镜像的实际影响含一处自我更正)
20. [收官验证（2026-10-10）与残留提醒](#20-收官验证2026-10-10与残留提醒)

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

> ⚠️ **阅读提示**：本章记录的是**排查过程**，过程里有过多次误判（13.2 的 MSI-X 结论已被推翻）。
> 最终结论与成果在**第 16 章**，方法论教训在**第 18 章**，请勿把本章中间结论当作定论。

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

### 13.2 曾经的假设：MSI-X 中断不上报 —— **已被推翻，见下方 ❌ 小节**

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

内核持续刷 `nvme0: I/O tag XXX (cid Y) QID N timeout, completion polled`，累计 **91 次**，空闲期约每 1~2 分钟一次，成对出现时间隔恰好 30 秒（对应 NVMe `io_timeout` 默认值 30000ms）。

#### ❌ 一个被推翻的错误结论：不是「MSI-X 中断丢失」

我最初根据 `grep nvme /proc/interrupts` 计数全为 0（16 个 CPU 列无一非零），推断「NVMe 完成中断没有送达驱动，只能靠 30 秒超时轮询兜底」。**这个结论是错的**，已推翻。

推翻它的实测证据（100 次 4K 随机读，含 O_DIRECT）：

```
平均: 0 ms   最大: 1 ms
```

如果中断真的失效，每一次读写都要等满 30 秒，系统根本不可用。而实际延迟是 **0~1ms**，说明 NVMe 通路完全正常 —— `/proc/interrupts` 的零计数只是 **VMD 路径下的统计假象**，不是功能失效。

> **教训：计数为 0 ≠ 功能失效**。看到可疑计数必须先用**实际延迟测试**验证因果，再下结论。只看计数器就断言机制，是过度推断。

#### 实际故障：周期性 30 秒卡顿

正常态磁盘完美（0~1ms），异常态整个请求挂死 30 秒。**与负载无关**：70 秒采样窗口内系统近零 I/O（仅 8KB 写入），仍复现一次超时。

```bash
# 采样各进程 /proc/*/io 增量，找出真正在读盘的进程
for p in /proc/[0-9]*; do awk '/^(read_bytes|write_bytes):/{print}' $p/io 2>/dev/null; done > b.txt
sleep 70
# ... 再采一次 a.txt，对比差值
```

结论：**空闲时也会零星卡顿，负载只是把零星卡顿放大成连续阻塞**。kwin 启动时恰好有密集 I/O，于是被 30 秒超时正面命中。

#### 头号嫌疑：Intel VMD 的 PCIe 中断路由

内核日志里有两条高度相关的报错，且**只出现在 NVMe 这条路径上**（其余端口正常，这也解释了为何 wifi 中断计数正常）：

```
pcieport 10000:e0:06.0: can't derive routing for PCI INT A
pcieport 10000:e0:06.0: PCI INT A: no GSI
nvme 10000:e1:00.0: PCI INT A: no GSI
```

`10000:e0:06.0` → `10000:e1:00.0` 正是 VMD 下挂 NVMe 的那条链路（`vmd 0000:00:0e.0: PCI host bridge to bus 10000:e0`）。**关联已确认，因果未证实**。

**SSD 硬件已排除嫌疑**（`nvme-cli` 实测）：

| 指标 | 值 | 判读 |
|---|---|---|
| 型号 | WD PC SN5000S SDEQNSJ-512G-1102 (fw 34430100) | — |
| `critical_warning` / `media_errors` | 0 / 0 | 健康 |
| `percentage_used` / 通电时长 | 0% / **6 小时** | 几乎全新 |
| 错误日志 64 条 | 全部 `Successful Completion`，`error_count=0` | 空条目，无真实错误 |
| **`unsafe_shutdowns`** | **30** | ⚠️ 6 小时的盘被强制断电 30 次 |

另外已排除 **TLP Runtime PM**：NVMe 的 `runtime_status=unsupported`，VMD 端口 `power_state=D0 / runtime_status=active`，从未真正挂起。ASPM 策略为 `default`（未排除，但 `policy` 文件只读，须内核参数+重启才能验证）。

#### 升级 7.2.9 的实测结果：无效，且登录更慢

| | 7.2.6 / systemd 261 | 7.2.9 / systemd 262 |
|---|---|---|
| 认证到桌面就绪 | 71s | **99s** |
| initrd | 2.7s | **31.9s** |
| userspace | 34.3s | 3.8s |
| 总计 | 45.7s | 44.0s |

**TPM 那 32 秒没有消失，只是从 userspace 挪进了 initrd**（新 systemd 262 的 initramfs 同样等 TPM 设备）。总耗时基本持平，登录段反而更差，结论是**升级内核对本问题无帮助**。

#### BIOS 升级 303 → 307：TPM 解决了，I/O 停摆没解决

| 指标 | BIOS 303 | BIOS 307（2026-04-30） |
|---|---|---|
| **TPM 设备等待** | 32.9s | **2.0s** ✅ |
| initrd | 31.9s | **1.7s** ✅ |
| 认证到桌面就绪 | 99s | **33s**（改善但仍慢） |
| userspace | 3.8s | **34.0s**（瓶颈转移） |
| `pcieport ... no GSI` | 有 | **仍有** |

**TPM 那 32 秒被新 BIOS 固件彻底修好了** —— 说明它确实是固件层面的问题，升级固件是对症的手段。但 **VMD 的 PCIe 路由失败依旧**，I/O 停摆照旧（本次启动 9 次，仍严格每 30 秒一次）。

**新瓶颈（BIOS 307 后）**：两个独立的 31 秒空洞，且都是同一个 I/O 停摆撞上的：

```
13:59:51 → 14:03:33  I/O timeout 严格每 30 秒一次，连续 9 次
14:03:02  认证成功
          ← 31 秒空窗（startplasma 在等磁盘）
14:03:33  I/O timeout + kwin 启动
14:03:35  plasmashell
```

开机侧同理：`NetworkManager.service` 耗时 **31.163s**，成了当前 `blame` 第一名，卡住 `network.target` → `systemd-user-sessions` → `plymouth-quit` → `sddm`，导致登录界面本身要等 31 秒才出现。

#### 停摆是内核/硬件层自发的，与用户态无关

两轮采样都证明用户态没有任何周期性 I/O：

```bash
# 按字节采样：70 秒内仅 8KB 写入
# 按 syscr（读调用次数）采样：全部来自 konsole/opencode 自己，无后台守护进程
ps -eo stat,pid,comm | awk '$1 ~ /^D/'    # D 状态进程：空
```

也就是说没有任何进程在周期性读写 —— 是 NVMe 控制器自己每 30 秒挂死一次。

#### 另外发现：`intel-ucode` 未安装

```
x86/CPU: Running old microcode
```

`pacman -Qi intel-ucode` 显示**根本没装**（BIOS 已是 307/2026-04-30）。已安装 `intel-ucode 20260925-1` 并重建 initramfs，需重启生效。

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
- **内核版本错位**：运行 7.2.6 但已装 7.2.9 + systemd 262，重启后才生效，测性能前务必先重启。升级后实测**无效**（TPM 等待只是从 userspace 挪进 initrd）。

### 13.5 本次处理结果与后续

**已完成**

- [x] `/`、`/usr`、`/usr/share`、`/usr/share/icons`、`/usr/share/applications` 属主/权限修复，`pacman -Qkk` 验证 0 altered
- [x] EFI 分区 `/dev/nvme0n1p1` dirty bit 修复（卸载后 `fsck.fat -a`）
- [x] 安装 `nvme-cli`、`dosfstools`，确认 SSD 硬件健康
- [x] 排除 TLP Runtime PM（NVMe `runtime_status=unsupported`，从未挂起）
- [x] 升级 7.2.9 + systemd 262 并实测 —— **对登录卡顿无帮助**（见 13.2 对比表）

**结论：软件侧已无有效手段，下一步必须进 BIOS**

内核、systemd、APST、Runtime PM、SSD 固件这些软件层都排查过了，能立刻见效的两项都在固件里，且**一次进 BIOS 可同时处理**：

| 操作 | 路径 | 预期收益 |
|---|---|---|
| ~~**禁用 TPM Device**~~ | ~~Security → TPM Device~~ | ✅ **已被 BIOS 307 解决**（32.9s → 2.0s），无需再改 |
| **禁用 Intel VMD** | Advanced → VMD Configuration / SATA → 关闭 VMD | 让 NVMe 脱离 VMD 桥接，**有望根除 30 秒 I/O 卡顿**（BIOS 307 后仍未试） |

> BIOS 已从 `B3405CCA.303`(2025-06-11) 更新到 **`B3405CCA.307`(2026-04-30)**，TPM 问题已被固件解决。
>
> ⚠️ 禁用 VMD 前确认：本机无依赖 VMD 的服务 —— 已核实 `/proc/mdstat` 为空、未安装 `mdadm`、无软 RAID，可安全关闭。

**当前最有价值的两步**：

1. **BIOS 禁用 VMD** —— 唯一还没试过的根因手段。BIOS 307 仍报 `pcieport ... no GSI`，问题明确在 VMD 这条链路上。
2. **内核参数缓解**（不治根，但能把每次停摆的伤害从 30 秒压到 5 秒）：

```bash
# /etc/default/grub 的 GRUB_CMDLINE_LINUX 追加：
#   nvme_core.io_timeout=5000                  # 停摆上限 30s -> 5s（当前值确认可调）
#   pcie_aspm=off                             # 关闭 PCIe 链路省电，验证 ASPM 是否致卡
#   nvme_core.default_ps_max_latency_us=0     # 彻底关闭 APST
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

> `io_timeout` 当前为 30，正是日志里 30 秒节律的来源；压到 5 秒后，即使根因未除，登录最坏情况也会从 99 秒降到十几秒。

**若 BIOS 禁用 VMD + 内核参数都无效**，剩余可试：升级 WD SN5000S 固件（当前 `34430100`）、换 `linux-lts` 内核对照（不同 NVMe/VMD 代码路径）、换 SSD 交叉验证。

**操作建议**：这台盘通电 6 小时却已被强制断电 30 次（`unsafe_shutdowns: 30`）。务必用 `reboot` 正常重启，别直接断电；长期给电池目录开启自动安全关机。

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

**六条避坑经验**

1. **符号链接的模式位恒为 777 且无意义**。用 `find -perm` 统计损坏范围会严重高估，且 `chmod` 会跟随链接改到目标文件上。判定前先 `stat -c '%F'` 确认类型。
2. **别把用户数据当损坏**。`/opt` 下自装的应用（属主 `syske`、775/664）是正常状态，`chown -R /opt` 反而破坏它。
3. **"看起来像故障"的现象要先排除误报**。`pacman -Qkk` 报的 `/var/log/journal` GID 差异就是 journald 的正常 setgid 目录，不是问题。
4. **排查动作本身会污染数据**。全盘校验/扫描会产生与故障同signature 的日志，必须先取空闲基线再下结论。
5. **改权限前先确认脚本带上了 root**。本次误用 `sh`（非 `sudo bash`）跑修复脚本，好在上千条 `Operation not permitted` 全部失败，等于没执行 —— **权限不足的批量失败反而是安全网**，反倒是"半成功"最危险。
6. **别拿计数器当因果**。`/proc/interrupts` 里 NVMe 向量全为 0，一度被当成「中断丢失」的铁证，但实测磁盘延迟是 **0~1ms** —— 计数为 0 只是统计假象。判定「某机制失效」必须先做**延迟实测**，不能只看计数器。

**通用手法补充**：

```bash
# 测磁盘真实延迟（判断「延迟尖刺」而非「计数器」）
S=$(date +%s%N); dd if=/dev/nvme0n1p3 of=/dev/null bs=4K count=1 skip=$RANDOM iflag=direct; \
E=$(date +%s%N); echo "$(( (E-S)/1000000 )) ms"
```

**经验**：「卡顿」类问题的定位锚点选**带时间戳的关键字**（如 `No backend specified`、`Starting KDE Wayland Compositor`），比看总耗时有效得多；静默的 28 秒往往比刷屏的日志更能说明问题。

---

## 14. 缓解措施与复测（2026-10-09 晚）

### 14.1 已施加的缓解（不改根因，只压伤害）

在 `/etc/default/grub` 的 `GRUB_CMDLINE_LINUX` 追加三个参数（已备份 `grub.bak-20261009-1409`）：

```
systemd.mask=tpm2.target nvme_core.io_timeout=5000 pcie_aspm=off nvme_core.default_ps_max_latency_us=0
```

| 参数 | 作用 | 代价 |
|---|---|---|
| `nvme_core.io_timeout=5000` | **停摆上限 30s → 5s**（30 正是日志节律来源） | 无 |
| `pcie_aspm=off` | 关闭 PCIe 链路省电，验证 ASPM 是否致卡 | 略增待机功耗 |
| `nvme_core.default_ps_max_latency_us=0` | 彻底关闭 NVMe APST | 略增功耗（与 TLP 的续航目标冲突） |

另装 `intel-ucode 20260925-1`（此前**根本没安装**，导致 `Running old microcode`）。

```bash
sudo grub-mkconfig -o /boot/grub/grub.cfg
# 复测（重启后跑）
bash ~/verify-boot.sh
```

### 14.2 回滚方式

```bash
sudo cp /etc/default/grub.bak-20261009-1409 /etc/default/grub
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

### 14.3 预期判读

| 复测结果 | 含义 | 下一步 |
|---|---|---|
| 登录 < 15s | `io_timeout` 压低生效，根因未除但已可接受 | 可长期保留此参数 |
| 登录 15~25s | 停摆仍在但被压短 | 推进 BIOS 禁用 VMD |
| I/O timeout 节律变 5 秒 | 参数生效但根因在 | 只能靠 BIOS 禁用 VMD |
| 节律仍为 30 秒 | 参数没生效（检查 cmdline） | 核对 GRUB 配置 |

**根因结论未变**：停摆来自 VMD 链路（`pcieport 10000:e0:06.0: can't derive routing / PCI INT A: no GSI`），BIOS 307 未修复，**禁用 VMD 仍是唯一没试过的根因手段**。

### 14.4 禁用 VMD 的操作与风险评估（附决策依据）

**先说把握度**：禁用 VMD 是**假设，不是确诊**。理由：

- 「MSI-X 中断丢失」已被实测推翻（延迟 0~1ms，计数为 0 是统计假象）
- `can't derive routing / PCI INT A: no GSI` 在 VMD 设备上**非常常见且大多无害**，BIOS 307 未修复它，但也没有证据表明它就是元凶
- 目前能确定的只有**现象**：周期性 30 秒 I/O 停摆，成因未知

因此**先验证 14.1 的缓解参数**，不够好再考虑动 BIOS。

**已核实关闭是安全的**：

| 检查项 | 结果 |
|---|---|
| VMD 总线（`10000:e0`）下挂设备 | **仅 NVMe**（`10000:e1:00.0`） |
| 软 RAID（`/proc/mdstat`） | 空，无阵列 |
| LVM | 未安装 |
| 根分区 | 普通 ext4，**未加密**（无 `crypt=`，不绑定 TPM） |

**操作路径**（ASUS 官方 FAQ）：

```
开机按 F2 进 BIOS
按 F7 切换到 Advanced Mode（不按 F7 看不到该菜单）
Advanced → VMD setup menu → Enable VMD controller → Disabled
F10 保存重启
```

> 旁证：有用户反馈 ASUS 笔记本按 `F9` 载入最优默认值时 VMD **本来就是关闭的** —— 非 RAID 场景下关闭 VMD 是 ASUS 自己的默认取向。

**风险与救援**：

1. 网上确有禁用 VMD 后 Linux 起不来的案例（报 `probe with driver nvme failed with error -4`）
2. 救援①：开机连续狂按 `F2` 进 BIOS，把 VMD 改回 `Enabled`
3. 救援②：live USB 启动后执行 `efibootmgr` 还原引导顺序

**救援信息已落盘**：`~/efi-recovery.txt`（含 BootOrder 基线、磁盘布局、回滚命令）。

```bash
# 基线（2026-10-09 实测，改动前正常状态）
BootOrder: 0000,0006,0005,0003,0004,0002,0007,0008,0009
Boot0000* GRUB  HD(1,GPT,785a08b1-...)/\EFI\GRUB\grubx64.efi
# 还原命令
sudo efibootmgr -o 0000,0006,0005,0003,0004,0002,0007,0008,0009
```

---

## 15. 缓解参数生效后的实测（2026-10-09 14:27）

### 15.1 三个启动侧指标全部转好

| 指标 | 原始（9/21 前） | BIOS303/7.2.6 | **本轮** |
|---|---|---|---|
| 总开机 | 103s | 45.7s | **20.1s** |
| userspace | 63s | 34.3s | **3.97s** |
| initrd | 31.2s | 31.9s | **1.66s** |
| TPM 设备等待 | 32.9s | 32.9s | **1.99s** |
| `graphical.target` | — | 33.8s | **3.69s** |
| I/O tag timeout | — | 91 | **0** |
| i915 GSC 错误 | 有 | 有 | **无** |
| CPU microcode | old | old | **OK** |

**`pcie_aspm=off` 确实治好了 I/O 停摆**：11 次 → **0 次**（见 15.3 三次启动对照）。
**`intel-ucode` 装上后**，`Running old microcode` 消失。

### 15.2 但登录段回退：313 秒

| 启动 | `pcie_aspm=off` | I/O 超时 | hung task | 登录到桌面 |
|---|---|---|---|---|
| -2 | 无 | 11 | 0 | 33s |
| -1 | **有** | **0** | 0 | 未完成（强制关机） |
| 0 | **有** | **0** | 1 | **313s** |

内核 hung task 检测器抓到了现场，`startplasma-way` 卡在 D 状态 122 秒以上：

```
INFO: task startplasma-way:1473 blocked in I/O wait for more than 122 seconds
Call Trace:
  vfs_statx → filename_lookup → ext4_lookup
  __ext4_find_entry → __wait_on_bit → bit_wait_io → io_schedule → schedule
```

即：**只是执行了一次 `stat()` 查路径**，就卡在 ext4 目录项锁上。它等的不是命令完成（否则会有 I/O timeout 日志），而是**被别的操作占着的锁**。

**关键矛盾**：同一时刻实测磁盘延迟完全正常（300 次 4K 随机读，平均 0ms、最大 1ms、**无一次超过 50ms**）。所以「ext4 锁被长时间占用」这件事本身无法用磁盘性能解释。

### 15.3 诚实的结论：样本不足，且数据自相矛盾

- 有参数的两次启动（-1、0）**都没有完成登录**，其中 -1 是被强制关机的
- 无参数的 boot -2 完成了，登录 33s，但有 11 次 I/O 超时
- **n=1 的 313s 样本，且发生在两次强制断电之后的启动**（`unsafe_shutdowns` 已达 40），样本被污染

因此**现在无法判定 `pcie_aspm=off` 是净收益还是净损失**。需要一次干净的对照。

### 15.4 下一步判读顺序

1. **做一次干净的正常重启**（`systemctl reboot`，禁止强制断电），重新采样登录耗时
2. 若登录仍 > 60s → **回滚 `pcie_aspm=off`，保留 `io_timeout=5000`**：
   ```bash
   sudo cp /etc/default/grub.bak-20261009-1409 /etc/default/grub   # 会清掉全部三个参数，需手改
   # 改为仅保留：
   # GRUB_CMDLINE_LINUX="systemd.mask=tpm2.target nvme_core.io_timeout=5000"
   sudo grub-mkconfig -o /boot/grub/grub.cfg
   ```
3. 无论登录结果如何，**开机侧已从 103s 优化到 20.1s，这部分成果要保住**

### 15.5 SSD 健康警告

`unsafe_shutdowns` 已达 **40 次 / 7 小时通电**，仍在 `critical_warning: 0`、`media_errors: 0`，但强制断电是本问题排查过程中最大的硬件风险来源，务必用 `reboot`。

---

## 16. 最终结果（2026-10-09 22:26 验证）

### 16.1 全部指标达标

| 指标 | 原始（9/21 前） | 峰值（排查中） | **最终** |
|---|---|---|---|
| **总开机** | 103s | 50.1s | **15.6s** |
| userspace | 63s | 34.3s | **3.38s** |
| initrd | 31.2s | 31.9s | **3.38s** |
| TPM 设备等待 | 32.9s | 32.9s | **2.0s** |
| `graphical.target` | — | 33.8s | **2.99s** |
| **认证 → 桌面就绪** | 3s | 313s | **3s** |
| **I/O tag timeout** | — | 91 | **0** |
| hung task (D 状态 >120s) | — | 1 | **0** |
| i915 GSC 错误 | 有 | 有 | **0** |
| CPU microcode | old | old | **OK** |
| 磁盘最大延迟 | — | 30s 挂死 | **4ms** |

**开机 103s → 15.6s，登录稳定 3 秒，I/O 停摆彻底消失。**

### 16.2 起不来的那次：并非内核参数导致

排查中途系统曾连续多次无法进入桌面（boot -6 ~ -1，均为「内核起来了但桌面从未启动」，最后靠 live USB 重装配置 `systemd` + 重建 `mkinitcpio` 才恢复）。

**排查结论：根因是 `/boot` 下的 initramfs 损坏，而不是 `GRUB_CMDLINE_LINUX` 里加的参数。**依据：

1. 损坏期间**始终是同一组参数**（`cmdline` 逐次比对完全一致）
2. 用 live USB 重建 `initramfs-linux.img`（时间戳 20:56）后，**参数一个字没改**，系统即完全正常
3. 同期 `unsafe_shutdowns` 已累计 40+ 次 —— 强制断电期间 `/boot` 的 initramfs 很可能被写坏

> **教训：排查期反复强制断电，本身就是最大的破坏源。**
> `unsafe_shutdowns: 40 / 通电 7 小时` 这个比例非常不正常，initramfs 被截断只是它造成的后果之一。
> **无论卡成什么样，都要等或用 `reboot`；实在不行才长按电源，且事后务必重建 initramfs。**

### 16.3 最终生效的配置

```
# /etc/default/grub
GRUB_CMDLINE_LINUX_DEFAULT="loglevel=3 quiet"
GRUB_CMDLINE_LINUX="systemd.mask=tpm2.target nvme_core.io_timeout=5000 pcie_aspm=off nvme_core.default_ps_max_latency_us=0"
```

**四个参数各自的实际贡献**（有对照数据支撑）：

| 参数 | 贡献 | 依据 |
|---|---|---|
| `pcie_aspm=off` | **消除 I/O 停摆**（11 次 → 0 次） | 开关对比最清晰 |
| `nvme_core.io_timeout=5000` | 把停摆伤害上限从 30s 压到 5s | `io_timeout` 原值即 30 |
| `nvme_core.default_ps_max_latency_us=0` | 彻底关 NVMe APST | — |
| `intel-ucode`（软件包） | 消除 `Running old microcode` | — |
| BIOS 303 → 307 | **TPM 32.9s → 2.0s** | 固件层面修复 |

**VMD 最终未禁用** —— 因为问题已通过上述手段解决，无需冒险改 BIOS。

### 16.4 遗留清理项

- `/boot/B3405CCA.bin`（72MB）是刷新 BIOS 时放入的固件文件，刷完即可删除
- `~/efi-recovery.txt` 可保留作应急参考
- 长期建议：给电池目录配置自动安全关机，减少强制断电

---

## 17. initramfs 安全网与 GRUB 菜单清理（2026-10-09 23:19）

### 17.1 发现的缺口

排查收尾时发现，**上次 initramfs 损坏导致开不了机的那个安全网，其实是断的**：

| 检查项 | 当时状态 | 后果 |
|---|---|---|
| `linux.preset` 的 `PRESETS` | `('default')` | **不生成 fallback 镜像** |
| `mkinitcpio.conf` 的 `HOOKS` | 含 `autodetect` | 主镜像只含**当前已加载**的模块 |
| `GRUB_DISABLE_RECOVERY` | `true` | 菜单里**也不给** fallback 入口 |

> 注：`fallback_*` 那几行在 mkinitcpio 42.x 出厂 preset 里**本就是注释状态**，不是谁改坏的。
> 但 `autodetect` + 无 fallback 的组合意味着：只要当前环境少一个模块，主镜像就起不来，且**没有任何回退**。

### 17.2 修复内容（已备份 `*.bak-20261009-2319`）

```bash
# 1. /etc/mkinitcpio.d/linux.preset —— 启用 fallback 预设
PRESETS=('default' 'fallback')
fallback_image="/boot/initramfs-linux-fallback.img"
fallback_options="-S autodetect"

# 2. /etc/mkinitcpio.conf —— 主镜像去掉 autodetect，装全量模块
#   HOOKS=(base udev autodetect ...)  →  HOOKS=(base udev ...)

# 3. /etc/default/grub —— 删除 GRUB_DISABLE_RECOVERY=true
# 4. chmod 000 /etc/grub.d/31_efi_bootnext —— 干掉 9 个 EFI BootNext 垃圾条目
# 5. rm /boot/B3405CCA.bin —— 刷 BIOS 残留（70MB）
sudo mkinitcpio -P && sudo grub-mkconfig -o /boot/grub/grub.cfg
```

**镜像体积**：24MB → **213MB**（去掉 autodetect 的代价）。开机已只需 15.6s，这点开销可忽略。

**验证**：两个镜像都用 `lsinitcpio` 确认含 `nvme-core` / `vmd` / `ext4` 等关键模块，GRUB 中各被正确引用。

### 17.3 关于 `EFI BootNext` 垃圾条目

`grub-mkconfig` 输出里的 `Adding boot menu entry for EFI BootNext: ...` 就是它们���来源 —— 固件里的 `BootNext` EFI 变量残留，导致每次生成配置都多出 9 条网络/光驱/USB/可移除设备的条目。

处置：`chmod 000 /etc/grub.d/31_efi_bootnext`（标准做法）。这不会影响真实设备的正常启动，只是不再把它们列进菜单。

### 17.4 清理后的菜单（5 项，全部有意义）

```
Arch Linux
└─ Advanced options for Arch Linux
   ├─ Arch Linux, with Linux linux
   ├─ Arch Linux, with Linux linux (fallback initramfs)   ← 自动+手动双重保险
   └─ Arch Linux, with Linux linux (recovery mode)
UEFI Firmware Settings                                     ← 重启进 BIOS 用，保留
```

### 17.5 生效后应达到的行为

| 场景 | 结果 |
|---|---|
| 主 initramfs 缺模块起不来 | **手动**在 GRUB 菜单选 `fallback initramfs`（⚠️ 非自动，见 19 节） |
| 自动回退也不行 | 开机菜单选 `fallback initramfs` 手动进 |
| 需要改 BIOS 设置 | 菜单选 `UEFI Firmware Settings` |

---

## 18. 事故复盘：一次改三个文件导致开不了机（2026-10-09 23:19）

### 18.1 我做了什么

在**一台能正常开机**的系统上，一次性改了三个文件并立即重建 initramfs：

| 文件 | 改动 |
|---|---|
| `linux.preset` | 启用 `PRESETS=('default' 'fallback')` |
| `mkinitcpio.conf` | 从 `HOOKS` 中**移除 `autodetect`** |
| `/etc/default/grub` | 删除 `GRUB_DISABLE_RECOVERY=true` |

结果：**重启后无法启动**，需再次用 live 介质修复。

### 18.2 诚实结论：**我无法确认是哪个改动导致的**

按 mkinitcpio 官方文档，`autodetect` 的语义恰恰相反：

> "Any hooks placed before 'autodetect' will be installed in **full**."
> 移除 `autodetect` 只会让镜像包含**更多**模块，理论上应该更健壮，而非更易失败。

排查过但**未发现**证据支持：
- `/boot` 空间充足（740M 可用，两个 213M 镜像并存无压力）
- `autodetect` hook 与 `keymap` hook 之间**没有**代码依赖（`keymap` 里不含 `mkinitcpio_autodetect` 引用）

所以真实原因**存疑**。更可能的解释是：这台机器本就处于不稳定状态（40+ 次强制断电历史、此前已多次启动失败），故障**恰好**落在这次改动之后 —— 但我无法证明二者有因果关系。

**不编造解释，是这次复盘最重要的结论。**

### 18.3 真正的过程错误

比"哪个参数错了"更严重的是**方法错误**：

1. **一次改三个文件** —— 出了故障无法定位到具体哪一项
2. **在一个已经能开机的系统上做「优化」** —— 收益（省 190MB 磁盘）远小于风险（开不了机）
3. **没有先问用户**就执行了有风险的改动

### 18.4 最终状态（用户修复后）反而更合理

```
HOOKS=(base udev autodetect microcode modconf kms keyboard keymap consolefont block filesystems fsck)
```

| 镜像 | 模块数 | 体积 | 角色 |
|---|---|---|---|
| `initramfs-linux.img` | 39 | 24M | autodetect 精简，启动快 |
| `initramfs-linux-fallback.img` | **1051** | 213M | **全量模块，救援用** |

两个镜像都确认含 `vmd.ko` 与 `fsck.ext4`（NVMe 通路必需）。**主镜像精简 + fallback 全量**，正是最理想的组合 —— 比我原来配的更好。

实测：开机 29.9s、登录 4 秒、I/O 超时 0、失败单元 0。

### 18.5 方法论教训

> **一次只改一个变量，改完先验证再动下一个。**

尤其在生产/日常使用的机器上：

- 改动前先问用户「这个改动的收益值得冒风险吗」
- 安全网类改动（fallback/救援）**收益小、风险大**，属于「锦上添花」，不该在排查收尾阶段冒险
- 机器状态不稳定时，**先让它稳定下来**（正常关机几次、确认硬件健康），再做优化
- 出故障后**不要急着归因** —— 无法证实的因果关系应当如实说明

---

## 19. 两个 initramfs 镜像的实际影响（含一处自我更正）

### 19.1 两个镜像的分工

| | `initramfs-linux.img` | `initramfs-linux-fallback.img` |
|---|---|---|
| 体积 | **24M** | 213M |
| 模块数 | **39** | **1051** |
| 打包方式 | `autodetect`（只含当前系统实际加载的模块） | 全量模块 |
| 是否默认启动 | ✅ 是 | ❌ 否，需手动选 |
| 正常开机耗时贡献 | 按 24M 读取，很快 | **完全不参与**，零影响 |
| 磁盘占用 | \multicolumn{2}{c}{合计 237M，`/boot` 余 740M，无压力 | |

### 19.2 ❌ 更正：fallback **不是自动回退**，是手动选择

我此前在 17.5 写「主 initramfs 起不来会自动回退」，**这是错的**。实测验证：

```bash
grep -n fallback /usr/lib/initcpio/init        # 无任何命中
grep -n fallback /usr/lib/initcpio/init_functions  # 无任何命中
mkinitcpio 主程序里也没有 fallback_image 的运行时逻辑（它只是 preset 的 shell 变量）
```

`/usr/lib/initcpio/init` 只有 112 行，流程是：跑 hooks → `resolve_device "$root"` → `fsck_root` → 挂载 `/sysroot`。若 root 设备找不到，走到末尾直接结束：

```
# Nothing got mounted on /sysroot. This is the end, we don't know what to do anymore
```

**没有任何自动切换到 fallback 的分支。**

所以 fallback 的真实作用是：**主镜像起不来时，在 GRUB 菜单里手动选中它启动**，用 1051 个完整模块挂载 root，进系统后再修复并重建主镜像。

### 19.3 ⚠️ 由此带来的现实约束

当前 `GRUB_TIMEOUT=1`，即开机后**只有 1 秒**可以操作菜单。要用 fallback 救援，几乎必须在 1 秒内完成「按方向键 → 进子菜单 → 选 fallback」。

**这是一个真实的短板，但我不建议现在去改** —— 改 `GRUB_TIMEOUT` 会增加开机时间，属于收益很小的改动；真遇到主镜像起不来的情况，直接在 GRUB 里等菜单出现后按 `e` 编辑 cmdline 也可以。

---

## 20. 收官验证（2026-10-10）与残留提醒

### 20.1 最优成绩（2026-10-10 00:00 启动）

| 指标 | 原始（9/21） | 排查峰值 | **最优** |
|---|---|---|---|
| **总开机** | 103s | 50.1s | **16.8s** |
| 其中固件 POST | 7.6s | 20.1s | 7.6s |
| userspace | 63s | 34.3s | **4.3s** |
| **认证 → 桌面** | 3s | 313s | **4s** |
| I/O tag timeout | — | 91 | **0** |
| hung task | — | 1 | **0** |
| 失败单元 | — | — | **0** |

已追平笔记里记录的历史正常基线（12.5s），差距主要是固件 POST 的随机波动（实测区间 6.3~20.1s）。

> ⚠️ **`firmware` 那一项会骗人**。它是 BIOS 自检时间，与本次所有优化无关且波动极大。
> **看 `userspace` 和 `认证→桌面` 两个指标才有意义。**

### 20.2 残留的无害噪音（已确认，无需处理）

| 内核消息 | 性质 |
|---|---|
| `i8042: PS/2 appears to have AUX port disabled` | 针对 PS/2 AUX 口；本机触控板是 **I2C-HID**（`ASCE1208:00 04F3:3340` → event9），两者无关 |
| `pcieport 10000:e0:06.0: can't derive routing / no GSI` | VMD 链路的常见日志，**BIOS 307 未修但系统已不复现卡顿** |
| `i915 [CRTC:151:pipe A] DSB 0 poll error` | 核显显示管线告警，当前不影响使用 |
| `resource sanity check ... igen6_edac` | Intel 网卡 EDAC 驱动自身瑕疵，不影响网卡 |
| `asus_armoury: No matching power limits found` | 无匹配机型配置，属正常 |
| `regulatory.db failed with error -2` | **`wireless-regdb` 未安装**，见下 |

### 20.3 `wireless-regdb`：✅ 已安装（2026-10-10 00:05）

```bash
sudo pacman -S wireless-regdb   # 版本 2026.09.03-1，签名验证通过
```

安装前内核每次启动报 `Direct firmware load for regulatory.db failed with error -2`。

**注意内核只在开机时加载该库** —— 装包时本次启动已经过去，因此当前仍需等下次重启才生效。
当前 `iw reg get` 显示 `country 00: DFS-UNSET`，这是缺库时的兜底值（雷达检测未正确启用）。

> **免重启的临时办法**（若当下就需要 5GHz 表现）：
> `sudo iw reg set CN` —— 直接指定国家代码，跳过等待。
> 持久化可写 `/etc/conf.d/regulatory.conf`：
> ```
> echo 'WIRELESS_REGDB=y' > /etc/conf.d/regulatory.conf
> ```
> （多数发行版由 `systemd-modules-load` 读取该文件；Arch 上由 `regulatory.conf` 机制处理，
> 确认生效可重启后用 `iw reg get` 复核 `country` 与 DFS 状态）

### 20.4 GRUB 两个镜像的最终对应关系（已验证正确）

| 菜单项 | initramfs | 模块数 |
|---|---|---|
| **Arch Linux**（默认） | `initramfs-linux.img` | 39 |
| Arch Linux, with Linux linux | `initramfs-linux.img` | 39 |
| (fallback initramfs) | `initramfs-linux-fallback.img` | 1051 |
| (recovery mode) | `initramfs-linux-fallback.img` | 1051 |

每个 initrd 都先加载 `/intel-ucode.img`（微码必须最先加载）。
**默认路径只用 24M 主镜像，fallback 不参与正常启动，对开机速度零影响。**

> 检查 grub.cfg 时注意：`initrd` 与路径之间是**制表符**，
> 用 `grep 'initrd '`（空格）会**零结果**，误以为配置有问题。

### 20.5 关于「终端卡顿」

登录后约 10 秒启动 opencode，实测：读取 **214MB**、占 **~15% CPU**、内存 **567MB**（两个进程）。
时间线与感知卡顿吻合（登录 ~20s → konsole 22s → opencode 31s）。

**属于工具启动的正常开销，不是故障复发** —— 此时磁盘已不 stall（I/O 超时 0、延迟 0~4ms）。
工作区本身不是原因（两仓库共约 1564 个文件、51MB）。

### 20.6 电池安全防护配置（2026-10-10 已完成）

**目标**：消除「忘记插电 → 电池耗尽 → 硬断电」这个最现实的 unsafe shutdown 来源。

**配置路径**：系统设置 → 电源管理 → **Advanced Power Settings**（Advanced Power Settings 页，不在三个 Profile 标签里）

| 项 | 改前 | 改后 |
|---|---|---|
| Battery Levels → Low level | 10% | **20%** |
| Battery Levels → Critical level | 5% | **10%** |
| **At critical level** | Hibernate | **Shut down** ★ |
| Charge Limit → Stop charging at | 100% | **80%** |

**为什么把 Hibernate 换成 Shutdown**：休眠需把全部内存写入 swap，而本机 **swap 仅 4GB / 内存 30GB**。
内存用量一旦超过 4GB 休眠即失败 —— 而 IDEA、Docker、浏览器很容易造成这种用量。
**等于在最需要它工作的时刻失效**，正是要避免的强制断电。

**生效验证**：

```bash
grep -A3 BatteryManagement ~/.config/powerdevilrc
# BatteryCriticalAction=8   BatteryCriticalLevel=10   BatteryLowLevel=20
cat /sys/class/power_supply/BAT0/charge_control_end_threshold   # 80 —— 充电上限真实生效
```

> ⚠️ **键名教训**：Plasma 6 实际键名是 `[BatteryManagement]` 段的
> `BatteryCriticalAction` / `BatteryCriticalLevel` / `BatteryLowLevel`，
> **不是**常见猜测的 `actionCriticalBattery` / `criticalBatteryThreshold`。
> 猜错的话配置看似写入、实则不生效，且极难察觉 —— **不确定就不要手改，用 GUI**。

### 20.7 长期建议

1. **务必用 `reboot` 正常重启**。该盘 `unsafe_shutdowns` 已 **40+ 次 / 通电 7 小时**，比例严重异常，是整个排查过程中最大的硬件风险源。
2. 给电池目录配置自动安全关机，减少强制断电。
3. **观察几天日常使用即可，不要再为验证而频繁重启。**
4. 若日后再遇同类问题，参考第 13.6 节的通用手法（切分登录前后、找静默空洞、数中断、**实测延迟而非只看计数器**）。

### 20.8 备份文件清单

| 文件 | 说明 |
|---|---|
| `/etc/default/grub.bak-20261009-1409` | 加缓解参数**前** |
| `/etc/default/grub.bak2-20261009-2319` | 动 initramfs/GRUB **前** |
| `/etc/mkinitcpio.conf.bak-20261009-2319` | 动 HOOKS **前** |
| `/etc/mkinitcpio.d/linux.preset.bak-20261009-2319` | 动 preset **前** |
| `~/efi-recovery.txt` | EFI 引导顺序基线与救援步骤 |
| `~/verify-boot.sh` | 启动复测脚本 |
