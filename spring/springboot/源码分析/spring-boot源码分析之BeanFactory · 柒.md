# spring-boot源码分析之BeanFactory · 柒

### 前言

今天继续看`refresh`方法，今天的目标是搞定三个方法：

- `obtainFreshBeanFactory`
- `prepareBeanFactory`
- `postProcessBeanFactory`

### refresh

#### obtainFreshBeanFactory

​	这个方法的实际作用就是获取`beanFactory`，其内部调用流程如下：

![](https://gitee.com/sysker/picBed/raw/master/20210910083102.png)

首先，它的内部调用了`AbstractApplicationContext`的`refreshBeanFactory`方法，由于在我们当前容器`AnnotationConfigServletWebServerApplicationContext`的所有父类（或者父类的父类）中，只有`GenericApplicationContext`重写了这个方法，所以实际调用的是`GenericApplicationContext`的`refreshBeanFactory`。

`refreshBeanFactory`方法中其实就做了两件事，一个是设置`refreshed`的值，这里用到了`java`的`CAS`机制，是线程安全的一个机制，如果实际值与预期值（`expect`）一致，则将值设置为更新值（`update`），这一块属于多线程线程安全领域的内容；另一个操作就是设置`beanFactory`的`serializationId`，这个值默认设置的是`spring.application.name`的值。



#### prepareBeanFactory

这个方法内部实际就进行了下面几种操作：

- 设置`BeanFactory`的参数，包括`beanClassLoader`（类加载器）、`BeanExpressionResolver`（表达式解析器）、`TempClassLoader`（临时类加载器）；

- 往`beanFactory`中添加了一些组件，包括`PropertyEditorRegistrar`（属性编辑注册器）、`BeanPostProcessor`（后置处理器）；

- 忽略接口依赖的操作；

- 注册依赖的操作；

- 最后，往`beanFactory`中注册了环境相关的`bean`

### 总结