# spring-boot基于redis实现计数器限流算法

### 前言

昨天我们已经预告了今天的内容——实现计数器限流算法，所以今天不需要过多说明，我们直接开始正文。

### 计数器限流算法

关于计数器限流算法的实现原理，我们昨天已经介绍过了，今天的内容算是基于我们昨天所说的原理的一种应用和实现，当然还是有必要说下我们的实现思路的：

在接口内部最开始的地方，设置调用方的计数器（`key`为调用方唯一的身份信息），第一次调用时将其值设置为`1`并放进缓存中，同时缓存设置过期时间，有效期内每次调用计数器`+1`，时间过期，缓存会自动删除。可以把相关逻辑封装成自定义注解，搞成通用组件，这样只需要在需要限速的接口上加上对应的的注解即可，明天我们可以来实现下。

#### 创建项目

这里我们直接创建一个`spring boot`的`web`项目，然后引入`redis`客户端的依赖：

```xml
 <dependency>
     <groupId>org.springframework.data</groupId>
     <artifactId>spring-data-redis</artifactId>
     <version>2.3.6.RELEASE</version>
</dependency>

<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
</dependency>
```

`redis`用的是`spring boot`的`RedisTemplate`，当然你也可以用其他的，没有任何限制，然后是`redis`客户端设置：

```yml
spring:
  redis:
    database: 0
    host: 127.0.0.1
    port: 6379
    password: redis1234567
    # 连接超时时间（ms)
    timeout: 5000
    # 高版本springboot中使用jedis或者lettuce
    jedis:
      pool:
        # 连接池最大连接数（负值表示无限制）
        max-active: 8
        # 连接池最大阻塞等待时间（负值无限制)
        max-wait: 5000
        # 最大空闲链接数
        max-idle: 8
        # 最小空闲链接数
        min-idle: 1
```

`redis`配置类：

```java
@Configuration
public class RedisConfig {

    private static Logger logger = LoggerFactory.getLogger(RedisConfig.class);

    @Value("${spring.redis.host}")
    private String host;
    @Value("${spring.redis.password}")
    private String password;
    @Value("${spring.redis.port}")
    private int port;
    @Value("${spring.redis.database}")
    private int database;

    @SuppressWarnings("all")
    @Bean
    public StringRedisTemplate redisTemplate(RedisConnectionFactory factory) {
        StringRedisTemplate template = new StringRedisTemplate(factory);
        Jackson2JsonRedisSerializer jackson2JsonRedisSerializer = new Jackson2JsonRedisSerializer(Object.class);
        ObjectMapper om = new ObjectMapper();
        om.setVisibility(PropertyAccessor.ALL, JsonAutoDetect.Visibility.ANY);
        om.enableDefaultTyping(ObjectMapper.DefaultTyping.NON_FINAL);
        jackson2JsonRedisSerializer.setObjectMapper(om);
        RedisSerializer stringSerializer = new StringRedisSerializer();
        template.setKeySerializer(stringSerializer);
        template.setValueSerializer(jackson2JsonRedisSerializer);
        template.setHashKeySerializer(stringSerializer);
        template.setHashValueSerializer(jackson2JsonRedisSerializer);
        template.afterPropertiesSet();
        return template;
    }


    @Bean
    public JedisConnectionFactory jedisConnectionFactory() {
        logger.info("jedisConnectionFactory:初始化了");
        RedisStandaloneConfiguration configuration = new RedisStandaloneConfiguration();
        configuration.setHostName(host);
        configuration.setPassword(RedisPassword.of(password));
        configuration.setPort(port);
        configuration.setDatabase(database);
        return new JedisConnectionFactory(configuration);
    }
}
```

至此，项目的基本环境基本上搭建完成，下面开始编写业务代码。

#### 限流业务实现

为了能够实现业务层面的低耦合，同时也为了便于应用到实际业务中，这里我将限流器封装到拦截器中，然后通过自定义注解的方式实现拦截器的业务去耦合。

##### 限速注解组件

我的第一步是定义一个计数器限流注解组件：

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface CounterLimit {

    /**
     * 调用方唯一key的名字
     * 
     * @return
     */
    String name();
    /**
     * 限制访问次数
     * @return
     */
    int limitTimes();

    /**
     * 限制时长，也就是计数器的过期时间
     *
     * @return
     */
    long timeout();

    /**
     * 限制时长单位
     *
     * @return
     */
    TimeUnit timeUnit();

}
```

注解包括四个属性，`name`表示调用方身份唯一性的参数名，比如`userId`；`limitTimes`表示限制访问次数，也就是他在指定时间内可以访问多少次；`timeout`表示限制访问次数的有效期，一分钟还是一个小时；`timeUnit`表示限速实际的单位，秒、分钟、小时等。

##### 限速拦截器

没做之前，考虑的是通过切面来实现，但是今天实际实践的时候，发现之前想偏了（竟然会犯入参低级错误，说明最近轮子造的有点少），最终是通过拦截器实现的（忠告：没事还是要多造轮子，不然容易手生）：

```java
@Component
public class CounterLimiterHandlerInterceptor implements HandlerInterceptor {

