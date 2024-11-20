# 初探spring事件applicationEvent

### 前言
不知道各位小伙伴对事件（`event`）这个比较抽象的名词如何理解，从我实际开发和使用经验来说，事件通常指的是某一特定条件下触发的一组操作。

做过生态开发（`ISV`）的小伙伴一定对事件不陌生，因为在和这些生态厂商（钉钉、企微、飞书等）进行业务交互的时候，总是避不开事件的，我们总是要对接他们的各种事件，比如入职事件、离职事件、用户变更事件、部门变更事件等等。

今天我们就来通过一个简单的示例，来演示下`ApplicationListener`应用级事件的使用流程。


### ApplicationEvent

#### 是什么
一个事件主要包括以下几个要素：
- 事件注册
- 事件监听
- 事件触发

所以`ApplicationEvent`就是`spring`提供的一套集事件注册、监听、触发为一体的事件实现。



#### 如何用

##### 创建项目，增加模块配置

首先我们需要创建一个`spring-boot`项目，然后在项目的`resouces/META-INF`文件夹下增加名为`spring.factories`的文件，如果文件夹不存在，需要手动创建。

这个文件的作用是配置`spring boot`的常用组件，当然我们也可以通过注解的方式进行配置，关于注解的说明我们后面再说。

我们需要在文件中增加如下配置：
```
org.springframework.context.ApplicationListener=io.github.syske.springbootbeanlisttest.listener.SyskeApplicationListener
```
这个文件除了可以配置`ApplicationListener`之外，还可以配置`EnvironmentPostProcessor`、`PropertySourceLoader`、`SpringApplicationRunListener`，这几个组件的应用，我们后期也会逐一分享。

这种配置方式其实就是`SPI`机制，这种配置的好处是，可以在不变更项目代码的基础上实现组件的增加和移除。

创建自己的`ApplicationListener`，这里需要实现`ApplicationListener`接口，并实现`onApplicationEvent`方法，事件触发时，会执行该方法。
```java
public class SyskeApplicationListener implements ApplicationListener<SyskeApplicationEvent> {
    @Override
    public void onApplicationEvent(SyskeApplicationEvent event) {
        String eventName = event.getEventName();
        System.out.println(eventName);
        Object eventBody = event.getEventBody();
        System.out.println(eventBody);
    }
}
```
这个方法的入参是`ApplicationEvent`或者它的子类，所以这里我们可以根据需要自定义自己的事件，并继承`ApplicationEvent`
```
public class SyskeApplicationEvent extends ApplicationEvent {
  
    public SyskeApplicationEvent(Object source) {
        super(source);
    }

    private String eventName;

    private Object eventBody;
    // getter/setter方法省略
}
```



#### 事件注册

因为我们是直接在`spring boot`项目中使用的`spring`的事件组件，所以我们并不需要自己去做事件的注册，因为在`spring boot`的启动过程中，会帮我们把事件进行注册，关于这块的内容，我在之前分享`spring boot`启动过程的时候已经分享过了，感兴趣的小伙伴可以去看下（时间久到我都忘记了🐶）：

这里放一个启动流程的图：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20220904194644.png)
从上面这个图中，我们可以清楚地看到，这里获取了所有的`SpringApplicationRunListener`，并分别执行了他们的`starting`和`started`方法，但是这里的`listener`并不是我们的事件监听器，而是`spring boot`的运行监听器，但是我们事件监听器的初始化确实是在这里完成的，因为这里也初始化了我们事件的运行监听器，并执行了它的的`starting`和`started`方法：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20220904195614.png)
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20220904200341.png)
好了，至此，我们知道`spring boot`的事件是何时注册的，下面我们来一起看下事件如何触发。

##### 事件触发
事件的触发，没啥好解释的，就是让事件监听器的`onApplicationEvent`方法执行
```java
 SyskeApplicationEvent syskeApplicationEvent = new SyskeApplicationEvent("test");
        syskeApplicationEvent.setEventName("sysk-event");
        syskeApplicationEvent.setEventBody("sysk-body");
        applicationContext.publishEvent(syskeApplicationEvent);
```

##### 测试

```java
@GetMapping("/event")
    public Object testEvent() {
        SyskeApplicationEvent syskeApplicationEvent = new SyskeApplicationEvent("test");
        syskeApplicationEvent.setEventName("sysk-event");
        syskeApplicationEvent.setEventBody("sysk-body");
        applicationContext.publishEvent(syskeApplicationEvent);
        return "success";
    }

```
运行结果：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20220830231514.png)

其实，除了我们上面展示的这种配置方式，`spring boot`还提供了另一套更简单便捷的事件实现方式：

```java
@Component
public class Syske2ApplicationListenerConfig {

    @EventListener
    public void onApplicationEvent(Syske2ApplicationEvent event) {
        String eventName = event.getEventName();
        System.out.println(eventName);
        Object eventBody = event.getEventBody();
        System.out.println(eventBody);
        System.out.println("Syske2ApplicationEvent");
    }
}
```
也就说，我们只需要定义自己的事件，然后编写事件触发的操作方法，并在方法上加上`@EventListener`即可，这里的方法名无关紧要，可以随便指定，事件的触发也没有任何区别：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20220904203115.png)
另外，根据实际测试发现，`spring boot`的事件是支持多监听的，也就是类似于广播消息，这里我两个地方都监听了同一个事件，可以看到两个地方都被触发了：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20220904203437.png)



#### 知识扩展

##### 事件
除了今天我们介绍的`ApplicationEvent`之外，还有很多优秀的开源事件组件，比如`guava`的`eventBus`，后面有机会的话，我们可以单独分享下`eventBus`的用法。

##### spring.factories
在今天的内容中，我们在`resouces/META-INF`文件夹下，创建了`spring.factories`文件，其实在`spring-boot`的核心`jar`文件的`META-INF`文件夹也是有这个文件的，当然文件的内容更完整，它包括了以下配置：
- 资源加载器（`org.springframework.boot.env.PropertySourceLoader`）
- 运行监听器（`org.springframework.boot.SpringApplicationRunListener`）
- 错误报告器（`org.springframework.boot.SpringBootExceptionReporter`）
- 应用上下文初始化组件（`org.springframework.context.ApplicationContextInitializer`）
- 应用监听器（`org.springframework.context.ApplicationListener`）
- 环境后置处理器（`org.springframework.boot.env.EnvironmentPostProcessor`）
- 失败分析组件（`org.springframework.boot.diagnostics.FailureAnalyzer`）
- 失败分析报告组件（`org.springframework.boot.diagnostics.FailureAnalysisReporter`）

当然，并不是所有的公司都会用到事件，因为事件本身有一些局限性，比如说如果你的服务是集群环境的话，事件是不可以多节点共享的，所以很多公司可能会更愿意用`mq`。

其实，关于事件的使用场景以及为什么要使用事件，我觉得我好像还没想明白，在我看来，事件应该是类似于异步线程池一样的存在，当然这样的思考可能有失偏薄，毕竟每一种技术的存在都是为了解决某些其他技术解决不了的问题~

好了，今天的内容就到这里吧，感谢各位小伙伴的支持，晚安哟