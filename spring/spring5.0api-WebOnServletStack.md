这部分文档涵盖对Servlet Stack的支持，构建在Servlet API上并部署到Servlet容器的Web应用程序。单独的章节包括Spring MVC， View技术，CORS支持和WebSocket支持。对于WebSocket，Web应用程序，请转至Web on Reactive Stack.。

# 1.Spring web MVC
## 1.1. 介绍

与Spring Web MVC并列，Spring Framework 5.0引入了一个反应栈，名称为Spring WebFlux的Web框架基于它的源模块 spring-webflux。本节涵盖Spring Web MVC。在下一节 介绍Spring WebFlux。

有关基准信息以及与Servlet容器和Java EE版本的兼容性，请访问Spring Framework Wiki。

## 1.2. DispatcherServlet

Spring MVC，像许多其它Web框架一样，是围绕前端控制器模式设计的，在这个模式中，中心Servlet (DispatcherServlet)提供了一个用于请求处理的共享算法，而实际工作由可配置的委托组件执行。该模型非常灵活，支持多种工作流程。

DispatcherServlet，和任意Servlet一样，需要根据Servlet规范使用Java配置或web.xml声明和映射。反过来，DispatcherServlet使用Spring配置来找到请求映射、视图解析、异常处理等所需的委托组件。

下面是注册和初始化DispatcherServlet的Java配置示例。这个类由Servlet容器自动检测(参见Servlet配置):

```
public class MyWebApplicationInitializer implements WebApplicationInitializer {

    @Override
    public void onStartup(ServletContext servletCxt) {

        // Load Spring web application configuration
        AnnotationConfigWebApplicationContext ac = new AnnotationConfigWebApplicationContext();
        ac.register(AppConfig.class);
        ac.refresh();

        // Create and register the DispatcherServlet
        DispatcherServlet servlet = new DispatcherServlet(ac);
        ServletRegistration.Dynamic registration = servletCxt.addServlet("app", servlet);
        registration.setLoadOnStartup(1);
        registration.addMapping("/app/*");
    }
}
```

> 除了直接使用ServletContext API，你也可以通过继承AbstractAnnotationConfigDispatcherServletInitializer 并且重写特定方法

下面是在web.xml中注册和初始化 DispatcherServlet 的示例：
```
<web-app>

    <listener>
        <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
    </listener>

    <context-param>
        <param-name>contextConfigLocation</param-name>
        <param-value>/WEB-INF/app-context.xml</param-value>
    </context-param>

    <servlet>
        <servlet-name>app</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value></param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>

    <servlet-mapping>
        <servlet-name>app</servlet-name>
        <url-pattern>/app/*</url-pattern>
    </servlet-mapping>

</web-app>
```

> Spring Boot 遵循不同的初始化序列，而不是挂载进 Servlet容器的生命周期，Spring Boot 使用Spring配置来引导自己和嵌入的Servlet容器。在Spring配置中检测过滤器和Servlet声明，并在Servlet容器中注册。有关更多细节，请查看Spring Boot文档。

### 1.2.1 上下文（Context Hierarchy）

DispatcherServlet需要一个WebApplicationContext，一个普通ApplicationContext上下文的扩展，用于它自己的配置。WebApplicationContext有一个ServletContext及其关联的Servlet的链接。它还绑定到ServletContext，以便在需要的时候，应用程序可以使用requestcontext tutils的静态方法来查找WebApplicationContext。

对于许多只有一个WebApplicationContext的应用程序来说，这是简单而充分的。还可以有一个上下文层次结构，其中一个根WebApplicationContext跨多个DispatcherServlet(或其他Servlet)实例共享，每个实例都具有自己的子WebApplicationContext配置。有关上下文层次结构特性的更多信息，请参见ApplicationContext的其他功能。

根WebApplicationContext通常包含需要跨多个Servlet实例共享的基本bean，如数据存储库和业务服务。这些bean实际上是继承的，并且可以在Servlet特定的子WebApplicationContext中被重写(即重新声明)，该上下文通常包含给定Servlet的本地bean:

![image](https://note.youdao.com/yws/api/personal/file/8B1C5D0DECFA4916AD877188217AD891?method=download&shareKey=a72fc856ae3ad4a67769562ef47e3e23)

以下是具有WebApplicationContext层次结构的示例配置：

```
public class MyWebAppInitializer extends AbstractAnnotationConfigDispatcherServletInitializer {

    @Override
    protected Class<?>[] getRootConfigClasses() {
        return new Class<?>[] { RootConfig.class };
    }

    @Override
    protected Class<?>[] getServletConfigClasses() {
        return new Class<?>[] { App1Config.class };
    }

    @Override
    protected String[] getServletMappings() {
        return new String[] { "/app1/*" };
    }
}

```

> 如果不需要应用程序上下文层次结构，则应用程序可以通过getRootConfigClasses()和null从中返回所有配置getServletConfigClasses()。

```
<web-app>

    <listener>
        <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
    </listener>

    <context-param>
        <param-name>contextConfigLocation</param-name>
        <param-value>/WEB-INF/root-context.xml</param-value>
    </context-param>

    <servlet>
        <servlet-name>app1</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>/WEB-INF/app1-context.xml</param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>

    <servlet-mapping>
        <servlet-name>app1</servlet-name>
        <url-pattern>/app1/*</url-pattern>
    </servlet-mapping>

</web-app>
```

> 如果不需要应用程序上下文层次结构，应用程序可能只配置一个“根”上下文，并将contextConfigLocationServlet参数留空。

### 1.2.2 特殊Bean 类型

DispatcherServlet委托特殊的bean来处理请求并呈现相应的响应。我们所说的“特殊bean”是指实现WebFlux框架契约的spring管理的对象实例。它们通常带有内置的契约，但您可以定制它们的属性、扩展或替换它们。


Bean type | 说明
---|---
HandlerMapping | 将请求映射到处理程序以及用于预处理和后处理的拦截器列表 。该映射基于一些标准，其细节因HandlerMapping 实施而异。这两个主要的HandlerMapping实现是RequestMappingHandlerMapping支持@RequestMapping注释的方法，并SimpleUrlHandlerMapping为处理程序维护URI路径模式的显式注册。
HandlerAdapter |帮助DispatcherServlet调用映射到请求的处理程序，而不管实际调用处理程序的方式如何。例如，调用带注释的控制器需要解析注释。a的主要目的HandlerAdapter是屏蔽DispatcherServlet这些细节。
HandlerExceptionResolver | 解决异常的策略，可能将它们映射到处理程序，或HTML错误视图或其他。请参阅异常（Exceptions）。
ViewResolver | 将从处理程序返回的逻辑基于String的视图名称解析为实际View 的呈现给响应的名称。请参阅查看分辨率和查看技术。
LocaleResolver, LocaleContextResolver | 解决Locale客户正在使用的问题，可能还有他们的时区，以便能够提供国际化视图。请参阅区域设置。
ThemeResolver | 解析Web应用程序可以使用的主题，例如，提供个性化布局。请参阅主题（Themes）。
MultipartResolver | 在一些多部分解析库的帮助下解析多部分请求（例如浏览器表单文件上载）的抽象。请参阅Multipart解析器。
FlashMapManager | 存储和检索“输入”和“输出” FlashMap，可用于将属性从一个请求传递到另一个请求，通常是通过重定向。请参阅Flash属性。
