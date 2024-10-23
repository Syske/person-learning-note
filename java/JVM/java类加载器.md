
### 概念

在`java`中，类的加载都是通过类加载器实现的，类加载器将字节码文件加载到内存中，并最终转换成可以执行的`java`对象
### 分类

#### 引导类加载器（Bootstrap ClassLoader）

- 它用来加载 `Java` 的核心库（如`java.lang.*`、`java.utl.*`等），这些类通常位于`<JAVA_HOME>/lib`目录下的`rt.jar`等文件中
- `Bootstrap`类加载器不是由`java`代码实现的，而是由虚拟机自身实现的，因此它没有对应的`java.lang.ClassLoader`对象

#### 扩展类加载器（Extensions ClassLoader）

- 它用来加载 Java 的扩展库，这些类通常位于`<JAVA_HOME>/lib/ex`目录下或由`java.ext.dirs`系统属性指定的目录中。
- 扩展类加载器是由`sun.misc.Launcher$ExtClassLoader`实现的。

#### 应用程序类加载器（Application class loader）

- 负责加载应用程序的类路径`classpath`中的类，这些类通常位于`-classpath`或者`-cp`参数指定的目录下
- 应用程序类加载器是由`sun.misc.Launcher$ApplicationClassloader`实现，例如`tomcat`为每个`App`创建一个`Loader`，里面保存着此`WebApp`的`ClassLoader`。需要加载`WebApp`下的类时，就取出`ClassLoader`来使用

#### 自定义类加载器

这类类加载器是用户根据自己的需要构建的类加载，需要通过继承`ClassLoader`来实现

### 类的加载过程

#### 委托模型

`java`的类加载器遵循委托模型。当一个类加载器收到加载类的请求时，它首先会将请求委托给父类加载器，只有当父类加载器无法加载该类时，才会尝试自己加载。

#### 默认行为

当运行一个`java`应用程序时，如果没有特别指定类加载器，那么应用程序中的类通常会被应用程序类加载器加载。例如：

```java
public class Main {
	public static void main(String[] args) {
		System.out.println(Main.class.getClassLoader())
	}

}
```

#### 类加载运行时机

##### jvm启动时创建类加载器

- 对于`Bootstrap ClassLoader`、`Extension ClassLoader`、`Application ClassLoader`会在`jvm`启动时被创建，其中应用程序类加载器会是最后一个被创建的类加载器

##### 加载应用程序类

这里主要是针对`classpath`或者`cp`参数指定的库下面的类


###### 按需加载

应用程序类加载器遵循按需加载的原则。这意味着类并不会在应用程序启动时全部加载，而是在需要时才加载。具体来说，类加载的时机包括：
- 首次使用类时：当应用程序第一次引用某个类时，类加载器会加载该类（`import`不会被加载，必须是初始化、使用类的属性或者访问类的`class`，比如代码中用到了`Sample.class`，这种情况下就会触发类的加载）
- 通过反射加载类：使用`Class.forName()`、`Class.getClassLoader().loadClass()`等反射方法加载类
- 初始化类时：当类的静态初始化块或者静态变量需要初始化时，类加载器会加载该类


### 类加载器的使用

#### 创建自定义类加载

这里有两个要点：
1. 需要继承`java.lang.ClassLoader`类
2. 重写`findClass`方法：`findClass`方法是查找并加载类的核心方法。在这个方法中，我们可以定义自己的类加载逻辑，类如从文件系统、网络或者其他任何数据源加载类字节码

```java
public class MyClassLoader extends ClassLoader {  
    @Override  
    public Class<?> findClass(String name) throws ClassNotFoundException {  
        byte[] classData = loadClassData(name);  
        if (classData == null) {  
            throw new ClassNotFoundException();  
        }  
        System.out.println("load class data end");  
        return defineClass(name, classData, 0, classData.length);  
    }  
  
    protected static byte[] loadClassData(String className) {  
        // 绝对路径
        String fileName = "D:/workspace/learning/learning-dome-code/class-loader/target/classes/" + className.replace('.', '/') + ".class";  
        try (InputStream is = Files.newInputStream(Paths.get(fileName));  
             ByteArrayOutputStream bos = new ByteArrayOutputStream()) {  
            int ch;  
            while (-1 != (ch = is.read())) {  
                bos.write(ch);  
            }  
            return bos.toByteArray();  
        } catch (IOException e) {  
            throw new RuntimeException(e);  
        }  
    }  
}
```


#### 自定义类加载器的使用方式


要加载的类：

```java
public class MyClass {  
    private String name = "syske";  
  
    public String getName() {  
        return this.name;  
    }  
}
```
##### 反射

就是通过类加载器的`loadClass`方法拿到类对象，然后通过反射实现类的实例化和方法调用
```java
public class Main {  
    public static void main(String[] args) throws Exception {  
        MyClassLoader myClassLoader = new MyClassLoader();  
		Class<?> aClass = myClassLoader.findClass("io.github.syske.MyClass");  
		System.out.println("classLoader:" + aClass.getClassLoader().getClass());
        Object newInstance = aClass.getDeclaredConstructor().newInstance();  
		System.out.println("obj instance" + newInstance);  
		Method getName = aClass.getMethod("getName");  
		Object invoke = getName.invoke(newInstance);  
		System.out.println("result:" + invoke);
    }  
}
```

运行结果：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/fb0803b7-12a1-4b29-9268-62ae4770ac9e.jpg)

从打印结果我们可以看到，这里的`ClassLoader`已经是我们上面定义的类加载器了
##### 补充说明

- 类加载器的作用域：每个类加载器都有自己的命名空间。当一个类加载器加载了一个类，这个类的信息只会在这个类加载器的作用域内可见。因此，由不同类加载器加载的相同类名的类在`JVM`中是完全不同的类
- 类的唯一性：在`JVM`中，类的唯一性不仅取决于类的全限定名，还取决于加载该类的类加载器。因此，即使是同一个类名，如果由不同的类加载器加载，也会被视为不同的类

基于上述两个原因，每个类加载器加载的类在`jvm`中被视为不同的类，所以无法实现类型强转，代码和报错见下图：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/6bab2d84-da0d-48c3-bb78-16e45dab2c0b.jpg)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/55fd1849-d9ec-4f53-87db-7be4ac7cf1b3.jpg)

原因很简单，就是因为下面`（MyClass）`其实是将我们自定义类加载器加载的类强准为应用程序类加载器的类，自然是无法转换成功的。

但是针对这个问题，除了通过反射完成所有逻辑，还有个比较折中的方案：

###### 通过继承接口实现强转

```java
public interface MyInterface {  
    String getName();  
}


public class MyClass implements MyInterface {  
    private String name = "syske";  
  
    @Override  
    public String getName() {  
        return this.name;  
    }  
}

public static void main(String[] args) throws Exception {  
    MyClassLoader myClassLoader = new MyClassLoader();  
    Class<?> aClass = myClassLoader.findClass("io.github.syske.MyClass");  
    System.out.println("classLoader:" + aClass.getClassLoader().getClass());  
    MyInterface newInstance = (MyInterface)aClass.getDeclaredConstructor().newInstance();  
    System.out.println(newInstance.getName());
    }


```
运行结果

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/d6dc9d9d-630a-4744-84e8-51a3f0fc3038.jpg)