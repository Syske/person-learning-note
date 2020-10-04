不论你学习多先进的技术，扎实的基本功和良好的编程习惯永远是最基本的，今天给大家推荐阿里巴巴的java开发手册（嵩山版）：

> 链接:https://pan.baidu.com/s/1ZVBMJnavsJX76I3iyq4mMg 提取码:t5wj 复制这段内容后打开百度网盘手机App，操作更方便哦





# 多线程　

刚开始接触java多线程的时候，我觉得，应该像其他章节的内容一样，了解了生命周期、构造方法、方法、属性、使用的条件，就可以结束了，然而随着我的深入学习了解，我发现java的多线程是java的一个特别重要的章节，也是java web部分的一个重要的基础知识。java作为一种面向对象编程语言，自带了并发属性，在多线程这里引发了更深更广的编程应用——并发编程，我觉得自己就是个小白，java领域有太多知识要去学习…… 

### 1、线程的概念：

- 线程——是系统的最小执行单元；

- 进程是由线程组成的。

### 2、线程与线程之间的互动：互斥  同步　　

### 3、Thread的生命周期：

#### （1） **新建（new Thread）**

当创建Thread类的一个实例（对象）时，此线程进入新建状态（未被启动）。
例如：Thread t1=new Thread();

#### （2）就绪（runnable）

线程已经被启动，正在等待被分配给CPU时间片，也就是说此时线程正在就绪队列中排队等候得到CPU资源。例如：**t1.start();**

#### 　（3）运行（running）

线程获得CPU资源正在执行任务（run()方法），此时除非此线程自动放弃CPU资源或者有优先级更高的线程进入，线程将一直运行到结束。

#### （4）堵塞（blocked）

由于某种原因导致正在运行的线程让出CPU并暂停自己的执行，即进入堵塞状态。

　　正在睡眠：用sleep(long t) 方法可使线程进入睡眠方式。一个睡眠着的线程在指定的时间过去可进入就绪状态。

　　正在等待：调用wait()方法。（调用motify()方法回到就绪状态）

　　被另一个线程所阻塞：调用suspend()方法。（调用resume()方法恢复）

#### （5）死亡（dead）

当线程执行完毕或被其它线程杀死，线程就进入死亡状态，这时线程不可能再进入就绪状态等待执行。

自然终止：正常运行run()方法后终止

异常终止：调用**stop()**方法让一个线程终止运行

### 4、线程的创建：（两种方式）

#### （1）通过继承Thread类创建，如下例：

```java
public class ThreatTest extends Thread{
    public void run(){
    System.out.println(getName()+"线程开始运行");
    System.out.println(getName()+"线程结束了");
    }
}
```

#### （2）通过 interfance Runnable接口创建，如下例：

```java
class MissThread implements Runnable{
    public void run(){        
        System.out.println(Thread.currentThread().getName()+"线程开始运行");
        System.out.println(Thread.currentThread().getName()+"线程结束了");    
    }
}
```

其中，run(){}方法为必须的。**接口不可实例化，所以参数必须为实现接口的类或匿名类。**

有关线程更详细的构造方法、方法请查阅Java jdk API，本文会在后续进一步的扩充和归纳！

　　

### 5.常用方法

```java
void run()  // 创建该类的子类时必须实现的方法

void start() // 开启线程的方法

static void sleep(long t) // 释放CPU的执行权，不释放锁

static void sleep(long millis,int nanos) // 使线程挂起一段时间

final void wait() // 释放CPU的执行权，释放锁

final void notify() // 唤醒一个等待（对象的）线程并使该线程开始执行

static void yied() //可以对当前线程进行临时暂停（让线程将资源释放出来）
```

**注意：**

（1）结束线程原理：就是让run方法结束。而run方法中通常会定义循环结构，所以只要控制住循环即可

（2）方法----可以boolean标记的形式完成，只要在某一情况下将标记改变，让循环停止即可让线程结束

（3）public final void join()//让线程加入执行，执行某一线程join方法的线程会被冻结，等待某一线程执行结束，该线程才会恢复到可运行状态

### 6、主线程与子线程之间的关系：参考别人的一篇博客[^1]

Java编写的程序都运行在Java虚拟机（JVM）中，在JVM的内部，程序的多任务是通过线程来实现的。

每用java命令启动一个java应用程序，就会启动一个JVM进程。在同一个JVM进程中，有且只有一个进程，就是它自己。在这个JVM环境中，所有程序代码的运行都是以线程来运行的。JVM找到程序的入口点main（），然后运行main（）方法，这样就产生了一个线程，这个线程称之为主线程。当main方法结束后（没有其他线程时），主线程运行完成。JVM进程也随即退出。

操作系统将进程线程进行管理，轮流（没有固定的顺序）分配每个进程很短的一段时间（不一定是均分），然后在每个进程内部，程序代码自己处理该进程内部线程的时间分配，多个线程之间相互的切换去执行，这个切换时间也是非常短的。

对于程序来说，如果主进程在子进程还未结束时就已经退出，那么Linux内核会将子进程的父进程ID改为1（也就是init进程），当子进程结束后会由init进程来回收该子进程。

　　那如果是把进程换成线程的话，会怎么样呢？假设主线程在子线程结束前就已经退出，子线程会发生什么？

　　首先我们来看一个网上很多人的例子：

