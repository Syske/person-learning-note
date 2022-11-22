# spring-boot源码分析小结 · 壹

### 前言

最近一个月，我们一直在剖析`spring boot`源码的相关内容，截止到目前，我已经把能够分享的内容都基本上分享完了，是时候该做一次小结了。当然，`spring boot`的相关内容还是比较多的，我们目前分享的内容都算不上冰山一角，所以今天不仅算是小结，也算是一次反思。

### 第一部分
这一部分是关于`spring boot`的`run`方法展开的，总共有四块内容。

开始之前，我们先来回顾下在最开始画的`run`方法执行流程，我们后面开展的内容也基本上都是围绕这整个流程开展的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/run方法运行时序图.svg)


- 从代码层面看`spring boot`启动过程

  比较浅显地剖析了`run`方法的运行流程，也就是我们上面展示的启动流程的文字描述版。

  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/face-img-8819ef8d05b144fcb923c2a8a26a7dae.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420639&idx=1&sn=63349378ae68e26512564acd7a199dc9&chksm=bea6df9589d1568371a55c7ab93f14f032639224f61e46c55bdd341914a9aeb3bd06c42a1048&token=202015350&lang=zh_CN#rd

- `spring-boot`启动过程源码分析 · 贰

  纠正了关于`SpringBootExceptionReporter`内容的谬误，同时补充了`spring boot`异常分析和处理方面的相关内容。

  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/face-img-a6dc65f21dea4be9b9e5e067cec319d4.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420661&idx=1&sn=7c607f2acc6de2cddeba693306caa0a6&chksm=bea6dfbf89d156a9e07de28246d6c734d73db81bc798c6a5cc1c6c67f5a1a8c3ff126672db16#rd

- `spring-boot`源码分析之`ConfigurableApplicationContext`

  `ConfigurableApplicationContext`是所有容器（上下文）的基类，这篇内容主要剖析了它的基本属性和常用的方法

  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/face-img-a5c342044e8d46c9bf6df180c6777553.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420687&idx=1&sn=05093d800e430f250a3bd4b866ad9aa0&chksm=bea6dfc589d156d3871d7e5a3aa7975ca453a348120cd5e969b7425bcb3aedad6640a0273f7f&token=202015350&lang=zh_CN#rd

- `spring-boot`源码分析之`beanDefinitionNames `· 壹

  `beanDefinitionNames`是`beanFactory`的一个成员变量，它是存放`beanFactory`中所有`bean`的定义名的，这篇内容主要剖析了`beanDefinitionNames`，同时也补充了`spring boot`容器的初始化内容。（现在再看当时写的内容，我感觉写的确实太粗了）

  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/face-img-ab4142cb248c42fdb3c3fd8fc01e7dce.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420725&idx=1&sn=3c720ee98c97b22f7a276ab754886701&chksm=bea6dfff89d156e947c7e4f5854750585683551044db0c2f5f2ca6090b1794020f7ddd1e9c89&token=202015350&lang=zh_CN#rd
  

### 后记

关于总结的内容，今天就先分享一部分，因为总共有`20`篇内容，一次分享完的话，内容确实有点多。实话，实说，如果没有今天的总结，我可能也很难搞清楚到底哪篇到底说的啥

经过这两天的思考，目前对于未来的学习目标，有了一些想法，关于后续的内容分享，我目前想到以下几个方向：

- 设计模式相关的内容。在看源码的过程中，我确实可以很清楚地发现这一点，而且这块能力的提升，可以有效提升编程能力，让我们程序设计更合理，写的代码更少。
- 继续深挖源码，期间会根据情况做一些实战的`demo`或者其他内容的延申，比如`tomcat`的源码，`mybatis`的源码，`dubbo`的源码

  