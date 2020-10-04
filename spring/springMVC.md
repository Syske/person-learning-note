
### Spring MVC

#### spring MVC请求处理流程

![image](https://note.youdao.com/yws/api/personal/file/0CE5985DC4834AB4B85CA522194928ED?method=download&shareKey=a6b8aa4cc313dc2e8ab1b5298e0326f3)

- 在Spring MVC中，DispatcherServlet就是前端控制器

- DispatcherServlet的任务是将请求发送给Spring MVC控制器（controller），在典型的应用程序中可能会有多个控制器。DispatcherServlet需要知道应该将请求发送给哪个控制器

- DispatcherServlet通过查询一个或多个处理器映射（handler mapping）来确定请求的下一站在哪里，处理器映射会根据请求所携带的URL信息进行决策 

- 选择了合适的控制器，DispatcherServlet会将请求发送给选中的控制器

- 控制器在完成逻辑处理后，通常会产生一些信息，这些信息（model）需要返回给用户并在浏览器上显示(信息需要发送给一个视图（view）,通常是jsp)

- 控制器所要做的最后一件事就是将模型数据打包，并且标识出用于渲染输出的视图名，它接下来会将请求连同模型和视图名发送回DispatcherServlet

- 控制器不会与特定的视图相耦合，传递给DispatcherServlet的视图名并不直接表示某个特定的JSP。实际上，它甚至不能确定就是JSP。相反，它仅仅传递了一个逻辑名称，这个名字将会用来查找产生结果的真正视图。DispatcherServlet将会使用视图解析器（view resolver）来将逻辑视图名匹配为一个特定的视图名称，它可能是也可能不是JSP

- 最后DispatcherServlet将试图实现，在这里它交付模型数据 。视图将使用模型数据渲染输出，这个输出会通过响应对象传递给客户端（不会像听上去那样硬解码）



#### 搭建Spring MVC

#### 配置DispatcherServlet

DispatcherServlet是Spring MVC的核心，在这里请求会第一次接触到框架，它要负责将请求路由到其他的组件中

 
