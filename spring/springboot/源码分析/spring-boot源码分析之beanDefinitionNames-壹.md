# spring-boot源码分析之beanDefinitionNames · 壹

### 前言

今天原本打算搞清楚`spring boot`初始化`scan`的流程的，但是在调试过程中，发现压根就没有执行`scan`方法，这个方法只有`basePackage`不为空的时候才会执行，起初我以为是需要在`@SpringBootApplication`指定包路径才可以，但是加了之后发现还是没用，所以最后就暂时放弃了：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210902205740.png)

然后我就不知道该分享什么了……

但是最后我在`debug`的时候，发现`beanFactory`有个 `beanDefinitionNames`的成员变量，它的元素数量会在`reflush`方法执行之后急剧增加，同时也有个与之对应的成员变量`beanDefinitionMap`元素数量和它一致，也是在`reflush`之后数据量增多，而且从名字也可以看出来他们和`spring bean`相关的组件，另外他们所存储的数据包含了我自己定义的服务：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210902211230.png)

所以最后我决定沿着`beanFactory`的`beanDefinitionNames`的初始化路线，看下这些数据到底是如何初始化的，希望最后能更接近`spring boot`初始化的核心秘密，于是就有了今天的内容。



### beanDefinitionNames

开始分享`beanDefinitionNames`相关知识点之前，我们先补充一个知识点——`spring boot`默认容器。从创建容器的源码我们可以看出，在不指定容器类别的情况下，`spring boot`默认为我们创建的容器是`AnnotationConfigServletWebServerApplicationContext`（在此之前，我一直以为它走的是`default`那块的代码，`debug`之后发现我理解错了），这个默认容器本身是继承了`ServletWebServerApplicationContext`，所以说默认情况下，`spring boot`为我们创建的是`servlet`容器：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210902081459.png)

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210902081545.png)

好了，默认容器的相关知识点我们先补充这么多，下面我们开始`beanDefinitionNames`的相关内容分享。

首先，我们先介绍下`beanDefinitionNames`。从上面的`debug`截图中我们其实可以看出来一些信息，`beanDefinitionNames`其实就是存放`spring boot`中`bean`的名字的，通过这个名字我们就可以从`spring boot`的容器中拿出我们`bean`的实例：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210902212728.png)

这也就是说，`beanDefinitionNames`就是`spring boot`中`IOC`容器的名单，通过这个名单我们可以找到容器中的每一个类。

关于`beanDefinitionNames`我们暂时就先说这么多，等后面分析`BeanFactory`的时候我们到时候再来补充。下面我们来看下面这张时序图：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/%E5%AE%B9%E5%99%A8%E5%88%B7%E6%96%B0%E5%90%AF%E5%8A%A8%E6%97%B6%E5%BA%8F%E5%9B%BE.svg)

时序图`svg`原图地址如下：

```

https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/%E5%AE%B9%E5%99%A8%E5%88%B7%E6%96%B0%E5%90%AF%E5%8A%A8%E6%97%B6%E5%BA%8F%E5%9B%BE.svg
```

这张时序图比较清楚地展示了`spring boot`初始化`beanFactory`的`beanDefinitionNames`的过程（`beanDefinitionMap`的初始化也是如此），但关于这张时序图我感觉我能说的很少，虽然调用过程很清晰，但我目前还没有梳理清楚各个方法的作用（初始化过程所起的作用），因为每一个方法除了我这里罗列的方法调用外，还有很多其他的操作，而且由于时间关系，今天也没有时间梳理了，目前的计划是明天把这块的内容补上，然后尽可能再多扩充一些新的知识。

### 总结

实话说，`spring boot`的源码是真的难啃，从我自己的感觉，以及产出成果来说，确实是太难了，不仅进度慢，难出成果，而且出来的东西也确实没有以前分享`demo`或者其他内容那么顺畅，现在的感觉就像是在乱石堆里挖井，挖半天下不去，自己还类的够呛，但是把，万事开头难，等所有内容都梳理的七七八八了，我相信一切都会变的顺畅起来的，所以接着啃呗！
