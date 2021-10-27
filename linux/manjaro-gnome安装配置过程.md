# manjaro安装配置指南

### 前言

关注我时间久一点的小伙伴应该知道，我对`linux`有着一种特殊的情怀，所以也一直特别喜欢折腾`linux`，而且在学校那会更是热衷于体验各种`linux`发行版，从那时候起我的电脑就一直是`linux + win`双系统，也一直有想法将`linux`作为自己日常系统使用，但是由于有时候还需要用到`ps`这些软件，所以也就一直是双系统。

直到前段时间换了电脑之后，旧电脑（双系统，`win`装的是固态）就一直闲置，所以我一直考虑抽个时间把系统重新整下，但一直没时间（可能是懒），一切最终在上周天发生了改变，然后就在那天开始这个`manjaro`安装计划，所以就有了今天的内容。

整个过程中，最花时间的也就是安装搜狗输入法了，可能我也是闲的，一般人折腾下就放弃了，我竟然折腾了一天半，我可能也比较爱折腾，反正整个过程还是挺爽的，特别是一切最终都经过自己的探索和尝试解决了，真的很有意义，也正是由于很有爽，所以关于整个过程我就特别能说，所以最终的结果就是这篇文章会特别长，但是过程也比较详细，而且感兴趣的小伙伴一定会找到自己的答案。

由于时间的关系，我们本次只分享`manjaro gnome`环境下搜狗输入法的安装过程，其他软件的安装配置，我们放在下次发分享，好了，说了这么多废话，我们开始今天的正文吧！

### manjaro安装搜狗输入法

前面的系统安装过程我就不再赘述了，之前已经分享过了，还想回顾的小伙伴点击下面的链接回顾：

http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648421482&idx=1&sn=538ca03374779e41bb83f74a52696409&chksm=bea6dae089d153f6f90b37de5db7d968a5f4438aac8dd33dba06d1f25bf9b1a0edf38eac86e6#rd

系统安装完成后，第一次进来效果如下，因为我选择的是`gnome`版本的，所以和`kde`、`xface`显示会有一些差异。

