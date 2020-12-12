# shiro与spring的整合

tags: [#shiro, #spring]

上一期，我们分享了如何在项目中使用shiro，了解了shiro的基本用法，但毕竟学习shiro的目的就是在项目中应用shiro，更准确地说是在web项目中应用shiro。那么，今天我们就来探讨一下shiro在spring web项目中的应用，这里依然参考官方sample部分的代码。好了，废话少说，直接开战。

### spring xml方式

首先当然是创建spring项目，这里提供两种方案，一种是通过xml配置的spring项目，一种是纯注解的spring项目。先来说xml配置的方式，为什么要说xml的方式，因为在实际项目应用中，很多公司目前运行的方式还是xml配置的方式，为了我们更好的上手，更好地工作，我们先将xml的方式，当然也是因为目前我们公司采用的就是xml配置的方式。好了，让我们还是吧！

#### 一、创建spring项目（xml方式）

关于spring项目的创建，这里不做过多说明，但我会放上自己的项目结构和各类配置。

##### pom.xml文件

先创建web项目

```xml
<?xml version="1.0" encoding="UTF-8"?>

<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>io.github.syske</groupId>
  <artifactId>shiro</artifactId>
  <version>1.0-SNAPSHOT</version>
  <packaging>war</packaging>

  <name>shiro Maven Webapp</name>
  <!-- FIXME change it to the project's website -->
  <url>http://www.example.com</url>

  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.source>1.7</maven.compiler.source>
    <maven.compiler.target>1.7</maven.compiler.target>
  </properties>

  <dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>4.11</version>
      <scope>test</scope>
    </dependency>
  </dependencies>

  <build>
    <finalName>shiro</finalName>
    <pluginManagement><!-- lock down plugins versions to avoid using Maven defaults (may be moved to parent pom) -->
      <plugins>
        <plugin>
          <artifactId>maven-clean-plugin</artifactId>
          <version>3.1.0</version>
        </plugin>
        <!-- see http://maven.apache.org/ref/current/maven-core/default-bindings.html#Plugin_bindings_for_war_packaging -->
        <plugin>
          <artifactId>maven-resources-plugin</artifactId>
          <version>3.0.2</version>
        </plugin>
        <plugin>
          <artifactId>maven-compiler-plugin</artifactId>
          <version>3.8.0</version>
        </plugin>
        <plugin>
          <artifactId>maven-surefire-plugin</artifactId>
          <version>2.22.1</version>
        </plugin>
        <plugin>
          <artifactId>maven-war-plugin</artifactId>
          <version>3.2.2</version>
        </plugin>
        <plugin>
          <artifactId>maven-install-plugin</artifactId>
          <version>2.5.2</version>
        </plugin>
        <plugin>
          <artifactId>maven-deploy-plugin</artifactId>
          <version>2.8.2</version>
        </plugin>
      </plugins>
    </pluginManagement>
  </build>
</project>

```

##### 引入spring依赖

```xml
<dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-context</artifactId>
      <version>5.1.7.RELEASE</version>
    </dependency>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-web</artifactId>
      <version>5.1.7.RELEASE</version>
    </dependency>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-beans</artifactId>
      <version>5.1.7.RELEASE</version>
    </dependency>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-webmvc</artifactId>
      <version>5.1.7.RELEASE</version>
    </dependency>    
```

##### 添加spring配置：webapp/WEB-INF/spring-servlet.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:mvc="http://www.springframework.org/schema/mvc"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/mvc
        http://www.springframework.org/schema/mvc/spring-mvc.xsd
        http://www.springframework.org/schema/context
        http://www.springframework.org/schema/context/spring-context.xsd">
   <context:component-scan base-package="io.github.syske.shiro"></context:component-scan>

    <bean class="org.springframework.web.servlet.view.InternalResourceViewResolver">
        <property name="prefix" value="/"></property>
        <property name="suffix" value=".jsp"></property>
    </bean>

    <mvc:annotation-driven></mvc:annotation-driven>
    <mvc:default-servlet-handler/>

</beans>
```

##### 在web.xml中配置spring容器

```xml
 <context-param>
        <param-name>contextConfigLocation</param-name>
        <param-value>classpath*:springApplicationContext.xml</param-value>
    </context-param>
    
    <listener>
        <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
    </listener>

    <servlet>
        <servlet-name>spring</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <load-on-startup>1</load-on-startup>
    </servlet>

    <servlet-mapping>
        <servlet-name>spring</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>
```

至此，spring项目创建完成，然后启动下你的spring项目，如果没有问题，那就继续往下看。



#### 二、引入我们今天的主角：shiro和她的小伙伴

##### 引入shiro的依赖包

```xml
<dependency>
      <groupId>org.apache.shiro</groupId>
      <artifactId>shiro-spring</artifactId>
      <version>1.2.6</version>
    </dependency>

    <dependency>
      <groupId>org.apache.shiro</groupId>
      <artifactId>shiro-ehcache</artifactId>
      <version>1.2.6</version>
    </dependency>
    <!-- configure logging -->
    <dependency>
      <groupId>org.slf4j</groupId>
      <artifactId>jcl-over-slf4j</artifactId>
      <version>1.7.24</version>
      <scope>runtime</scope>
    </dependency>
    <dependency>
      <groupId>org.slf4j</groupId>
      <artifactId>slf4j-log4j12</artifactId>
      <version>1.7.24</version>
      <scope>runtime</scope>
    </dependency>
    <dependency>
      <groupId>log4j</groupId>
      <artifactId>log4j</artifactId>
      <version>1.2.17</version>
      <scope>runtime</scope>
    </dependency>

    <dependency>
      <groupId>org.slf4j</groupId>
      <artifactId>slf4j-nop</artifactId>
      <version>1.7.24</version>
    </dependency>

    <dependency>
      <groupId>net.sf.ehcache</groupId>
      <artifactId>ehcache-core</artifactId>
      <version>2.6.11</version>
    </dependency>
```

##### 在web.xml中配置shiro拦截器

这个配置是必须的，没有这个配置，你的项目和shiro半毛钱关系都没有，更不会有什么效果。所以，当哪位小伙伴发现自己的项目没效果的时候，检查下这个配置是否添加了，是否配置正确。

```xml
 <!-- 配置shiro的shiroFilter -->

    <filter>
        <filter-name>shiroFilter</filter-name>
        <filter-class>org.springframework.web.filter.DelegatingFilterProxy</filter-class>
        <init-param>
            <param-name>targetFilterLifecycle</param-name>
            <param-value>true</param-value>
        </init-param>
    </filter>

    <filter-mapping>
        <filter-name>shiroFilter</filter-name>
        <url-pattern>/*</url-pattern>
    </filter-mapping>
```

**注意：**需要注意的一点是，这里的filter-name必须与classpath/springApplicationContext-shiro.xml中ShiroFilterFactoryBean的bean id一致，否项目启动的时候，会提示找不到name为shiroFilter的bean。

当然，如果你非要修改这个name，要让他们不一样，那你必须在filte中添加如下配置:

```xml
 <init-param>
           <param-name>targetBeanName</param-name>
           <param-value>shiroFilter</param-value>
 </init-param>
```

其中，param-value对应你的bean id，否则还是会报相同的错。

##### 添加shiro的配置：classpath/springApplicationContext-shiro.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
    
    <!--
     配置 SecurityManager!
    -->
    
    <bean id="securityManager"  class="org.apache.shiro.web.mgt.DefaultWebSecurityManager"/>    
    
<!--
    配置 ShiroFilter.
    id 必须和 web.xml 文件中配置的 DelegatingFilterProxy 的 <filter-name> 一致.
                      若不一致, 则会抛出: NoSuchBeanDefinitionException. 因为 Shiro 会来 IOC 容器中查找和 <filter-name> 名字对应的 filter bean.
    -->
    <bean id="shiroFilter" class="org.apache.shiro.spring.web.ShiroFilterFactoryBean">
        <property name="securityManager" ref="securityManager"/>

       <property name="filterChainDefinitions">
            <value>
                /login.jsp = anon 
                /shiro/login = anon
                /** = authc
            </value>
        </property>

    </bean> 
</beans>
```

以上配置是最基本的，然后你就可以启动项目了。不出意外的话，你会发现，项目会自动跳转到

login.jsp，当然前提条件是的jsp页面必须存在。以上步骤只是让大家看到，shiro本质上是个拦截器，他会根据你的配置信息，拦截相应的路径，但shiro真正的作用并没有体现出来，下面让我们进一步深入了解吧。

#### 三、创建我们的shiro Controller

这里controller的名字你可以随便起，反正不影响。这里这个controller的作用就是处理我们的的登录请求先上代码：

```java
package io.github.syske.shiro.controller;

import org.apache.shiro.SecurityUtils;
import org.apache.shiro.authc.*;
import org.apache.shiro.session.Session;
import org.apache.shiro.subject.Subject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

/**
 * @program: shiro-spring4
 * @description: shiro 认证授权
 * @create: 2019-10-27 06:13
 */
@Controller
@RequestMapping("/shiro")
public class ShiroController {
    private static final transient Logger log = LoggerFactory.getLogger(ShiroController.class);

    @RequestMapping("/login")
    public String login(@RequestParam(name = "username") String username,
                        @RequestParam(name = "password") String password) {
        // 获取当前用户Subject
        Subject currentUser = SecurityUtils.getSubject();

        // 判断用户是否已经登录
        if (!currentUser.isAuthenticated()) {
            UsernamePasswordToken token = new UsernamePasswordToken(username, password);
            token.setRememberMe(true);
            try {
                currentUser.login(token);
            } catch (AuthenticationException ae) {
                log.error("登录失败：" + ae);
            }
        }
        return "redirect:/list.jsp";
    }
}
```

小伙伴还记得我们分享的第一个shiro示例吗，这里我们再来回顾下shiro的基本认证流程，然后再来解释代码：

```java
// 创建SecurityManager实例工厂
Factory<SecurityManager> factory = new IniSecurityManagerFactory("classpath:shiro.ini");
// 通过工厂创建SecurityManager实例
SecurityManager securityManager = factory.getInstance();
// 将SecurityManager对象传给SecurityUtils
SecurityUtils.setSecurityManager(securityManager);
// 从SecurityUtils中获取Subject
Subject currentUser = SecurityUtils.getSubject();
// 创建密码用户名令牌
UsernamePasswordToken token = new UsernamePasswordToken("lonestarr", "vespa");
// 设置是否记住登录状态
token.setRememberMe(true);
// 用户登录
currentUser.login(token);
```

对照我们的spring配置，你会发现我们只完成了factory、securityManager以及SecurityUtils的设置，对于后面的逻辑，我们并没有实现。这里controller就是用来实现我们后面几个步骤的。参照第一个shiro示例应该可以看明白，这里不做过多解释。

**提示：**这里要提一点的是，shiro的session非常强大，他可以让你在非controller中拿到session，更重要的是他的session包含了HttpServletSession中所有内容，也就是说你不需要通过任何转化或操作，可以直接在shiro的session中拿到你放在HttpServletSession，这样你在工具类中就可以很轻易地拿到session，是不是很完美^_^!

创建完controller，修改完我们的登录页面，再次重启我们的项目，然后随便输入用户名和密码，如果没有什么意外的话，会报错。你没看错，会报错，大致错误提示如下：

```shell
java.lang.IllegalStateException: Configuration error:  No realms have been configured!  One or more realms must be present to execute an authentication attempt.
	at org.apache.shiro.authc.pam.ModularRealmAuthenticator.assertRealmsConfigured(ModularRealmAuthenticator.java:161)
	at org.apache.shiro.authc.pam.ModularRealmAuthenticator.doAuthenticate(ModularRealmAuthenticator.java:264)
	at org.apache.shiro.authc.AbstractAuthenticator.authenticate(AbstractAuthenticator.java:198)
	at org.apache.shiro.mgt.AuthenticatingSecurityManager.authenticate(AuthenticatingSecurityManager.java:106)
	at org.apache.shiro.mgt.DefaultSecurityManager.login(DefaultSecurityManager.java:270)
	at org.apache.shiro.subject.support.DelegatingSubject.login(DelegatingSubject.java:256)
	at io.github.syske.shiro.controller.ShiroController.login(ShiroController.java:27)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.springframework.web.method.support.InvocableHandlerMethod.doInvoke(InvocableHandlerMethod.java:190)
	at org.springframework.web.method.support.InvocableHandlerMethod.invokeForRequest(InvocableHandlerMethod.java:138)
	at org.springframework.web.servlet.mvc.method.annotation.ServletInvocableHandlerMethod.invokeAndHandle(ServletInvocableHandlerMethod.java:104)
	at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.invokeHandlerMethod(RequestMappingHandlerAdapter.java:892)
	at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.handleInternal(RequestMappingHandlerAdapter.java:797)
	at org.springframework.web.servlet.mvc.method.AbstractHandlerMethodAdapter.handle(AbstractHandlerMethodAdapter.java:87)
	at org.springframework.web.servlet.DispatcherServlet.doDispatch(DispatcherServlet.java:1039)
	at org.springframework.web.servlet.DispatcherServlet.doService(DispatcherServlet.java:942)
	at org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:1005)
	at org.springframework.web.servlet.FrameworkServlet.doPost(FrameworkServlet.java:908)
