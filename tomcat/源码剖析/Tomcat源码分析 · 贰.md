# Tomcat源码分析 · 贰

### 前言

今天我们来继续分析`tomcat`源码，昨天我们已经分析完了它的启动脚本和其中的`init`方法，我们现在知道`init`其实就是进行了`ClassLoader`的初始化操作，其中资源路径来源于`catalina.properties`文件，同时我们还知道最终初始化的`ClassLoader`是`URLClassLoader`。

下面我们来看下`Tomcat`启动过程中的其他操作。

### Tomcat

昨天关于`init`方法还没讲完，所以今天先要继续分析剩余内容。

#### init方法补充

关于`init`方法其实昨天基本上已经分析完了，因为昨天后半段都在分析`initClassLooders`方法，所以今天回过头再来补充下`init`后续的其他方法。

![](https://gitee.com/sysker/picBed/raw/master/images/20210928130435.png)

首先是`setContextClasserLoader`，这里的操作其实就是设置容器的类加载器，而这里的类加载器就是`intiClassLoaders`中生成的创建的类加载器。这个方法方法就是一个简单赋值操作就不展开讲了，需要注意的是这里获取并建议了`java`的安全策略管理器：

![](https://gitee.com/sysker/picBed/raw/master/images/20210928132924.png)

然后是加载类的操作`securityClassLoad`，这里也校验了安全策略管理器，下面截图已经详细展示了每一个操作具体加载的包，然后通过类的加载方法`loadClass`加载对应包下的类：

![](https://gitee.com/sysker/picBed/raw/master/images/20210928132738.png)

再接着，通过`catalinaLoader`类加载器，加载了`org.apache.catalina.startup.Catalina`，并创建它的实例，最后反射调用它的`setParentClassLoader`方法，设置父级类加载器为`java.lang.ClassLoader`，最终将实例化结果赋值给`BootStrap`的`catalinaDaemon`属性，至此`init`方法执行完成。

#### 继续main方法

执行完`bootstrap`的初始化操作之后，会把`bootstrap`赋值给`daemon`，然后紧接着会解析`command`命令，分别执行它的`load`和`start`方法。



这两天看源码一直有个问题，为啥`Tomcat`中有很多变量都用到了`catalina`这个单词，是有什么特殊含义吗？百度之后，发现`catalina`直接翻译过来就是凯特琳娜，所以网上有两种说法，一种说法是开发者老婆的名字叫凯特琳娜，一种说法是美国西海岸有一个叫`catalina`的小岛，开发者比较喜欢那里，所以叫这个名字。我觉得第一种可能性还是蛮高的，毕竟`Tomcat`本身就是作者养的一只猫的名字，所以`catalina`是他老婆的名字也很顺理成章，而且这也算是程序员的浪漫吧！我的变量里面有你的影子……

