最近除了折腾`N1`盒子外，还折腾了笔记本电脑的`linux`系统，从大学接触`linux`开始就一直给笔记本安装的是双系统，但是因为通过铜豌豆工具给`ubuntu`安装原生微信，导致系统进不去了（挺尴尬），尝试了多种修复方式，都不奏效，于是一不做二不休就考虑换个系统，再三考虑之后，最终选择了`arch linux`，原因有三个：
- 稳定性高一点，滚动式发布，而且社区活跃都高
- 生态丰富，有好多开源的软件库
- 之前把玩过一段时间`manjaro`还算熟悉
虽然，之前在一个老笔记本上安装过，但是最终由于太卡了，也没能折腾下来，所以这一次也踩了很多坑，下面是详细记录：
## 镜像下载刻录

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

## 安装
### 安装准备 

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
使用 `curl` 下载位于中国大陆的 `HTTPS` 镜像站：
```
curl -L "[https://archlinux.org/mirrorlist/?country=CN&protocol=https](https://archlinux.org/mirrorlist/?country=CN&protocol=https)" -o /etc/pacman.d/mirrorlist
```

也可以手动修改`mirrorlist`文件，在最上面的`Server`前面加入镜像站，我这里还是用的南阳理工学院的开源软件镜像站。

这里用的软件是`nano`，`ctrl + o`保存，`ctrl + x`退出

```sh
nano /etc/pacman.d/mirrorlist

# 加入下面的地址
Server = https://mirror.nyist.edu.cn/archlinux/$repo/os/$arch
# 阿里云的可以配置这个
Server = https://mirrors.aliyun.com/archlinux/$repo/os/$arch
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

```
[root@archiso ~]$ sudo fdisk /dev/nvme0n1 # 这里换成自己的磁盘

Welcome to fdisk (util-linux 2.40.2).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

This disk is currently in use - repartitioning is probably a bad idea.
It's recommended to umount all file systems, and swapoff all swap
partitions on this disk.


Command (m for help): p # 打印磁盘分区

Disk /dev/nvme0n1: 476.94 GiB, 512110190592 bytes, 1000215216 sectors
Disk model: SAMSUNG MZVLB512HBJQ-000L2
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: B65CCCD6-C78A-4C65-AE97-DE9434ADDB0D

Device             Start        End   Sectors   Size Type
/dev/nvme0n1p1      2048     534527    532480   260M EFI System
/dev/nvme0n1p2    534528     567295     32768    16M Microsoft reserved
/dev/nvme0n1p3    567296  419997695 419430400   200G Microsoft basic data
/dev/nvme0n1p4 419997696  683591679 263593984 125.7G Microsoft basic data
/dev/nvme0n1p5 998166528 1000214527   2048000  1000M Windows recovery environment
/dev/nvme0n1p6 683591680  788449279 104857600    50G Linux root (x86-64)
/dev/nvme0n1p7 788449280  998166527 209717248   100G Linux home
# 这里其实我已经分区完成了，所以没法展示真正的分区情况了，但是过程基本类似 

Partition table entries are not in disk order.

Command (m for help): n  # 输入 n 创建新的分区，这个分区将是根分区
Partition number (6-128, default 6):  # 分区编号保持默认，直接按 Enter
First sector (683591680-998166527, default 683591680):  # 第一个扇区，保持默认
Last sector, +/-sectors or +/-size{K,M,G,T,P} (683591681-998166527, default 998166527): +50G  # 创建 50 GiB 大小的根分区，您可以根据自己的硬盘空间决定根分区的大小

Created a new partition 6 of type 'Linux filesystem' and of size 50 GiB.

Command (m for help): t  # 输入 t 改变分区类型，请勿遗忘此步
Partition number (1-6, default 6):   # 保持默认
Partition type or alias (type L to list all): 23  # 输入 23 代表 Linux root (x86-64) 类型
Changed type of partition 'Linux filesystem' to 'Linux root (x86-64)'.

Command (m for help): n  # 输入 n 创建新的分区，这个分区将是 home 分区
Partition number (7-128, default 7):   # 保持默认
First sector (788449280-998166527, default 788449280):   # 保持默认
Last sector, +/-sectors or +/-size{K,M,G,T,P} (788449281-998166527, default 998166527):   # 保持默认，将剩余空间全部分给 home 分区

Created a new partition 7 of type 'Linux filesystem' and of size 100 GiB.

Command (m for help): t  # 输入 t 改变分区类型
Partition number (1-7, default 7):   # 保持默认
Partition type or alias (type L to list all): 42  # 输入 42 代表 Linux home 类型
Changed type of partition 'Linux filesystem' to 'Linux home'.

