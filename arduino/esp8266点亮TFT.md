# esp8266制作太空人天气时钟

### 背景

简单来说，就是最近太闲了，然后下班也无所事事，在B站上刷着一众`up`们的`diy`视频，一次又一次地激起了我应该做点啥的想法，于是在这一阵又一阵的激励下，我再次燃起了对`diy`硬件的兴趣，于是我便又一次把自己年前买到的一些硬件翻出来，开始自己的新一轮`arduino`之旅。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/S30307-20522323.png)

### 材料准备

本次项目的总成本不到`30RMB`，`esp8266`开发板的成本`13RMB`，`1.3`寸`IPS`屏幕成本`15RMB`

- `esp8266`开发板
- 杜邦线`6`条
- `1.3`寸`TFT`屏幕一个（`ST7789`）


### 准备工作

#### 接线

接线对应关系如下：

TFT | esp8266 | 备注
---|---|---
GND | G  |
VCC | 3V |
SCL | D5 |
SDA | D7 |
RES | D4 |
DC  | D3 |

视频发出来之后，有好多小伙伴在问如何接线，这里我放出一张实物的接线示意图，各位小伙伴直接对照图片进行连接即可：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230307211304.png)

#### 依赖库

安装`TFT_eSPI`库，这里算是`arduino`的最基本操作了，我们就不展开了。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230228230533.png)

如果对`esp8266`的开发环境还有疑问的小伙伴可以看下我之前发出来了的相关内容：

<https://zhuanlan.zhihu.com/p/589448075>


### 运行测试用例

这里运行测试用例的意义是为了验证我们的接线和环境配置是否正常

#### 修改配置

运行测试用例前，我们要先修改`Arduino\libraries\TFT_eSPI`下的`User_Setup.h`文件，修改这个文件的作用是配置屏幕的相关数据，确保代码可以驱动我们的屏幕，主要包括屏幕驱动版本、分辨率和屏幕引脚定义，具体修改的点如下：

- 驱动文件设置：这里根据`TFT`屏幕的驱动版本选择
  
![驱动](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230228230850.png)

- 屏幕分辨率：这里也是根据屏幕参数选择

![分辨率](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230228231357.png)

- 引脚设置：这里只需要设置`dc`和`rst`引脚即可，要和接线部分的引脚相对应

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230228231504.png)

其余配置项保持默认即可。

#### 运行测试用例

选择一个示例，这里我们选择`Colour_test`

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230228231903.png)

然后选择串口和开发板，上传即可。如果接线和代码都没有问题，那么屏幕会显示如下图像：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230307213217.png)

至此，我们的准备工作告一段落，下面开始我们的代码编写。

### 开始撸代码

本项目是基于esp8266和IPS彩屏的一个桌面天气时钟，项目代码基于嘉立创开源平台的《ESP8266太空人天气时钟》源码，优化了其中HTTPClient的报错，代码本身未作大的调整，项目地址如下：

<https://oshwhub.com/nanxiangxiao/tai-kong-ren-shi-zhong_copy>

本次项目演示的代码仓库如下:
<https://github.com/Syske/esp8266-click-weather-ips>

下面我们简单介绍下代码的修改点，确保各位小伙伴看了之后就可以直接点亮。这里我们要修改的文件只有一个——`click-weather.ino`，由于代码本身内容过多，这里我们只贴出需要修改的部分：

#### wifi相关信息

这里把`wifi`改成你自己的，之后直接上传代码即可。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230307214008.png)


#### 关于城市编码

在实际测试过程中，发现`ip`识别城市会有异常的情况，这时候我们可以通过配置城市编码的方式来解决，当然也需要将根据`ip`获取城市编码的相关代码注释掉

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230307230040.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230307225952.png)

城市的编码信息可以从下面这个地址中搜索：
<https://gitee.com/sysker/LocationList/blob/master/China-City-List-latest.csv>

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230307230133.png)

至此，我们本次的项目基本上就结束了。


#### 其他修改点

如果只是想复刻项目的小伙伴，以下内容可以不关注，这里说的是我在原代码基础上的优化点。其实这里的优化点和没有优化一样，因为这里所谓的优化点应该是由于`httpClient`版本问题，优化的原因是原代码在编译过程中报错了，然后我根据错误提示做了简单的调整：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230307215556.png)

错误的意思是`HTTPClient`的`begin(URL)`过期了，推荐我们使用`begin(WiFiClient, url)`，所以我的优化点就是改成了新方法：

- 首先实例化一个`WiFiClient`

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230307220011.png)

- 然后替换所有调用`begin`方法的地方，之后成功编译代码

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230307220454.png)


### 简单总结

本次项目的难点有两个，第一个是`esp8266`点亮屏幕部分的配置和接线，这一块如果顺利，本次项目基本上就算完成了`70%`；第二个就是项目源码的修改和上传，这块要求对`arduino`和`C++`的基础知识，但是参照本教程也可以顺利完成。好了，关于这个项目，我们就先说这么多，有疑问的小伙伴可以留言，我们一起探讨交流。