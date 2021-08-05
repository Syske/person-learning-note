# spring-cloud-Hystrix监控面板

### 前言

昨天我们分享了`Hystrix`熔断的相关知识点，但由于时间的关系，还有一些基础内容没有来得及分享，今天我们花一点时间补充下。

今天我们补充的内容主要是关于`Hystrix`监控面板，这一块不算核心内容，但是也比较重要。好了，下面我们直接开始吧。

### Hystrix控制面板

首先你需要创建一个`spring-boot`项目，或者用我们之前的项目也可以，然后添加`hystrix-dashboard`相关依赖。

#### 依赖

```xml
 <dependency>
     <groupId>org.springframework.cloud</groupId>
     <artifactId>spring-cloud-starter-netflix-hystrix-dashboard</artifactId>
     <version>2.2.9.RELEASE</version>
</dependency>
```

同时，你还需要引入`hystrix`的相关配置：

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
    <version>2.2.9.RELEASE</version>
</dependency>
```

否则在启动时会报错

![](https://gitee.com/sysker/picBed/raw/master/20210805082845.png)

#### 配置

控制面板的配置比较简单，只需要在主入口加上`@EnableCircuitBreaker`和`@EnableHystrixDashboard`注解即可启用熔断器面板

```java
@SpringBootApplication
@EnableCircuitBreaker
@EnableHystrixDashboard
public class SpringCloudHystrixDashboardDemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringCloudHystrixDashboardDemoApplication.class, args);
    }

}
```

#### 添加监控服务

以上配置工作完成后，访问如下地址即可访问熔断器管理页面

```
http://localhost:9991/hystrix
```

页面效果如下

![](https://gitee.com/sysker/picBed/raw/master/20210805084625.png)

然后我们需要在页面上配置我们需要访问的服务



#### 踩坑

如果访问结果如下

![](https://gitee.com/sysker/picBed/raw/master/image-20210805083752789.png)

同时后台控制台有如下提示信息，表面你没有配置允许访问熔断监控页面的地址：

![](https://gitee.com/sysker/picBed/raw/master/20210805084005.png)

你只需要在你的`hystrix-dashBoard`配置文件中添加如下配置即可：

```properties
hystrix.dashboard.proxy-stream-allow-list= localhost
```



如果一直如下显示，这是因为你的服务一直没有被访问，所以没有监控数据

![](https://gitee.com/sysker/picBed/raw/master/image-20210805083500577.png)

只要你调用以下服务，就会看到如下监控数据

![](https://gitee.com/sysker/picBed/raw/master/20210805083421.png)

### 总结

