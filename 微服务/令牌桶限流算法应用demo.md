# 令牌桶限流算法应用demo

### 前言

今天原本是要出一个令牌桶限流算法的`web`应用`demo`的，但是实际在搜索和实现相关算法的时候，发现似乎实现都不理想，于是我就花费了大量的实践用来寻找合适的限流算法，所以也就没有足够的时间来完成相关`demo`了，我不过我这里可以分享下思路，结合我们昨天和前天分享的内容，我想各位小伙伴应该能够自己做出来：

令牌桶限流依然是在拦截器层实现，定义一个令牌桶限流注解，注解中定义速率和令牌桶容量，然后在拦截中获取接口方法注解，实例化限流算法示例，调用限流算法`acquire`方法获取`token`，如果`token`获取失败，则表示目前没有可用令牌（触发限流机制），直接返回错误信息，如果获取到`token`，直接进入到接口中。

下面我们看下今天我这边搜集到额令牌算法：

### 令牌桶限流算法

首先我们先回忆下令牌桶算法的原理：在令牌桶算法中，令牌生产算法以恒定速率不断生成新的令牌放进令牌桶中，当数量达到令牌桶的上线时，生成的新令牌会被丢弃掉。对客户端请求来说，每次请求处理前，先要从令牌桶中获取令牌，如果获取到令牌，则进出接口服务处理相关请求，否则请求被拒绝。

在令牌桶限流算法中，最核心的点有以下几个：

- 令牌的生成速率控制
- 令牌的补充
- 令牌的消耗
- 令牌的获取

我测试了网上绝大多数算法实现，最后只找到一种完全满足需求的算法：

```java
public class TokenBucket5 {
    private ArrayBlockingQueue<Integer> blockingQueue;
    private int limit;
    private TimeUnit unit;
    private int rate;
    private ScheduledExecutorService scheduledExecutorService = Executors.newScheduledThreadPool(1);

    public TokenBucket5(int capacity, TimeUnit unit, int rate) {
        // 存放令牌的队列
        this.blockingQueue = new ArrayBlockingQueue<>(capacity);
        // 令牌桶容量
        this.capacity = capacity;
        // 限流的时间单位
        this.unit = unit;
        // 限流的时间限制（速度），用于控制令牌生成速度
        this.rate = rate;
        init();
        start();
    }

    // 初始化令牌桶
    private void init() {
        for (int i = 0; i < capacity; i++) {
            blockingQueue.add(i);
        }
    }

    // 创建令牌
    private void createToken() {
        blockingQueue.offer(1);
    }

    // 启动令牌创建定时线程池
    private void start() {
        scheduledExecutorService.scheduleAtFixedRate(this::createToken, rate, rate, unit);
    }

    // 获取令牌资源
    public boolean acquire() {
        return blockingQueue.poll() == null ? false : true;
    }

    // 释放线程池资源
    public void release() {
        scheduledExecutorService.shutdown();
    }
}
```

在这个算法实现中，令牌的生成采用了定时线程池，生成的线程池被放进固定尺寸的令牌队列中，获取令牌时令牌从队列中删除掉（当队列的`count`为`0`时，返回为`null`，所以如果`poll`方法不为空时表示仍然有令牌），生成令牌时会将令牌插入队列。

#### 测试

下面我们进行一些简单测试：

```java
public static void main(String[] args) {
    TokenBucket5 tokenBucket5 = new TokenBucket5(5, TimeUnit.MILLISECONDS, 100);
    try {
        for (int i = 0; i < 100; i++) {
            boolean acquire = tokenBucket5.acquire();
            System.out.printf("timestamp:%s, hello，result: %s\n", System.currentTimeMillis(), acquire);
            Thread.sleep(5L);
        }
    } catch (InterruptedException e) {
        e.printStackTrace();
    } finally {
        tokenBucket5.release();
    }

}
```

运行结果如下：

![](https://gitee.com/sysker/picBed/raw/master/blog/20211102234547.png)

当我们的业务处理时间很短，而令牌生成很慢时，绝大多数请求都获取令牌失败（每隔`100ms`生成一个，业务只需要`5ms`），如果将业务处理时间增加或者将令牌生成时间减小，这时候就可以发现，绝大多数的业务都会处理成功，偶尔会有个别获取令牌失败：

![](https://gitee.com/sysker/picBed/raw/master/blog/20211102234916.png)

至此，我们的限流目的也基本上达到了。

### 总结

关于令牌桶限流这块没有什么好总结的，但是在真个检索算法的过程中，感触倒是不少，特别是越发地意识到自己对多线程这块地认知真的是太浅薄了，所以后面会加强这块地学习。好了，今天就先到在这里吧，各位小伙伴，晚安吧！