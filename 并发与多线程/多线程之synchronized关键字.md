# 多线程之synchronized关键字

### 前言

原本这些内容前几天就要分享出来的，但是由于工作实在太忙了（在家办公好卷呀😑），也就没有太多时间完善，只能零零散散写一点点，然后拖到了今天，不过总算完成了，后面的话还是要再勤快点了，感觉最近在家办公产出少了好多。好了，就先吐槽这么多吧，下面开始今天的正文：

不知道给位小伙伴对`synchronized`关键字的认知如何，反正从我学习多线程开始，我似乎对`synchronized`的了解一直都很浅，总觉得很朦胧，似懂非懂，以至于前段时间在分享多线程相关内容的时候，还犯了一个特别低级的错误，所以今天我打算抽点时间全面了解下这个关键字。



### synchronized

和其他的线程安全技术一样，`synchronized`关键字的作用也是为了保障数据的原子性、可见性和有序性，只是相比于其他技术，`synchronized`资历更老，历史更久，而且也更基础，基本上我们在学习线程相关内容的时候，就会学习这个关键字。

在用法上，`synchronized`关键字可以修饰变量、方法和代码块，修饰不同的对象最终产生的影响范围也有所不同，下面我们通过一些简单示例，来看下`synchronized`修饰不同的对象所产生的效果：

#### 修饰方法

`synchronized`修饰方法，该方法会被加上一个`ACC_SYNCHRONIZED`同步标识，表明在执行该方法时，必须先拿到该方法的锁，否则相关线程会被阻塞。

其执行流程是：线程进入`synchronized`修饰的方法时会先上锁（假设没有其他线程访问），方法执行完成后会自动解锁，之后下一个线程才能进入这个方法里，不解锁的话，其他线程是无法访问改方法的。

##### 原理

它的原理是在方法的`flags`中增加`ACC_SYNCHRONIZED`标记，有`ACC_SYNCHRONIZED`标记的方法在被调用时，调用指令会先去检查方法的`ACC_SYNCHRONIZED`访问标志是否设置，如果设置了，执行线程先要持有同步锁，然后才能执行方法，否则相关线程会被阻塞。

下面我们通过一段测试代码来看下`ACC_SYNCHRONIZED`标记效果，方法很简单，就是一个`synchronized`修饰的空方法：

```java
synchronized public static void synchronizedTest() {

}
```

然后我们通过`javap`反编译下上面的这段代码，最终反编译结果如下：

```java
// javap -c -v .\target\test-classes\io\github\syske\thread\SynchronizeTest.class
  public static synchronized void synchronizedTest();
    descriptor: ()V
    flags: ACC_PUBLIC, ACC_STATIC, ACC_SYNCHRONIZED
    Code:
      stack=0, locals=0, args_size=0
         0: return
      LineNumberTable:
        line 57: 0
```

这里需要注意的是，方法要是`public`修饰，否则在反编译代码中是看不到的，这块又到了知识盲区了，后面有空了研究下。

从反编译结果中，我们可以看出`ACC_SYNCHRONIZED`标记，表明该方法是`synchronized`的，同时我们还看到了`ACC_PUBLIC`和`ACC_STATIC`，这两个标记应该就分别访问范围和是否是静态方法。



#### 修饰代码块

`synchronized`修饰的代码块叫同步代码块，通常我们需要在`synchronized()`中指明进入同步代码块的`key`，这里的`key`可以是`Object`、`this`或者`class`。

在原理上，`synchronized`修饰代码块是通过` monitorenter`和` monitorexit`指令进行同步处理的，在执行`monitorenter`时必须要拿到`key`对应的锁才能进入，否则会被阻塞。下面我们通过一段简单代码看下` monitorenter`和` monitorexit`指令，这里以修饰`class`为例：

```java
 public static void synchronizedCodeBlock() {
            synchronized (SynchronizeTest.class) {
                int count = 100;
            }
        }
```

上面的这段代码，最终反编译结果如下：

