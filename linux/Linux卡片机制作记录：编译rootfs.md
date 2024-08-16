
### 前言

昨天我们分享了`linux`内核的编译过程，我们今天来再接再厉，分析`rootfs`的编译过程。顾名思义，`rootfs`的全称就是`root file system`，也就是根 文件系统，如果说`linux`内核是提供我们与硬件（`CPU`、`USB`、现实等）交互的能力，那么`rootfs`就提供让我们与文件交互的能力。

下面是`linux`的系统架构图，等下我们可以看到，其实在编译`rootfs`的过程，我们也是可以配置我们的`shell`的，按这个逻辑来说，`shell`其实也算是`rootfs`的一部分。
好了，废话少说，让我们直接开始吧！


![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/c50500d5-2576-42bb-b142-c9b34e20b55e.jpg)

### 编译rootfs
#### 下载解压源文件

和编译内核类似，也需要先下载源码，这里我用的也是比较新的版本。下载完之后直接解压即可

``` sh
# 下载
wget https://buildroot.org/downloads/buildroot-2024.05.tar.xz
# 解压
tar -xvf buildroot-2024.05.tar.xz
```

然后进入源码根目录，开始配置编译菜单。

#### 编译配置

这里配置的就是编译之后的`rootfs`的功能以及编译过程中的一些配置项，包括`shell`、依赖下载镜像、芯片版本等，下面我们逐步展开解释。

```sh
# 编译
make menuconfig
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810104345.png)

##### Target options

首先配置目标选项，这里主要是选择芯片的架构，配置指令集等信息，`F1C200s/F1C100s`直接参照下图配置即可

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810104229.png)

因为`F1C200s`的文档说的很清楚，其架构是`ARM9`:
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/7e58854d-9390-46da-9d39-be8ff6bfbe9d.jpg)
##### Build options

这个选项下面，我们配置的就是编译相关的内容，需要配置两个：镜像、库

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810104658.png)
###### Mirrors and Download locations

这里配置的是编译过程中的依赖下载镜像，如果不修改这个，编译会特别慢，而且容易失败，我下面的配置都是实测的，可以直接参照修改。

- 原配置：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810105108.png)

- 配置后
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810105452.png)

这里是对应的配置
```text
Backup download = http://sources.buildroot.net  
Kernel.org mirror = http://mirrors.ustc.edu.cn/kernel.org/ 
GUN Software mirror = http://mirrors.nju.edu.cn/gnu/
LuaRocks mirror = https://luarocks.cn  
CPAN mirror = http://mirrors.nju.edu.cn/CPAN/s
```

北京交大的镜像慢了，可以换一下网易的
```
Kernel_mirror = http://mirrors.163.com/kernel/
```


###### libraries

库`libraries`这里选择`both static and shared`，默认是`shared only`。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810110449.png)

##### Toolchain 

这里是内核和头文件的设置。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810110603.png)

在这个选项下，我们要配置`C`的库、`kernel`的头文件版本，关于头文件版本不知道具体有什么差异，我这里保险起见，选择了比内核版本低的版本，我的内核版本是`6.4`，但是选项中没有`6.4`

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810111648.png)

关于`C`库的差异，我搜索到如下内容：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810111557.png)

其他配置项，根据自己的需要启用
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810112105.png)

#### 系统配置

这里的配置项包括主机名、欢迎语、`root`密码等，其他的设置项可以自己研究下

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810112351.png)

这里说一下`sh`设置`zsh`的方式，也是在系统配置下面

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810131214.png)

默认情况下是不能选择`zsh`的，需要启用`BR2_PACKAGE_BUSYBOX_SHOW`
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810131439.png)

设置的路径如下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810133422.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810133541.png)

然后，`shell`就可以修改了
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810133706.png)

然后，保存设置并退出。

至此，编译配置完成，下面开始正式编译。

### 开始编译

```sh
make -j6
```

如果不出意外的话，最后会有如下提示，表示`rootfs`编译成功：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/400457a3-e0f1-4ed2-a095-7fd487247b21.jpg)

编译成功的文件路径如下，文件名：

```sh
buildroot-2024.05\output\images\rootfs.tar
```

相比内核`rootfs`编译过程要顺利太多，基本上没有报错。

#### 报错1

缺少`cpio`

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810135204.png)

解决方法：

直接安装相关依赖即可，然后继续编译



#### 烧录

`rootfs`不需要特殊烧录，我们直接通过`tar`解压到我们内存卡的对应分区即可。

```
sudo tar -xvf rootfs.tar -C /media/syske/rootfs/
```

需要注意的是在前面编译内核的时候，我们设置的`rootfs`分区格式是`ext4`，所以在`wsl`环境下是无法识别的，所以需要用户`linux`的系统，我直接安装的双系统`win + ubuntu`，没有双系统的小伙伴可以直接上虚拟机，相关内容我在《`uboot`编译烧录》已经分享过了，这里就不赘述了。

完成上述操作，我们直接上电操作即可。关于上电演示的图片，昨天已经分享过了，今天再贴一次：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240809012228.png)

按照正常流程，没有`rootfs`的`linux`是无法登陆的，默认`root`密码我们再编译配置的时候设置了，用那个密码直接登录即可。

虽然`F1C200s`的运行内存只有`64M`，但是单跑`linux`命令行还是很流畅的。

### 结语

到这里`linux card`制作基本上告一段落，目前发现之前的电路设计还有一些问题，比如无法以`host`的方式识别`USB`设备，这样就无法连接鼠标、键盘、网卡，所以后面会要再调整下电路，然后继续折腾。

初步的规划是，参照稚晖君的`Planck-Pi`项目，在原有电路基础上增加`OLED`屏幕，优化`USB`电路，将其中一个`micro USB`改成`Type`口，电路基本已经完成了，后续会打样重新焊接，放几张渲染图给大家看看：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/875df898-8dea-40a0-bc46-f4cf03b64973.jpg)
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/959a88c1-633a-4ee9-98cd-dc12b69f76ca.jpg)