    @Autowired
    private RedisTemplate redisTemplate;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        if (handler instanceof HandlerMethod) {
            HandlerMethod handlerMethod = (HandlerMethod) handler;
            // 判断方法是否包含CounterLimit，有这个注解就需要进行限速操作
            if (handlerMethod.hasMethodAnnotation(CounterLimit.class)) {
                CounterLimit annotation = handlerMethod.getMethod().getAnnotation(CounterLimit.class);
                JSONObject result = new JSONObject();
                String token = request.getParameter(annotation.name());
                response.setContentType("text/json;charset=utf-8");
                result.put("timestamp", System.currentTimeMillis());
                BoundValueOperations<String, Integer> boundGeoOperations = redisTemplate.boundValueOps(token);
                // 如果用户身份唯一key为空，直接返回错误
                if (StringUtils.isEmpty(token)) {
                    result.put("result", "token is invalid");
                    response.getWriter().print(JSON.toJSONString(result));
                // 如果限速校验通过，则将请求放行
                } else if (checkLimiter(token, annotation)) {
                    result.put("result", "请求成功");
                    Long expire = boundGeoOperations.getExpire();
                    logger.info("result：{}, expire: {}",  result, expire);
                    return true;
                // 否则告知调用方达到限速上线
                } else {
                    result.put("result", "达到访问次数限制，禁止访问");
                    Long expire = boundGeoOperations.getExpire();
                    logger.info("result：{}, expire: {}",  result, expire);
                    response.getWriter().print(JSON.toJSONString(result));
                }
                return false;
            }
        }
        return true;
    }

    /**
    * 限速校验
    */
    private Boolean checkLimiter(String token, CounterLimit annotation) {
        BoundValueOperations<String, Integer> boundGeoOperations = redisTemplate.boundValueOps(token);
        Integer count = boundGeoOperations.get();
        if (Objects.isNull(count)) {
            redisTemplate.boundValueOps(token).set(1, annotation.timeout(), annotation.timeUnit());
        } else if (count >= annotation.limitTimes()) {
            return Boolean.FALSE;
        } else {
            redisTemplate.boundValueOps(token).set(count + 1, boundGeoOperations.getExpire(), annotation.timeUnit());
        }
        return Boolean.TRUE;
    }
}
```

代码逻辑也比较简单：

- 首先判断接口方法是否包含`CounterLimit`注解，有这个注解就需要进行限速操作
- 如果用户身份唯一`key`为空，直接返回错误
- 如果限速校验通过，则将请求放行，否则告知调用方达到限速上线
- 在校验限速方法中，如果`count`为空，表示首次访问，则存放一个`count`，并设置过期时间
- 如果达到访问限制上限，直接拒绝，未达到则`count+1`，过期时间设置为剩余时间

代码也有比较详细的注解，各位小伙伴也应该能看懂。

**注意：** 当然如果你的项目本身已经有了完善的全局异常处理机制，这里的拦截器可以直接抛出对应的异常，这里为了方便我偷了个懒，并没有做全局异常处理，而是直接通过`response`返回了异常信息，实际项目开发中，这种写法肯定是不合理的，各位小伙伴一定要注意哦！

##### 拦截器配置

这一块就属于复习内容了，也属于比较入门级别的`spring boot`操作了，这里不再过多赘述，详细代码如下：

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Autowired
    private CounterLimiterHandlerInterceptor counterLimiterHandlerInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // 计数器限速
        registry.addInterceptor(counterLimiterHandlerInterceptor).addPathPatterns("/**");
        WebMvcConfigurer.super.addInterceptors(registry);
    }
}
```



##### 接口配置

接口这块也比较简单，就是简单的`controller`方法，然后方法上多了我们的自定义限速器注解`CounterLimit`，这个注解的参数我们上面已经解释过了，所以这里也就不再赘述：

```java
	@CounterLimit(name = "token",limitTimes = 5, timeout = 60, timeUnit = TimeUnit.SECONDS)
    @GetMapping("/limit/count-test")
    public Object counterLimiter(String name, String token) {
        JSONObject result = new JSONObject();
       result.put("data", "success");
        return result;
    }
```



#### 测试

完成以上内容之后，我们就可以进行相关测试了，首先将我们的项目启动起来，然后直接访问我们的接口即可，访问接口的时候记得带着我们的`token`（唯一`key`），最终访问结果如下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20211031232851.png)

从结果中我们可以看出来，在第一次访问的时候，`token`的过期时间为`60`，我们连续访问`5`次之后，接口限制我们访问的，然后等到限制过期之后（`token`过期），又可以继续访问了。至此，我们的计数器限流的算法实现也算是完美达成，是不是很简单呢？

### 总结

本次`demo`总体来说很简单，除了算法本身之外，基本上都是`java`或者`spring boot`的简单知识点应用，但是从我自己实践的感受来说，我觉得以后还是得多造轮子，因为之前比较熟悉得好多配置和写法都生疏了，好多都要翻看之前的`demo`才能想起来。当然，话句话说就是，很多看起来很简单的实例或者`demo`，其实在真正实践的时候并不简单，因为我们往往总会高估自己的能力……

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20211031233839.png)

项目完整代码：

```
https://github.com/Syske/learning-dome-code/tree/dev/spring-boot-counter-limiter
```

好了，各位小伙伴，晚安吧！

