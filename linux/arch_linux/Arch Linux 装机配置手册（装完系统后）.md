# Arch Linux 装机配置手册（装完系统后，一次到位）

> 归档时间：2026-09-21
> 适用：办公开发机（Java 后端 + 中文环境 + 日常软件），KDE Plasma 6 / Wayland，稳定优先
> 前置：系统基础安装（镜像/分区/pacstrap/GRUB）见 [arch-linux安装记录.md](./arch-linux安装记录.md)
> 本手册按顺序执行即可；`<占位>` 处替换为自己的值

---

## 0. 全局原则

1. **AUR 不用 helper**（paru-bin 等预编译包与系统 libalpm 版本不匹配会报 `libalpm.so.X` 错误），统一手动流程：
   ```bash
   git clone https://aur.archlinux.org/<包名>.git && cd <包名>
   # ① 装 depends（看 PKGBUILD）② makepkg --noconfirm（不带 -s，避免交互卡住）③ sudo pacman -U *.pkg.tar.zst
   ```
2. **GitHub 下载需要代理**：`export http_proxy=http://127.0.0.1:7897 https_proxy=http://127.0.0.1:7897`
3. **不要用 `pkill -f` 匹配命令行里出现的模式**（会误杀执行命令的 shell），用 `pkill -x 进程名` 或按 PID
4. 每步做完验证（`pacman -Q` / 启动测试）再继续

---

## 1. 系统基础

### 1.1 镜像源 & multilib
```bash
sudo sed -i '1i Server = https://mirrors.aliyun.com/archlinux/$repo/os/$arch' /etc/pacman.d/mirrorlist
# 启用 multilib（手动编辑 /etc/pacman.conf，取消 [multilib] 及其 Include 行的注释）
# ⚠️ 教训：不要用 sed 批量取消注释，会连 #[core-testing] 等注释段后的 Include 一起启用，
#    导致孤立 Server 行落入 [options] 段报 warning
sudo pacman -Sy
```

### 1.2 locale / 时区 / 时间
```bash
sudo sed -i 's/^#zh_CN.UTF-8/zh_CN.UTF-8/' /etc/locale.gen && sudo locale-gen
sudo localectl set-locale LANG=zh_CN.UTF-8
sudo timedatectl set-timezone Asia/Shanghai
sudo timedatectl set-ntp true
```

### 1.3 基础包
```bash
sudo pacman -S base-devel git wget curl unzip zip p7zip tree \
  networkmanager openssh bash-completion
sudo systemctl enable --now NetworkManager
```

---

## 2. 桌面环境（KDE Plasma 6）

```bash
sudo pacman -S plasma-meta konsole dolphin kate ark gwenview okular spectacle \
  kcalc systemsettings plasma-nm plasma-pa sddm plasma-x11-session
sudo systemctl enable --now sddm
# SDDM 主题（AUR, 手动流程）
git clone https://aur.archlinux.org/sddm-astronaut-theme.git && cd sddm-astronaut-theme
makepkg --noconfirm && sudo pacman -U *.pkg.tar.zst
# /etc/sddm.conf.d/kde_settings.conf: [Theme] Current=sddm-astronaut-theme
```
- **X11 备用会话**：`plasma-x11-session`（投屏兜底，钉钉/企业微信投屏走 X11）
- **中文字体**：`sudo pacman -S noto-fonts noto-fonts-cjk noto-fonts-emoji`

---

## 3. 硬件与启动优化

### 3.1 声卡无输出（新平台必做）
```bash
sudo pacman -S sof-firmware    # Core Ultra/新锐龙等 SOF 声卡; 装完重启
# 验证: pactl info 的 Default Sink 不再是 auto_null
```

### 3.2 启动优化（TPM 等待 32s → 12.5s）
详见 [Arch Linux 新机优化与故障排查](./Arch%20Linux%20新机优化与故障排查（华硕ExpertBook%20P3455）.md)：
```bash
sudo systemctl mask tpm2.target
# /etc/default/grub 的 GRUB_CMDLINE_LINUX 加: systemd.mask=tpm2.target
# GRUB_TIMEOUT=1; 然后 sudo grub-mkconfig -o /boot/grub/grub.cfg
```

