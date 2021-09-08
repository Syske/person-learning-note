# spring-boot源码分析之beanFactory · 伍

### 前言



### prepareContext补充

下面这些内容原本是昨天要一起分享的，但是由于内容比较多，而且昨天时间有点晚了，所以就没来得及分享，下面我们就先来做一些简单的补充说明。

#### 创建BeanDefinitionLoader

![](https://gitee.com/sysker/picBed/raw/master/20210907211014.png)

  首先是创建`bean`的定义加载器，创建`beanDefiniton`加载器的时候，首先是一个赋值操作，然后创建了`AnnotatedBeanDefinitionReader`，它的创建就稍微有点复杂。 ![](https://gitee.com/sysker/picBed/raw/master/20210907211446.png)

##### 实例化ConditionEvaluator

  创建`AnnotatedBeanDefinitionReader`的时候要先创建`ConditionEvaluator`，而`ConditionEvaluator`实例化的时候又需要先实例化`ConditionContextImpl`，这里的`ConditionEvaluator`和`ConditionContextImpl`是`spring boot`引入的新特性，主要用于条件配置，我们可以通过`@Conditional`注解使用这一特性，后面专门来分析吧（又发现新大陆了……）。

  最后一步都是赋值操作，就没啥好讲的了。

  ![](https://gitee.com/sysker/picBed/raw/master/20210907212256.png)

  另外，在`load`方法中调用了另一个方法`registerAnnotationConfigProcessors`。就说这方法看着眼熟，原来我们昨天分析`beanDefinitionMap`初始化的时候，已经研究过了。  ![](https://gitee.com/sysker/picBed/raw/master/20210907214219.png)

  这里注册完成后`beanDefinitionMap`会多出`5`个元素。  ![](https://gitee.com/sysker/picBed/raw/master/20210906212208.png)

  下面两个`Reader`的初始化就不再详细分析了，基本上都是简单的实例化和赋值操作：  ![](https://gitee.com/sysker/picBed/raw/master/20210907214756.png)

##### 实例化scanner

  后面两个操作有必要讲一下，首先实例化了`scanner`，在实例化过程中，注册了三个注解类型过滤器（`AnnotationTypeFilter`）

![](https://gitee.com/sysker/picBed/raw/master/20210908082829.png) 

事实上，`javax.inject.Named`，并没有被注册成功，因为当前`class`并不存在，关于这一点，下面的截图可以很清楚地说明，因为在注册`JSR-330`的`class`时候报了`java.lang.ClassNotFoundException`异常，所以最终的结果就是`@Component`和`@ManagedBean`这两种注解类型拦截器被成功注入，我们通过`includeFilters`的大小也可以看出这一点。

![](https://gitee.com/sysker/picBed/raw/master/20210908083456.png) 

##### 注册排除过滤器

排除过滤器（`excludeFilters`）就是过滤不需要被扫描的资源。所以这一步的操作就比较简单了，就是往`scanner`的 排除过滤器（`excludeFilters`）中增加了一个`ClassExcludeFilter`，传入的是`sources`，目前`sources`只有我们`spring boot`项目的主类。

这里需要注意的是，`excludeFilters`本身是个`List`，所以这里`add`的时候其实是把新的排除注册器放在`excludeFilters`的最前面。

![](https://gitee.com/sysker/picBed/raw/master/20210908084904.png)

#### 设置loader属性

下面就是这只`loader`的属性，包括`beanNameGennerator`、`resourceLoader`和`environment`

![](https://gitee.com/sysker/picBed/raw/master/20210908090105.png)

### 总结