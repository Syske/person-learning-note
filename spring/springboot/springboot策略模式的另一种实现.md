# springboot策略模式的另一种实现

### 前言

在很早之前，我们曾分享过`springboot`的一种策略模式实现，在我们当时的实现中，不仅需要自定义策略服务的初始化过程，而且我们还需要手动处理策略服务的类扫描逻辑，整个实现逻辑不仅繁琐、不够简洁，而且需要增加项目的基础配置类，一定程度上会破坏项目的整体架构，所以我在实际开发中也很少用，除非策略模式特别必须，而且策略服务特别多，否则我也不太愿意增加整套初始化操作。

对之前策略模式实现过程感兴趣的小伙伴（主要是通过自定义注解和自定义类的扫描、初始化过程实现策略注入），可以去回顾下：

对之前策略模式实现过程感兴趣的小伙伴可以去回顾下：

https://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&amp;mid=2648421490&amp;idx=1&amp;sn=a0e8bcda3b70daa8b05c11d513576765&amp;chksm=bea6daf889d153eeef60c9a83d68c34b654eac25cdf8fd2fb90590bc9a0b445531667e671aa8&token=525022170&lang=zh_CN#rd

今天我们来分享另一种策略模式的实现方式，好处就是实现简单，不需要引入额外的配置类和繁琐的服务初始化过程，下面我们就来一起看下具体的实现过程吧。



### 实现过程

首先，我们需要定义一个策略服务的接口，这个接口的作用就是为了让具体的策略实现，然后便于后面`springboot`帮我们注入到策略容器中，比如我们有一个`TestInterface`的策略接口，接口很简单只有一个方法：

```java
public interface TestInterface {
    
    String hello();
}
```

它的实现分别是：

这里需要留意的是，我们这里为每个策略的实现类制定了`bean`的名称，这个名称可以作为一种业务选择器来使用，大家可以理解为策略类型，在后面的代码中，我们可以看到，我们其实是可以根据这个名称拿到对应策略的实例的

策略服务`Test1`

```java
@Service("Test1")
public class Test1Impl implements TestInterface {
    @Override
    public String hello() {
        return "Test1Impl";
    }
}
```

策略服务`Test2`

```java
@Service("Test2")
public class Test2Impl implements TestInterface {
    @Override
    public String hello() {
        return "Test2Impl";
    }
}
```

策略服务`Test3`

```java
@Service("Test3")
public class Test3Impl implements TestInterface {
    @Override
    public String hello() {
        return "Test3Impl";
    }
}
```

然后在我们需要用到策略服务的地方，注入我们策略服务的容器：

```java
@RestController
public class TestController {
    // 可以将我们的策略注入到list中
    @Autowired
    private List<TestInterface> testInterfaces;
    // 或者注入到Map中
    @Autowired
    private Map<String, TestInterface> testInterfaceMap;

    @GetMapping("/test")
    public Object test(String name) {
        int size = testInterfaces.size();
        System.out.println(testInterfaces.get(2).hello());
        TestInterface testInterface = testInterfaceMap.get(name);
        System.out.println(testInterface.hello());
        System.out.println(size);
        return size;
    }
}
```

下面我们简单测试一下：

```
###
GET http://localhost:8088/test?name=Test1
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20220626210859.png)

可以看到我们已经拿到了`Test1`的策略服务，执行结果如下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20220626211225.png)

整个过程是不是很简单呢？这里的核心代码其实就是这一行：

```java
@Autowired
private Map<String, TestInterface> testInterfaceMap;
```

这一段代码的作用就是构建策略服务的`beanName`和`bean`实例的映射关系，因为我们在`testInterfaceMap`变量上加了`@Autowired`注解，所以容器的填充其实是由`spring boot`帮我们自动完成的。

这里我觉得有必要稍微解释下，当时看到有同事写了类似这样的代码：

```java
@Autowired
private List<TestInterface> testInterfaces;
```

在接口的处理逻辑中，他直接循环遍历上面的`testInterfaces`，然后调用接口的方法。

我当时第一眼看到这样的代码，我其实也是懵逼的，我寻思这`testInterfaces`没有进行初始化操作，实际调用不会报错吗，我还以为他是在别的地方写了初始化和注入的操作。

然后找了半天也没找到，最后和他探讨之后，才知道，原来这样的操作是`spring boot`本身就具备的特性（然鹅我竟然一直不知道😲），而且很简单、很常用。

今天我们用的`Map`的写法，也是类似的操作，类似一种变形，在实际应用的时候，稍微测试下应该就可以琢磨出来，感觉也不太难，这玩意就是你不用，你永远可能都不知道🐶。



### 总结

今天的内容很简单，其实核心就是`@Autowired`的特殊使用，既是分享普及，又是回顾总结。分享普及是对压根不知道的小伙伴而言的，比如我，回顾总结是对已经应用过的小伙伴。

下面，我们再简单对比下这种策略模式的一些区别，方便各位小伙伴根据自己的需求选用：

今天我们实现的策略模式相比于之前我们实现的策略模式，更简单、更方便，从代码量上来说，也更简洁，而且可以满足我们日常开中绝大多数的策略模式实现需求；

但是它也有一定的局限性，如果我们的策略服务初始化过程中有一些特出的处理需求，比如注入特殊的配置文件，这时候我们之前的策略模式实现方式就显得更灵活。

简单一句话总结，就是前者小而简单，后者大而灵活。

最后，我们来说的题外话，最近一段时间，应该说很久很久，我已经没有更新新的内容了，原因很多，说起来很复杂，但是核心的点还是懒（不在状态呀，卷不动了），不过从本次内容的更新开始，就意味着失踪人口的回归（再不产出点东西，脑子都瓦特啦)，所以未来我会尽可能分享更多有价值的内容，好了，今天的内容就先到这里吧，感谢各位小伙伴的关注和支持，晚安吧！