```

错误提示很清楚，我们没有配置realms。那么我们该如何设置realms，设置给谁呢？我们沿着报错信息排查看看，当你找到ModularRealmAuthenticator这个类的代码时，你会发现如下代码：

```java
  protected AuthenticationInfo doAuthenticate(AuthenticationToken authenticationToken) throws AuthenticationException {
        this.assertRealmsConfigured();
        Collection<Realm> realms = this.getRealms();
        return realms.size() == 1 ? this.doSingleRealmAuthentication((Realm)realms.iterator().next(), authenticationToken) : this.doMultiRealmAuthentication(realms, authenticationToken);
    }
```

我们通过继承关系可以看到，ModularRealmAuthenticator的父类并没有realms属性，所以我们应该将realms配给ModularRealmAuthenticator。但是我们依然不知道如何设置，我们来看下ModularRealmAuthenticator又是什么。同样是根据我们的报错信息，通过继承关系，我们发现ModularRealmAuthenticator是Authenticator的实现类，而AuthenticatingSecurityManager有一个属性就是Authenticator，而AuthenticatingSecurityManager底层又实现了SecurityManager接口。到这里，我们的思路就有了，设置顺序应该是这样的：

- 将reamls设置给ModularRealmAuthenticator
- 再将Authenticator(ModularRealmAuthenticator)设置给SecurityManager

#### 四、创建realm

通过分析ModularRealmAuthenticator源码，我们发现realms本质上是集合Realm。在设置SecurityManager的属性的时候，我发现有个realm属性，分析源码发现，当我们只有一个realm时，没必要通过容器的方式注入，但是注意authenticator的realms和securityManager的realm属性不能同时设置，否则会报错。我的配置如下：

```xml
<bean id="securityManager" class="org.apache.shiro.web.mgt.DefaultWebSecurityManager">
        <property name="realm" ref="shiroRealm"/> 
        <!--
