# win10开启wsl系统，让我们愉快的使用Linux

### 前言

不知道各位小伙伴是否有听说过`wsl`呢？`wsl`的全程是`Windows Subsystem for Linux`，也就是`windows`的`linux`子系统，它是由微软与`Canonical`公司合作开发的，从`win10`开始支持`wls`开始，我就一直在关注，而且一直在用。了解我的小伙伴应该知道，我其实特别喜欢`linux`操作系统，特别是`ctl`（命令行终端）模式，用起来很方便，感觉也很爽，在我心里，`linux`才是操作系统`yyds`，只是很多常用的办公软件不支持，其他的没得说。

好了，扯远了，我们回到今天的主角——`wsl`。如果启用了这个功能，我们就可以在`windows`环境下愉快地使用`Linux`，对像我这样爱折腾的小可爱来说，简直就是福音了。

以前没有这个开源项目的时候，想要用`linux`系统同时又要保留`windows`系统，所以一直电脑都装的是双系统，占内存不说，系统之间传输数据也不方便，关键是两个系统直接切换必须关机重启，不能同时使用。

但是如果你启用了`wsl`之后，特别是切换到`wsl2`之后，很多原生的`linux`应用就可以很好地使用了，当然实际使用过程中，可能也会有很多问题，但有总比没有强。

下面，我们来看下如何启用`wsl`。

### 启用wsl

#### 安装`linux`发行版

首先，我们需要进入`win10`应用商店，搜索`wsl`。目前`wsl`支持地`linux`发行版本还是比较丰富的，连大名鼎鼎的`kali`也支持（`kali`用的好，监狱进的早）

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210624130959.png)

这里面版本最全的当属`ubuntu`，很多人的`linux`启蒙发行版，我当年用的第一个`linux`就是`ubuntu`。

然后选中你要安装的`linux`，点击安装，这里以`ubuntu`为例：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210624131427.png)

然后慢慢等他安装完成。

#### 启用wsl相关功能

安装完成后，你的开始菜单会多出来这样一个软件（版本不同会有一些差别，但是大同小异）

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210624131708.png)

然后点击运行这个软件，大概率会是如下提示：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210624131532.png)

这个提示的意思是，`wsl`的功能没有用，这时候我们需要在应用里面设置一下。

首先打开应用和功能设置，点击右侧程序和功能

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210624131843.png)

接着点击左侧启用或关闭`windows`功能

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210624131948.png)

勾选启动的`Linux`的`windows`子系统这个选项，确定后重启电脑。

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210624132109.png)

这时候再次打开上面的应用，你会发现`wsl`已经启用完成了，你可以在里面进行各种`linux`的命令行操作。

真正感兴趣的小伙伴，可以去看下`windows`官方文档，里面有详细的说明，包括`wsl`的版本切换问题：

```
https://docs.microsoft.com/zh-cn/windows/wsl/install-win10
```

### 安装Windows Terminal

虽然安装完成了，但是原生的`linux`的终端确实不够美观，毕竟爱使用`bash`的小伙伴哪个不希望自己的`teminal`更好看呢？这一点`windows`已经替你想好了，我们可以使用`windows`的另一个开源项目`Windows Terminal`来让我们的命令终端更好看。

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210624132859.png)

安装方式也很简单，也是进入`windows`应用商店直接搜索安装即可：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210624133047.png)

选择第一个就可以了，第二个是预览版。关于这一块的美化，我下次专门分享吧，我是对`terminal`的颜值有要求的。

然后点击安装，等待安装完成，直接启动。

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210624133251.png)

默认启动的终端是`powershell`，你可以点击窗口标题栏右侧小箭头选你要开启的终端，其中`ubuntu`就是我们刚安装的`wsl`。

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210624133419.png)

终端也安装完成了，这样我们就可以在`windows`环境下愉快地玩`linux`，`so happy`!

原生的`docker`、`k8s`等都是可以的，最近我正在搞`wsl2`环境下的`k8s`集群部署，环境已经搭建好了，但是服务一直访问不到，等这块最后的问题解决了，后面专门再分享一期。

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210624133857.png)

希望后面`windows`上可以直接运行原生的`linux`系统，那就美滋滋了

### 总结

我一直觉得`linux`是最好的操作系统，当然事实也确实如此，除了基于`linux`的`Android`外，绝大多数的系统服务也都是跑在`linux`，而且像我们日常用到的很多嵌入式设备，比如路由器这些都是基于`linux`的，在云应用中，`linux`也一直是云环境最原生、最好的选择。

当然，从更个人的角度来说，确实是因为我喜欢这个系统，使用这个系统最大的乐趣就是只要你动手能力强，你可以`linux anything`，你可以尽情折腾，而且整个过程很有趣。

最后，关于国产操作系统，我想说几句。网上经常有人喷国产的某个系统是基于`linux`的套壳系统，什么就是换了一层皮……我想说的是，`linux`作为最优秀的操作系统（没有之一），基于它开发国产操作系统并不丢人，而且这些年我们也没少给`linux`做贡献，根据最新`linux`内核贡献榜数据，华为已经荣登贡献榜榜首：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210624142443.png)

操作系统难的并非是技术，而是生态圈，就算你做了一个全球最牛逼的操作系统，但是常用的软件都不支持，也没有开发者愿意为这个操作系统开发软件，那依然解决不了国产操作软之痛。在这个无人愿意探索的领域，更需要的应该是支持和鼓励，而不是质疑和职责，用一句流行的话说就是，可以不爱，但请别伤害……



