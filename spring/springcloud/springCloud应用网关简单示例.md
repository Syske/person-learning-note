# springCloud应用网关简单示例

近来工作不是很忙，加上空闲时间比较多，想好好了解下springCloud相关知识，今天就从网关系统开始吧。开始之前，我们先简单介绍下什么是微服务。

### 什么是微服务

我们先看下微服务的发展历史，根据维基百科的介绍，可以整理出如下信息：

- 2005年：Dr. PeterRodgers在Web ServicesEdge大会上提出了“Micro-Web-Services”的概念。
- 2011年：一个软件架构工作组使用了“microservice”一词来描述一种架构模式。
- 2012年：同样是这个架构工作组，正式确定用“microservice”来代表这种架构。
- 2012年：ThoughtWorks的James Lewis针对微服务概念在QCon San Francisco 2012发表了演讲。
- 2014年：James Lewis和Martin Flower合写了关于微服务的一篇学术性的文章，详细阐述了微服务。

由此可以看出微服务并非是一个新名词，它火起来是因为martin fowler和James Lewis，但他们并非是微服务的创始人，只是他们在2014年的时候，写了一篇博客，系统地介绍了微服务，同时将微服务和传统架构进行了比较，之后微服务便开始蓬勃发展，很难说是不是他们推动了微服务的火热发展，但微服务的发展，他们功不可没。

在Martin的博客中，他们是这样解释微服务的：

> 微服务架构样式[[1\]](https://martinfowler.com/articles/microservices.html#footnote-etymology)是一种将单个应用程序开发为一组小服务的方法，每个小服务都在自己的进程中运行并与轻量级机制（通常是HTTP资源API）进行通信。这些服务围绕业务功能构建，并且可以由全自动部署机制独立部署。这些服务几乎不需要集中管理，可以用不同的语言编写并使用不同的数据存储技术。

简单来说，微服务就是一种软件架构方式，其理念就是将服务划分成更细小的微粒单元，然后独立部署。关于微服务的详细介绍，我已经在写另外一篇博客了，本来打算今天发那个的，但由于时间安排的问题，还没写完，所以今天就先不发了，等下次。

#### springCloud

这里还需要介绍下springCloud的相关知识，springCloud是spring官方的微服务解决方案，致力于为典型的用例和扩展机制提供良好的开箱即用体验。更多信息，你要自己去查资料了。springCloud集成了如下模块：

- 配置管理（configuration management）
- 服务发现（service discovery）
- 断路器（circuit breakers）
- 智能路由（intelligent routing）
- 微代理（micro-proxy）
- 控制总线（control bus）
- 一次性令牌（one-time tokens）
- 全局锁（global locks）
- 分布式选主（leadership election）
- 分布式会话（distributed sessions）
- 群集状态（cluster state）

上面这些都是springCloud官方给出的，当然更多模块需要去看官方文档，今天我们要讲的应用网关从功能上划分，包括智能路由、断路器等模块

### 应用网关基本知识点

首先我查了相关资料，整理了gateway的基本知识点：

#### 定义

首先我们看下什么是Spring Cloud Gateway，官方文档给出的解释是：

> 提供了一个用于在Spring MVC之上构建API网关的库。Spring Cloud Gateway旨在提供一种简单而有效的方法来路由到API，并为它们提供横切关注点，例如：安全性，监视/指标和弹性

#### 特性

Spring Cloud Gateway 产品特点:

- 基于Spring Framework 5、Project Reactor和Spring Boot 2.0构建
- 能够在任何请求属性上匹配路由。
- 对明确指定的路由进行断言过滤。
- Hystrix断路器集成。
- Spring Cloud DiscoveryClient集成
- 易于编写的断言和过滤器
- 请求速率限制
- 路径重写

#### 路由配置

gateway支持两种方式的配置，一种是在application.yml文件中配置，另外还可以通过配置类的方式配置路由规则：

##### application.yml

```yaml
spring:
  cloud:
    gateway:
      routes:
      - id: after_route
        uri: https://example.org
        predicates:
        - Cookie=mycookie,mycookievalue
```

其中，id指的是路由id，可以随意指定，但不能重复，必须保证唯一；uri指的是目标主机，也就是请求转发的目的主机；predicates指的是我们的路由规则，也叫断言，具体的规则，后面再研究。当请求参数符合你配置的断言规则时，就会把相应的请求转发至你配置的目标主机上。

##### 配置类

在本次示例中，我采用的是配置类的方式，如果你的配置类和我的一样，那么当你访问路径为`/hello/`开头的任意服务时，请求将被转发至`127.0.0.1:8888`的地址上，比如你服务地址是：`http://127.0.0.1:8080/hello/helloWord`，那么最终访问的地址是``http://127.0.0.1:8888/hello/helloWord``

```java
@Configuration
public class GatewayConfig {
    @Bean
    public RouteLocator myRoutes(RouteLocatorBuilder builder) {
        return builder.routes()
                .route(p -> p
                        .path("/hello/**")
                        .filters(f -> f.addRequestHeader("Hello", "World"))
                        .uri("http://127.0.0.1:8888"))
                .build();
    }
}
```



### 创建项目

这里我们选择spring Initializr来创建：![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200520153630.png)

填写项目信息：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200520153802.png)

选择spring cloud Routing >> gateway：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200520153839.png)

完整依赖如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.3.0.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>io.github.syske</groupId>
    <artifactId>api-gateway-demo</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>api-gateway-demo</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>1.8</java.version>
        <spring-cloud.version>Hoxton.SR4</spring-cloud.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-gateway</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
            <exclusions>
                <exclusion>
                    <groupId>org.junit.vintage</groupId>
                    <artifactId>junit-vintage-engine</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
    </dependencies>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${spring-cloud.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>
```

