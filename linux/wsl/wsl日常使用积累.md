### 迁移wsl到D盘

```sh
# 停用wsl
wsl --shutdown
# 导出要迁移的wsl
wsl --export archlinux D:\dev-tool\archlinux.tar

# 取消注册
wsl --unregister archlinux

# 重新导入
wsl --import archlinux D:\dev-tool\wsl\archlinux  D:\dev-tool\archlinux.tar
```

迁移过程，可以通过下述命令来查看`wsl`信息：
```sh
wsl -l
```

---

### WSL 突然「已退出进程，代码为 1」怎么判（2026-11-12）

**现象**：Windows Terminal 打出
```
[已退出进程，代码为 1 (0x00000001)]
现在可以使用 Ctrl+D 关闭此终端，或按 Enter 重新启动。
```

**这个提示有两种完全不同的原因，必须靠 dump 区分，不能凭提示判定崩溃：**

| 原因 | 特征 | 处置 |
|------|------|------|
| ① 正常：WSL 空闲自动关机 | 最后一个 WSL 进程退出后约 8 秒 VM 自动关闭；**无 dump** | 重开终端即可 |
| ② 崩溃：guest 内核 panic | `%LOCALAPPDATA%\Temp\wsl-crashes\` 下出现新的 `kernel-panic-*.txt` | 见下方处置 |

**判别命令（第一步永远是看有没有新 dump）**
```bash
ls -l --time-style=+%m-%d\ %H:%M /mnt/c/Users/71544/AppData/Local/Temp/wsl-crashes/
uptime   # 对比 uptime 与 dump 时间：VM 是否刚重启
```

**实例：2026-11-12 本机一天内三次**

| dump | panic 时刻 | 该 VM uptime | 之后的新 boot | 内核 |
|------|-----------|--------------|---------------|------|
| `kernel-panic-1794462973-{ef0d3300…}.txt` | 13:56:13 | 190284s ≈ 52.9h | 13:56:21 | 6.18.58.1 |
| `kernel-panic-1794463755-{d5610e99…}.txt` | 14:09:15 | 779s ≈ 13min | 14:09:22 | 6.18.58.1 |
| `kernel-panic-1794464557-{c451ec89…}.txt` | 14:22:43 | 352s ≈ 6min | 14:22:43 | **6.6.87.1**（回退后仍 panic） |

三份 dump 同构（WSL 3.0.5.0 + Win 10.0.26300.9711 / 26H2）：
```
mce: [Hardware Error]: CPU 1: Machine Check Exception: 4 Bank 0: b200000080060001
mce: [Hardware Error]: PROCESSOR 0:c0652 … APIC 1 microcode ffffffff
mce: [Hardware Error]: Machine check: Processor context corrupt
Kernel panic - not syncing: Fatal machine check
```

**判读要点**
- `MCi_STATUS=0xB200000080060001` → VAL/UC/**PCC** 置位：未纠正 + 处理器上下文损坏，内核无恢复路径，只能 panic。
- **dump 里没有 `MCi_ADDR`/RIP 行**（ADDRV=0、MISCV=0），`MCACOD=0x0001` 不在内存控制器错误码区间 → 寄存器内容不指向 DRAM。
- 宿主 30 天 `Microsoft-Windows-WHEA-Logger` = **0** 条、无 `Kernel-Power 41/6008` → Windows 侧没记硬件错误、没蓝屏，MCE 是「只进 guest」的。
- guest 内存充裕（15Gi 中仅用 2.8Gi、swap 0）、无 oom-killer → guest 侧不是 OOM。
- **但宿主侧高度相关（3/3）**：每次 panic 同一秒附近都有一条 `Microsoft-Windows-Resource-Exhaustion-Detector` **事件 2004「虚拟内存不足」**（13:56:14 / 14:09:15 / 14:22:38，当时 vmmemWSL 占 commit 10.3–13.3GB、idea64 4.9GB）。
  - 基线校准：当日 2004 共 10 次，只有最后 3 次对应 panic（11:29–13:08 的 7 次没崩）→ **内存耗尽是相关但非充分条件**，机制未明（真正的内存硬件错误应带 MCi_ADDR 且宿主 WHEA 会有记录）。
- 三次 panic 的内存使用量差异巨大（53h vs 13min vs 6min）但状态码完全相同 → 同一触发源。

**尝试①：回退内核（❌ 已证伪）** —— 回退后 6 分钟又 panic（14:22:43，6.6.87.1），说明**不是 guest 内核版本回归**。

```ini
# C:\Users\71544\.wslconfig
[wsl2]
memory=16GB
processors=8
swap=4GB
networkingMode=mirrored
kernel=C:\\Users\\71544\\wsl-kernels\\bzImage-6.6.87.1   # ← 回退到 6.6.87.1

