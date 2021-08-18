# dubbo其他知识点分享

### 前言



### 其他知识点

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



### 总结