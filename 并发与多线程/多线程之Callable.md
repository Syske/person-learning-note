# 多线程之Callable

## 前言

相比于`Runnable`，`Callable`在日常开发中用的比较少，所以对于这块的内容也理解的不够透彻，今天我打算抽点时间熟悉下`callable`的相关知识点。


## Callable

### 基本概念

我们讲到线程创建的时候，都知道多线程的创建方式有三种，其中一种就是`Callable`，但是想必很多小伙伴和我一样，日常开发中也很少会想起他，他的用法和`Runnable`类似：

为了编码方便，以下演示代码均采用`lambda`方式，代码也会看起来更简洁

```java
Callable<String> callable1 = () -> {
    System.out.println("hello callable before ");
    return "hello callable";
};
```

简单解释下，`Callable`和`Runnable`其中的一个区别是前者的`run`方法有返回值，而后者的没有：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202309171001877.png)

`Callable`的运行上没有`Runnable`那么灵活，必须通过线程池：

```java
ExecutorService executorService = Executors.newSingleThreadExecutor();
Future<String> submit = executorService.submit(callable1);
// 获取线程返回值
String out = submit.get();
System.out.println(out);
```

列表方式运行：

```java
List<Callable<String>> callableList = Lists.newArrayList();
for (int i = 0; i < 10000; i++) {
    int finalI = i;
    Callable<String> callable2 = () -> {
        return "hello callable" + finalI;
    };
    callableList.add(callable2);
}
long start = System.currentTimeMillis();
List<Future<String>> futures = executorService.invokeAll(callableList);
System.out.printf("use：%s%n", (System.currentTimeMillis() -start));
for (Future<String> future : futures) {
    System.out.println(future.get());
}
```


### 应用场景

`Callable`的应用场景也是特别广泛的，特别是我们日常业务开发中，如果接口性能受限，而业务实现中又可以横向切片时，我们就可以直接使用`Callable`以提升我们的接口性能，下面给出一个简单示例：

需求：查询一批人员信息，包括人员基本信息，人员扩展信息，人员登录信息

通常情况下我们是这样实现的：

```java
List<Long> userIds = request.getUerIds();
// 查询人员基本信息
List<UserBaseInfo> userBaseInfoList = baseMapper.listUserInfo(userIds)；
// 查询扩展信息
List<UserExtendInfo> userBaseInfoList = extendMapper.listUserInfo(userIds)；
// 查询人员登录信息
List<UserLoginInfo> userLoginInfoList = loginMapper.listUserLogin(userIds);
// 组装返回结果
List<UserResult> userResultList = buildUserResultList(userBaseInfoList, userBaseInfoList, userLoginInfoList);
```
在上面这种实现方式下，如果我们的数据量比较大，可能会导致接口超时（如果是`rpc`通信），为了优化这种超时的实现方式，我们可以通过`Callable`来提升我们的接口性能：

```java
// 线程池
ExecutorService executorService = Executors.newSingleThreadExecutor();
        

List<Long> userIds = request.getUerIds();
// 查询人员基本信息
Callable<UserBaseInfo> userBaseInfoCallable = () -> {
    return baseMapper.listUserInfo(userIds);
};
// 查询扩展信息
Callable<UserExtendInfo> userExtendInfoCallable = () -> {
    return extendMapper.listUserInfo(userIds);
};
// 查询人员登录信息
Callable<UserLoginInfo> userLoginfoCallable = () -> {
    return loginMapper.listUserLogin(userIds);
};
// 异步查询，获取结果
List<UserBaseInfo> userBaseInfoList = executorService.submit(userBaseInfoCallable);
List<UserExtendInfo> userBaseInfoList = executorService.submit(userExtendInfoCallable);
List<UserLoginInfo> userLoginInfoList = executorService.submit(userLoginfoCallable);
// 组装返回结果
List<UserResult> userResultList = buildUserResultList(userBaseInfoList, userBaseInfoList, userLoginInfoList);
```

## 总结

