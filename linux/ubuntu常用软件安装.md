# Ubuntu常用软件安装

### 前言

最近，犹豫和纠结之后，又决定把`ubuntu`当做日常主要的系统来使用了，于是又开始新一轮折腾`ubuntu`的相关配置，一个算是给自己积累点知识库，另一个也算是提想尝试的小伙伴踩个坑，好了，废话少说，让我们直接开始吧。

### 常用软件安装

`ubuntu`系统的软件安装方式，一种是在线安装，也就是通过包管理命令 ` apt`进行安装，通常命令如下：

```bash
# softwareName表示软件或者包名称
sudo apt install softwareName
```

另一种是离线安装，软件包格式通常为  `*.deb`，针对这种软件包，我们最常用的安装命令如下：

```bash
# 安装deb文件
sudo dpkg -i *.deb
```

#### 搜狗输入法

首先，我们要安装`fcitx`以及相关依赖，因为搜狗输入法是基于`fcitx`构建的，而`ubuntu`的系统默认输入法是`ibus`

```sh
# 更新软件库
sudo apt update
# 安装小企鹅输入法
sudo apt install fcitx
```


然后需要去官方网站下载最新的 `deb`软件包：

```bash
https://shurufa.sogou.com/linux
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202303082242160.png)

之后，通过`dpkg`命令进行安装：

```sh
sudo dpkg -i sogoupinyin_*.deb
```

如果有报错，通过如下命令进行强制安装：
```sh
sudo apt install -f
```
之后再执行安装命令，接着还需要安装输入法的其他相关依赖：
```sh
sudo apt install libqt5qml5 libqt5quick5 libqt5quickwidgets5 qml-module-qtquick2
sudo apt install libgsettings-qt1
```

安装完成之后，重启下电脑，然后进行输入法的配置：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202303082308747.png)

配置路径：区域&语言 -> 管理安装的语言 -> 选择输入法，这里选择`fcitx4`，之后就可以通过`ctrl+空格`进行输入法切换。

#### 微信

目前微信官方并没有针对`linux`的原生应用，但是我们可以安装优麒麟应用商店的微信，下载地址如下：
```
https://www.ubuntukylin.com/applications/
```
商店内提供了三款微信，其中第二款依赖于优麒麟商店，我这边没有安装完成，我这里安装的是第一款，比较简洁，相比于`win`环境少了很多菜单。
第三款是`wine`版本的，和`win`环境下的微信功能完全一致。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202303082318025.png)

安装方式也很简单，下载对应的`deb`软件包，然后通过`dpkg`命令进行安装即可。

第一款微信：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202303082320577.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202303082321227.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202303082322628.png)


#### 钉钉

钉钉使用原生`linux`版本的，所以我们直接访问官网下载即可：
```
https://page.dingtalk.com/wow/z/dingtalk/simple/ddhomedownlaod#/
```
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202303082325939.png)

安装方式和微信一样，直接通过`dpkg`命令进行安装。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202303082326889.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202303082328481.png)


#### 截图工具

`flameshot`是`linux`环境下最接近`snipaste`，配合`picgo`，功能上和`win`环境没有任何区别，它也是支持贴图和标记的，还是很方便的。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202303082338301.png)

安装方式也很简单：
```sh
sudo apt install flameshot
```

之后设置一个快捷键即可：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202303082340419.png)

快捷键的命令如下：

```sh
flameshot gui
```
快捷键根据自己的习惯设置。
完成以上操作之后，如果你的截图软件无法调出贴图页面或者需要点击【share】菜单才能调出贴图菜单:

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202303082343781.png)

你可能还要改个系统设置:

```
 sudo gedit /etc/gdm3/custom.conf 
```

将其中的`WaylandEnable=false`的注释删掉，然后重启系统，之后`flameshot`就可以正常工作了

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202303082347271.png)

#### 创建图标
首先创建后缀为`.desktop`的文件，然后在其中加入如下内容：

```sh
[Desktop Entry]
Type=Application
Name=picGo
Exec=/home/syske/tools/picgo/PicGo-2.3.1.AppImage
Icon=/home/syske/tools/picgo/picgo.png
Categories=tools;picture;
Terminal=false

```

其中，`Type`表示图标类型，这个不要改，`Name`表示图标名字，`Exec`表示图标要执行的命令，`Icon`表示图标的`logo`，`Categories`表示图标分类，`Terminal`表示是否在终端中运行

之后保存文件，并将`*.desktop`文件复制到`/usr/share/applications/`目录下，这样在应用搜索的时候就可以搜到我们刚刚创建的图标：

```sh
sudo cp picgo.desktop /usr/share/applications/picgo.desktop
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202303082355236.png)


#### 扩展

现在有很多应用为了更好地支持`linux`系统，会提供`AppImage`格式的应用，正常情况下添加了运行权限之后，`AppImage`就可以通过`./*.AppImage`方式运行，如果有如下报错，则说明我们本地缺少`libfuse2`的依赖：

```
AppImages require FUSE to run.
You might still be able to extract the contents of this AppImage
if you run it with the --appimage-extract option.
See https://github.com/AppImage/AppImageKit/wiki/FUSE
for more information
```

这时候我们要手动安装`libfuse2`:


```sh
sudo apt install libfuse2
```


之后再次运行即可。



### 结语
