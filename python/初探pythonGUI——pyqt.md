# 初探Python GUI——pyqt

#python #qt

### 前言

从接触计算机以来，我一直对编写GUI程序有着一种难以言说的感情，从刚开始的易语言，后来用java，再后来了解到electron，虽然没有做出像样的gui软件，但我还是喜欢gui，也说不出来为什么，前几天，在一种机缘巧合之下，了解到pyqt，虽然很早就知道QT，Qt库是目前最强大的库之一，很多智能设备就是用qt开发的应用界面，用它可以开发出特别炫酷的交互界面，而且很多大型的3D软件就是用它开发的，由于对C++不是特别熟悉（其实就是没学过😂），所以也没有用过，但一直有一种在搞事的边缘试探，直到了解了pyqt，我突然觉得GUI又可以搞起来了。

### 简介

pyqt是QT基于python平台的一种解决方案，python大家应该都了解，特点是构建应用比较快速，开发效率高。百度百科给出的解释是：

> PyQt是一个创建GUI应用程序的工具包。它是[Python](https://baike.baidu.com/item/Python)编程语言和[Qt](https://baike.baidu.com/item/Qt)库的成功融合。Qt库是目前最强大的库之一。PyQt是由Phil Thompson 开发。
>
> **PyQt**实现了一个Python模块集。它有超过300类，将近6000个函数和方法。它是一个多平台的工具包，可以运行在所有主要操作系统上，包括UNIX，Windows和Mac。 **PyQt**采用双许可证，开发人员可以选择GPL和商业许可。在此之前，GPL的版本只能用在Unix上，从**PyQt**的版本4开始，GPL许可证可用于所有支持的平台。

### 优势

pyqt也有很多优势，首先它有基于GPL许可证的开源版本，从**PyQt**的版本4开始，GPL许可证可用于所有支持的平台；另一个优势是，由于基于python，入门相对简单，而且再加上pyqt提供了图形化的设计界面，我们可以在设计器设计好界面，然后转换成python代码，简直不要太爽。

### 环境搭建

#### 安装python

先去python官网下载最新安装包，这里我选择的是安装包，当然你也可以选择压缩版，下载完直接解压也行。区别就是压缩版需要手动配置环境变量。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200530091628.png)

#### 配置环境变量

这是我本地的安装目录和环境变量配置，一般安装版会自动设置，如果没有，可以参照设置

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200530092121.png)

配置完后，需要测试下看我们的环境变量设置是否正确，在任意目录打开cmd命令窗口，输入如下命令：

```sh
python --version
```

如果显示类似如下，那基本上你的环境就ok了：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200530092530.png)

#### 安装pip

pip就是个包管理工具，我们可以通过它管理我们的python模块，安装很简单，我们选择在线安装，在cmd命令窗口中执行如下命令：

```sh
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```

这行命令的作用就是下载pip，由于网络原因，下载可能比较慢，耐心等待就好，如果网络问题下载失败，多试几次，如果还不行，可以通过下面的网址去官网下载：

```html
https://pypi.org/project/pip/
```

下载完成后，我们通过如下命令进行安装：

```sh
python get-pip.py
```

没有错误提示，基本上都可以安装成功，然后我们测试下看是否安装成功：

```sh
pip --version
```

如果如下结果，那安装就ok了

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/image-20200530093301683.png)

#### 更改pip源

因为pip官方源国内访问比较慢，安装组件超级慢，经常出现失败情况，所以我们要配置国内的镜像源。目前国内的镜像站如下：

```
（1）阿里云 http://mirrors.aliyun.com/pypi/simple/
（2）豆瓣http://pypi.douban.com/simple/
（3）清华大学 https://pypi.tuna.tsinghua.edu.cn/simple/
（4）中国科学技术大学 http://pypi.mirrors.ustc.edu.cn/simple/
（5）华中科技大学http://pypi.hustunique.com/
```

首先进入当前用户的用户目录，一般就是，c盘Users下找到你用户名对应的文件夹，比如`C:\Users\test\`，然后创建一个名为`pip`的文件夹，在文件夹下创建`pip.ini`文件，windows下要记得先让自己的文件拓展名可见，最后再添加如下内容：

```ini
[global]

