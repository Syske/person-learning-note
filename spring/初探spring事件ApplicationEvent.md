# 初探spring事件applicationEvent

### 前言
不知道各位小伙伴对事件（`event`）这个比较抽象的名词如何理解，从我实际开发和使用经验来说，事件通常指的是某一特定条件下触发的一组操作。
一个事件主要包括以下几个要素：
- 事件的注册
- 事件的触发


### Application

#### 是什么




#### 如何用


首先我们需要创建一个`spring-boot`项目，然后在项目的`resouces/META-INF`文件夹下增加名为`spring.factories`的文件，如果文件夹不存在，需要手动创建。
这个文件的作用是配置`spring boot`的常用组件，当然我们也可以通过注解的方式进行配置。

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

##### 事件触发
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



我们需要在文件中增加如下配置：
```
org.springframework.context.ApplicationListener=io.github.syske.springbootbeanlisttest.listener.SyskeApplicationListener
```
这个文件除了可以配置`ApplicationListener`之外，还可以配置`EnvironmentPostProcessor`、`PropertySourceLoader`、`SpringApplicationRunListener`，这几个组件的应用，我们后期也会逐一分享。

这种配置方式其实就是`SPI`机制，这种配置的好处是，可以在不变更项目代码的基础上实现组件的增加和移除。




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
