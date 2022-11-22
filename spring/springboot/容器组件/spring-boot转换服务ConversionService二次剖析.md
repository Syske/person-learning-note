# spring-boot转换服务ConversionService二次剖析

### 前言

今天我们来剖析下`conversionService`的初始过程，看下这个组件到底是如何初始化的，当然毕竟前天、昨天都剖析的差不多了，所以今天应该不会花太多时间。

好了，闲话少说，毕竟明天就放假了，所以今天要早点结束，然后开启假日模式。

### 初始化过程

`ConversionService`服务本身是属于`beanFactory`的一个属性，但它并没有跟随`beanFactory`初始化，根据下面的截图我们可以看出来，在容器初始化之后，`beanFactory`的`conversionService`依然是`null`。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210918083644.png)

直到在`prepareContext`方法调用了`postProcessApplicationContext`，我们`beanFactory`的`cpnversionService`才真正被初始化，关于这一块我们在剖析`spring boot`启动过程中以及分享过了，不过这一次我们是沿着`conversionService`的初始化的过程来看的，所以关于`conversionService`的相关内容会更加细致：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210918084454.png)

初始化之后`conversionService`被成功注入`134`个转换器，关于这一块的内容，我们前天也分享过了，最终我们通过配置类添加的转换器也会被加到`converters`中：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210918084756.png)

这里的`conversionService`来源于`ApplicationConversionService.getSharedInstance()`，所以接下来我们要看下`ApplicationConversionService`的初始化过程：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210918085713.png)

这里的`getSharedInstance`方法其实就是为了获取并返回`ApplicationConversionService`的`sharedInstance`属性，由于这个属性是静态的，所以它只会被初始化一次（也就是单例的）。

从上面的源码中我们可以看到，如果`sharedInstance`如果为空，则会为我们创建一个`ApplicationConversionService`赋值给`ApplicationConversionService`的`shareInstance`，并将实例结果返回。

由于`shareInstance`是静态的所以，全局只有一个，下一次在执行`getShareInstace`方法的时候，会直接返回，这里未来避免多线程并发导致数据被覆盖，所以对`ApplicationConversionService.class`加了锁，同时还进行了两次空判断，这也可以确保线程更安全，特别是锁内的判断。下面我们看下`ApplicationConversionService`的实例化操作：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/Snipaste_2021-09-18_13-44-35.jpg)

在`ApplicationConversionService`的构造方法中，先调用了`setEmbeddedValueResolver`设置了`StringValueResolver`，这个解析器的作用就是解析`string`类型的配置，方法内部就是简单的赋值；

然后调用了`config`方法，对当前转换服务进行配置，主要就是注册转换器和转换器工厂，包括`string`到`Duration`（`JDK1.8`引入的时长类）的转换

### 总结

好了，今天就先到这里了，我要修下键盘，前两天晚上吃饭的时候，不小心把馄饨汤倒进机械键盘了（浪费了我的高汤，键盘怕不是渴了），这两天键盘已经变成魔鬼输入法了，我今天要抽时间修理下，所以就先到这里吧，明天可以把我最近修理的小玩意都分享下。

最后，祝各位小伙伴中秋快乐呀！
