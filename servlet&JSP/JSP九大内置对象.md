### 1、九大内置对象

##### application

- - javax.servlet.ServletContext的实例，该实例代表JSP所属的WEB应用本身，可用于JSP页面，或者在Servlet之间交换信息；


##### config

- javax.servlet.ServletConfig的实例，该实例代表该JSP的配置信息


##### exception

- java.lang.Throwable的实例，该实例代表其他页面中的异常和错误。只有当页面时错误处理页面，即编译指令page的isErrorPage属性为true时，该对象才可以使用

##### out
- javax.servlet.jsp.jspWriter的实例，该实例代表Jsp页面的输出流，用于输出内容，杏花村呢个HTML页面

##### page
- 代表该页面本身，通常没有太大用处，也就是Servlet中的this。

##### pagecontext
- javax.servlet.jsp.PageContext的实例，该对象代表该JSP页面上下文，使用该对象可以访问页面中的共享数据

##### request
- javax.servlet.http.HttpServletRequest的实例，该对象封装了一次请求，客户端的请求参数都被封装在该对象里。这是一个常用的对象，获取客户端请求参数必须使用该对象

##### response
- javax.servlet.http.HttpServletResponse的实例，代表服务器对客户端的响应。通常很少使用该对象直接响应，而是使用out对象，除非需要生成非字符响应，常用于重定向

##### session
- javax.servlet.http.HttpSession的实例对象，该对象代表一次会话。当客户端浏览器与站点建立连接时，会话开始；当客户端关闭浏览器时，会话结束



### 2、Application对象

 ####  作用：
  - 在整个web应用的多个JSP、Servlet之间共享数据
```  
application.setAttribute(object, object);
```
  
- 访问Web应用的配置参数
```
application.getInitParameter("parameterName");
```
- - 这些配置参数必须在web.xml文件中使用context-param元素配置<context-param.../>元素配置一个参数，该元素下有如下两个元素：
- - - param-name：配置web参数名
- - - param-value:配置web参数值

### 3、config对象

- config对象代表当前JSP配置信息，但JSP页面通常无需配置，因此也就不存在配置信息，所以JSP页面也就不存在配置信息，所以页面很少用该对象。但在Servlet中则用处相对较大，因为servlet需要在web.xml文件中进行配置，可以指定配置参数。 