<property name="authenticator" ref="authenticator">
            
        </property>
-->
        
    </bean>

    <bean id="shiroRealm" class="io.github.syske.shiro.realms.ShiroRealm"/>
    <!--   
   <bean id="authenticator"
          class="org.apache.shiro.authc.pam.ModularRealmAuthenticator">
        <property name="realms">
            <list>
                <ref bean="shiroRealm"></ref>
            </list>
        </property>
    </bean>
-->
```

本来打算自己创建realm，但又想能不能不自己创建realm，所以我就选了SimpleAccountRealm。创建自己的realm后面再讲，同时也是为了让大家清楚为什么要创建自己的realm。

再次重启我们的项目，然后随意输入用户名和密码，你发现又报错了，大致错误如下：

```verilog
严重: Servlet.service() for servlet [spring] in context with path [] threw exception [Request processing failed; nested exception is org.apache.shiro.authc.UnknownAccountException: Realm [org.apache.shiro.realm.SimpleAccountRealm@6c38d83a] was unable to find account data for the submitted AuthenticationToken [org.apache.shiro.authc.UsernamePasswordToken - 61000004, rememberMe=true].] with root cause
org.apache.shiro.authc.UnknownAccountException: Realm [org.apache.shiro.realm.SimpleAccountRealm@6c38d83a] was unable to find account data for the submitted AuthenticationToken [org.apache.shiro.authc.UsernamePasswordToken - 61000004, rememberMe=true].
	at org.apache.shiro.authc.pam.ModularRealmAuthenticator.doSingleRealmAuthentication(ModularRealmAuthenticator.java:184)
	at org.apache.shiro.authc.pam.ModularRealmAuthenticator.doAuthenticate(ModularRealmAuthenticator.java:267)
	at org.apache.shiro.authc.AbstractAuthenticator.authenticate(AbstractAuthenticator.java:198)
	at org.apache.shiro.mgt.AuthenticatingSecurityManager.authenticate(AuthenticatingSecurityManager.java:106)
	at org.apache.shiro.mgt.DefaultSecurityManager.login(DefaultSecurityManager.java:270)
	at org.apache.shiro.subject.support.DelegatingSubject.login(DelegatingSubject.java:256)
	at io.github.syske.shiro.controller.ShiroController.login(ShiroController.java:27)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.springframework.web.method.support.InvocableHandlerMethod.doInvoke(InvocableHandlerMethod.java:190)
	at org.springframework.web.method.support.InvocableHandlerMethod.invokeForRequest(InvocableHandlerMethod.java:138)
	at org.springframework.web.servlet.mvc.method.annotation.ServletInvocableHandlerMethod.invokeAndHandle(ServletInvocableHandlerMethod.java:104)
	at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.invokeHandlerMethod(RequestMappingHandlerAdapter.java:892)
	at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.handleInternal(RequestMappingHandlerAdapter.java:797)
	at org.springframework.web.servlet.mvc.method.AbstractHandlerMethodAdapter.handle(AbstractHandlerMethodAdapter.java:87)
	at org.springframework.web.servlet.DispatcherServlet.doDispatch(DispatcherServlet.java:1039)
	at org.springframework.web.servlet.DispatcherServlet.doService(DispatcherServlet.java:942)
	at org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:1005)
	at org.springframework.web.servlet.FrameworkServlet.doPost(FrameworkServlet.java:908)

