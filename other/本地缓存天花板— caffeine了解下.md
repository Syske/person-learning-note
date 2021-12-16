# 本地缓存天花板— caffeine了解下？

### 前言

最近，我们在重构公司的一个项目（我好像已经说了好多次了，这个项目周期确实比较长），由于一个应用场景并发量特别高，目前设计的并发量为`10`万，虽然有用`redis`作为数据库来存储数据，性能上应该问题不大，但是为了更大性能保证系统性能，我们又在系统中加入了本地化缓存，关于本地缓存，目前的组件比较多，除了`MemoryCache`之外，`guava`也有本地缓存解决方案，但是我们用的是`caffeine`，关于这个组件我大概查了下（之前还真没听说过，有点孤陋寡闻了），发现它的性能确实强，性能是`guava`本地缓存的好几倍，今天我们就来一次`caffeine`破冰。

### caffeine

#### 是什么

`caffeine`是一款高性能的本地缓存组件，关于它的定义，官方描述如下：

> Caffeine is a high performance, near optimal caching library. 

简单翻一下就是：`Caffeine`是一款高性能、最优缓存库。

定义很是简洁，同时文档中也说明了`caffeine`是受`Google guava`启发的本地缓存（青出于蓝而胜于蓝），在`Cafeine`的改进设计中借鉴了 `Guava` 缓存和 `ConcurrentLinkedHashMap`

![](https://gitee.com/sysker/picBed/raw/master/images/20211215212317.png)

##### 项目地址

```
https://github.com/ben-manes/caffeine
```



#### 如何用

下面我们结合官方文档看下，如何在我们的项目中使用`Caffeine`。首先我们需要在项目中增加`Caffeine`的依赖，这里以`maven`为例，其他管理工具可以参考官方文档：

```xml
<dependency>
  <groupId>com.github.ben-manes.caffeine</groupId>
  <artifactId>caffeine</artifactId>
  <version>3.0.5</version>
</dependency>
```

`Caffeine`提供了四种缓存添加策略：

- 手动加载
- 自动加载
- 手动异步加载
- 自动异步加载

值得表扬的是，官方文档提供了中文支持，对不习惯看英文文档的小伙伴简直就是福音，中文文档地址如下：

```
https://github.com/ben-manes/caffeine/wiki/Population-zh-CN
```

这里需要注意的是，`Caffeine`的版本需要和`JDK`对应，比如最新版本（`3.0.5`）对应的`jdk`为`11`，如果`jdk`版本太低，会报如下错误：

![](https://gitee.com/sysker/picBed/raw/master/images/20211215225359.png)

##### 手动加载

手动加载其实就是通过官方提供的`api`，比如`get`、`put`、`invalidate`等接口，手动操作缓存，关于这块的详细描述，官方文档也给出了详细说明，所以我就直接引用了：

> `Cache` 接口提供了显式搜索查找、更新和移除缓存元素的能力。
>
> 缓存元素可以通过调用 `cache.put(key, value)`方法被加入到缓存当中。如果缓存中指定的key已经存在对应的缓存元素的话，那么先前的缓存的元素将会被直接覆盖掉。因此，通过 `cache.get(key, k -> value)` 的方式将要缓存的元素通过原子计算的方式 插入到缓存中，以避免和其他写入进行竞争。值得注意的是，当缓存的元素无法生成或者在生成的过程中抛出异常而导致生成元素失败，`cache.get` 也许会返回 `null` 。
> 当然，也可以使用`Cache.asMap()`所暴露出来的`ConcurrentMap`的方法对缓存进行操作。

下面是手动加载的示例，我是在官方示例的基础上做了小调整：

```java
Cache<String, Object> cache =
            Caffeine.newBuilder().expireAfterWrite(10, TimeUnit.MINUTES).maximumSize(10_000).build();
String key = "hello_caffeine";

// 查找一个缓存元素， 没有查找到的时候返回null
Object object = cache.getIfPresent(key);
// 查找缓存，如果缓存不存在则生成缓存元素, 如果无法生成则返回null
object = cache.get(key, k -> createObject(key));
// 添加或者更新一个缓存元素
cache.put(key, object);
// 移除一个缓存元素
cache.invalidate(key);
System.out.println(cache);
}

private static Object createObject(String key) {
    return "hello caffeine 2021";
}
```



##### 自动加载

自动加载，顾名思义就是查不到数据时，系统会自动帮我们生成元素的缓存，只是这里构建的是`LoadingCache`，同时需要指定元素缓存的构造方法（也就是获取对象的方式，比如查库获取）

```java
// 自动加载
LoadingCache<String, Object> cache2 = Caffeine.newBuilder().maximumSize(10_000)
    .expireAfterWrite(10, TimeUnit.MINUTES).build(CaffeineDemo::createObject);

String key2 = "hello2";
// 查找缓存，如果缓存不存在则生成缓存元素, 如果无法生成则返回null
Object value = cache2.get(key2);
System.out.println(value);
List<String> keys = new ArrayList<>();
keys.add("hello1");
keys.add("hello2");
// 批量查找缓存，如果缓存不存在则生成缓存元素
Map<String, Object> objectMap = cache2.getAll(keys);
System.out.println(objectMap);
```



### 结语