```java
  public static void synchronizedCodeBlock();
    descriptor: ()V
    flags: ACC_PUBLIC, ACC_STATIC
    Code:
      stack=2, locals=3, args_size=0
         0: ldc           #22                 // class io/github/syske/thread/SynchronizeTest
         2: dup
         3: astore_0
         4: monitorenter
         5: bipush        100
         7: istore_1
         8: aload_0
         9: monitorexit
        10: goto          18
        13: astore_2
        14: aload_0
        15: monitorexit
        16: aload_2
        17: athrow
        18: return
      Exception table:
         from    to  target type
             5    10    13   any
            13    16    13   any
      LineNumberTable:
        line 60: 0
        line 61: 5
        line 62: 8
        line 63: 18
      LocalVariableTable:
        Start  Length  Slot  Name   Signature
      StackMapTable: number_of_entries = 2
        frame_type = 255 /* full_frame */
          offset_delta = 13
          locals = [ class java/lang/Object ]
          stack = [ class java/lang/Throwable ]
        frame_type = 250 /* chop */
          offset_delta = 4
```

从反编译结果中，可以看到`code`的`4`行有`monitorenter`指令，在`9`和`15`行有`monitorexit`指令。需要注意的是，在修饰代码块的时候，`synchronize(obj)`中的`obj`除了是`class`外，还可以是`object`或者`this`，当然他们所起的作用也不是不同的：

##### object

```java
private final static Object key = new Object(); 
private void write(int change) throws InterruptedException {
     synchronized (key) {
         Thread.sleep(10L);
         number += change;

     }
 }
```

`synchronized(object)`表示必须拿到`key`对象的锁才能执行`synchronized`代码块，凡是进入该同步代码块中的线程都必须先获得锁；

##### this

```java
private void write(int change) throws InterruptedException {
     synchronized (this) {
         Thread.sleep(10L);
         number += change;

     }
 }
```

`synchronized(this)`表示必须拿到该当前实例的锁才能执行`synchronized`代码块，同一个实例的线程在进入该同步代码块会互斥；

最上面示例代码中的`synchronized(class)`表示必须拿到`class`的锁才能执行`synchronized`代码块，同一个类下所有实例的线程都会受到影响。

下面我们通过一个完整实例来测试下我们上面的结论。



#### 测试

因为这块的代码都比较简单，而且变动部分也不多，所以这里我直接放出完整的代码。

##### this

首先看下`synchronized`修饰`this`的情况：

```java
public class SynchronizedDemo {
    private final static Object key = new Object();
    public static void main(String[] args) {
        ThisTest thisTest = new ThisTest();
        ThisTest thisTest2 = new ThisTest();
        new Thread(thisTest).start();
        new Thread(thisTest2).start();
    }


    static class ThisTest implements Runnable {

        private static int number = 0;
        @Override
        public void run() {
            for (int i = 0; i < 100; i++) {
                System.out.println("thread name:" + Thread.currentThread().getName());
                try {
                    write(1);
                    read();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            System.out.println("增加 100 次已完成");
        }

        private void read() {
            System.out.println("number = " + number);
        }

        private void write(int change) throws InterruptedException {
            synchronized (this) {
                Thread.sleep(10L);
                number += change;

            }
        }
    }
}
```

这里有两个点需要注意：

- 在`main`方法中，我们分别创建了两个`ThisTest`实例（`thisTest`和`thisTest2`），然后分别通过他们启动两个线程；
- `write`方法中我们通过`synchronized`修饰`this`

最终运行结果如下（大致）：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20220118092022.png)

按照我们的预期，`number`最后的值应该是`200`，但是实际为`193`，说明`this`加`synchronized`不能约束不同实例实例之间的资源共享（线程不安全）。

但是如果我们把`main`方法中`new Thread(thisTest2).start()`的`thisTest2`，替换成`thisTest`，然后再运行，这时候就会发现，最终的运行结果始终就是`200`了（线程安全）：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20220118092545.png)

