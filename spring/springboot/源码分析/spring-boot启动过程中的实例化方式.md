# spring-boot启动过程中的实例化方式

### 前言

最近一直在肝`spring boot`的源码，这么久了真的感觉挺上头的，不过昨天总算是结束了这个漫长的过程，所以从今天开始我们的内容会稍微轻松一点，然后内容上也会更丰富一些。

但是由于之前的分享过程中还有一些遗漏和缺失，因此近期还是会在之前的基础上做一些补充，当然也会有一些总结的内容，今天我们来看下`spring boot`启动过程中的集中实例化方式，也算是对`spring boot`实例化这块的一个简单梳理和总结。

### 实例化方式

根据最近一段事件对`spring boot`启动过程的研究和摸索，我发现`spring boot`常用的实例化方式主要有四种，一种是通过`newInstance`的方式，第二种是`new`的方式，这种主要是初始化某些组件的属性，第三种是`supplier`，这种方式就比较高级了，我也是最近才发现这种方式，最后一种就是工厂方法，这种方式是最古老的实例化方法，当然也在`spring boot`的初始化过程频繁出现。

下面我们就分别展开分享下这几种实例化方式。

#### newInstance

这种方式好多小伙伴都知道，也特别常用，很多小伙伴第一次接触就是在`java`调用`mySql`驱动的时候，首先是通过`Class.forName`拿到类的`class`，然后通过`class`的`newInstance`方法构建类的实例：

```java
try {
    Class<?> contextClass = Class.forName("java.lang.String");
    String str = (String)contextClass.newInstance();
} catch (ClassNotFoundException e) {
    e.printStackTrace();
} catch (InstantiationException e) {
    e.printStackTrace();
} catch (IllegalAccessException e) {
    e.printStackTrace();
}
```

这里最典型的就是`spring boot`在创建容器实例的时候，当然`spring boot`的实例化要比我这里写的高级，它是调用`class`的构造方法进行实例化的，是可以指定参数的，我这里演示的调用的是无参构造方法：

![](https://gitee.com/sysker/picBed/raw/master/20210914221328.png)

![](https://gitee.com/sysker/picBed/raw/master/20210914221417.png)

![](https://gitee.com/sysker/picBed/raw/master/20210914221254.png)



#### new

这种方式在`spring boot`初始化过程中也经常出现，通常是在初始化相关组件的属性的时候。

![](https://gitee.com/sysker/picBed/raw/master/20210914221804.png)

![](https://gitee.com/sysker/picBed/raw/master/20210914221620.png)

这种方式就不需要过多解释了，我们通常情况下都是通过`new`的方式实例化对象的。



#### supplier

这种方式相比前面两种，要高级一点，首先是它比较新，是`jdk 1.8`引入的新功能，在使用方面也很简单：
![](https://gitee.com/sysker/picBed/raw/master/20210914223046.png)

和前面两种初始化比起来，它更灵活，下面我们看下关于它的示例：

```java
 Supplier<String> stringSupplier = String::new;
 String s = stringSupplier.get();
```

从形式上看，它其实是基于`lambda`实现的，也就是我们常说的函数式编程，看起来也很简洁。

其中第一行定义了初始化要调用的方法，这时并没有进行实例化，当你执行第二行的`get`操作时，这时候开始实例化。

这种方式在`spring boot`的初始化过程中出现频率也很高，但是由于其本身比较隐晦，所以很难发现。

下面就是`spring boot`中使用`supplier`这种方式的几个方法，可以看到全部都是在注册`bean`的时候调用的：

![](https://gitee.com/sysker/picBed/raw/master/20210914222914.png)

![](https://gitee.com/sysker/picBed/raw/master/images/20210914133038.png)

这些方法都是在`spring 5.0`以后引入的，这可能也是我没有找到`spring boot`集中实例化对象然后再注入容器的相关代码的原因。

`bean`的`supplier`通常被绑定在其`BeanDefainition`信息下的`instanceSupplier`属性下：

![](https://gitee.com/sysker/picBed/raw/master/20210914224352.png)

比如下面这个注册`BeanDefinitionRegistry`的方法就是通过这种方式将`supplier`注入`beanDefinition`中的

```java
private void register(BeanDefinitionRegistry registry) {
            BeanDefinition definition = BeanDefinitionBuilder.genericBeanDefinition(SharedMetadataReaderFactoryContextInitializer.SharedMetadataReaderFactoryBean.class, SharedMetadataReaderFactoryContextInitializer.SharedMetadataReaderFactoryBean::new).getBeanDefinition();
            registry.registerBeanDefinition("org.springframework.boot.autoconfigure.internalCachingMetadataReaderFactory", definition);
        }
```

这样在注册`bean`的时候，只需要执行的`BeanDefainition`下`instanceSupplier`方法即可获取该对象的实例，确实要比前两种更灵活。

#### 工厂方法

这种方式虽然存在，但是不太好找，所以这里就不展示了，但是在`beanDefinition`信息中我们看到了`factoryMethodName`，这个就是`bean`的工厂方法名称：
![](https://gitee.com/sysker/picBed/raw/master/20210914230344.png)

### 总结

好了，关于`spring boot`的四种初始化方式我们就先说这么多，这里需要特别关注的是第三种方式，算是一个比较新的知识点。

另外，关于工厂方法确实在`spring boot`现在的源码中不好找，后面看情况，如果有幸被我遇到了，我们到时候再来分享。

好了，各位小伙伴晚安吧！
