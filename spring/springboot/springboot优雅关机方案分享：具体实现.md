## 前言

前两次分享，我们已经介绍过了`k8s`节点关机的流程和优雅关机要实现的流程，今天我们来一起来看下具体的代码实现，主要内容如下：
- `SIGTERM`监听逻辑
- 预关机逻辑
- 各个组件的关机逻辑和监控逻辑

## 实现过程

### 前置要点

前面我们说了，本项目实际是个`spring-boot-starter`，所以你要先创建`spring-boot-starter`的项目，这里就不赘述具体过程了，具体可以参考之前的分享：
[[编写你的第一个spring-boot-starter]]

这里提几个需要注意的点：

#### pom依赖

这块有两个标签要注意，`scope`和`optional`，组合使用，可以确保依赖的灵活性，同时避免依赖冲突：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/b6104695-62fb-4154-873e-a556fea18e7d.jpg)

#####  scope（作用域）

依赖的作用范围，控制依赖的使用范围，这里的`provided`表示编译和测试时有效，运行时由运行环境提供，也就是不会打进包里。这样可以确保我们的`starter`引入项目后不会影响原项目的`pom`依赖关系，带来未知风险。常见的作用域还有：
- **compile**（默认）：编译、测试、运行都有效，会打包
- **provided**：编译和测试时有效，运行时由容器提供
- **runtime**：运行时需要，编译时不需要
- **test**：仅测试时使用
- **system**：类似provided，但需要显式指定本地jar路径

##### optional（可选依赖）

当设置为 `true` 时：
- **不会传递依赖**：即使其他项目依赖本项目，也不会继承这个可选依赖
- **需要显式声明**：使用者必须主动声明才能使用
- **场景**：可选功能、有冲突的依赖、特定环境才需要的依赖

当然，这两个`pom`标签通常是配合`spring-boot`的条件配置来使用，或者你可以确保代码运行时一定包含对应的依赖，否则会导致运行时异常。

#### spring.factories

这个文件是`starter`的核心，当我们的项目被引入时，`springboot`会根据我们的`spring.factories`初始化我们的`starter`，并根据我们的配置类，完成加载和配置。这个项目通常位于`src/main/resources/META-INF/spring.factories`下，配置内容如下：

```
# src/main/resources/META-INF/spring.factories  
org.springframework.boot.autoconfigure.EnableAutoConfiguration=\  
io.syske.springboot.starter.config.GracefulShutdownAutoConfiguration,\  
io.syske.springboot.starter.compent.SpringContextUtilConfig
```

配置的内容就是我们的配置类，有多个配置类用逗号分隔开就行。因为配置类本身是支持`import`的，所以我们通常只需要配置一个主配置类即可，其他的直接`@Import`即可：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/5ffad59d-6fa7-49e1-b4c3-90efecef35fc.jpg)

我这里配置两个是由于另一个类不能条件注入，所以单独配置了，具体大家根据自己实际情况看。

##### 条件配置

这里简单说下本次用到的几个条件注解：

- `@ConditionalOnProperty`：这个注解的作用是根据某个配置文件判断，类或者方法支付要执行，通常和`@Configuration`或者`@Bean`组合使用。在我们上面的截图中，实际就是通过判断优雅关机开关是否开启进行条件配置，如果条件缺失，我们给了默认值`true`。
- `@ConditionalOnMissingBean`：当缺少某个类的`bean`时配置，类似单例模式
- `@ConditionalOnClass`：当有指定的`class`的时候触发配置。这个就是我前面说的要和`pom`那两个标签组合的条件配置。所有的关机组件逻辑都要加上这个判断，确保核心类存在（也就是依赖存在）时，才配置对应组件的关机逻辑。
- `@ConditionalOnWebApplication`：这个注解是加在`Tomcat`的关机组件上的，确保它是`WebApplication`


### SIGTERM逻辑

核心实现其实就是创建一个`bean`，并在`bean`初始化逻辑中定义一个处理`TERM`信号的`Signal`，并在`Signal`的`handle`逻辑中加入我们的预关机逻辑即可：
```java
try {  
    Signal signal = new Signal("TERM");  
    Signal.handle(signal, sig -> {  
        logger.info("Received SIGTERM signal from K8s, starting graceful shutdown");  
        // 处理关机信号
        handleShutdownSignal();  
    });  
    logger.info("SIGTERM handler registered successfully");  
  
} catch (Exception e) {  
    logger.warn("Failed to register SIGTERM handler: {}, using shutdown hook as fallback", e.getMessage());  
    setupShutdownHook();  
}
```

