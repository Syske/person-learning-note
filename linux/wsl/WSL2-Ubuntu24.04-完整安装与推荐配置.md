# WSL2 + Ubuntu 24.04 LTS 完整安装与推荐配置（2026-08）

> 目标：在 Windows 上启用 WSL2，将 Ubuntu 24.04 LTS 安装到非 C 盘（D:\dev-tool），并完成推荐配置（用户、镜像源、开发工具、SSH 凭证、资源分配）。

## 一、环境信息

| 项目 | 值 |
|------|-----|
| Windows | 10.0.26200.8973（Windows 11） |
| CPU | AMD Ryzen 5 5600U（12 线程） |
| 内存 | 36 GB |
| 安装前 WSL 版本 | 2.7.11.0（Store 最新稳定版） |
| 安装后 WSL 版本 | 2.7.11.0（无需升级） |
| 内核 | 6.18.33.2-microsoft-standard-WSL2 |
| 安装的发行版 | Ubuntu 24.04.4 LTS (Noble Numbat) |
| 安装位置 | `D:\dev-tool\WSL\Ubuntu-24.04`（ext4.vhdx） |

---

## 二、确认/启用 WSL

### 1. 检查 WSL 状态

```powershell
wsl --status
wsl --version
```

输出关键项：
```
WSL 版本:     2.7.11.0
内核版本:     6.18.33.2-2
Windows:      10.0.26200.8973
```

> 说明：新装系统 `wsl --install` 会默认启用 WSL2 并安装内核。本机已就绪，无需重复启用。

### 2. 查看可用发行版

```powershell
wsl --list --online
```

推荐选择 **Ubuntu 24.04 LTS**（成熟稳定、支持到 2029，生态兼容性最好）。

---

## 三、安装 Ubuntu 到自定义目录（D:\dev-tool）

> 核心思路：`wsl --install` 只能装到 C 盘默认位置；要装到自定义目录必须用 `wsl --import` 导入 rootfs。

### 1. 下载官方 rootfs 镜像

```powershell
curl.exe -L -o "$env:TEMP\ubuntu-noble-wsl.rootfs.tar.gz" `
  "https://cloud-images.ubuntu.com/wsl/releases/24.04/current/ubuntu-noble-wsl-amd64-wsl.rootfs.tar.gz"
```

约 340 MB。镜像说明：官方 cloud-images 页面提示 WSL 镜像已迁移至 `cdimages.ubuntu.com/ubuntu-wsl/`，但 rootfs 仍可用上述 URL 下载。

> 注意架构：AMD 选 `amd64`，ARM 选 `arm64`。

### 2. 创建目标目录并导入

```powershell
New-Item -ItemType Directory -Path "D:\dev-tool\WSL\Ubuntu-24.04" -Force
wsl --import Ubuntu-24.04 "D:\dev-tool\WSL\Ubuntu-24.04" "C:\Users\syske\AppData\Local\Temp\opencode\ubuntu-noble-wsl.rootfs.tar.gz" --version 2
```

### 3. 验证

```powershell
wsl --list --verbose
wsl -d Ubuntu-24.04 -- cat /etc/os-release
```

输出确认：`Ubuntu 24.04 LTS (Noble Numbat)`、VERSION=2。

### 4. 清理临时文件

```powershell
Remove-Item "C:\Users\syske\AppData\Local\Temp\opencode\ubuntu-noble-wsl.rootfs.tar.gz"
```

---

## 四、初始化用户与基础配置

### 1. 创建用户并授予 sudo

```bash
sudo useradd -m -s /bin/bash syske
sudo usermod -aG sudo syske
sudo bash -c 'echo "syske ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/syske && chmod 440 /etc/sudoers.d/syske'
```

### 2. 设置默认用户 + 启用 systemd

导入的发行版没有 wsl.conf（导入的是 tar，不能直接改 Windows 侧文件），需在 WSL 内写入：

```bash
sudo tee /etc/wsl.conf > /dev/null << 'EOF'
[user]
default=syske
[boot]
systemd=true
EOF
```

> 关键经验：`wsl --import` 生成的是单个 `ext4.vhdx` 虚拟磁盘，无法像 Store 版那样直接编辑 `D:\...\etc\wsl.conf`。必须进入 WSL 内部写文件。
> 写完后新开的 wsl 会话即以 syske 登录，之前的 root 会话操作文件需补 sudo。

---

## 五、配置清华镜像源

Ubuntu 24.04 使用 deb822 格式源文件：`/etc/apt/sources.list.d/ubuntu.sources`。

### 1. 备份

```bash
sudo cp /etc/apt/sources.list.d/ubuntu.sources /etc/apt/sources.list.d/ubuntu.sources.bak
```

### 2. 替换官方源为清华源

```bash
sudo sed -i \
  's|http://archive.ubuntu.com/ubuntu|https://mirrors.tuna.tsinghua.edu.cn/ubuntu|;
   s|http://security.ubuntu.com/ubuntu|https://mirrors.tuna.tsinghua.edu.cn/ubuntu|' \
  /etc/apt/sources.list.d/ubuntu.sources
