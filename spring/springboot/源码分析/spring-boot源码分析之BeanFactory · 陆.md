# spring-boot源码分析之BeanFactory · 陆

### 前言

从今天开始，我们要啃硬骨头了——`refreshContext`。

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

这里通过`getEnvironment`方法获取系统的环境设置，主要包括`profiles`以及资源解析器，这里的`defaultProfiles`表示`spring boot`的默认配置文件，`activeProfiles`表示`spring boot`启动时激活的配置文件。

![](https://gitee.com/sysker/picBed/raw/master/images/20210909131025.png)

关于`profile`文件，相比各位小伙伴应该都不陌生，在`spring boot`中我们的配置文件就叫`profile`，默认情况下的配置文件是`application.*`，文件类型可以是`properties`文件或者`yaml`文件，我们通常通过`spring.profiles.active=@profileActive@`（``yml`方式类似）指定需要激活的文件（环境配置）

![](https://gitee.com/sysker/picBed/raw/master/images/20210909132234.png)

获取完配置资源之后，会调用`ConfigurableWebEnvironment`的`initPropertySources`方法，下面是`initPropertySources`方法的内部调用流程。在`debug`过程中，我发现默认情况下`servletContext`和`servletConfig`都为空，所以`replace`方法实际并未执行。

![](https://gitee.com/sysker/picBed/raw/master/images/20210909133426.png)

##### validateRequiredProperties

这里校验是根据我们`AbstractPropertyResolver`解析器的`requiredProperties`中如果存在为空的配置就会报错：

![](https://gitee.com/sysker/picBed/raw/master/images/20210909202806.png)

这里的`requiredProperties`和`environment`有关，是`AbstractEnvironment`的`setRequiredProperties`方法中初始化的。

![](https://gitee.com/sysker/picBed/raw/master/images/20210909204118.png)

##### 监听器赋值

下面就是一些监听器集合的赋值操作，`earlyApplicationListeners`表示预刷新容器应用监听器集合（`pre-refresh ApplicationListeners`），`applicationListeners`表示当前容器监听器集合，`earlyApplicationEvents`就表示预刷新应用监听事件。

![](https://gitee.com/sysker/picBed/raw/master/images/20210909204652.png)



### 总结

今天效率有点低呀，但是也没办法，今天事情确实比较多——今天我负责处理`oncall`问题，然后下午又开了三个多小时的会，所以就没有太多事件搞源码分析了。

不过，我看了下剩余的内容，明天至少可以搞定`3`个方法，剩余`11`个方法，最多再需要三天应该也可以搞定，所以今天就先到这里吧~