### 3.3 BIOS 项（手动）
- BIOS → Boot → **Fast Boot**（省固件自检 4-5s）

---

## 4. 中文输入法（fcitx5 + Rime 雾凇）

细节见 [输入法配置文档](./Arch%20Linux%20输入法配置（Fcitx5%20%2B%20Rime%20雾凇拼音）.md)，关键命令：
```bash
sudo pacman -S fcitx5 fcitx5-rime librime
# 环境变量 /etc/environment.d/im.conf
cat > /etc/environment.d/im.conf <<'EOF'
GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS=@im=fcitx
SDL_IM_MODULE=fcitx
EOF
# 自启 + KWin 虚拟键盘
cp /usr/share/applications/org.fcitx.Fcitx5.desktop ~/.config/autostart/
kwriteconfig6 --file kwinrc --group Wayland --key InputMethod org.fcitx.Fcitx5.desktop
# 雾凇（plum 方式, 比 AUR 可控）
git clone --depth=1 https://github.com/rime/plum.git ~/plum
cd ~/plum && rime_dir="$HOME/.local/share/fcitx5/rime" bash rime-install iDvel/rime-ice
```
**两个关键坑**：
- ⚠️ 改 `~/.config/fcitx5/profile` 前**先 `pkill -x fcitx5`**（fcitx5 退出时用内存配置覆盖文件）
- ⚠️ **不要装 Rime 万象语法模型**（401MB，登录卡 43s；需要长句排名的场景再装）

---

## 5. 网络与代理

### 5.1 Clash Verge（AUR）
```bash
git clone https://aur.archlinux.org/clash-verge-rev-bin.git && cd clash-verge-rev-bin
makepkg --noconfirm && sudo pacman -U *.pkg.tar.zst
# 配置目录: ~/.local/share/io.github.clash-verge-rev.clash-verge-rev/verge.yaml
# 必改: auto_check_update: true -> false（否则每次启动静默下载新版, 慢）
# 手动启动（不设自启, 用户习惯）
```

### 5.2 终端代理开关（写入 ~/.bashrc）
```bash
proxy_on() { export http_proxy=http://127.0.0.1:7897 https_proxy=http://127.0.0.1:7897 all_proxy=socks5://127.0.0.1:7897; echo "✔ 代理已开"; }
proxy_off() { unset http_proxy https_proxy all_proxy; echo "✔ 代理已关"; }
```

### 5.3 防火墙
```bash
sudo pacman -S ufw && sudo systemctl enable --now ufw && sudo ufw enable
```

---

## 6. 开发环境（Java 后端）

```bash
sudo pacman -S jdk8-openjdk maven
archlinux-java status                    # 确认默认 JDK8
echo 'JAVA_HOME=/usr/lib/jvm/java-8-openjdk' | sudo tee /etc/environment.d/java.conf
```

### IDEA Community
- AUR 有 `intellij-idea-community-edition-bin`（GitHub 大文件，走代理）
- 手动方案：官网下载 `idea-2026.2.3.tar.gz`（**x86_64 版**，aarch64 版解压无法运行）→ `/opt/idea-oss` + `/usr/local/bin/idea` 软链 + 桌面入口

### mycli（数据库命令行）
```bash
sudo pacman -S python-pipx
PIP_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple" pipx install mycli
```

### Git 双身份 + SSH key
```bash
ssh-keygen -t ed25519 -C "github" -f ~/.ssh/id_ed25519 -N ""
# 公钥加 GitHub: https://github.com/settings/ssh/new
# 全局=公司身份; 私人仓库按目录 includeIf:
git config --global user.name "<公司名>"
git config --global user.email "<公司邮箱占位>"
cat > ~/.gitconfig-personal <<'EOF'
[user]
    name = syske
    email = 715448004@qq.com
EOF
git config --global --add includeIf."gitdir:~/workspace/ai-system/".path ~/.gitconfig-personal
git config --global --add includeIf."gitdir:~/workspace/person-learning-note/".path ~/.gitconfig-personal
# 验证(必须在仓库内): cd ~/workspace/ai-system && git config user.name -> syske
```

---

## 7. 办公与日常软件