```

> **重要坑点**：清华镜像没有独立的 `ubuntu-security` 目录（404），security 包在 `/ubuntu/dists/noble-security` 下，所以安全源也必须指向 `/ubuntu`，不要写成 `/ubuntu-security`。

### 3. 防止 cloud-init 覆盖

```bash
sudo bash -c 'grep -q apt_preserve_sources_list /etc/cloud/cloud.cfg || echo "apt_preserve_sources_list: true" >> /etc/cloud/cloud.cfg'
```

### 4. 更新与升级

```bash
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y upgrade --with-new-pkgs   # 升级被 keep-back 的包
```

### 5. 升级中的两个坑点

- **cloud-init / wsl-setup / ubuntu-wsl 配置失败**：dpkg 在升级 cloud-init 时遇到 `cloud.cfg` 配置文件冲突会交互询问，非交互环境直接报错。解决：
  ```bash
  sudo dpkg --force-confold --configure -a
  ```
  `--force-confold` 保留本地已改配置文件并跳过交互提示。
- **libgl1-amber-dri 无法升级**：Mesa 过渡期 `libglapi-amber` 与新版 `libglapi-mesa` 存在 Breaks 冲突，属 Ubuntu 官方包管理的过渡阶段，保留旧版即可，不影响使用。

---

## 六、安装基础开发工具

```bash
sudo apt-get -y install build-essential git curl wget htop ca-certificates zip unzip
```

| 包 | 说明 |
|----|------|
| build-essential | GCC/G++ 编译工具链（gcc、g++、gdb、make、binutils），编译源码/pip 原生扩展/npm 原生模块必需 |
| git | 版本控制 |
| curl / wget | 网络工具 |
| htop | 进程/资源监控 |
| zip / unzip / ca-certificates | 压缩与证书 |

验证：`gcc --version` → GCC 13.3.0；`git --version` → 2.43.0。

---

## 七、安装 Node.js（nvm 方式）

推荐用 nvm 管理，便于切换版本。

### 1. 安装 nvm

```bash
curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```

### 2. 安装 LTS 版本

```bash
export NVM_DIR="$HOME/.nvm"
. "$NVM_DIR/nvm.sh"
nvm install --lts
nvm alias default 'lts/*'
```

结果：Node.js v24.19.0（Krypton LTS）、npm v11.17.0。

> **Windows 传参经验**：通过 `wsl -d <distro> -- bash -c '...'` 传带 `$`、引号的脚本时，wsl.exe 会破坏参数（`$HOME` 丢失、`/nvm.sh` 路径错误）。稳妥做法：先把脚本写入临时文件，再 `wsl -d <distro> -- bash /mnt/c/path/script.sh` 执行。

---

## 八、配置 Git 用户信息

WSL 与 Windows 的 git 配置互相独立（`$HOME` 不同），不会自动继承。

```bash
git config --global user.name "syske"
git config --global user.email "<GIT_EMAIL>"
```

> 软链接继承 Windows 配置虽可行，但会带入 `core.autocrlf=true`、`http.sslverify=false` 等 Windows 专属设置，Linux 下不推荐。建议各自独立配置。

---

## 九、SSH 凭证（独立生成）

为 WSL 单独生成密钥（与 Windows 分离，避免冲突）：

```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
ssh-keygen -t ed25519 -C "syske@wsl-ubuntu24" -N "" -f ~/.ssh/id_ed25519
```

查看公钥：
```bash
cat ~/.ssh/id_ed25519.pub
```

将公钥添加到 GitHub（Settings → SSH keys）与阿里云云效 Codeup（个人设置 → SSH 公钥）。

验证连通性：
```bash
ssh -T git@github.com          # Hi Syske! You've successfully authenticated...
ssh -T git@codeup.aliyun.com   # Welcome to Codeup, syske!
```

---

## 十、WSL 资源分配（.wslconfig）

### 1. 确认硬件资源

```powershell
(Get-CimInstance Win32_OperatingSystem).TotalVisibleMemorySize/1MB   # 35.8 GB
(Get-CimInstance Win32_Processor | Measure-Object NumberOfLogicalProcessors -Sum).Sum  # 12
```

### 2. 写入配置

文件位置：`C:\Users\syske\.wslconfig`

```ini
[wsl2]
networkingMode=mirrored
memory=16GB
processors=8
swap=4GB

