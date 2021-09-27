# Tomcat源码分析 · 壹

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

![](https://gitee.com/sysker/picBed/raw/master/blog/20210926085107.png)

这个结构和我们平时下载到的发布版本基本上一致。这里源码剖析和版本无关，但是如果线上环境使用的话，建议使用最新版，因为`9.0.31`以下的版本存在漏洞，关于漏洞加固可以看下我之前分享的内容：





下面我们看下`Bootstrap`的`main`方法执行过程：

![](https://gitee.com/sysker/picBed/raw/master/blog/20210927082820.png)

首先，它以单例模式创建了`Bootstrap`实例，并执行它的初始化操作，最后讲创建的对象赋值给`daemon`对象，如果发生异常会调用`handleThrowable`方法进行异常处理。这里创建方式是单例模式，首先`daemon`是一个静态私有变量，同时它被`volatile`关键字修饰，确保它在修改后对所有线程可见，为了进一步保证线程安全，这里还引入了`daemonLock`变量，并加了`synchronized`锁，下面是这两对象的定义及修饰：

![](https://gitee.com/sysker/picBed/raw/master/blog/20210927083045.png)

在`main`方法的下半部分中，它需要执行`daemon`的`load`方法和`start`方法来启动容器，这里发生异常，同样会调用`handleThrowable`方法来处理异常。另外从这几行代码中，我们可以看出来，`command`其实只支持通过`args`参数传入的，需要注意的是，`command`必须是`args`的最后一个参数：

![](https://gitee.com/sysker/picBed/raw/master/blog/20210927084215.png)

下面我们就来逐一看下与 `Bootstrap`相关的几个方法。

#### init

首先是`init`方法，这个方法主要有两部分操作，一部分就是关于类加载器的操作，一部分就是关于`Catalina`的操作。

![](https://gitee.com/sysker/picBed/raw/master/blog/20210927085524.png)