### 7.1 浏览器
```bash
sudo pacman -S firefox
# Chrome (AUR): git clone https://aur.archlinux.org/google-chrome.git ... (同步需代理)
# Chrome 打不开 = 僵尸实例: pkill -x chrome; rm -f ~/.config/google-chrome/Singleton*; 重开
```

### 7.2 钉钉
```bash
# AUR dingtalk-bin: PKGBUILD 需去掉已下架的 gtk2 依赖再构建
# Wayland 下投屏不可用(8.2.8 用 DRM/GBM 抓屏, hook 无效); 网页版已停用
# 投屏兜底: 登录界面选 Plasma (X11) 会话
```

### 7.3 企业微信（Wine 方案）
完整过程见 [企业微信安装文档](./Arch%20Linux%20安装企业微信（Wine%20方案）.md)，结论：
- 官方无 Linux 原生版；AUR `com.qq.weixin.work.deepin` 提供程序文件
- **deepin-wine 的 wow64 与 WXWork 5.0 不兼容**（comctl32/DuiLib 加载失败）
- 正解：**官方 wine + 全新容器**：`sudo pacman -S wine`（先启用 multilib）→ `wineboot -u` 建 `WeCom-official` 容器 → 拷贝 WXWork 程序 → 启动脚本 `~/.local/bin/wecom`

### 7.4 软件中心提速（Discover）
```bash
sudo pacman -S packagekit          # 后端缺失会启动干等超时
sudo appstreamcli refresh-cache --force   # 生成 AppStream 缓存(写到 /usr/share/swcatalog)
# 不用 flatpak 的话在 设置 里关掉 Flatpak 后端
```

### 7.5 卸载欢迎程序（防开机弹窗）
```bash
sudo pacman -Rns plasma-welcome     # 它每次登录拉起 systemsettings
```

---

## 8. 终端增强

```bash
sudo pacman -S fzf ripgrep bat eza zoxide btop tldr
```
`~/.bashrc` 追加（完整块，可直接粘贴）：
```bash
# --- fzf: Ctrl+R 历史 / Ctrl+T 文件 / Alt+C 目录 ---
if command -v fzf >/dev/null 2>&1; then
  source /usr/share/fzf/key-bindings.bash 2>/dev/null
  source /usr/share/fzf/completion.bash 2>/dev/null
  export FZF_DEFAULT_OPTS='--height 40% --border --preview "bat --color=always --line-range=:200 {}" 2>/dev/null'
fi
# --- zoxide 智能跳转 ---
if command -v zoxide >/dev/null 2>&1; then eval "$(zoxide init bash)"; fi
# --- eza / bat ---
if command -v eza >/dev/null 2>&1; then
  alias ls='eza --group-directories-first'; alias ll='eza -la --group-directories-first --git'
  alias la='eza -a'; alias lt='eza -T --group-directories-first'
fi
if command -v bat >/dev/null 2>&1; then alias cat='bat --paging=never'; export BAT_THEME='ansi'; fi
# --- PS1: 用户@主机 路径 (git分支) 失败✗ ---
__git_branch() { git branch --show-current 2>/dev/null; }
__ps1_status() { [ "${_last:-0}" -ne 0 ] && printf ' ✗'; }
PROMPT_COMMAND='_last=$?; history -a'
PS1='\[\e[1;32m\]\u@\h\[\e[0m\] \[\e[1;34m\]\w\[\e[0m\]\[\e[1;36m\]$(__git_branch)\[\e[0m\]\[\e[1;31m\]$(__ps1_status)\[\e[0m\] \$ '
# --- 历史增强: 扩容/去重/时间戳/多终端同步 ---
export HISTSIZE=10000 HISTFILESIZE=100000
export HISTCONTROL='ignoreboth:erasedups'
export HISTTIMEFORMAT='%F %T '
export HISTIGNORE='ls:ll:la:lt:cd:cd ..:pwd:exit:clear:c:history'
shopt -s histappend
# --- git 简写 ---
alias gs='git status' ga='git add' gc='git commit' gp='git push' gl='git pull'
alias gd='git diff' gst='git stash' glog='git log --oneline --graph --decorate -20'
fshow() { git log --graph --color=always --format='%C(auto)%h %s %an %ad' --date=short "$@" | fzf --ansi --preview 'git show --stat --color=always {1}' | awk '{print $1}' | xargs -r git show; }
# --- pacman 简写 ---
alias pac='sudo pacman' pacs='sudo pacman -S' pacr='sudo pacman -Rns' pacu='sudo pacman -Syu' pacq='pacman -Q' orph='pacman -Qdt'
# --- 代理(见第5章) ---
```
**Konsole 深色主题**（可选）：`~/.local/share/konsole/Dark.profile`（ColorScheme=BreezeDark, Font=Noto Sans Mono,14），konsolerc 设 `DefaultProfile=Dark.profile`

