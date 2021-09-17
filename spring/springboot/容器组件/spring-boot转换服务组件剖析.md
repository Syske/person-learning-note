# spring-boot转换服务组件剖析

### 前言



### 转换组件

这里我们说的转换组件其实指的是`ConversionService`，它是`spring`为我们提供的类型转换接口，通过调用`convert(Object, Class) `方法就可以实现一个类型到另一个类型的完美转换，而且更重要的是，它是线程安全的：

![](https://gitee.com/sysker/picBed/raw/master/images/20210916131632.png)

这个接口为我们提供了四个核心方法：

- 判断是否可以进行类型转换

```java
boolean canConvert(@Nullable Class<?> sourceType, Class<?> targetType);
```

- 判断是否可以进行类型转换。和第一个方法类似，入参有所不同：

```java
boolean canConvert(@Nullable TypeDescriptor sourceType, TypeDescriptor targetType);
```

- 进行类型转换，返回目标类型的实例

```java
<T> T convert(@Nullable Object source, Class<T> targetType);
```

- 进行类型转换，和上一个方法作用相同，只是这里返回的是`Object`，而且入参也有所不同

```java
Object convert(@Nullable Object source, @Nullable TypeDescriptor sourceType, TypeDescriptor targetType);
```

与此相关的还有两个接口，一个是`GenericConverter`，另一个是`Converter<S, T>`







### 总结

