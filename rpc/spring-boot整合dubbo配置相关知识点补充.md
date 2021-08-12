# spring-boot整合dubbo相关知识点补充

### 前言

昨天我们分享了`spring-boot`整合`dubbo`的相关内容，不过准确地说，应该是和`spring `整合，因为我们其实并没有用`dubbo`的`starter`，而是通过注解的方式把`dubbo`的相关配置注入到`spring`的`ioc`容器中。

这种方式只是省去了`xml`配置的繁琐配置，改成了注解的方式，本质上只能算`web`层面的集成，因为`spring-boot`的核心在`stater`，`starter`的核心在自动配置，关于定制自己的`spring-starter`我们前面有分享过，感兴趣的小伙伴可以去看下：

不过，这对不喜欢`xml`配置的小伙伴来说（我算其中有一个，当然`xml`有其优势），已经算福音了。好了，废话就说这么多，今天我们来对昨天的内容做一个简单的补充说明，由于昨天的内容过于繁杂，而且内容有点多，好多细节的知识点，没有在展开说明，下面我们就来对这些知识点做一个说明。

### dubbo内容补充

#### 配置

`dubbo`的配置主要有三部分，一部分是注册中心的相关配置，一部分是应用本身的配置，另外一部分是注册中心的配置。今天主要说明前两种配置，注册中心的配置暂时先不讲。

```
	private String name;

    private String version;

    private String owner;

    private String organization;

    private String architecture;

    private String environment;

    private String compiler;

    private String logger;

    private List<RegistryConfig> registries;
    private String registryIds;

    private MonitorConfig monitor;

    private Boolean isDefault;

    private String dumpDirectory;

    private Boolean qosEnable;

    private String qosHost;

    private Integer qosPort;

    private Boolean qosAcceptForeignIp;

    private Map<String, String> parameters;

    private String shutwait;

    private String hostname;

    private String metadataType;

    private Boolean registerConsumer;

    private String repository;
```



#### 注解

注解这块主要有两个注解注解比较重要，一个`@DubboService`，一个是`@Reference`。

##### DubboService

`@DubboService`注解是`2.7.7`引入的，其主要作用就是为了标记和配置服务提供者，它的前任是`@Service`，这个注解也算是个新人，它是`2.7.0`引入的，从注解属性上看，他们没有本质区别，`@Service`目前已经被弃用，我猜测弃用应该是注解名称太容易被混淆了，不利于服务代码开发维护，毕竟`spring`的原生注解也就`@Service`：

![](https://gitee.com/sysker/picBed/raw/master/images/20210812125920.png)

文档也说的很清楚，`DubboService`是`Serivce`的继任者。

![](https://gitee.com/sysker/picBed/raw/master/images/20210812130021.png)

##### DubboReference

`@Reference`注解也是`dubbo 2.7.7`引入的，主要是用来发现服务的，也就是标记服务消费者。这个注解的继任者是`Reference`，也是`2.7.0`引入的。

![](https://gitee.com/sysker/picBed/raw/master/images/20210812190902.png)

![](https://gitee.com/sysker/picBed/raw/master/images/20210812190159.png)

说明，在`dubbo 2.7.0`之前的版本是不支持注解式配置，而且我发现`2.7.0`以前的版本是属于`com.alibaba`这个`groupId`的，之后的版本是`org.apache.dubbo`这个`groupId`的，这是因为在`2.7.0`之后，阿里巴巴把`dubbo`捐献给`apache`基金会了，现在它是`apache`旗下的顶级项目之一。

![](https://gitee.com/sysker/picBed/raw/master/images/20210812191439.png)

![](https://gitee.com/sysker/picBed/raw/master/images/20210812191522.png)



### 总结