index-url = http://pypi.douban.com/simple

[install]

trusted-host=pypi.douban.com
```

这里我用的是豆瓣的，你也可以改成阿里的镜像地址

#### 安装pyqt5

通过如下命令安装pyqt5，你会发现替换了源之后的pip，下载速度特别给力：

```sh
pip install pyqt5
```

紧接着，我们安装pyqt5的组件，里面包含设计器

```
pip install pyqt5-tools
```

这里我推荐上面这种安装方式，不存在兼容性问题，如果通过离线安装的方式，很可能不兼容。

#### 测试pyqt5

我们先创建个小脚本试一下：

```python
from PyQt5 import QtWidgets, QtGui
import sys

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget();
window.show()
sys.exit(app.exec_())
```

运行上面的脚本，如果有如下窗口弹出，那么恭喜你，pyqt5环境已经就位

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200530100703.png)

下来，我们用pycharm来创建项目，做一些简单配置

### 创建项目

打开pycharm，首先要简单配置下pyqt，然后创建我们的项目。

#### 配置pyqt5

首先打开工具，在`External Tools`中增加pyqt的两个工具，一个是`qtDesigner`，也就是我们说的设计器，另一个就是把qt的ui转成py脚本的。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200530101507.png)

我们先看`qtDesginer`：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200530102025.png)

参照图片配置即可，需要注意的是pyqt5设计器的路径，很多博客说的是`python`安装目录下的`Lib\site-packages\pyqt5_tools\Qt\bin`，但我在实际使用的时候发现并不是，当然更多的原因可能是版本不一样，我这里是`pyqt5`，上面的配置信息如下：

```
Program：     D:\software\python\python38\Scripts\pyqt5designer.exe
Working directory:		$ProjectFileDir$
```

再下来就是ui转py脚本的工具配置：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200530102813.png)

这里的`program`配置的是`python.exe`，也就是在你的`python`安装目录`bin`下，其他参数如下：

```
Argument：    -m PyQt5.uic.pyuic $FileName$ -o $FileNameWithoutExtension$.py
Working directory:	    $FileDir$
```

#### 创建项目

上面这些配置完成，就可以开始我们的项目了。首先创建一个项目，填写项目相关信息

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200530101149.png)

这里需要注意的是，要勾选上图两项，保证pyqt的包可以正常导入

#### 设计ui

项目右键，选择External Tools下我们刚刚配置的共，打开设计器

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200530103401.png)

然后我们的设计器就启动了，它是这个样子的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200530103557.png)

左侧侧是组件区，包括常用的各类组件，中间是设计核心区，右侧就是属性显示，我们先创建个主窗口，然后什么都不做，然后输入文件名保存。

#### ui转为py

如果配置没有问题，我们的ui文件默认是在我们项目根目录的，我们直接选中要转换的ui，右键选择我们配置好的转换工具。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/image-20200530104606791.png)

不出意外，我们会发现项目根目录多了一个和UI同名的`py`文件，但是这个文件并不能直接执行，我们先看下文件内部吧:

```PYTHON
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(290, 140, 121, 51))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "确定"))
```

然后我们创建一个新的脚本，来启动这个窗口：

```python
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

import mainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = mainWindow.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
```

如果你的窗口类名和我的不一致，把上面的脚本改成和你的对应的，然后双击运行，一个新的窗口出来了：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200530105225.png)

因为我这里的示例加了一个按钮，所以他可能和你的不一样，不过没关系，能正常运行就好。

到这里，我们本次的内容就结束了，我们在这里总结下。

### 总结

今天我们主要探讨了如何使用pyqt开发一个gui应用，我们从python安装，环境变量配置，到pyqt5的安装、配置，以及pycharm集成pyqt5，详细演示了一个pyqt GUI应用的设计开发过程，虽然代码不太多，有用的内容也没多少，但还是希望有帮到你，哪怕是给了你学习python的动力，或者让你发现了编程的乐趣，那也是值得的。当然，对我来说，能够将我所了解和知道的和你分享，解决你的问题，这就很有趣……