### springboot自定义注解

注解（Annotation）对做java开发的小伙伴肯定不陌生，不能说熟悉，但一定在学习或者做项目的过程中有所耳闻，特别是随着springboot框架的大火，“约定大于配置”的开发理念被越来越多的人所喜爱。当然使用注解的最重要的好处就是减少代码的侵入，降低系统耦合性，当然就这一个理由就足够了。

在没有详细了解注解，没有自己定义注解，没有应用自定义注解之前，我对注解的认知仅仅停留在它是一种标记，特别是在springboot中，通过注解我们可以免去繁琐的配置过程，简化开发流程，但现在我发现自定义注解如果真的用的好，可以解决很多实际开发过程中的痛点、难点，让我们可以提出更多更合理的非侵入式解决方案，比如方法的鉴权、多数据源的数据源选择。好了，这里我们先不多说了，开始正文。

### 什么是注解

这里要多说些，介绍下注解的一些情况。注解（Annotation）相当于一种标记，在程序中加入注解就等于为程序打上某种标记。标记可以加在包、类、属性、方法、方法的参数以及局部变量上。通过反射可以拿到类、方法、变量上的注解。我们随便打开一个注解，比如springboot里面的Configuration注解：

```java
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Component
public @interface Configuration {
    @AliasFor(
        annotation = Component.class
    )
    String value() default "";

    boolean proxyBeanMethods() default true;
}
```

根据上面的代码，我们可以得出以下结论：

- 创建注解的关键字是@interface
- 注解上也可以加注解
- 注解可以有属性

但注解上加的都是什么注解，都有什么含义呢？这里要引入注解的一个概念——元注解。所谓元注解就是声明在注解上的注解，元注解是注解的一种声明，元注解分别有以下五种：

- **@Retention**：保留期，声明注解的存活时间
  - RetentionPolicy.SOURCE：仅源代码时保留，在编译时会被丢弃忽略
  - RetentionPolicy.CLASS：编译为class时保留，但不会被加载到jvm中
  - RetentionPolicy.RUNTIME：运行环境保留，会被加载到jvm中
- **@Documented**：保留本类中的注解并能够被javadoc识别
- **@Target**：指定注解的添加位置（类/方法/变量等）
  - ElementType.TYPE：类注解
  - ElementType.FIELD：字段注解
  - ElementType.METHOD：方法注解
  - ElementType.PARAMETER：方法内的参数注解
  - ElementType.CONSTRUCTOR：构造方法注解
  - ElementType.LOCAL_VARIABLE：局部变量注解
  - ElementType.ANNOTATION_TYPE：注解注解
  - ElementType.PACKAGE：包注解
  - ElementType.TYPE_PARAMETER
  - ElementType.TYPE_USE
- **@Inherited**：注解是否能够被子类继承

注解的介绍就到这里，我们继续往下看。

### 创建springboot项目

这里其实我不想介绍太多，因为我觉得这些都是很基础的东西，应该是每个小伙伴都会的，但考虑到还有一些小伙伴处在初学阶段，所以我还是会贴出我的项目结构，方便这些小伙伴参考：

首先是项目结构

![](https://gitee.com/sysker/picBed/raw/master/images/20200801085718.png)

pom.xml文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>io.github.syske</groupId>
    <artifactId>custom-annotation-demo</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>custom-annotation-demo</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>1.8</java.version>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <spring-boot.version>2.3.0.RELEASE</spring-boot.version>
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

        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>fastjson</artifactId>
            <version>1.2.61</version>
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
                <configuration>
                    <source>1.8</source>
                    <target>1.8</target>
                    <encoding>UTF-8</encoding>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>
```

### 自定义注解

根据我们注解的介绍，我们在声明注解的时候必须用到元注解，否则这个注解是没有任何意义的。开始定义我们的第一个注解：

```java
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface CheckAuth {
}
```

这样我们的第一个注解就定义好了，包含了两个元注解，一个指明注解的类型，一个指明注解的生存时间，是不是很简单，接下来，我们要开始使用我们的注解。

### 自定义注解应用

我先说下本次示例注解的应用思路：我刚定义的注解是为了方法鉴权操作，所以我把刚定义的注解加在需要进行鉴权操作的方法上，然后定义一个拦截器，拦截器的拦截规则设置为拦截所有，然后在拦截器内进行判断和校验，如果方法有鉴权注解，则进行鉴权操作，否则跳过，具体如下：

拦截器

```java
public class AuthenticationInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        if (handler instanceof HandlerMethod) {
            HandlerMethod handlerMethod = (HandlerMethod) handler;
            if (handlerMethod.hasMethodAnnotation(CheckAuth.class)) {
                System.out.println("有CheckAuth注解");
                String token = request.getParameter("token");
                if (!"ABCDEF12345".equals(token)) {
                    throw new AuthException();
                }
            }
        }
        return true;
    }
}
```

拦截器配置：

```java
 // 鉴权拦截器
registry.addInterceptor(new AuthenticationInterceptor()).addPathPatterns("/**");
```

这里最核心的操作是`handlerMethod.hasMethodAnnotation(CheckAuth.class)`，即判断当前方法是否有`CheckAuth.class`注解。

当然从handler中获取方法也是很重要的一个操作，我们只有从handler中拿到方法，才能判断该方法是否有我们自定义的注解。我们先来看下handler都有哪些类型：

- HandlerMethod：方法
- ResourceHttpRequestHandler：静态资源

根据目前掌握的资料，我还没发现其他类型的handler，后面发现了再补充。

### 总结

好了，今天的内容就到这里，核心内容就是学会自定义注解，然后可以应用自定义注解解决问题。今天提供的思路就是通过自定义注解实现拦截器解耦，即新增方法后只需要在方法上增加鉴权注解即可，无需修改拦截器配置。某个方法不想鉴权，仅需要去掉方法上的鉴权注解即可。好了，大家周末愉快哦！！！