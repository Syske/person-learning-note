# linux卡片机制作记录：uboot编译烧录

## 前言

在正式开始今天的内容之前，我想先简单介绍下我用到的这款主控芯片——`F1C200S`，这是国产厂商全志科技推出的一款移动应用处理器，`88`个引脚，`QFN`封装，`40nm`制程，集成了`usb otg`、`uart`、`spi`、`tWI`、`tp`、`sd/mmc`、`csi`等接口，支持`1080`高清视频解码、音频解码、相机等外设，内置了`64M`的`DDR1`内存，可以支持诸如`MELIS`、`Linux`等操作系统，当然这也是我选择这块主控芯片的原因。

这里是芯片的架构图和数据手册，感兴趣的小伙伴可以去了解下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230826093837.png)

数据手册：

```sh
https://atta.szlcsc.com/upload/public/pdf/source/20211016/C2879851_80200E64F493B5C5B5C583D1EECFE2F1.pdf
```

全志还有一款芯片和`F1C200S`基本上完全一致——`F1C100S`，只是内存小一点，只有`32M`，当然性能上，`F1C200S`更高，但架构和引脚完全一致，可以完美互替：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230826094756.png)

`F1C100S`之所以有名气，与一款开发板有着很大的关系——`LicheePi Nano`，把玩过树莓派的小伙伴应该听说过这块板子：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230826095346.png)

这里是`LicheePi Nano`的相关简介：

```sh
https://wiki.sipeed.com/hardware/zh/lichee/Nano/Nano.html
```

`LicheePi Nano`的存在，确保了`F1C200s/F1C100s`的生态和可玩性，让我们可以以更低的门槛窥探嵌入式开发的秘密，享受把玩硬件的乐趣。也是因此，`F1C200s/F1C100s`的原理图和教程文档特别多，可以让我们在遇到问题的时候，站在大佬的肩膀上，完美避坑，这也是我选择`F1C200s`开发`Linux`卡片机的重要原因。

## uboot编译烧录

### 资源分享

在开始`uboot`相关内容之前，我还想再分享一些与`F1C200s/F1C100s`相关的优质资源，方便感兴趣的小伙伴去了解学习：

#### 哇酷开发者社区

  特别小众的一个论坛，但是技术讨论上一点也不小众，各种优秀分享和讨论

  网址：  https://whycan.com/

#### 优质的教程和文档

下面是我参考的一些文档，相对来说质量还比较高，当然过程中参考的文档实际远远超过这些，我会在后面的内容中逐一补充完善。

##### Linux开发板(F1C200s)系列

   第一个文档：https://whycan.com/p_69548.html

   我最早就是参考的这个文档，最开始的原理图就是参考的这个博主的，虽然是直接抄的，但是还是踩了很多坑，当然主要还是自己太菜了。

   第二个文档：https://zhuanlan.zhihu.com/p/634442525

   `linux`编译和烧录的时候参考过这个文档，解决了我编译配置的相关困惑

##### 驱动安装及flash烧录

因为我画的板子没有`spiflash`，所以这里其实主要是安装驱动之后，验证芯片是否正常驱动。最开始没有`get`到`spiflash`是干啥的，所以参考这个文档搞了很久，最后才后知后觉。关于`spiflash`的简单介绍，我们后面再展开

文档地址：<https://whycan.com/t_993.html>


### 准备工作

#### 什么是uboot

在开始`uboot`的相关内容之前，让我们先来了解下`uboot`是什么。简单来说`uboot`是一个用于嵌入式系统的引导加载程序，可以支持多种不同的计算机系统结构，包括`PPC`、`ARM`、`AVR32`、`MIPS`、`x86`、`68k`、`Nios`与M`icroBlaze`，我们这里的`F1C200s`就是一款基于`ARM9`的`MCU`，我们通过配置`uboot`的加载指令，驱动`linux`内核和设备树文件，让我们的`F1C200s`来运行`Linux`。

#### F1C200s上电启动顺序

这里我觉得还有必要讲下`F1C200s`上电之后是如何启动的，因为完整的启动流程应该是：

```sh
F1C200S -> uboot -> linux
```

