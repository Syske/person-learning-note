# manjaro安装配置指南

系统安装完成后，第一次进来效果如下，因为我选择的是`gnome`版本的，所以和`kde`、`xface`显示会有一些差异。

![](https://gitee.com/sysker/picBed/raw/master/manjaro/2021-10-25 03-26-48屏幕截图.png)

然后打开终端

![](https://gitee.com/sysker/picBed/raw/master/manjaro/2021-10-24 23-19-15屏幕截图.png)

### 基本配置

#### 选择国内镜像

```sh
sudo pacman-mirrors -i -c China -m rank
```

```sh
sudo pacman-mirrors -g
```
![](https://gitee.com/sysker/picBed/raw/master/manjaro/2021-10-24 23-17-43屏幕截图.png)

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

![](https://gitee.com/sysker/picBed/raw/master/manjaro/2021-10-24 23-31-57屏幕截图.png)

不过这个问题我们可以通过`yay`包管理工具来解决这个问题。

关于`yay`这个工具我们多说两句，因为之前安装搜狗输入法的时候用过，这次专门去查了下：

> Yay是用Go编写的Arch Linux AUR帮助工具，它可以帮助你以自动方式从PKGBUILD安装软件包， yay有一个AUR Tab完成，具有高级依赖性解决方案，它基于yaourt、apacman和pacaur，同时能实现几乎没有依赖、为pacman提供界面、有像搜索一样的yaourt、最大限度地减少用户输入、知道git包何时升级等功能。

另外关于这里提到的`AUR`也有一些说明资料：

> AUR是Arch Linux/Manjaro用户的社区驱动存储库，创建AUR的目的是使共享社区包的过程更容易和有条理，它包含包描述（PKGBUILDs），允许使用makepkg从源代码编译包，然后通过pacman安装它。

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

```
sudo pacman -Syy && sudo pacman -S archlinuxcn-keyring
```

![](https://gitee.com/sysker/picBed/raw/master/manjaro/2021-10-24 23-37-15屏幕截图.png)

如果这里安装`key`报错的话，可以用下面这种方式解决

```
sudo pacman -Syu haveged
systemctl start haveged
systemctl enable haveged

sudo rm -fr /etc/pacman.d/gnupg
sudo pacman-key --init
sudo pacman-key --populate archlinux
sudo pacman-key --populate archlinuxcn
```

```
sudo pacman -S fcitx fcitx-im fcitx-configtool
```


```
sudo pacman -S yaourt
```

```
sudo pacman -Sy base-devel
```

##### 安装yay工具

```
sudo pacman -Sy yay
```

![](https://gitee.com/sysker/picBed/raw/master/manjaro/2021-10-25 09-55-27屏幕截图.png)

##### 安装搜狗拼音

```
yay -S fcitx-sogoupinyin 
```

![](https://gitee.com/sysker/picBed/raw/master/manjaro/2021-10-25 09-56-29屏幕截图.png)

![](https://gitee.com/sysker/picBed/raw/master/manjaro/2021-10-26 17-05-05 的屏幕截图.png)

##### 添加启动配置

```sh
nano ~/.pam_environment  
```

增加如下内容：

```
GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS=@im=fcitx
```

然后重启电脑，然后就可以看到搜狗输入法了，除了不能安装好看的皮肤，其他的都还好，还挺稳定的。

![](https://gitee.com/sysker/picBed/raw/master/manjaro/2021-10-26 16-57-39 的屏幕截图.png)



#### 安装nodeJs

这里安装`nodeJs`是为了后面安装`picGo`的`gitee`插件，没有`nodeJs`插件是装不上的。

首先，官网下载对应系统的`tar`压缩文件，下载完成后解压

```sh
tar -vxf node-v14.18.1-linux-x64.tar.xz  
```

移动到目标路径，这里我直接放在了`opt`文件夹下：

```sh
sudo mv node-v14.18.1-linux-x64 /opt 
```

##### 建立链接

这里其实就是讲`npm`和`node`映射到`usr/local/bin`目录下，这样我们就可以在任意路径下执行`nmp`和`node`命令了，类似于配置环境变量。

```
sudo ln -s /opt/node-v14.18.1-linux-x64/bin/npm /usr/local/bin/ 
sudo ln -s /opt/node-v14.18.1-linux-x64/bin/node /usr/local/bin/
```

##### 修改更新源

```sh
npm config set registry https://registry.npm.taobao.org
```

