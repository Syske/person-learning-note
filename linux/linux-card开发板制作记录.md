# linux card开发板制作

## 电路设计



## 打板焊接


## 镜像烧录过程

### 准备工作

#### 安装驱动

```
https://zadig.akeo.ie/
```

#### 安装芯片工具

```sh
sudo apt install pkg-config pkgconf zlib1g-dev libusb-1.0-0-dev
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