这里我就直接放截图了，处理关机信号逻辑：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/859f4ff5-ee40-4796-88a9-538c1a885eeb.jpg)然后就是预关机逻辑：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/8345fccf-bb95-47ac-9b3d-c46139464c8f.jpg)
这里简单说下:
- 服务标记为不健康：这里我自定义了一个`healthIndicator`，实际没太大作用，因为我们的服务健康检查并不依赖这个，如果你们的服务健康检查依赖的是`springboot`的健康检查机制，那实现自定义健康检查则是需要考虑的。
- 等待负载均衡感知：这个实际和网关有关系，在本项目中非必须，逻辑中只是睡了`5`秒。
- 执行优雅关机：这里就是根据我们自定义的优先级，依次关机各个组件。

下面，我们逐步介绍各组件的实现逻辑。

### Tomcat

#### 监控逻辑

`tomcat`优雅关机要实现`TomcatConnectorCustomizer`接口，并实现`customize`方法，主要是为了关机时能获取到连接器，同时设置`Executor`实现统计活跃请求数的逻辑：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/92812d34-3bc5-4a73-9393-09327772ef42.jpg)
计数执行器逻辑：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/c25732c2-5b79-495a-9d61-2998c61aab9a.jpg)

#### 组件核心逻辑

核心逻辑就三步：
```java
// 1. 暂停接收新请求  
pauseConnector();  
  
// 2. 等待活跃请求完成  
waitForActiveRequests();  
  
// 3. 关闭连接器  
stopConnector();
```
停止接受新请求实际就是调用连接器的暂停方法：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/e51f87fa-befd-4952-936a-c6cb6318f880.jpg)
等待活跃请求完成，实际就是等待线程池关闭：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/4a74ac67-875a-448d-b0a9-c0db20df7734.jpg)
关闭线程池实际就是调用`shutdown`方法，超时强制关闭实际就是超时后调用`shutdownNow`，然后再等待：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/599ed0c9-8840-45f2-8e08-6fdbe833a701.jpg)
线程池考虑了`org.apache.tomcat.util.threads.ThreadPoolExecutor`和`java.util.concurrent.ThreadPoolExecutor`，是分别处理，实际两者是继承关系，其实可以省略第一个：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/361e0d0d-6bfc-4509-9241-14333c9e499b.jpg)
停止连接器也很简单，就是调用`stop`方法，不过关闭前需要判断下，避免重复关闭（`springboot`本身的关机逻辑也会触发关闭）：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/2ace3b41-cf4e-4555-afba-05d14526134f.jpg)
### RPC提供者

#### 监控逻辑

监控这里的逻辑是通过`sofa-rpc`的`Filter`来实现的：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/e8b6903a-37c2-420b-8bb0-069dfd9b1b7c.jpg)
- 统计请求数量
- 服务注册：这里的注册实际是个辅助逻辑，确保没有正常注册的提供者在调用过程中注册。真正的服务提供中注册逻辑是基于`ApplicationRunner`实现的

关于拦截器的注册有几个点：
- 拦截器只能通过`SPI`方式注入，且要正确配置`@AutoActive`和`@Extension`，需要注意的是`@Extension`配置的名称要与`com.alipay.sofa.rpc.filter.filter`文件中配置的名称一致，否则不生效
	![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/721c093c-3536-4d8c-b3a9-88c4908a0799.jpg)
- `com.alipay.sofa.rpc.filter.filter`文件必须正确配置：配置的`key`是`@Extension`配置的值，`value`是拦截器的全类名：
	![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/4245b770-79d7-449a-9ac4-95fdda305c0e.jpg)
**注意**：这里还有个比较坑的点，`sofa-boot`的拦截器不能直接使用`springboot`的`bean`，所以需要借助`SpringContextUtil`，这也是我的`spring.factories`里面还配置了`SpringContextUtilConfig`的原因。因为拦截器没法实现条件配置，所以`SpringContextUtil`也不能条件配置。

#### 目标发现逻辑

`Runer`核心逻辑如下：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/226a9b44-e20b-47a8-a17a-d1455437c369.jpg)
这里搞了好久一直没有搞定，最后是在`sofa-boot`的代码中找到的，然后直接解决了提供者发现问题：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/a3698851-eaf8-41e9-a91f-89c405510587.jpg)

#### 组件核心逻辑

组件核心逻辑就三步：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/dbbade38-9659-4bc5-8c6f-3bb02bd6fe20.jpg)
1. 标记为关闭状态：实际这一步并没有拦截请求
2. 取消服务者注册：这一步直接调用`unExport`方法
	![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/c46ee58f-19f4-4b37-b5ab-b07e4170304b.jpg)
3. 等待处理中的请求完成：判断活跃请求的逻辑来自监控逻辑
	![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/5c256a55-201e-4abb-babf-ac2b16c0366f.jpg)

### ActiveMQ

#### 监控逻辑

`activeMQ`的监控逻辑实际是通过`DefaultMessageListenerContainer`直接获取的，所以监控逻辑本身没什么特殊的：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/f5d2e618-9d5f-4d82-9535-fe556fb65ba5.jpg)

#### 目标发现逻辑

