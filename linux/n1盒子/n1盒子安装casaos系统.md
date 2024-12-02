
### 安装Armbian系统

#### 下载
```
https://github.com/ophub/amlogic-s9xxx-armbian/releases?page=1
```

下载的时候选择`s905d`的版本
### 刻录系统

我这里选择的刻录软件是`balenaEtcher`，下载地址如下：

```
https://github.com/balena-io/etcher/releases/
```
选择最新版本即可，目前最新的版本是`1.19.25`

下载完成后安装打开，然后选择镜像和`U`盘，等待烧录完成。这里需要注意的是，`U`盘需要选择`USB2.0`的，否则可能会有问题

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/e3c1813f-aadc-43d9-ad3d-f1cac86ada1d.jpg)
### 安装armbian

将`U`盘插入靠近`HDMI`接口的`USB`，插电启动。这里尽量在启动前连接显示器，方便我们查看日志

通过`ssh`工具远程连接`N1`盒子，默认账号密码是：`root/1234`

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/246d7c9f-80d7-4fd9-bce8-e2eb8f076bce.jpg)
登录成功后，输入`armbian-install`，然后按照提示安装即可，`ID`那里我们输入`101`（`N1`盒子对应的版本），等待安装`success`完成提示。

最后输入`poweroff`命令，拔掉电源和`U`盘，重新插电启动，这时候在插电的同时要插入网线。首次登录可能会让你修改登录密码，按照提示修改即可。

至此，`armbian`底包刷入成功，下面开始安装我们的`casaos`系统。
### 安装casaos

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
然后编辑`fstab`在其中添加自动挂载配置：
```sh
sudo nano /etc/fstab
```
我的配置如下：
```c
# my nas
UUID=14F89820F89801E2 /mnt/nas ntfs-3g defaults 0 0
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/65b00ba0-9a13-48ab-894e-44768ed4b799.jpg)

如果没有安装`ntfs-3g`，需要安装相关软件：
```sh
sudo apt-get update 
sudo apt-get install ntfs-3g
```

#### NFS共享

```sh
sudo apt-get update 
sudo apt-get install nfs-kernel-server
```

编辑配置：
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

参考文档：
1. https://baijiahao.baidu.com/s?id=1797388138356939249&wfr=spider&for=pc