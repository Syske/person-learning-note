# RPC框架之dubbo简单入门

### 前言

现阶段，`web`后端开发主流的接口协议类型主要有两种，一种就是我们传统的`rest`接口，另一种比较流行的就是`rpc`，今天我们就来简单说下`rpc`接口，同时我们会通过一个简单示例，来分享`dubbo`框架的基本用法。

`rpc`全称`Remote Procedure Call`，中文的意思是远程程序调用。简单来说，`rpc`就是一种基于`socket`的调用方式，一种有别于`rest`的调用协议。其核心技术就是动态代理，关于`rpc`动态代理的实现，我们前面其实有写过一个简易版的`rpc`接口，有兴趣的小伙伴可以去看下：



下面是`rpc`的调用原理，这里放上百度百科的一张图片，供大家参考：

![](https://gitee.com/sysker/picBed/raw/master/images/20210616082500.png)

好了，关于`rpc`的理论介绍，我们先说这么多，下面我们通过一个实例来分享下`dubbo`的简答用法。

### dubbo

我相信很多小伙伴经常在实际开发过程中有用到`rpc`，但是对于`rpc`的相关知识，很多小伙伴肯定没有系统学习过（当然也包括我），因为我们在实际工作中，大部分的时间都花在了业务实现方面，很少有机会能真正参与系统架构的搭建，所以很多时候这些知识就显得不那么重要了。

但是考虑到未来个人职业发展，同时也为了让我们在日常工作中更快地解决各类`rpc`的相关问题，掌握一些`rpc`的基础知识就尤为重要了，所以从今天开始，我们开始系统地探讨下`rpc`的相关知识，下面我们先从一个简单的`dubbo`实例开始。

关于`dubbo`我想大家应该都比较熟悉了，就算实际工作没有用到，在面试的过程中也一定听过。`dubbo`是`alibaba`开源的一款`rpc`服务框架，被各大公司广泛应用，现在也算是`java`开发必学的`web`开发框架之一，目前最新版本是`3.0`。想要了解更多信息，可以去官方网站看下：

```
https://dubbo.apache.org/zh/
```

![](https://gitee.com/sysker/picBed/raw/master/20210811082136.png)

#### 创建项目

首先我们要创建一个`spring boot`项目，然后引入`dubbo`的依赖。



服务提供者

```xml
<bean id="demoService" class="org.apache.dubbo.samples.basic.impl.DemoServiceImpl"/>

<dubbo:service interface="org.apache.dubbo.samples.basic.api.DemoService" ref="demoService"/>
```



消费者

```xml
<dubbo:reference id="demoService" check="true" interface="org.apache.dubbo.samples.basic.api.DemoService"/>
```



### 总结