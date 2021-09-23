# spring-boot启动过程实例化补充



上一次我们在分析`spring boot`启动过程实例化方式的时候，关于工厂方法没有做过多说明，一方面是我确实当时不太清楚，另一方面在`spring boot`的启动流程中，我们并没有找到相关代码，所以最后就一笔带过了。

由于最近这两天把`spring boot`之前提出的示例`demo`已经分享完了，最近也正苦于没有学习目标，因此呢，今天我们就来详细看下`spring boot`的工厂实例化方式。

我们今天不在从启动流程入手，我们换个思路，直接从`@Bean`注解入手，看下`@Bean`注解的方法到底是如何被处理的，以及它是何时被处理的。



### @Bean注解

首先我搜索了全局有用到`Bean.class`的地方，找到以下结果：

![](https://gitee.com/sysker/picBed/raw/master/images/20210923132356.png)

总共找到`10`条记录，其中前两条和我们昨天分享的条件配置有关，主要是判断方法是否存在`@Bean`注解，但是这里并不进行实例化操作，所以我们这里就不深入研究了；

第三行、第四行是获取所有包含`@Bean`注解的方法的元数据，但是由于这个类是和异常报告相关的（`NoSuchBeanDefinitionFailureAnalyzer`，从名字可以看出来是个失败分析器，找不到`bean`的定义信息时触发），所以我们也不做过多说明。不过从调用的方法名来看，这个方法的作用是获取所有的`beanMethod`：
![](https://gitee.com/sysker/picBed/raw/master/images/20210923134626.png)



![](https://gitee.com/sysker/picBed/raw/master/blog/20210923084335.png)



![](https://gitee.com/sysker/picBed/raw/master/blog/20210923084430.png)