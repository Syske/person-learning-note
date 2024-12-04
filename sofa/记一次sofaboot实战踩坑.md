### 背景
前段时间，线上有个查询接口需要优化下，为了偷懒，我直接直接继承了别人已经创建好的`VO`，就是因为这简简单单的继承，让我踩到了一个很无厘头的坑——接口的返回结果一直为空，但是接口的逻辑很简单，就是直接查库，然后把数据转换下，通过`facade`接口返回之后，`vo`的值变成了`null`。

### 复现过程
#### 创建sofaboot项目
这里就不展开讲了，一个服务提供者，一个消费者，需要注意的是，消费者和提供者一定要依赖`rpc-sofa-boot-starter`，否则在测试过程中，可能会出现这样的错误：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221107214652.png)
或者这样的错误：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221107215048.png)

#### 编写接口
因为问题并非是出在接口上，所以接口就随便创建：
```java
public interface HelloFacadeService {

    HelloBaseResult getBaseHello(BaseRequest request);

    HelloDataResult getDataHello(BaseRequest request);
}
```
这里我创建两个接口，主要是为了对比返回结果，两个接口的入参也是一样的：
```java
@Data
public class BaseRequest {
    private String type;
}
```
再下来是返回结果，也就是出现无厘头`bug`的地方:
```java
@Data
public class HelloBaseResult {
    private Long id;
    private String name;
}
```
第二个返回结果继承了一个`vo`
```java
@Data
public class HelloDataResult extends HelloBaseResult {
    private Long id;
}
```

再接着是接口实现：
```java
@Service
@SofaService(interfaceType = HelloFacadeService.class, bindings = {@SofaServiceBinding(bindingType = "bolt")})
public class HelloFacadeServiceImpl implements HelloFacadeService {

    @Override
    public HelloBaseResult getBaseHello(BaseRequest request) {
        HelloBaseResult result = new HelloBaseResult();
        result.setId(123123123L);
        result.setName("hello");
        return result;
    }

    @Override
    public HelloDataResult getDataHello(BaseRequest request) {
        HelloDataResult result = new HelloDataResult();
        result.setId(123123123L);
        result.setName("hello");
        return result;
    }
}
```

#### 开始复现
完成接口编写之后，我们直接启动服务，然后分别调用上面两个方法，按照我们的预期，第一个接口和第二个接口的返回结果应该是一样的，然而实际的调用结果却并非如此：
- 第一个接口返回结果：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221107215934.png)
这个结果和我们预期是一致的。
- 但是第二个接口的返回结果就让人懵逼了：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221107220051.png)
好家伙，`id`竟然变成`null`，我们明明在接口里面给它设置的是`123123123`，为何和我们想象的不一样。

问题最终的解决方法是，删除掉`HelloDataResult`的`id`属性，然后返回结果就会正常，但原因是什么呢？
下面我们就来试着找到具体的原因，首先我们猜测一下，有哪些可能：
- 序列化问题，然后我分别在返回结果加上`Serializable`接口，并重写了`serialVersionUID`，实测发现并不能解决问题，而且根据我反序列化测试，也可以确定和反序列化没关系：



### 总结