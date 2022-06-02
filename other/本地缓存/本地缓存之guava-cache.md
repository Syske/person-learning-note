# 本地缓存之guava-cache

### 前言

前几天我们分享了一款性能非常优秀的本地缓存组件——`caffeine`，在`caffeine`的官方文档中提到设计上参考了`guava cache`的相关内容，所以今天我们本着追流溯源的想法，来看下`guava cache`的相关内容。



### guava cache

关于`guava`这个工具包，想必各位小伙伴肯定不会陌生，从集合工具包，到限流组件，再到上次刚分享的布隆过滤器，每一次都刷新了我对`guava`这个工具包的认知，现在想想自己以前真的是孤陋寡闻，搞`java`开发，竟然连`guava`都不知道。

`guava cache`之前在安利`guava`工具包的时候有提到过，但之后并没有并没有深入研究过，所以今天算是对`guava cache`的一次简单探索。

`guava cache`位于`com.google.common.cache`包下，核心的类有两个，一个是`CacheBuilder`，是用来构建缓存的，另一个是`Cache`，也就是缓存容器，用来存放缓存数据的。

#### 简单用法

下面是`guava cache`的一个简单示例：

```java
// 实例化缓存构建器
CacheBuilder cacheBuilder = CacheBuilder.newBuilder();
// 构建缓存容器
Cache<String, String> cache = cacheBuilder.build();
// 缓存数据
cache.put("cache", "cache-value");
// 获取缓存数据
String value = cache.getIfPresent("cache");
// 删除缓存
cache.invalidate("cache5");
```



#### CacheBuilder方法

下面我们看下`CacheBuilder`的一些常用的配置方法。

##### maximumSize

设置构建缓存容器的最大容量，当缓存数量达到该容量是，会删除其中的缓存（根据实际测试结果，会先删除先放入的数据）

```java
CacheBuilder cacheBuilder = CacheBuilder.newBuilder().maximumSize(10L);
Cache<String, String> cache = cacheBuilder.build();
for (int i = 0; i < 11; i++) {
    cache.put("cache" + i, "cache-value" + i);
}
System.out.println(cache.size());
System.out.println(cache.getIfPresent("cache0"));
System.out.println(cache.getIfPresent("cache10"));
```

最终运行结果：
![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211219165506.png)

##### concurrencyLevel

设置并发等级，也就是同时操作缓存的线程数。默认是`4`。在`guava cache`的实现中，会根据这个值创建一个希表段，每个哈希表段由其自己的写锁控制。每次显式写入都会使用一次段锁，每次缓存加载计算都会使用两次段锁（一次在加载新值之前，一次在加载完成之后），许多内部缓存管理是在段粒度上执行的。

```java
CacheBuilder cacheBuilder = CacheBuilder.newBuilder().maximumSize(10L).concurrencyLevel(5);
```



##### expireAfterWrite

缓存写入多久后过期，这个方法和我们前面分享的`Caffeine`是一样的。



##### expireAfterAccess

访问后多久过期，这个方法也和`Caffeine`是一样的。



##### refreshAfterWrite

缓存写入多久后刷新，这个方法也和`Caffeine`的一样，这几个方法应该就是`Caffeine`文档中所说的设计借鉴吧。



##### 其他方法

`initialCapacity`：设置内部哈希表的最小容量，这个值的设置通常与`concurrencyLevel`方法相关，如果设置不当会浪费不必要的内存



#### Cache方法

`cache`的方法主要是用来操作缓存的，除了我们前面示例中的几种常用方法之外，`Cache`还提供了以下方法：

- `get`：`key`不存在时，则通过执行指定的`Callable`构建缓存，这个操作和`Caffeine`中的手动加载很像：

```java
String getCache = cache.get("cache0", () -> buildCache("cache0"));
```

- `getAllPresent`：根据指定的`keys`获取对应的缓存数据，和`getIfPresent`方法很像，只是这里是获取多个数据
- `putAll`：和`map`的操作一样，这里就是将一批数据放到缓存中。
- `invalidateAll`(带参数)：删除一批缓存数据，需要指定`key`
- `invalidateAll`：删除缓存中所有数据



### 结语

好了，关于`guava cache`的简单用法我们就分享这么多，感兴趣的小伙伴可以亲自上手实践下。当然，我也清楚，`guava cache`最值得研究的应该就是它的源码实现了，所以后面有时间我要先去研究下，然后再视情况分享。

近期，因为工作上的事一直忙的焦头烂额，偶尔也回来比较晚，所以也没有输出太多有价值的内容。明天打算梳理下思绪，重新学习多线程相关内容，这一块的内容是值得反复学习和琢磨的；另外上次也说了自己数据结构方面的知识比较薄弱，所以数据结构和算法相关的内容也要加强，最后一块就是`jvm`的相关内容了，这一块也算是和数据结构关系比较紧密，而且也涉及到很多底层实现，学好这一块才能对`java`有更深的理解，毕竟数不能白买不是！

最近疫情有严重了，天气也变冷了，各位小伙伴一定要做好个人防护，毕竟也快过年了，还是要照顾好自己的，身体才是革命的本钱嘛。好了，各位小伙伴晚安吧！

最后再给各位小伙伴安利一本高赞的数，我最近也打算好好研读下：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211219230324.png)

没有资源的小伙伴可以联系我！