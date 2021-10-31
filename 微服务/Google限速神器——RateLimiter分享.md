# Google限速神器——RateLimiter分享

### 前言

对微服务有所涉猎的小伙伴，应该都知道限流组件这个东西，它是微服务领域中有一个特别重要的组件，它的作用是限制同一时间点访问某一个服务的线程的数量或者请求数，而且这样的场景在现实应用开发中使用的也别广泛，比如双十一秒杀、春运抢票。

如果没有这个组件的加持，那么我们的服务器很容易因为瞬时并发数量过高而导致宕机，所以换句话说，一个系统运行是否稳定，限流组件起着特别重要的作用的，所以从今天开始，我打算搜集下常用的限流解决方案，逐一研究下其基本原理，当然以我现阶段的积累，可能不会涉及太深。

今天我们就来看下`googlg` 的`guava`中提供的一款限流组件——`RateLimiter`，关于`guava`这个工具包，我们之前已经分享过其中集合部分的应用，感兴趣的小伙伴可以去看下：

![](https://gitee.com/sysker/picBed/raw/master/blog/face-img-cb6bcf37e7ce49879104ba69d4909e3f.jpg)

https://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648417486&idx=1&sn=eb5aeaa688345cd64e3b77e527e95901&chksm=bea6ca4489d14352265b659325965918ad148ef932ad60af0baeaa85525afea0d2d31a2e0539&token=643197278&lang=zh_CN#rd

其实关于限流组件这块，我们当时在分享多线程相关内容的时候，有一个多线程组件就可以用来做限速使用，不知道给位小伙伴是否还记得——`Semaphore`，如果你还记得名字，说明你多线程这块学的还是比较扎实的，忘记了也没关系，好好复习下就好。

另外，因为`Semaphore`之前已经分享过了，所以今天就不再赘述了，感兴趣的小伙伴自己可以去看下：

![](https://gitee.com/sysker/picBed/raw/master/blog/face-img-16e960fb24364c81849607aab7d6c429.jpg)

https://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648419288&idx=1&sn=e893e3ee0877070fe541ce3add98781a&chksm=bea6c55289d14c44b11d27ac99a3c19d0ca1ba12bad8ecaf4671200e7d743f896a477da69195&token=643197278&lang=zh_CN#rd



### RateLimiter

我们先看下官方文档对于`RateLimiter`的描述：

> `RateLimiter`经常用于限制对一些物理资源或者逻辑资源的访问速率。与`Semaphore `相比，`Semaphore `限制了并发访问的数量而不是使用速率。
>
> 通过设置许可证的速率来定义`RateLimiter`。在默认配置下，许可证会在固定的速率下被分配，速率单位是每秒多少个许可证。为了确保维护配置的速率，许可会被平稳地分配，许可之间的延迟会做调整。
>
> 可能存在配置一个拥有预热期的`RateLimiter` 的情况，在这段时间内，每秒分配的许可数会稳定地增长直到达到稳定的速率。

从概念上讲，速率限制器（`RateLimiter`）以可配置的速率分发许可证。 如有必要，每个`acquire() `都会阻塞，直到获得许可为止，然后获取它。 获得许可后，无需发放许可证。

`RateLimiter `对于并发使用是安全的：它将限制来自所有线程的总调用率。 但请注意，它并不能保证公平。

这块的文字描述显得很生硬，不过等你看完示例之后再来看，应该就明白了。



#### 源码简单分析

从源码来看，`RateLimiter`是一个抽象类，而且它并没有直接对外提供构造方法，所以我们只能通过静态方法`create`来创建`RateLimiter`的实例：

![](https://gitee.com/sysker/picBed/raw/master/blog/20211028215055.png)

另外，从源码中发现，这个组件的使用环境必须大于等于`jdk13`，所以各位小伙伴在测试的时候一定要注意：

![](https://gitee.com/sysker/picBed/raw/master/blog/20211028220458.png)

#### 简单使用

其实关于`RateLimter`的使用，在源码的注释中，官方已经给出了相应的示例：

![](https://gitee.com/sysker/picBed/raw/master/blog/20211028221548.png)

第一的示例的作用是，限制线程的执行速率，也就是每秒执行不能超过两次。下面我们通过简单的代码演示下这个示例，然后从实例中体会`RateLimiter`的应用场景。

代码实现很简单，我们通过线程池提交了`100`个打印操作，然后在线程启动前，我们加了一行代码：

```
rateLimiter.acquire()
```

这行代码的作用就是控制速率，这个方法就更过分了，它需要`jdk16`以上才能运行，我这里刚好是`16`， `13`的版本返回值是`void`:

![](https://gitee.com/sysker/picBed/raw/master/blog/20211028222246.png)

根据这段代码，以及我们的多线程使用经验来说，这个方法本身是阻塞的，而且阻塞是基于`stopwatch`来实现的，而且这里阻塞的时长是根据我们的速率计算的，关于速率我们等下会说到。

下面是示例的完整实现：

```java
public class RateLimiterTest {
    public static void main(String[] args) {
        final RateLimiter rateLimiter = RateLimiter.create(2.0);
        ExecutorService executorService = Executors.newFixedThreadPool(100);
        List<Runnable> tasks = Lists.newArrayList();
        for (int i = 0; i < 100; i++) {
            rateLimiter.acquire();
            executorService.execute(() -> {
                String dateTime = new SimpleDateFormat("HH:mm:ss:SSS").format(new Date());
                System.out.printf("limiter-%s%n", dateTime);
            });
        }
        executorService.shutdown();
    }
}
```

运行结果如下：

![](https://gitee.com/sysker/picBed/raw/master/blog/20211028222717.png)

从运行结果可以看出来，不论运行多少次，每一秒始终只会运行两次，而且两次的间隔时间刚好是`500ms`，这说明时间间隔的算法是`1000ms / 2`（`2`就是我们上面指定的速率），我们可以测试下：

![](https://gitee.com/sysker/picBed/raw/master/blog/20211028223105.png)

当我们将速率设置为`4`时，线程之间间隔的时间接近`250ms`，说明我们上面的推断基本正确，但是速率的具体控制算法还需要进一步研究源码。



### 结语

鉴于时间的关系，`RateLimiter`先将这么多，这里算是引入`RateLimiter`的限流解决方案，希望借此能够勾起各位小伙伴对于限流组件实现原理的思考。

从实际应用角度来看，`RateLimiter`似乎还不具备实际业务应用的条件，一个是因为它的运行环境要求比较高，必须`jdk 16`及以上，现阶段应该很少有企业在正式环境使用这个版本；另一个原因是，`RateLimiter`的类和部分方法上加了`@Bate`这样的注解，表明它应该还是一款正处于开发测试阶段的产品，尚未经过相关论证，应用到先说环境确实也需要谨慎验证。

但是如果作为学习借鉴的话，那`RateLimiter`无疑是比较完美的实验品，从个人的角度来说，我觉得`RateLimiter`的源码值得研究，而且我后期还会进一步探究它的实现原理。好了，今天就先到这里吧，各位小伙伴晚安呀！