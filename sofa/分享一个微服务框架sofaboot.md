## 前言

大家应该都知道，最近我刚入职新公司，所以有好多东西要去学习，`SOFABoot`作为一个比较核心的框架，应该是我后面技术攻坚的重点对象，今天我们就先来简单了解下。



## 正文

### SOFABoot是什么

`SOFABoot` 是蚂蚁金服开源的基于 `Spring Boot` 的研发框架，它在 `Spring Boot` 的基础上，提供了诸如 `Readiness Check`，类隔离，日志空间隔离等能力。在增强了 `Spring Boot` 的同时，``SOFABoot` 提供了让用户可以在 `Spring Boot` 中非常方便地使用 `SOFA` 中间件的能力。

#### 功能描述

`SOFABoot` 在 `Spring Boot` 基础上，提供了以下能力：

- 扩展 `Spring Boot` 健康检查的能力：在 `Spring Boot` 健康检查能力基础上，提供了 `Readiness Check` 的能力，保证应用实例安全上线。
- 提供模块化开发的能力：基于 `Spring` 上下文隔离提供[模块化开发](https://www.sofastack.tech/projects/sofa-boot/modular-development)能力，每个 `SOFABoot` 模块使用独立的 `Spring` 上下文，避免不同 `SOFABoot` 模块间的 `BeanId` 冲突。
- 增加模块并行加载和 `Spring Bean` 异步初始化能力，加速应用启动；
- 增加日志空间隔离的能力：中间件框架自动发现应用的日志实现依赖并独立打印日志，避免中间件和应用日志实现绑定，通过 [sofa-common-tools](https://github.com/sofastack/sofa-common-tools) 实现。
- 增加类隔离的能力：基于 [SOFAArk](https://github.com/sofastack/sofa-ark) 框架提供类隔离能力，方便使用者解决各种类冲突问题。
- 增加中间件集成管理的能力：统一管控、提供中间件统一易用的编程接口、每一个 `SOFA` 中间件都是独立可插拔的组件。
- 提供完全兼容 `Spring Boot`的能力：``SOFABoot` 基于 `Spring Boot` 的基础上进行构建，并且完全兼容 `Spring Boot`。

#### 应用场景

`SOFABoot` 本身就脱胎于蚂蚁金服内部对于 `Spring Boot` 的实践，补充了 `Spring Boot` 在大规模金融级生产场景下一些不足的地方，所以 `SOFABoot` 特别适合于这样的场景。

当然，`SOFABoot` 的每个组件都是可选的，用户可以灵活选择其中的功能来使用，比如如果仅仅想在 `Spring Boot` 下面引入 `SOFA` 中间件，可以不需引入 `SOFABoot` 中的类隔离能力。



## 简单示例

接下来我们简单看下如何用`SOFABoot`构建我们的项目，这里我们直接构建`rpc`项目。`SOFABoor`本身就是一个比较强大，但是也比较复杂的框架，所以为了能够嚼烂它，我们先挑软的来。

下面是`SOFARPC`的架构图：

