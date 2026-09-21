# Arch Linux 安装企业微信（Wine 方案）

> 归档时间：2026-09-21
> 环境：Arch Linux / KDE Plasma 6 (Wayland) / 华硕 ExpertBook P3455
> 版本：WXWork 5.0.0.6008（企业微信 Linux 版）

---

## 结论先行

- **企业微信官方没有 Linux 原生版**（2026-09 确认，与 QQ、微信不同，后两者已有官方 Linux 版），只能通过 Wine 运行。
- 程序文件来自 AUR 包 `com.qq.weixin.work.deepin`（Deepin-wine 打包，自带 5.0 版程序），但 **deepin-wine 自带的 wine（wow64 实验模式）与 WXWork 5.0 不兼容**，无法直接运行。
- **最终方案：用 Arch 官方 wine 11 + 全新容器**运行 WXWork，稳定驻留、零错误。
- 已配置桌面图标「企业微信」+ 启动脚本 `~/.local/bin/wecom`。

---

## 1. 安装 AUR 包（获取 WXWork 程序文件）

`com.qq.weixin.work.deepin` 依赖两个 deepin-wine 运行环境和 spark 助手，全部走 AUR 手动流程（本机未装 AUR helper）：

```bash
cd ~/aur
# 依赖链: 按顺序 clone
git clone https://aur.archlinux.org/deepin-wine8-stable.git
git clone https://aur.archlinux.org/deepin-wine10-stable.git
git clone https://aur.archlinux.org/spark-dwine-helper.git
git clone https://aur.archlinux.org/com.qq.weixin.work.deepin.git

# 每个包: 先装系统依赖(可查 PKGBUILD 的 depends), 再构建安装
# 系统依赖都在官方仓库: alsa-lib glibc dbus ... zenity p7zip python-pyqt5 等
sudo pacman -S --noconfirm <depends...>
makepkg --noconfirm          # 不带 -s, 避免 makepkg 调 sudo 卡交互
sudo pacman -U *.pkg.tar.zst
```

> **代理注意**：`spark-dwine-helper`（GitHub releases deb）和主包（GitHub 上的 wqy-microhei.ttc 字体）需要代理下载：
> `export http_proxy=http://127.0.0.1:7897 https_proxy=http://127.0.0.1:7897` 再 `makepkg`。

## 2. 关键坑：deepin-wine 的 wow64 与 WXWork 5.0 不兼容

### 现象
WXWork.exe 启动后**静默退出**（无窗口、无报错），退出码 53。

### 诊断（用 WINEDEBUG=+process,+loaddll 逐步定位）
```
err:module:import_dll Loading library COMCTL32.dll (needed by DuiLib.dll) failed (c0000020)
err:module:import_dll Library DuiLib.dll (needed by WXWork.exe) not found
err:module:loader_init Importing dlls for WXWork.exe failed, status c0000135
```

### 根因
- WXWork.exe 是 **PE32 i386（32 位）** 程序，依赖 `DuiLib.dll`（自带，在 `5.0.0.6008/` 子目录）+ 系统 `comctl32.dll`。
- deepin-wine8/10 的 wow64 是 **"experimental wow64 mode"**，加载 32 位内置 DLL（comctl32 等）失败 → 连带 DuiLib 报 not found。
- 补充：deepin-wine 的容器内系统 DLL 是**软链接**（指向 /opt/deepin-wineXX/lib），用官方 wine 跑该容器还会报 `create_dest_file failed (error=80)` 冲突。

## 3. 终极方案：官方 wine 11 + 全新容器

### 3.1 启用 multilib 并安装官方 wine

```bash
# 编辑 /etc/pacman.conf, 取消 [multilib] 段注释 (Include = /etc/pacman.d/mirrorlist)
sudo pacman -Sy
sudo pacman -S wine     # 官方 wine 11.17, 完整 wow64, ~600M
```

### 3.2 用官方 wine 建全新容器（不能用 deepin 容器）

```bash
export WINEPREFIX=/home/syske/.deepinwine/WeCom-official
wineboot -u                                  # 初始化干净容器(~776M)
# 拷贝 WXWork 程序文件(真实文件, 非软链接)
cp -r "/home/syske/.deepinwine/Deepin-WXWork/drive_c/Program Files (x86)/WXWork" \
      "$WINEPREFIX/drive_c/Program Files (x86)/"
# 启动
wine "c:/Program Files (x86)/WXWork/WXWork.exe"
```

> 旧容器 `~/.deepinwine/Deepin-WXWork` 由 deepin-wine 创建、含软链接，官方 wine 无法复用。

### 3.3 固化启动（脚本 + 桌面图标）

`~/.local/bin/wecom`:
```bash
#!/bin/bash
export WINEPREFIX=/home/syske/.deepinwine/WeCom-official
exec /usr/bin/wine "c:/Program Files (x86)/WXWork/WXWork.exe" "$@"
```

`~/.local/share/applications/com.qq.weixin.work.deepin.desktop`（用户级覆盖系统入口）:
```ini
[Desktop Entry]
Name=企业微信
Exec=/home/syske/.local/bin/wecom
Icon=com.qq.weixin.work.deepin
Terminal=false
Type=Application
Categories=Network;InstantMessaging;
```

## 4. 使用说明

- 启动：开始菜单「企业微信」或终端 `wecom`
- 首次登录用手机企业微信扫码
- **Wine 版投屏/会议共享不可用**（同钉钉场景），日常聊天、审批、文件、工作台正常
- 界面字体/缩放不合适时用 `winecfg`（官方 wine）调 DPI

## 5. 其他踩坑记录

| 坑 | 说明 |
|---|---|
| deepin-wine 首次启动卡在缩放设置 | 缺 `DEEPIN_WINE_SCALE` 环境变量 → 脚本弹 GUI 等待；设 `DEEPIN_WINE_SCALE=2` 可跳过（仅 deepin 链需要，官方 wine 方案不需要） |
| sed 误伤 pacman.conf | 批量取消 `#Include` 注释时把 `#[core-testing]` 等注释段后的 Include 也启用了 → 孤立 Server 行落入 `[options]` 段报 warning；需把 testing 段（段名被注释）后的 Include 加回 `#` |
| makepkg 下载 GitHub 慢 | 设 http_proxy/https_proxy 走 Clash |
| WXWork 容器反复 wineboot | 中断初始化导致容器状态不完整；删除容器重建即可 |

## 6. 磁盘占用（可接受）

| 项 | 大小 |
|---|---|
| deepin-wine8-stable | 1.2G（WXWork AUR 包依赖，保留） |
| deepin-wine10-stable | 354M（同上） |
| 官方 wine | ~600M（含 lib32） |
| WeCom-official 容器 | ~776M + WXWork 程序 |
