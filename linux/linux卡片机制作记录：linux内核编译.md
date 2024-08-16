# linux内核编译

## 前言

相比于`u-boot`的编译，`linux`的内核编译要相对简单一点，唯一踩坑的点，就是编译过程中的各种报错，下面就让我们一起来看看如何编译`linux`内核吧。

以下编译过程在`wsl`环境下进行，版本是`ubuntu 20.04 TSL`

## linux内核编译


### 准备工作

#### 源码下载

源码我们可以直接去官方网站下载，地址如下：

```sh
https://www.kernel.org/
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230828082910.png)

在上面图片中，第一列是版本，`mainline`表示主线版本，是正在开发的版本，`stable`表示稳定版，`longterm`表示长期支持版，这里推荐下载`longterm`，国内推荐直接通过镜像站进行下载，下面是中国科学技术大学的镜像地址：

```sh
http://mirrors.ustc.edu.cn/kernel.org/linux/kernel/
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230828083840.png)

选择对应的版本进行下载即可，选择`tar.*`格式的文件，这样我们就可以通过`tar`命令进行解压了。

这里的`linux`我选择的是`linux-6.1.46`版本，想直接开始的小伙伴可以直接通过下面的命令下载`6.1.46`版本：

```sh
 wget http://mirrors.ustc.edu.cn/kernel.org/linux/kernel/v6.x/linux-6.1.46.tar.gz
```

下载完成后，直接解压：

```sh
tar -xvf linux-6.1.46.tar.gz
```

网上大部分文档都下载的是`5.X`，但是选择这个版本之后，我发现还是有惊喜的，就是`lichee nano`的设备树相关配置都已经有了，不需要自己再手动编辑了，这一点对我等小白很友好。下面是需要修改的配置和文件（具体看自己的版本，`6.4`是不需要修改的，配置已经包含了），标红部分是需要增加的：

```
 vim linux-6.1.46/arch/arm/boot/dts/suniv-f1c100s-licheepi-nano.dts
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824083113.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824083627.png)

```
 vim linux-6.1.46/arch/arm/boot/dts/suniv-f1c100s.dtsi
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824083223.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824083413.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824083524.png)


#### 工具准备

这里和`u-boot`的编译有点类似，工具也基本上是相同的，就不再赘述了

#### 初始化配置

首先，需要下载荔枝派的配置文件，解压并复制到`linux`内核源码的`arch/arm/configs/`目录下：

```sh
wget https://files.cnblogs.com/files/twzy/linux-licheepi_nano_defconfig.zip
unzip -x linux-licheepi_nano_defconfig.zip
cp linux-licheepi_nano_defconfig linux-6.4/arch/arm/configs/
```

然后开始`make`的配置操作：

```sh
# 进入到linux内核源码根目录
cd linux-6.4/
# 应用荔枝派配置
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- linux-licheepi_nano_defconfig
```
如下提示则表示配置成功

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240809010102.png)

然后开始配置菜单：

```sh
# 没有修改配置，测试一下
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- menuconfig
```
由于我并不需要对菜单进行编辑，所以这里直接默认配置保存即可：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240809010346.png)

然后就可以开始编译了：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240809010523.png)

### 开始编译

我最开始选择的就是`6.1.46`，后面试过`6.4`，`wsl`环境下编译可以成功，编译命令如下：

```sh
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- -j6
```

如下提示则表示编译成功了：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240809011524.png)

编译会生成两个文件，一个是内核文件，一个是设备树文件：
```sh
# 内核文件，大小4.81M
linux-6.4/arch/arm/boot/zImage  
# 设备树，大小6.6k
linux-5.15.114/arch/arm/boot/dts/suniv-f1c100s-licheepi-nano.dtb
```
之后需要将上述文件分别拷贝到对应的分区目录下面

#### 编译过程中的报错

##### 报错1

```sh
 fatal error: gmp.h: No such file or directory
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230819220134.png)

解决方法

```sh
 sudo apt-get install libgmp-dev
```

##### 报错2

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230819220403.png)

```sh
fatal error: mpc.h: No such file or directory
```

解决方法

```sh
sudo apt-get install libmpc-dev
```


### 烧录

#### SD卡分区

分区如图所示，按图示顺序分区，BOOT前要保留1MB空间用来刷u-boot。

| 分区名    | 距前一个分区保留大小 | 文件系统  | 分区尺寸  |
| ------ | ---------- | ----- | ----- |
| BOOT   | 1MB        | fat16 | 32MB  |
| rootfs | 0          | ext4  | 100MB |
| other  | 0          | 任意    | 剩余区域  |

这里分区主要有两种方式，一种是通过`Gparted`这样的`GUI`工具，第二种是通过`fdisk`直接进行分区，两种方式我下面都会介绍，各位小伙伴根据自己的情况选择。

##### Gparted

`Gparted`作为一款优秀的磁盘管理工具，在我们项目中出现频率还是很高的
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202408090847641.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202408090853915.png)
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202408090857422.png)e

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202408090855586.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202408090855534.png)
##### fdisk

该部分的分区操作，参考的是稚晖君`Planck-Pi`项目中的分区方式：

命令行方式如下，首先查看电脑上已插入的TF卡的设备号（一般为 /dev/sdb1,下面以/dev/sdb1为例：

```
sudo fdisk -l 
```

若自动挂载了TF设备，先卸载（有多个分区则全部卸载）：

```
sudo umount /dev/sdb1...
```

进行分区操作：

```
sudo fdisk /dev/sdb
```

操作步骤如下：

1. 若已存分区即按 d 删除各个分区
    
2. 通过 n 新建分区，第一分区暂且申请为1M用于储存uboot-with-spl，第二分区32M用于储存Linux内核，剩下的空间都给root-fs
    
    > - **第一分区操作**：p 主分区、默认 1 分区、默认2048、+16M
    >     
    >     ```
    >     n p [Enter] [Enter] [Enter] +1M
    >     ```
    >     
    > - **第二分区操作**：p 主分区、2 分区、默认2048、+128M
    >     
    >     ```
    >     n p [Enter] [Enter] [Enter] +128M
    >     ```
    >     
    > - **第三分区操作**：p 主分区、3 分区、默认2048，剩下的全部分配
    >     
    >     ```
    >     n p [Enter] [Enter] [Enter] [Enter]
    >     ```
    >     
    > - w 保存写入并退出
    >     
    

分区格式化：

```
sudo mkfs.vfat /dev/sdb1 # 将第1分区格式化成FAT
sudo mkfs.ext4 /dev/sdb2 # 将第2分区格式化成FAT  
sudo mkfs.ext4 /dev/sdb3 # 将第3分区格式化成EXT4
```

> **格式说明：**
> 
> - EXT4：只用于Linux系统的内部磁盘
> - NTFS：与Windows共用的磁盘
> - FAT：所有系统和设备共用的磁盘



### 上电测试

如果编译、配置都没有问题的话，正常就会进入登录界面，烧录之后的系统，默认的用户名和密码都是`root`，输入密码之后就可以看到熟悉的`linux`命令行：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240809012228.png)

至此，我们的`linux`内核交叉编译完美收官
## 结语

`linux`内核编译的核心其实就是环境的配置，整个过程就是疯狂踩坑。甚至如果选择的是`6.X`的版本，甚至省去了配置文件的修改过程，就更简单了。
好了，有兴趣的小伙伴快去动手吧。

另外，项目的电路设计部分已经开源了，感兴趣的小伙伴可以去看看：
https://oshwhub.com/syske/7L5S3cM12t8euqRi6ylftf59yqr5j7Js