![](https://gitee.com/sysker/picBed/raw/master/images/20210411111551.png)

### 创建项目

这里我们创建一个`spring boot`项目，这里我们只需要引入`starter-web`即可：

![](https://gitee.com/sysker/picBed/raw/master/images/20210411104743.png)

创建完成后`pom`文件的依赖如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>io.github.syske</groupId>
    <artifactId>sofaboot-rpc-demo2</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>sofaboot-rpc-demo2</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>1.8</java.version>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <spring-boot.version>2.3.7.RELEASE</spring-boot.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
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
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>${spring-boot.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.8.1</version>
                <configuration>
                    <source>1.8</source>
                    <target>1.8</target>
                    <encoding>UTF-8</encoding>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <version>2.3.7.RELEASE</version>
                <configuration>
                    <mainClass>io.github.syske.sofabootrpcdemo2.SofabootRpcDemo2Application</mainClass>
                </configuration>
                <executions>
                    <execution>
                        <id>repackage</id>
                        <goals>
                            <goal>repackage</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>

</project>
```



### 修改依赖

首先我们要增加`parent`节点，节点配置的是`sofaboot-dependencies`:

```xml
<parent>
    <groupId>com.alipay.sofa</groupId>
    <artifactId>sofaboot-dependencies</artifactId>
    <version>3.1.0</version>
</parent>
```

然后增加`rpc-sofa`的依赖

```xml
<dependency>
    <groupId>com.alipay.sofa</groupId>
    <artifactId>rpc-sofa-boot-starter</artifactId>
</dependency>
```

### 创建facade接口

`facade`就是`rest`接口中的`service`

```java
/**
 * @program: sofaboot-rpc-demo2
 * @description: hello
 * @author: syske
 * @create: 2021-04-11 10:55
 */
public interface HelloService {
    String sayHello(String name);
}
```

### 创建服务提供者

```java
/**
 * @program: sofaboot-rpc-demo2
 * @description: hello服务实现类
 * @author: syske
 * @create: 2021-04-11 10:59
 */
@SofaService(interfaceType = HelloService.class, bindings = { @SofaServiceBinding(bindingType = "bolt") })
@Service
public class HelloServiceImpl implements HelloService {
    @Override
    public String sayHello(String name) {
        return name + ", hello!";
    }
}
```

`SofaService`的作用是注册`sofa`服务，其中`SofaServiceBinding`的作用是指定服务注册协议，目前支持 `bolt`，`RESTful`，`dubbo`，`H2C`，`jvm`，不指定的话，默认就是`jvm`，其中 `bolt` 是蚂蚁金融服务集团开放的基于 `Netty` 开发的网络通信框架。这里我们用的也是`bolt`。

### 添加注册中心配置

根据`SOFARPC`架构图，我们知道`SOFARPC`是需要注册中心的，所以这里我们指定`zookeeper`作为注册中心：

```properties
com.alipay.sofa.rpc.registry.address=zookeeper://127.0.0.1:2181
```

当然`SOFABoot`也支持其他注册中心，比如`nocas`

### 启动

项目本身就是基于`spring boot`项目，所以启动方法与启动`spring boot`项目一样。

#### 依赖报错

如果启动报如下错误：

```sh
***************************
APPLICATION FAILED TO START
***************************

Description:

An attempt was made to call the method org.springframework.core.type.AnnotationMetadata.introspect(Ljava/lang/Class;)Lorg/springframework/core/type/AnnotationMetadata; but it does not exist. Its class, org.springframework.core.type.AnnotationMetadata, is available from the following locations:

    jar:file:/E:/TheServer/repository/org/springframework/spring-core/5.1.2.RELEASE/spring-core-5.1.2.RELEASE.jar!/org/springframework/core/type/AnnotationMetadata.class

It was loaded from the following location:

    file:/E:/TheServer/repository/org/springframework/spring-core/5.1.2.RELEASE/spring-core-5.1.2.RELEASE.jar


Action:

Correct the classpath of your application so that it contains a single, compatible version of org.springframework.core.type.AnnotationMetadata
```

请删除`pom`中的如下配置后重新启动：

```xml
 <dependencyManagement>
     <dependencies>
         <dependency>
             <groupId>org.springframework.boot</groupId>
             <artifactId>spring-boot-dependencies</artifactId>
             <version>${spring-boot.version}</version>
             <type>pom</type>
             <scope>import</scope>
         </dependency>
     </dependencies>
</dependencyManagement>
```

导致找个错误的原因是重复依赖，初步推测可能是因为`SOFABoot`已经包含了该依赖，再次依赖就会报错。

#### 注册中心报错

因为本项目依赖注册中心，所以在启动项目前请先启动注册中心，否则会报如下错误：

```sh
2021-04-11 11:33:09.640  WARN 6096 --- [127.0.0.1:2181)] org.apache.zookeeper.ClientCnxn          : Session 0x0 for server null, unexpected error, closing socket connection and attempting reconnect

java.net.ConnectException: Connection refused: no further information
	at sun.nio.ch.SocketChannelImpl.checkConnect(Native Method) ~[na:1.8.0_251]
	at sun.nio.ch.SocketChannelImpl.finishConnect(SocketChannelImpl.java:717) ~[na:1.8.0_251]
	at org.apache.zookeeper.ClientCnxnSocketNIO.doTransport(ClientCnxnSocketNIO.java:361) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
	at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1081) ~[zookeeper-3.4.6.jar:3.4.6-1569965]
```

#### 查询服务是否注册成功

启动成功后，我们通过`zkCli`连接`zookeeper`确认服务是否注册成功：

```sh
 $ ls /sofa-rpc
 $ ls /sofa-rpc/io.github.syske.sofabootrpcdemo2.facade.HelloService/providers
```

如果注册成功，显示结果应该是这样的：

![](https://gitee.com/sysker/picBed/raw/master/images/20210411114315.png)

如果还有小伙伴不知道如何使用`zookeeper`可以私信我。



### 测试

这里我偷个懒就不写服务消费者了，直接在测试用例中调用，为了能在`zookeeper`中查看服务消费者，我这里加了一些循环：

```java
@SpringBootTest
class SofabootRpcDemo2ApplicationTests {

    @Test
    void contextLoads() {
        int i = 0;
        long start = System.currentTimeMillis();
        while(i < 10000) {
            System.out.println(sayClientAnnotation("test"));
            i++;
        }
        long stop = System.currentTimeMillis();
        System.out.println("用时：" + (stop - start));
    }

    @SofaReference(interfaceType = HelloService.class, binding = @SofaReferenceBinding(bindingType = "bolt"))
    private HelloService helloService;


    public String sayClientAnnotation(String str) {

        String result = helloService.sayHello(str);

        return result;
    }
}
```

这里需要解释的是`SofaReference`的作用是发现服务，一般就是远程调用的时候发现服务的，它和`SofaService`是对应的，注册的服务和调用的服务必须一致才能正常调用成功。



## 结语

其实，目前我对`SOFABoot`的认知还比较浅显，后面还需要进一步的探索和研究，当然同步增强的还有`RPC`相关的知识点，后面我想先去了解下`restful`和`rpc`协议的区别，目前我就知道相比于`restful`协议（三次握手）`rpc`效率更高，响应速度更快，所以这块的知识点还需要进一步加强，然后再深入了解`SOFABoot`、`Spring boot`相关内容，从源码层面更深入认识他们，当然与之相关的组件也在我们后续研究学习的范畴之中。好了，今天就先到这里吧，小伙伴们周末愉快呀！🥰😜😝



示例代码获取还是老地方：

```
https://github.com/Syske/learning-dome-code
```

