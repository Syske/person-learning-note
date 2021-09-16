# spring-boot自定义容器初始化组件

### 前言

前段时间我们在分享`spring boot`启动过程的时候，提到有几个`dome`要分享下，至于分享这些`dome`的原因主要有以下几点，第一点是结合`spring boot`启动过程从实践的角度看这些组件的用法和作用；第二点是，从源码能发掘`spring boot`潜在的高级知识点，学习和消化这些知识点，实现自我提升，所以从今天开始我们会逐一把前面说的`demo`分享出来，今天我们先来看下容器初始化组件——`ApplicationContextInitializer`。

### 自定义初始化组件

#### 初始化组件

定义一个初始化组件，实现`ApplicationContextInitializer`，然后在`initialize`方法中写入我们要进行的初始化操作：

```java
/**
 * 自定义容器初始化类
 *
 * @author syske
 * @version 1.0
 * @date 2021-09-15 8:02
 */
public class SyskeInitializer implements ApplicationContextInitializer {
    private Logger logger = LoggerFactory.getLogger(SyskeInitializer.class);
    @Override
    public void initialize(ConfigurableApplicationContext configurableApplicationContext) {
        logger.info("====================start======================");
        logger.info("SyskeInitializer initialize方法被执行……");
        logger.info("ApplicationName: {}", configurableApplicationContext.getApplicationName());
        logger.info("isActive: {}", String.valueOf(configurableApplicationContext.isActive()));
        logger.info("====================end======================");
    }
}
```

这样我们的初始化组件就写好了。

#### 配置

在`resources`文件夹下创建`META-INF`文件夹，并在其下创建`sping.factories`文件，具体结构如下：

![](https://gitee.com/sysker/picBed/raw/master/20210915083035.png)

然后在`spring.factories`文件中加入初始化组件的配置：

```properties
org.springframework.context.ApplicationContextInitializer=io.github.syske.springbootlearning.initializer.SyskeInitializer
```

这里的`org.springframework.context.ApplicationContextInitializer`就是我们前面实现的初始化接口，`io.github.syske.springbootlearning.initializer.SyskeInitializer`就是我们的初始化组件的具体实现，加这个配置的作用有两点，一个就是让`spring boot`能够识别我们自己增加的组件，二一个就是声明我们组件的类型是`org.springframework.context.ApplicationContextInitializer`，这样`spring boot`在启动的过程中就会按初始化组件进行处理。

这种配置方式通常被称作`SPI`机制（`Service Provider Interface`），在各类第三方框架中经常出现，比如`dubbo`、`spring boot`，通过这种方式既可以为框架提供各种扩展，同时又可以降低框架与扩展之间的依赖，可以实现有效解耦，确实很方便，当然也很强大。

在`spring boot`中除了`org.springframework.context.ApplicationContextInitializer`之外，还为我们提供了如下扩展：

- `org.springframework.boot.env.PropertySourceLoader`：`Property`资源加载器
- `org.springframework.boot.SpringApplicationRunListener`：容器运行监听器
- `org.springframework.boot.SpringBootExceptionReporter`：异常报告器
- `org.springframework.context.ApplicationListener`：应用监听器
- `org.springframework.boot.env.EnvironmentPostProcessor`：环境变量后置处理器
- `org.springframework.boot.diagnostics.FailureAnalyzer`：失败分析器
- `org.springframework.boot.diagnostics.FailureAnalysisReporter`：失败分析报告器

当然，以上这些可能补充的也不是很完整，这里仅供参考。用法上和我们今天演示的`ApplicationContextInitializer`基本上都是一样的，各位小伙伴可以自行尝试。

另外需要提一点的是，`spring-boot`的`starter`也是基于`spring.factories`来实现的，感兴趣的小伙伴可以回顾下：





#### 启动测试

完成以上代码编写和配置工作以后，我们直接运行启动`spring boot`，然后会在控制台输出我们在`initialize`方法输出的内容：

![](https://gitee.com/sysker/picBed/raw/master/20210915081858.png)

从上面的启动日志中，我们可以发现，`ApplicationContextInitializer`组件是紧挨着`banner`打印被执行的，结合我们最近分析的启动过程，我们可以知道，初始化组件是在`prepareContext`方法中被执行的，而这个方法是紧挨着容器创建的：

![](https://gitee.com/sysker/picBed/raw/master/20210915085854.png)

从`setInitializer`方法这里我们可以看到，我们自己定义的`ApplicationContextInitalizer`已经被注册到`initializers`中了

![](https://gitee.com/sysker/picBed/raw/master/20210915081441.png)



#### 加载过程分析

具体的配置和用法分享完了，下面我们结合最近研究的`spring boot`启动过程分析下`spring.factories`的加载过程。

`spring.factories`文件需要放在`META-INF`文件夹下，注意观察文件名，我们可以发现，文件后缀刚好是`factory`的复数形式，这也说明了这个文件的用途。它是在`run`方法中被解析的，更准确的说是在实例化`SpringApplication`的时候被解析的：

首先我们在程序主入口中调用了`SpringApplication`的静态方法`run`：

![](https://gitee.com/sysker/picBed/raw/master/20210915081735.png)

然后静态`run`方法调用了另一个静态`run`，并在第二个静态`run`方法内部实例化`SpringApplication`：

![](https://gitee.com/sysker/picBed/raw/master/20210915081608.png)

实例化`SpringApplication`的时候，会同步调用`setInitializers`（紧挨着的`setListeners`是设置应用监听器的），这里设置的就是容器初始化组件（包括我们自定义的），这里获取初始化组件的方法`getSpringFactoriesInstances`其内部进行了`spring.factories`文件的解析操作：

![](https://gitee.com/sysker/picBed/raw/master/20210915081523.png)

下面就是`getSpringFactoriesInstances`方法的内部实现：

其中的`SpringFactoriesLoader.loadFactoryNames`就是解析并获取`spring.factories`文件中的`Factory`的名字，然后将最终结果放进缓存中并返回：

![](https://gitee.com/sysker/picBed/raw/master/20210915082048.png)

![](https://gitee.com/sysker/picBed/raw/master/loadFactoryNames.jpg)

### 总结

今天我们分享了自定义初始化组件，演示了定义过程、配置方式以及最终测试，整体来说还是比较简单的，当然重要的还是如何将这一组件和我们的具体业务相结合，实现我们具体的业务，这应该才是我们应该思考的。好了，关于`spring boot`初始化组件我们暂时就分享这么多，有兴趣的小伙伴可以亲自动手试一下。





