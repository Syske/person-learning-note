# spring-boot源码分析之BeanFactory · 陆

### 前言

从今天开始，我们要啃硬骨头了——`refreshContext`

### refreshContext

`refreshContext`就做了两件事，一个是注册容器关闭钩子函数，另外一个就是刷新容器。关闭钩子函数可以让我们更优雅地关闭`spring boot`容器，这一块后期也专门分享一次；刷新容器方法最终会调用容器的刷新方法，关于这个方法，我们之前已经分享过了，她就是刷新容器中的持久化资源，这里的资源包括`xml`、`java`配置、注解、配置文件、数据库等。

![](https://gitee.com/sysker/picBed/raw/master/20210909081203.png)

下面，我们就来详细看下它的内部实现。我们先看下它的调用流程：

![](https://gitee.com/sysker/picBed/raw/master/20210909082926.png)

从上面图中我们可以看出来，最终其实调用的是`AbstractApplicationContext`的`refresh`方法，这个方法内部比较长，总共调用了`15`个方法，下面我们就逐一剖析这些方法。

![](https://gitee.com/sysker/picBed/raw/master/refresh.png)

#### prepareRefresh

这个方法的作用就是为后面的刷新操作做准备，内部实现如下：

![](https://gitee.com/sysker/picBed/raw/master/prepareRefresh.png)

首先设置`spring boot`的启动时间，获取的是当前时间，然后分别设置`closed`和`active`为`flase`和`true`，这两个属性都是原子类`AtomicBoolean`。

接着会根据日志设置等级输出日志，不过这里必须是`begug`级别才会输出，如果是`trace`等级的，则会输出更详细的日志信息。

##### initPropertySources

再下来就是`property`资源的初始化。由于 `AbstractApplicationContext`的`initPropertySources` 方法是空实现，而且`AnnotationConfigServletWebServerApplicationContext`并没有重写该方法：

![](https://gitee.com/sysker/picBed/raw/master/20210909085724.png)

所以最后调用的是`AnnotationConfigServletWebServerApplicationContext`父类的这个方法

![](https://gitee.com/sysker/picBed/raw/master/20210909085855.png)

### 总结

