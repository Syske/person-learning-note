# spring-boot源码分析之ConfigurableApplicationContext

### 前言



### ConfigurableApplicationContext

`ConfigurableApplicationContext`就是我们`spring-boot`最核心的内容——应用容器，`run`内部也基本都是针对它进行的各种初始化操作，运行完成后返回的也是它，所以今天我们就来看下这个`spring boot`的主角。

`ConfigurableApplicationContext`是一个基础接口，它是`03.11.2003`引入的（好早呀），内部包括`7`个静态常量，`13`给接口方法，同时它还继承了`ApplicationContext`、`Lifecycle`和`Closeable`。

`ApplicationContext`是所有容器的基类，`spring boot`提供了很多容器的实现，这里我们目前只看默认的容器；`Lifecycle`是和类生命周期有关的接口，它的内部提供了三个方法，`start`、`stop`和`isRunning`

#### 静态常量

- ```
  CONFIG_LOCATION_DELIMITERS
  ```



### 总结

