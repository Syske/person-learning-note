最近闲来无事，将家里的`N1`盒子又折腾了一遍，将原来的`openWrt`换成`armbian`，原因嘛，主要是`openWrt`对`docker`的支持不够好，可玩性太低，而且我对旁路由也没有什么需求，于是就趁着周末，把`N1`盒子的系统重新折腾了下，下面就是完整的过程。
### 安装Armbian系统

#### 下载
```
https://github.com/ophub/amlogic-s9xxx-armbian/releases?page=1
```

下载的时候选择`s905d`的版本，我没有选择太新的版本，选择了`jammy`，如果是`N1`盒子可以无脑直接下载：

```
https://github.com/ophub/amlogic-s9xxx-armbian/releases/download/Armbian_jammy_save_2024.10/Armbian_24.11.0_amlogic_s905d_jammy_6.1.112_server_2024.10.02.img.gz
```
#### 刻录系统

我这里选择的刻录软件是`balenaEtcher`，下载地址如下：

```
https://github.com/balena-io/etcher/releases/
```
选择最新版本即可，目前最新的版本是`1.19.25`

下载完成后安装打开，然后选择镜像和`U`盘，等待烧录完成。这里需要注意的是，`U`盘需要选择`USB2.0`的，否则可能会有问题

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/e3c1813f-aadc-43d9-ad3d-f1cac86ada1d.jpg)
#### 安装armbian

将`U`盘插入靠近`HDMI`接口的`USB`，插电启动。这里尽量在启动前连接显示器，方便我们查看日志

通过`ssh`工具远程连接`N1`盒子，默认账号密码是：`root/1234`

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/246d7c9f-80d7-4fd9-bce8-e2eb8f076bce.jpg)
登录成功后，输入`armbian-install`，然后按照提示安装即可，`ID`那里我们输入`101`（`N1`盒子对应的版本），等待安装`success`完成提示。

最后输入`poweroff`命令，拔掉电源和`U`盘，重新插电启动，这时候在插电的同时要插入网线。首次登录可能会让你修改登录密码，按照提示修改即可。

至此，`armbian`底包刷入成功，下面开始安装我们的`casaos`系统。
#### 安装casaos

通过`wget`下载安装`sh`并执行
```sh
wget -qO- https://get.casaos.io | sudo bash
```
静静等待安装完成：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/243eac96-8917-48f2-9d72-10675aeb3044.jpg)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/22f542a8-ef27-400b-9d7f-c9d42a41e0da.jpg)

然后通过`N1`盒子的`ip`地址访问即可，比如我的`ip`地址是`192.168.0.101`，紧接着注册账号登录即可，颜值还是嘎嘎的
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/0e4b5cc3-1830-4b7f-9169-489e36950273.jpg)

### NFS挂载磁盘

为了实现`nfs`网盘方式，这里需要将硬盘连接`N1`盒子，然后在`casaos`磁盘管理中移除挂载的磁盘，然后手动指定磁盘挂载路径

```sh
# 我的移动硬盘是/dev/sda

# 通过fdisk查看磁盘分区
 fdisk -l /dev/sda
# 然后将对应的分区挂载到指定的目录
 mount /dev/sda1 /mnt/nas/
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/231a5a33-8c68-4944-855f-c08b4b325228.jpg)

挂载成功后，通过`blkid`查看磁盘`id`，为后面自动挂载做准备
```
$ blkid
```
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/17352af6-0bab-4a12-b01f-bdd5d88b7736.jpg)

我的磁盘`id`如下：
```
/dev/sda1: BLOCK_SIZE="512" UUID="14F89820F89801E2" TYPE="ntfs" PARTUUID="91de00b0-01"
```

#### 自动挂载磁盘

编辑`fstab`在其中添加自动挂载配置：
```sh
sudo nano /etc/fstab
```
我的配置如下：
```c
# my nas
UUID=14F89820F89801E2 /mnt/nas ntfs-3g defaults 0 0
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/65b00ba0-9a13-48ab-894e-44768ed4b799.jpg)

#### NFS共享
##### 安装依赖

如果没有安装`ntfs-3g`，需要安装相关软件：
```sh
sudo apt-get update 
sudo apt-get install ntfs-3g nfs-kernel-server
```

##### 编辑配置

```sh
sudo nano /etc/exports
```
加入共享的路径配置
```
/mnt/nas 192.168.0.0/24(rw,sync,no_subtree_check)
```
启动服务
```sh
sudo exportfs -a 
sudo systemctl restart nfs-kernel-server
```
客户端挂载
```sh
sudo mount 192.168.0.100:/mnt/nas /mnt/nfs-share
```

### SMB

原本是直接通过`nfs`方式实现磁盘共享的，但是实际使用的时候发现`windows`和安卓都需要安装特殊的客户端软件，所以又安装了`SMB`，实现兼容性更好的局域网网盘。
#### 安装smb

```sh
 sudo apt update
 sudo apt install samba -y
```

#### 配置账号密码
```sh
# 设置smb账号密码
sudo smbpasswd -a syske
```

#### 修改配置

```sh
sudo nano /etc/samba/smb.conf
```
配置内容如下
```config
[nas]
path = /mnt/nas
available = yes
valid users = syske
read only = no
browsable = yes
public = yes
writable = yes
```
这里我共享的路径是`/mnt/nas`，需要提前挂载磁盘，并实现自动挂载。

#### 客户端连接

根据上面的配置，我们客户端可以通过如下方式访问我们的`smb`
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/bf7aab17-35e5-4460-85de-b2062ebac0d7.jpg)

后面在使用过程中发现，`casaos`的文件系统也提供了`nas`的能力，我们可以通过更简单的方式实现`smb`共享磁盘：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/27a79d0e-9da8-4172-9ccf-b687980a567a.jpg)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/310fd58a-e6cf-46f9-a7fc-bc347f780ac6.jpg)
点击要共享的目录右键选择【共享】
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/dec2588e-970c-4c2b-a2ae-f4e46ff70dcf.jpg)
然后会弹出磁盘的共享路径：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/924ecd64-9fc8-4a5e-b42e-b90292713aaa.jpg)
至此`smb`目录共享完成。

### 其他软件

除了共享磁盘外，我还在`casaos`中安装了`syncthing`、`emby`、`Alist`等软件

#### syncthing

`syncthing`是一个区中心化的备份软件，可以实现单向或者双向的数据备份和同步，这里我主要是为了将自己手机的照片和视频备份到`N1`盒子挂载的磁盘上，还是很方便的
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/4ea3c7d9-edf9-46c2-9f01-85e50414f0c3.jpg)
#### emby

`emby`是一个在线视频播放平台，可以直接挂载我们本地或者网络视频库，实现随时随地在线追剧。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/5797f3c6-abb6-4c6f-b449-03c97f7718ce.jpg)

参考文档：
1. https://baijiahao.baidu.com/s?id=1797388138356939249&wfr=spider&for=pc