Command (m for help): p  # 输入 p 打印分区表，请检查分区是否有误，如果有误，请输入 q 直接退出
```
如果打印没有问题，比如我的分区如下：
```
Disk /dev/nvme0n1: 476.94 GiB, 512110190592 bytes, 1000215216 sectors
Disk model: SAMSUNG MZVLB512HBJQ-000L2
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: B65CCCD6-C78A-4C65-AE97-DE9434ADDB0D

Device             Start        End   Sectors   Size Type
/dev/nvme0n1p1      2048     534527    532480   260M EFI System
/dev/nvme0n1p2    534528     567295     32768    16M Microsoft reserved
/dev/nvme0n1p3    567296  419997695 419430400   200G Microsoft basic data
/dev/nvme0n1p4 419997696  683591679 263593984 125.7G Microsoft basic data
/dev/nvme0n1p5 998166528 1000214527   2048000  1000M Windows recovery environment
/dev/nvme0n1p6 683591680  788449279 104857600    50G Linux root (x86-64)
/dev/nvme0n1p7 788449280  998166527 209717248   100G Linux home
```
确认分区没有问题，就可以写入磁盘改变：
```
Command (m for help): w  # 输入 w 写入分区表，该操作不可恢复
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
```

##### 格式化分区
完成分区后，我们需要将上面刚创建的分区格式化成`ext4`：

```sh
# 格式化root分区
[root@archiso ~]$ mkfs.ext4 /dev/nvme0n1p6
# 格式化home分区
[root@archiso ~]$ mkfs.ext4 /dev/nvme0n1p7
```

##### 问题梳理
在最开始分区的时候，闹了个乌龙，因为我之前安装过`ubuntu`，所以当时分区`nvme0n1p6`是`ubuntu`的安装分区，当时确实对`fdisk`的分区操作不了解，于是最开始我们是直接对`nvme0n1p6`操作分区的（下面是错误演示）：

```
# 这个操作不报错，但是对分区是不能这么操作
fdisk /dev/nvme0n1p6
```
然后我就开始各种`n`和`t`的操作，但是在`w`写入的时候报错了，试了好多次都是一样的报错，也查了很多资料，甚至问了`AI`，问题还是没解决，最后才赫然发现，我竟然在对一个分区进行分区，报错大致如下，大家注意避坑。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/0347507b-b0bc-40d1-b581-a6edc1e3167e.jpg)

#### 挂载目录 
这里挂载目录是为了后面`arch-chroot`做准备。
```
# root分区挂载
mount /dev/nvme0n1p6 /mnt

# EFI 分区挂载
mount --mkdir /dev/nvme0n1p1 /mnt/boot
# home分区挂载
mount --mkdir /dev/nvme0n1p7 /mnt/home
```

#### 创建交换文件

按照官方文档推荐，我们应该创建交换分区（`swap`），这里直接用交换文件替代，电脑的内存是`16G`，这里交换文件我给`8G`

```sh
root@archiso ~ $ dd if=/dev/zero of=/mnt/swapfile bs=1M count=8192 status=progress
```


```sh
# 修改文件权限
root@archiso ~ $ chmod 0600 /mnt/swapfile
# 格式化swap
root@archiso ~ $ mkswap -U clear /mnt/swapfile
# 启用交换文件
root@archiso ~ $ swapon /mnt/swapfile
```

至此，安装准备工作完成，下面开始正式安装

### 系统安装

#### 安装基础包
使用 `pacstrap` 脚本，安装 `base`包 软件包和 `Linux` 内核以及常规硬件的固件：
```sh
pacstrap -K /mnt base linux linux-firmware
```

这时候可以同时额外安装计算机的 `CPU` 微码包。如果计算机是`Intel`的 `CPU` ，使用 `intel-ucode`包，`AMD CPU` 则使用 `amd-ucode`包。也可以暂时都不安装，等到进入系统后再安装。

#### 配置密钥

这部分是确保我们可以正常安装应有的，否则系统会认为安装的应用不合法
```sh
root@archiso ~ $ pacman-key --init  # 初始化密钥环
root@archiso ~ $ pacman-key --populate
root@archiso ~ $ pacman -Sy archlinux-keyring  # 更新 archlinux-keyring
```

#### 生成fstab
`fstab`文件可用于定义磁盘分区，各种其他块设备或远程文件系统应如何装入文件系统。

通过以下命令生成 `fstab`文件 (用 `-U` 或 `-L` 选项设置 `UUID` 或卷标)：

```
genfstab -U /mnt >> /mnt/etc/fstab
```

**强烈建议**在执行完以上命令后，检查一下生成的 `/mnt/etc/fstab` 文件是否正确。

```sh
cat /mnt/etc/fstab
```

#### chroo到挂载的分区

```sh
arch-chroot /mnt
```
**提示**：此处使用的是arch-chroot而不是直接使用chroot，注意不要输错了。


#### 设置时区

```sh
ln -sf /usr/share/zoneinfo/Region（地区名）/City（城市名） /etc/localtime
```

例如，在中国大陆需要将时区设置为北京时间，那么请运行 `# ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime`。时区名称是上海而非北京，是因为上海是该时区内人口最多的城市

