# spring-boot源码分析之beanFactory · 拾

### 前言

今天分享的`refresh`是的最后三个方法：

- `destroyBeans`
- `cancelRefresh`
- `resetCommonCaches`

这三个方法中，有两个位于`catch`语句块，主要是用于`refresh`方法运行异常时，清除已经构建的`bean`和依赖的，另一个方法位于`finally`语句块中，主要用于启动成功或失败后重置各类缓存。

### refresh最后的晚餐

#### finishRefresh补充

在开始今天的内容之前，我们先对`finishRefresh`做一个简单的补充个。

![](https://gitee.com/sysker/picBed/raw/master/images/image-20210912221356093.png)

`finishRefresh`方法内部共调用了`5`个方法，第一个方法就是情况`Resource`的缓存，其内部就是将`DefaultResourceLoader`的`resourceCaches`属性置空，这个属性是`class`和资源的`map`集合。

![](https://gitee.com/sysker/picBed/raw/master/20210913081232.png)

![](https://gitee.com/sysker/picBed/raw/master/20210913081312.png)

第二个方法是初始化生命周期处理器，其内部就是往`beanFactory`中注册一个名字为`lifecycleProcessor`的单例`bean`。并将这个`bean`赋值给当前容器的`lifecycleProcessor`。

![](https://gitee.com/sysker/picBed/raw/master/20210913081616.png)

第三个方法就是获取到第二个方法赋值的`lifecycleProcessor`，并执行它的`onRefresh`方法。

从第二个方法哪里可以看出来，生命周期处理器的类型为`DefaultLifecycleProcessor`，所以这里的的`onRefresh`方法内部实现如下：

![](https://gitee.com/sysker/picBed/raw/master/20210913082224.png)

`onRefresh`方法内部调用了 `startBean`方法，它的内部实现如下：![](https://gitee.com/sysker/picBed/raw/master/20210913082536.png)

根据`bebug`结果，最终还是会进入`forEach`的`if`条件中，虽然`autoStartOnly`是`true`，但后面的条件是成立的，因此下面的`for`循环也会被执行，最终会 `LifecycleGroup`的`start`方法：

![](https://gitee.com/sysker/picBed/raw/master/20210913083907.png)

`LifecycleGroup`最终会调用`bean`的生命周期的`start`（就是我们昨天分析的`createWebServer`方法那里注册的两个生命周期`bean`）

![](https://gitee.com/sysker/picBed/raw/master/20210913084142.png)

后面两个方法都很简单，一个是推送事件，这里推送的是`ContextRefreshedEvent`事件；另一个方法是将当前容器添加到`LiveBeansView`的`applicationContexts`容器中，也就不展开说明了。

#### 剩余方法

今天要分析的是剩余的三个方法，这三个方法有两个在`catch`中，也就是用了处理异常信息的，另一个个在`finally`中，也就是无论如何都会被执行的，下面我们就详细展开看一下。

![](https://gitee.com/sysker/picBed/raw/master/20210913085556.png)

##### destroyBeans

这个从名字就可以看出它的作用了，是的，就是销毁已经实例化完成的`bean`，也就是说如果`refresh`方法发生异常，会先销毁所有的`bean`

![](https://gitee.com/sysker/picBed/raw/master/20210913085400.png)

在`destroySingletons`方法内部，它首先调用了父类的`destroySingletons`方法，最终在父类的方法内部调用`destroySingletons`以递归的方式销毁`bean`和`bean`的依赖，具体流程如下：

![](https://gitee.com/sysker/picBed/raw/master/Snipaste_2021-09-13_21-26-22.jpg)
=======
这里最后调用的是`DefaultListableBeanFactory`的`destroySingletons`，也就是我们默认容器的销毁方法：

![](https://gitee.com/sysker/picBed/raw/master/images/20210913133143.png)

首先它调用了父类的销毁方法，在父类的销毁方法中，最终会销毁`bean`和它的依赖：

![](https://gitee.com/sysker/picBed/raw/master/images/destoryBean.jpg)

##### cancelRefresh

发生异常后取消容器刷新操作，这里只是将容器的激活状态改为`false`

![](https://gitee.com/sysker/picBed/raw/master/20210913085511.png)

##### resetCommonCaches

这个方法始终会被执行，它的作用就是清理各种缓存以及`classLoader`，其中`ReflectionUtils`清理的是和反射相关的缓存，`AnnotationUtils`清理的是和注解相关的缓存，`ResolvableType`清理的是和解析类型相关的缓存，`CachedIntrospectionResults.clearClassLoader`清理的是类加载器的相关缓存。

![](https://gitee.com/sysker/picBed/raw/master/20210913085707.png)

至此，`refresh`方法算是彻底分享完了，`run`方法中剩余的方法，由于之前已经分析过了，所以这里就不过多赘述了，后面就该花时间把最近一段时间的内容好好梳理下，然后该补充的再补充下（比如上周五的内容）。

![](https://gitee.com/sysker/picBed/raw/master/20210913214403.png)

![](https://gitee.com/sysker/picBed/raw/master/20210913085707.png)

到这里`refresh`方法就算执行完毕了。

整个`run`方法，除了`refreshContext`方法之外，还有`6`个方法，这六个方法前面也已经分析过了，所以这一次就不重复说了。

![](https://gitee.com/sysker/picBed/raw/master/images/20210913131334.png)



### 总结

说实话我是没想到剩余的三个方法这么简单，总体内容都没有昨天`finishRefresh`的补充内容多，不过也能想明白，毕竟今天内容就是`catch`和`finally`语句块的方法，也不会有太核心的内容。

今天分享完毕后，剩余的工作就是查漏补缺和知识点梳理了，原本想着经过梳理`run`方法会发现有集中初始化的代码，但是截止到现在都没找到，至少不像我之前手写的`web`服务器那种，不过现在感觉似乎已经对`spring boot`的`bean`的完整初始化过程有了一点点懵懂的认知，我想等我梳理完最近分析的代码，这一团迷雾一定会被揭开，好了，今天就先到这里吧，各位小伙伴，晚安哟！
