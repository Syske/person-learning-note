# spring-boot源码分析之beanFactory · 捌

### 前言

今天，多余的话就不说了，按照原计划往下啃就行了，因为内容确实多，废话多了怕分享不完。

我们今天要分享四个方法：

- `invokeBeanFactoryPostProcessors`：调用前面注册的`beanFactory`后置处理器
- `registerBeanPostProcessors`：注册`bean`后置处理器
- `initMessageSource`：初始化消息资源
- `initApplicationEventMulticaster`：初始化容器事件广播（`multicaster`多播器）

下面我们就逐一展开讲下这四个方法。

### refresh方法

#### invokeBeanFactoryPostProcessors

我们先看调用过程，在`invokeBeanFactoryPostProcessors`主要有两部分操作。

一部分就是调用`PostProcessorRegistrationDelegate`类的静态方法`invokeBeanFactoryPostProcessors`方法，这个方法内容有点多，我们等下展开讲；

另一部分操作是往`beanFactory`中添加了`LoadTimeWeaverAwareProcessor`处理器，从名字可以看出这个处理器和切面编程有关，同时包含了`loadTime`，说明它和加载时间有关系，应该是统计资源或者类的加载时间的的切面处理器，这里还往容器中`set`了一个临时类加载器。

![](https://gitee.com/sysker/picBed/raw/master/images/image-20210911145730753.png)

下面我们展开看下静态处理方法`invokeBeanFactoryPostProcessors`。下面是这个方法的完整代码：

![](https://gitee.com/sysker/picBed/raw/master/images/Snipaste_2021-09-11_20-12-04.jpg)

##### part1

先看`part1`的内容。

在`invokeBeanFactoryPostProcessors`方法内部，先循环`beanFactoryPostProcessors`，然后根据其类型，分别放进`beanFactory`和`beanDefinitonRegistry`后置容器中，前一种和`beanFactory`相关的处理器，后一种是和这里的后置处理来源于容器，这里分类放置，是为了后期执行不同的后置处理方法。

对于`BeanDefinitionRegistryPostProcessor`类型的后置处理器，除了往容器中添加之外，还会执行`postProcessBeanDefinitionRegistry`方法，这个方法和我们昨天分享的`postProcessBeanFactory`方法很类似，方法的作用也大同小异，至少操作的对象不一样，昨天的方法针对的是`beanFactroy`，今天的这个方法针对的是`beanDefinitionRegisty`。所以这个方法的作用就是在标准初始化之后（`bean`已加载未进行实例化操作），修改`bean`的定义信息（在下次后置处理之前）。

##### part2~4

`part2~4`的大部分代码都一样，唯一的区别是`if`条件语句不一样，`part2`匹配的是继承了`PriorityOrdered`（优先顺序）的后置处理器；`part3`匹配的是继承了`Ordered`，且不在`processedBeans`（未被添加过，即不包括`part2`已经处理的）；`part4`匹配的是前两类未处理的。匹配完之后，先进行排序操作，然后再放进`registryProcessors`中，最后进行统一操作。这里还会调用`invokeBeanDefinitionRegistryPostProcessors`方法，当然实际上调用的是`BeanDefinitionRegistryPostProcessor`的`postProcessBeanDefinitionRegistry`方法，也就是我们`part1`说的方法。

再下面就是根据`bean`的类型获取`beanFactory`的`postProcessor`的名字，然后再根据`postProcessor`的名字拿出对应的`beanFactory`后置处理，放进不同的容器中，有顺序的的需要先排个序，最后执行调用`beanFactory`的`postProcessBeanFactory`，这个方法中基本上都是在进行依赖注册。

#### registerBeanPostProcessors

这个方法从名字来看，它应该是注册`bean`的后置处理器的，这里它调用的也是`PostProcessorRegistrationDelegate`静态方法，不过它调用的是`registerBeanPostProcessors`，这个静态方法内容实现还挺多的，所以我们也需要展开分析下。

![](https://gitee.com/sysker/picBed/raw/master/images/image-20210911185454382.png)

下面我们就展开这个方法讲一下，这个方法我也把它分为四个部分，我们先看`part 1`。

![](https://gitee.com/sysker/picBed/raw/master/images/Snipaste_2021-09-11_20-13-59.jpg)

##### part1

这部分就是往`beanFactory`中注入了一个`bean`的后置处理器，从名字看这个后置处理器应该是一个后置处理器的检查器，这个检测器的其中一个参数是我们`bean`后置处理器数量+`bean`后置处理器名字集合的大小+`1`。

##### part2

这一部分循环遍历了`bean`后置处理器的名字集合，然后根据名字获取`bean`的后置处理器，对于优先顺序的后置处理器会直接放进它的后置处理集合中，其他类型的后置处理器，会存放后置处理器名称，便于`part3`和`part4`进行循环操作。循环完之后，对有顺序（优先顺序）的后置处理器要进行排序操作，之后会把排序之后的后置处理器注册到`beanFactory`中。

##### part3

这里的逻辑比`part2`差不多，而且比`part2`简单，所以就不再赘述。

##### part4

`part4`比`part3`多了一步注册，因为`part4`要注册两种后置处理器，一种是内部后置处理器，一种是无序的后置处理器。

最后还往`beanFactory`中注册了一个`bean`后置处理，这个后置处理器的是应用监听器的探测器，应该就是类似于监控这样的功能，它检测的是应用的监听器。

#### initMessageSource

从名字看，这个方法进行的是消息源的初始化，我记得我们前面好像提到过，这个方法是和国际化有关的。这个方法其实就做了一件事，注册`messageSource`，如果已经被注册，则需要把注册的值赋给容器的`messageSource`属性

![](https://gitee.com/sysker/picBed/raw/master/images/image-20210911195152210.png)

#### initApplicationEventMulticaster

初始化应用事件的广播器（多播）。与消息源初始化类似，这里就是简单的注册和赋值，不存在就实例化然后注册，存在就直接赋值。

![](https://gitee.com/sysker/picBed/raw/master/images/image-20210911195430590.png)



### 总结

今天这四个方法算是比较圆满地分享完了，主要是前两个方法确实有点长，分析完之后，才发现其实内部也没有太复杂的逻辑，甚至有些简单，但是我看了下字数，感觉问题也并不简单，因为目前字数已经`1500+`了，如果照这个字数，明天四个方法很可能是分享完的，至少字数是要大大超出今天这个量的，所以如果明天真的打脸我也认了

好了，今天的四个方法就先分享到这里，胜利的曙光在望，加油呀~



