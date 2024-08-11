

#### 下载解压源文件

``` sh
# 下载
wget https://buildroot.org/downloads/buildroot-2024.05.tar.xz
# 解压
tar -xvf buildroot-2024.05.tar.xz
```


#### 编译配置

```sh
# 编译
make menuconfig
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810104345.png)

##### Target options
这里主要是选择芯片的架构，配置指令集等信息，`F1C200s/F1C100s`直接参照下图配置即可

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810104229.png)

##### Build options

这个选项下面，我们需要配置两个：镜像、库

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810104658.png)
###### Mirrors and Download locations
原配置：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810105108.png)

配置后
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

这里选择`both static and shared`

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810110449.png)

##### Toolchain 

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810110603.png)

在这个选项下，我们要配置`C`的库、`kernel`的头文件版本

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810111648.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810111557.png)

其他配置项，根据自己的需要启用
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810112105.png)

#### 系统配置

包括主机名、欢迎语、`root`密码等，其他的设置项可以自己研究下

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


### 开始编译


#### 报错1

缺少`cpio`

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240810135204.png)


#### 复制

```
sudo tar -xvf rootfs.tar -C /media/twzy/rootfs/
```