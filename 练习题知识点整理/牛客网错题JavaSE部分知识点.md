### 牛客网错题知识点整理

tags: #错题 #知识点

- #### 1、java中对于文本文件和二进制文件，都可以当做二进制文件进行操作；

---

- #### 2、Flie类是对文件整体或者文件属性操作的类，例如创建文件、删除文件、查看文件是否存在等功能，不能操作文件内容；

---

- #### 3、文件内容是通过IO流操作的；

---

- #### 4、当输入过程中以外到达文件或流的末尾时，抛出EOFException异常，正常情况下读取文件到末尾时，返回一个特殊值表示文件读取完成，例如read()返回-1表示文件读取完成；

---


- #### 5、一个以”.java”为后缀的源文件只能有一个与文件名相同的类，可以包含其他类

---

- #### 6、JDK提供的用于并发编程的同步器：Semaphore、CyclicBarrier、CountDownLatch 

---

- #### 7、基本类型初始化：整型默认为int，如果需要long，须加l或L。小数默认double，d或D可省略，但如果需要float，须加f或F，例如float = 0.1f；

---

- #### 8、Java程序经编译后会产生byte code；

---

- #### 9、计算余弦值使用Math类的cos()方法：

- - toRadians()是将角度转换为弧度；

- - toDegrees()是将弧度转换为角度；

---


- #### 10、管道（Pipe）知识点:

- - 进程对管道进行读操作和写操作都可能被阻塞;

- - 一个管道可以有多个进程对其读；也可以有多个进程写，只不过不能同时写;

- - 匿名管道只能单向；命名管道可以双向；

- - 管道是内存中的,所以管道的容量受内存大小影响；

---

- #### 11、线程安全的map在JDK 1.5及其更高版本环境的实现方式：

```java
Map map = new ConcurrentHashMap();
Map map = Collections.synchronizedMap(new HashMap());
```

---


- #### 12、内部类（也叫成员内部类）可以有4种访问权限。

- - private

- - protected

- - public

- - 默认的访问权限

---

- #### 13 、在调用getName()方法时getName()返回的是：包名+类名；getSimpleName()返回的是类名；

---

- #### 14、java 的字符类型采用的是 Unicode 编码方案，每个 Unicode 码占用**16**个比特位。

---

- #### 15、java中Object的方法：

- > equals(Object obj);

- > getClass();

- > hashCode();

- > notify();

- > toString();

- > wait();

- > wait(long timeout);

- > wait(long timeout,int nanos);

---
- #### 16、Integer

- > intValue()是把Integer对象类型变成int的基础数据类型； 
- > parseInt()是把String 变成int的基础数据类型； 
- > Valueof()是把String 转化成Integer对象类型；（现在JDK版本支持自动装箱拆箱了。）

---

- #### 17、JAVA的初始化顺序：

```
graph LR
A[父类的静态成员初始化] --> B[父类的静态代码块] 
B --> C[子类的静态成员初始化]
C --> D[子类的静态代码块]
D --> E[父类的代码块]

```

```
graph LR

E[父类的代码块]
E --> F[父类的构造方法]
F --> G[子类的代码块]
G --> H[子类的构造方法]
```

- - 注意：

 > 1.静态成员和静态代码块只有在类加载的时候执行一次，再次创建实例时，不再执行，因为只在方法区存在一份，属于一整个类。

> 2.上述的是通用的加载顺序，如果没有则省略。 


- #### 18、constructor在一个对象被new 时执行，方法可以和class同名，但必须有返回值；

- #### 19、有一个源代码，只包含import java.util.* ;能访问java/util目录下的所有类，不能访问java/util子目录下的所有类

- #### 20、Java关键字

abstract | assert | boolean | break | byte
    ---  |   ---  |    ---  |   --- |---
    case |  catch |   char  |  class|const
continue | default|     do  | double|else
enum     | extends|final    |finally|float
for      |goto    | if      |implements|import
instanceof|int    |interface|long   |native
new      | package|private  |protected|public
return   | strictfp|short   |static   | super
switch   |synchronized |this | throw |throws
transient |try  | void | volatile| while