[experimental]
autoMemoryReclaim=gradual
sparseVhd=true
```

| 项 | 值 | 说明 |
|----|-----|------|
| networkingMode | mirrored | 镜像网络模式，共享 Windows 网络栈（代理可镜像进 WSL） |
| memory | 16GB | 给 WSL 分配一半内存，留足 Windows |
| processors | 8 | 12 线程中分配 8 |
| swap | 4GB | 交换空间 |
| autoMemoryReclaim | gradual | 闲置 5 分钟后自动缓慢回收缓存内存还给 Windows |
| sparseVhd | true | VHD 随使用自动缩小（实验特性） |

### 3. 关键坑点

- **`autoMemoryReclaim` / `sparseVhd` 必须放在 `[experimental]` 段**，放 `[wsl2]` 段会报 `wsl: Unknown key`。
- 修改 `.wslconfig` 后需 `wsl --shutdown` 重启才生效。

### 4. 现有发行版转换为 sparse VHD

`sparseVhd=true` 只对**新建** VHD 生效，已有发行版需手动转换：

```powershell
wsl --shutdown          # 必须先彻底关闭（含残留 vmmemWSL/wslrelay 进程退出）
wsl --manage Ubuntu-24.04 --set-sparse true --allow-unsafe
```

> `--set-sparse` 提示不安全需 `--allow-unsafe`；且发行版必须在 Stopped 状态，否则报 `WSL_E_DISTRO_NOT_STOPPED` 或 `ERROR_SHARING_VIOLATION`。转换仅标记文件，无数据风险。

### 5. 网络模式：镜像代理（消除 localhost 代理告警）

**现象**：Windows 配置了 localhost 代理（如 Clash/V2Ray，`127.0.0.1:7897`）后，每次启动 WSL 提示：

```
wsl: 检测到 localhost 代理配置，但未镜像到 WSL。NAT 模式下的 WSL 不支持 localhost 代理。
```

**根因**：WSL2 默认 **NAT 模式**，WSL 内的 `127.0.0.1` 指向 WSL 自身而非 Windows，代理无法镜像。

**方案**：`.wslconfig` 的 `[wsl2]` 段启用 `networkingMode=mirrored`（WSL 与 Windows 共享网络栈）：

```ini
[wsl2]
networkingMode=mirrored
memory=16GB
processors=8
swap=4GB

