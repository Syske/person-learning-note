# dubbo其他知识点分享
tags: [#rpc, #dubbo]

### 前言

`dubbo`的相关知识点这几天我们已经分享的差不多了，剩余的知识点一方面比较零碎，单独拎出来讲的话，内容比较少，另一方面这些知识点可能在日常工作中很少用到，所以我打算今天把抽几个剩余的知识点分享下，剩余的内容，各位小伙伴可以自己去了解下，确保遇到问题的时候知道如何解决问题，知道在那查资料就行了。好了，下面让我们开始吧。

### 其他知识点

我们这里说到的知识点，都可以在`dubbo`官网的高级用法下查到，没有提到的内容，各位小伙伴自己去看下：

```
https://dubbo.apache.org/zh/docs/advanced/
```

![](https://gitee.com/sysker/picBed/raw/master/images/20210818124801.png)

#### 启动时检查

启动时检查其实是一个配置，我们可以针对某一个服务进行设置，也可以针对整个应用设置。这个设置项的作用是在启动时检查依赖的服务是否可用，默认值是`true`，如果你的服务不需要启动时检查是否可以，你可以将这个配置设置为`false`，设置的方式有三种，一种是直接加在配置文件中：

```properties
# 设置某个服务关闭检查
dubbo.reference.com.foo.BarService.check=false
# 关闭所有服务的启动时检查（没有提供者时报错）
dubbo.consumer.check=false
# 关闭注册中心启动时检查（注册订阅时报错）
dubbo.registry.check=false
```

第二种方式是在服务的注解或者`xml`配置中指定：

```xml
<dubbo:reference interface="com.foo.BarService" check="false" />
<dubbo:consumer check="false" />
<dubbo:registry check="false" />
```

注解的方式只针对消费者，而且只能对某一个服务进行设置：

```java
@DubboReference(version = "1.0", interfaceName = "demoService", check = false, interfaceClass = DemoService.class)
    private DemoService demoService;
```

第三种方式是在服务启动时候，通过`java`命令行的方式指定：

```sh
java -Ddubbo.reference.com.foo.BarService.check=false
java -Ddubbo.consumer.check=false 
java -Ddubbo.registry.check=false
```

##### 说明

`dubbo.reference.com.foo.BarService.check`，覆盖 `com.foo.BarService`的 reference 的 check 值，就算配置中有声明，也会被覆盖。

`dubbo.consumer.check=false`，是设置reference的 `check` 的缺省值，如果配置中有显式的声明，如：`<dubbo:reference check="true"/>`，不会受影响。

`dubbo.registry.check=false`，前面两个都是指订阅成功，但提供者列表是否为空是否报错，如果注册订阅失败时，也允许启动，需使用此选项，将在后台定时重试。

#### 集群容错

集群容错是针对`dubbo`服务集群提供的容错机制，集群调用失败时，`dubbo`会根据我们设定的容错方案进行容错处理，默认提供的容错方案为`failover `，顾名思义就是失败后会跳过当前服务，重新调用其他服务。

下面是官方给出的集群调用流程图：

![](https://gitee.com/sysker/picBed/raw/master/cluster.jpg)

各节点关系官方也给出了说明：

- 这里的 `Invoker` 是 `Provider` 的一个可调用 `Service` 的抽象，`Invoker` 封装了 `Provider` 地址及 `Service` 接口信息
- `Directory` 代表多个 `Invoker`，可以把它看成 `List<Invoker>` ，但与 `List` 不同的是，它的值可能是动态变化的，比如注册中心推送变更
- `Cluster` 将 `Directory` 中的多个 `Invoker` 伪装成一个 `Invoker`，对上层透明，伪装过程包含了容错逻辑，调用失败后，重试另一个
- `Router` 负责从多个 `Invoker` 中按路由规则选出子集，比如读写分离，应用隔离等
- `LoadBalance` 负责从多个 `Invoker` 中选出具体的一个用于本次调用，选的过程包含了负载均衡算法，调用失败后，需要重选

##### 容错模式

###### Failover

失败自动切换，当出现失败，重试其它服务器。通常用于读操作，但重试会带来更长延迟。可通过 `retries="2"` 来设置重试次数(不含第一次，默认`retries`的值是`2`)。所以，如果我们采用`Failover `容错的话，直接设置重试次数即可：

```xml
<dubbo:service retries="2" />
<dubbo:reference retries="2" />
<dubbo:reference>
    <dubbo:method name="findFoo" retries="2" />
</dubbo:reference>
```

或者注解方式：

```java
// 服务提供者
@DubboService(version = "1.0", interfaceName = "demoService", interfaceClass = DemoService.class,
        loadbalance = "roundrobin", retries = 4)
public class DemoServiceImpl implements DemoService {}
// 服务消费者
@DubboReference(version = "1.0", interfaceName = "demoService", retries = 4, interfaceClass = DemoService.class)
    private DemoService demoService;
```

###### Failfast

快速失败，只发起一次调用，失败立即报错。通常用于非幂等性的写操作，比如新增记录。

###### Failsafe

失败安全，出现异常时，直接忽略。通常用于写入审计日志等操作。

###### Failback

失败自动恢复，后台记录失败请求，定时重发。通常用于消息通知操作。

###### Forking

并行调用多个服务器，只要一个成功即返回。通常用于实时性要求较高的读操作，但需要浪费更多服务资源。可通过 `forks="2"` 来设置最大并行数。

###### Broadcast

广播调用所有提供者，逐个调用，任意一台报错则报错。通常用于通知所有提供者更新缓存或日志等本地资源信息。

##### 集群配置

集群配置也很简单，`xml`配置如下：

```xml
<dubbo:service cluster="failsafe" />
<dubbo:reference cluster="failsafe" />
```

注解方式：

客户端

```java
@DubboReference(version = "1.0", interfaceName = "demoService", interfaceClass = DemoService.class,
cluster =  ClusterRules.FAIL_FAST)
private DemoService demoService;
```

服务端

```java
@Service
@DubboService(version = "1.0", interfaceName = "demoService", cluster = ClusterRules.FAIL_OVER, interfaceClass = DemoService.class, loadbalance = "roundrobin")
public class DemoServiceImpl implements DemoService {}
```

#### 线程模型

线程模型主要是设置哪些应用场景需要通过线程池来完成，设置方式也很简单，但是具体的参数需要结合实际应用场景来确定：

```xml
<dubbo:protocol name="dubbo" dispatcher="all" threadpool="fixed" threads="100" />
```

配置文件

```properties
dubbo.protocol.name=dubbo
# 线程池场景
dubbo.protocol.dispatcher=all
# 线程池类别
dubbo.protocol.threadpool=fixed
# 线程名称
dubbo.protocol.threadname=dubbo-server-task
# 核心线程数
dubbo.protocol.corethreads=10
# 线程池大小（固定大小）
dubbo.protocol.threads=100
# io线程池大小（固定大小）
dubbo.protocol.iothreads=100
```

##### 线程池场景

- `all` 所有消息都派发到线程池，包括请求，响应，连接事件，断开事件，心跳等。
- `direct` 所有消息都不派发到线程池，全部在 IO 线程上直接执行。
- `message` 只有请求响应消息派发到线程池，其它连接断开事件，心跳等消息，直接在 IO 线程上执行。
- `execution` 只有请求消息派发到线程池，不含响应，响应和其它连接断开事件，心跳等消息，直接在 IO 线程上执行。
- `connection` 在 IO 线程上，将连接断开事件放入队列，有序逐个执行，其它消息派发到线程池。

##### 线程池类别

- `fixed` 固定大小线程池，启动时建立线程，不关闭，一直持有。(缺省)
- `cached` 缓存线程池，空闲一分钟自动删除，需要时重建。
- `limited` 可伸缩线程池，但池中的线程数只会增长不会收缩。只增长不收缩的目的是为了避免收缩时突然来了大流量引起的性能问题。
- `eager` 优先创建`Worker`线程池。在任务数量大于`corePoolSize`但是小于`maximumPoolSize`时，优先创建`Worker`来处理任务。当任务数量大于`maximumPoolSize`时，将任务放入阻塞队列中。阻塞队列充满时抛出`RejectedExecutionException`。(相比于`cached`:`cached`在任务数量超过`maximumPoolSize`时直接抛出异常而不是将任务放入阻塞队列)

#### 直连提供者

直连提供者一般是在开发测试环境下，为了方便测试，绕过注册中心，测试特定服务，具体操作方式有两种：

- `jvm`命令行：

  ```sh
  java -Dcom.alibaba.xxx.XxxService=dubbo://localhost:20890
  # 或者
  java -Ddubbo.resolve.file=xxx.properties
  ```

  文件内容

  ```properties
  com.alibaba.xxx.XxxService=dubbo://localhost:20890
  ```

  `2.0` 以上版本自动加载 `${user.home}/dubbo-resolve.properties`文件，不需要配置

- `xml`或者注解

  xml

  ```xml
  <dubbo:reference id="xxxService" interface="com.alibaba.xxx.XxxService" url="dubbo://localhost:20890" />
  ```

  

  注解
  
  ```java
  @DubboReference(version = "1.0", interfaceName = "demoService", interfaceClass = DemoService.class,
              url = "dubbo://localhost:20890")
      private DemoService demoService;
  ```

### 总结

好了，今天就说这么多，其他更多配置建议各位小伙伴看下官方文档。大部分都很简单，基本上都是加个配置就可以搞定的，而且有好多内容我们在之前分享的过程中都已经提到过了，所以就更简单了。

