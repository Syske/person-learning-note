# Tomcat源码分析 · 叁——init方法补充

tags: [#Tomcat, #源码]

### 前言



### Tomcat

今天我们先来看下`init`中反射调用的`catalina`的`load`和`start`方法的具体实现，先看`load`方法：

![](https://gitee.com/sysker/picBed/raw/master/blog/20210929082442.png)

从这里我们可以看出来，它调用的是`catalina`中有参的`load`方法，参数就是`main`方法的`args`参数。进入`load`方法之后，它先调用了`arguments`方法，并根据这个方法的返回值判断是否需要执行`load`方法（无参）：

![](https://gitee.com/sysker/picBed/raw/master/blog/20210929082747.png)

`arguments`方法会校验`args`中的参数，如果`args`为空，或者非法参数，该方法返回`false`，我们从前天的内容知道，这里的`args`参数第一个值为`start`，所以最终这个方法会返回`true`。另外，这里的`usage`方法是在我们输入非法参数的时候，打印具体的用法，就类似于`shell`中的`usage`提示：

![](https://gitee.com/sysker/picBed/raw/master/blog/20210929083026.png)

下面我们继续看无参的`load`方法，这个方法太长了，这里我们直接分段截图讲解。先看第一部分：

![](https://gitee.com/sysker/picBed/raw/master/blog/20210929084520.png)

首先是初始化文件夹方法`initDirs`，实际上这个方法并没有用，而且根据目前官方的注释，将在`10`版本移除这个方法：

![](https://gitee.com/sysker/picBed/raw/master/blog/20210929084921.png)

然后是`initNaming`方法，这个方法的主要作用是设置系统的配置参数，这些参数最终会被存放在`System`的`props`属性中（这里的`props`是一个`Properties`对象）：

![](https://gitee.com/sysker/picBed/raw/master/blog/20210929085007.png)

再下来就是`createStartDigester`，这个方法的作用是创建并配置`xml`文件消化器，为后续解析`Tomcat`的`xml`配置文件做准备：

![](https://gitee.com/sysker/picBed/raw/master/blog/20210929085832.png)

然后就是`configFile`方法在，这个方法的作用是获取`conf/server.xml`文件：

![](https://gitee.com/sysker/picBed/raw/master/blog/20210929090116.png)

### 总结