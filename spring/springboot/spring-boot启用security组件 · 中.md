# spring-boot启用security组件 · 中

### 前言

昨天我们分享了`spring-boot`启用`security`组件的一些基础知识，演示了`security`的基本配置和简单用法，虽然也可以应用于实际开发，但还是过于简单，并不能真正发挥`sercurity`的作用，所以今天我们还要继续深挖`security`的其他配置和用法。目前，我计划花三天时间分享`security`相关知识点，不过具体还是要看实际情况。

好了，话不多说，我们直接开整。

### security

#### 用户名及密码配置补充

开始之前，我们先补充一个`security`组件密码和用户名配置的知识点，昨天我们分享了通过配置类整合我们自己的用户数据，在翻看`spring boot`相关书籍的时候，我发现它还有另外一种方式配置用户名和密码——配置文件，配置方式也很简单，就是在我们的`application.properties`文件中添加如下配置：

```properties
spring.security.user.name=myuser
spring.security.user.password=l23456
```

但是，需要把我们昨天加的配置类和`service`先注释掉，否则会有冲突。在我实际测试过程中，我发现只要实现了`UserDetailsService`类，加上`@service`注解（不需要配置类），其实已经相当于自定义了`security`组件的用户数据，只是后台会报错误：

![](https://gitee.com/sysker/picBed/raw/master/20210721082251.png)

所以我们还是需要通过配置类设定加密器，关于用户名和密码配置，还有另外一种方式，也是基于配置类的：

```java
protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth.inMemoryAuthentication().passwordEncoder(new BCryptPasswordEncoder()).withUser("syske").password("123456");
        }
```

这种方式和配置文件的方式差不多一样，但是配置文件是支持多用户配置的：

```java
auth.inMemoryAuthentication().passwordEncoder(new BCryptPasswordEncoder())
                .withUser("syske").password("123456").and()
                .withUser("admin").password("admin");
```

#### 配置登录页面和资源权限控制

下面我们分享`security`的另一个配置组件，这个组件的作用主要是配置页面和用户可访问的资源，我们可以在这个方法下设置用户登录页。

默认配置如下：

```java
protected void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests().anyRequest().authenticated().and()
                .formLogin().and()
                .httpBasic();
    }
```

