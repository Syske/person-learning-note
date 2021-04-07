# nacos作为服务注册中心

## 前言

上一次，我分享了`nacos`作为配置中心的的`demo`，介绍了`nacos`的安装、配置启动过程，以及`springboot`整合`nacos`的过程，今天我们要分享的是`nacos`作为注册中心的应用，会介绍如何如何注册服务、获取并调用服务。`nacos`的配置和安装之前已经介绍了，所以今天就不再介绍。

## 正文

在开始今天的内容，我们先看下什么是服务注册中心。

### 注册中心

在微服务的时代，所有对外提供的服务基本都是以集群的方式存在的，而且随着业务的不断扩展，服务也面临着集群的扩展，微服务的规模从几十、几百，甚至到几千都有可能，如果我们把所有的服务地址都写在配置文件中，或者写在代码中，这样导致了服务之间的耦合性太高，不利于服务的扩展和升级，同时由于服务规模的不断扩大，服务的管理也变得复杂，不可能通过人工方式管理的方式，一方面人工确实容易出错，另一方确实效率也太低了。

另外从服务调用方来讲，如果你的服务地址发生了变化，如果他没有做相应的修改变更，那将导致相关服务不可用，影响业务办理。所以，在这样的业务需求之下，就诞生了注册中心这样的系统组件。

**注册中心**，简单来说就是微服务的管理中心，他不仅要负责服务的注册（服务提供者）、服务发现（服务消费者），还要服务的监测，服务的治理，举个例子来说，注册中心就类似之前的号码百事通，如果你想知道某个机构的服务电话，你只需要拨打114(号码百事通)，他就会告诉你相应的电话号码，然后你再打给对应的机构即可。这里你就是服务的调用方，号码百事通就是注册中心，对应的机构就是服务提供者，我们看下面的图就更容易理解了：