然后运行 hwclock以生成 `/etc/adjtime`：

```
 hwclock --systohc
```

#### 区域和本地化设置

需要设置这两个文件：`locale.gen` 与 `locale.conf`。

编辑 `/etc/locale.gen`，然后取消掉 `en_US.UTF-8 UTF-8` 和其他需要的 `UTF-8` 区域设置前的注释（`#`），这里我把中文的语言配置打开了：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/59c3510b-ad8a-473b-ab30-36896f4dfc90.jpg)

接着执行 `locale-gen` 以生成 locale 信息：

```sh
locale-gen
```

然后创建 `locale.conf`文件，并编辑设定 `LANG` 变量，比如：

```sh
nano /etc/locale.conf

LANG=en_US.UTF-8
```
官方文档专门针对中文给出了说明：
- 将系统 locale 设置为 `en_US.UTF-8` ，系统的 log 就会用英文显示，这样更容易判断和处理问题；
    - 也可以设置为 `en_GB.UTF-8` 或 `en_SG.UTF-8`，附带以下优点：
        - 进入桌面环境后以 24 小时制显示时间；
        - LibreOffice 等办公软件的纸张尺寸会默认为 `A4` 而非 `Letter(US)`；
        - 可尽量避免不必要且可能造成处理麻烦的英制单位。
    - 设置的 LANG 变量需与 locale 设置一致，否则会出现以下错误：
        - `Cannot set LC_CTYPE to default locale: No such file or directory`

#### 网络配置

设置主机名
```sh
nano /etc/hostname

yourhostname #主机名，例如：arch-linux
```
安装网络管理器：
```
pacman -S networkmanager
```

注册网络服务：
```sh
systemctl enable NetworkManager.service
```

#### 设置root密码

```sh
passwd
```


#### 配置引导

```
# 安装必要的软件
pacman -S grub efibootmgr os-prober
```

##### 安装`GRUB`引导配置
```sh
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
```
如果如下提示：
```
Installation finished. No error reported.
```
说明安装成功，可以继续下面的步骤。否则请检查错误。

##### 配置 os-prober
配置 `os-prober`，以检测 `Windows` 系统，否则将不能进入 `Windows` 系统。

```text
[root@archiso ~]# nano /etc/default/grub
```

搜索`GRUB_DISABLE_OS_PROBER=false`一行，并去掉开头的“#”注释，保存并退出。
##### 生成`GRUB`配置
```sh
grub-mkconfig -o /boot/grub/grub.cfg
```

#### 重启

首先，退出 chroot 环境。

```text
[root@archiso ~]# exit
```

然后，关闭交换文件。

```text
root@archiso ~ # swapoff /mnt/swapfile
```

随后，取消挂载 `/mnt`。

```text
root@archiso ~ # umount -R /mnt
```

最后，重新启动计算机。

```text
root@archiso ~ # reboot
```

## 安装常用软件
### 安装桌面环境

由于默认情况下，`arch linux`默认进入的是终端模式，当然也是由于我们没有安装桌面环境，所以重启后先安装桌面环境。

最早考虑安装`gnome`，后面配置过程发现中文输入法一直安装不上，于是又试了下`xorg`，中文输入法还是不行，最后就换到了`kde`，中文输入法完美解决。

```sh
# 先更新下软件包
sudo pacman -Syu
sudo pacman -S plasma kde-applications packagekit-qt5
```


### 安装中文输入法

#### 安装核心依赖

这里其实安装的是小企鹅输入法

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

使用`arch`那必然是先安装`yay`：

```sh
sudo pacman -S yay
```
然后就可以通过`yay`安装各种常用的软件了。
#### 知识库软件

强烈推荐，我觉得很好用

```sh
yay -S obsidian
```

#### 常用软件

##### 截图软件


```
yay -S flameshot
```
`flameshot`我感觉是目前为止`linux`下最好的截图软件，类似`snipaste`

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/manjaro/20211027224853.png)
##### google chrome

```sh
yay -S google-chrome
```

#### 国内常用软件
##### dingtalk

```sh
yay -S dingtalk-bin
```

##### wechat

目前可以安装最新版本的原生`linux`版本微信，是基于`qt`开发的
```sh
yay -S wechat
```


### 注意点

- 除了 `/etc/pacman.d/mirrorlist` 之外的软件或配置不会从 Live 环境传递到安装的系统中。

### 安装完成

至此，安装完成，效果如下：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/9ba999fb-ed8f-48a3-99bd-dffcb631c792.jpg)
到这里，我们就可以愉快地使用我们的`arch linux`了

参考文档：
[官方安装指南](https://wiki.archlinuxcn.org/wiki/%E5%AE%89%E8%A3%85%E6%8C%87%E5%8D%97)
https://zhuanlan.zhihu.com/p/596227524