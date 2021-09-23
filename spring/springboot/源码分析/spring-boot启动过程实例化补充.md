# spring-boot启动过程实例化补充



上一次我们在分析`spring boot`启动过程实例化方式的时候，关于工厂方法没有做过多说明，一方面是我确实当时不太清楚，另一方面在`spring boot`的启动流程中，我们并没有找到相关代码，所以最后就一笔带过了。

由于最近这两天把`spring boot`之前提出的示例`demo`已经分享完了，最近也正苦于没有学习目标，因此呢，今天我们就来详细看下`spring boot`的工厂实例化方式。

我们今天不在从启动流程入手，我们换个思路，直接从`@Bean`注解入手，看下`@Bean`注解的方法到底是如何被处理的，以及它是何时被处理的。



![](https://gitee.com/sysker/picBed/raw/master/blog/20210923084335.png)



![](https://gitee.com/sysker/picBed/raw/master/blog/20210923084430.png)