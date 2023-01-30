# spring-boot源码分析之BeanFactory · 柒

### 前言

今天继续看`refresh`方法，今天的目标是搞定三个方法：

- `obtainFreshBeanFactory`
- `prepareBeanFactory`
- `postProcessBeanFactory`

今天下午突然有事把我的计划打乱了，剩下的内容还没有补充进去，我又不想打断自己的计划，索性就先发一部分，剩余内容后续完善后再更新。

下面我们就先来简单看下吧！

### refresh

#### obtainFreshBeanFactory

​	这个方法的实际作用就是获取`beanFactory`，其内部调用流程如下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210910083102.png)

首先，它的内部调用了`AbstractApplicationContext`的`refreshBeanFactory`方法，由于在我们当前容器`AnnotationConfigServletWebServerApplicationContext`的所有父类（或者父类的父类）中，只有`GenericApplicationContext`重写了这个方法，所以实际调用的是`GenericApplicationContext`的`refreshBeanFactory`。

`refreshBeanFactory`方法中其实就做了两件事，一个是设置`refreshed`的值，这里用到了`java`的`CAS`机制，是线程安全的一个机制，如果实际值与预期值（`expect`）一致，则将值设置为更新值（`update`），这一块属于多线程线程安全领域的内容；另一个操作就是设置`beanFactory`的`serializationId`，这个值默认设置的是`spring.application.name`的值。



#### prepareBeanFactory

这个方法内部实际就进行了下面几种操作：

- 设置`BeanFactory`的参数，包括`beanClassLoader`（类加载器）、`BeanExpressionResolver`（表达式解析器）、`TempClassLoader`（临时类加载器）；

- 往`beanFactory`中添加了一些组件，包括`PropertyEditorRegistrar`（属性编辑注册器）、`BeanPostProcessor`（后置处理器）；

- 忽略接口依赖的操作；

- 注册依赖的操作；

- 最后，往`beanFactory`中注册了环境相关的`bean`

  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/prepareBeanFactory.jpg)

  #### postProcessBeanFactory

  关于这个方法官方注释给出如下说明：

  > Modify the application context's internal bean factory after its standard initialization. All bean definitions will have been loaded, but no beans will have been instantiated yet. This allows for registering special BeanPostProcessors etc in certain ApplicationContext implementations.

  意思就是说，这个方法是在标准初始化之后，修改应用容器的内部`beanFactory`，这时候，所有`bean`定义都已加载，但尚未实例化任何`bean`，是允许往容器中注册特殊的`BeanPostProcessor`的。所以这个方法其实就是在`bean`实例化前，往`beanFactory`中注册`BeanPostProcessor`（`bean`后置处理器）。

  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210910224239.png)

### 总结

今天由于一些特殊情况，我的原有计划又被打乱了，有点无语，但是事情撂给我了，我也不能撒手不管，所以今天只能先到这里。

虽然三个方法也算分析完了，但是原本更细致的内容还没来得及剖析，好多内容都没来得及剖析，剩余的内容，我明后两天再抽时间完善下，届时再重新分享。

好了，各位小伙伴，晚安哦！	