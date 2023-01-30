# 安利一个java开发利器——guava

## 前言

工欲善其事必先利其器，一个好的工具让你花更少的时间，干更多的活，一定程度上比较高效地解放了你的的生产力，让你可以有更多的时间搞事情（摸鱼、划水呀），作为`java`后端开发人员，`guava`对我们而言，就是这样的工具，今天我们就来了解下这把利器。

## guava

### guava是什么

`Guava`是`Google`提供的一组核心`Java`库，包括新的集合类型（如`multimap`和`multiset`）、不可变集合、图形库以及用于并发、`I/O`、哈希、缓存、原语、字符串等的实用程序！它广泛应用于`Google`内部的大多数`Java`项目，也被许多其他公司广泛使用。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210501163756.png)

## guava的应用

既然是工具，那我们关注的就是它的用法，接下来我们就分别从集合、图形、`I/O`、哈希、缓存、原语、字符串等方面，分享一些`guava`的常见应用，让他真正能够解放你的生产力，今天主要介绍`collect`包下的内容，其他内容，感兴趣的小伙伴自己去研究。

首先在我们的项目中，添加`guava`的依赖：

```xml
<dependency>
    <groupId>com.google.guava</groupId>
    <artifactId>guava</artifactId>
    <version>30.1.1-jre</version>
    <!-- or, for Android: -->
    <!--<version>30.1.1-android</version>-->
</dependency>
```

如果是`android`，换下依赖的版本即可。

### 集合(Lists)

包路径：`com.google.common.collect.Lists`

#### 创建和添加对象

正常情况下，我们在`java`中创建和使用`List`的时候，基本都是这样的：

```java
// 创建集合
List<String> stringList1 = new ArrayList<>();
// 添加对象
stringList1.add("hello");
stringList1.add("world");
```

但是，如果你用了`guava`，那上面这些你都可以一步到位：

```java
List<String> stringList2 = Lists.newArrayList("hello", "world");
```

还支持直接传入数组：

```java
String[] strings = new String[] {"1231", "23432423"};
ArrayList<String> strings1 = Lists.newArrayList(strings);
```

#### list分割

更强大的是，它还支持`List`分割，我们在日常开发中经常有这样的需求，比如某个接口或方法限制了`List`数据量大小（比如`list`的大小不能超过`200`），这时候你如果自己手动写一个分割工具类就很麻烦，但如果用`guava`，那就很简单：

```java
List<List<String>> partition = Lists.partition(stringList1, 200);
```

上面代码的作用就是把我们的`stringList1`分割成`200`一份的小`list`，这时候你再配合上`forEach`，需求就完美实现了。

让你的开发过程更简单，更便捷，其他`List`的子类创建类似。

#### list反转

实际开发中，经常要将`list`反转，比如`1, 2, 3, 4`的`list`反转成`4, 3, 2, 1`，自己写的话，需要写个`for`循环，然后反向输出到另一个`List`，但是用`guava`就贼简单：

```java
List<Integer> integerList = Lists.newArrayList(1, 2, 3, 4);
// 反转list
List<Integer> reverse = Lists.reverse(integerList);
```

#### list转换

比如我要将一个`List<String>`根据一定的条件转换成一个`List<Boolean>`，我可以这样操作：

```java
List<String> stringList2 = Lists.newArrayList("hello", "world", "");
List<Boolean> transform = Lists.transform(stringList2, s -> !"".equals(s));
```

我转换的条件是只有不是空字符串就是`true`，这里`s -> !"".equals(s)`是`lamubda`表达式的写法（最近一直在提这个，这个现在确实已经是主流了），展开写确实占行数：

```java
List<Boolean> transform2 = Lists.transform(stringList2, 
     new Function<String, Boolean>() {
            @Override
            public @Nullable Boolean apply(@Nullable String input) {
                return !"".equals(input);
            }
        });
```

其他更多方法，大家自己下载研究，上面这些已经很可以了，满足日常大部分需求，接下来，我们再来看下`Maps`。

### Maps

与`List`类似，`Maps`这个类也提供了很多`map`相关的方法，下面我们就来看一下。

#### 创建map

```java
HashMap<Object, Object> objectObjectHashMap = Maps.newHashMap();
        HashMap<Object, Object> objectObjectHashMap1 = Maps.newHashMap(objectObjectHashMap);
```

#### 比较两个map

这个方法就很强大，不仅可以返回两个`map`的交集，还能返回每个`map`不同的地方，结果都是`map`

```java
HashMap<Object, Object> objectObjectHashMap = Maps.newHashMap();
        objectObjectHashMap.put("k1", "v1");
        objectObjectHashMap.put("k2", "v2");
        objectObjectHashMap.put("k3", "v3");

        HashMap<Object, Object> objectObjectHashMap1 = Maps.newHashMap(objectObjectHashMap);
        objectObjectHashMap.put("k4", "v4");
        objectObjectHashMap1.put("k5", "v5");
// 比较两个map
        MapDifference<Object, Object> difference = Maps.difference(objectObjectHashMap, objectObjectHashMap1);
// 返回交集
        Map<Object, Object> objectObjectMapCommon = difference.entriesInCommon();
// 返回左侧map特有的
        Map<Object, Object> objectObjectMap1Left = difference.entriesOnlyOnLeft();
// 返回右侧map特有的
        Map<Object, Object> objectObjectMap2Right = difference.entriesOnlyOnRight();
        System.out.println(objectObjectMapCommon);
        System.out.println(objectObjectMap1Left);
        System.out.println(objectObjectMap2Right);
```

#### 将集合转为Map

这里还提供了将`List`等集合转为`map`的方法：

```java
ImmutableMap<String, String> stringStringImmutableMap2 = Maps.toMap(stringList, s -> s);
```

上面的代码就是将一个`list`转成`key`和`value`都一样的`map`。

或者将`map`转换为新的`map`:

```java
        ImmutableMap<Map.Entry<String, Object>, Boolean> entryBooleanImmutableMap = Maps.toMap(stringObjectImmutableMap.entrySet(), k -> "123123".equals(k));
```



## 总结

今天，我们分享了`Lists`和`Maps`的很多常用的方法，并演示了常用的方法，还有很多内容没讲到，一方面说明它也不常用（我没用到就是不常用），另外一方面，`guava`目前我只用到了集合下的一部分功能，所以目前就分享这么多。但是，`guava`用起来真的很方便，也确实解决了很多开发中的问题，提高了我们的开发效率，至于其他的内容，后期看情况。

最后，我们先安利另外一款比较火的工具包——`huTool`，提供的方法也很丰富，因为是国人开源的，所以很容易上手，这里我们先简单预告下，后期专门分享，工具包官方开源地址：

```
https://hutool.cn/
```

好了，今天就到这里吧！