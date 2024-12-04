最近除了折腾`N1`盒子外，还折腾了笔记本电脑的`linux`系统，从大学接触`linux`开始就一直给笔记本安装的是双系统，但是因为通过铜豌豆工具给`ubuntu`安装原生微信，导致系统进不去了（挺尴尬），尝试了多种修复方式，都不奏效，于是一不做二不休就考虑换个系统，再三考虑之后，最终选择了`arch linux`，原因有三个：
- 稳定性高一点，滚动式发布，而且社区活跃都高
- 生态丰富，有好多开源的软件库
- 之前把玩过一段时间`manjaro`还算熟悉
虽然，之前在一个老笔记本上安装过，但是最终由于太卡了，也没能折腾下来，所以这一次也踩了很多坑，下面是详细记录：
### 镜像下载刻录

#### 下载
直接官网下载，选择国内的镜像站
```
https://archlinux.org/download/#http-downloads
```

这里我强烈推荐【南阳理工学院】的开源站，速度嘎嘎好，比阿里云、清华等下载速度快，分分钟下载完成：

```
https://mirror.nyist.edu.cn/archlinux/iso/2024.12.01/
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/5ec7bcdf-49d4-4ccb-b85b-54bab8fef1b8.jpg)

#### 镜像刻录

这里需要准备一个`USB2.0`的`U`盘，我用的是`sd`加读卡器，然后用`balenaEtcher`刻录镜像:

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/db841b90-dcbc-4f20-80e1-b6fe45f230e1.jpg)

#### 启动安装

刻录完成后，选择`live`方式进入系统：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/25508b41-49e2-4906-8f7f-0b68539de67c.jpg)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/92c0f5d5-23b8-43f4-a67d-db1792ed84b9.jpg)

### 安装
#### 安装准备 

从我多次实际踩坑的感受来说，安装步骤主要如下：
- 基本设置：设置字体
- 配置网络，修改软件源
- 系统分区
- 磁盘挂载
- arch-chroot
- 安装桌面系统
- 安装常用软件

其中设置字体、配置网络、修改软件源、系统分区、磁盘挂载都属于准备工作，后面的都属于正式的安装，下面我们来逐个看下这些过程：

#### 基本设置

由于这里我们主要分享的是`arch linux`的安装过程，所以不过多介绍引导启动相关内容，关于`UEFI`的相关设置可以根据自己的机型自行设置。

需要特殊说明的是，本次教程是基于`UEFI`模式启动的，可以通过下面的命令，确认是否是`UEFI`模式：

```sh
cat /sys/firmware/efi/fw_platform_size
```
如果结果是`32`或者`64`，说明我们就是`UEFI`模式启动

##### 设置窗口字体

根据自己的屏幕分辨率设置，具体的字体取值可以看下`/usr/share/kbd/consolefonts`，如果显示合适，可以不调整。

```sh
$ setfont ter-128b
```

对于同一个字体比如我这里的`ter-xxxb`，数字越大表示字体越大，选择一个合适的大小就行。


#### 配置网络

这里网络只介绍无线网络连接方式，工具用的是`iwctl`，进入系统默认是安装的

```sh
# 直接进入无线网络管理工具
iwctl

# 查看网络设备
device list
```

 输出结果大致如下，正常情况展示的应该是wlan0，由于截图是在虚拟机，所以展示是空的
```
                       Devices
------------------------------------------------------
Name   Address            Powered  Adapter  Mode
------------------------------------------------------
wlan0  xx:xx:xx:xx:xx:xx  on       phy0     station
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/54c35a58-5a97-4370-883e-436aaf5122e9.jpg)

```
# 扫描无线网络
station wlan0 scan
```

正常情况会输出无线网络列表，这里没有拍照保留，就不展示了。

```
# 连接指定的wifi，这里的syske-wifi换成你的wifi名称
station wlan0 connect syske-wifi
# 然后根据提示输入wifi密码
```
之后`ping`下看网络是否连接成功：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/befbf64f-3131-47c5-b118-4774517cd844.jpg)

网络配置`ok`之后，我们开始修改软件源镜像。

#### 修改软件源

在修改软件源之前先更新下系统时钟，确保后续签名校验正常：

```sh
timedatectl
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/527e97a5-5d21-4c02-82b6-8ac4df33a1dd.jpg)



修改`mirrorlist`文件，在最上面的`Server`前面加入镜像站，我这里还是用的南阳理工学院的开源软件镜像站。

这里用的软件是`nano`，`ctrl + o`保存，`ctrl + x`退出

```sh
nano /etc/pacman.d/mirrorlist

# 加入下面的地址
Server = https://mirror.nyist.edu.cn/archlinux/$repo/os/$arch
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/d640e8c0-f54e-4d9f-b8e8-bc3e2ae478ef.jpg)
如果你的`mirrorlist`是这样的也不影响，
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/6a09d1e6-97ad-4d65-b827-4c359c052cc0.jpg)

然后更新下系统：
```sh
pacman -Syu
```

#### 系统分区

首先通过`fdisk`确认我们的磁盘分区，确认我们要在哪个磁盘上创建我们的系统分区。由于我安装的是`win + arch`双系统，所以我提前已经有一个空置的磁盘分区了，可以直接在空置的磁盘区域上进行分区，没有磁盘空间的小伙伴可以通过 `win`系统的磁盘管理工具进行压缩卷：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/a75af285-87c7-499d-a04c-343ccd1a3b4e.jpg)