`activeMQ`的服务发现逻辑也比较简单，核心其实就是将`JmsListenerEndpointRegistry`注入我们的关机组件，关机组件要通过这个对象获取所有的`DefaultMessageListenerContainer`消费者容器：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/39208ba3-71a8-424e-8f98-50defe26c6a2.jpg)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/bfb87661-d08e-42fa-9099-7b6ad2b57e9e.jpg)

#### 组件核心逻辑

核心逻辑如下：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/f014ef39-e9fc-417e-a319-6f2a7a67f621.jpg)
1. 发现所有监听者，并打印容器状态
2. 停止容器：调用`stop`方法
	![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/503003a6-5c47-4ac5-91dc-4f7ff432cb5c.jpg)
3. 等待处理中的消息处理完成：
	![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/967e8ed7-045c-4186-8226-3b2e07927901.jpg)

### RocketMQ

#### 监控逻辑

监控逻辑是根据容器是否是`running`状态判断的，比较简单：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/0905c566-8ac7-46b5-a393-f4d0b5ecb178.jpg)

#### 目标发现逻辑

组件的发现逻辑是通过`spring`的后置处理器来完成的，将所有的`DefaultRocketMQListenerContainer`收集起来。
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/e31bae59-2ada-4ae2-8cf4-0b192caa33e8.jpg)

#### 组件核心逻辑

核心逻辑如下：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/b432c1a3-a080-4777-a8c9-d0abd4cacdd5.jpg)

1. 停止监听器逻辑：这里是调用`stop`方法进行停止
	![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/7342b158-705e-485b-887d-a7c12dde2d08.jpg)
2. 等待处理中的容器停止：这里直接用的是容器状态判断的，因为消费中的消息数量，需要调用`rpcketMQ`的服务端接口，实际意义不大，而且要依赖外部服务，所以直接判断容器状态。
	![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/dcebbe4b-fddd-43e7-94fa-47412c587a21.jpg)
### 线程池

#### 监控逻辑

没什么监控逻辑，实际就是直接打印线程池的活跃的线程数：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/18156132-6d8c-4e89-9fe1-48b25a6469ce.jpg)

#### 目标发现逻辑

发现逻辑也是基于`spring`的后置处理器完成的，根据不通的线程池注册到不通的集合中：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/566d56d3-2538-4fb7-945a-e7b33dd21f99.jpg)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/fe19c9e3-f270-4450-b3ea-707169c3f1bc.jpg)

#### 组件核心逻辑

核心逻辑：不同的线程池挨个关闭
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/2cc0afbe-9c2a-4fcb-adba-f92546fe127e.jpg)

关闭逻辑都差不多：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/2f6b103a-175f-42c1-81f3-432577251b1e.jpg)
1. 线程池关机：调用`shutdown`方法
2. 等待完成：调用`awaitTermination`，超时后调用`shutdownNow`

`ForkJoinPool`比较特殊，只能等待：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/859f82f2-9a76-4d9d-a06f-574d31653ca1.jpg)

### RPC客户端

客户端也叫运行时环境，这个销毁就比较简单了，没有监控，直接通过反射调用`RpcRuntimeContext`的`destroy`方法即可。
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/43520fd4-3c1e-49ae-86b3-d14b17c78da9.jpg)

至此，我们的`k8s`环境下的`spring-boot`服务优雅关机方案就完成了。下面我们简单总结下：

## 总结

我们用了三篇文章，和大家聊清楚了 K8s 环境下 Spring Boot 服务“优雅关机”这回事儿：

**第一篇：先弄懂 K8s 是怎么关机的**  
带大家梳理了 K8s 节点和 Pod 关闭的基本流程。了解了它的“套路”，咱们自己设计方案时才能心里有底。

**第二篇：咱们的方案长啥样？**  
知道了 K8s 的流程，那我们的 Spring Boot 服务该怎么配合着“优雅退场”呢？这一篇就讲了咱们的整体设计思路，关机要分几步、每一步要注意啥，都给大家掰扯明白了。

**第三篇：动手！把代码写出来**  
光说不练假把式。最后一篇咱们直接上代码，手把手讲解了怎么监控组件、怎么发现需要关闭的目标，再把整个关闭流程像拼积木一样组合起来。让大家能从代码层面真正搞懂怎么写。

当然了，咱们现在这个方案还不是“终极完美版”。除了之前提到的（比如 `Tomcat` 和 `RPC`提供者可以同时关）这些优化点，其实还有一些地方可以做得更好。

比如说 **“重复关闭”的问题**：虽然代码里加了判断，不会因为重复调用而报错，但 `Spring Boot` 底层的关机钩子 (`ShutdownHook`) 逻辑其实还在，这里未来还有更优雅的解法。

我们特意把这个点提出来，其实就是想“抛砖引玉”。优雅关机这件事，细节很多，也欢迎大家一起来思考、讨论，看看还有哪些地方可以优化得更好。