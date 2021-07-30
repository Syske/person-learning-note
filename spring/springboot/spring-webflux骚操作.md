# spring-webflux骚操作

### 前言



### webflux

#### 接口配置

```java
 public Mono<ServerResponse> sendTimePerSec(ServerRequest serverRequest) {
        return ServerResponse.ok().contentType(MediaType.TEXT_EVENT_STREAM).body(  // 1
                Flux.interval(Duration.ofSeconds(1)).   // 2
                        map(l -> new SimpleDateFormat("HH:mm:ss").format(new Date())),
                String.class);
    }
```

#### 路由配置

```java
@Bean
    public RouterFunction<ServerResponse> routSayHi(HiHandler handler) {
        return RouterFunctions
                .route(RequestPredicates.GET("webflux/hi")
                        .and(RequestPredicates.accept(MediaType.ALL)), handler::sayHi)
                .andRoute(RequestPredicates.GET("/webflux/test")
                        .and(RequestPredicates.accept(MediaType.APPLICATION_JSON)), handler::sendTimePerSec);
    }
```



![](https://gitee.com/sysker/picBed/raw/master/20210730083452.png)

![](https://gitee.com/sysker/picBed/raw/master/20210730083523.png)

### 总结