如果不搞清楚，我们就很难理解`u-boot`的相关配置指令和它具体的作用，这里我就不装大佬了，直接放其他大佬的结论：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230826111744.png)

这里的启动流程图是全志`V3S`的，`F1C200S/F1C100S`用户手册中并没有相关说明，启动顺利都是一样的

> 1. 上电后, `f1c100s`内部`BROM`(芯片内置，无法擦除)启动
> 2. 首先检查 `SD0`有没有插卡, 如果有插卡就读卡`8k`偏移数据，是否是合法的启动数据, 如果是`BROM`引导结束, 否则进入下一步
> 3. 检测`SPI0 NOR FLASH(W25QXXX, MX25LXXX)` 是否存在, 是否有合法的启动数据, 如果是`BROM`引导结束, 否则进入下一步
> 4. 检测`SPI0 NAND FLASH`是否存在, 是否有合法的启动数据, 如果是`BROM`引导结束, 否则进入下一步
> 5. 因为找不到任何可以引导的介质，系统进入`usb fel`模式， 可以用`USB`烧录了。

根据上面这些内容，我们知道`F1C200s`启动的时候会优先去`SD0`的`8k`偏移处读取数据，所以需要我们把`uboot`写入到`sd`卡`8k`偏移处即可被正常读取。

至于上面这些启动顺序逻辑是直接由芯片内部的代码逻辑控制的，我们是没法进行变更修改的。


### uboot下载编译烧录

#### 环境准备

这里需要在`linux`环境下操作，我用的是`wsl`，还挺方便的，就是不支持`dd`命令，也没法用`gparted`（虽然能安装，但是用不了），关于`wsl`的安装配置，可以看下之前的内容。


另外还需要`linux`虚拟机，主要是为了烧录系统和`sd`卡分区，最开始我是双系统，在`wsl`编译，然后在`ubuntu`烧录，但是要一直重启系统，很不方便，应该有小伙伴疑问为啥不直接在`ubuntu`上直接编译烧录，因为我的`ubuntu`编译一直报错，不想花时间折腾了，所以搞了个虚拟机进行烧录和分区。

虚拟机推荐`vm workstation`，`win10`的读不了`USB`设备。

##### 源码下载

以上工作完成后，就可以下载我们的`uboot`源码了：

```sh
git clone https://gitee.com/LicheePiNano/u-boot.git -b nano-v2018.01&&cd u-boot
```

这里没有什么好说的，都是简单的`git`操作，克隆指定分支，然后进入`u-boot`源码目录

#### 编译准备

克隆完成后就可以直接开始编译了，在有些文档中，博主会修改`Makefile`，这样后面再编译就不用指定参数了，但是也给很多小白带来了困惑，这里我建议大家直接通过指定参数的方式进行编译，因为如果改错了，会带来更多问题。

##### 选择编译配置

首先是生成编译配置文件，`configs`文件夹下有两个`licheepi_nano`相关的配置文件，需要你根据自己的需要进行选择：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230826115832.png)

第一个是默认配置，没有`spiflash`的都选择这个；

如果你有`spiflash`，而且需要用到`spiflash`，那你就选择第二个，选择第二个你需要通过`sunxi-fel`写入我们编译的`u-boot`镜像，具体可以参考下面这个文档：

```sh
https://whycan.com/t_7558.html
```

确定好配置文件之后，通过下面的命令生成我们的编译配置文件：
```sh
##  有flash的用这个
# sudo make licheepi_nano_spiflash_defconfig

sudo make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- licheepi_nano_defconfig
```

通常针对同一个设备，这个命令只需要执行一次，因为每次执行都会把我们之前的配置覆盖掉。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230826120901.png)


##### 配置核心启动信息

之后，我们需要通过如下方式来配置我们的`u-boot`编译信息，执行之后会在我们终端里面模拟一个`GUI`菜单，让我们通过图形化进行操作：

