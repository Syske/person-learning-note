# spring-cloud服务之间的调用

### 前言

昨天，我们通过一个实例演示了，`spring-cloud`服务注册组件——`Eureka`的基本配置和简单用法，但是服务注册就是为了方便后期的发现和调用，所以今天我们趁热打铁，分享下`spring-cloud`服务之间的调用。

### 服务间的调用

关于`spring-cloud`的服务调用，我们首先需要了解它的两个核心组件`Ribbon`和`Feign`。

我们都知道，`spring boot`的接口都是基于`REST`实现的，但是在实际线上运行的时候，考虑到用户规模、服务可用性等方面的因素，我们一般很少是单节点运行的，通常都是以集群模式部署的，但是在集群部署中，又有一个核心的问题必须解决——负载均衡。关于负载均衡，各位小伙伴应该不陌生，最常用的组件之一`nginx`其中一个很核心的用途就是做负载均衡，但是`nginx`在实际做负载均衡的时候，确实不够方便，需要手动配置服务地址，如果服务地址发生变化，相关配置也需要修改，所以不够灵活。

当然`spring cloud`作为一款微服务综合框架，它自然也提供了自己的一套负载均衡解决方案，所以接下来我们就来看下`spring cloud`的负载均衡组件——`Ribbon`。

#### Ribbon

`Ribbon`中文的意思是丝带、带状物，正如它的含义，它就是连接调用方和服务之间的纽带。我们先通过一个简单实例，来演示下，然后再来解释，首先是它的核心依赖：

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-ribbon</artifactId>
    <version>2.2.9.RELEASE</version>
</dependency>
```

这个组件你需要添加到服务**调用方**的依赖中。同时，还需要增加它的配置：

```java
@Configuration
public class RibbonConfig {

    // 多节点负载
    @LoadBalanced
    @Bean(name = "restTemplate")
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
```

`@LoadBalanced`注解的作用是启用多节点负载，这样后期我们在调用的时候，`RestTemplate`客户端其实就是通过负载均衡的方式在调用服务提供者。

然后，在服务调用方，我们通过`RestTemplate`去调用我们的服务提供者：

```java
@Autowired
private RestTemplate restTemplate;

@GetMapping("/ribbon")
public Object queryUserByProductId() {
    List<JSONObject> jsonObjectList = Lists.newArrayList();
    for (int i = 0; i < 10; i++) {
        JSONObject forObject = restTemplate.getForObject("http://user-center/user/" + (i + 1), JSONObject.class);
        jsonObjectList.add(forObject);
    }
    return jsonObjectList;
}
```

我们分别启动服务调用发和被调用方。



![](https://gitee.com/sysker/picBed/raw/master/20210802085349.png)

![](https://gitee.com/sysker/picBed/raw/master/20210802085436.png)

![](https://gitee.com/sysker/picBed/raw/master/20210802085532.png)

![](https://gitee.com/sysker/picBed/raw/master/20210802085621.png)

### 总结