通过`fdisk`查看磁盘分区情况
```
fdisk -l
```

这里我的磁盘是`/dev/nvme0n1`，所以下面我要操作的就是这个磁盘
```sh
fdisk /dev/nvme0n1
```
`fdisk`是一个强大的磁盘管理工具，我们通过如下命令管理磁盘分区：
- d : 删除分区，按照提示输入分区编号
- n : 创建分区，按照提示输入分区大小、开始等数据
- p : 打印分区表，用于展示分区情况
- t : 改变分区类型
- w : 写入分区结果（写入后不可撤销，谨慎操作）
- q : 不保存退出
- g : 创建`GPT`分区表

由于我是安装双系统，所以直接分区即可，过程大致如下：

```
root@archiso ~ # fdisk /dev/nvme0n1  # 请将 nvme0n1 更换为您的设备名，如 sda

Welcome to fdisk (util-linux 2.x).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Command (m for help): p  # 输入 p 打印分区表，检查已有的分区。我们有 260 MiB 大小的 EFI 分区和 16 MiB 大小的 reserved 分区，以及 200 GiB + 125.7G 大小的 C 盘和 D 盘，还有1000M的windows recovery分区，另外就是我压缩出来要安装arch linux的分区了

Disk /dev/sda: 29.16 GiB, 31312576512 bytes, 61157376 sectors
Disk model: Storage device
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: doc
Disk identifier: xxxxxxxx

Device           Start        End   Sectors   Size   Type
/dev/nvme0n16p1           64      2004991   2004928   979M    Empty
/dev/sda2      2004992   2363391    358400    175M  EFI (FAT-12/16/32)

Command (m for help): n  # 输入 n 创建新的分区，这个分区将是根分区
Partition number (5-128, default 5):  # 分区编号保持默认，直接按 Enter
First sector (210282496-315831057, default 210282496):  # 第一个扇区，保持默认
Last sector, +/-sectors or +/-size{K,M,G,T,P} (210282496-315831057, default 315831057): +50G  # 创建 50 GiB 大小的根分区，您可以根据自己的硬盘空间决定根分区的大小

Created a new partition 5 of type 'Linux filesystem' and of size 50 GiB.

Command (m for help): t  # 输入 t 改变分区类型，请勿遗忘此步
Partition number (1-5, default 5):   # 保持默认
Partition type or alias (type L to list all): 23  # 输入 23 代表 Linux root (x86-64) 类型
Changed type of partition 'Linux filesystem' to 'Linux root (x86-64)'.

Command (m for help): n  # 输入 n 创建新的分区，这个分区将是 home 分区
Partition number (6-128, default 6):   # 保持默认
First sector (252225536-315831057, default 252225536):   # 保持默认
Last sector, +/-sectors or +/-size{K,M,G,T,P} (252225536-315831057, default 315831057):   # 保持默认，将剩余空间全部分给 home 分区

Created a new partition 6 of type 'Linux filesystem' and of size 30.3 GiB.

Command (m for help): t  # 输入 t 改变分区类型
Partition number (1-6, default 6):   # 保持默认
Partition type or alias (type L to list all): 42  # 输入 42 代表 Linux home 类型
Changed type of partition 'Linux filesystem' to 'Linux home'.

Command (m for help): p  # 输入 p 打印分区表，请检查分区是否有误，如果有误，请输入 q 直接退出

Disk /dev/sda: 150.6 GiB, 161705518592 bytes, 315831091 sectors
Disk model: xxx
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disklabel type: gpt
Disk identifier: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

Device        Start        End   Sectors   Size  Type
/dev/sda1      2048     534527    532480   260M  EFI System
/dev/sda2    534528     567295     32768    16M  Microsoft reserved
/dev/sda3    567296  105424895 104857600    50G  Microsoft basic data
/dev/sda4 105424896  210282495 104857600    50G  Microsoft basic data
/dev/sda5 210282496  252225535  41943040    50G  Linux root (x86-64)
/dev/sda6 252225536  315830271  63604736  30.3G  Linux home

Command (m for help): w  # 输入 w 写入分区表，该操作不可恢复
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
```


#### 挂载目录 

```
# root分区挂载
mount /dev/nvme0n1p6 /mnt

# EFI 分区挂载
mount --mkdir /dev/nvme0n1p1 /mnt/boot
# home分区挂载
mount --mkdir /dev/sda3 /mnt/home
```

### 安装桌面环境

```sh
sudo pacman -S plasma kde-applications packagekit-qt5
```


### 安装中文输入法

#### 安装核心依赖

```sh
sudo pacman -S fcitx5 fcitx5-gtk fcitx5-configtool fcitx5-qt fcitx5-chinese-addons fcitx5-material-color kcm-fcitx5 fcitx5-lua

```

#### 配置环境

```sh
sudo vim /etc/environment 
```

```sh
# sougou pin yin input config
GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS=@im=fcitx
```

### 安装常用应用

#### 知识库软件

强烈推荐，我觉得很好用

```sh
yay -S obsidian
```

#### 国内常用软件

##### google chrome

```sh
yay -S google-chrome
```

##### dingtalk

```sh
yay -S dingtalk-bin
```

##### wechat

目前可以安装最新版本的原生`linux`版本微信，是基于`qt`开发的
```sh
yay -S wechat
```


[官方安装指南](https://wiki.archlinuxcn.org/wiki/%E5%AE%89%E8%A3%85%E6%8C%87%E5%8D%97)