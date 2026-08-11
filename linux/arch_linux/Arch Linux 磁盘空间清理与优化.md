# Arch Linux 磁盘空间清理与优化

## 背景

根分区 `/` 使用率 97%，仅剩 1.6G 可用空间。根分区大小 49G，主要集中在系统缓存、日志和冗余软件包。

## 磁盘分析

### 分区结构

| 挂载点 | 设备 | 大小 | 使用率 |
|--------|------|------|--------|
| `/` | /dev/nvme0n1p6 | 49G | 97% → **62%** |
| `/home` | /dev/nvme0n1p7 | 98G | 47% |
| `/boot` | /dev/nvme0n1p1 | 256M | 49% |

> `/home` 为独立分区，根分区的主要占用在 `/var`、`/opt`、`/usr` 等目录。

### 清理前空间占用 TOP

| 路径 | 大小 | 说明 |
|------|------|------|
| `/var/cache/pacman/pkg` | 9.7G | pacman 包缓存 |
| `/opt/rocm` | 4.8G | AMD ROCm 驱动（无 AMD GPU 时可卸载） |
| `/var/log/journal` | 2.4G | systemd 日志 |
| `/var/cache/debtap` | 1.1G | debtap 转换缓存 |
| `/var/cache/pkgfile` | 855M | pkgfile 缓存 |
| 孤儿包 | 464M | 56 个无依赖包 |

## 清理步骤

### 1. 清理 pacman 缓存

pacman 默认会保留所有已安装包的缓存，需要手动清理。

```bash
# 清理所有缓存包（仅保留当前安装的版本）
sudo pacman -Scc
```

> 也可设置缓存保留数量：编辑 `/etc/pacman.conf`，取消 `CleanMethod = KeepCurrent` 的注释。

### 2. 清理 systemd 日志

journalctl 默认无日志上限，会持续积累。

```bash
# 保留近 7 天日志
sudo journalctl --vacuum-time=7d
```

持久化限制（编辑 `/etc/systemd/journald.conf`）：

```ini
SystemMaxUse=500M
MaxFileSec=7day
```

### 3. 删除孤儿包

`pacman -Qdtq` 列出不再被依赖的包。

```bash
sudo pacman -Rns $(pacman -Qdtq)
```

### 4. 删除无用软件（按需）

如果硬件不需要，可以移除：

```bash
# AMD ROCm（NVIDIA 或核显用户）
sudo pacman -Rns rocm-core rocm-device-libs rocm-llvm rocm-opencl-runtime hsa-rocr
sudo rm -rf /opt/rocm
```

### 5. 清理其他缓存

```bash
# pkgfile 缓存（软件包文件名索引）
sudo pkgfile -u && sudo rm -rf /var/cache/pkgfile/*

# debtap 缓存（AUR deb 转换工具）
sudo rm -rf /var/cache/debtap/*

# /tmp 临时文件（重启自动清理，无需手动）
```

## 清理效果

| 指标 | 清理前 | 清理后 | 释放空间 |
|------|--------|--------|----------|
| 根分区使用率 | 97% | **62%** | **16G** |
| 可用空间 | 1.6G | **19G** | |

## 预防措施

### 限制 journal 日志大小

```bash
# /etc/systemd/journald.conf
SystemMaxUse=500M
MaxFileSec=7day
```

### 自动清理 pacman 缓存（安装后自动删除）

```bash
# 安装 pacman-contrib 提供的 paccache hook
sudo pacman -S pacman-contrib

# 启用每日清理服务
sudo systemctl enable --now paccache.timer
```

### 定期检查

```bash
# 快速查看根分区占用
df -h /

# 查看大目录
sudo du -sh /* 2>/dev/null | sort -rh | head -10

# 检查孤儿包
pacman -Qdtq

# 检查缓存目录大小
du -sh /var/cache/* | sort -rh
```
