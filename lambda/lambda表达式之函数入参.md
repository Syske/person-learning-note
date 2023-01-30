# lambda表达式之函数式接口

### 前言

我们都知道，从`JDK1.8`开始，`java`已经对函数式编程有了比较完善的支持，除了我们常用的`stream`之外，还有`Optional`、`Supplier`、`Function`等，其中`Function`就是函数式接口的一种方式，函数式编程极大提升了我们的编程效率和代码逻辑简洁度，今天我们就抽点时间来看下`@FunctionalInterface`（函数式接口）的简单应用。



### @FunctionalInterface

虽然`@FunctionalInterface`和其他的`lambda`一样，都是`jdk1.8`引入的，但相比于`stream`和`Optional`这两种常用的新特性，我对`@FunctionalInterface`的了解就显得很浅薄了。

哪怕是经常在`stram()`中用到它，但对于具体如何使用它，如何更好的应用它，我还真的是一知半解。

下面我们先通过一个简单的实例，来见识下`@FunctionalInterface`的魅力：

#### 一个简单场景

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

当然这样写没有任何问题，但是如果我们执行结果的逻辑还需要在其他方法中执行，而且其中成功和失败的业务处理还不尽相同，这样在传统操作中，我们要么需要多加一层业务判断，要么重新写个方法，不过这两种方式都增加了冗余代码：

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

当然，如果是一两个业务，我觉得都还可以接受，但如果是十几个或者几十个业务的时候，这种处理方式就显得很不友好，而且往往`success`和`failed`需要处理的业务逻辑可能不尽相同，所以我们还需要更友好更能够简化我们业务实现逻辑的方法，这时候就到了函数式接口发光发热的时候了：

#### 函数式接口应用

如果采用函数式接口的方式，对于上面这样的需求场景，我们只需要增加两个`Consumer`入参即可——成功回调、失败回调：

```java
/**
     * 结果回调
     * @param result
     * @param successFun
     * @param failedFun
     */
public void dealThing(String parameter, Consumer<String> successFun, Consumer<String> failedFun) {
    // 执行业务
    String result = "124".equals(parameter) ? "success" : "failed";
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
String parameter = "123";
new FunctionalInterfaceTest().dealThing(parameter, s -> {System.out.println("业务执行成功" + s);
                                            }, 
                               f -> {System.out.println("业务执行失败" + f);
                                                    });
```

运行结果如下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220225082723.png)

#### Consumer函数式接口

下面我们来简单看下`Consumer`接口的基本结构：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220225083029.png)

和我们通常定义的接口有所不同的是，函数式接口有一个`@FunctionalInterface`注解，其中的`accept`方法就是我们在调用方法时需要实现的方法。除了`Consumer`函数式接口之外，`java`还为我们提供了其他很多有用的函数式接口，比如`Function`，与`Consumer`不同的是，`Function`提供的函数式接口是可以有返回值的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220225084212.png)

#### 定义自己的函数式接口

关于官方提供的函数式接口我们就先看这么多，下面我们一起来看下如何定制自己的函数式接口，其实也很简单：

首先是定义接口和接口方法，然后加上`@FunctionalInterface`，这样一个函数式接口就定义好了：

```java
@FunctionalInterface
public interface MyFunctionInterface<T> {
    void syske(T t);
}
```

使用和我们上面演示的用法没有任何区别：

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

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220225084944.png)

#### 多参数函数式接口

上面我们演示的都是单参数的函数式接口，其实官方也提供了很多其他的函数式接口，比如带返回值的函数式接口`Function`、多参数的接口`BiFunction`

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220228084711.png)

这里的`BiFunction`有两个入参和一个返回值，如果两个参数依然满足不了你的需要，你还可以自己定义多参数接口，这里我定义的函数式接口有`5`个参数：

```java
@FunctionalInterface
public interface MyFunctionInterface2<T, R, U, X, Y> {
    void syske(T t, R r, U u, X x, Y y);

}
```

调用方式也是大同小异：

```java
public void setMyFunctionInterface2(String t, String r, String u, String x, String y, MyFunctionInterface2<String, String, String, String, String> interface2) {
        interface2.syske(t, r, u, x, y);
    }
    
new FunctionalInterfaceTest().setMyFunctionInterface2("parameter1", "parameter2", "parameter3", "parameter4", "parameter5", (t, r, u, x, y) -> System.out.printf("%s.%s.%s.%s.%s", t, r, u, x,y));
```



### 结语

相比于传统的方法调用，函数式接口的入参更灵活也更方便，让我们可以在不同的业务中使用不同的逻辑实现方式，可以极大简化代码中的`if-else`逻辑，甚至在某些场景下，还可以代替策略模式。好了，关于函数式接口的简单介绍和应用我们就先分享这么多，感兴趣的小伙伴可以亲自动手试试，当然最好的实践就是在实践应用中使用它，并让它为我们的开发工作带来便利。