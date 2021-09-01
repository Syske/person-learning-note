# 从代码层面看spring boot启动过程

### 前言

我们都知道`spring boot`项目是通过`main方法来启动运行的`，但是`main`方法执行之后，`spring boot`都替我们完成了哪些操作，最终让我们的服务成功启动呢？今天我们就来从源码层面探讨下这个问题。

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
  listeners.starting();
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

- 准备容器，这一步会进行初始化操作，把环境设置、系统参数、`banner`注入到容器中，并把容器绑定到监听器上

  ```java
  prepareContext(context, environment, listeners, applicationArguments, printedBanner);
  ```

- 刷新容器，这里其实进行了两步操作，一个是给我们的`spring boot`绑定`SpringContextShutdownHook`钩子函数，有了这个函数，我们就可以优雅地关闭`spring boot`了；另一个是刷新`beanFactory`，默认情况下`spring boot`为我们创建的是`GenericApplicationContext`容器，初始化完后，所有的对象都被初始化在它的`beanFactory`，为了确保其他组件也能拿到`beanFactory`中的内容，`refreshContext`方法内还进行了同步操作（直接`copy`给他们）：

```java
refreshContext(context);
```

从源码中可以很明显看出这一点：

![](https://gitee.com/sysker/picBed/raw/master/20210830212720.png)



- 刷新完成后会执行`afterRefresh`方法，但是这个方法默认情况下是空的

  ```java
  afterRefresh(context, applicationArguments);
  ```

  ![](https://gitee.com/sysker/picBed/raw/master/20210830212928.png)

- 停止秒表。这个秒表的作用应该就是计时

  ```java
  stopWatch.stop();
  ```

- 调用监听器`started`方法，这方法修改了容器的状态。和前面`starting`方法不同的是，这个方法必须在`beanfactory`刷新后执行：

  ```
  listeners.started(context);
  ```

  ![](https://gitee.com/sysker/picBed/raw/master/20210830213921.png)

- 运行容器中的`runner`，这里的`runner`主要有两类，一类是继承`ApplicationRunner`的，一类是继承`CommandLineRunner`。我猜测这个应该是为了方便我们实现更复杂的需求实现的，目前还没用到过，后面可以找时间研究下

  ```
  callRunners(context, applicationArguments);
  ```

  ![](https://gitee.com/sysker/picBed/raw/master/20210830214854.png)

- 最后一步还是监听器的操作。这个方法最后将容器的状态改为`ACCEPTING_TRAFFIC`，表示可以接受请求

  ```
  listeners.running(context);
  ```

  到这里，`spring boot`就启动成功了。下面是整个`run`方法的源码，虽然不长，但是我感觉读起来还是有点吃力，想想自己模仿`spring boot`写的`demo`，真的是小巫见大巫。

![](https://gitee.com/sysker/picBed/raw/master/images/20210830131800.png)

### 总结

`spring boot`启动过程虽然看起来简单，用起来简单，但是当我一行一行看源码的时候，我觉得不简单，就好比老远看一棵大树，不就是一个直立的杆嘛，但是当你抵近看的时候，你会发现树干有树杈，树杈又有小树杈，总之看起来盘根错节的，总是感觉看不到树真实的样子。不过，随着后面我们不断地将`spring boot`的树叶、小树杈一一拿掉的时候，我相信我们会越来越清楚地看到`spring boot`这棵大树真实的样子。

今天的内容，其实如果有一张时序图，看起来就比较友好了，但是由于时间的关系，今天来不及做了，我们明天争取把时序图搞出来。

另外，后面我还会把今天一笔带过的方法尽可能详细地研究然后讲解的，我的目标就是由大到小（从树干到树杈，最后到树叶）地剖析`spring boot`的源码，最后把`spring boot`的核心技术梳理清楚。好了，今天就先到这里吧！