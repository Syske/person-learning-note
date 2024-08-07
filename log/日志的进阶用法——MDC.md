
### 前言

最近在优化现网消息服务的时候，突然想着给服务加上`TraceId`，这样在查系统日志的时候更方便。虽然日常处理工单的时候经常会根据`TraceId`查一些日志，但是对于`TraceId`的具体实施方案却是一知半解（而且有时候面试也会问道`tranceId`如何实现），于是本着学习了解的心态，搜了一些资料，然后顺藤摸瓜了解到`MDC`。

到这里不知道还有没有小伙伴没有听说过`TraceId`的，这里我们先做个小小的科普，`TraceId`其实就是某个线程执行链路的`id`，我们可以通过这个`Id`查到整个链路的执行日志，这里放出一张截图：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202407292208155.png)
在上面这张图中，`0a6906fd172226205190022801`就是当次请求的线程链路`id`，通过这个`id`，我们可以跟踪请求执行的所有日志，包括报错的日志。

有过`oncall`经历的小伙伴肯定清楚，经常会出现日志突然断掉，或者找不到的情况，但是如果对应服务或者接口有`traceId`，那简直不要太良心，只要日志打印了，我们肯定能找到问题原因。

但是如果没有`traceId`的时候，如果执行链路有报错，我们往往只能根据时间和线程号来确定可能的报错日志，这是因为通常我们会将报错日志和正常的日志输出到不同的文件中。
### MDC
#### 什么是MDC

`MDC`的英文全称是`Mapped Diagnostic Context`，翻译成中文是映射诊断上下文，它是`org.slf4j`提供的一个线程安全的存放诊断日志的容器。至于为何它是线程安全的，点开它的实现可以发现，它底层的数据存储是通过`ThreadLocal`实现的，说明它只在单个线程内有效，所以换句话说线程安全也没有毛病：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202407292233058.png)
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202407292230665.png)

所以`MDC`到底是什么呢？一句话：他就是个容器，存储诊断上下文用到的数据，比如`traceId`，机器信息等，然后它的使用范围是当前线程。

#### 如何使用MDC

上面说了`MDC`就是一个存储诊断信息的容器，所以我们日常使用的时候，就是把我们日志中用到的各种信息存到`MDC`，然后按照我们的需求体现在输出的日志上。

首先，我们需要引入`org.slf4j`的依赖:

```xml
<dependency>  
    <groupId>org.slf4j</groupId>  
    <artifactId>slf4j-api</artifactId>
    <version>1.7.25</version>
</dependency>
```



### 结语
