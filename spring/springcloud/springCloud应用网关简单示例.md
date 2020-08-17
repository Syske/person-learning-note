# springCloud应用网关Gateway简单示例

近来工作不是很忙，加上空闲时间比较多，想好好了解下springCloud相关知识，今天就从网关系统开始吧。首先我查了相关资料，整理了gateway的基本知识点：

### 基本知识点

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

其中，id指的是路由id，可以随意指定，但不能重复，必须保证唯一；uri指的是目标主机，也就是请求转发的目的主机；predicates指的是我们的路由规则，也叫断言，具体的规则，后面再研究。

##### 配置类

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

这里我们选择spring Initializr来创建：![](https://gitee.com/sysker/picBed/raw/master/images/20200520153630.png)

填写项目信息：

![](https://gitee.com/sysker/picBed/raw/master/images/20200520153802.png)

选择spring cloud Routing >> gateway：

![](https://gitee.com/sysker/picBed/raw/master/images/20200520153839.png)

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