![](https://gitee.com/sysker/picBed/raw/master/blog/20211026233626.png)

然后打开终端，这里可以看到终端应该已经安装了`oh-my-zsh`，后面我们有时间了看下具体如何优化：

![](https://gitee.com/sysker/picBed/raw/master/blog/20211026233531.png)

### 基本配置

#### 选择国内镜像

```sh
sudo pacman-mirrors -i -c China -m rank
```

```sh
sudo pacman-mirrors -g
```
![](https://gitee.com/sysker/picBed/raw/master/blog/20211026233734.png)

#### 更新软件库

```sh
sudo pacman -Syyu
```

### 安装常用软件
#### 搜狗输入法

搜狗输入法安装过程简直不要太坑，昨天折腾到凌晨，最后搜狗输入法是安装上了，但是愣是没法启动使用，然后今天又查了一些资料，最终才搞定。

##### 安装基本依赖

`fcitx`是小企鹅输入法的依赖。小企鹅输入法是一个以 `GPL `方式发布的输入法平台,可以通过安装引擎支持多种输入法，支持简入繁出，是在 `Linux` 操作系统中常用的中文输入法。它的优点是，短小精悍、跟程序的兼容性比较好。关于小企鹅输入法的更多资料，各位小伙伴可以自行检索。

```sh
# fcitx
sudo pacman -S fcitx
sudo pacman -S fcitx-configtool
sudo pacman -S fcitx-gtk2 fcitx-gtk3
sudo pacman -S fcitx-qt5
```

网上有很多教程说，安装完以上依赖之后，可以直接通过以下命令安装搜狗拼音：

```sh
sudo pacman -S fcitx-sogoupinyin
```

但我这里是不行的，直接安装的话，会提示无法找到软件包（真后悔上次安装的时候没有形成文档，那会我安装的还可以安装官方皮肤，不知道是不是版本的问题）：

![](https://gitee.com/sysker/picBed/raw/master/blog/20211026233748.png)

不过这个问题我们可以通过`yay`包管理工具来解决这个问题，关于`yay`我们后面还会讲到它的安装。

我们先要增加下`arch-linux`的软件源，对`linux`发行版本有了解的小伙伴应该知道，`manjaro`是基于`arch-linux`发行的，所以`arch-linux`支持的软件，`manjaro`也就可以安装，因此我们添加了`arch-linux`之后，就可以在`manjaro`上享受`arch-linux`的生态，岂不是美滋滋！

##### 修改软件源权限

这里要修改下`pacman`的软件包配置：

```sh
sudo nano /etc/pacman.conf
```

这里的`nano`是一个轻量级的文本编辑器，在很多`linux`发行版中都会附带，树莓派官方`linux`中就有这个编辑器，所以我对这个工具比较熟悉。这个工具操作也很简单，直接编辑内容即可，`Ctrl + O`是写入操作，也就是保存，`Ctrl + X`是关闭。

然后在其中增加如下软件包配置：

```properties
[archlinuxcn]
SigLevel = Optional TrustedOnly
Server = https://mirrors.ustc.edu.cn/archlinuxcn/$arch
```

这里的`SigLevel`设置的是软件源的前面等级，取值范围如下：

- `TrustedOnly`：如果检查了签名，则该签名必须位于密钥环中并且完全受信任； 边际信任不符合此条件；
- `TrustAll`：如果检查了签名，则签名必须在密钥环中，但不需要分配信任级别（例如，未知或边际信任）
- `Never`：表示不进行签名检查
- `Optional`：表示将检查签名（如果存在），但也将接受未签名的数据库和软件包。
- `Required`：则所有软件包和数据库都需要签名。

默认为`Optional TrustedOnly` 

##### 更新软件源、添加key

这里主要是强制更新系统，同时还要安装`archlinuxcn-keyring`

```
sudo pacman -Syy && sudo pacman -S archlinuxcn-keyring
```

![](https://gitee.com/sysker/picBed/raw/master/blog/20211026233803.png)

我当时在安装签名的时候就报错了，当时忘记截图了，错误提示类似下面：

```sh
error: php53: signature from "lilac (build machine) <lilac@build.archlinuxcn.org>" is unknown trust
```

如果你也是这样的报错的话，可以用下面这种方式解决：

```
sudo pacman -Syu haveged
systemctl start haveged
systemctl enable haveged

sudo rm -fr /etc/pacman.d/gnupg
sudo pacman-key --init
sudo pacman-key --populate archlinux
sudo pacman-key --populate archlinuxcn
```

这个是我搜的解决方法，也是`Arch`给出的解决方案：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027055611.png)

地址如下：

```
https://www.archlinuxcn.org/gnupg-2-1-and-the-pacman-keyring/
```

##### 继续安装依赖

完成`Arch`的相关配置之后，我们还要安装一些依赖，这里的`fcitx-im`是小企鹅输入法的核心组件（`im`应该就是`input method`的简写）

```sh
sudo pacman -S  fcitx-im
```

`base`包是基础系统，基本上装`arch`这个包组都要装的，而`base-devel`里的是一些常用的开发工具，编译安装某些软件，就会用到其中的一些编译工具，比如`automake`， `cmake`之类的：

```sh
sudo pacman -Sy base-devel
```

##### 安装yay工具

关于`yay`这个工具我们多说两句，因为之前安装搜狗输入法的时候用过，这次专门去查了下：

> Yay是用Go编写的Arch Linux AUR帮助工具，它可以帮助你以自动方式从PKGBUILD安装软件包， yay有一个AUR Tab完成，具有高级依赖性解决方案，它基于yaourt、apacman和pacaur，同时能实现几乎没有依赖、为pacman提供界面、有像搜索一样的yaourt、最大限度地减少用户输入、知道git包何时升级等功能。

另外关于这里提到的`AUR`也有一些说明资料：

> AUR是Arch Linux/Manjaro用户的社区驱动存储库，创建AUR的目的是使共享社区包的过程更容易和有条理，它包含包描述（PKGBUILDs），允许使用makepkg从源代码编译包，然后通过pacman安装它。

安装命令如下：

```
sudo pacman -Sy yay
```

 这里如果在安装过程中报如下错误的话：

![](https://gitee.com/sysker/picBed/raw/master/blog/20211026233844.png)

可以将`/etc/pacman.conf`中的`community`的`SigLevel`改成`Optional TurstAll`

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027064006.png)

然后再次执行安装命令就可以安装成功：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027064413.png)

##### 安装搜狗拼音

安装完`yay`工具之后，我们就可以愉快地安装搜狗输入法了，安装命令如下

```
yay -S fcitx-sogoupinyin 
```

这里如果安装还是报错，好好检查下`pacman.conf`文件中软件源的配置项是否正常：

![](https://gitee.com/sysker/picBed/raw/master/blog/20211026233904.png)

前天晚上，我为了装好搜狗拼音，一直熬到凌晨，最后的解决方法很粗暴，直接将所有软件源的`SigLevel`改成`Optional TrustAll`：

![](https://gitee.com/sysker/picBed/raw/master/blog/20211026233919.png)

然后搜狗拼音就完美安装成功了：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/image-20211027064851922.png)

可以看到安装日志中有词库的解压操作：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027065231.png)

##### 添加启动配置

这里也是个大坑，我那天安装完后，死活无法启动，最后发现是配置文件搞错了，一个是配置文件名称搞错了，我之前创建的配置文件是` ~/.xprofile`，但是这个文件对`gnome manjaro`无效；另一个是我用`sudo`权限创建的文件，所以最终搜狗都没启动起来。最终我想明白了后一个问题，同时找到了另外一种配置方法，也就是创建这里的`~/.pam_environment`文件：

```sh
nano ~/.pam_environment  
```

然后在其中增加如下内容：

```sh
GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS=@im=fcitx
```

最后重启电脑，再然后就可以看到搜狗输入法了，除了不能安装好看的皮肤，其他的都还好，还挺稳定的。今天这篇内容，我就是在`manjaro`环境下，用搜狗拼音敲出来的。

![](https://gitee.com/sysker/picBed/raw/master/blog/20211026233936.png)





### 结语

关于最新版本的`gnome`镜像，国内镜像站都没有，官方地址我这边连不上，最后我是在`sourceforge`找到的，下载速度还可以：

```
https://sourceforge.net/projects/manjarolinux/files/gnome/
```

关于`manjaro`的镜像我下载了两次，第一次下载的`kde`版本，因为国内不好找`gnome`的资源，但是安装完之后，感觉还是`gnome`好用，可能我和最开始用的`ubuntu`有关系，所以一直觉得`gnome`挺好用的，然后又全网找`gnome`版本，最后又重新安装了一次。

而且在我重装`manjaro`我就用的`gnome`版本的，要不是我想把`manjaro`安装在固态硬盘上，我是不打算重新安装的，毕竟之前也配置了好久，而且我感觉最近更新完`gnome`，`manjaro`整体都流畅了好多。

另外需要补充说明的是，我当期的`manjaro`是基于`gnome`的，它的版本是`21.1.6`：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027070132.png)