[experimental]
autoMemoryReclaim=gradual
sparseVhd=true
```

**效果**：
- 启动告警消失
- 代理环境变量（`http_proxy`/`https_proxy`/`no_proxy`）自动注入 WSL
- WSL 内可直接用 `127.0.0.1:<端口>` 访问 Windows 代理（实测连通）
- 代理端口变更时只需改系统代理设置，WSL 自动跟随

**注意**：
- 镜像模式与 NAT 共存，eth0 仍分配虚拟 IP，但网络栈共享
- **`localhostForwarding` 在镜像模式下无效**（会报 `wsl: 使用镜像网络模式时，wsl2.localhostForwarding 设置无效`），必须移除该行
- 依赖固定 WSL IP / 严格 NAT 隔离的服务可能受影响（一般无碍）
- 修改后需 `wsl --shutdown` 重启生效

---

## 十一、最终验证

```powershell
wsl --list --verbose
wsl -d Ubuntu-24.04 -- bash -c "whoami; free -h | head -2; nproc"
wsl -d Ubuntu-24.04 -- systemctl is-system-running   # running
```

结果：
```
NAME           STATE    VERSION
Ubuntu-24.04   Running  2
syske
Mem: 15Gi（16GB）
8
running
```

---

## 十二、使用方式速查

| 命令 | 说明 |
|------|------|
| `wsl` 或 `wsl -d Ubuntu-24.04` | 进入系统（默认 syske 用户） |
| `wsl --shutdown` | 关闭所有发行版（改配置后用） |
| `wsl --terminate <名称>` | 关闭指定发行版 |
| `wsl --manage Ubuntu-24.04 --set-sparse true --allow-unsafe` | 转换 sparse VHD |
| `nvm install 20` | 切换 Node 版本 |

系统盘为 ext4.vhdx（`D:\dev-tool\WSL\Ubuntu-24.04`），容量自动扩容，当前可用约 954G。

---

## 十三、安装配置 pi agent 与 opencode（参考 Windows 配置）

> 目标：将 Windows 端已配置好的 pi agent 与 opencode 完整同步到 WSL（Linux 原生版），包括认证、模型、插件、MCP、skills。

### 1. 检查现状

```bash
export NVM_DIR="$HOME/.nvm"
. "$NVM_DIR/nvm.sh"
which pi opencode        # 初始指向 Windows 版 (/mnt/d/tools/...)
pi --version
opencode --version
```

> 关键坑点：WSL 的 PATH 默认含 Windows 路径（`/mnt/d/...`），`which` 会先命中 Windows 的 npm shim 脚本。必须用 WSL 的 nvm node 装 Linux 原生版。

### 2. 安装 Linux 原生版

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
npm install -g opencode-ai
```

> 坑点：新版本 npm 默认拦截 postinstall 脚本（`allow-scripts` 安全机制），opencode 需要下载原生二进制，需显式放行：
> ```bash
> npm install -g --allow-scripts=opencode-ai opencode-ai
> ```

验证安装位置指向 WSL：
```bash
which pi        # ~/.nvm/versions/node/v24.19.0/bin/pi
which opencode  # ~/.nvm/versions/node/v24.19.0/bin/opencode
```

### 3. 同步 pi 配置

#### 认证（含 API key，脱敏）

```bash
mkdir -p ~/.pi/agent
cp /mnt/c/Users/syske/.pi/agent/auth.json ~/.pi/agent/auth.json   # 含 <DEEPSEEK_API_KEY>
cp /mnt/c/Users/syske/.pi/agent/models.json ~/.pi/agent/models.json
cp /mnt/c/Users/syske/.pi/agent/models-store.json ~/.pi/agent/models-store.json
```

