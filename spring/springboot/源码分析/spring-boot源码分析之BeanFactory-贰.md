# spring-boot源码分析之BeanFactory · 贰

### 前言

`BeanFactory`是`spring boot`的最重要的核心组件，当然也是`spring boot`非常基础的组件，所以梳理清楚`BeanFactory`的源码才是梳理清楚`Spring boot`源码的关键。前天，我们分享了`beanDefinitionNames`和`beanDefinitionMap`的初始化过程，虽然过程中有涉及到`beanFactory`的相关知识点，但是关于`beanFactroy`我们还没有正式地分析过它，关于它的初始化过程，也是一无所知，为了更系统地了解`beanFactory`，从今天开始我们开始更系统地分析`beanFactory`的相关源码，下面我们就先来看下`BeanFactory`的初始化过程。

### BeanFactory初始化

今天我们依然是从一张时序图开始讲起，下面这张时序图就是`spring boot`容器的`BeanFactory`初始化过程，`beanFactory`初始化其实是和容器的初始化同时完成的，它也是容器初始化过程中的重要一步：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/BeanFactory创建过程.svg)

在上面的时序图中，最关键的内容就是`AnnotationConfigServletWebServerApplicationContext`的实例化过程，这里面涉及到`java`类的初始化流程：创建子类时，必须先调用父类无参构造方法，所以`AnnotationConfigServletWebServerApplicationContext`是在所有父类实例化完成后，才完成它自己的实例化过程的。下面我们就来看`AnnotationConfigServletWebServerApplicationContext`的初始化流程。

#### createApplicationContext

在`debug`的过程中，我发现 `BeanFactory`在容器被创建后就已经被初始化，这也就是说`BeanFactory`其实是在`spring boot`容器创建过程中被初始化的，所以我们今天主要就是研究容器创建过程，也就是`createApplicationContext()`方法：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210905162244.png)

关于`createApplicationContext`这个方法，我们前面已经展示过了，它的作用就是通过反射创建容器实例：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210905163221.png)

#### AnnotationConfigServletWebServerApplicationContext实例化

通过跟踪代码，最终可以确认，调用的是`AnnotationConfigServletWebServerApplicationContext`无参构造方法：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210905163442.png)

所以下面就是对`AnnotationConfigServletWebServerApplicationContext`的实例化，由于容器这块继承关系比较复杂，所以实例化顺序也比较复杂。

##### 容器实例化

虽然各位小伙伴可能很清楚`java`对象实例化过程，但是我觉得还是有必要再补充说明下。在有继承关系的`java`对象实例化过程中，如果当前类继承了父类，在实例化当前类时，先要调用父类的无参构造方法（就算不指定，也会隐式调用）。所以，在这里初始`AnnotationConfigServletWebServerApplicationContext`时，会先调用它的父类无参构造方法，下面是`AnnotationConfigServletWebServerApplicationContext`的继承关系，看起来确实很复杂：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/diagram.png)

在跟踪代码的过程中，最终我确认`BeanFactory`是在`GenericApplicationContext`的无参构造方法中完成初始化的，也就是`AnnotationConfigServletWebServerApplicationContext`父类的父类的父类：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210905165410.png)

所以初始化的过程就是，`AnnotationConfigServletWebServerApplicationContext`的无参构造方法中先调用`ServletWebServerApplicationContext`的无参构造方法，`ServletWebServerApplicationContext`的无参构造方法中先调用`GenericWebApplicationContext`的无参构造方法，`GenericWebApplicationContext`的无参构造方法先调用`GenericApplicationContext`的无参构造方法（无限套娃）……

##### 知识扩展

后续的调用这里就直接省略了，因为他们和`BeanFactory`没有关系，而且因为继承关系过于复杂，所以这里我们要尽可能简单。在这里所有的初始化操作中，调用父类构造方法始终是首先被执行的，也必须首先被执行（首先调用父类的无参构造方法），这也就是为什么我们在写类的有参构造方法的时候，如果父类没有无参构造方法时，必须显式调用父类有参构造方法，且必须放在第一行的原因：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210905171741.png)

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/image-20210905171806764.png)

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210905171852.png)

### 总结

截止到今天，我们已经梳理清楚`beanFactory`的两块内容，一个是`beanDefinitionNames`和`beanDefinitionMap`，他们都是`beanFactory`的核心属性，另一块就是我们今天的`BeanFactory`的初始化，下一步应该还是会进一步深挖`beanFactory`的相关知识点，因为从一开始我的想法就是要找到`spring boot`包扫描和实例化`bean`的相关逻辑，但到目前为止还没有理清楚这一块的逻辑和流程，不过我相信很快我们就能完成这个目标了，因为我们的每一步都在更靠近目标……