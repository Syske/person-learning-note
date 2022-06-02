# wsl安装其他盘解决方案



### 前言

最近有小伙伴在问`wsl`默认安装在`C`盘的问题，觉得安装在`C`盘太占内存，毕竟一般新买的电脑默认`C`盘也就分了`100`多`G`，时间久了确实不够用。以前我还真没关注过这个问题，但是最近我发现我的`C`盘也越来越小了，甚至这几天已经飘红了，所以今天就来解决下这个问题。

### 解决问题

#### 好家伙，直接解决问题

有时候，感觉解决一个问题往往就是如此简单，当我想要解决这个问题的时候，我在`windows`应用商店`ubuntu`的评论区竟然就找到了问题的答案，起初我是不信的，但是看到上千人点赞，我决定试一下：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211008193136.png)

#### 下载软件包

我访问了评论里面提到的地址，找到了下载地址：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20211008211443.png)

选择对应的版本就可以直接下载了，因为我之前安装的是`18.04`，所以我依然选择这个版本，如果不知道的话就选`20.04`或者`18.04`，然后等待下载完成，这里下载的是扩展名为`.appx`的软件包：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20211008212035.png)



#### 解压

接着，修改软件包扩展名，改为`.zip`即可，然后解压（想安装到哪个磁盘，解压到哪个磁盘）：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20211008212352.png)



#### 双击运行

直接双击我们解压的`ubuntu1804.exe`可执行文件就可以开始安装了：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20211008212648.png)

然后输入用户名和密码之后，`wsl`安装成功。同时，我们可以发现，在`ubuntu1804.exe`的同级目录下，会生成一个`.vhdx`的文件，这个文件就是`wsl`的虚拟磁盘，说明我们的`wsl`已经成功的安装在了`D`盘。



#### 遇到的问题

虽然整个过程很简单，但是我还是遇到了一些问题。为了偷个懒，我没有修改文件扩展名，而是用`7-zip`直接拖到本地文件加中，结果启动的时候报错了：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211008194711.png)

搜了下这个错误码，说是我没有启动`windows update`服务，然后一顿操作之后，依然不行。然后又老老实实改了下扩展名，再运行又好了，有点诡异呀。所以各位小伙伴最好老老实实改名，然后再解压运行。



#### 扩展

关于上面我们这种操作方式，其实`windows`官方是有说明的，我是在解决`0x80070002`这个问题的时候发现的：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20211008213620.png)

它这里就是我们上面的操作，只是它是基于命令行操作的，下面是详细文档地址：

```
https://docs.microsoft.com/zh-cn/windows/wsl/install-on-server
```

#### 资源地址

评论提到的地址：

```
https://docs.microsoft.com/en-us/windows/wsl/install-manual
```

中文地址如下：

```
https://docs.microsoft.com/zh-cn/windows/wsl/install-manual
```

下面是软件包的下载地址，不想自己找的小伙伴可以直接访问下载

- `Ubuntu 20.04`

  ```
  https://aka.ms/wslubuntu2004
  ```

  

- `Ubuntu 20.04 ARM`

  ```
  https://aka.ms/wslubuntu2004arm
  ```

  

- `Ubuntu 18.04`

  ```
  https://aka.ms/wsl-ubuntu-1804
  ```

  

- `Ubuntu 18.04 ARM`

  ```
  https://aka.ms/wsl-ubuntu-1804-arm
  ```

  

- `Ubuntu 16.04`

  ```
  https://aka.ms/wsl-ubuntu-1604
  ```

  

- `Debian GNU/Linux`

  ```
  https://aka.ms/wsl-debian-gnulinux
  ```

  

- `Kali Linux`

  ```
  https://aka.ms/wsl-kali-linux-new
  ```

  

- `SUSE Linux Enterprise Server 12`

  ```
  https://aka.ms/wsl-sles-12
  ```

  

- `SUSE Linux Enterprise Server 15 SP2`

  ```
  https://aka.ms/wsl-SUSELinuxEnterpriseServer15SP2
  ```

  

- `openSUSE Leap 15.2`

  ```
  https://aka.ms/wsl-opensuseleap15-2
  ```

  

- `Fedora Remix for WSL`

  ```
  https://github.com/WhitewaterFoundry/WSLFedoraRemix/releases/
  ```

  

### 总结

好了，关于`wsl`安装在非`C`盘的解决方案我们暂时就先说这么多，还有疑问的小伙伴可以留言或者私信，我们可以继续探讨。

最后再多说一些闲话，就在刚刚，我刷到了野生钢铁侠稚晖君刚更新的视频——《我造了一台钢铁侠的机械臂》，整个内容挺震感的（视频的分量太重了），主要是巨佬（大佬已经无法形容了）太强了，从前期设计、画图，到硬件开发、软件开发，再到算法开发，全都是一个完成，真的是一个人干了一个团队甚至一个公司都干不了的事，这可能就是天才和我们普通人的区别吧！

其实，关注巨佬好久了，每一次都能拿出让你不得不佩服的作品，真的是太强了，让你看完之后有一种强烈的自卑感，感觉自己好像是原始人一样，当然我也深深地被巨佬所激励，我觉得我得好好努力了，因为我就特别想成为这样的极客，我对硬件开发有着一种特殊的情感……好了，下面给大家几张评论截图，自己感受：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20211008221233.png)

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20211008221939.png)

感兴趣的小伙伴可以去`B`站看下原视频，说不定你就找到前进的动力了呢！
