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
git config --global user.email "715448004@qq.com"
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
localhostForwarding=true
memory=16GB
processors=8
swap=4GB

[experimental]
autoMemoryReclaim=gradual
sparseVhd=true
```

| 项 | 值 | 说明 |
|----|-----|------|
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
