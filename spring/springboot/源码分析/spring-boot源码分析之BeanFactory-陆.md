# spring-boot源码分析之BeanFactory · 陆

### 前言

从今天开始，我们要啃硬骨头了——`refreshContext`。这个方法就是我们一直在说的`spring boot`最核心的方法，这个方法执行完成后，`spring boot`基本上就初始化完了，剩下的方法就是推送启动事件，回调相关的监听器之类的，反正就是吃透`refresh`方法，基本上就可以宣告革命胜利了，换句话说，就是如果我们啃下这块硬骨头之后，`spring boot`启动这块我们就算彻底剖析完了，剩下的都是查漏补缺的小知识点了，搂草打兔子，顺手的事。

好了，大话就说这么多，下面我们开始干活~

### refreshContext

容器的刷新首先是从`refreshContext`方法开始的，然后`refreshContext`方法内部会调用容器的`refresh`方法。 

这里 `refreshContext`就做了两件事，一个是注册容器关闭钩子函数，另外一个就是刷新容器。

关闭钩子函数可以让我们更优雅地关闭`spring boot`容器，这一块后期也专门分享一次；刷新容器方法最终会调用容器的刷新方法，关于这个方法，我们之前已经分享过了，她就是刷新容器中的持久化资源，这里的资源包括`xml`、`java`配置、注解、配置文件、数据库等。

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210909081203.png)

下面，我们就来详细看下它的内部实现。我们先看下它的调用流程：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210909082926.png)

从上面图中我们可以看出来，最终其实调用的是`AbstractApplicationContext`的`refresh`方法，这个方法内部比较长，总共调用了`15`个方法，下面我们就逐一剖析这些方法，不过工作日时间有限，今天可能也分享不了太多内容，具体视情况而定吧。

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/refresh.png)

#### prepareRefresh

我们先说`prepareRefresh`方法，这个方法的作用就是为后面的刷新操作做准备，内部实现如下：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/prepareRefresh.png)

简单解释下它的执行流程：

- 首先设置`spring boot`的启动时间，获取的是当前时间；
- 然后分别设置`closed`和`active`为`flase`和`true`，这两个属性都是原子类`AtomicBoolean`。

- 接着会根据日志设置等级输出日志，不过这里必须是`begug`级别才会输出，如果是`trace`等级的，则会输出更详细的日志信息。
- 再然后，它会调用`initPropertySources`方法，这个方法的作用就是进行配置资源初始化初始化，我们等下详细剖析；
- 再下面就是资源的校验，这块也需要展开分析
- 最后是监听器和监听事件的赋值操作

##### initPropertySources

`initPropertySources`方法进行的就是`property`资源的初始化，当前容器并没有重写该方法：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210909085724.png)

由于 `AbstractApplicationContext`的`initPropertySources` 方法是空实现，而且`AnnotationConfigServletWebServerApplicationContext`并没有重写该方法，所以最后调用的是父类`GenericWebApplicationContext`的这个方法，父类的方法中最后调用的是`ConfigurableWebEnvironment`的配置资源初始化方法：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210909085855.png)

在方法内部，首先通过`getEnvironment`方法获取系统的环境设置，然后同获取到的环境设置进行配置资源初始化，其中`servletConfig`的入参直接为`null`。

关于这里获取到的`ConfigurableWebEnvironment`，我们做一点点扩展补充，`ConfigurableWebEnvironment`主要的属性是`profiles`和资源解析器，这里的`defaultProfiles`表示`spring boot`的默认配置文件，`activeProfiles`表示`spring boot`启动时激活的配置文件，从下面截图也可以很清楚看出来：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210909131025.png)

关于`profile`文件，相比各位小伙伴应该都不陌生，在`spring boot`中我们的配置文件就叫`profile`，默认情况下的配置文件是`application.*`，文件类型可以是`properties`文件或者`yaml`文件，我们通常通过`spring.profiles.active=@profileActive@`（``yml`方式类似）指定需要激活的文件（环境配置）

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210909132234.png)

获取完配置资源之后，会调用`ConfigurableWebEnvironment`的`initPropertySources`方法，下面是`initPropertySources`方法的内部调用流程。在`debug`过程中，我发现默认情况下`servletContext`和`servletConfig`都为空，所以`replace`方法实际并未执行。

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210909133426.png)

##### validateRequiredProperties

这里校验是根据我们`AbstractPropertyResolver`解析器的`requiredProperties`属性进行判断的，如果存在为空的配置就会报错，说这个方法内部实现也很简单，流程也不是很复杂，就是一些简单的资源获取和空判断：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210909202806.png)

这里的`requiredProperties`和`environment`有关，它是`AbstractEnvironment`的`setRequiredProperties`方法中初始化的，关于这个方法的调用，等我们回头分析`environment`初始化的时候再来研究。

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210909204118.png)

##### 监听器赋值

`prepareRefresh0`方法的最后就是一些监听器集合的赋值操作，`earlyApplicationListeners`表示预刷新容器应用监听器集合（`pre-refresh ApplicationListeners`），`applicationListeners`表示当前容器监听器集合，`earlyApplicationEvents`就表示预刷新应用监听事件。

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210909204652.png)

其实也就是监听器的初始化，代码也很简单，加上注释就很容器理解，我也就不再赘述了。

### 总结

今天效率有点低呀，一整天就搞定了一个方法，确实有些离谱，但是也没办法，今天事情确实比较多——今天我负责处理`oncall`问题，然后下午又开了三个多小时的会，下班那会还在排查处理线上问题，有点难呀~

不过，好在之前已经把今天的内容写的七七八八了，不然今天新内容就悬了……刚刚又看了下剩余的内容，明天应该可以搞定`3`个方法，然后还剩`11`个方法，后天`4`个，大后天`4`个，周一安排`3个`，完美，所以今天就先到这里吧~