```

错误提示很明显：未知用户名，这也就说明我们配置的realm生效了，至于用户名未知，那是因为我们没有配置任何用户信息，shiro找不到我们的用户信息，所以校验失败。那么用户信息如何设置呢，在哪里设置呢，和上面一样，我们依据错误信息来看源码：

```java
 protected AuthenticationInfo doGetAuthenticationInfo(AuthenticationToken token) throws AuthenticationException {
        UsernamePasswordToken upToken = (UsernamePasswordToken)token;
        SimpleAccount account = this.getUser(upToken.getUsername());
        if (account != null) {
            if (account.isLocked()) {
                throw new LockedAccountException("Account [" + account + "] is locked.");
            }

            if (account.isCredentialsExpired()) {
                String msg = "The credentials for account [" + account + "] are expired";
                throw new ExpiredCredentialsException(msg);
            }
        }

        return account;
    }
```

上面错误的原因本质上是因为SimpleAccountRealm的doGetAuthenticationInfo方法中account为空导致的，而account是通过getUser获取到的，getUser通过在users属性中查找我们当前用户，然后返回查找结果，由于我们并没有给realm设置users属性，所以自然返回结果就是空。先在你应该清楚了，下一步我们该给我们的realm设置users属性。

但是在给SimpleAccountRealm的users注入值的时候，发现该属性无法没有set方法，但是发现有addAccount方法，可以通过手动方式添加用户，但我发现这种方式比较麻烦，毕竟我们用的是spring，手动方式并不方便，至少获取SimpleAccountRealm的bean很麻烦，所以我们直接使用官方的realm宣告失败😂（有想法的童鞋可以自己试一下，写个springContext的工具类，获取到SimpleAccountRealm，然后给他加用户信息就行了）。

下来，我们开始定义自己的realm，通过继承官方的realm来满足自己的特殊需求。直接上代码：

```java
package io.github.syske.shiro.realms;

