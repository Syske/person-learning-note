# spring-boot源码分析之beanFactory · 肆

### 前言

昨天我们又分析了容器的创建过程，从容器的创建过程中，我们找到了`beanFactory`实例化后最基本的初始化——注册需要忽略的接口（`ignoreDependencyInterface`）、注册配置处理器（`registerAnnotationConfigProcessors`），`beanFactory`剩余的初始化操作都在后面的方法中，今天我们先来看`prepareContext`，虽然在`prepareContext`前面还有一个`getSpringFactoriesInstances`方法，但是这个方法并没有和`beanFactory`进行交互，所以就直接跳过了。

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210907082542.png)

### prepareContext

关于这个方法，我们前面已经分析过了，但基本上都是一带而过，所以今天我们就沿着`beanFactory`的初始化过程再来看下这个核心方法：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210907083403.png)

我们先来梳理下这个方法的执行流程：

- 设置容器环境（`context.setEnvironment`），这一步操作基本与`beanFacotry`没有关系，有的也是一些取值操作，并没有往`beanFactory`中注册数据：

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210907084306.png)

- 容器后置处理（`postProcessApplicationContext`），这个方法内部主要有三步操作。第一步是往`beanFactory`中注册`beanName`生成器，但由于默认情况下这个配置为空，所以并未进行注册操作；第二步是设置容器的资源加载器，由于`resourceLoader`是空，所以这里也没有设置；最后一步是注册转换服务，默认情况下会为我们注册`136`个转换器，这些转换器的作用就是进行类型转换，如果能在实际开发中用起来，那也是美滋滋了：

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210907084806.png)

  可以看到默认情况下为我们注册的转换器包括了`String`转`Date`这种常用的转换，当然我们也可以定义自己的转换器，这个我记下来，后面专门出一期`demo`示例。

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210907130505.png)
  
- 初始化操作（`applyInitializers`），这个方法我们昨天已经分析过了，这里就不再赘述了，后面关于`ApplicationContextInitializer`的初始化我也会专门做一期`demo`分享的。

- 绑定容器初始化事件（`contextPrepared`），这个方法在容器创建并准备好之后，资源加载完成前执行，这一步和`beanFactory`也没有关系

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210907132035.png)

- 打印`startupInfo`。下面那一段代码就是打印启动日志信息， 默认情况下`logStartupInfo`是`true`，所以控制台会输出两行日志：

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210907132528.png)

- 获取`beanFactory`（ `context.getBeanFactory()`），这个是为了方便后面注册数据，因为紧接着就需要把`springApplicationArguments`、`springBootBanner`等注册到`beanFactory`中：

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210907132902.png)

  最终`registerSingleton`方法会把他们注册到`singletonObjects`容器中，从名字我们就可以看出来，这是个存放单例对象的容器。

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210907133313.png)

- 设置是否允许同名覆盖（`setAllowBeanDefinitionOverriding`），默认情况下为`true`（`allowBeanDefinitionOverriding`属性默认值）。如果为`true`，后面的`BeanDefinition`数据会将前面的覆盖掉。但是默认启动时，`spring boot`会将它该为`false`

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210907135410.png)

- 添加`beanFactory`懒加载后置处理器（`addBeanFactoryPostProcessor`），由于默认情况下并未启动懒加载，所以默认情况下懒加载后置处理器也不会被添加

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210907205656.png)

- 获取所有资源（`getAllSources`），默认情况下只包括当前`spring boot`项目的主类，同时关联了包括`classLoader`、`packages`等数据

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210907210316.png)

- 将资源加载到容器中（`load`，官方文档给的解释是`bean`）。这个方虽然看起来其貌不扬，但是内部操作还是蛮多的。本来内容已经写出来了，但是介于篇幅我决定把剩余内容放到明天分享，当然也是因为`load`方法确实也比较重要，其内部不仅包括了`scanner`的初始化，而且包括了`filter`的相关内容，这些都算是`spring boot`的核心内容，所以还是要尽可能详细些。


### 总结

原本是打算把`prepareContext`的内容一次性分享完的，但是实际分享的时候，发现内容还是蛮多的，特别是`load`方法，一个看起来小小的方法，没想到它的内部初始化操作还挺复杂的。不过，经过今天的梳理之后，我感觉对`prepareContext`认识要比之前清晰多了，而且在分析的过程中，还发现了两个需要`demo`实践的内容，相关内容的`flag`已经立起来了，后面就该填坑了，这也算是意外的收获吧。

好了，今天就先到这里吧！