```sh
sudo make ARCH=arm menuconfig
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230826121207.png)

通过`Tab`、方向键进行菜单切换，空格键控制勾选和取消勾选，回车键进行确认，可以自己摸索适应下。

这里需要修改三个选项：

- 勾选`Enable boot arguments`，勾选之后`Boot arguments (NEW)`配置项才会展示


- 配置`Boot arguments (NEW)`内容

- 配置`bootcmd value`


第一个勾选`Enable boot arguments`没什么好说的，直接选择，然后空格进行勾选

###### 配置Boot arguments (NEW)

配置内容如下：

```sh
console=tty0 console=ttyS0,115200 panic=5 rootwait root=/dev/mmcblk0p2 rw
```

这里简单解释下配置的作用：

- `console=tty0 console=ttyS0,115200`是指定串口端口和频率；
- `panic=5`是设置`panic`异常的等待时间，也就是发生`Kernel panic`后等待的时间，单位是秒；
- `rootwait`参数的作用是内核无限期地等待根设备出现，如果不存在根设备会导致后续启动失败
- `root=/dev/mmcblk0p2`是指定`linux`文件树系统的分区，后面我们在`linux`编译烧录的时候会看到，这个分区其实就是`rootfs`分区，存放文件系统
- `rw`是告诉内核将根文件系统挂载为读/写

这个配置最核心的其实是第一个配置项，如果第一个配置不对，其他的就算配置没有问题，也没用，因为在本次项目中，我只能通过串口查看相关信息。

###### 配置`bootcmd value`

配置内容如下：

```sh
load mmc 0:1 0x80C00000 suniv-f1c100s-licheepi-nano.dtb;load mmc 0:1 0x80008000 zImage;bootz 0x80008000 - 0x80C00000;
```

这里简单解释下，`load mmc`有三个参数：第一个参数是`mmc`(`TF`卡)分区，第二个参数是内存中目标地址，第三个参数是源文件。

`bootz`命令的作用是启动`zImage`镜像文件，它的命令格式如下：

```sh
bootz [addr [initrd[:size]] [fdt]]
```

命令有三个参数:

- `addr` 是 `Linux` 镜像文件在 `DRAM` 中的位置
- `initrd` 是 `initrd` 文件在`DRAM` 中的地址，如果不使用 `initrd` 的话使用`-`代替即可
- `fdt` 就是设备树文件在 `DRAM` 中的地址

所以上面这些配置就是执行两条`load mmc`命令和一条`bootz`命令:

- 第一条命令意思是将`mmc`的`0:1` 分区中的`suniv-f1c100s-licheepi-nano.dtb`复制到内存中的`0x80C00000`地址处。这里的`suniv-f1c100s-licheepi-nano.dtb`就是`Linux`的设备树文件，`0:1`这个可以这样理解`0`表示`TF`卡，`1`这表示`TF`卡的第一个分区(`boot`分区)后面会提到。
- 第二条命令意思是将`mmc`的`0:1` 分区中的`zImage`复制到内存中的`0x80008000`地址处。`zImage`就是我们生成的`linux`内核文件，后面我们会专门分享`linux`内核的编译和烧录
- 第三条命令的作用就是启动`linux`和设备树文件

配置完成后是这个样子的，然后选择保存，退出：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230826130127.png)

这里推荐一种方式检查配置文件是否配置正常，可以用文本工具打开`.config`文件进行确认，我直接`vim`，相关配置在`270`行附近：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230826130425.png)

#### 编译

在开始正式编译之前，我们要先配置交叉编译环境，也就是配置`f1c200s`的编译环境。因为我们的电脑通常都是`x86`架构，所以需要通过交叉编译来编译成`f1c200s`能够运行的可执行文件。

这里顺便解释下什么是交叉编译：
> 交叉编译是指在一台计算机上进行编译生成可以在另一台不同架构的计算机上运行的程序。常见的应用场景是将程序从开发机上编译成能够在嵌入式系统、移动设备或其他平台上运行的可执行文件。
> 在进行交叉编译时，需要使用特定的编译工具链，该工具链包含了针对目标平台的编译器、链接器和库文件。

##### 安装依赖

执行`sudo apt update`和`sudo apt upgrade`更新软件，然后安装编译依赖的软件包：

```sh
sudo apt install xz-utils nano wget unzip build-essential git bc swig libncurses5-dev libpython3-dev libssl-dev pkg-config zlib1g-dev libusb-dev libusb-1.0-0-dev python3-pip gawk bison flex 
```

等待安装完成

##### 开发工具链下载

然后我们需要安装交叉编译工具链，编译工具链官网：<https://www.linaro.org/>

你也可以根据自己的需要下载对应的版本，直接下载链接：

```sh
http://releases.linaro.org/components/toolchain/binaries/
```

然后选择版本，这里选择的是`latest-7`，之后进入`arm-linux-gnueabi`目录，选择要下载的版本，我选择的是`gcc-linaro-7.5.0-2019.12-x86_64_arm-linux-gnueabi.tar.xz`，你也可以直接通过`wget`直接下载：

```sh
# 下载
wget https://releases.linaro.org/components/toolchain/binaries/latest-7/arm-linux-gnueabi/gcc-linaro-7.5.0-2019.12-x86_64_arm-linux-gnueabi.tar.xz

