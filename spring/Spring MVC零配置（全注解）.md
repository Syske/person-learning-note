```
// 核心配置类
package spittr.config;

import org.springframework.web.servlet.support.AbstractAnnotationConfigDispatcherServletInitializer;

public class SpittrWebAppInitializer extends AbstractAnnotationConfigDispatcherServletInitializer{

    @Override
    protected Class<?>[] getRootConfigClasses() {
        // TODO Auto-generated method stub
        return new Class<?>[] {RootConfig.class};
    }

    @Override
    protected Class<?>[] getServletConfigClasses() {
        // 指定配置类
        return new Class<?>[] {WebConfig.class};
    }
    /**
     * 将一个或多个路径映射到DispatcherServlet上
     */
    @Override
    protected String[] getServletMappings() {
        // 将DispatcherServlet映射到“/”
        return new String[] {"/"};
    }

}

```

```
package spittr.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.ViewResolver;
import org.springframework.web.servlet.config.annotation.DefaultServletHandlerConfigurer;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import org.springframework.web.servlet.view.InternalResourceViewResolver;

@Configuration
@EnableWebMvc // 启用Spring MVC
@ComponentScan("spittr.web") // 启用组件扫描
public class WebConfig implements WebMvcConfigurer {
    /**
     * 配置JSP视图解析器
     * 
     * @return
     */
    @Bean
    public ViewResolver viewResolver() {
        InternalResourceViewResolver resolver = new InternalResourceViewResolver();
        resolver.setPrefix("/WEB-INF/views/");
        resolver.setSuffix(".jsp");
        resolver.setExposeContextBeansAsAttributes(true);
        return resolver;
    }

    @Override
    public void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer) {
        configurer.enable();
    }

}

```

```
package spittr.config;

import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.ComponentScan.Filter;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.FilterType;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;

@Configuration
@ComponentScan(basePackages= {"spitter"},
        excludeFilters= {
                @Filter(type=FilterType.ANNOTATION, value=EnableWebMvc.class)
                })
public class RootConfig {

}


```

```
package spittr.web; 

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
public class HomeController {
    static {
        System.out.println("=============HomeController============");
    }
    @RequestMapping("/home")
    public String home() {
        System.out.println("hellow");
        return "home";
    }
}

```