import org.apache.shiro.authc.*;
import org.apache.shiro.realm.AuthenticatingRealm;
import org.apache.shiro.util.ByteSource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * @program: shiro-spring
 * @description:
 * @create: 2019-10-20 22:12
 */
public class ShiroRealm extends AuthenticatingRealm {

    private static final transient Logger log = LoggerFactory.getLogger(AuthenticatingRealm.class);

    @Override
    protected AuthenticationInfo doGetAuthenticationInfo(AuthenticationToken token)
            throws AuthenticationException {
        log.info("doGetAuthenticationInfo toke" + token);
        UsernamePasswordToken usernamePasswordToken = (UsernamePasswordToken) token;
        // 下面用到的用户名密码在实际应用中对应的是你数据库查到的用户信息，这里为了方便演示，没有配置数据库，关于收据库shiro整合，后期详细讲
        String username = usernamePasswordToken.getUsername();

        String password = null;

        if ("admin".equals(username)) {
            password = "admin";
        } else if ("user".equals(username)) {
            password = "user";
        } else {
            password = "123456";
        }

        if ("unkonw".equals(username)) {
            throw new UnknownAccountException("用户不存在！");
        }

        if ("locked".equals(username)) {
            throw new LockedAccountException("用户被锁定！");
        }

        SimpleAuthenticationInfo info = new SimpleAuthenticationInfo(username, password, getName());
        return info;
    }

}

```

这里我们继承的是AuthenticatingRealm，实现他的doGetAuthenticationInfo方法。关于官方的Realm，我打算抽个时间好好了解熟悉下，到时候详细说明。

然后将我们地realm改成我们刚刚创建的realm，然后重启你的项目。不出意外，你就可以登陆成功了。完美，优秀😂

因为今天确实写的有点太多了，有点像刘姥姥的裹脚布了，所以后面的内容留到后面来讲，提前预告下，也算是给自己立的flag：

- shiro整合数据库
- shiro拦截器详细配置
- shiro各种realm的应用场景

#### 总结

本次写shiro部分的内容其实准备的不是很充分，本身我现在也还在学习shiro，实际项目中有应用，但不是很多，所以对于很多细节的知识点掌握的并不太好，也没有比较深刻的理解，但就这篇博客而言，我觉得我是有收获的，至少提升了我通过源码来学习、来解决问题的能力，更重要的是，还很有可能让一些刚开始学校的小伙伴能避免一些坑，是吧😏