# 解压
tar -xvf gcc-linaro-7.5.0-2019.12-x86_64_arm-linux-gnueabi.tar.xz

# 创建文件夹
sudo mkdir /usr/local/arm

# 移动工具链
sudo mv gcc-linaro-7.5.0-2019.12-x86_64_arm-linux-gnueabi/ /usr/local/arm/
```

配置工具链：

```sh
nano  ~/.bashrc
# 或 vim ~/.bashrc
```

添加工具链环境变量：

```sh
export PATH=$PATH:/usr/local/arm/gcc-linaro-7.5.0-2019.12-x86_64_arm-linux-gnueabi/bin
```

通过`source`命令让配置生效：

```sh
source ~/.bashrc
```

确认工具链是否配置成功：

```sh
arm-linux-gnueabi-gcc -v
```

我本地的`wsl`实际安装的版本是`9.4.0`:

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230826151053.png)

至此，我们的工具链算是配置完成，下面就开始正式的编译。

##### 正式编译

首先要确保我们进入了`uboot`的源码根目录：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230826151335.png)

然后开始执行我们的编译命令：

```sh
sudo make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- -j8
```

这里的`-j`指定的是编译的核心数，这个数字具体取决于我们的电脑`cpu`核心数，对编译结果没有影响，只是会影响编译速度，具体根据电脑核心数设置。

另外`ARCH`和`CROSS_COMPILE`可以配置在`Makefile`中，这样参数就可以省略了：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230826151751.png)

如果你的运气够好，很快就可以看到编译成功：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230826151850.png)

这里生成的`u-boot-sunxi-with-spl.bin`就是我们需要的文件，后面烧录的就是这个文件。

然鹅，现实总是残酷的，哪能一次就让你成功，下面就是我踩到的一些坑：

##### 报错记录

- `arm-linux-gnueabi-gcc: command not found`：这个可能是最开始我没有配置工具链，解决之后，工具链也不需要手动配置了，时间久了，我也记不清楚原因了

![arm-linux-gnueabi-gcc: command not found](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221227215448.png)

解决方法：

```sh
 sudo apt install gcc-arm*
```

- `No module named _libfdt`：这个是因为编译需要用到`python2`，而本地默认的`python`链接的是`3.8`

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221227214530.png)

本地`python`的软连接记录：

![python软连接](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221227214750.png)

解决方法：

```sh
sudo ln -f /usr/bin/python2 /usr/bin/python
```

变更后：
![变更后](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221227214905.png)

- `Python.h: No such file or directory`：这个是因为少包了

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221227214411.png)

解决方法：

```sh
apt install python-dev
```

- `multiple definition of 'yylloc'`：这个问题是因为`gcc`版本的问题，导致语法不能识别

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202308262339536.png)

解决方法：
编辑`scripts/dtc/dtc-lexer.lex.c_shipped`文件

```sh
vim scripts/dtc/dtc-lexer.lex.c_shipped
# 并在634行 YYLTYPE yylloc 前面加上extern
```

并在634行 `YYLTYPE yylloc `前面加上`extern`

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202308262342857.png)


- `Unable to parse input tree`：这个也是因为版本的问题

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202308262349092.png)

解决方法：

修改`scripts/Makefile.lib`，找到下面这行代码，删除其中的`/`

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202308262346239.png)

解决完这些问题之后，`u-boot`就编译成功了。至此，`u-boot`的编译就完成了，下面我们开始`u-boot`烧录。

### 镜像烧录

首先要确保我们的`linux`环境可以连接`USB`设备，虚拟机也可以，准备一张`SD`卡，插入读卡器，连接电脑，我这里以接入虚拟机为例：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230826153648.png)

通过`fdisk`找到我们的设备编号：

```sh
sudo fdisk -l
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230826154206.png)

