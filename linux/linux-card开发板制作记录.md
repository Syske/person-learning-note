# linux card开发板制作

## 电路设计

这里其实是踩坑最多的，因为这里如果设计不正确，会导致后面直接失败，先来看下我都踩了那些坑

### 串口电路连接错误

在本次设计中，串口芯片用的是`CH340E`，电路比较简单，但是`CH340E`的`RXD`和`TXD`应该分别对应主控芯片的`TXD`和`RXD`，但是对于我这样的小白来说，我一直觉得应该是一一对应的，结果导致的原因就是按下`RESET`按钮之后，串口通信就断开了，百思不得其解，最好对比了一众大佬设计的原理图，发现自己搞错了，下面是一众大佬的设计：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230421111412.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230421111519.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230421112335.png)s

## 镜像烧录过程

### 准备工作

#### 安装驱动

```
https://zadig.akeo.ie/
```

#### 安装芯片工具

```sh
sudo apt install pkg-config pkgconf zlib1g-dev libusb-1.0-0-dev swig python-dev
```

获取`sunxi-tools`:

```
git clone https://github.com/Icenowy/sunxi-tools.git
```


#### 编译uboot

```sh
git clone https://gitee.com/LicheePiNano/u-boot.git -b nano-v2018.01&&cd u-boot
##  有flash的用这个
# sudo make licheepi_nano_spiflash_defconfig

sudo make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- licheepi_nano_defconfig
sudo make ARCH=arm menuconfig
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230823083403.png)
```sh
# boot args
console=tty0 console=ttyS0,115200 panic=5 rootwait root=/dev/mmcblk0p2 rw

# boot cmd
load mmc 0:1 0x80C00000 suniv-f1c100s-licheepi-nano.dtb;load mmc 0:1 0x80008000 zImage;bootz 0x80008000 - 0x80C00000;

```

```sh
sudo make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- -j8
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221226210230.png)

忘了之前参考那个大佬的文档，把串口改成了`PD3/PD4`，导致我烧录的`u-boot`一直不成功，这里建议大家确认好自己的串口端口，默认是`0`号，也就是`PE0/PE1`:

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230823084450.png)



### 报错记录

- `arm-linux-gnueabi-gcc: command not found`

![arm-linux-gnueabi-gcc: command not found](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221227215448.png)

```sh
 sudo apt install gcc-arm*
```

- `No module named _libfdt`

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221227214530.png)


`python`的软连接记录
![python软连接](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221227214750.png)

```sh
sudo ln -f /usr/bin/python2 /usr/bin/python
```

变更后：
![变更后](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221227214905.png)

- `Python.h: No such file or directory`

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221227214411.png)

```
apt install python-dev
```

#### 成功点亮

今天我又把之前的板子拿出来研究了，起因是我前天睡不着，翻开了我的原理图，对比了其他大佬的原理图，发现我好像把串口的电阻阻值单位搞错了，其他大佬要么没有电阻，要么有也是多少欧姆，而我画的是`680KΩ`，怪不得串口一直不能正常工作。当然，上次串口报错主要还是我把串口连接搞错了。

另外，今天主要的改动点是，我把串口`USB`后面的保险丝直接拿掉了，不知道保险丝是不是坏了，保险丝后面的电压直接变成`2.67V`，拿掉保险丝，之后连接串口，终端终于显示正常了：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230819124737.png)


看到这些信息，我简直不要太激动，前前后后，断断续续差不多搞了一年了，心态都被搞崩了，但是此时此刻，我觉得踩的坑都是值得的，奥里给~


#### linux编译

镜像地址

```sh
http://mirrors.ustc.edu.cn/kernel.org/linux/kernel/
```

这里的`linux`我选择的是`linux-6.1.46`版本，网上大部分文档都下载的是`5.X`，但是选择这个版本之后，我发现还是有惊喜的，就是`lichee nano`的设备树相关配置都已经有了，不需要自己再手动编辑了，这一点对我等小白很友好：

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

#### sd卡分区

BOOT

rootfs



#### 运行linux

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230823223606.png)


#### 编译buildroot

<https://buildroot.org/downloads/>


##### 编译报错

不通过`sudo`编译提示没有权限：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230823225656.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230823230017.png)


root编译还是报错

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230823225757.png)

```sh
export FORCE_UNSAFE_CONFIGURE=1
export FORCE=1
```

遇到下载特别慢的资源，可以手动下载之后，放进`buildroot-2020.11.4\dl`下对应的资源目录中，终止编辑，然后重新跑下就好了，比如`linux`下载就很慢，我就通过镜像地址下载之后，复制到`dl/linux`目录下


编译完成后，将`ooutput`文件夹下的`rootfs.tar`解压到我们`sd`卡的`rootfs`分区中，解压命令如下：

```sh
sudo tar -xvf rootfs.tar -C /media/syske/rootfs
```

需要注意的是，操作解压是，确保我们的`rootfs`分区是挂载的，具体路径可以通过属性菜单进行查看：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230823235332.png)

解压完成后，我们可以在`rootfs`分区看到如下文件夹及文件，也就是我们的文件系统：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230823235431.png)

之后将`sd`卡插入我们的板子，然后连接`com`串口，可以看到如下信息：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230823234434.png)

至此我们算是彻底完成了`linux-card`的所有开发工作，虽然只是个`demo`版，但是我还是感觉很有收获，而且收获到满满的成就感，特别是`u-boot`成功进入的那一刻，虽然之后也踩了很多坑，但是也将整个过程梳理清楚了，了解了其中的各种原因，后面我应该还会把整个过程再进一步梳理完善，感谢各位小伙伴的关注和支持，这个历时两年的`linux-card`开发制作暂时告一段落。

参考文档：

1. <https://whycan.com/t_7558.html> 
2. <https://whycan.com/p_69548.html>
3. 全志sunxi-tools烧录工具安装和使用:<https://blog.csdn.net/p1279030826/article/details/112719638>
4. Ubuntu下编译最新版本全志开源FEL模式工具sunxi-tools:<https://www.pudn.com/news/6228cf289ddf223e1ad13c34.html>
5. <https://whycan.com/t_993.html>
6. <https://blog.csdn.net/weixin_37214729/article/details/119393266>
7. <https://zhuanlan.zhihu.com/p/504152168>
8. <https://whycan.com/t_4781.html>
9. <https://whycan.com/t_7558.html>
10. <https://blog.csdn.net/qq_44159389/article/details/122760661>
11. <https://zhuanlan.zhihu.com/p/634414429>
12. <https://blog.csdn.net/nongchaoer201012/article/details/114609518>
13. <https://zhuanlan.zhihu.com/p/605529215?utm_id=0>
