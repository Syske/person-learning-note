# Tomcat源码分析 · 贰

### 前言

今天我们来继续分析`tomcat`源码，昨天我们已经分析完了它的启动脚本和其中的`init`方法，我们现在直到`init`其实就是进行了`ClassLoader`的初始化操作，其中资源路径来源于`catalina.properties`文件，同时我们还知道最终初始化的`ClassLoader`是`URLClassLoader`