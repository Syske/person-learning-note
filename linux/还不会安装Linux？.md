# 还不会安装linux系统？

最近一段时间，网上有很多关于迁移到Linux环境的文章，大同小异地都在说Linux用起来如何爽，今天我也来蹭波热度，给大家分享下如何安装Linux操作系统。客观来说，操作系统本无好坏之说，只要够用就好，适合的就是最好的，当然爱折腾的人另说（我觉得我就是）。

## Linux简单介绍

先来简单介绍下Linux。Linux是自由和开放源代码的操作系统（属于unix体系，像苹果的mac也属于此体系）。由Linus Torvalds出于爱好开发的，于1991年10月5日发布，到今天Linux已经29岁了。

本质上来讲，Linux只是操作系统内核，基于它开发的操作系统特别多，比如安卓（Android），pc端的发行版本也比较多，比如Deppin、Ubuntu、Debian、RedHat、Centos、manjaro、elementary OS、麒麟操作系统等。

其中Deppin是国内目前做的最好的操作系统，由武汉深之度开发，全球Linux发行版排名第11位，前段时间特别火的UOS系统就是由他们主导开发的。Deppin OS系统很漂亮，也符合国人使用习惯，生态圈也比较完善，有成熟的应用商店，像我们日常用到的软件都有：微信、QQ、WPS、搜狗输入法、网易云音乐等；

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200829102320.png)

银河麒麟操作系统是由中标麒麟软件开发的，风格类似win7，有统一软件商店，大部分国产软件都支持，如：搜狗输入法、WPS等。同时最新发布的v10，整合了技德（这个公司特别强，其开发的Renux OS因为威胁到安卓操作系统，被迫下线消费者版）开发的安卓虚拟技术Kydroid3.0，可以让pc端完美运行安卓app，目前支持2000余款安卓应用（如微信、QQ、办公、股票、游戏等）

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200829101820.png)

Ubuntu，很多小白的Linux入门必选，优麒麟就是Ubuntu中国版，对国人比较友好，好多软件可以直接下载后安装，比如搜狗输入法、WPS、网易云音乐等

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/c404705c-video-youtube.jpg)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/qilin-4k.png)

elementary OS号称最美的Linux发行版，系统特别漂亮

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/desktop.jpg)

RedHat是红帽公司开的商业操作系统，操作系统本身开源免费，当增值服务需要付费，目前该公司已被IBM收购。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200829101940.png)

manjaro就是我们今天的主角，我今天演示的就是它的安装。它是全球目前最流行的发行版本，排名第一，系统性能优秀。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/13.png)

## manjaro安装演示

我自己特别喜欢linux操作系统，从上大学开始，就经常体验各类Linux发行版，到目前为止我的电脑一直是双系统，最近正在考虑将Linux作为日常工作的主系统来用，所以如果你也有兴趣的话，大胆地折腾起来。

### 准备工作

#### 下载操作系统

- 下载地址：https://manjaro.org/download/
- 我这里演示的是xfce版本，你也可以根据自己的需要，不知道咋选的话，就下载gonme版，kde系统界面比较好看

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200829102713.png)

#### 准备优盘

准备一个4G以上U盘，用于制作系统启动盘

#### 系统启动盘制作

制作工具我选的是win32ImgWriter，你也可以用其他的。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200829103239.png)

制作完成后，直接重启电脑，然后选择优盘启动

### 系统安装

#### 启动界面

重启电脑后，选择优盘启动，会出现如下界面，如果你不做任何操作，他会默认进入live系统，可以作为体验版使用。也就是说你可以选择不安装直接体验。当然，这个界面你可以这只语言版本，改为中文

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/1.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/2.png)

#### 进入live系统

直接启动后，会进入如下界面，也就是桌面

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/3.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/4.png)

在这里你可以直接体验系统各种操作，你也可以选择桌面的安装，将系统安装到你的硬盘上。

#### 配置安装信息

##### 选择语言

双击桌面的安装程序，开始系统安装前的配置，首先选择语言

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/5.png)



##### 选择区域

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/6.png)



##### 选择键盘布局

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/7.png)



##### 选择磁盘并进行分区设置

这里你如果打算安装双系统的话，需要选择手动分区

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/8323.png)



##### 设置用户信息

这里包括用户名、主机名、用户密码、root用户及密码的设置

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/9.png)



##### 选择是否安装office

因为我要安装WPS，所以这我选择不安装ofiice

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/10.png)



#### 开始安装

完成上面配置步骤后，下来就要开始安装了

##### 安装确认

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/11.png)



##### 开始安装

这里要等十几二十分钟，具体时长取决于你的电脑配置。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/12.png)



##### 安装完成

经过漫长等待，系统安装完成，现在让我们重启，体验刚刚安装的manjaro![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/14.png)

#### 开始使用

##### 用户登陆

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/15.png)



##### 用户桌面

安装完成，登陆后页面是这样的，如果你选择的是其他版本，界面会有一些差异。![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/16.png)



到这里今天的内容就结束了，考虑到篇幅，系统的配置和常用软件的安装放到下一次来讲，如果你想马上用起来，你可以找找相关资料文档，网上的教程还是比较丰富的。

