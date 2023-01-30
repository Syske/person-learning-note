# spring-boot源码分析之beanFactory · 玖

### 前言

今天我们开始看`refresh`的最核心方法，这四个方法剖析完成，`spring boot`就真的启动成功了：

- `onRefresh`
- `registerListeners`
- `finishBeanFactoryInitialization`
- `finishRefresh`

### refresh

#### onRefresh

这个方法就是初始化特殊子类容器中的特殊`bean`，这个方法的具体调用流程如下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/image-20210912175455943.png)

首先它先调用了`abstractApplicationContext`的`onRefresh`方法，由于这个是个抽象类，所以实际上调用的是当前容器或者其父类继承了`abstractApplicationContext`的类的`onRefresh`方法，实现`onRefresh`的类总共有`5`个：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/image-20210912181514838.png)

但其中只有`ServletWebServerApplicationContext`是我们当前容器的父类，所以实际上最后调用的是`ServletWebServerApplicationContex`的`onRefresh`方法，在它的方法内部有两部分调用，一个是调用父类的`onRefresh`方法，父类的方法内部其实就是进行了`themeSource`资源的初始化；另一部分，调用了`createWebServer`方法，顾名思义，就是创建`web`服务器。

##### initThemeSource

先看父类`onRefresh`的调用，它的内部其实就是进行了主题资源的初始化，准确地说就是进行了实例化和赋值，最后将`themeSource`返回：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/initThemeSource.jpg)

看了半天才搞明白，原来这里的`themeSource`指的就是主题资源，我还在纳闷`spring boot`为啥还需要主题（就是手机桌面这种主题），最后才发现原来是给消息资源使用，主要包括`css`、图片等资源：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/image-20210912181259998.png)

##### createWebContext

这个方法就是为了创建`webServer`，这一点从名字就可以看出来：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/image-20210912183728213.png)

默认情况下`webServer`和`servletContext`都是`null`，所以会创建`webServer`实例，默认情况下创建的是`TomcatWebServer`的实例，创建完成后会往`beanFactory`中注册`webServer`的两个生命周期实例，一个是`shutdown`，一个是`startStop`，这两个生命周期主要是用来控制服务启停的。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/image-20210912190041589.png)



#### registerListeners

这个方法就是注册监听器，而且方法注释上也写的很清楚：校验并注册监听器

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/image-20210912195223725.png)

内部实现也很简单，首先是往应用事件广播器中添加监听器；

然后还把监听器的`beanName`注册进应用监听器的接收器（`defaultRetriever`）列表中，而且这里注释的很清楚：这里不初始化`FactoryBeans`；

最后是推送应用预刷新事件（也就是我们第陆部分的内容，这里的监听器是在`prepareRefresh`方法中进行初始化的）

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/image-20210912195442790.png)

#### finishBeanFactoryInitialization

从名字就可以看出来，这个方法就是完成最后的`beanFactory`初始化，方法注释也说的很清楚，会初始化剩余的单例`bean`。

方法主要有四块内容，第一块是设置`beanFacory`的转换服务，我就说这一块的代码咋看着有点眼熟，原来是在分析`prepareContext`方法的时候，当时也有调用这个方法。

第二块是注册已经嵌入的配置值的解析器，这里是`lambda`的写法，这注册的应该是对`$Value{name}`这样的配置的解析器

第三块是获取加载时间织入器，但是有一点我有点看不懂，`getBean`是有返回值的，这里也没有接收，所以这里调用只是为了校验？

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/image-20210912202656004.png)

第四块就是调用`beanFactory`的三个方法，首先是调用`setTempClassLoader`置为`null`，官方给的注释是停止使用临时加载器；然后调用`freezeConfiguration`方法，官方给的注释是仅获取`bean`的定义元数据，不做其他操作；最后调用`preInstantiateSingletons`方法，从方法名来看这个方法会进行单例`bean`的预初始化操作，官方给的注释是实例化剩余的单例。

下面我们详细看下`freezeConfiguration`和`preInstantiateSingletons`，先看`freezeConfiguration`方法：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/image-20210912211019971.png)

本以为这个方法内部实现很复杂，点进来才发现就两行代码，第一行将`configurationFronzen`设置为`true`，这个属性用于标记`bean`的定义元数据是否已经被缓存。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/image-20210912211254992.png)

第二行是将`bean`定义名赋值给`frozenBeanDefinitionNames`，从名字推测这个应该是为了冻结`bean`定义名，这也就意味着在这个方法执行之后，不会再注册新的`bean`定义名。

下面我们看第四块的第三个方法——`preInstantiateSingletons`，这个方法主要有两大块内容，一块是实例化非懒加载的`bean`（通过`getBean`方法，看来我对这个方法理解的不够透彻，但是这个方法内部并没有进行`newInstance`这样的操作，而是直接从`bean`的`beanFactory`中获取）；

另一块是初始化后，回调操作。这里的`doPrivileged`方法是`java.security`包下提供的一个特权操作，关于这一块后面需要深入研究下。这个`doPrivileged`内部调用了`afterSingletonsInstantiated`，这个方法在单例实例化完成后调用，就是我们说的回调操作

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/image-20210912213047177.png)

#### finishRefresh

这个方法就是完成最后的清理工作，同时会初始化容器的生命周期处理器，然后执行容器生命周期的刷新操作，最后会推送启动刷新完成事件

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/image-20210912221356093.png)



### 总结

紧赶慢赶，四个方法总算全部分享完了，差一点点就分析不完了，而且最后一个方法实在分析地有点拉垮。

总之，关于这两天的内容更新，我总结出来两点：

第一，周末效率有点低下，没玩好也没学好，特别容易被打扰，内容输出还是要找一个安静、舒适的环境，这样精力比较集中；

第二，`spring boot`真的上头呀。感觉`run`方法的核心代码都已经分析完了，但我咋发现，我好像还是没理清楚`spring boot`的启动流程呢？或者更准确的说是感觉目前分析的内容和我预期的是有差异的，而且差异很大，具体的差异感觉得等我把`run`方法整体分析完，再回过头来总结，才能得出结论。现在感觉好像懂了，但是又没完全懂，说不懂吧，整体的知识更清晰了，感觉还是很朦胧。

确实有点上头了，而且`spring boot`的类名和方法名还老长，经常比对方法名比对半天……说多了都是泪，怕不是有点走火入魔了吧，赶快结束吧，后面要慢慢花时间笑话了……