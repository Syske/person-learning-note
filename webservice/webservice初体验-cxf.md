#### 前言

最近一段时间，说忙也不是很忙，说闲但确实很少有时间能静下心来写点东西。但于我而言，做任何仪式感很重要，就算没时间坚持，那仪式感也不能丢，这是一种态度，也是最后的底线。今天的这篇推文，是很久以前就实践过了，前几天又整理了一下，上周没有发，本周必须要更新，不敢再堕落了，毕竟已经2020年了。好了开始正题吧。

#### 1、依赖环境

```xml
      <dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>4.11</version>
      <scope>test</scope>
    </dependency>
    
       <dependency>
            <groupId>org.apache.cxf</groupId>
            <artifactId>cxf-rt-frontend-jaxws</artifactId>
            <version>${cxf.version}</version>
        </dependency>
        <dependency>
            <groupId>org.apache.cxf</groupId>
            <artifactId>cxf-rt-transports-http</artifactId>
            <version>${cxf.version}</version>
        </dependency>
        <dependency>
            <groupId>org.apache.cxf</groupId>
            <artifactId>cxf-rt-transports-http-jetty</artifactId>
            <version>${cxf.version}</version>
        </dependency>
        <dependency>
            <groupId>org.apache.cxf</groupId>
            <artifactId>cxf-rt-features-logging</artifactId>
            <version>${cxf.version}</version>
        </dependency>

    <!-- https://mvnrepository.com/artifact/org.apache.logging.log4j/log4j-core -->
    <dependency>
      <groupId>org.apache.logging.log4j</groupId>
      <artifactId>log4j-core</artifactId>
      <version>2.11.1</version>
    </dependency>
    
    <dependency>
      <groupId>org.apache.logging.log4j</groupId>
      <artifactId>log4j-slf4j-impl</artifactId>
      <version>2.11.1</version>
      <scope>test</scope>
    </dependency>   
```

**注意：** 上面的写法是maven加载包的方式，如果不想创建maven项目，可以直接把cxf/lib下的所有包加载到你的项目中也是可以的

#### 2、基本写法

```java
@WebService()
@SOAPBinding(style = SOAPBinding.Style.RPC)
public interface MyService {
    /**
     * 人员基本信息查询校验
     *
     * @param name
     * @return String
     * @throws GeneralException
     */
    @WebMethod
    String sayHello(@WebParam(name = "name") String name);
}
```

- **注意**：如果action不清楚的话，建议不写

##### 实现类：

```java
public class MyserviceImpl implements Myservice {
    @Override
public String sayHello(String name) {
    return name + ",Hello!";
}
```

**注意：**

> 实现类必须和接口在同一级目录下，否则会出现参数无法被识别的情况

#### 3、发布方式

- (1).默认的发布方式

我发布就是用的这种方式，将发布的代码写在监听器里，这种方式最简单

```java
public class StartListener implements ServletContextListener {
private Logger log = LogManager.getLogger(StartListener.class);
    private final Myservice myservice = new MyserviceImpl();
    private Endpoint endpoint = null;
    String address="http://localhost:7001/myservice";
    @Override
    public void contextInitialized(ServletContextEvent servletContextEvent) {
            endpoint = Endpoint.publish(address, myservice);
            log.info("发布MyserviceImpl webservice成功，地址：" + address);
    }

    @Override
    public void contextDestroyed(ServletContextEvent servletContextEvent) {
        if (this.endpoint.isPublished())
            this.endpoint.stop();
        log.error("服务被销毁……");
    }
}
```