[experimental]
sparseVhd=true
```
```powershell
wsl --shutdown   # 之后重开终端，uname -r 应为 6.6.87.1-microsoft-standard-WSL2
```

> ⚠️ **段归属坑（两个方向相反，极易搞混）**
> - `kernel=` 必须在 **`[wsl2]`**；
> - `autoMemoryReclaim` / `sparseVhd` 必须在 **`[experimental]`**（放 `[wsl2]` 会报 `wsl: Unknown key`）。
> 本机原配置把 `kernel=` 注释在 `[experimental]` 段下，位置无效 —— 取消注释也不会生效。

**回滚安全网（不依赖 WSL 能启动）**
- `C:\Users\71544\.wslconfig.bak-20261112-141615-before-kernel-rollback`（原始配置）
- `C:\Users\71544\revert-wslconfig.cmd`（双击即恢复备份 + `wsl --shutdown`）

**观察判据（24–48h）**：`wsl-crashes` 目录是否出现**新的** dump（基线：13:56:13 / 14:09:15 / 14:22:43 三个）。出现新文件即该尝试无效。

**尝试②：消除宿主 commit 耗尽（待验证）**
```ini
[wsl2]
memory=10GB          # 16GB 会让 vmmemWSL commit 冲到 13GB，而宿主 commit 上限仅 47.2GB
processors=8
swap=4GB
networkingMode=mirrored

[experimental]
autoMemoryReclaim=gradual   # 笔记推荐过但真机没落地，闲置即归还缓存
sparseVhd=true
```
同时：提高页面文件（自动管理→显式 32GB，抬高 commit limit）、IDEA(4.7GB commit)/Chrome/企业微信 按需关。

**页面文件实测（2026-11-12 14:35）**
```
PagingFiles = ["C:\pagefile.sys 2048 4096", "D:\pagefile.sys 32768 32768"]
效果：commit limit 45.6 GB → 72.7 GB（无需重启即生效，D:\pagefile.sys 32GB 已创建）
      committed 40.8 GB / 72.7 GB = 56%（余量 32GB）
```
> ⚠️ 坑：`New-CimInstance -ClassName Win32_PageFileSetting -Property @{InitialSize=32768;...}` 会报
> 「属性 InitialSize 的类型不匹配」——该属性是 UInt32，哈希表里的 32768 被当 Int32 传。
> 加 `[uint32]` 转换，或直接写注册表
> `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management` 的 `PagingFiles`（REG_MULTI_SZ，格式 `路径 初始MB 最大MB`）。
>
> ⚠️ 关键：**`InitialSize` 决定 commit limit**（limit = 物理内存 + 各页面文件当前大小），
> `MaximumSize` 只是天花板、不参与计算。所以初始值给小了（如 8GB）等于没改；
> 只调 MaximumSize 没有任何意义。

**若仍 panic，按此阶梯逐步验证（每步 24h）**
1. 装 `C:\Users\71544\wsl-kernels\wsl.2.5.7.0.x64.msi`（WSL 版本整体回退；此时内核已是配套的 6.6.87.1）
2. `[wsl2] nestedVirtualization=false`（guest 里 `kvm_intel` 在 boot 3.4s 就加载，是最大未知变量）
3. 硬件侧：BIOS 307(2026/04/30) 升级、恢复默认档（不 undervolt/OC/XMP）、`mdsched.exe`
4. 报上游：附 dump + `wsl --version` + CPU/BIOS + 「host WHEA=0」；症状帖 microsoft/WSL#8524，同签名 #13258

**无关项（已排除，避免重复排查）**
- `/tmp/pi-clipboard-*.png`：pi 的图片粘贴落盘文件（`alt+v` 写 `$TMPDIR`、插入路径、从不删除），与崩溃无因果；panic 重启时 `systemd-tmpfiles --boot` 会清空 `/tmp`，所以它们会「莫名消失」。
- 终端本身：Windows Terminal 只是显示 `wsl.exe` 的退出码，是乘客不是原因 —— 判别看 `boot_id`/`uptime` 是否重置（VM 重启）还是仅窗口关闭（VM uptime 连续）。

**已知无害噪声**：dump 与 `dmesg` 里成片的 `WSL (130) ERROR: CheckConnection: getaddrinfo() failed: -5` + `connect() failed: 101`，属 mirrored 网络的 DNS 探测失败，不影响使用。