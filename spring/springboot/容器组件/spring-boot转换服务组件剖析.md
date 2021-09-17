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



我们先说下这三个接口的关系，首先最基本的当然是`ConversionService`，它是所有转换类的基类接口，它为我们提供了四个基本方法：



但是仅有这四个基本方法还不够，因为我们还需要往`ConversionService`中添加转换器，因为`ConversionService`不可能只提供某几种特定的类型转换，为了能够实现转换器的扩展，同时对转换器实现管理，`spring boot`引入了`ConverterRegistry`（转换器注册接口），这个接口为我们提供了五个方法，分为三类：

- 添加转换器

```java
void addConverter(Converter<?, ?> converter);
// 也是一个新增接口，入参不一样
<S, T> void addConverter(Class<S> sourceType, Class<T> targetType, Converter<? super S, ? extends T> converter);
// 第三种转换器新增
void addConverter(GenericConverter converter);
```

- 添加转换器工厂

```java
void addConverterFactory(ConverterFactory<?, ?> factory);
```

- 移除转换器

```java
void removeConvertible(Class<?> sourceType, Class<?> targetType);
```

在上面这几个方法中，`sourceType`表示原始类型，`targetType`表示目标类型，`converter`就是我们的转换器，这里转换器主要有两种，一种是直接继承了`Converter`的转换器，就比如我们昨天演示的`String`转日期的转换类：

![](https://gitee.com/sysker/picBed/raw/master/blog/20210917085230.png)

另一种就是基于`GenericConverter`实现的类型转换，它本身也是一个接口，而且是独立的，它有两个核心方法：

- 获取转换类型

```java
Set<ConvertiblePair> getConvertibleTypes();
```

这里的`ConvertiblePair`是`GenericConverter`接口的一个内部类，它是保存`sourceType`和`targetType`的容器：

![](https://gitee.com/sysker/picBed/raw/master/blog/20210917090318.png)

- 类型转换

```java
Object convert(@Nullable Object source, TypeDescriptor sourceType, TypeDescriptor targetType);
```

们昨天分享的内容可以看出来，`ConversionService`服务主要的作用就是进行数据类型转换，通常情况下，我们并不需要实现`ConversionService`接口，而是实现`GenericConverter`转换器即可，而且从昨天我们启动测试的情况来看，基本上所有的转换器都是基于`GenericConverter`实现的：

![](https://gitee.com/sysker/picBed/raw/master/20210916225158.png)

### 总结

