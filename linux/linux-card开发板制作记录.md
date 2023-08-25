# linux card开发板制作

## 电路设计

这里其实是踩坑最多的，因为这里如果设计不正确，会导致后面直接失败，先来看下我都踩了那些坑

### 串口电路连接错误

在本次设计中，串口芯片用的是`CH340E`，电路比较简单，但是`CH340E`的`RXD`和`TXD`应该分别对应主控芯片的`TXD`和`RXD`，但是对于我这样的小白来说，我一直觉得应该是一一对应的，结果导致的原因就是按下`RESET`按钮之后，串口通信就断开了，百思不得其解，最好对比了一众大佬设计的原理图，发现自己搞错了，下面是一众大佬的设计：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230421111412.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230421111519.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230421112335.png)


## 打板焊接

打板直接就在嘉立创白嫖了，由于设计错误，我已经打了`6`次板了，但是这一路踩坑，确实也学了很多，也成长了。

### 第一版

刚开始甚至连封装为何物都不知道，画板子的时候，各种封装都涉及到了，包括`0805`、`0603`、`0402`，甚至画了`01005`和`0201`封装的，所以第一张板子基本上没法焊接，当然这也是为啥我现在手里的板子封装还是乱七八糟的，毕竟买的元器件不能浪费了

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824200958.png)

### 第二版 && 第三版

重新画图打板，第二次焊接之后发现芯片引脚错位了，一直短路，然后就有了第三版。


![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824200343.png)

第二版到第三版还有个改动，就是将串口的`LED`拿掉的，我这里其实是参考其他大佬的原理图，他连接的是发光二极管，说应该连接二极管，然后我画的是`1N4148`开关二极管，先不说合理不合理，反正瞎画肯定不合适，这里也给抄电路的小伙伴提个醒，一定要先搞清楚原理，再抄，不然真的自己坑自己。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824213013.png)


### 第三版

第三版由于`sd`卡槽不匹配，然后重新打板，毕竟嘉立创的板子可以白嫖:

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824201752.png)

### 第四版 && 第五版

第四版芯片正常驱动，但是串口插上，按`reset`开关，直接断开，经过比对，发现串口连接错了，我这里用的是`CH340E`，`RXD`和`TXD`应该分别对应`F1C200S`芯片的`DTX`和`DRX`，也就是读对应芯片的发，发对应芯片的读，结果之前不知道，画错了，然后导致了这个乌龙，之后第五版应运而生：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824202653.png)
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824202250.png)

### 第五版 && 第六版

第五版到第六版基本上没有改动，只是因为串口一直没有生效，参考了其他人的原理图，然后在`reset`引脚上增加了一个滤波电容，容值`1uf`：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824204546.png)

同时还增加了一些电压测试点位：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824204833.png)

然而，就在我觉得一切都要结束了，我终于要点亮这个小板板的时候，上天又一次给我开了个玩笑🤪，串口依然不行，甚至芯片都读不出来了。

真的心态都崩了，反正那之后的很长时间（最后一版打板时间是`4-21`），我基本上都放弃了。然后在这些捣鼓不下来的空挡，我搞新的项目，虽然都是小项目，但是我觉得还是很有意思的，项目的简介我放在后面了，感兴趣的小伙伴可以去瞅瞅。


### 柳暗花明又一村

直到最近，一天晚上睡不着，也没啥事，于是我又开始查阅`F1C200S`相关的内容，然后经过比对，我发现了华点——别人的串口基本上都没有电阻，而我抄的串口为啥还有电阻，然后我去看了我之前参考的原理图，发现人家的电阻单位是`680`，没有单位，而我抄的时候误以为是`680K`，所以买的时候也是按这个买的，焊接的时候也是用的这个阻值，因为恰好电路那里用到了`680K`的电阻。

串口的问题算是解决了，但是为什么我的芯片为啥还是不能工作，我打算重新焊一块板子，结果我在对着这块板子焊新板子的时候，发现有一个点电阻和电容搞错了，应该焊接电阻的地方，放的是电容，应该焊电阻的地方放的是电容~

好家伙，原来问题处在这里了，于是调换了原来板子的电阻和电容，芯片可以识别了，插上之前烧录的`sd`卡，连接串口，成功显示信息，我擦，幸福来得有点突然，困惑了小半年的问题解决了，简直不要太爽

### 结语

从一个只有高中电路知识的纯小白（当然主要是一直喜欢这些，但是日常主要还是搞维修，纯玩），到学习电路原理图、`PCB`的绘制，到后面自己踩坑了解封装知识，再到后面搜集元器件的手册和文档，亲自动手画板子，慢慢可以看懂大佬的原理图，能看懂简单的数据手册，到现在这个板子的设计、打板、焊接、编译、烧录，虽然现在依然还是小白，但我也慢慢能找到自己的方向，至少在这条自己热爱的路上，我越走越顺，也越走越自信……

### 其他项目

#### usb2.0扩展坞

搞了一个`USB`的扩展板，很迷你，已经正常打板了，感兴趣的小伙伴可以去看看：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824210756.png)

这里是项目地址

```
https://oshwhub.com/syske/usb-ext
```

#### 触摸台灯

搞了个触摸台灯的板子

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824211117.png)

这个项目也打板验证了，目前我的床头台灯就是这个板子，灯泡、底座是买的，罩子和骨架是家里拆的吊灯，这是实物：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824211850.png)

#### F1C200S板子2.0

画了`F1C200S`新的`V2`版本：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824212229.png)

还专门绘制了`3D`外壳，已经按照我现在最新点亮的原理图做了调整，元器件的封装尺寸也调整统一了，除了极个别元件，电阻和电容都是`0603`封装，颜值一下提升了不少。


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

```
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
```
 fatal error: gmp.h: No such file or directory
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230819220134.png)
```
解决方法
```
 sudo apt-get install libgmp-dev
```


报错2

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230819220403.png)
```
fatal error: mpc.h: No such file or directory
```
解决方法
```
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

```
export FORCE_UNSAFE_CONFIGURE=1
export FORCE=1
```

遇到下载特别慢的资源，可以手动下载之后，放进`buildroot-2020.11.4\dl`下对应的资源目录中，终止编辑，然后重新跑下就好了，比如`linux`下载就很慢，我就通过镜像地址下载之后，复制到`dl/linux`目录下


编译完成后，将`ooutput`文件夹下的`rootfs.tar`解压到我们`sd`卡的`rootfs`分区中，解压命令如下：

```
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
