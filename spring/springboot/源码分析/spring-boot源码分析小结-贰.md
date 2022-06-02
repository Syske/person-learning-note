# spring-boot源码分析小结 · 贰

今天分享的是总结的第二部分，是关于`beanFactory`的初始化展开的

- `spring-boot`源码分析之`BeanFactory `· 壹

  主要围绕容器的`refresh`方法（抽象父类`AbstractApplicationContext`）简单剖析了其内部方法的作用，同时对`beanDefinitionNames`也有一些补充说明。

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/face-img-25d21934f4c542a29b0040ffaccc4557.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420757&idx=1&sn=2f85da10f233b8e7030a19c943cbe5a2&chksm=bea6df1f89d156095f778a206df399b6d381a04bd4b00aeb3cd2428a35be08b96c386dc91618#rd



- `spring-boot`源码分析之`BeanFactory `· 贰

  主要围绕`BeanFactory`的初始化过程，更详细地剖析了容器实例化过程，最后我们也确定了，`BeanFactory`是在容器创建地时候，就已经被初始化的。

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/face-img-6d34cb9ad0dd4e62a4082f9ad809aab6.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420794&idx=1&sn=6994c458f44444718afecb514257c726&chksm=bea6df3089d15626523e7b9df5c0471a2226685926004f5a406a430a8e356e813e0c79abdac9#rd

  

- `spring-boot`源码分析之`BeanFactory `· 叁

  围绕`BeanFactory`初始化过程，剖析了`ApplicationContextInitializer`、`ignoredDependencyInterfaces`和`beanDefinitionMap`的相关内容。

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/face-img-cac30d451b774e41a7e26efbbc65ae28.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420823&idx=1&sn=80352a8c4287354ba1372dec559073cd&chksm=bea6df5d89d1564b3399ac96dac7ed870fc1df7e7bb921f6d7d1b0edfb709adb6bd66a96db50#rd

  

- `spring-boot`源码分析之`beanFactory `· 肆

  这篇内容主要围绕`prepareContext`方法展开，当然也是依托于`BeanFactory`的初始化过程，毕竟`spring boot`的初始化其实就是`beanFactory`的初始化。全篇详细剖析了`prepareContext`方法内部调用过程，以及相关操作的作用。

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/face-img-da10b38455794c69af9695815e849b29.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420847&idx=1&sn=ce5588d59f92b36809be8a26abb7cc61&chksm=bea6df6589d15673a08e7967dbc88e316b6f176c9a222f1ee7eb1ee931ffb7e44990682501ef#rd

  

- `spring-boot`源码分析之`beanFactory` · 伍

  这里依然是`prepareContext`的相关内容，由于`prepareContext`的内容比较多，所以分了两次。

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/face-img-112776b65ba14abab7f8ce7d80fb9e7a.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420874&idx=1&sn=6ebe69fb0e0c08f62e229ce7769ab9fd&chksm=bea6dc8089d15596523c27ac5f84f38edddceac94e9f215c631e96162960af269d09250188c1#rd

  

- `spring-boot`源码分析之`BeanFactory` · 陆

  这篇主要分析了`refreshContext`，但由于整个方法内容比较多，所以这一篇实际上就只分析了它内部的`prepareRefresh`方法

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/face-img-7a3465721ace4596b37e76943c30fc99.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420899&idx=1&sn=f598dcdb374b466b49be240e34b5e8e2&chksm=bea6dca989d155bf7d9eb074c209622a1e6045e5d5f6b414d732afe32ada32032922c93909f6#rd

  

- `spring-boot`源码分析之`BeanFactory` · 柒

  这篇也是围绕着`refreshContext`展开的，主要分析了它内部的三个方法：`obtainFreshBeanFactory`、`prepareBeanFactory`和`postProcessBeanFactory`，这三个方法从名字是就可以看出来和`BeanFactory`相关。

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/face-img-452589e3116f451db52fbfe847ec8e19.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420915&idx=1&sn=a57291e5dd46ec9588f832734c566651&chksm=bea6dcb989d155af668e70f568e9d12f1945600c98d23c9104c869ed4ba8dd6e7a51aae3e4c3#rd

  

- `spring-boot`源码分析之`beanFactory` · 捌

  这篇也是围绕着`refreshContext`展开的，主要分析了它内部的四个方法：

  - `invokeBeanFactoryPostProcessors`：调用前面注册的`beanFactory`后置处理器
  - `registerBeanPostProcessors`：注册`bean`后置处理器
  - `initMessageSource`：初始化消息资源
  - `initApplicationEventMulticaster`：初始化容器事件广播（`multicaster`多播器）

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/face-img-d7251774e04848cca347e40c027fa7af.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420938&idx=1&sn=50e9c05c6da1ce6e9addb037ea7aed9d&chksm=bea6dcc089d155d6bb7a66440b5500099e6984deaa7fa1e139a8023c4fcc4fe130c7dc5f2b60#rd

  

- `spring-boot`源码分析之`beanFactory` · 玖

  这篇也是围绕着`refreshContext`展开的，主要分析了它内部的四个方法：`onRefresh`、`registerListeners`、`finishBeanFactoryInitialization`和`finishRefresh`

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/face-img-6ffe7c83f7b74b8e9b5c403d5b0d265c.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420962&idx=1&sn=b9e35efb3acb3d5ad4b480090481cd96&chksm=bea6dce889d155fe3c4e952cad11f65847f790dc9032b811d278927628bb41788d59f0e3df44#rd

  

- `spring-boot`源码分析之`beanFactory` · 拾

  这篇也是围绕着`refreshContext`展开的，主要分析了它内部的最后三个方法：`destroyBeans`、`cancelRefresh`和`resetCommonCaches`

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/face-img-234cb502f32d408195d5db2733cb47dc.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648420987&idx=1&sn=b802f58ec64ef5277f615e5f4ad65b7f&chksm=bea6dcf189d155e702539884c647c93f4473d3d1122f13f5244c6cd2c4f993d1a604ac824f58#rd

