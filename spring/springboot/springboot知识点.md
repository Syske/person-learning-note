# springboot知识点

### 1、项目不需要加载数据库时，为避免启动报错，需在启动入口加上如下注解

```java
@SpringBootApplication(exclude={DataSourceAutoConfiguration.class,HibernateJpaAutoConfiguration.class})
```

### 2、集中异常处理

#### 方式一：ExceptionHandle

定义自己的异常类型，根据不同类型做不同处理，比如我定义的MyException：

```java
public class MyException extends RuntimeException {
    public MyException(String msg) {
        super(msg);
    }
}
```

然后通过MyExceptionHandle处理该异常，需要注意的是异常不能在filter中抛出，抛出也没法捕获

```java
@RestControllerAdvice
public class MyExceptionHandle {

    @ExceptionHandler(MyException.class)
    public Result exceptionHandle(MyException e) {
        return Result.getFailed( "system error:MyException" + e.getMessage());
    }
}
```

在controller、service以及拦截器的预处理方法中都可以完美捕获，这里特殊说下拦截器：

```java

public class MyInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        //throw new MyException("拦截器错误：MyInterceptor");
        // 这里的异常会完美捕获，并返回
        return true;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) {
        throw new MyException("拦截器错误：MyInterceptor");
        /** 能捕获异常信息并返回给客户端，但并不会覆盖已经请求成功的返回结果，但会包含在返回结果中，比如我的返回结果：
         {"code":1,"success":true,"msg":"请求成功","result":true}{"code":0,"success":false,"msg":"system error:MyException拦截器错误：MyInterceptor","result":null}
         */
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) {
        throw new MyException("拦截器错误：MyInterceptor");
        // 这里抛出的异常并不能被捕获，会直接在后台抛出，相当于回掉函数，请求结果已经返回
    }
}
```

上面的解释已经够清楚了，就不做过多说明了。刚刚我们说了，上面的这种方式，对于filter是不起作用的，下面我们说的这种方式，主要就是针对filter来说的

#### 方式二：ExceptionFilter

定义一个controller，请求路径可以自己指定，比如`/error/exthrow`:

```java
@Controller
public class ExceptionController {

    @RequestMapping("/error/exthrow")
    public void rethrow(HttpServletRequest request) throws Exception {
        throw ((Exception) request.getAttribute("filter.error"));
    }
}
```

再定义一个异常拦截器，在需要抛出异常的拦截器中直接抛出异常，然后在异常拦截器中try-catch，发生异常时直接转发至前面定义的异常controller，这里需要注意的是，如果你的filter是实现Filter或者继承OncePerRequestFilter，那你不需要任何处理，直接`request.setAttribute("filter.error", e)`就可以了。

由于我把自己的filter交给shiro管理，而且是继承BasicHttpAuthenticationFilter的，不知到什么原因，直接catch到的异常类型是ServletException，为了拿到真正的异常信息，我需要通过getCause()方法获取filter中抛出的异常。因为controller抛出的异常最后还是会交给我们定义的MyExceptionHandle去处理，如果获取到的异常不是我们自定义的异常或者他的子类的话，就会返回500错误（在这个示例前，我以为所有的filter都是这样的，后来实践后发现并不是这样😂）。

```java
@Component
public class ExceptionFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        try {
            chain.doFilter(request, response);
        } catch (Exception e) {            
            request.setAttribute("filter.error", e);
            //将异常分发到/error/exthrow控制器
            request.getRequestDispatcher("/error/exthrow").forward(request, response);
        }
    }

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
    }

    @Override
    public void destroy() {

    }
}
```

我的filter:

实现Filter接口：

```java
public class MyFilter implements Filter {
    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        throw new MyException("MyFilter过滤器抛出异常");
        //filterChain.doFilter(servletRequest, servletResponse);
    }
   
}
```

filter2继承OncePerRequestFilter：

