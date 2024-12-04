# spring-boot转换服务组件剖析

### 前言

今天要分享的内容原本是要昨天分享的，具体原因昨天也说过了，虽然昨天没分享成，但是最后还是有意外收获的，特别是关于`converter`的相关内容，瞬间就让我搞清楚了`converter`的用法和场景，所以这样来说，其实今天的内容算是对昨天内容的延申和扩展。

好了，废话不多说，下面我们直接看`converter`的相关内容。

### 转换组件

转换组件算是`spring boot`的另一块比较系统，而且也比较通用的内容，所以在剖析`converter`之前，我们有必要先看下转换服务`ConversionService`，以及它的小伙伴，当然其中也包括我们的`converter`。

#### ConversionService

这里我们说的转换组件其实指的是`ConversionService`，它是`spring`为我们提供的类型转换接口，通过调用`convert(Object, Class) `方法就可以实现一个类型到另一个类型的完美转换，而且更重要的是，它是线程安全的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210916131632.png)

与此相关的还有四个接口，一个是`GenericConverter`，一个是`Converter<S, T>`，还有一个是`ConfigurableConversionService`，最后一个是`ConverterRegistry`，我们先来说下这几个接口的关系，首先最基本的当然是`ConversionService`，它是所有转换服务类的基类接口，它为我们提供了四个基本方法：

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

但是仅有这四个基本方法还不够，所以`spring boot`引入了`ConverterRegistry`接口。

#### ConverterRegistry

`ConverterRegistry`接口的主要作用就是实现最转换器的管理，主要包括往`ConversionService`中添加转换器。因为`ConversionService`不可能只提供某几种特定的类型转换，为了能够实现转换器的扩展，同时对转换器实现管理，`spring boot`引入了`ConverterRegistry`（转换器注册接口）：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210917131258.png)

这个接口为我们提供了五个方法，分为三类：

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

在上面这几个方法中，`sourceType`表示原始类型，`targetType`表示目标类型，`converter`就是我们的转换器，这里转换器主要有两种，一种是直接继承了`Converter`的转换器，另一种就是基于`GenericConverter`实现的类型转换，所以下面我们就分享下这两个接口的相关内容。

#### converter和GenericConverter

这里的`converter`类型的转换器是最常用的转换器类型，比如我们昨天演示的`String`转日期的转换类，就属于这种：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210917085230.png)

`GenericConverter`本身也是一个接口，而且是独立的，它不同于`converter`：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210917132445.png)

它有两个核心方法：

- 获取转换类型

```java
Set<ConvertiblePair> getConvertibleTypes();
```

这里的`ConvertiblePair`是`GenericConverter`接口的一个内部类，它是保存`sourceType`和`targetType`的容器：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210917090318.png)

- 类型转换

```java
Object convert(@Nullable Object source, TypeDescriptor sourceType, TypeDescriptor targetType);
```

们昨天分享的内容可以看出来，`ConversionService`服务主要的作用就是进行数据类型转换，通常情况下，我们并不需要实现`ConversionService`接口，而是实现`GenericConverter`转换器即可，而且从昨天我们启动测试的情况来看，基本上所有的转换器都是基于`GenericConverter`实现的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210916225158.png)

`ConverterRegistry`接口对这两种接口都提供了支持，可以直接对这两种转换器进行新增和移出。

#### ConfigurableConversionService

这里的`ConfigurableConversionService`接口其实是`ConversionService`接口和`ConverterRegistry`接口的合体，它直接继承了这两个接口，具备这两个接口的能力，而且从名字也可以看出来，它应该是用来配置我们的转换服务的。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210917212239.png)

### 总结

今天主要是梳理了和`ConversionService`相关的接口以及接口的方法，算是对昨天内容的补充和延申，但是`ConversionService`的相关内容还比较多，所以我打算分两到三次分享，这样我们就可以更细致地展开，了解的也更深入。

好了，关于`converter`的相关内容我们暂时先说这么多，明天我们再结合`run`方法看下`ConversionService`以及它的小伙伴的初始化过程。
