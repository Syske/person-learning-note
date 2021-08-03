# spring-cloud服务间调用 - 下 （feign）

### 前言



### Feign

#### 踩坑

![](https://gitee.com/sysker/picBed/raw/master/20210803082224.png)

版本问题导致

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
    <version>2.2.9.RELEASE</version>
</dependency>

<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
    <version>3.0.3</version>
</dependency>
```

只需要把`openfeign`的版本改成`2.2.9.RELEASE`即可，即`cloud`组件的版本必须与`spring-cloud`的版本保持一致

![](https://gitee.com/sysker/picBed/raw/master/20210803082522.png)

这个问题也是由于依赖不正确导致的，如果你的`spring-boot`依赖是:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter</artifactId>
</dependency>
```

那么你需要把`starter`改成`starter-web`，然后再次启动即可。

![](https://gitee.com/sysker/picBed/raw/master/20210803082815.png)

然后再看下我们的注册中心`Eureka`：

![](https://gitee.com/sysker/picBed/raw/master/20210803082856.png)

![](https://gitee.com/sysker/picBed/raw/master/20210803083600.png)

上面这个报错有两个原因，一个可能是服务名写错了；另一个就是你可能把`ribbon.eureka.enabled`设置成`false`

![](https://gitee.com/sysker/picBed/raw/master/20210803084522.png)

### 总结

