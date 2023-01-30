# Spring boot进阶-配置Controller、interceptor...
tags: [#springboot, #interceptor]

原本今天是要分享`ConversionService`相关内容的，结果下班走的急，忘记将之前写好的内容`push`到仓库里了，所以今天就暂时先不分享相关内容了，不过可以回顾一些和`ConversionService`相关的内容。

今天的内容，原本之前已经分享过了，但是今天看了下，发现很多内容都比较粗糙，我自己看了都有点懵逼，所以就对相关内容做了一些补充，给位小伙伴就权当回顾复习了

### 1、SpringBoot启动banner设置

对`spring boot`来说，容器配置一直是特别基本，但是又特别重要的内容，所以学好`spring boot`是一定要学好容器的相关配置的，下面是关于`banner`的简单配置过程，其中有两个需要注意的地方，一个是关于`banner`内容替换，可以根据自己的需要替换成自己喜欢的`banner`文件，另一个是关于是否启用`banner`的设置，设置为关闭后，启动时将不再打印`banner`信息：
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
        //关闭banner，也可以通过在resouces文件夹下添加banner.txt替换banner，banner生成网站
        // http://patorjk.com/software/taag/#p=testall&h=0&f=Chiseled&t=syske
        application.setBannerMode(Banner.Mode.OFF);
        application.run(args);
    }
}
```

### 2、创建配置类
配置类也是`spring boot`中特别重要，特别核心的内容，下面是一个简单的配置类演示，主要包括几个常用的配置项，比如页面映射配置、拦截器配置、转换器配置，其中的配置项后面会有详细说明
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
        registry.addConverter(new DateConverter());
    }
}
```

### 3、配置页面与`url`映射

- 主要是针对一些仅需要返回页面的`url`地址，如果需要返回`model`及视图则不适用

```java
 @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        registry.addViewController("/user/login").setViewName("login");
    }
```
- 通过`addViewController`方法添加前端访问的`url`，后面`setViewName`设置的是前面`url`对应的视图名称，如配置的`url`对应的访问地址如下：
```
http://localhost:8080/user/login.html
```
- 方法内可以配置多个视图模型


### 4、配置DateFomatters

自定义的`convertor`，这里其实注册的就是我们本来今天打算要分享的`ConversionService`家族的主角。配置方式很简单，只需要将自定义的转换器添加到`Spring boot`配置中即可：

```java
  @Override
    public void addFormatters(FormatterRegistry registry) {
        //给当前的Spring容器中添加自定义格式转换器.
        registry.addConverter(new DateConverter());
    }
```
转换器具体实现如下：

```java
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

之前在写这块内容的时候，忘记写用法了，今天我在看这块内容的时候都有点懵逼，所以今天补充下。

完成配置类实现和相关配置之后，我们只需要在用到转换器的地方通过`Autowired`引入`ConversionService`，然后就可以直接调用它的`convert`方法进行类型转换，就像下面这样：

```java
    @Autowired
    private ConversionService conversionService;

    @RequestMapping("/converter")
    public Object testConverter() {
        Date date = conversionService.convert("2021-09-16", Date.class);
        System.out.println(date);
        return date;
    }
```
根据官方说法，这种方式是线程安全的，而且很灵活，具体等我们分享完`ConversionService`相关内容，大家就清楚了

最终返回结果如下：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210916221527.png)


### 5、配置拦截器

自定义拦截（`Interceptor`）

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
将自定义的拦截器添加到`Spring boot`配置中

```java
 @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new SessionInterceptor())
                .addPathPatterns("/**")
                .excludePathPatterns("/login","/user/login.html","/bootsrap/**");
    }
```

### 6、拦截器测试

登录拦截测试，以及格式化打印

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

关于`converter`的用法，除了我们前面演示的那种直接用法，在前后端进行参数传递的时候，也可以使用，我想这应该才是它真正的用武之地。比如下面这个测试，我在前端调用`login`接口，传了两个参数——`username`和`logindate`，这里我的`logindate`是`String`，但是到后台直接变成了`Date`，而这一步就是`spring boot`的`ConversionService`帮我们完成的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210916224351.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210916224322.png)

看到这我突然感觉自己捂了，明白为啥默认启动的时候，`spring boot`默认为我们提供了好几种转换器，原来就是为了前后端进行数据转换的，呀，我可真是个小机灵鬼！！！

可以看到，`spring boot`启动的时候，已经为我们提供了`134`中类型转换器了，而且种类特别丰富，忽然直接感觉早上的疑问都解开了，有时候搞清楚一个东西可能就是在这一瞬间：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210916225158.png)

好了，今天的内容就先到这里吧！