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

从我多次实际踩坑的感受来说，安装步骤主要如下：
- 基本设置：设置字体
- 配置网络，修改软件源
- 系统分区，磁盘挂载
- arch-chroot
- 安装桌面系统
- 安装常用软件


### 系统分区

```sh
fdisk /dev/sda
```

### 安装




#### 配置网络

```sh
# 直接进入无线网络管理工具
iwctl
# 连接指定的wifi
station wlan0 connect syske-wifi
# 然后输入wifi密码
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