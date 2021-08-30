# 从代码层面看spring boot启动过程

### 前言

我们都知道`spring boot`项目是通过`main方法来启动运行的`，但是`main`方法执行之后，`spring boot`都替我们完成了哪些操作，最终让我们的服务成功启动呢？今天我们就来从源码层面探讨下这个问问题。

### spring boot启动过程

在开始之前，我们先看这样一段代码：

```java
@SpringBootApplication
public class DailyNoteApplication {

    public static void main(String[] args) {
        SpringApplication.run(DailyNoteApplication.class, args);
    }

}
```

上面的这段代码就是我们最常见的`spring boot`启动的`main`方法，今天我们就从这个`main`方法开始，进入`spring boot`的世界。

#### springApplication

首先，在`main`方法内部执行了`SpringApplication.run(DailyNoteApplication.class, args)`，这个方法有两个入参，一个是项目主类（当前类）的`class`，另一个就是`main`方法的`args`。

这里先说下这个`args`参数，我们都知道`spring boot`是支持以命令行的方式注入配置信息的，它的实现就是依赖于这个`args`参数的。如果你将`args`删掉，项目也是可以正常启动的，只是你再也没办法通过命令行的方式注入配置了。关于这一块，我们之前在通过`k8s`启动`spring boot`项目的时候踩过坑，发现注入的参数不起作用，最后发现就是少了`args`。

##### run方法

在`run`方法内部，首先实例化了一个`springApplication`对象，然后又调用了另一个`run`方法：

![](https://gitee.com/sysker/picBed/raw/master/images/20210830084931.png)

###### springApplication实例化

我们先看`springApplication`的实例化过程：

![](https://gitee.com/sysker/picBed/raw/master/images/20210830085231.png)

前两个`this`都是简单的赋值，这里暂时先不过多研究，第三个`this`这里的`WebApplicationType.deduceFromClasspath()`是判断我们的服务器类别，在`spring boot`中，有两种服务器一种就是传统的`sevlet`，也就是基于`tomcat`（其中一种）这种，另一种就是`reactive`，也就是我们前面分享的`webflux`这种流式服务器。

紧接着是初始化`ApplicationContextInitializer`和`ApplicationListener`，这里主要是获取他们的`spring`工程实例，方便后续创建他们的实例，为了保证主流程的连贯性，我们暂时不看其方法内部实现。

最后一个赋值操作是找出包含`main`方法的类的`className`。

###### run方法开始执行

下面我们看下`springApplication`实例的 `run`方法内部执行过程：

- 创建了一个`StopWatch`对象，并调用它的`start`方法

  ```java
  StopWatch stopWatch = new StopWatch();
  stopWatch.start();
  ```

  

- 设置`java`的`java.awt.headless`值，如果已经设置过就取系统设置的值，如果没有设置，则设置为`true`。这个是设置`java`的无头模式，启用之后，可以用计算能力来处理可视化操作（类似于用算力代替显卡渲染能力）

  ```java
  configureHeadlessProperty();
  ```

  

- 获取`spring boot`运行监听器

  ```java
  SpringApplicationRunListeners listeners = getRunListeners(args);
  ```

  

- 解析控制台参数（`args`），获取应用参数

  ```java
  ApplicationArguments applicationArguments = new DefaultApplicationArguments(args);
  ```

- 配置需要忽略的`bean`信息，从源码中我们可以看出了，如果我们没有设置`spring.beaninfo.ignore`，`spring boot`会给他默认`true`：

  ```java
  configureIgnoreBeanInfo(environment);
  //方法内部实现
  private void configureIgnoreBeanInfo(ConfigurableEnvironment environment) {
  		if (System.getProperty(CachedIntrospectionResults.IGNORE_BEANINFO_PROPERTY_NAME) == null) {
  			Boolean ignore = environment.getProperty("spring.beaninfo.ignore", Boolean.class, Boolean.TRUE);
  			System.setProperty(CachedIntrospectionResults.IGNORE_BEANINFO_PROPERTY_NAME, ignore.toString());
  		}
  	}
  ```

- 打印`banner`信息，这个`banner`就是`spring boot`启动的时候打印的哪个`logo`，那个是支持自定义的

  ```java
  Banner printedBanner = printBanner(environment);
  ```

- 创建`spring boot`容器，这里创建的时候会根据我们应用的不同，选择不同的容器

  ```java
  context = createApplicationContext();
  ```

  ![](https://gitee.com/sysker/picBed/raw/master/images/20210830193403.png)

- 创建`spring`工厂实例

  ```java
  exceptionReporters = getSpringFactoriesInstances(SpringBootExceptionReporter.class,
  					new Class[] { ConfigurableApplicationContext.class }, context);
  ```

  

![](https://gitee.com/sysker/picBed/raw/master/images/20210830131800.png)



### 总结