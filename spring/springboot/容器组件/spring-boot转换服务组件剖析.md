# spring-boot转换服务组件剖析

### 前言



### 转换组件

这里我们说的转换组件其实指的是`ConversionService`，它是`spring`为我们提供的类型转换接口，通过调用`convert(Object, Class) `方法就可以实现一个类型到另一个类型的完美转换，而且更重要的是，它是线程安全的



与此相关的还有两个接口，一个是`GenericConverter`

另一个是`Converter<S, T>`







### 总结

