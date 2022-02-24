# lambda表达式之函数入参

### 前言

我们都知道，从`JDK1.8`开始，`java`已经对函数式编程有了比较完善的支持，除了我们常用的`stream`之外，还有`Optional`、`Supplier`、`Function`等，今天我就抽点时间来看下`Function`的简单应用。



### Function

`function`和其他的`lambda`一样，都是`jdk1.8`引入的，但是相比于`stream`和`Optional`这两种常用的，我之前对`Funciton`的了解也很浅薄，甚至连它具体如何使用都一知半解，但是当我对它进行了一些简单的了解和实践之后，我发现`Function`确实很好用，而且应用场景也很频繁，下面我们直接开始实例：

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

当然，如果是一两个业务，我觉得都还可以接收，但如果是十几个或者几十个业务的时候，这种处理方式就显得很不友好，而且往往`success`和`failed`需要处理的业务逻辑可能不尽相同，所以我们还需要更友好更能够简化我们业务实现逻辑的方法，这时候就`Function`发光发热的时候了。

对于上面这样的需求场景，我们只需要用`Funciton`增加两个入参即可——成功回调、失败回调：

```java
/**
     * 结果回调
     * @param result
     * @param successFun
     * @param failedFun
     */
public void callBack(String result, Function<String, String> successFun, Function<String, String> failedFun) {
    if ("success".equals(result)) {
        successFun.apply(result);
    }

    if ("failed".equals(result)) {
        failedFun.apply(result);
    }
}
```



```
String result = "failed";
        new ListLamubdaTest().callBack(result, s -> {System.out.println("业务执行成功" + s);
            return s;
        }, f -> {System.out.println("业务执行失败" + f);
        return f;
        });
```

