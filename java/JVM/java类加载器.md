- 1、引导类加载器（bootstrap class loader）：它用来加载 Java 的核心库，是用原生代码来实现的

- 2、扩展类加载器（extensions class loader）：它用来加载 Java 的扩展库。

- 3、系统类加载器（system class loader）：它根据 Java 应用的类路径（CLASSPATH）来加载 Java 类
- 4、tomcat为每个App创建一个Loader，里面保存着此WebApp的ClassLoader。需要加载WebApp下的类时，就取出ClassLoader来使用