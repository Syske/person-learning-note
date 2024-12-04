# spring-cloud核心知识点简单总结

### 前言

本周，我们围绕`spring cloud`常用组件，分享了一些知识点，今天花点时间，简单回顾总结一下。

本周总分分享了四个核心组件，其中包括注册中心组件`eureka`、负载均衡组件`ribbon/feign`、断路器组件`hystrix`以及应用网关组件`zuul`，其中最核心的就是注册中心`eureka`，至于原因想必大家都能猜出来，因为其他几个组件的功能实现基本上都是依赖于`eureka`展开的，可以说离开了`eureka`注册中心，其他组件基本上都无法正常工作了。

### 回顾总结

今天回顾的方式也是从一张脑图开始，这张脑图主要展示了各个组件的启用流程和步骤，需要脑图源文件的小伙伴，公众号回复【spring-cloud总结】即可获取。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210808163210.png)

#### 内容纲要

##### 注册中心

###### eureka

- 服务端

  - 引入依赖

    ```
    spring-cloud-starter-netflix-eureka-server
    ```

    

  - 启用组件

    ```
    @EnableEurekaServer
    ```

    

  - 核心配置

    - 注册服务器主机名称

      ```
      eureka.instance.hostname
      ```

      

    - 是否注册给服务中心

      ```
      eureka.client.register-with-eureka
      ```

      

    - 是否检索服务

      ```
      eureka.client.fetch-registry
      ```

      

    - 治理客户端服务域

      ```
      eureka.client.service-url.defaultZone
      ```

      

###### eureka客户端

- 服务发现/注册

  - 引入依赖

    ```
    spring-cloud-starter-netflix-eureka-client
    ```

    

  - 启用组件

    - 低版本需要启用

      ```
      @EnableDiscoveryClient
      ```

      

  - 核心配置

    - 同服务端，通常我们只配置注册中心的地址

      ```
      eureka.client.service-url.defaultZone
      ```

      

  - 其他

    - 如果需要spring cloud监测服务运行状态，需要引入监控组件

      ```
      spring-boot-starter-actuator
      ```

      

##### 负载均衡

###### ribbon

- 引入依赖

  ```
  spring-cloud-starter-netflix-ribbon
  ```

  

  - 引入eureka客户端组件及配置

- 注入`RestTemplate`

  - 在注入`RestTemplate`时，在实例方法上加上负载均衡注解

    ```
    @LoadBalanced
    ```

    

- 通过`RestTemplate`访问相关访问

  - 访问服务时需要指定服务`id`

###### feign

- 声明式调用

  - 引入依赖

    ```
    spring-cloud-starter-openfeign
    ```

    

  - 引入`eureka`客户端组件及配置

  - 启用组件

    ```
    @EnableFeignClients
    ```

    

  - 声明目标服务接口

    - 指定服务id

      ```
      @FeignClient("user-service")
      ```

      

    - 指定接口

      - ```
        @GetMapping("/user/{id}")
        ```

      - 方法入参

  - 注入声明接口，并调用

##### 网关

###### zuul

- 核心依赖

  ```
   spring-cloud-starter-netflix-zuul
  ```

  

- 引入`eureka`客户端组件及配置

- 启用组件

  ```
  @EnableZuulProxy
  ```

  

- 服务访问

  - 通过应用网关访问所有服务
  - 访问地址：应用网关服务地址+服务注册`id  ` + 接口地址

- 扩展知识

  - 配置访问规则

    ```
    zuul.routes.product-service.path
    ```

    

  - 配置服务地址

    ```
    zuul.routes.product-service.url
    ```

    

  - 指定服务`id`

    ```
    zuul.routes.product-service.service-id
    ```

    

##### 熔断器

###### hystrix

- 核心依赖

  ```
  spring-cloud-starter-netflix-hystrix
  ```

  

- 启用组

  ```
   @EnableCircuitBreaker
  ```

  

- 接口启用熔断机制

  - 对应方法增加`@HystrixCommand`注解

    - 可以在注解中指定熔断回调方法

      ```
      @HystrixCommand(fallbackMethod = "error")
      ```

      

    - 可以设定熔断相关配置

      - 超时时间

##### hystrix-dashboard

- 核心依赖

  ```
  spring-cloud-starter-netflix-hystrix-dashboard
  ```

  

- 启用组件

  ```
  @EnableHystrixDashboard
  ```

  

- 添加监控主机

  - 客户端引入`actuator`监控组件

  - 添加主机地址

    - `turbine`集群

      ```
      https://turbine-hostname:port/turbine.stream
      ```

      

    - `turbine`集群中某一个节点

      ```
      https://turbine-hostname:port/turbine.stream?cluster=[clusterName]
      ```

      

    - 单节点

      ```
      https://hystrix-app:port/actuator/hystrix.stream
      ```



### 总结

好了，回顾总结就到这里，今天主要是把之前的知识点过一遍，加深下相关知识的印象，如果还有小伙伴已经忘记了，可以点击下面相关知识的链接进行回顾：