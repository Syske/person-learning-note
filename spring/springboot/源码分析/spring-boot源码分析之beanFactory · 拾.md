# spring-boot源码分析之beanFactory · 拾

### 前言



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

##### cancelRefresh

发生异常后取消容器刷新操作，这里只是将容器的激活状态改为`false`

![](https://gitee.com/sysker/picBed/raw/master/20210913085511.png)

##### resetCommonCaches

这个方法始终会被执行，它的作用就是清理各种缓存以及`classLoader`

![](https://gitee.com/sysker/picBed/raw/master/20210913085707.png)