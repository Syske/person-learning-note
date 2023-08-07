# linux card开发板制作

## 电路设计

这里其实是踩坑最多的，因为这里如果设计不正确，会导致后面直接失败，先来看下我都踩了那些坑

### 串口电路连接错误

在本次设计中，串口芯片用的是`CH340E`，电路比较简单，但是`CH340E`的`RXD`和`TXD`应该分别对应主控芯片的`TXD`和`RXD`，但是对于我这样的小白来说，我一直觉得应该是一一对应的，结果导致的原因就是按下`RESET`按钮之后，串口通信就断开了，百思不得其解，最好对比了一众大佬设计的原理图，发现自己搞错了，下面是一众大佬的设计：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230421111412.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230421111519.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230421112335.png)


## 打板焊接

打板直接就在嘉立创白嫖了，由于设计错误，我已经打了`6`次板了，但是这一路踩坑，确实也学了很多，也成长了，从刚开始连封装为何物，到后面可以看懂大佬的原理图，能看懂简单的数据手册，到现在这个板子的设计、打板、焊接、编译、烧录，虽然还是小白，但也慢慢能找到自己的方向。


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
make licheepi_nano_spiflash_defconfig
make menuconfig
```


![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221226210230.png)



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