```java
package test;

public class Test1 extends Thread
{
    @Override
    public void run()
    {
        while (true)
        {
            try
            {
                Thread.sleep(2000);
            }
            catch (InterruptedException e)
            {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
            System.out.println("我还活着");
        }
    }

    public static void main(String[] args) throws InterruptedException
    {
        Thread t = new Test1();
        t.start();
        Thread.sleep(5000);
        System.out.println("Main End");
    }
}
```

输出： 

```
我还活着
我还活着
Main End
我还活着
我还活着
```

 上文说了 JVM找到程序的入口点main（），然后运行main（）方法，这样就产生了一个线程，这个线程称之为主线程。当main方法结束后（没有其他线程时），主线程运行完成。JVM进程也随即退出。然而上述输出表明当main()运行到最后后，子线程依然在输出。所以大家就得出了结论，父线程要等待子线程完成后才会退出。然而我们再看个例子： 

```java
package test;

public class Test extends Thread
{
    @Override
    public void run()
    {
        Thread sonthread = new a();
        sonthread.start();
    }

    public static void main(String[] args) throws InterruptedException
    {
        Thread fatherThread = new Test();
        fatherThread.start();
        Thread.sleep(5000);
        fatherThread.interrupt();
        Thread.sleep(2000);
        System.out.println("fatherThread.isAlive()?  "+fatherThread.isAlive());
    }
}

class a extends Thread
{
    @Override
    public void run()
    {
        while (true)
        {
            try
            {
                Thread.sleep(1000);
            }
            catch (InterruptedException e)
            {
                e.printStackTrace();
            }
            System.out.println("我还活着");
        }
    }
}
```

输出： 

```
我还活着
我还活着
我还活着
我还活着
我还活着
我还活着
fatherThread.isAlive()? false
我还活着
我还活着
我还活着
```

 很明显，父线程死后子线程还在输出。两个例子到底哪个是正确的呢？

查了很多资料得到了解答。

如果main方法中没有创建其他线程，那么当main方法返回时JVM就会结束Java应用程序。但如果main方法中创建了其他线程，那么JVM就要在主线程和其他线程之间轮流切换，保证每个线程都有机会使用CPU资源，main方法返回(主线程结束)JVM也不会结束，要一直等到该程序所有线程全部结束才结束Java程序(另外一种情况是：程序中调用了Runtime类的exit方法，并且安全管理器允许退出操作发生。这时JVM也会结束该程序)。

那么又有个思考，JVM是怎么知道线程都结束的呢？

JVM中有一个线程DestroyJavaVM，执行main()的线程在main执行完后调用JNI中的jni_DestroyJavaVM()方法唤起DestroyJavaVM线程。JVM在Jboss服务器启动之后，就会唤起DestroyJavaVM线程，处于等待状态，等待其它线程（java线程和native线程）退出时通知它卸载JVM。线程退出时，都会判断自己当前是否是整个JVM中最后一个非deamon线程，如果是，则通知DestroyJavaVM线程卸载JVM。

ps：扩展一下：

1.如果线程退出时判断自己不为最后一个非deamon线程，那么调用thread->exit(false)，并在其中抛出thread_end事件，jvm不退出。

2.如果线程退出时判断自己为最后一个非deamon线程，那么调用before_exit()方法，抛出两个事件： 

事件1：thread_end线程结束事件、事件2：VM的death事件。

然后调用thread->exit(true)方法，接下来把线程从active list卸下，删除线程等等一系列工作执行完成后，则通知正在等待的DestroyJavaVM线程执行卸载JVM操作。

所以第一个例子时，主线程运行完，但是它不是最后一个非守护线程，所以JVM并没有退出，所以子线程还会继续运行。

第二个例子。主线程一直在，所以JVM不会退出。当父线程死去后，子线程还在运行。说明父线程的生命周期与子线程没有关系。

 

### 7、通过查阅资料，我发现，创建线程（Thread）还有另外一种方法，现在补充在后面：　　

#### 通过Callable和FutureTask创建线程 

①创建Callable接口的实现类，并实现call()方法，该call()方法将作为线程执行体，并且有返回值。

②创建Callable实现类的实例，使用FutureTask类来包装Callable对象，该FutureTask对象封装了该Callable对象的call()方法的返回值。

③使用FutureTask对象作为Thread对象的target创建并启动新线程。

④调用FutureTask对象的get()方法来获得子线程执行结束后的返回值

例：

```java
package thread;  
   
import java.util.concurrent.Callable;  
   
public class MyCallable implements Callable{  
   
    @Override 
    public Integer call() throws Exception {  
        // TODO Auto-generated method stub  
        return 1111;  
    }  
   
}
```

```java
package thread;  
   
import java.util.concurrent.ExecutionException;  
import java.util.concurrent.FutureTask;  
   
public class Main{  
    public static void main(String[] args) {  
        FutureTask ft = new FutureTask<>(new MyCallable());  
        new Thread(ft).start();  
        try {  
            System.out.println(ft.get());  
        } catch (InterruptedException e) {  
            // TODO Auto-generated catch block  
            e.printStackTrace();  
        } catch (ExecutionException e) {  
            // TODO Auto-generated catch block  
            e.printStackTrace();  
        }  
    }  
}
```

　　

**创建线程的三种方式的对比**

1. 采用实现 Runnable、Callable 接口的方式创见多线程时，线程类只是实现了 Runnable 接口或 Callable 接口，还可以继承其他类。

2. 使用继承 Thread 类的方式创建多线程时，编写简单，如果需要访问当前线程，则无需使用 Thread.currentThread() 方法，直接使用 this 即可获得当前线程。

 

[^1]: 博客地址：https://my.oschina.net/hosee/blog/509557

