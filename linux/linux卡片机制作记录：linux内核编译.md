# linux内核编译

## 前言

相比于`u-boot`的编译，`linux`的内核编译要相对简单一点，唯一踩坑的点，就是编译过程中的各种报错，下面就让我们一起来看看如何编译`linux`内核吧。

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

网上大部分文档都下载的是`5.X`，但是选择这个版本之后，我发现还是有惊喜的，就是`lichee nano`的设备树相关配置都已经有了，不需要自己再手动编辑了，这一点对我等小白很友好：

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


#### 初始化配置

### 开始编译

我最开始选择的就是`6.1.46`，后面试过`6.4`，`wsl`环境下编译可以成功00


报错1

```sh
 fatal error: gmp.h: No such file or directory
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230819220134.png)

解决方法

```sh
 sudo apt-get install libgmp-dev
```

报错2

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

这里分区主要有两种方式，一种是通过`Gparted`这样的`GUI`工具，第二种是通过`fdisk`直接进行分区，两种方式我下面都会介绍，各位小伙伴根据自己的情况选择。

##### Gparted

`Gparted`作为一款优秀的磁盘管理工具，在我们项目中出现频率还是很高的


##### fdisk






## 结语