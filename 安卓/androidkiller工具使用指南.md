# androidkiller工具使用指南

### 下载安装
直接百度搜索，或者可以去`52pojie`去下载，具体可以参考这个；
[androidkiller使用指南](https://www.52pojie.cn/thread-726176-1-1.html)
这个软件本身是免安装的，所以直接解压就可以使用。
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221016095055.png)

### 配置
因为`androidkiller`集成了`apktool`、`adb`、`dex2jar`、`jd-gui`等工具，而除了`adb`其他工具都需要`java`开发环境，所以我们现要确保本地安装了`JDK`环境，关于`JDK`的安装和配置这里就不赘述了。
如果打开软件有如下提示，则表示你的`JDK`路径未设置或者设置路径不正确：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221016095743.png)
首先，点击`ok`进入软件之后，点击配置菜单，设置`JDK`路径即可
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221016095937.png)
这里需要注意的是，`JDK`环境配置争取的情况下版本信息才会显示，否则就是你的路径配置不正确。
另外一种配置`JDK`的方式是修改`config.ini`文件，找到其中的`javaSDK`配置项，值改为你的`JDK`路径即可
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221016100219.png)


### 逆向apk文件
#### 打开apk文件

打开 -> 选择`apk`文件 -> 打开
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221016100617.png)
然后回自动分析并逆向`apk`文件
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221016100758.png)
看到分析完成的提示，说明项目已经逆向完成，下面就可以开始进行`smail`文件的修改了
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221016101151.png)
左侧区域为项目信息展示区，工程信息主要展示项目入口和项目的权限信息，这块的内容是无法编辑的；工程管理是我们最核心的区域，这块会展示项目的源码，双击其中的文件，我们便可以对他进行编辑：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221016101522.png)

#### 编辑源码
这里我们主要说的是编辑`smail`原代码文件，为了我们能看懂源码，同时确保我们修改的不会报错，这块要先熟悉`smail`的语法，可以自己百度，随后我也会补充`smail`的一些常用语法

#### 编译文件
点击菜单栏的`android`选项，然后点击编译菜单，项目就会自动进行编译打包，并进行签名，生成`apk`文件，具体路径也会提示
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221016102015.png)

#### 调试
可以看到`Android`菜单下还有一些其他菜单，比如设备、安装、工具，这块的菜单，主要是针对`adb`的，也就是通过这几个菜单，可以直接安装、卸载和运行我们打包生成的`apk`文件到我们的设备上，当然前提条件是要先安装手机的驱动软件。
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221016102303.png)
驱动程序安装也挺繁琐的，为了图方便，我直接安装了`91`手机助手，然后插上手机，打开开发者模式，驱动会自动安装。

至此，`androidkiller`的基本使用，我们算是分享完了，剩余的菜单和功能，感兴趣的小伙伴可以自己去摸索下。