通过这两次测试结果对比，我们可以确定，`synchronized`在修饰`this`的时候，只能确保同一个实例下所有线程之间的同步代码块互斥（线程安全），而不同实例的线程是不受影响的（线程不安全）。



##### class

`synchronized`修饰`class`的代码和`this`没有太多区别，不一样的点是`synchronized`修饰的对象不同：

```java
// 省略其他代码
private void write(int change) throws InterruptedException {
    synchronized (ThisTest.class) {
        Thread.sleep(10L);
        number += change;
    }
}
```

改成`class`之后，再次运行上面的代码，可以发现，这时候不论创建多少个实例，始终是线程安全的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20220119211502.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20220119211557.png)

当然，通过这个实例，也可以进一步证明`synchronized`修饰`class`必须拿到`class`的锁才能执行`synchronized`代码块，同一个类下所有实例的线程都会受到影响。



##### Object

`synchronized`修饰`object`会和前面的两种有所不同，因为变量可以加不同的修饰符。首先我们看`static`修饰的变量：

```java
private static Object key = new Object();
// 省略其他代码
private void write(int change) throws InterruptedException {
    synchronized (key) {
        Thread.sleep(10L);
        number += change;

    }
```

最终运行效果如下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20220119230338.png)

从原理上来讲，`static`修饰的变量属于`class`层面的变量，所以最终形成的互斥效果和`class`类似；

相应地，如果`key`是成员变量（非`static`），那他产生的效果应该和`this`类似，当然，最终的实验结果也证明了这一点（这里我就不再重复演示了）；

第三种情况是，如果`key`是由第三方类提供的话，那从逻辑上讲应该会对所有的调用方产生互斥，这个推论应该是没有问题的，但是我不知道如何验证。

最后一种情况是，如果`key`是局部变量，这种情况也是可以的，但是需要注意的是，局部变量能够产生的效果最多也就和`this`差不多，并不适用与不同实例的场景，同时还需要注意的是，这时`key`不能是包装类，也不能是由`new`生成的对象，具体可以看我们下面的演示效果：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20220119232453.png)

字符串常量是可以的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20220119232602.png)

但是`new`实例的字符串常量是不可以的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20220119232737.png)

这样`new`生成的都是不可以的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20220119232959.png)

但是赋值操作是可以的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20220119233139.png)

好了，关于局部变量的演示就展示这么多，感兴趣的小伙伴可以自己尝试下。

### 总结

从上面这几个实例中，我们可以看出，`synchronized`在修饰不同类型数据的时候，锁的粒度（互斥范围）也是不同的（这里只说最大粒度），简单总结就是：方法 > `object` > `class` > `this`。

`this`只会影响当前实例的线程访问；`class`会影响当前类所有实例的线程访问；而`object`会影响所有访问同步代码的访问；在方法上加`synchronize`关键字影响范围就更大了，会影响所有当前方法的访问，所以，其中最重的就是修饰方法时候，其次是修饰`object`，然后才是`class`和`this`。

当然`object`在一些特殊操作之下，也可以达到和`class`、`this`类似的效果，关于这一点，我们上面也给出了具体示例，在具体使用中，需要各位小伙伴根据自己的实际需求合理选择。

最后需要注意的是，`synchronized`在修饰`object`的时候，必须是不可变的对象（也就是钥匙必须唯一），否则是起不到阻塞（锁）的作用的，关于这一点我曾经就犯过很低级的错误（上面的示例也演示了这一点）：

```java
try {
    Thread.sleep(1000);
    synchronized (count){
        System.out.println(count++);
        if (count == 99) {
            System.out.println("用时:" + (System.currentTimeMillis() - startTime));
        }
    }
} catch (InterruptedException e) {
    e.printStackTrace();
}
```

好了，关于`synchronized`关键字，我们就说这么多，到今天我也算是对`synchronized`有了相对比较全面的认识和了解，当然更重要的是，让我真正从原理上清楚了`synchronized`各种适用场景，也纠正了以前对于`synchronized`的错误认知。好了，今天就先到这里吧，各位小伙伴，晚安哦！

