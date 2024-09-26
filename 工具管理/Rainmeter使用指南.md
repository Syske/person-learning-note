### Rainmeter

想要用起来这个软件，首先要学一些基本的语法，下面我们讲解一些简单的语法，如果只是简单修改和使用的话，肯定是够了，感兴趣的小伙伴可以看下官方文档：

https://docs.rainmeter.net/

中文版的文档网上也很方便，我这里放出之前自己搜集的文档：
链接: https://pan.baidu.com/s/1ftoOCJUPOa-w3jE4kDQ0Iw?pwd=krwb 提取码: krwb 

#### 基本语法

先看一张图：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/fe83c564-b5be-473a-97bd-8ba6fa8906d7.jpg)
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/9351511e-ea7f-4ae0-8d97-1154bfaea008.jpg)
在上面图片中：
- `[]` 扩起来的表示节点，节点包括两类，一类是默认节点，有具体含义的，包括`Rainmeter`、`Metadata`、`Variables`等，节点名称必须唯一，否则节点不会生效
- `;`开头的表示注释语法，有编程基础的小伙伴应该不陌生
- 自定义节点下的`Meter=String`表示我们当前节点展示的是文字内容，其中的`Text`表示我们展示的文字内容，`FontColor`表示字体颜色，`MeterStyle`就是字体等样式，`X/Y/W/H`分别表示屏幕展示坐标和宽高，`FontSize`表示字体大小，`LeftMouseUpAction`表示鼠标左键触发的操作
- `X`和`Y`可以是相对尺寸，比如`5R`就表示相对上一个节点，在`Y`方向下移`5`个像素，`X`如果加`R`也是一样的意思（坐标的原点是屏幕的左上角）
- 如果`LeftMouseUpAction`指定的是本地的文件夹地址，点击之后就是打开对应的路径，如果填写的是软件的地址（`.EXE`结尾），则点击之后就是打开对应的软件，如果填写的是网络链接，则是用默认浏览器打开对应的地址，如果想通过指定浏览器打开对应的地址，则可以这样写：![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/c610c0a0-cd3e-41b6-b392-6f99381f8aa4.jpg)

下面我分享出自己的皮肤，想要使用的小伙伴，可以直接复制皮肤内容，编辑替换自己本地的`welcome.ini`即可，记得修改成自己的`url`:

