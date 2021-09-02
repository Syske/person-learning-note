# spring-boot源码分析之ConfigurableApplicationContext

### 前言

`ConfigurableApplicationContext`就是我们`spring-boot`最核心的内容——应用容器，`run`内部也基本都是针对它进行的各种初始化操作，运行完成后返回的也是它，所以今天我们就来看下这个`spring boot`的主角。

### ConfigurableApplicationContext

`ConfigurableApplicationContext`是一个基础接口，它是`03.11.2003`引入的（好早呀），内部包括`7`个静态常量，`13`给接口方法，同时它还继承了`ApplicationContext`、`Lifecycle`和`Closeable`。

`ApplicationContext`是所有容器的基类，`spring boot`提供了很多容器的实现，这里我们目前只看默认的容器；`Lifecycle`是和类生命周期有关的接口，它的内部提供了三个方法，`start`、`stop`和`isRunning`

#### 静态常量

- `CONFIG_LOCATION_DELIMITERS`：配置文件路径分隔符，主要用来分割各个配置文件路径的
- `CONVERSION_SERVICE_BEAN_NAME`：转换服务的`bean name`，通过这个服务，我们则可以实现类型转换操作
- `LOAD_TIME_WEAVER_BEAN_NAME`：`spring boot`加载期代码织入器的`bean name`，这个组件的作用主要是为`spring boot`自定义类加载器提供支持的
- `ENVIRONMENT_BEAN_NAME`：环境的`bean name`
- `SYSTEM_PROPERTIES_BEAN_NAME`：系统配置的`bean name`
- `SYSTEM_ENVIRONMENT_BEAN_NAME`：系统环境变量`bean name`
- `SHUTDOWN_HOOK_THREAD_NAME`：关闭钩子函数线程名称

#### 接口方法

- `setId`：设置应用容器的唯一`id`
- `setParent`：设置父级容器（上下文）
- `setEnvironment`：设置当前容器环境变量
- `getEnvironment`：返回此应用程序上下文的环境，允许进一步自定义
- `addBeanFactoryPostProcessor`：添加`BeanFactoryPostProcessor`，`BeanFactoryPostProcessor`功能比较强大，它可以修改容器的内部`bean factory`，改变`bean`的创建
- `addApplicationListener`：添加容器监听器，主要是指继承了`ApplicationListener`的监听器
- `setClassLoader`：设置类加载器
- `addProtocolResolver`：注册协议解析器。协议解析器的作用就是根据指定的地址和资源加载期，解析资源并将资源返回
- `refresh`：加载或者刷新配置持久化代理，它的来源可以是`java`基础配置、 `xml`文件、属性文件、数据库或者其他文件格式。根据官方文档描述，`refresh`是一个启动方法，如果执行失败，它会销毁已经创建的单例，以避免悬空资源。也就是说，在调用这个方法之后，要么全部实例化，要么根本不实例化。
- `registerShutdownHook`：注册关闭钩子函数
- `close`：关闭容器
- `isActive`：获取容器是否活跃
- `getBeanFactory`：获取`bean factory`

父类方法

- `getId`：获取容器`id`
- `getApplicationName`：获取应用名称
- `getDisplayName`：获取应用展示名称
- `getStartupDate`：获取启动时间
- `getParent`：获取父类容器
- `getAutowireCapableBeanFactory`：获取自动装备`bean`工厂，根据官方给出的解释，这个方法主要给`spring boot`外部使用的，便于我们将非`spring boot`的`bean`装配进`spring boot`容器中。

下面我们简单调几个方法看下效果：

![](https://gitee.com/sysker/picBed/raw/master/images/20210901192845.png)

然后我们再调一下`close`方法看下：

![](https://gitee.com/sysker/picBed/raw/master/images/20210901193023.png)

根据输出的日志我们可以看出来，执行完`close`方法之后，容器成功关闭，关闭之前`isActive`是`true`，关闭之后变成了`false`。我们调用`close`方法实际上调用的是关闭的钩子函数：

![](https://gitee.com/sysker/picBed/raw/master/20210901211952.png)

另外，在测试过程中，我发现`bean`注入容器是在`refresh`方法中进行的，但是目前还没有梳理清楚。

### 总结

今天这些内容搞完之后，我发现我有点懵逼了，`spring boot`的启动过程还是很复杂的，特别是容器的初始化过程，虽然看起来就只是基于`ConfigurableApplicationContext`，但事实上涉及到的内容特别多，比如`BeanFactoryPostProcessor`、`ApplicationListener`、`ProtocolResolver`等，这些组件每一个都是有着比较复杂的实现，以前真的只考虑用了，也从来不考虑它的内部是如何实现的，只有实际去看源码的时候，才发现类与类、类与接口、接口与接口关系原来是如此的复杂，感觉想梳理清楚真的好难。

不过幸运的是，经过这几天的摸索，阅读晦涩的源码，`debug`代码，我发现一天要比一天容易一点。我现在就感觉自己好像在挖宝藏，只能一点一点刨，但是目前刨出来东西还不足以让我看清`spring boot`的全貌，不过我相信随着不断的深入探索和研究，未来一切都会更清晰，当然后面我应该是不会再贪多了，分析源码本来就是一个费力花时间还不出活的过程，只能一点点地啃了。

最后，我特别想知道各位小伙伴最希望我分享哪方面的知识，可以给我私信或者留言，我现在基本上都是自己想到哪分享到那，所以内容上可能不一定符合各位小伙伴的口味和节奏，如果你能说出自己的需求或者想法，那这个学习过程才意思，你说呢？

好了，今天就先到这里吧！

