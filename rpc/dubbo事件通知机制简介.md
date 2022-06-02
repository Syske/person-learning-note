

# dubbo事件通知机制简介
tags: [#rpc, #dubbo]

### 前言

原本今天是想分享`dubbo`的事件通知机制的，但是试了好多次，一直都没有成功，最后看到官方给出的回复：

```
oninvoke ,onreturn,onthrow do work well in xml ,but do not work when use annotation
```

也就是说事件通知在注解模式下不支持，所以我就不打算继续研究了，我现在就只想研究注解模式，感兴趣的小伙伴自己去看下，这里我们就简单介绍下事件通知机制。

### 事件通知

事件通知机制简单来说就是针对在调用之前、调用之后、出现异常时的时间通知，就是我们人为指定的回调函数，从`2.0.7`以后的版本开始支持，我想后续应该会增加对注解模式的支持。

事件回调机制主要是针对服务调用方，也就是消费者的，配置方式也很简单，只需要在`dubbo`的消费者`xml`中加入`dubbo:method`，并指定`oninvoke`、`onreturn`、`onthrow`方法：

```xml
<bean id ="demoCallback" class = "org.apache.dubbo.callback.implicit.NotifyImpl" />
<dubbo:reference id="demoService" interface="org.apache.dubbo.callback.implicit.IDemoService" version="1.0.0" group="cn" >
      <dubbo:method name="get" async="true" onreturn = "demoCallback.onreturn" onthrow="demoCallback.onthrow" oninvoke = "demoCallback.oninvoke"/>
</dubbo:reference>
```

其中，`demoCallback`是我们自己定义的回调接口，具体实现如下：

```java
class NotifyImpl implements Notify {
    public Map<Integer, Person>    ret    = new HashMap<Integer, Person>();
    public Map<Integer, Throwable> errors = new HashMap<Integer, Throwable>();
    
    public void onreturn(Person msg, Integer id) {
        System.out.println("onreturn:" + msg);
        ret.put(id, msg);
    }
    
    public void onthrow(Throwable ex, Integer id) {
        errors.put(id, ex);
    }
    
    public void oninvoke(Integer id) {
        System.out.print(id)
    }
}
```

#### 我的错误

下面是我的调用方代码：

```java
@DubboReference(version = "1.0", interfaceName = "demoService", interfaceClass = DemoService.class,
            loadbalance = "roundrobin", methods = {@Method(name = "sayHello", oninvoke = "callBackDemoService.oninvoke")})
    private DemoService demoService;

    @RequestMapping("/test")
    public Object demo() {
        String hello = demoService.sayHello("world");
        System.out.println(hello);
        return hello;
    }
```

回调接口实现：

```java
@Service("callBackDemoService")
public class CallBackDemoServiceImpl implements CallBackDemoSevice {
    @Override
    public void oninvoke(String name) {
        System.out.println("oninvoke name =" + name);
    }

    @Override
    public String onreturn(String response) {
        System.out.println("onreturn response =" + response);
        return "onreturn" + response;
    }

    @Override
    public void onthrow(Throwable t) {
        System.err.println("onthrow Throwable =" + t);
    }
}
```

我通过注解指定了`oninvoke`的方法，但是在调用服务提供者的时候报错了，控制台错误提示如下：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210817134225.png)

然后我`debug`发现，是因为`AsyncMethodInfo`的`oninvokeMethod`方法为空导致的

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210817134125.png)

在搜集错误的过程中，我发现了下面这些很有用的知识点，各位小伙伴可以看下：

##### `oninvoke`方法

- 必须具有与真实的被调用方法`sayHello`相同的入参列表：例如，`oninvoke(String name)`

##### `onreturn`方法

-  至少要有一个入参且第一个入参必须与`getUserName`的返回类型相同，接收返回结果：例如，`onReturnWithoutParam(String result)`；
- 可以有多个参数，多个参数的情况下，第一个后边的所有参数都是用来接收`getUserName`入参的：例如， `onreturn(String result, String name)`

##### `onthrow`方法

- 至少要有一个入参且第一个入参类型为`Throwable`或其子类，接收返回结果；例如，`onthrow(Throwable ex)`;
- 可以有多个参数，多个参数的情况下，第一个后边的所有参数都是用来接收`getUserName`入参的：例如，`onthrow(Throwable ex, String name)`;

- 如果是`consumer`在调用`provider`的过程中，出现异常时不会走`onthrow`方法的，`onthrow`方法只会在`provider`返回的`RpcResult`中含有`Exception`对象时，才会执行。（`dubbo`中下层服务的`Exception`会被放在响应`RpcResult`的`exception`对象中传递给上层服务）

#### 好吧，我妥协了

最后，我还是用`xml`的方式测试了，确实是可以回调的，`dubbo`消费者`xml`配置如下：

```xml
<?xml version="1.0" encoding="utf-8" ?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:dubbo="http://dubbo.apache.org/schema/dubbo"
       xmlns="http://www.springframework.org/schema/beans" xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
       http://dubbo.apache.org/schema/dubbo http://dubbo.apache.org/schema/dubbo/dubbo.xsd http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd">
    <context:property-placeholder/>
    <bean id ="demoCallback" class = "io.github.syske.demo.service.consumer.callback.impl.CallBackDemoServiceImpl" />
    <dubbo:reference id="demoService" interface="io.github.syske.common.facade.DemoService" version="1.0" >
        <dubbo:method name="sayHello" async="true" oninvoke="demoCallback.oninvoke" onreturn = "demoCallback.onreturn" onthrow="demoCallback.onthrow" />
    </dubbo:reference>

    <dubbo:application name="callback-consumer"/>

    <dubbo:registry address="zookeeper://${zookeeper.address:127.0.0.1}:2181"/>

</beans>
```

修改主程序，删除原有注解：

```java
@SpringBootApplication
//@EnableDubbo
public class DemoConsumerApplication {

    public static void main(String[] args) {
        ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext("consumer.xml");
        context.start();
        DemoService demoService = (DemoService) context.getBean("demoService");
        String hello = demoService.sayHello("world");
        System.out.println(hello);
    }

}
```

然后启动运行，从控制台看出，我们的回调方法都被执行了：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210817152119.png)

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210817152105.png)

根据实现机制，我推测回调方法是基于动态代理实现的，关于动态代理的应用我们前面在分享手写`rpc`的时候有讲过，最常用的场景之一就是`AOP`，据说`Spring`、`Struts`等框架就是通过动态代理技术来实现日志、切面编程这些操作的。

#### 柳暗花明又一村

用`xml`的方式测试完成后，我又看了下关于那个问题官方给出的回复，发现在`2021.5.12`日这个问题已经被修复了，说明之后的版本已经可以通过注解方式进行事件通知回调了，而且我亲测在`2.7.12`之后的版本就已经可以了：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210817153344.png)

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210817153450.png)

感觉我可真是个小机灵鬼，这都让我发现了😊，当然我也停享受这个柳暗花明又一村的感觉的，这种学习方式感觉挺好，就像发现新大陆一样……

### 总结

目前来看，事件通知的最大应用场景就是`AOP`，但是缺点是，每个方法都需要单独指定（`@Method(name = "sayHello", oninvoke = "callBackDemoService.oninvoke")`中的`name`是必填项，而且不支持正则表达式），这就很不友好了，但是有总比没有强，你说呢？

好了，今天的内容就到这里吧，有兴趣的小伙伴自己动手试下哦！

项目源码地址如下：

```
https://github.com/Syske/learning-dome-code/tree/dev/spring-boot-dubbo-demo
```

