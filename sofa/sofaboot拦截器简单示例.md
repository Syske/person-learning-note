# sofaboot拦截器示例

## 前言

拦截器是`web`应用开发中的一个特别重要的技术工具，通过它我们可以实现很多复杂的业务场景，比如鉴权、参数校验等


## 拦截器

下面的拦截器继承的是`com.alipay.sofa.rpc.filter.Filter`，这是`sofa-rpc`提供的一个`Filter`的`SPI`抽象类，`spfa`的官方依赖中也有很多已经实现的拦截器：
![拦截器实现](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221219121543.png)

`Filter`有三个方法，分别是：

- `needToLoad`：调用时是否需要加载，该方法有默认实现，默认返回`true`
- `invoke`：该方法为抽象方法，是必须要实现，同时它也是拦截器的核心部分，你的拦截业务需求就是在这里完成的
- `onAsyncResponse`：顾名思义，该方法是异步响应回调，根据方法说明，该方法仅对消费者一侧生效，会在异步调用响应后执行

根据`sofa-rpc`提供的拦截器实现，我们可以看到，拦截器可以增加如下注解：

- `@Extension`：该注解的核心参数有两个，一个是`value`，值为拦截器的名称，官方说明是扩展点名称，参数不能省略，必须和配置文件中的名字保持一致；另一个核心参数是`order`，表示优先级，默认不需要
- `@AutoActive`：是否自动激活，该注解有两个参数，一个是`providerSide`，表示提供者侧是否激活，一个是`consumerSide`，表示消费者侧是否激活，默认两个参数都是`false`，从这里可以看出，如果拦截器缺少这个注解或者注解参数不配置，拦截器本身不会生效。

### 拦截器实现

到这里，我们会发现拦截器的实现本身已经没有任何难度了，我们只需要实现`invoke`方法，完成我们的拦截需求即可，当然如果你有异步调用需求的话，你可能还需要实现`onAsyncResponse`方法

```java
@Extension(value = "myRpcFilter")
@AutoActive(providerSide = true, consumerSide = true)
@Slf4j
public class MyRpcFilter extends Filter {
    @Override
    public SofaResponse invoke(FilterInvoker filterInvoker, SofaRequest sofaRequest) throws SofaRpcException {
        log.info("sofaRequest:{}",sofaRequest);
        SofaResponse sofaResponse = filterInvoker.invoke(sofaRequest);
        log.info("sofaResponse:{}",sofaRequest);
        return sofaResponse;
    }
}
```

我们这里的实现很简单，只是简单打印了请求入参和响应结果

### 配置

首先，你需要在项目的`resources/META-INF`文件夹下创建`services/sofa-rpc`文件夹；

然后在该文件夹下创建一个名为`com.alipay.sofa.rpc.filter.Filter`，在文件中加入如下的配置即可：

```properties
myRpcFilter=io.gihub.syske.sofa.sofaserver.filter.MyRpcFilter
```

需要注意的是，这里的`myRpcFilter`是我自己定义的，你可以修改，但是必须与拦截器的`@Extension`注解的`value`保持一致，否则拦截器不会被识别。

![拦截器](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221219121121.png)


### 简单测试

`sofaRequest`：

![sofaRequest](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221219125728.png)

`sofaResponse`:
![sofaResponse](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221219125913.png)


## 总结