- （2）spring发布

  - 1）引入Spring包

  加入如下依赖

  ```xml
         <dependency>
              <groupId>org.springframework</groupId>
              <artifactId>spring-context</artifactId>
              <version>${spring.version}</version>
          </dependency>
          <dependency>
              <groupId>org.springframework</groupId>
              <artifactId>spring-web</artifactId>
              <version>${spring.version}</version>
          </dependency>
  ```

  或者直接引入二进制包

  ```
  spring-aop-5.1.4.RELEASE.jar
  spring-beans-5.1.4.RELEASE.jar
  spring-context-5.1.4.RELEASE.jar
  spring-core-5.1.4.RELEASE.jar
  spring-expression-5.1.4.RELEASE.jar
  spring-web-5.1.4.RELEASE.jar
  ```

  - 2）在classPath下添加applicationContext-cxf.xml配置文件

 ```xml
<?xml version="1.0" encoding="UTF-8"?>  
<beans xmlns="http://www.springframework.org/schema/beans"  
    xmlns:amq="http://activemq.apache.org/schema/core" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  
    xmlns:jaxws="http://cxf.apache.org/jaxws" xmlns:soap="http://cxf.apache.org/bindings/soap"  
    xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd  
        http://cxf.apache.org/jaxws http://cxf.apache.org/schemas/jaxws.xsd"> <!-- 这里配置的是webservice的实现类， --> 
  <!--相当于：JaxWsServerFactoryBean factory = new JaxWsServerFactoryBean();   -->
<jaxws:server address="/" serviceClass="lss.medicare.ydjy.ejb.YDJYHospServiceBean">  
    <!-- 配置消息拦截器 -->
    <!-- 这种方式已经过期 -->
  	<!--
    <jaxws:inInterceptors>  
        <bean class="org.apache.cxf.interceptor.LoggingInInterceptor"></bean>  
    </jaxws:inInterceptors>  
    <jaxws:outInterceptors>  
        <bean class="org.apache.cxf.interceptor.LoggingOutInterceptor"></bean>  
    </jaxws:outInterceptors>  
    -->
        <!-- 这个是替代类 -->
    <jaxws:features>
        <bean class="org.apache.cxf.ext.logging.LoggingFeature"/>
    </jaxws:features>
</jaxws:server>
</beans>  
 ```

- 3）在web.xml中添加如下配置

```xml
<context-param>  
    <param-name>contextConfigLocation</param-name>  <!-- 
    这里配置我们上面添加的配置文件，保证配置可以正常加载
    -->
    <param-value>classpath:applicationContext-cxf.xml</param-value>  
</context-param>  
<listener>
    <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
</listener>
<servlet>
    <servlet-name>cxf</servlet-name>
    <servlet-class>org.apache.cxf.transport.servlet.CXFServlet</servlet-class>
    <load-on-startup>1</load-on-startup>
</servlet>
<servlet-mapping>
    <servlet-name>cxf</servlet-name>
    <!-- 这里配置的是访问路径，我下面的配置的访问路径是  http://127.0.01:9901/webservice/webservice?wsdl -->
    <url-pattern>/webservice/*</url-pattern>
</servlet-mapping>
```

**说明：** 配置完成就可以启动你的服务了，如果没有意外，服务已经可以正常考虑

#### 4、注意事项

####  4.1、客户端兼容性考虑：<br>

- 因为我这边的需求是要兼容旧版本的webservice(编码格式encoded，也就是weblogic 12C之前的版本)，所以单使用cxf并没有解决我的问题，查阅很很多资料，搜索了很多博客，也尝试了很多方法，最后我的解决方案是引入axis1.4来生成客户端，来兼容老版本的webservice，以下是引入axis的操作：

##### 依赖

```xml
  <dependency>
    <groupId>org.apache.axis</groupId>
    <artifactId>axis</artifactId>
    <version>1.4</version>
</dependency>

<dependency>
    <groupId>com.pansky.axis</groupId>
    <artifactId>jaxrpc</artifactId>
    <version>1.0.0</version>
</dependency>

<!-- https://mvnrepository.com/artifact/commons-logging/commons-logging -->
    <dependency>
        <groupId>commons-logging</groupId>
        <artifactId>commons-logging</artifactId>
        <version>1.1.1</version>
    </dependency>
    <!-- https://mvnrepository.com/artifact/commons-discovery/commons-discovery -->
    <dependency>
        <groupId>commons-discovery</groupId>
        <artifactId>commons-discovery</artifactId>
        <version>0.2</version>
    </dependency>
```

**注意：**<br>
1、这里需要注意的是除了引入axis的包还要引入jaxrpc.jar这个包，当然这包在axis的lib下有，如果你本地用maven的话需要你手动添加到本地仓库，不是很清楚网上有没有，反正我是自己添加的；<br>
2、这里还要添加的是commons-logging和commons-discovery，因为axis1.4依赖这两个包，不添加的话启动会报错<br>
3、这一点和你发布的环境有关，因为我发布的是weblogic，应该这样说吧，都会有冲突，但是本地没有任何冲突，但是到正式环境启动的时候提示javax.xml.namespace.QName冲突，因为在jdk的rt.jar包下用这个类，在jaxrpc.jar中也存在，最后我的解决方法简单粗暴：<br>
 **删除jaxrpc.jar下的这个类，因为我的项目完全没有用的这里包下的这个类，所以问题解决了，也没有其他问题**


 ##### 接口Java客户端代码生成

 ```sh
 wsdl2java -p io.github.syske.webservice.client -d java -client http://127.0.0.1/webservice
 ```

 > -p   包名<br>
 > -d   保存路径<br>
 > -client 服务端地址<br>