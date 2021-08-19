# Dubbo回顾总结

### 前言



### 回顾总结

开始之前，我们先看下`dubbo`的架构原理图：

![](https://gitee.com/sysker/picBed/raw/master/20210819083948.png)

从这张原理图，我们可以看出`dubbo`的启动过程、调用过程，以及整体的架构：

- 启动服务提供者（包括`rpc`容器启动）；

- 服务提供者注册至注册中心；
- 服务消费者订阅服务
- 注册中心通知消费者订阅结果
- 消费者发起`rpc`调用
- 消费者和提供者分别向监控中心发送心跳数据

这里需要提一点的是，`dubbo`官方其实为我们默认提供了一个`container`容器，这个容器是可以独立运行的，官方为我们默认提供了三种容器的实现，包括`springContainer`、`LogbackCOntainer`和`Log4jContainer`

![](https://gitee.com/sysker/picBed/raw/master/20210819085843.png)

其中`springContainer`默认会加载`classpath*:META-INF/spring/*.xml`，也就是说只要我们把`dubbo`相关配置放在这个路径下，我们是可以直接通过`dubbo`自己的容器启动的，而不需要借助第三方容器，而且官方默认为我们指定的就是`springContainer`。

![](https://gitee.com/sysker/picBed/raw/master/20210819090040.png)

好了，关于容器我们就说这么多，有兴趣的小伙伴可以深入了解下。