# spring-boot启动过程中的实例化方式

### 前言

最近一直在肝`spring boot`的源码



### 实例化方式

#### instant



#### new



#### supplier

![](https://gitee.com/sysker/picBed/raw/master/images/20210914133038.png)

比如下面这个注册`BeanDefinitionRegistry`的方法就是通过这种方式将`supplier`注入`beanDefinition`中的

```java
private void register(BeanDefinitionRegistry registry) {
            BeanDefinition definition = BeanDefinitionBuilder.genericBeanDefinition(SharedMetadataReaderFactoryContextInitializer.SharedMetadataReaderFactoryBean.class, SharedMetadataReaderFactoryContextInitializer.SharedMetadataReaderFactoryBean::new).getBeanDefinition();
            registry.registerBeanDefinition("org.springframework.boot.autoconfigure.internalCachingMetadataReaderFactory", definition);
        }
```

