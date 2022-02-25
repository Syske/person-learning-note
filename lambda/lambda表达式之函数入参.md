# lambda表达式之函数式接口

### 前言

我们都知道，从`JDK1.8`开始，`java`已经对函数式编程有了比较完善的支持，除了我们常用的`stream`之外，还有`Optional`、`Supplier`、`Function`等，今天我就抽点时间来看下`@FunctionalInterface`的简单应用。



### @FunctionalInterface

`@FunctionalInterface`和其他的`lambda`一样，都是`jdk1.8`引入的，但是相比于`stream`和`Optional`这两种常用的，我之前对`@FunctionalInterface`的了解也很浅薄，虽然经常在`stram()`中用到它，但对于具体如何使用它，我还真的是一知半解。下面我们先通过一个简单的实例，见识下`@FunctionalInterface`：

假设我们有一个方法，需要在方法中的某个执行结果为`success`的时候执行一段代码或者调另一个方法，在执行结果为`failed`的时候执行另一段代码，在传统实现下，我们需要这样操作：

```java
  public void dealThing(String parameter) {
        // 执行业务
        String result = "123".equals(parameter) ? "success" : "failed";
        if ("success".equals(parameter)) {
            System.out.println("业务1执行成功");
        }

        if ("failed".equals(parameter)) {
            System.out.println("业务1执行失败");
        }
    }
```

当然这样写没有任何问题，但是如果我们执行结果的逻辑还需要在另一个方法中执行，在传统操作中，我们要么需要多加一层业务判断，要么重新写个方法：

```java
// 增加逻辑处理
public void dealThing(String parameter) {
        if ("业务1".equals(parameter)) {
             // 执行业务
            String result = "123".equals(parameter) ? "success" : "failed";
            if ("success".equals(result)) {
                System.out.println("业务1执行成功");
            }

            if ("failed".equals(result)) {
                System.out.println("业务1执行失败");
            }
        } else {
             // 执行业务
            String result = "124".equals(parameter) ? "success" : "failed";
            if ("success".equals(result)) {
                System.out.println("业务2执行成功");
            }

            if ("failed".equals(result)) {
                System.out.println("业务2执行失败");
            }
        }       
    }

// 或者重写方法
public void dealThing2(String parameter) {
        // 执行业务
        String result = "124".equals(parameter) ? "success" : "failed";
        if ("success".equals(parameter)) {
            System.out.println("业务2执行成功");
        }

        if ("failed".equals(parameter)) {
            System.out.println("业务2执行失败");
        }
    }
```

当然，如果是一两个业务，我觉得都还可以接收，但如果是十几个或者几十个业务的时候，这种处理方式就显得很不友好，而且往往`success`和`failed`需要处理的业务逻辑可能不尽相同，所以我们还需要更友好更能够简化我们业务实现逻辑的方法，这时候就到了函数式接口发光发热的时候了。

对于上面这样的需求场景，我们只需要增加两个`Consumer`入参即可——成功回调、失败回调：

```java
/**
     * 结果回调
     * @param result
     * @param successFun
     * @param failedFun
     */
public void callBack(String result, Consumer<String> successFun, Consumer<String> failedFun) {
    if ("success".equals(result)) {
        successFun.accept(result);
    }

    if ("failed".equals(result)) {
        failedFun.accept(result);
    }
}
```

这里的`Consumer`就是函数式接口的一种，使用也很简单，就是在调用具体方法的时候，要提供接口的具体实现，也就是我们上面的`successFun`、`failedFun`入参，具体调用实例如下：

```java
String result = "failed";
new FunctionalInterfaceTest().callBack(result, s -> {System.out.println("业务执行成功" + s);
                                            }, 
                               f -> {System.out.println("业务执行失败" + f);
                                                    });
```

运行结果如下：

![](https://gitee.com/sysker/picBed/raw/master/blog/20220225082723.png)

下面我们来简单看下`Consumer`接口：

![](https://gitee.com/sysker/picBed/raw/master/blog/20220225083029.png)

和我们通常定义的接口有所不同的是，函数式接口有一个`@FunctionalInterface`注解，其中的`accept`方法就是我们在调用方法时需要实现的方法。除了`Consumer`函数式接口之外，`java`还为我们提供了其他很多有用的函数式接口，比如`Function`，与`Consumer`不同的是，`Function`提供的函数式接口是可以有返回值的：

![](https://gitee.com/sysker/picBed/raw/master/blog/20220225084212.png)

关于官方提供的函数式接口我们就先看这么多，下面我们一起来看下如何定制自己的函数式接口，其实也很简单：

```java
@FunctionalInterface
public interface MyFunctionInterface<T> {
    void syske(T t);
}
```

首先是定义接口和接口方法，然后加上`@FunctionalInterface`，这样一个函数式接口就定义好了，使用和我们上面演示的用法没有任何区别：

```java
new FunctionalInterfaceTest().functionTest("syske", "hello", parameter -> System.out.println( "syske, " + parameter));
```

当然除了上面我们演示的这种方式之外，我们还可以通过下面这种方式来使用函数式接口：

```java
public void syskeFun(String parameter) {
        System.out.println( "syske, " + parameter);
    }
// 当前类的非静态方法调用
new FunctionalInterfaceTest().functionTest("syske", "hello", this::syskeFun);
// 静态方法调用，在这种情况下，需要把syskeFun定义为静态方法
new FunctionalInterfaceTest().functionTest("syske", "hello", FunctionalInterfaceTest::syskeFun);
```

需要注意的是，函数式接口中只能定义一个未实现的接口，否则会报编译错误：

![](https://gitee.com/sysker/picBed/raw/master/blog/20220225084944.png)

### 结语

相比于传统的方法调用，函数式接口的入参更灵活也更方便，



`FunctionalInterface`确实很好用，也确实很方便。