# Dubbo回顾总结
tags: [#rpc, #dubbo]

### 前言

最近一段时间，我们一直在分享`dubbo`相关的知识点，从最开始的入门配置、依赖，到后面的集群负载，我们都有不同程度的涉猎，当然还有很多的内容没有分享，但是这其中绝大多数都是我觉得参考官方文档很容易自己完成的，所以也就没有深入展开，而且我分享内容的原则是，首先要自己愿意分享，其次分享的内容必须有价值，因此我觉得`dubbo`的相关知识点我应该做一个简单的总结，然后剩余的内容，交给大家自己去学习，这样我也算是抛砖引玉了。

### 回顾总结

开始之前，我们先看下`dubbo`的架构原理图：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210819083948.png)

从这张原理图，我们可以看出`dubbo`的启动过程、调用过程，以及整体的架构：

- 启动服务提供者（包括`rpc`容器启动）；

- 服务提供者注册至注册中心；
- 服务消费者订阅服务
- 注册中心通知消费者订阅结果
- 消费者发起`rpc`调用
- 消费者和提供者分别向监控中心发送心跳数据

这里需要提一点的是，`dubbo`官方其实为我们默认提供了一个`container`容器，这个容器是可以独立运行的，官方为我们默认提供了三种容器的实现，包括`springContainer`、`LogbackCOntainer`和`Log4jContainer`

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210819085843.png)

其中`springContainer`默认会加载`classpath*:META-INF/spring/*.xml`，也就是说只要我们把`dubbo`相关配置放在这个路径下，我们是可以直接通过`dubbo`自己的容器启动的，而不需要借助第三方容器，而且官方默认为我们指定的就是`springContainer`。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210819090040.png)

好了，关于容器我们就说这么多，有兴趣的小伙伴可以深入了解下。

### 内容小结

本次`dubbo`的知识总结我们主要通过一张脑图展开，详细的知识点可以参考我们之前分享的内容，同时对于我们没有分享到的知识点，各位小伙伴可以参考官方文档。脑图获取方式：公众号回复【dubbo脑图】即可获取源文件。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210819133334.png)

下面是所有`dubbo`的知识点索引，大家可以按照下面的索引，对相关知识点进行回顾：

#### 依赖

##### 核心依赖

- dubbo

##### 注册中心

- zk
- nacos
- Redis
- Simple
- Multicast

#### 配置

##### 注册配置

- RegistryConfig

##### 应用配置

- ApplicationConfig

##### 协议配置

- ProtocolConfig

##### 监控配置

- MonitorConfig

##### 提供者配置

- ProviderConfig

##### 消费者配置

- ConsumerConfig

##### 配置中心配置

- ConfigCenterBean

##### 元数据配置

- MetadataReportConfig

##### 监测配置

- MetricsConfig

##### ssl配置

- SslConfig

##### 模块配置

- ModuleConfig

#### 进阶用法

##### 常用操作

- 启动时检查
- 集群容错
- 负载均衡
- 服务降级
- 参数验证

##### 开发测试常用

- 直连提供者
- 只订阅
- 回声测试
- 只注册

##### 线程相关

- 线程模型
- 异步执行
- 异步调用
- 并发控制
- 消费端线程池模型

##### 配置相关

- 多协议
- 服务分组
- 多版本
- 配置规则
- 注册信息简化

##### 缓存

- 结果缓存
- ReferenceConfig缓存

##### 控制管理

- 连接控制
- 延迟暴漏
- 延迟连接
- 分组聚合
- 静态服务

##### 回调

- 参数回调
- 事件通知

##### 安全

- TLS
- 令牌验证
- 分布式事务

##### 运维相关

- 路由规则
- 优雅停机
- 日志适配
- 访问日志
- 导出线程堆栈
- 主机绑定
- 主机配置

##### 其他

- 服务容器
- Netty4支持
- Kryo 和 FST 序列化
- Protobuf 与 Interface 对比
- 泛化调用
- Protobuf
- 上下文信息
- 隐式参数
- 本地存根
- 本地伪装

#### 基本原理

- 服务提供者（容器）

- 服务消费者

- 注册中心

- 监控中心

- SPI扩展

#### 协议扩展

- 调用拦截扩展

- 引用监听扩展

- 暴露监听扩展

- 集群扩展

- 路由扩展

- 负载均衡扩展

- 合并结果扩展

- 注册中心扩展

- 监控中心扩展

- 扩展点加载扩展

- 动态代理扩展

- 编译器扩展

- 配置中心扩展

- 消息派发扩展

- 线程池扩展

- 序列化扩展

- 网络传输扩展

- 信息交换扩展

- 组网扩展

- Telnet 命令扩展

- 状态检查扩展

- 容器扩展

- 缓存扩展

- 验证扩展

- 日志适配扩展

#### 协议

##### dubbo 协议

- dubbo:// 协议参考手册

##### http 协议

- http:// 协议参考手册

##### hessian 协议

- hessian:// 协议参考手册

##### redis 协议

- redis:// 协议参考手册

##### thrift 协议

- thrift:// 协议参考手册

##### gRPC 协议

- grpc:// 协议参考手册

##### memcached 协议

- memcached:// 协议参考手册

##### rmi 协议

- rmi:// 协议参考手册

##### webservice 协议

- webservice:// 协议参考手册

##### Triple 协议

- Triple 协议使用

##### 开发 REST 应用

- 在 Dubbo 中开发 REST 风格的远程调用



### 总结

`dubbo`相对而言，是一个比较容易上手的`rpc`框架，但是想要真正吃透`dubbo`，你也是要狠下功夫的，一方面`dubbo`如此流行，自然有其优秀之处，这优秀之处自然是值得我们每一个新生代码农学习的；另外一方面，`dubbo`整个生态体系是特别庞大的，不仅兼容我们常见的注册中心、`spring boot`、`spring cloud`、`k8s`等主流框架及技术，同时在性能方面也是特别优秀；当然，还有一个比较现实的问题，我们在找工作的面试的时候，不仅要求要会用框架，更要了解框架内部的工作原理和流程，这就要求我们对`dubbo`有更深入的了解和认知，不然很难在众多候选人中脱颖而出。

最后，我想说的是，学习这件事，看别人的输出成果，和自己动手去实践验证，收获是有天壤之别的。

很多时候，我们看别人东西的时候，总觉得很容易、不难，但是到自己真正动手去做的时候，却又不知所措，本质上还是因为你没有踩坑，你没有跌倒，没有积累和成长的过程，而这些恰恰是别人输出成果之外的东西，这些别人无法教给你，你也学不会，换句话说，你只有自己去踩坑，去解决问题，你才能更快成长，因为思维的顿悟，是没有人可以帮你的。

写一万行代码，和写一百万行代码的人，他比你多的是不仅仅是代码的数量，而是九十九万行代码的实践体验和思维蜕变，实践的终极目标是让你看清问题的本质，而这才是提升效率的关键。