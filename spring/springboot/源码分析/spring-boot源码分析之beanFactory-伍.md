# spring-boot源码分析之beanFactory · 伍

### 前言

原本是打算昨天把`prepareContext`方法梳理完，今天开始啃硬骨头——`refresh`方法的，结果大家昨天就知道了：由于篇幅的问题，剩余内容放在今天分享了。

然后今天的想法是除了昨天需要补充的内容外，看能不能把`refresh`的内容也分享一部分，毕竟是硬骨头，然而现实情况是在我把昨天需要补充的内容梳理之后，发现剩余的内容还不少，所以就只能先不开始新的内容了，等`prepareContext`方法彻底剖析完毕之后我们再啃硬骨头。

下面就让我们看下`prepareContext`的剩余内容吧！

### prepareContext补充

下面这些内容原本是昨天要一起分享的，但是由于内容比较多，而且昨天时间有点晚了，所以就没来得及分享，下面我们就先来做一些简单的补充说明。

#### 创建BeanDefinitionLoader

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210907211014.png)

  首先是创建`bean`的定义加载器，创建`beanDefiniton`加载器的时候，首先是一个赋值操作，然后创建了`AnnotatedBeanDefinitionReader`，它的创建就稍微有点复杂。 ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210907211446.png)

##### 实例化ConditionEvaluator

  创建`AnnotatedBeanDefinitionReader`的时候要先创建`ConditionEvaluator`，而`ConditionEvaluator`实例化的时候又需要先实例化`ConditionContextImpl`，这里的`ConditionEvaluator`和`ConditionContextImpl`是`spring boot`引入的新特性，主要用于条件配置，我们可以通过`@Conditional`注解使用这一特性，后面专门来分析吧（又发现新大陆了……）。

  最后一步都是赋值操作，就没啥好讲的了。

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210907212256.png)

  另外，在`load`方法中调用了另一个方法`registerAnnotationConfigProcessors`。就说这方法看着眼熟，原来我们昨天分析`beanDefinitionMap`初始化的时候，已经研究过了。  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210907214219.png)

  这里注册完成后`beanDefinitionMap`会多出`5`个元素。  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210906212208.png)

  下面两个`Reader`的初始化就不再详细分析了，基本上都是简单的实例化和赋值操作：  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210907214756.png)

##### 实例化scanner

  后面两个操作有必要讲一下，首先实例化了`scanner`，在实例化过程中，注册了三个注解类型过滤器（`AnnotationTypeFilter`）

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210908082829.png) 

事实上，`javax.inject.Named`，并没有被注册成功，因为当前`class`并不存在，关于这一点，下面的截图可以很清楚地说明，因为在注册`JSR-330`的`class`时候报了`java.lang.ClassNotFoundException`异常，所以最终的结果就是`@Component`和`@ManagedBean`这两种注解类型拦截器被成功注入，我们通过`includeFilters`的大小也可以看出这一点。

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210908083456.png) 

##### 注册排除过滤器

排除过滤器（`excludeFilters`）就是过滤不需要被扫描的资源。所以这一步的操作就比较简单了，就是往`scanner`的 排除过滤器（`excludeFilters`）中增加了一个`ClassExcludeFilter`，传入的是`sources`，目前`sources`只有我们`spring boot`项目的主类。

这里需要注意的是，`excludeFilters`本身是个`List`，所以这里`add`的时候其实是把新的排除注册器放在`excludeFilters`的最前面。

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210908084904.png)

#### 设置loader属性

下面就是这只`loader`的属性，包括`beanNameGennerator`、`resourceLoader`和`environment`。但是由于这些参数都是空的，所以默认情况下这些设置方法并不会被执行：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210908130336.png)

#### loader加载资源

下面是`load`方法最核心的执行流程，核心部分就是注册`Bean`

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210908131728.png)

由于一张截图无法完整体现`registerBean`的流程，所以我分成了两张截图，这里最核心的就是`doRegisterBean`方法，这个方法内部会构建当前`class`的`BeanDefinition`。其中`AnnotatedGenericBeanDefinition`是根据注解信息生成的`bean`的`definition`信息，包括`beanClass`、`AnnotationMetadata`（注解元数据）、`scope`（范围）等，总之就是凡是通过注解方式配置的类，都是通过`AnnotatedGenericBeanDefinition`来构建它的`definition`信息的，它本身也就是为了支持注解元数据而生的。

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210908132127.png)

上面这些操作执行完毕后会往`beanFactory`的`beanDefinitionMap`和`beanDefinitionNames`分别保存`beanClass`的`beanName`和`beanDefinition`信息

#### 执行事件监听

这里调用的是监听器容器的`contextLoaded`方法，其方法内部本质上是触发对应的事件，从方法名上我们可以看出来这个方法其实发的就是容器已经加载完成的事件。下面是`Logger`

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210908144903.png)

`debug`过程中，我发现这里触发的时间类型是`ApplicationPeparedEvent`事件，这里的事件类别挺多的，不同的监听器会执行各自的`onApplicationEvent`方法，上面的流程中我们就是以`LoggingApplicationListener`为例，剖析其执行流程的

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210908214555.png)

对于`LoggingApplicationListener`总共会处理`5`种事件，这里处理的是`ApplicationPreparedEvent`事件，也就是我们前面看到的类型

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210908214752.png)

在当前事件类型下，`LoggingApplicationListener`的`onApplicationEvent`方法会往容器中注册两个单例实例，中间的`logFile`为空，所以并未成功注入。

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210908215403.png)



### 总结

好了，到今天我们算是把`prepareContext`方法的内容梳理完了，整体来看还算清晰。

说实话，我是没想到一小块补充内容能有这么多，但事实确实如此，这也从侧面说明了`spring boot`本身确实比较复杂，任何一小行代码，其内部可能都潜藏着核心的实现代码。我数了一下，不算括号和`if`语句，只有`17`行，但是就这短短的`17`行代码，我用了近三千字还没有说的特别清楚，我自己都不敢想象，不过好的一点是，虽然中间磕磕绊绊，但也算是啃下来了，不过更硬的骨头还在后头——`refresh`方法才是重头戏，还是不能松懈呀~

最后，我想说的是，任何一小行代码很有可能就是解开你心中困惑的钥匙，所以不论是坑，还是意外收获，更多时候都需要我们自己亲自蹚~