确认无误后，通过如下命令，将我们上面编译好的`u-boot-sunxi-with-spl.bin`文件烧录到我们的`SD`卡：

```sh
sudo dd if=path/to/u-boot-sunxi-with-spl.bin of=/dev/sdb bs=1024 seek=8
```
`dd`命令是一种用于数据转换和复制的命令行工具。这里的`if`表示读入数据的文件路径，也就是我们的`u-boot-sunxi-with-spl.bin`的存放路径，相对路径绝对路径都可以；`of`表示要写入的目标文件路径，这个别搞错了，写错地址，磁盘数据就丢了；`bs`表示设置读入/输出的块大小为多少个`K`字节；`seek`表示从输出文件开头跳过多少`K`个块后再开始复制，也就是偏移量，这里的`8`就来源于我们前面说到的加电启动偏移量。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230826155906.png)

至此，`u-boot`烧录也成功了，接下来，让我们插上`sd`卡，加电启动，这里我就直接贴上我当天启动成功写的记录：

#### 成功点亮

今天我又把之前的板子拿出来研究了，起因是我前天睡不着，翻开了我的原理图，对比了其他大佬的原理图，发现我好像把串口的电阻阻值单位搞错了，其他大佬要么没有电阻，要么有也是多少欧姆，而我画的是`470KΩ`，怪不得串口一直不能正常工作。当然，上次串口报错主要还是我把串口连接搞错了。

另外，今天主要的改动点是，我把串口`USB`后面的保险丝直接拿掉了，不知道保险丝是不是坏了，保险丝后面的电压直接变成`2.67V`，拿掉保险丝，之后连接串口，终端终于显示正常了：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230819124737.png)

看到这些信息，我简直不要太激动，前前后后，断断续续差不多搞了一年了，心态都被搞崩了，但是此时此刻，我觉得踩的坑都是值得的，奥里给~

连接串口，并将波特率设置为`115200`，这个就是我们前面设置启动参数的的时候设置的，这里工具推荐`xshell`，当然用`putty`也可以：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230826160540.png)

串口端口号具体看电脑识别情况，我这里识别的是`COM3`:

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230826160953.png)

连接串口之后如果日志打印不完整或者没有显示，有两种方法可以让信息重新打印，一种就是直接按`reset`按钮，让芯片重新上电启动，另一种是按几次回车之后，输入`reset`，这个命令的作用与`reset`按钮是一样的，最开始我输入的命令是`pri`，这个命令的作用是打印芯片的相信信息:

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230826161035.png)

更多命令可以自行百度:

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230826161334.png)


如果仔细观察`u-boot`打印的信息，你会发现有如下错误提示：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230826161427.png)

这个是因为`u-boot`启动成功后去加载设备树文件和`linux`内核，但是由于我们`SD`卡并不包含这两个文件，同时分区也不对，所以肯定没法启动，`linux`内核和设备树文件编译我们会在后面的内容专门分享，感谢大家的支持，今天的内容就到这里吧。


## 结语

在开始整理这块内容之前，原本想着篇幅应该很快能结束，因为这块的内容相对简单，至少相对于电路设计简单，然而实际整理和梳理时才发现，这里真正重要的其实是编译烧录之前的内容，包括一些概念性的内容，以及某些设置、选择背后的原因，这样来说今天的分享更像是针对`u-boot`编译的复盘，当然这也是有必要的，毕竟在第一次做这件事的时候，很多细节和问题在当时并没有意识到，但是现在来看，确实踩坑确实太低级了


参考内容：
1. <https://whycan.com/t_1746.html>
2. <https://www.cnblogs.com/twzy/p/14865952.html>
3. <https://github.com/peng-zhihui/Planck-Pi>
