# Tomcat源码分析 · 叁——init方法补充

tags: [#Tomcat, #源码]

### 前言

昨天剖析了`Tomcat`的`init`方法，整个流程看着虽然不长，但是分析起来确实挺繁琐的，所以今天要继续剖析。

实话实说，我都觉得挺拖沓的，不过暂时也没别的办法，毕竟我也正在找一个比较好的更新状态，因为持续高效输出也是我一直的追求，而且我也希望每天都能输出高价值的内容，所以如果各位老铁有好的想法或者建议，欢迎沟通交流，毕竟在这个成长进步的道路是永远不会休止的。

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

配置文件获取完成后，会根据获取到的配置文件构建`FileInputStream`和`InputSource`。

如果构建失败会再次通过`getConfigFile`获取配置文件，再次构建输入流和输入资源；如果这里还是构建失败，会基于`server-embed.xml`构建输入流和输入资源，如果以上操作之后还是失败，这时候会打印警告信息，然后返回：

```java
try {
    file = configFile();
    inputStream = new FileInputStream(file);
    inputSource = new InputSource(file.toURI().toURL().toString());
} catch (Exception e) {
    if (log.isDebugEnabled()) {
        log.debug(sm.getString("catalina.configFail", file), e);
    }
}
if (inputStream == null) {
    try {
        inputStream = getClass().getClassLoader()
            .getResourceAsStream(getConfigFile());
        inputSource = new InputSource
            (getClass().getClassLoader()
             .getResource(getConfigFile()).toString());
    } catch (Exception e) {
        if (log.isDebugEnabled()) {
            log.debug(sm.getString("catalina.configFail",
                                   getConfigFile()), e);
        }
    }
}

// This should be included in catalina.jar
// Alternative: don't bother with xml, just create it manually.
if (inputStream == null) {
    try {
        inputStream = getClass().getClassLoader()
            .getResourceAsStream("server-embed.xml");
        inputSource = new InputSource
            (getClass().getClassLoader()
             .getResource("server-embed.xml").toString());
    } catch (Exception e) {
        if (log.isDebugEnabled()) {
            log.debug(sm.getString("catalina.configFail",
                                   "server-embed.xml"), e);
        }
    }
}

if (inputStream == null || inputSource == null) {
    if  (file == null) {
        log.warn(sm.getString("catalina.configFail",
                              getConfigFile() + "] or [server-embed.xml]"));
    } else {
        log.warn(sm.getString("catalina.configFail",
                              file.getAbsolutePath()));
        if (file.exists() && !file.canRead()) {
            log.warn("Permissions incorrect, read permission is not allowed on the file.");
        }
    }
    return;
}
```

如果输入流和输入资源都创建`ok`，则会通过前面已经创建好的`digester`实例进行资源解析：

![](https://gitee.com/sysker/picBed/raw/master/images/20210929132439.png)

接着会获取`server`对象并设置它的属性：

![](https://gitee.com/sysker/picBed/raw/master/blog/20210929231008.png)

但是有个问题，在之前的过程中我并没有发现哪里有实例化`Server`，这里直接获取就不怕直接空指针嘛，所以初步推断前面有实例化`Server`的操作，由于目前`Tomcat`项目无法`debug`运行，所以暂时还跟不了代码，这个遗留问题后面再来回过头来看。

### 总结

到目前为止，`Tomcat`的源码还没有让我发现特别有价值的东西，所以分析这些源码其实挺无聊的，因此后面打算调整下节奏，先快速把整体流程过一下，然后找到适合分享的点再拿出来分享吧。

另外今天更新比较晚的原因是，在公司写工具分享内容，一下写了两篇，所以今天回来比较晚，也就更新晚了，不过好消息是，明天我可以把今天分享的工具内容同步分享出来，供各位小伙伴参考。

好了，今天就到这里吧，各位小伙伴晚安吧！