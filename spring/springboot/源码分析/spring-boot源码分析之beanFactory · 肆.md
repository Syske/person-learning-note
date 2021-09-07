# spring-boot源码分析之beanFactory · 肆

### 前言

昨天我们又分析了容器的创建过程，从容器的创建过程中，我们找到了`beanFactory`实例化后最基本的初始化——注册需要忽略的接口（`ignoreDependencyInterface`）、注册配置处理器（`registerAnnotationConfigProcessors`），`beanFactory`剩余的初始化操作都在后面的方法中，今天我们先来看`prepareContext`，虽然在`prepareContext`前面还有一个`getSpringFactoriesInstances`方法，但是这个方法并没有和`beanFactory`进行交互，所以就直接跳过了。

![](https://gitee.com/sysker/picBed/raw/master/20210907082542.png)

### prepareContext

关于这个方法，我们前面已经分析过了，但基本上都是一带而过，所以今天我们就沿着`beanFactory`的初始化过程再来看下这个核心方法：

![](https://gitee.com/sysker/picBed/raw/master/20210907083403.png)

我们先来梳理下这个方法的执行流程：

- 设置容器环境（`context.setEnvironment`），这一步操作基本与`beanFacotry`没有关系，有的也是一些取值操作，并没有往`beanFactory`中注册数据：

  ![](https://gitee.com/sysker/picBed/raw/master/20210907084306.png)

- 容器后置处理（`postProcessApplicationContext`），这个方法内部主要有三步操作。第一步是往`beanFactory`中注册`beanName`生成器，但由于默认情况下这个配置为空，所以并未进行注册操作；第二步是设置容器的资源加载器，由于`resourceLoader`是空，所以这里也没有设置；最后一步是注册转换服务，默认情况下会为我们注册`136`个转换器，这些转换器的作用就是进行类型转换，如果能在实际开发中用起来，那也是美滋滋了：

  ![](https://gitee.com/sysker/picBed/raw/master/20210907084806.png)

  可以看到默认情况下为我们注册的转换器包括了`String`转`Date`这种常用的转换，当然我们也可以定义自己的转换器，这个我记下来，后面专门出一期`demo`示例。

  ![image-20210907085757521](C:\Users\syske\AppData\Roaming\Typora\typora-user-images\image-20210907085757521.png)

### 总结