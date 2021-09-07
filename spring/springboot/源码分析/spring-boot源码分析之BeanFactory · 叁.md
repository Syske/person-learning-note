# spring-boot源码分析之BeanFactory · 叁

### 前言

今天我们继续研究`BeanFactory `，不过今天分享的内容有点零散，主要包括三个方面的内容，一个是`ApplicationContextInitializer`的初始化，这个严格来说和`BeanFactory`没什么关系，但是源码也分析了，所以这里提一下，另一个是`ignoredDependencyInterfaces`，这个是`BeanFactory`的一个核心属性，用于屏蔽我们不需要进行依赖检查和自动注入的接口，最后一个是`beanDefinitionMap`，这一次我们找到了它最开始初始化的代码，所以这里一起分享下。

### BeanFactory初始化过程

#### ApplicationContextInitializer初始化

下面是` ApplicationContextInitializer`的初始化操作，`ApplicationContextInitializer`是`spring boot`提供的一套初始化机制，它的`initialize`方法在`spring boot`容器刷新前执行，通常被用来进行配置文件初始化，我们也可以自己定义自己的`ApplicationContextInitializer`，后面我们可以做一期`demo`示例。

`ApplicationContextInitializer`的初始化操作是在 `prepareContext`方法中被执行的，默认情况下，会有`7`个 `ApplicationContextInitializer`被执行

![](https://gitee.com/sysker/picBed/raw/master/images/20210906132331.png)

下面是第一个`ApplicationContextInitializer`的方法源码其他类似，需要注意的是`ApplicationContextInitializer`本身是顺序的，而且方法内部也有排序操作：

![](https://gitee.com/sysker/picBed/raw/master/images/20210906133135.png)

在第二个`ApplicationContextInitializer`初始化方法内容，它往容器中注册了`BeanFactory`的后置处理器

![](https://gitee.com/sysker/picBed/raw/master/images/20210906133753.png)

#### 回到容器初始化开始的地方

根据下面的截图，我们可以看出来，`beanFactory`其实在容器创建完成后，已经完成了一部分初始化操作，所以想要搞清楚`beanFactroy`的初始，必须要回到`beanFactory`初始化的地方。

![](https://gitee.com/sysker/picBed/raw/master/images/20210906131949.png)

#### 发现ignoredDependencyInterfaces

`ignoredDependencyInterfaces`是`BeanFactory`的一个核心属性，用于屏蔽我们不需要进行依赖检查和自动注入的接口，下面是`BeanFactory`初始化` ignoredDependencyInterfaces`的代码，这段代码也是在创建容器的时候被执行的。

![](https://gitee.com/sysker/picBed/raw/master/images/20210906134241.png)`ignoredDependencyInterfaces`存放的是需要忽略的依赖接口，默认情况下只会加入`BeanFactoryAware`的接口，根据官方解释，加入`ignoredDependencyInterfaces`中的接口，会忽略依赖检查，并且不会被`autowire`

![](https://gitee.com/sysker/picBed/raw/master/20210906213753.png)

#### 找到beanDefinitionMap初始化开始的地方

下面是`beanDefinitionMap`最开始初始化的代码，我们可以看到，在执行完`registry.registerBeanSefinition`方法之后，第一个`bean`的`definition`信息被成功注册。

下面是`registerAnnotationConfigProcessors`方法的完整截图：

![](https://gitee.com/sysker/picBed/raw/master/20210906211558.png)

![](https://gitee.com/sysker/picBed/raw/master/20210906211930.png)

![](https://gitee.com/sysker/picBed/raw/master/20210906212005.png)

![](https://gitee.com/sysker/picBed/raw/master/20210906212208.png)

这个方法在`AnnotationConfigUtils`这个类中，它是在实例化`AnnotationConfigServletWebServerApplicationContext`的`reader`属性的时候被执行的。

![](https://gitee.com/sysker/picBed/raw/master/20210906214657.png)

![](https://gitee.com/sysker/picBed/raw/master/20210906214742.png)

这个方法的作用是注册给定的注解后置处理器，从包名上我们可以看出来，这五个类有两个是和事件监听器相关的，有三个是和注解相关的，其中还有一个类没有被注入，是和`jpa`相关的组件，应该和我们没有引入`jpa`的依赖和配置有关系。关于`beanDefinitionMap`我们暂时就先说这么多，至于这五个最先被注册的元老级类，我们后面再来详细了解。

### 总结

`spring boot`的源码真的太上头了，这些内容本来是中午要输出的，但是由于早上没有太多进展，最后连图都没画好，然后中午也没有理出内容，一直等到下班回到家，才开始真正干活，所以今天的绝大多数内容都是晚上回到家才搞出来的。严格来说，最近这几天都是如此，但是经过我最近这段时间的梳理和硬啃，现在感觉多少有点眉目了，自我感觉关于`run`方法我已经梳理完`40%~50%`的内容，剩下`reflush`方法大概能占到`30%`的内容，事件监听相关内容大概占比`20%`，反正感觉慢慢能看见胜利的曙光了……加油吧，没有别的选择了~

好了，各位小伙伴晚安！