```parperties
; Lines starting ; (semicolons) are commented out.
; That is, they do not affect the code and are here for demonstration purposes only.
; ----------------------------------

[Rainmeter]
; This section contains general settings that can be used to change how Rainmeter behaves.
Update=1000

[Metadata]
; Contains basic information of the skin.
Name=Welcome
Author=poiru
Information=The welcome skin for illustro.
License=Creative Commons BY-NC-SA 3.0
Version=1.0.0

[Variables]
; Variables declared here can be used later on between two # characters (e.g. #MyVariable#).
fontName=Trebuchet MS
textSize=9
colorBar=235,170,0,255
colorText=255,255,255,205


; ----------------------------------
; STYLES are used to "centralize" options
; ----------------------------------

[styleTitle]
StringAlign=Left
StringCase=Upper
StringStyle=Bold
StringEffect=Shadow
FontEffectColor=0,0,0,50
FontColor=#colorText#
FontFace=#fontName#
FontSize=10
AntiAlias=1
ClipString=1

[styleLeftText]
StringAlign=Left
; Meters using styleLeftText will be left-aligned.
StringCase=None
StringStyle=Bold
StringEffect=Shadow
FontEffectColor=0,0,0,20
FontColor=#colorText#
FontFace=#fontName#
FontSize=#textSize#
AntiAlias=1
ClipString=1

[styleSeperator]
SolidColor=255,255,255,15

; ----------------------------------
; METERS display images, text, bars, etc.
; ----------------------------------

[meterBackground]
Meter=Image
ImageName=Background.png
X=0
Y=0

[meterMidLine]
Meter=Image
SolidColor=255,255,255,80
W=1
H=200
X=245
Y=60

[meterTitle]
Meter=String
MeterStyle=styleTitle
; Using MeterStyle=styleTitle will basically "copy" the
; contents of the [styleTitle] section here during runtime.
X=20
Y=18
W=80
H=18
FontSize=11
Text=工作空间

[meterIllustroTitle]
Meter=String
MeterStyle=styleLeftText
X=20
Y=55
W=100
H=30
FontColor=255,217,120,255
FontSize=10
Text=本地常用链接


[meterLeftLink1]
Meter=String
MeterStyle=styleLeftText
X=20
Y=95
;W=60
H=14
FontColor=255,255,255,255
Text=项目源码
LeftMouseUpAction=["D:\workspace\project-resouce"]

[meterLeftLink2]
Meter=String
MeterStyle=styleLeftText
X=20
Y=5R
;W=50
H=14
FontColor=255,255,255,255
Text=个人笔记
LeftMouseUpAction=["D:\workspace\learning\person-learning-note"]

[meterLeftLink3]
Meter=String
MeterStyle=styleLeftText
X=20
Y=5R
;W=50
H=14
FontColor=255,255,255,255
Text= 工具
LeftMouseUpAction=["D:\tools"]

[meterLeftLink4]
Meter=String
MeterStyle=styleLeftText
X=20
Y=5R
;W=50
H=14
FontColor=255,255,255,255
Text= Learning
LeftMouseUpAction=["D:\workspace\learning"]

[meterLeftLink5]
Meter=String
MeterStyle=styleLeftText
X=20
Y=5R
;W=50
H=14
FontColor=255,255,255,255
Text= jd-gui
LeftMouseUpAction=["D:\tools\jd-gui-windows-1.6.6\jd-gui.exe"]


[meterLinksTitle]
Meter=String
MeterStyle=styleLeftText
X=260
Y=55
;W=50
H=30
FontColor=255,217,120,255
FontSize=10
Text=工作常用链接

;[meterLinksLine]
;Meter=String
;MeterStyle=styleLeftText
;X=260
;Y=95
;W=225
;H=80
;FontColor=#colorText#
;FontSize=9
;Text=There are literally thousands of skins available for Rainmeter. There are several good sites where you can download them. 


[meterRightLink_1_1]
Meter=String
MeterStyle=styleLeftText
X=260
Y=95
;W=50
H=14
FontColor=255,255,255,255
Text=codeUp
LeftMouseUpAction=["https://codeup.aliyun.com/"]

[meterRightLink_1_2]
Meter=String
MeterStyle=styleLeftText
X=260
Y=5R
W=50
H=14
FontColor=255,255,255,255
Text= 替换自己的地址
LeftMouseUpAction=["https://www.baidu.com/“]


[meterRightLink_2_1]
Meter=String
MeterStyle=styleLeftText
X= 340
Y= 95
;W=50
H=14
FontColor=255,255,255,255
Text= 替换自己的地址
LeftMouseUpAction=["https://www.baidu.com/"]

[meterRightLink_2_2]
Meter=String
MeterStyle=styleLeftText
X=340
Y=5R
W=50
H=14
FontColor=255,255,255,255
Text= 替换自己的地址
LeftMouseUpAction=["https://www.baidu.com/"]

[meterRightLink_2_3]
Meter=String
MeterStyle=styleLeftText
X=340
Y=5R
W=50
H=14
FontColor=255,255,255,255
Text= 替换自己的地址
LeftMouseUpAction=["C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" https://www.baidu.com/]

[meterRightLink_2_4]
Meter=String
MeterStyle=styleLeftText
X=340
Y=5R
W=50
H=14
FontColor=255,255,255,255
Text= 替换自己的地址
LeftMouseUpAction=["https://www.baidu.com/"]

[meterRightLink_2_5]
Meter=String
MeterStyle=styleLeftText
X=340
Y=5R
W=50
H=14
FontColor=255,255,255,255
Text= harbor
LeftMouseUpAction=["https://www.baidu.com/"]

[meterRightLink_2_6]
Meter=String
MeterStyle=styleLeftText
X=340
Y=5R
W=50
H=14
FontColor=255,255,255,255
Text= 替换自己的地址
LeftMouseUpAction=["https://www.baidu.com/"]
```

#### 修改皮肤

操作路径如下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/b7baebde-afb5-4018-81db-93f7f00f564e.jpg)

保险起见，最好在修改之前备份下，之后点击皮肤刷新下修改效果就会呈现：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/c79c003d-8eec-4246-9614-0326718931ae.jpg)



#### 资源分享

如果前期只想玩和了解，可以先去看下别人制作的皮肤：
- 贴吧：`rainmeter吧`
- 社区：https://bbs.rainmeter.cn/
- 官网：http://rainmeter.net/

以上就是`Rainmeter`的基本用法，感兴趣的小伙伴可以自己动手了。