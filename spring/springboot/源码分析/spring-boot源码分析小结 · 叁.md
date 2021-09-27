# spring-boot源码分析小结 · 叁

第三块是`spring boot`的几种实例化方式的剖析

- `spring-boot`启动过程中的实例化方式

  这篇主要分析了`spring boot`容器启动过程中的几种实例化方式，包括`newInstance`、`new`、`supplier`以及工厂方法

  ![](https://gitee.com/sysker/picBed/raw/master/blog/face-img-e01fae308318499b8e483920a3bcc126.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648421011&idx=1&sn=2f76cd689ad812dc325b61f2b8744227&chksm=bea6dc1989d1550ff8d8202a14e2eb9eabd820e052b00efaad5d9cd31b9331acd8e5cd910f22#rd

- `spring-boot`启动过程实例化补充——关于`@Bean`

  这篇算是对工厂方法的补充，围绕`@Bean`分析了它的工作原理

  ![](https://gitee.com/sysker/picBed/raw/master/blog/face-img-4d29d5a7f0904c4ea23a29ed4ff0d3f8.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648421198&idx=1&sn=6988d2b6ebc4a70cebe5daa186768d7d&chksm=bea6ddc489d154d2ce6892d562801db8bfc10b15d004953fa1856b0e3a222fe7f8972d974b11#rd



第四块是一些实战`demo`分享

- `spring-boot`自定义容器初始化组件

  这一篇主要演示了自定义`ApplicationContextInitializer`组件的用法

  ![](https://gitee.com/sysker/picBed/raw/master/blog/face-img-ae36d0f0f65d4a2cb3544920b7674e33.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648421046&idx=1&sn=bbde39303859fd511b146e7e54973e6d&chksm=bea6dc3c89d1552a15c9aff52ae7e0f287083baefb7fd2473c23abf3cc053c580cb121e99c46#rd

  

- `Spring boot`进阶回顾，然后我悟了……

  这一篇主要回顾了`ConversionService`之前的知识点，在回顾过程中，发现了`ConversionService`潜在的知识点。当然也包括其他`spring boot`进阶内容。

  ![](https://gitee.com/sysker/picBed/raw/master/blog/face-img-95ba19d5adce40be91f41c3e7fc41de2.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648421072&idx=1&sn=e746506407db968dea9e3a3d7ad19e0e&chksm=bea6dc5a89d1554c0d0fc4d14852b3f8ea273458902f5fc5bd99a03248286763c2518f7e8bf2#rd

  

- `spring-boot`转换服务组件剖析

  这一篇本来是对`ConversionService`内容的剖析，由于前一天内容回顾（`Spring boot`进阶回顾，然后我悟了……），让这一篇内容更容易懂

  ![](https://gitee.com/sysker/picBed/raw/master/blog/face-img-8ad536d26210455db5d5dbc755d78ee7.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648421099&idx=1&sn=4173879df8afe8ca816c2169f76dfc4b&chksm=bea6dc6189d15577ce2f2d629e9a9ae0763203fff91ca8f577e72e470c67e26c30c248fad4e0#rd

  

- `spring-boot`转换服务`ConversionService`二次剖析

  这一篇是对`ConversionService`的补充，主要剖析了`ConversionService`的初始化过程。

  ![](https://gitee.com/sysker/picBed/raw/master/blog/face-img-3e14089976714f4b9d0eba00ae50958f.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648421115&idx=1&sn=e197105c5bc6495cee42de6c8accca1a&chksm=bea6dc7189d15567374feb17c1a8012e8b6d35c4d430a7b43e50a9e3d3eb837f578ca43b8b72#rd

  

- `spring-boot`条件配置——`conditionContext`

  这一篇主要剖析了条件配置的相关内容，其中包括了演示内容。

  ![](https://gitee.com/sysker/picBed/raw/master/blog/face-img-5c83c0b5fa894278907cb04796f85215.jpg)

  http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648421178&idx=1&sn=1fed3dcbfa0398b85fa7a696b15e466a&chksm=bea6ddb089d154a65bedd06d2a6bedec1dd3a8873981e3065747a35a85c92ff9a8150f721443#rd

好了，到今天我们关于`spring boot`源码的内容就暂时分享完了，当然后续还是会持续关注`spring boot`相关内容，也会继续分享相关知识点的。