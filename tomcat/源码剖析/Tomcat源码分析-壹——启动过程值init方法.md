# Tomcat源码分析 · 壹

tags: [#tomcat, #源码]

### 前言

从今天开始，我们开始分析`tomcat`的源码，至于原因嘛，第一`Tomcat`是非常优秀的`web`服务器，它占据着全球一半以上的市场份额，就连`spring boot`这样的顶级框架都在用`tomcat`做底层实现，这足以说明其流行程度。当然，其流行的另一个重要原因是，它是开源的，它是`apache`基金会下的一个顶级项目，相比做`java`开发的小伙伴应该没人不知道`tomcat`吧。

基于以上原因，我们今天来看下`Tomcat`的源码实现。

昨天在某乎上看到一个大佬分享了`Tomcat`的源码视频，大佬说关于源码的学习应该从以下几点入手：

- 组件及功能
- 设计模式
- 线程安全
- 对比联想

所以本次源码分析我们就从以上几点开始入手。我昨天说要加强设计模式就是从这里看来的，毕竟看清楚了设计模式，源码分析起来就没那么难了。

### Tomcat

首先，我们看`Tomcat`源码的结构：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210926085107.png)

这个结构和我们平时下载到的发布版本基本上一致。这里源码剖析和版本无关，但是如果线上环境使用的话，建议使用最新版，因为`9.0.31`以下的版本存在漏洞，关于漏洞加固可以看下我之前分享的内容：





我们先来看下`bin`下面的启动脚本，从`startup`脚本中我们可以找到项目启动入口，这里我们以`windows`环境下的`bat`脚本为例：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210926131145.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210926132445.png)

可以看到`startup`脚本调用的是`catalina`脚本，而且传递的参数是`start`：

首先从下面的脚本中我们可以推测出，这里最终应该会通过执行`Bootstrap`的`main`方法来启动`Tomcat`，而且由于`%1`处的参数是`start`，所以最终他会去调用`noJpda`语句块：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210926134054.png)

在`noJpda`语句块中，由于我们的参数是`start`，所以他会调用`doStart`语句块：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210926132544.png)

在`ddStart`操作中，设置了启动参数，最后调用`execCme`操作：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210926132628.png)

在`execCmd`语句块中最终通过`java`命令行的方式，来运行`MAINCLASS`的`main`方法启动`tomcat`:

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210926134658.png)

下面我们就来简单看下`Bootstrap`的 `main`方法执行过程:：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210927082820.png)

首先，它以单例模式创建了`Bootstrap`实例，并执行它的初始化操作，最后讲创建的对象赋值给`daemon`对象，如果发生异常会调用`handleThrowable`方法进行异常处理。这里创建方式是单例模式，首先`daemon`是一个静态私有变量，同时它被`volatile`关键字修饰，确保它在修改后对所有线程可见，为了进一步保证线程安全，这里还引入了`daemonLock`变量，并加了`synchronized`锁，下面是这两对象的定义及修饰：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210927083045.png)

在`main`方法的下半部分中，它需要执行`daemon`的`load`方法和`start`方法来启动容器，这里发生异常，同样会调用`handleThrowable`方法来处理异常。另外从这几行代码中，我们可以看出来，`command`其实只支持通过`args`参数传入的，需要注意的是，`command`必须是`args`的最后一个参数：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210927084215.png)

下面我们就来逐一看下与 `Bootstrap`相关的几个方法。

#### init

首先是`init`方法，这个方法主要有两部分操作，一部分就是关于类加载器的操作，一部分就是关于`Catalina`的操作。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210927085524.png)

在`initClassLoaders`方法中，主要是创建了三个类加载器：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210927131123.png)

这里的`common`、`server`和`shared`分别表示不同的配置名，在`creaeteClassLoader`方法中会根据该名称从`catalina.properties`文件中获取对应的配置

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210927132336.png)

在获取配置资源的时候，会从三个地方获取`catalina.properties`文件，分别是系统的根目录、`conf`目录、和`/org/apache/catalina/startup/`包下面，但只会解析其中一个，会按照我们这里说的顺序解析，如果中间任意一个文件不为空，则后面的文件就不会被解析到：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210927133320.png)

在`config`目录下的`catalina.properties`文件中，只有`common.loader`是有值的，其他两个都是空的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210927133529.png)

可以看到`common.loader`共配置了四个路径，分别包括两个目录及其下的`jar`文件。

首先会在`replace`方法中替换其中`${catalina.base}`这样配置，然后在`getPaths`方法中最终匹配·其中配置的内容。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210927134254.png)

这里的`gatPaths`方法就是为了解析出配置文件中的路径，然后返回：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210927134332.png)

最后，调用`ClassLoaderFactory`的`creaeteClassLoader`方法创建了一个`URLClassLoader`的实例，入参就是出`jar`文件之外的路径：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210927220214.png)

好了，由于时间的关系，我们今天就只说`init`方法中的一部分，剩下的内容明天继续，另外今天打算搞下`tomcat`的环境，让`tomcat`能在`idea`环境下`debug`。

### 总结

从目前情况来看，`tomcat`的源码和`spring boot`比起来，还是比较简单的，当然这也不排除正是经历了`spring boot`源码的磨砺，才让我们现在看`tomcat`的源码如此地轻松。

另外有个好消息说下，由于最近一直忘记提交内容，所以今天我专门搞了一个定时任务提交内容，这样以后每天六点定时任务会自动帮我提交内容，我再也不用担心写好的内容忘记提交了，`so easy`！

好了，各位小伙伴晚安吧，我要继续搞环境了！