`auth.json` 结构（密钥脱敏为占位符）：
```json
{
  "deepseek": {
    "type": "api_key",
    "key": "<DEEPSEEK_API_KEY>"
  }
}
```

#### settings.json

```json
{
  "lastChangelogVersion": "0.84.0",
  "theme": "dark",
  "defaultProvider": "deepseek",
  "defaultModel": "deepseek-v4-flash",
  "defaultThinkingLevel": "medium",
  "packages": [
    "npm:pi-powerline",
    "npm:pi-cache-optimizer",
    "npm:pi-web-access",
    "npm:@mjasnikovs/pi-task"
  ]
}
```

> WSL 路径注意：settings.json 中 `packages` 的安装目标是 `~/.pi/agent/npm/`（Linux 路径）。

#### trust.json（路径映射为 WSL 挂载路径）

```json
{
  "/mnt/d/workspace/ai-workspace": true
}
```

#### 安装 pi 包

```bash
pi install npm:pi-powerline
pi install npm:pi-cache-optimizer
pi install npm:pi-web-access
pi install npm:@mjasnikovs/pi-task
pi list    # 验证 4 个包已装入 ~/.pi/agent/npm/
```

#### 扩展配置（pi-rtk-optimizer）

```bash
mkdir -p ~/.pi/agent/extensions/pi-rtk-optimizer
cp /mnt/c/Users/syske/.pi/agent/extensions/pi-rtk-optimizer/config.json \
   ~/.pi/agent/extensions/pi-rtk-optimizer/config.json
```

### 4. 同步 opencode 配置

#### 认证

```bash
mkdir -p ~/.local/share/opencode
cp /mnt/c/Users/syske/.local/share/opencode/auth.json ~/.local/share/opencode/auth.json
cp /mnt/c/Users/syske/.local/share/opencode/account.json ~/.local/share/opencode/account.json
```

`auth.json` 结构（密钥脱敏）：
```json
{
  "deepseek": { "type": "api", "key": "<DEEPSEEK_API_KEY>" },
  "opencode": { "type": "api", "key": "<OPENCODE_API_KEY>" }
}
```

#### opencode.jsonc（WSL 适配版）

Windows 端 MCP 用 `C:\Users\syske\.pyenv\...\python.exe`，WSL 端改为系统 Python 并补充 PATH：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["opencode-history-search"],
  "mcp": {
    "code-review-graph": {
      "type": "local",
      "command": ["/usr/bin/python3", "-m", "code_review_graph", "serve"],
      "cwd": ".",
      "environment": {
        "HF_HUB_DISABLE_SYMLINKS_WARNING": "1",
        "PATH": "/usr/bin:/bin:/home/syske/.local/bin"
      },
      "timeout": 60000,
      "enabled": true
    }
  }
}
```

> `opencode-history-search` 是 npm/git 插件，opencode 首次运行会自动从插件缓存安装（`~/.cache/opencode/packages/`），无需手动下载。

#### 安装 MCP 依赖（code-review-graph）

```bash
sudo apt-get -y install python3-pip python3-venv
/usr/bin/python3 -m pip install --break-system-packages \
  -i https://pypi.tuna.tsinghua.edu.cn/simple code-review-graph
