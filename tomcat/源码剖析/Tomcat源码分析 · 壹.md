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







我们先来看下`bin`下面的启动脚本，从`startup`脚本中我们可以找到项目启动入口，这里我们以`windows`环境下的`bat`脚本为例：

![](https://gitee.com/sysker/picBed/raw/master/images/20210926131145.png)

![](https://gitee.com/sysker/picBed/raw/master/images/20210926132445.png)

可以看到`startup`脚本调用的是`catalina`脚本，而且传递的参数是`start`：

首先从下面的脚本中我们可以推测出，这里最终应该会通过执行`Bootstrap`的`main`方法来启动`Tomcat`，而且由于`%1`处的参数是`start`，所以最终他会去调用`noJpda`语句块：

![](https://gitee.com/sysker/picBed/raw/master/images/20210926134054.png)

在`noJpda`语句块中，由于我们的参数是`start`，所以他会调用`doStart`语句块：

![](https://gitee.com/sysker/picBed/raw/master/images/20210926132544.png)

在`ddStart`操作中，设置了启动参数，最后调用`execCme`操作：

![](https://gitee.com/sysker/picBed/raw/master/images/20210926132628.png)

在`execCmd`语句块中最终通过`java`命令行的方式，来运行`MAINCLASS`的`main`方法启动`tomcat`:

![](https://gitee.com/sysker/picBed/raw/master/images/20210926134658.png)

下面我们就来简单看下`Bootstrap`的 `main`方法执行过程。