![](https://gitee.com/sysker/picBed/raw/master/20210308213512.png)

服务提供者和服务调用者在服务初始化时，向服务中心提交注册，同时调用者要向注册中心发生心跳请求，便于注册中心进行监测（当然不同组件实现方式会有所不同）

### 常见的注册中心

#### Zookeeper

ZooKeeper是非常经典的服务注册中心中间件，在国内环境下，由于受到Dubbo框架的影响，大部分情况下认为Zookeeper是RPC服务框架下注册中心最好选择

![](https://gitee.com/sysker/picBed/raw/master/20210308214238.png)

#### Eureka

SpringCloud框架生态中最原生的深度结合组件，Eureka是Netflix开发的服务发现框架，基于REST的服务，主要用于服务注册，管理，负载均衡和服务故障转移。但是官方声明在Eureka2.0版本停止维护，不建议使用。

![](https://gitee.com/sysker/picBed/raw/master/20210308214328.png)

#### Consul

Consul是用于服务发现和配置的工具。Consul是分布式的，高度可用的，并且具有极高的可伸缩性，而且开发使用都很简便。它提供了一个功能齐全的控制面板，主要特点是：服务发现、健康检查、键值存储、安全服务通信、多数据中心、ServiceMesh。Consul在设计上把很多分布式服务治理上要用到的功能都包含在内了

![](https://gitee.com/sysker/picBed/raw/master/20210308214448.png)

#### nacos

nacso是我们今天的主角，今天我们的`demo`就是基于他实现的。阿里出品，还是值得信赖的，而且一如既往优秀，在国内特别流行。

![](https://gitee.com/sysker/picBed/raw/master/20210308214528.png)

![](https://gitee.com/sysker/picBed/raw/master/20210308215153.png)



### nacos注册中心示例

今天的示例特别简单，代码量也特别少。

#### 核心依赖

```xml
<dependency>
        <groupId>com.alibaba.boot</groupId>
        <artifactId>nacos-discovery-spring-boot-starter</artifactId>
        <version>0.2.1</version>
</dependency>
```

#### 核心配置

```yaml
nacos:
  discovery:
    server-addr: 127.0.0.1:8848
```

#### 测试服务

```java
@Service
public class TestServiceImpl implements TestService {
    @Override
    public String sayHello(String name) {
        return "hello, " + name;
    }
}
```

#### 测试controller

```java
	@NacosInjected
    private NamingService namingService;   
  /**
     * 获取已注册服务的注册信息
     * @param serviceName
     * @return
     * @throws NacosException
     */
@RequestMapping(value = "/get", method = GET)
@ResponseBody
public List<Instance> get(@RequestParam String serviceName) throws NacosException {
    return namingService.getAllInstances(serviceName);
}

 /**
     * 被注册的服务
     * @param name
     * @return
     */
@RequestMapping(value = "/hello", method = GET)
@ResponseBody
public String sayHello(@RequestParam String name) {
    return testService.sayHello(name);
}
```

#### 注册服务

我们先用官方文档中的方式注册服务：

```sh
curl -X PUT "http://127.0.0.1:8848/nacos/v1/ns/instance?serviceName=example&ip=127.0.0.1&port=8080"
```

这里简单解释下，`http://127.0.0.1:8848/nacos`是你的`nocas`地址；`serviceName`后面的是你要注册的服务名，这个必须唯一，发现服务的时候，就是通过`serviceName`获取的；`ip`是你的服务部署地址；`post`就是你的服务端口。

当然，`nocas`本身也提供的丰富的`API`，我们通过`API`接口也可以注册服务，下面一个简单示例：

```java
	@NacosInjected
    private NamingService namingService;
  /**
     * 注册服务
     * @param serviceName
     * @param ip
     * @param port
     * @return
     * @throws NacosException
     */
    @RequestMapping(value = "/register", method = GET)
    @ResponseBody
    public String register(@RequestParam String serviceName, @RequestParam String ip,
                                   @RequestParam int port) throws NacosException {
        namingService.registerInstance(serviceName, ip, port);
        return "服务注册成功";
    }
```



#### 获取服务信息

首先我们先启动前面写好的示例：

![](https://gitee.com/sysker/picBed/raw/master/20210308220641.png)

可以在浏览器打开如下地址：

```
http://localhost:8080/test/get?serviceName=example
```

或者从通过`shell`访问：

```sh
curl http://localhost:8080/test/get?serviceName=example
```

如果返回结果是`[]`，首先确认`nacos`服务是否启动，然后确认服务是否注册，如果服务正常且服务已经注册过，那么正常的返回结果是这样的：

```json
[{"instanceId":"127.0.0.1#8080#DEFAULT#DEFAULT_GROUP@@example","ip":"127.0.0.1","port":8080,"weight":1.0,"healthy":true,"cluster":{"serviceName":null,"name":"","healthChecker":{"type":"TCP"},"defaultPort":80,"defaultCheckPort":80,"useIPPort4Check":true,"metadata":{}},"service":null,"metadata":{}}]
```

#### 调用测试服务

首先我们再来注册个测试服务`hello`:

```sh
curl -X PUT "http://127.0.0.1:8848/nacos/v1/ns/instance?serviceName=hello&ip=127.0.0.1&port=8080"
```

然后我们使用`nacos`的`API`获取已经注册的服务信息，并调用它：

```java
/**
     * 发现并调用服务
     * @param serviceName
     * @return
     * @throws NacosException
     */
    @RequestMapping(value = "/getService", method = GET)
    @ResponseBody
    public String getService(@RequestParam String serviceName) throws NacosException {
        Instance instance = namingService.getAllInstances(serviceName).get(0);
        String serviceUrl = "http://" + instance.getIp() + ":" + instance.getPort()
                + "/test/hello" + "?name=test";
        System.out.println(serviceUrl);
        return restTemplate.getForObject(serviceUrl, String.class);
    }
```

然后访问我们的`getService`这个接口即可返回`hello`服务的调用结果：

![](https://gitee.com/sysker/picBed/raw/master/20210308222502.png)

这里要安利下`spring`的`restfull`调用工具`RestTemplate`，我也是最近发现`spring`还有这个工具，可怜的我还在用自己的`httpUtil`，使用方式也很简单，在配置类中加入如下配置：

```java
@Bean
public RestTemplate restTemplate() {
    return new RestTemplate();
}
```

然后再需要的地方注入即可：

```java
@Autowired
private RestTemplate restTemplate;
```



## 总结

今天分享了`nacos`注册中心的一些简单操作，包括简单的配置、服务注册、服务发现和调用，因为我也正在学习和摸索，所以更高阶的应用还需要进一步探索，这里算是给不清楚的小伙伴做一个科普和介绍。

完整示例请访问`github`获取：

```
https://github.com/Syske/learning-dome-code/tree/dev/springboot-nacos-discovery-demo
```

简单介绍下这个仓库，这个仓库主要存放我日常学习的一些示例和工作中实践的一些总结，我会把项目中比较好的解决方案，或者比较具有代表性的需求单独抽出来形成一个小`demo`，方便下一次在类似的需求中使用，对我而言它就是个资源库，如果它也能给你一些帮助或者能解决你的一些问题，那我深感荣幸😊！