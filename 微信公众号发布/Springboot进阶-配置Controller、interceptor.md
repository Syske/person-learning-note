# Spring boot进阶-配置Controller、interceptor

tags: [#springboot]

### 1、配置SpringBootApplication(对spring boot来说这是最基本)

```java
package io.github.syske.springboot31;

import org.springframework.boot.Banner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Configuration;

@Configuration
@SpringBootApplication
public class SpringBoot31Application {

    public static void main(String[] args) {

        //SpringApplication.run(SpringBoot31Application.class, args);
        SpringApplication application = new SpringApplication(SpringBoot31Application.class);
        //关闭banner，也可以通过在resouces文件夹下添加banner.txt替换banner，
        // banner生成网站
        // http://patorjk.com/software/taag/#p=testall&h=0&f=Chiseled&t=syske
        application.setBannerMode(Banner.Mode.OFF);
        application.run(args);
    }
}
```

这里解释下，上面application.setBannerMode(Banner.Mode.OFF)这行代码是关闭spring boot默认的baaner，然后你就可以配置自己的banner了，只需要把你的banner放在resources文件夹下，名字改为banner.txt即可，然后spring boot启动的时候就可以看到你的自定义banner了，我的banner如下：

```sh
                            __                 
                           /\ \                
  ____   __  __      ____  \ \ \/'\       __   
 /',__\ /\ \/\ \    /',__\  \ \ , <     /'__`\ 
/\__, `\\ \ \_\ \  /\__, `\  \ \ \\`\  /\  __/ 
\/\____/ \/`____ \ \/\____/   \ \_\ \_\\ \____\
 \/___/   `/___/> \ \/___/     \/_/\/_/ \/____/
             /\___/                            
             \/__/                             
```

生成方式链接之一：

> http://patorjk.com/software/taag/

### 2、创建配置类

这里就是本文最核心的地方，所有MVC的配置都将在本类中进行，包括controller、Interceptors、Formatters……当然还有其他配置，这里不做过多说明，想详细了解的小伙伴们可以看下WebMvcConfigurer的其他方法，可以参考spring boot官方文档

> 配置类完整代码

```java
package io.github.syske.springboot31.config;

import io.github.syske.springboot31.formatter.DateFomaters;
import io.github.syske.springboot31.interceptor.SessionInterceptor;
import org.springframework.context.annotation.Configuration;
import org.springframework.format.FormatterRegistry;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.ViewControllerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class Webconfig implements WebMvcConfigurer {
    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        registry.addViewController("/user/login.html").setViewName("login");
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new SessionInterceptor())
                .addPathPatterns("/**")
                .excludePathPatterns("/login","/user/login.html","/bootsrap/**");
    }

    @Override
    public void addFormatters(FormatterRegistry registry) {
        //给当前的Spring容器中添加自定义格式转换器.
        registry.addConverter(new DateFomaters());
    }
}
```

### 3、配置Controller

> controller是在配置类中添加的

- 主要是针对一些仅需要返回页面的Controller，如果需要model操作则不适用

```java
 @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        registry.addViewController("/user/login.html").setViewName("login");
    }
```

- 主要是通过addViewController方法进行添加，方法中传入的是访问的路径，上面配置的访问路径为：http://localhost:8080/user/login.html, setViewName方法设置的是返回的视图名，我的配置对应的是login.html
- 方法内可以配置多个视图模型

### 4、配置DateFomatters

> 自定义的convertor

```java
package io.github.syske.springboot31.formatter;


import org.springframework.core.convert.converter.Converter;
import org.springframework.util.StringUtils;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class DateFomaters implements Converter<String, Date> {



    @Override
    public Date convert(String source) {
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        Date date = null;
        if(!StringUtils.isEmpty(source)) {
            try {
                date = dateFormat.parse(source);
            } catch (ParseException e) {
                e.printStackTrace();
            }
        }
        return date;
    }
}
```

> 将自定义的转化类添加到Spring boot配置中

```java
  @Override
    public void addFormatters(FormatterRegistry registry) {
        //给当前的Spring容器中添加自定义格式转换器.
        registry.addConverter(new DateFomaters());
    }
```

### 5、配置拦截器（Interceptor）

> 自定义拦截器

```java
package io.github.syske.springboot31.interceptor;

import org.springframework.web.servlet.mvc.WebContentInterceptor;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

public class SessionInterceptor extends WebContentInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws ServletException {
        Object username = request.getSession().getAttribute("username");
        if(username != null) {
            return true;
        } else {
            try {
                request.getRequestDispatcher("/user/login.html").forward(request,response);
            } catch (IOException e) {
                e.printStackTrace();
            }
            return false;
        }
    }
}
```

> 将自定义的拦截器添加到Spring boot配置中

```java
 @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new SessionInterceptor())
                .addPathPatterns("/**")
                .excludePathPatterns("/login","/user/login.html","/bootsrap/**");
    }
```

### 6、测试

> 登录拦截测试，以及格式化打印

```java
package io.github.syske.springboot31.controller;

import org.springframework.stereotype.Controller;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.RequestMapping;

import javax.servlet.http.HttpSession;
import java.util.Date;

@Controller
public class LoginController {
    @RequestMapping("/login")
    public String login(String username, Date logindate, HttpSession session) {
        if(!StringUtils.isEmpty(username)) {
            session.setAttribute("username", username);
            System.out.println(logindate);
            return "index";
        }
        return "login";

    }
}
```