---

## 9. 系统维护与优化

```bash
# TLP 电源管理
sudo pacman -S tlp && sudo systemctl enable --now tlp
# swappiness
echo 'vm.swappiness=10' | sudo tee /etc/sysctl.d/99-swappiness.conf
# journald 限流
echo 'SystemMaxUse=200M' | sudo tee -a /etc/systemd/journald.conf && sudo systemctl restart systemd-journald
# paccache 定时清理
sudo systemctl enable --now paccache.timer
# baloo 排除大目录: ~/.config/baloofilerc 的 [Excluded Folders] 加 Downloads/.cache
```
**KDE 自带应用清理**（办公机不需要的）：
```bash
# 分批卸载, 每组后验证核心: plasma-workspace/kwin/dolphin/konsole/fcitx5 完好
sudo pacman -Rns kontact kmail korganizer kaddressbook akregator akonadi-* kdepim-addons
sudo pacman -Rns elisa k3b ktorrent konversation kdenlive koko dragon juk calligra kdevelop*
sudo pacman -Rns kleopatra kgpg kget krdc krfb kdeconnect falkon konqueror angelfish
# ⚠️ 教训: pacman -Rns 有一个包不存在整个事务中止, 先 pacman -Q 逐个确认
# ⚠️ 保留: v4l-utils(ffmpeg 依赖); 结束后 pacman -Qdt 应为 0 孤儿
```
磁盘清理细节见 [磁盘清理文档](./Arch%20Linux%20磁盘空间清理与优化.md)。

---

## 10. 数据与笔记同步

```bash
# 个人笔记仓库(私人身份自动生效)
git clone git@github.com:Syske/person-learning-note.git ~/workspace/person-learning-note
cd ~/workspace/person-learning-note && git config user.name   # 应输出 syske
```

---

## 11. 最终检查清单

- [ ] 输入法：登录后 3s 内 fcitx5 就绪，Ctrl+Space 切换，中文输入正常
- [ ] 启动：`systemd-analyze` 总时间 < 15s（TPM 已 mask）
- [ ] 声音：`pactl info` Default Sink 非 auto_null
- [ ] 时钟：`timedatectl` 显示 Asia/Shanghai + NTP active
- [ ] 终端：新开窗口 PS1 带 git 分支，Ctrl+R 模糊历史，`z` 跳转可用
- [ ] git：`ssh -T git@github.com` 认证通过；双身份按目录生效
- [ ] 代理：Clash 手动启动，`proxy_on` 后能访问 Google/GitHub
- [ ] 软件：Chrome(同步)、钉钉、企业微信、IDEA、Maven 均可启动
- [ ] 无开机弹窗：欢迎程序已卸载
- [ ] `pacman -Qdt` = 0 孤儿；`pacman -Q` 无残留测试包
- [ ] Discover 打开 < 5s

---

## 附录：参考文档索引（本仓库 linux/arch_linux/）

| 文档 | 内容 |
|---|---|
| arch-linux安装记录.md | 基础安装（镜像/分区/pacstrap） |
| Arch Linux 输入法配置（Fcitx5 + Rime 雾凇拼音）.md | 输入法细节 |
| Arch Linux 新机优化与故障排查（华硕ExpertBook P3455）.md | TPM/声卡/钉钉/AUR 坑/应用故障 |
| Arch Linux 磁盘空间清理与优化.md | 磁盘清理 |
| Arch Linux 安装企业微信（Wine 方案）.md | 企业微信完整过程 |
| arch-linux安装deb软件.md | debtap 转 deb 方案（旧） |