```java
public class MyFilter2 extends OncePerRequestFilter {
    @Override
    protected void doFilterInternal(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, FilterChain filterChain) throws ServletException, IOException {
        throw new MyException("MyFilter2异常");
    }
}
```

filter配置类：

```java
 @Bean
    public FilterRegistrationBean myFilterRegistration() {
        FilterRegistrationBean registration = new FilterRegistrationBean();
        registration.setFilter(new MyFilter());
        registration.setName("myFilter");
        registration.addUrlPatterns("/*");
        //此处尽量小，要比其他Filter靠前
        registration.setOrder(1);
        return registration;
    }

    @Bean
    public FilterRegistrationBean myFilter2Registration() {
        FilterRegistrationBean registration = new FilterRegistrationBean();
        registration.setFilter(new MyFilter2());
        registration.setName("myFilter2");
        registration.addUrlPatterns("/*");
        //此处尽量小，要比其他Filter靠前
        registration.setOrder(2);
        return registration;
    }

    /**
     * 配置拦截器
     * @return
     */
    @Bean
    public FilterRegistrationBean exceptionFilterRegistration() {
        FilterRegistrationBean registration = new FilterRegistrationBean();
        registration.setFilter(new ExceptionFilter());
        registration.setName("exceptionFilter");
        //此处尽量小，要比其他Filter靠前
        registration.setOrder(-1);
        return registration;
    }
```

#### 方式三：BasicErrorController

其实spring boot原生提供了异常集中处理，我们经常会看到：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200408224651.png)

但是这种方式不够友好，而且大部分情况不满足我们的需求，我们可以通过继承这个controller，然后重写error方法或者errorHtml方法，或者两个都重写，区别是errorHtml是处理请求头为`text/html`的请求发生的异常，而error是除了这个之外的其他异常。

下面是我定义的baseController，error部分返回的结果是空，还需要进一步的研究：

```java
@RestController
@RequestMapping(value = "error")
public class MyBaseErrorController extends BasicErrorController {

    public MyBaseErrorController(ErrorAttributes errorAttributes) {
        super(errorAttributes, new ErrorProperties());
    }

    @Override
    @RequestMapping(produces = {MediaType.ALL_VALUE})
    public ResponseEntity<Map<String, Object>> error(HttpServletRequest request) {

        return new ResponseEntity<Map<String, Object>>(Result.failedResultMap(000, "未知错误"), HttpStatus.OK);
    }

    @RequestMapping(
            produces = {"text/html"}
    )
    public ModelAndView errorHtml(HttpServletRequest request, HttpServletResponse response) {
        HttpStatus status = this.getStatus(request);
        response.setStatus(status.value());
        return null;
    }

}
```

最后，对于以上问题我最后的解决方法是继承ErrorController，然后定义errorHtml和error，更重要的是@RequestMapping注解，然后在方法中response写入返回值，这种方式不够优雅🤣：

```java
@RestController
@RequestMapping(value = "error")
public class MyBaseErrorController implements ErrorController {
    private static final String path_default = "/error";

    @Autowired
    private ErrorAttributes errorAttributes;


    @RequestMapping(produces = {MediaType.ALL_VALUE})
    public void error(HttpServletRequest request,  HttpServletResponse response) {
        setJsonError(response);
    }


    @RequestMapping(
            produces = {"text/html"}
    )
    public void errorHtml(HttpServletRequest request, HttpServletResponse response) {
        setJsonError(response);
    }

    @Override
    public String getErrorPath() {
        return path_default;
    }

    private void setJsonError(HttpServletResponse response) {
        PrintWriter writer = null;
        try {
            response.setStatus(200);
            response.setHeader("Content-type", "text/html;charset=UTF-8");
            response.setCharacterEncoding("UTF-8");
            writer = response.getWriter();
            writer.write(JSON.toJSONString(Result.getFailed("未知错误", null)));
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (writer != null) {
                writer.close();
            }
        }
    }

}
```

