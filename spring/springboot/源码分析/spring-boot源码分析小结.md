# spring-boot源码分析小结

最近一个月，我们一直在剖析`spring boot`源码的相关内容，截止到目前，我已经把能够分享的内容都基本上分享完了，是时候该做一次小结了。当然，`spring boot`的相关内容还是比较多的，我们目前分享的内容都算不上冰山一角，所以今天不仅算是小结，也算是一次反思。

开始之前，我们先来回顾下在最开始画的`run`方法执行流程，我们后面开展的内容也基本上都是围绕这整个流程开展的：

![](https://gitee.com/sysker/picBed/raw/master/images/run方法运行时序图.svg)

第一块是关于`spring boot`的`run`方法展开的

- 从代码层面看`spring boot`启动过程

  比较浅显地剖析了`run`方法的运行流程，也就是我们上面展示的启动流程的文字描述版。

  ![](https://gitee.com/sysker/picBed/raw/master/blog/face-img-8819ef8d05b144fcb923c2a8a26a7dae.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420639&idx=1&sn=63349378ae68e26512564acd7a199dc9&chksm=bea6df9589d1568371a55c7ab93f14f032639224f61e46c55bdd341914a9aeb3bd06c42a1048&token=202015350&lang=zh_CN#rd

- `spring-boot`启动过程源码分析 · 贰

  纠正了关于`SpringBootExceptionReporter`内容的谬误，同时补充了`spring boot`异常分析和处理方面的相关内容。

  ![](https://gitee.com/sysker/picBed/raw/master/blog/face-img-a6dc65f21dea4be9b9e5e067cec319d4.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420661&idx=1&sn=7c607f2acc6de2cddeba693306caa0a6&chksm=bea6dfbf89d156a9e07de28246d6c734d73db81bc798c6a5cc1c6c67f5a1a8c3ff126672db16#rd

- `spring-boot`源码分析之`ConfigurableApplicationContext`

  `ConfigurableApplicationContext`是所有容器（上下文）的基类，这篇内容主要剖析了它的基本属性和常用的方法

  ![](https://gitee.com/sysker/picBed/raw/master/blog/face-img-a5c342044e8d46c9bf6df180c6777553.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420687&idx=1&sn=05093d800e430f250a3bd4b866ad9aa0&chksm=bea6dfc589d156d3871d7e5a3aa7975ca453a348120cd5e969b7425bcb3aedad6640a0273f7f&token=202015350&lang=zh_CN#rd

- `spring-boot`源码分析之`beanDefinitionNames `· 壹

  `beanDefinitionNames`是`beanFactory`的一个成员变量，它是存放`beanFactory`中所有`bean`的定义名的，这篇内容主要剖析了`beanDefinitionNames`，同时也补充了`spring boot`容器的初始化内容。（现在再看当时写的内容，我感觉写的确实太粗了）

  ![](https://gitee.com/sysker/picBed/raw/master/blog/face-img-ab4142cb248c42fdb3c3fd8fc01e7dce.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420725&idx=1&sn=3c720ee98c97b22f7a276ab754886701&chksm=bea6dfff89d156e947c7e4f5854750585683551044db0c2f5f2ca6090b1794020f7ddd1e9c89&token=202015350&lang=zh_CN#rd

  

第二块是关于`beanFactory`的初始化展开的

- `spring-boot`源码分析之`BeanFactory `· 壹

  主要围绕容器的`refresh`方法（抽象父类`AbstractApplicationContext`）简单剖析了其内部方法的作用，同时对`beanDefinitionNames`也有一些补充说明。

  

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420757&idx=1&sn=2f85da10f233b8e7030a19c943cbe5a2&chksm=bea6df1f89d156095f778a206df399b6d381a04bd4b00aeb3cd2428a35be08b96c386dc91618#rd



- `spring-boot`源码分析之`BeanFactory `· 贰

  主要围绕`BeanFactory`的初始化过程，更详细地剖析了容器实例化过程，最后我们也确定了，`BeanFactory`是在容器创建地时候，就已经被初始化的。

  

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420794&idx=1&sn=6994c458f44444718afecb514257c726&chksm=bea6df3089d15626523e7b9df5c0471a2226685926004f5a406a430a8e356e813e0c79abdac9#rd

  

- `spring-boot`源码分析之`BeanFactory `· 叁

  围绕`BeanFactory`初始化过程，剖析了`ApplicationContextInitializer`、`ignoredDependencyInterfaces`和`beanDefinitionMap`的相关内容。

  

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420823&idx=1&sn=80352a8c4287354ba1372dec559073cd&chksm=bea6df5d89d1564b3399ac96dac7ed870fc1df7e7bb921f6d7d1b0edfb709adb6bd66a96db50#rd

  

- `spring-boot`源码分析之`beanFactory `· 肆

  这篇内容主要围绕`prepareContext`方法展开，当然也是依托于`BeanFactory`的初始化过程，毕竟`spring boot`的初始化其实就是`beanFactory`的初始化。全篇详细剖析了`prepareContext`方法内部调用过程，以及相关操作的作用。

  

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420847&idx=1&sn=ce5588d59f92b36809be8a26abb7cc61&chksm=bea6df6589d15673a08e7967dbc88e316b6f176c9a222f1ee7eb1ee931ffb7e44990682501ef#rd

  

- `spring-boot`源码分析之`beanFactory` · 伍

  这里依然是`prepareContext`的相关内容，由于`prepareContext`的内容比较多，所以分了两次。

  

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420874&idx=1&sn=6ebe69fb0e0c08f62e229ce7769ab9fd&chksm=bea6dc8089d15596523c27ac5f84f38edddceac94e9f215c631e96162960af269d09250188c1#rd

- `spring-boot`源码分析之`BeanFactory` · 陆

  这篇主要分析了`refreshContext`，但由于整个方法内容比较多，所以这一篇实际上就只分析了它内部的`prepareRefresh`方法

  

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420899&idx=1&sn=f598dcdb374b466b49be240e34b5e8e2&chksm=bea6dca989d155bf7d9eb074c209622a1e6045e5d5f6b414d732afe32ada32032922c93909f6#rd

  

- `spring-boot`源码分析之`BeanFactory` · 柒

  这篇也是围绕着`refreshContext`展开的，主要分析了它内部的三个方法：`obtainFreshBeanFactory`、`prepareBeanFactory`和`postProcessBeanFactory`，这三个方法从名字是就可以看出来和`BeanFactory`相关。

  

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420915&idx=1&sn=a57291e5dd46ec9588f832734c566651&chksm=bea6dcb989d155af668e70f568e9d12f1945600c98d23c9104c869ed4ba8dd6e7a51aae3e4c3#rd

  

- `spring-boot`源码分析之`beanFactory` · 捌

  这篇也是围绕着`refreshContext`展开的，主要分析了它内部的四个方法：

  - `invokeBeanFactoryPostProcessors`：调用前面注册的`beanFactory`后置处理器
  - `registerBeanPostProcessors`：注册`bean`后置处理器
  - `initMessageSource`：初始化消息资源
  - `initApplicationEventMulticaster`：初始化容器事件广播（`multicaster`多播器）

  

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420938&idx=1&sn=50e9c05c6da1ce6e9addb037ea7aed9d&chksm=bea6dcc089d155d6bb7a66440b5500099e6984deaa7fa1e139a8023c4fcc4fe130c7dc5f2b60#rd

  

- `spring-boot`源码分析之`beanFactory` · 玖

  这篇也是围绕着`refreshContext`展开的，主要分析了它内部的四个方法：`onRefresh`、`registerListeners`、`finishBeanFactoryInitialization`和`finishRefresh`

  

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420962&idx=1&sn=b9e35efb3acb3d5ad4b480090481cd96&chksm=bea6dce889d155fe3c4e952cad11f65847f790dc9032b811d278927628bb41788d59f0e3df44#rd

  

- `spring-boot`源码分析之`beanFactory` · 拾

  这篇也是围绕着`refreshContext`展开的，主要分析了它内部的最后三个方法：`destroyBeans`、`cancelRefresh`和`resetCommonCaches`

  

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420987&idx=1&sn=b802f58ec64ef5277f615e5f4ad65b7f&chksm=bea6dcf189d155e702539884c647c93f4473d3d1122f13f5244c6cd2c4f993d1a604ac824f58#rd



第三块是`spring boot`的几种实例化方式的剖析

- `spring-boot`启动过程中的实例化方式

  这篇主要分析了`spring boot`容器启动过程中的几种实例化方式，包括`newInstance`、`new`、`supplier`以及工厂方法

  

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648421011&idx=1&sn=2f76cd689ad812dc325b61f2b8744227&chksm=bea6dc1989d1550ff8d8202a14e2eb9eabd820e052b00efaad5d9cd31b9331acd8e5cd910f22#rd

- `spring-boot`启动过程实例化补充——关于`@Bean`

  这篇算是对工厂方法的补充，围绕`@Bean`分析了它的工作原理

  

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648421198&idx=1&sn=6988d2b6ebc4a70cebe5daa186768d7d&chksm=bea6ddc489d154d2ce6892d562801db8bfc10b15d004953fa1856b0e3a222fe7f8972d974b11#rd



第四块是一些实战`demo`分享

- `spring-boot`自定义容器初始化组件

  这一篇主要演示了自定义`ApplicationContextInitializer`组件的用法

  

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648421046&idx=1&sn=bbde39303859fd511b146e7e54973e6d&chksm=bea6dc3c89d1552a15c9aff52ae7e0f287083baefb7fd2473c23abf3cc053c580cb121e99c46#rd

  

- `Spring boot`进阶回顾，然后我悟了……

  这一篇主要回顾了`ConversionService`之前的知识点，在回顾过程中，发现了`ConversionService`潜在的知识点。当然也包括其他`spring boot`进阶内容。

  

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648421072&idx=1&sn=e746506407db968dea9e3a3d7ad19e0e&chksm=bea6dc5a89d1554c0d0fc4d14852b3f8ea273458902f5fc5bd99a03248286763c2518f7e8bf2#rd

  

- `spring-boot`转换服务组件剖析

  这一篇本来是对`ConversionService`内容的剖析，由于前一天内容回顾（`Spring boot`进阶回顾，然后我悟了……），让这一篇内容更容易懂

  

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648421099&idx=1&sn=4173879df8afe8ca816c2169f76dfc4b&chksm=bea6dc6189d15577ce2f2d629e9a9ae0763203fff91ca8f577e72e470c67e26c30c248fad4e0#rd

  

- `spring-boot`转换服务`ConversionService`二次剖析

  这一篇是对`ConversionService`的补充，主要剖析了`ConversionService`的初始化过程。

  

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648421115&idx=1&sn=e197105c5bc6495cee42de6c8accca1a&chksm=bea6dc7189d15567374feb17c1a8012e8b6d35c4d430a7b43e50a9e3d3eb837f578ca43b8b72#rd

  

- `spring-boot`条件配置——`conditionContext`

  这一篇主要剖析了条件配置的相关内容，其中包括了演示内容。

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648421178&idx=1&sn=1fed3dcbfa0398b85fa7a696b15e466a&chksm=bea6ddb089d154a65bedd06d2a6bedec1dd3a8873981e3065747a35a85c92ff9a8150f721443#rd



经过这两天的思考，目前对于未来的学习目标，有了一些想法，关于后续的内容分享，我目前想到以下几个方向：

- 设计模式相关的内容。在看源码的过程中，我确实可以很清楚地发现这一点，而且这块能力的提升，可以有效提升编程能力，让我们程序设计更合理，写的代码更少。
- 继续深挖源码，期间会根据情况做一些实战的`demo`或者其他内容的延申，比如`tomcat`的源码，`mybatis`的源码，`dubbo`的源码