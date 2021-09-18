# spring-boot转换服务ConversionService二次剖析

### 前言



### 初始化过程

`ConversionService`服务本身是属于`beanFactory`的一个属性，但它并没有跟随`beanFactory`初始化，根据下面的截图我们可以看出来，在容器初始化之后，`beanFactory`的`conversionService`依然是`null`。

![](https://gitee.com/sysker/picBed/raw/master/blog/20210918083644.png)

直到在`prepareContext`方法调用了`postProcessApplicationContext`，我们`beanFactory`的`cpnversionService`才真正被初始化，关于这一块我们在剖析`spring boot`启动过程中以及分享过了，不过这一次我们是沿着`conversionService`的初始化的过程来看的，所以关于`conversionService`的相关内容会更加细致：

![](https://gitee.com/sysker/picBed/raw/master/blog/20210918084454.png)

初始化之后`conversionService`被成功注入`134`个转换器，关于这一块的内容，我们前天也分享过了，最终我们通过配置类添加的转换器也会被加到`converters`中：

![](https://gitee.com/sysker/picBed/raw/master/blog/20210918084756.png)

这里的`conversionService`来源于`ApplicationConversionService.getSharedInstance()`，所以接下来我们要看下`ApplicationConversionService`的初始化过程：

![](https://gitee.com/sysker/picBed/raw/master/blog/20210918085713.png)

这里的`getSharedInstance`方法其实就是为了获取并返回`ApplicationConversionService`的`sharedInstance`属性，由于这个属性是静态的，所以它只会被初始化一次（也就是单例的）

### 总结

