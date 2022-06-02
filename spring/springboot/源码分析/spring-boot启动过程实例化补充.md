# spring-boot启动过程实例化补充



### 前言

上一次我们在分析`spring boot`启动过程实例化方式的时候，关于工厂方法没有做过多说明，一方面是我确实当时不太清楚，另一方面在`spring boot`的启动流程中，我们并没有找到相关代码，所以最后就一笔带过了。

由于最近这两天把`spring boot`之前提出的示例`demo`已经分享完了，最近也正苦于没有学习目标，因此呢，今天我们就来详细看下`spring boot`的工厂实例化方式。

我们今天不在从启动流程入手，我们换个思路，直接从`@Bean`注解入手，看下`@Bean`注解的方法到底是如何被处理的，以及它是何时被处理的。

### @Bean注解

首先我搜索了全局有用到`Bean.class`的地方，找到以下结果：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210923132356.png)

总共找到`10`条记录，其中前两条和我们昨天分享的条件配置有关，主要是判断方法是否存在`@Bean`注解，但是这里并不进行实例化操作，所以我们这里就不深入研究了；

第三行、第四行是获取所有包含`@Bean`注解的方法的元数据，但是由于这个类是和异常报告相关的（`NoSuchBeanDefinitionFailureAnalyzer`，从名字可以看出来是个失败分析器，找不到`bean`的定义信息时触发），所以我们也不做过多说明。不过从调用的方法名来看，这个方法的作用是获取所有的`beanMethod`：
![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210923134626.png)

第五行是判断某个方法是否包含`@Bean`注解：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210923205411.png)

第六行是获取注解的属性，并从属性中拿到`name`属性，这个属性最后会变成我们的`beanName`

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210923212240.png)

第七行是从方法的元数据中获取`@Bean`注解的属性信息，然后将这些属性信息赋值给`bean`的定义信息。这个方法很长，信息量也很多，不仅包括了工厂方法的设置，还包括`autowire`、`initMethod`、`destroyMethod`等信息的配置。

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/Snipaste_2021-09-23_22-07-37.jpg)

然后沿着这个方法我最后进入了`refresh`方法中，也就是说其实在`refresh`方法中会调用我们上面这个方法，下面是它的调用流程：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/Snipaste_2021-09-23_22-27-10.jpg)

看着这个方法，看着有点眼熟，但是感觉我上次好像没有讲到，然后我又回去翻了下上次源码分享的内容，最终确认这块的内容当时确实没有讲到，当时并没有将这么细。

总体来说，这块的核心代码就是处理`bean`的定义信息，处理完成后，通过`@Bean`注解配置的`bean`的定义信息就会被注册到容器中，然后会在后期实例化的时候，调用`bean`的工厂方法进行实例化，这种方式就是我们当时没有展开讲的工厂实例方式，这种方式在`spring boot`中也是广泛存在的，当然关于这一点我也是今天才知道的。

#### 测试

下面我们通过一个`@Bean`配置实例来看下。首先是我们通过`@Bean`注解配置的一个过滤器：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210923084430.png)

然后在一个偶然情况下，我找到了通过工厂方法实例化的方式（我到现在都不知道当时咋发现的，这就是机缘吧），这正是这一发现，我们才有今天的内容，总之就是很偶然。

这是位于`SimpleInstantiationStrategy`的一个实例化方法，从名字可以看出来，这个类是一种实例化策略，方法的作用就是根据工厂方法实例化对象，从`debug`截图可以看出来，这里的`factoryMethod`就是我们加了`@Bean`注解的方法名，`beanName`默认就是我们的方法名：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210923084335.png)

关于这个方法的调用流程，我们后面有机会再讲，今天确实有点太晚了，我们目前只需要搞清楚工厂方法的基本实例化方式就可以了。

### 总结

今天我们主要围绕着`@Bean`注解，分析了工厂方法实例化`bean`的方式和基本流程。

从内容上来讲，其核心就是`BeanFactory`相关的`bean`定义信息的设置和赋值，然后就是工厂实例化方式的演示。由于时间的问题，还有一些内容没有分析到，但是目前的内容已经可以让我们比较全面地看到`@Bean`注解的实例化方式，虽然有一定成都额运气成分，不过这也算是意外的收获吧。

好了，今天的内容就先到这里吧，各位小伙伴，晚安吧！

