# spring-cloud断路器之Hystrix

### 前言



### Hystrix

#### 依赖

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
    <version>2.2.9.RELEASE</version>
</dependency>
```

#### 配置

在项目入口类上加上`@EnableCircuitBreaker`注解，即可启用`Hystrix`熔断器

```java
@SpringBootApplication
@EnableCircuitBreaker
public class SpringCloudHystrixDemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringCloudHystrixDemoApplication.class, args);
    }

}
```

#### 接口熔断配置

```java
@RequestMapping("/hystrix/{name}")
@HystrixCommand
public Object hystrix(@PathVariable(name = "name") String name) {
    JSONObject jsonObject = new JSONObject();
    try {
        Double v = 3000 * Math.random();
        System.out.println("name: " + name + " 睡眠时间：" + v);
        jsonObject.put("sleep", v.longValue());
        jsonObject.put("name", name);
        jsonObject.put("message", "请求成功");
        Thread.sleep(v.longValue());
    } catch (Exception e) {
        System.out.println(e);
    }
    return jsonObject;
}
```

![](https://gitee.com/sysker/picBed/raw/master/20210804083229.png)

![](https://gitee.com/sysker/picBed/raw/master/20210804083200.png)

```java
@HystrixCommand(fallbackMethod = "error")
```

同时需要定义一个名字为`error`，参数与接口保持一致的熔断回调方法：

```java
public Object error(String name) {
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("message", "触发服务熔断机制");
        jsonObject.put("name", name);
        return jsonObject;
    }
```

回调方法的名字可以根据自己的需要自定义，但是参数必须与接口保持一致，否则会报错：

![](https://gitee.com/sysker/picBed/raw/master/20210804083708.png)



#### 调用方设置

```java
@RequestMapping("/testHystrix")
public Object testHystrix() {
    List<JSONObject> jsonObjectList = Lists.newArrayList();
    for (int i = 0; i < 10; i++) {
        jsonObjectList.add(restTemplate.getForObject("http://spring-cloud-Hystrix-demo/hystrix/" + i, JSONObject.class));
    }
    return jsonObjectList;
}
```



#### 测试





![](https://gitee.com/sysker/picBed/raw/master/20210804084528.png)

![](https://gitee.com/sysker/picBed/raw/master/20210804084550.png)



#### 启用监控面板

![](https://gitee.com/sysker/picBed/raw/master/20210804085015.png)

### 总结