# spring-boot启动过程源码分析内容补充

### 前言

昨天我们从源码层面简单分析了一下`spring boot`的启动过程，由于时间仓促，加上内容都是临场发挥，因此整个过程还是有点混乱的，而且内容是也有一点点的谬误，为了让昨天的内容看起来不那么混乱，同时也为了纠正昨天的谬误，我们今天先来做一点点补充，这样也有利于我梳理后续内容的思路。下面就让我们直接开始吧。

### run方法源码分析补充

昨天晚上我说过今天要先画一个时序图，所以开始之前，我们先看下`run`方法的执行过程时序图：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/run方法运行时序图.svg)

从上面这张时序图中，我们很直观地看出`run`方法的执行过程。其中最关键的内容有两部分，一个是和监听器相关的操作，另一个是和应用容器相关的操作，从图上我们也可以看出这一点，这两个的内容和操作都很多，而且基本上贯穿了整个`run`方法，所以下一步我们要分析的就是监听器和应用容器这两块的内容，但是今天可能来不及分享了。

#### 纠正谬误

下面我们纠正昨天的一个谬误，昨天我说这段代码是创建`spring`工厂实例，这么说虽然没有什么问题，但结合整段代码的逻辑来说就是有问题的。

```java
exceptionReporters = getSpringFactoriesInstances(SpringBootExceptionReporter.class,
					new Class[] { ConfigurableApplicationContext.class }, context);
```

这段代码在这里的作用是构建`SpringBootExceptionReporter`的实例对象，构建的对象是在`catch`中用的，详细查看源代码的话，你会发现其实它是用来分析启动过程中错误的。下面的这段代码，各位小伙伴看着肯定不陌生，在启动`spring boot`报错的时候会经常看到：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210831140824.png)

说到这里，我们再补充点`spring boot`启动异常处理的相关知识点。如果在启动过程中发生异常，`spring boot`会调用`handleRunFailure`方法处理异常，其中一个核心参数就是我们前面创建的`SpringBootExceptionReporter`实例集合，在方法内部主要进行了以下几步操作：

- 处理退出码。这个退出码是从异常中获取到的，获取到之后会注册到`SpringBootExceptionHandler`中。
- 调用监听器`failed`方法，推送`ApplicationFailedEvent`事件
- 调用`reportFailure`，打印错误报告
- 关闭`context`容器
- 抛出异常信息

方法源码如下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210831143149.png)

好了，`spring boot`启动主流程暂时就先分享这么多。

### 总结

经过今天的梳理之后，我发现对于`spring boot`的启动流程，整体感觉清晰了好多，特别是时序图画完之后。

而且更重要的是，从图上我们直接就能很直观地看出整个启动流程，看清楚启动过程的各个节点以及相关的操作，这就特别有助于我们理解`spring boot`的启动过程，另外从时序图上，我们还可以直观地看出启动过程的关键点、核心点，这样也有助于我们把握知识的重点，确定下一步地学习计划。

总之，我现在感觉画图确实是一个特别好的学习方式，比如画脑图、画时序图、流程图等，这些图表对于知识地梳理和总结都有着特别积极的地效果，我是越来越喜欢这种方式了。

