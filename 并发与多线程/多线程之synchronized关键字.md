# 多线程之synchronized关键字

不知道给位小伙伴对`synchronized`关键字的认知如何，反正从我学习多线程开始，我似乎对`synchronized`的了解一直都很浅，总觉得很朦胧，似懂非懂，所以今天我打算抽点时间全面了解下这个关键字。



简单来说`synchronized`关键的作用就是为了保障原子性、可见性和有序性。

首先`synchronized`关键字可以修饰变量、方法和代码块。

#### 修饰方法

线程进入`synchronized`修饰的方法时会先上锁（假设没有其他线程访问），方法执行完成后会自动解锁，之后下一个线程才能进入这个方法里，不解锁的话，其他线程是无法访问改方法的。

##### 原理

其原理是通过`flag`标记`ACC_SYNCHRONIZED`，判断方法是否有线程在执行。当调用方法时，调用指令会检查方法的`ACC_SYNCHRONIZED`访问标志是否设置，如果设置了，执行线程先要持有同步锁，然后才能执行方法。

测试方法源码：

```java
synchronized public static void synchronizedTest() {

}
```

反编译结果：

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

从反编译结果中，我们可以看出`ACC_SYNCHRONIZED`标记，表明该方法是`synchronized`的，同时我们还看到了`ACC_PUBLIC`和`ACC_STATIC`，这两个标记应该就分别访问范围和是否是静态方法。



#### 修饰代码块

修饰代码块采用的是` monitorenter`和` monitorexit`指令进行同步处理的，例如如下源码：

```java
 public static void synchronizedCodeBlock() {
            synchronized (SynchronizeTest.class) {
                int count = 100;
            }
        }
```

反编译之后结果如下：

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

这里我直接放出完整的代码。

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

![](https://gitee.com/sysker/picBed/raw/master/images/20220118092022.png)

按照我们的预期，`number`最后的值应该是`200`，但是实际为`193`，说明`this`加`synchronized`不能约束不同实例实例之间的资源共享。

但是如果我们把`main`方法`new Thread(thisTest2).start()`的`thisTest`，然后在运行，这时候就会发现，最终的运行结果始终就是`200`了：

![](https://gitee.com/sysker/picBed/raw/master/images/20220118092545.png)

通过这两次测试，我们可以进一步确定，`synchronized`修饰`this`，只能确保同一个实例的线程之间的同步代码块互斥，而不同实例是不受影响的。



##### class

`synchronized`修饰`class`的代码和`this`没有太多区别，不一样的点是`synchronized`修饰的对象不同：

```java
private void write(int change) throws InterruptedException {
    synchronized (ThisTest.class) {
        Thread.sleep(10L);
        number += change;

    }
}
```





锁的粒度：`object` > `class` > `this`



`this`只会影响当前实例的线程访问；`class`会影响当前类所有实例的线程访问；而`object`会影响所有访问同步代码的访问；在方法上加`synchronize`关键字影响范围就更大了，会影响所有当前方法的访问
