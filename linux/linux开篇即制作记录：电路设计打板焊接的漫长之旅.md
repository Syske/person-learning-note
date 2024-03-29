
## 打板焊接

距离上次`linux`卡片机项目的分享，已经过去一年半，之所以这么长时间没有更新，主要还是因为项目没有实质的进展，虽然打板`6`次，`PCB`改了又改，但是整个链路一直没跑通，所以也就是继续更新，当然也是因为我一贯的原则是，凡是分享的原创性内容，一定要尽可能是自己验证过的。

然而，幸运的是，最近一周内，所有问题都被完美解决，板子成功驱动、`u-boot`编译运行成功、`linux`成功运行，所以我又开始更新了，先给大家看看成功点亮的图片：

- uboot成功驱动
  
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230819124737.png)

- linux成功运行
  
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230823234434.png)

- 板子正面

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230825201711.png)

- 板子反面

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230825201743.png)

今天我们先来分享下我的打板和绘图血泪史，打了`6`次，焊了`N`次，熬了`N`次夜……不过还是值得的，下面这张图片就是六次的打板记录，从上到下，依次是第一一版到第六版，第六版虽然还有一些问题，但是跳线和短接之后已经可以正常运行了

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230825203727.png)

### 第一版

刚开始甚至连封装为何物都不知道，画板子的时候，各种封装都涉及到了，包括`0805`、`0603`、`0402`，甚至画了`01005`和`0201`封装的，所以第一张板子基本上没法焊接，当然这也是为啥我现在手里的板子封装还是乱七八糟的，毕竟买的元器件不能浪费了

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824200958.png)

### 第二版 && 第三版

重新画图打板，第二次焊接之后发现芯片引脚错位了，一直短路，然后就有了第三版。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824200343.png)

第二版到第三版还有个改动，就是将串口的`LED`拿掉的，我这里其实是参考其他大佬的原理图，他连接的是发光二极管，说应该连接二极管，然后我画的是`1N4148`开关二极管，先不说合理不合理，反正瞎画肯定不合适，这里也给抄电路的小伙伴提个醒，一定要先搞清楚原理，再抄，不然真的自己坑自己。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824213013.png)

### 第三版

第三版由于`sd`卡槽不匹配，然后重新打板，毕竟嘉立创的板子可以白嫖:

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824201752.png)

### 第四版 && 第五版

第四版芯片正常驱动，但是串口插上，按`reset`开关，直接断开，经过比对，发现串口连接错了，我这里用的是`CH340E`，`RXD`和`TXD`应该分别对应`F1C200S`芯片的`DTX`和`DRX`，也就是读对应芯片的发，发对应芯片的读，结果之前不知道，画错了，然后导致了这个乌龙，之后第五版应运而生：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824202653.png)
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824202250.png)

### 第五版 && 第六版

第五版到第六版基本上没有改动，只是因为串口一直没有生效，参考了其他人的原理图，然后在`reset`引脚上增加了一个滤波电容，容值`1uf`：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824204546.png)

同时还增加了一些电压测试点位：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824204833.png)

然而，就在我觉得一切都要结束了，我终于要点亮这个小板板的时候，上天又一次给我开了个玩笑🤪，串口依然不行，甚至芯片都读不出来了。

真的心态都崩了，反正那之后的很长时间（最后一版打板时间是`4-21`），我基本上都放弃了。然后在这些捣鼓不下来的空挡，我搞新的项目，虽然都是小项目，但是我觉得还是很有意思的，项目的简介我放在后面了，感兴趣的小伙伴可以去瞅瞅。

### 柳暗花明又一村

直到最近，一天晚上睡不着，也没啥事，于是我又开始查阅`F1C200S`相关的内容，然后经过比对，我发现了华点——别人的串口基本上都没有电阻，而我抄的串口为啥还有电阻，然后我去看了我之前参考的原理图，发现人家的电阻单位是`470`，没有单位，而我抄的时候误以为是`470K`，所以买的时候也是按这个买的，焊接的时候也是用的这个阻值，因为恰好电路那里用到了`470K`的电阻。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230825204120.png)

串口的问题算是解决了，但是为什么我的芯片为啥还是不能工作，我打算重新焊一块板子，结果我在对着这块板子焊新板子的时候，发现有一个点电阻和电容搞错了，应该焊接电阻的地方，放的是电容，应该焊电阻的地方放的是电容~

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230825204224.png)

好家伙，原来问题处在这里了，于是调换了原来板子的电阻和电容，芯片可以识别了，插上之前烧录的`sd`卡，连接串口，成功显示信息，我擦，幸福来得有点突然，困惑了小半年的问题解决了，简直不要太爽~

### 结语

从一个只有高中电路知识的纯小白（当然主要是一直喜欢这些，但是日常主要还是搞维修，纯玩），到学习电路原理图、`PCB`的绘制，到后面自己踩坑了解封装知识，再到后面搜集元器件的手册和文档，亲自动手画板子，慢慢可以看懂大佬的原理图，能看懂简单的数据手册，到现在这个板子的设计、打板、焊接、编译、烧录，虽然现在依然还是小白，但我也慢慢能找到自己的方向，至少在这条自己热爱的路上，我越走越顺，也越走越自信……

### 其他项目

#### usb2.0扩展坞

搞了一个`USB`的扩展板，很迷你，已经正常打板了，感兴趣的小伙伴可以去看看：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824210756.png)

这里是项目地址

```
https://oshwhub.com/syske/usb-ext
```

#### 触摸台灯

搞了个触摸台灯的板子

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824211117.png)

这个项目也打板验证了，目前我的床头台灯就是这个板子，灯泡、底座是买的，罩子和骨架是家里拆的吊灯，这是实物：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824211850.png)

#### F1C200S板子2.0

画了`F1C200S`新的`V2`版本：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230824212229.png)

还专门绘制了`3D`外壳，已经按照我现在最新点亮的原理图做了调整，元器件的封装尺寸也调整统一了，除了极个别元件，电阻和电容都是`0603`封装，颜值一下提升了不少。