```

> 坑点：WSL 里 `pip3` 可能指向 Windows 的 pyenv shim（无法执行），必须用 `/usr/bin/python3 -m pip`。`--break-system-packages` 是 Ubuntu 24.04 外部管理环境的必需参数。

#### 同步 skills

Windows 端 `~/.config/opencode/skills` 是 junction（reparse point），drvfs 无法穿透，`cp` 或 `cd` 会报 `Permission denied`。解法：在 Windows 侧用 robocopy 先复制到临时目录（排除 `.git`/`_archive`/`.system`），WSL 再从 `/mnt/c` 复制：

```powershell
# Windows 侧
robocopy "C:\Users\syske\.config\opencode\skills" "C:\...\Temp\skills_stage" /E /XD .git _archive .system
```

```bash
# WSL 侧
mkdir -p ~/.config/opencode/skills
cp -r /mnt/c/.../skills_stage/* ~/.config/opencode/skills/
```

同步结果：codegraph-helper、coolreview、find-skills、grilling、karpathy-guidelines、superpowers 共 6 个启用中的 skills。

#### 同步 opencode 全局插件（Witty-Skill-Insight）

```bash
mkdir -p ~/.opencode/plugins
cp /mnt/c/Users/syske/.opencode/plugins/* ~/.opencode/plugins/
cp /mnt/c/Users/syske/.opencode/package.json ~/.opencode/
cp /mnt/c/Users/syske/.opencode/package-lock.json ~/.opencode/
cd ~/.opencode && npm install
```

#### 安装 @opencode-ai 依赖

```bash
cd ~/.config/opencode && npm install   # 安装 @opencode-ai/plugin、sdk
```

> 坑点：npm 12.x 项目级安装不允许 `--allow-scripts`，直接 `npm install` 即可；个别包（msgpackr-extract）会有 allow-scripts 警告，不影响使用。

### 5. 验证

```bash
pi --version                       # 0.84.1
pi models                          # 显示 deepseek-v4-flash (active) / deepseek-v4-pro
opencode --version                 # 1.18.16
opencode models                    # 列出 opencode/deepseek 全部模型
```

端到端测试：
```bash
opencode run --model opencode/deepseek-v4-flash-free "reply OK"
# → OK
```

### 6. 遇到的坑点汇总

| 坑点 | 现象 | 解决 |
|------|------|------|
| PATH 命中 Windows 版 | `which pi` 指向 /mnt/d/tools | 用 nvm 的 npm 装 Linux 版 |
| npm 拦截 postinstall | opencode 装完无二进制 | `npm install -g --allow-scripts=opencode-ai` |
| pip 指向 Windows shim | `pip3` 报 cannot execute | 用 `/usr/bin/python3 -m pip` |
| Ubuntu 外部管理环境 | pip 拒绝安装 | 加 `--break-system-packages` |
| skills 是 junction | drvfs 报 Permission denied | Windows 侧 robocopy 中转 |
| npm 12 项目级 --allow-scripts | 报 EALLOWSCRIPTS | 去掉该参数直接 install |

---

## 十四、Git 提交测试（WSL git + SSH）

WSL 配置好 git 后，用它提交并推送文档到 GitHub 验证（SSH 凭证生效）：

```bash
cd /mnt/d/workspace/learning/note
git add "linux/wsl/WSL2-Ubuntu24.04-完整安装与推荐配置.md"
git commit -m "docs: WSL2 + Ubuntu 24.04 完整安装与推荐配置"
git push origin master
```

> 注意：WSL 视角下仓库大量文件显示为 modified，是 WSL/Windows 的 line-ending（autocrlf）差异导致，非真实改动。提交时只 `git add` 目标文件，不要 `git add .`。

已提交示例：
- `3a499d6` WSL 完整安装配置文档
- `a41595c` sofa-rpc 压测

---

## 十五、zsh + oh-my-zsh 终端环境

将 zsh 设为 WSL 日常主力 shell（比 bash 补全更强、可高度定制）。

### 1. 安装 zsh

```bash
sudo apt-get -y install zsh git curl
zsh --version    # zsh 5.9
```

### 2. 安装 oh-my-zsh

```bash
RUNZSH=no CHSH=no KEEP_ZSHRC=yes sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

> 坑点：若 GitHub clone 中断，`~/.oh-my-zsh` 可能只剩 `.git` 目录（不完整），安装脚本报 "The $ZSH folder already exists"。解法：`rm -rf ~/.oh-my-zsh` 后重装。

### 3. 安装常用插件

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions $ZSH_CUSTOM/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
```

### 4. 配置 .zshrc

```bash
sed -i 's/^ZSH_THEME="robbyrussell"/ZSH_THEME="agnoster"/' ~/.zshrc
sed -i 's/^plugins=(git)/plugins=(git z zsh-autosuggestions zsh-syntax-highlighting)/' ~/.zshrc
```

追加 nvm 集成与别名：
```bash
cat >> ~/.zshrc << 'EOF'

# nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# 常用别名
alias ls='ls --color=auto'
alias ll='ls -lah'
alias la='ls -la'
alias grep='grep --color=auto'
alias py='python3'
alias oc='opencode'

# Windows 互操作
alias win='cmd.exe /c'
alias psh='powershell.exe'
EOF
```

> 重要：`.zshrc` 中必须保留 nvm 初始化（`NVM_DIR` 块），否则新 zsh 会话中 node/npm 不可用（nvm 的 node 依赖 PATH 注入）。

### 5. 设置默认 shell

```bash
sudo usermod -s /usr/bin/zsh syske
```

> 坑点：`chsh -s /usr/bin/zsh` 会走 PAM 密码认证，即使 sudoers 配了 NOPASSWD 也会因需要用户密码而失败（Authentication failure）。改用 `sudo usermod -s` 可绕过。

### 6. 验证

```bash
zsh -i -c 'echo $ZSH_THEME; echo $plugins; node -v; git config user.name'
```

输出应包含：agnoster / git z zsh-autosuggestions zsh-syntax-highlighting / v24.19.0 / syske。

### 7. 使用体验

- **命令建议**：输入时灰色自动补全，按 `→` 接受
- **语法高亮**：命令正确显示绿色、错误红色
- **快速跳转**：`z 目录名` 跳到历史访问过的目录
- **git 信息**：agnoster 主题在提示符显示当前分支/工作区状态

---

## 十六、ai-system × WSL 集成

> 目标：让 `D:\workspace\ai-workspace\ai-system`（aic CLI 编排引擎）在 WSL 内可用，能正确解析 Linux 路径并启动 WSL 原生版 opencode/pi。

### 1. 背景与核心障碍

ai-system 是一个 Python CLI（`aic`），通过 `subprocess.call(shell=True)` 启动 agent（opencode/pi/claude）。默认环境配置 `config/environments/local.yaml` 使用 **Windows 绝对路径**（`D:\workspace\...`）。

- 在 WSL 中 Python 的 `Path("D:\...")` 会解析为**相对路径**（`PosixPath('/mnt/d/.../D:/workspace/...')`），导致所有路径错误。
- `aic` 命令默认命中 Windows 的 pyenv shim（`/mnt/c/Users/syske/.pyenv/pyenv-win/shims/aic`），在 Linux 下不可执行。

### 2. 解决方案：新增 WSL 环境配置

ai-system 原生支持 `--environment <name>`，按 `config/environments/<name>.yaml` 加载。新建 `config/environments/wsl.yaml`：

```yaml
workspace:
  root: /mnt/d/workspace/ai-workspace
  repository_root: /mnt/d/workspace/ai-workspace/projects

build:
  backend: maven   # WSL 无 IDEA，使用 maven CLI 后端

layers:
  ai_system:
    path: /mnt/d/workspace/ai-workspace/ai-system
  projects:
    path: /mnt/d/workspace/ai-workspace/projects
  methodologies:
    path: /mnt/d/workspace/ai-workspace/methodologies
  skills:
    path: /mnt/d/workspace/ai-workspace/extensions
```

### 3. WSL 内安装依赖

```bash
cd /mnt/d/workspace/ai-workspace/ai-system
python3 -m pip install --break-system-packages \
  -i https://pypi.tuna.tsinghua.edu.cn/simple \
  PyYAML pyperclip prompt_toolkit
python3 -m pip install --break-system-packages --no-build-isolation -e .
# aic 安装到 /home/syske/.local/bin/aic
```

### 4. 修复 PATH 优先级（关键）

WSL 默认会把 Windows PATH 追加进来，导致 `opencode/pi` 命中 `/mnt/d/tools/node-v24.18.0-win-x64/` 的 Windows 版，`aic` 命中 pyenv shim。需要在**各 shell 配置文件**中把原生 bin 提前。

**`~/.zshrc` 追加**（日常交互 shell）：

```bash
export PATH="$HOME/.local/bin:$PATH"
export PATH="$NVM_BIN:$PATH"
```

**`~/.bashrc` 与 `~/.profile` 追加**（`subprocess.call` / `bash -lc` 等非交互场景）：

```bash
if [ -n "$NVM_BIN" ]; then
    export PATH="$NVM_BIN:$HOME/.local/bin:$PATH"
fi
```

验证：

```bash
which aic opencode pi
# 应输出:
# /home/syske/.local/bin/aic
# /home/syske/.nvm/versions/node/v24.19.0/bin/opencode
# /home/syske/.nvm/versions/node/v24.19.0/bin/pi
```

> 注意：`aic` 通过 `subprocess.call(shell=True)` 启动 agent 时，子进程继承 aic 进程自身的 PATH。只要从 zsh 启动 aic（PATH 已含 nvm bin），链路即正确。

### 5. 使用方式

```bash
# 交互向导（项目选择 → workflow 选择 → 启动 opencode）
aic --environment wsl

# 非交互生成 prompt
aic verify --environment wsl --project demo
```

### 6. 日常使用建议

**WSL 无需常驻**：WSL2 是 VM 架构，最后一个 WSL 进程退出后约 8 秒自动关闭并释放内存；`.wslconfig` 的 `memory=16GB` 是上限而非预留，`autoMemoryReclaim=gradual` 会在空闲 1 分钟后逐步归还缓存内存。日常正常使用 CLI 不会常驻占内存。

**任务归属**：

| 场景 | 用哪个 | 原因 |
|------|--------|------|
| 跑 `aic` / opencode / pi（AI 编排） | WSL | 已集成 `--environment wsl`，命中原生 agent |
| 日常编码、git、Linux 工具链 | WSL | 文件系统 IO 快、工具全 |
| Windows 专属（IDEA、Office、PowerShell 脚本） | Windows | 无替代 |

**关键实践**：

1. **统一从 WSL 操作代码**：`D:\workspace\...` 在 WSL 里是 `/mnt/d/workspace/...`（9P 协议，比 WSL 原生 fs 慢）。避免两套工具交替改同一文件（行尾/权限会互相干扰）。
2. **跑 ai-system**：进 WSL 后 `cd` 到项目目录，直接 `aic --environment wsl`，PATH 已收敛无需额外设置。
3. **用完即走**：退出终端 WSL 自动关闭；改 `.wslconfig` 后需 `wsl --shutdown` 重启生效，其余情况无需手动关机。
4. **访问 Windows 文件**：用 `/mnt/c/...`、`/mnt/d/...` 直接读写，不要用 `cmd.exe` 反向操作 WSL 文件。
5. **可选加速**：在 `.zshrc` 加 `export CDPATH=/mnt/d/workspace/ai-workspace` 快速跳转，或把 Windows 的 `workspace-config.ps1` 别名同步到 `.zshrc` 统一体验。

### 7. 验证结果

| 项目 | 状态 |
|------|------|
| `paths(root, 'wsl')` 路径解析 | 全部存在 |
| `tools/check.py` | PASS（3 个原有 warning）|
| provider 元数据 | opencode/pi/claude 正常加载 |
| `aic verify --environment wsl` | exit 0，prompt 生成正常 |
| 交互向导（项目/ workflow 选择） | 正常流转 |
| subprocess 调 agent（PATH 继承） | 命中 WSL 原生版 |

之后 `wsl` 或 `wsl -d Ubuntu-24.04` 进入即默认 zsh。
