# spring-boot条件配置——conditionContext

### 前言

前几天，我们在剖析`spring boot`启动过程的时候，提到了一个比较核心的组件——`conditionContext`，这个组件的作用是，根据特定的条件，对`bean`进行依赖配置。这么说有点拗口，下面我们同一些具体的实例看下`conditionCOntext`到底是如何工作的。

### 条件配置

#### conditionContext初始化

在开始实例之前，我们先看下`conditionContext`的初始化过程，首先它是在创建容器的时候被初始化化的，更准确地说是在创建`AnnotatedBeanDefinitionReader`实例的时候被初始的：

![](https://gitee.com/sysker/picBed/raw/master/blog/20210922080354.png)

这里实例化的是`ConditionContextImpl`，它是条件配置接口的实现类，它的初始化过程也就是一些基本属性的赋值，包括容器（`registry`）、`bean`工厂、环境配置（`environment`）、资源加载器（`resourceLoader`）、类加载器（`classLoader`），它的`5`个核心方法分别就是这`5`个属性的获取方法，所以我们也不再过多说明。

需要注意的是，这里的`ConditionContextImpl`实现类是一个内部实现类。

由于`ConditionContextImpl`中并没有条件配置的相关方法，所以我们需要研究另一个持有`ConditionContextImpl`的组件——`ConditionEvaluator`。这个类名的意思是条件评估者，官方注释的意思是：评估条件注解的内部类。

![](https://gitee.com/sysker/picBed/raw/master/blog/20210922082549.png)

下面是这个类的核心方法`shouldSkip`：

![](https://gitee.com/sysker/picBed/raw/master/blog/20210922085941.png)

从这个类的`shouldSkip`方法中，我们可以得到几个核心的内容：

- `@Conditional`注解：条件配置最核心的注解之一，这个注解需要一个或多个继承了`Condition`接口的参数

  ![](https://gitee.com/sysker/picBed/raw/master/blog/20210922084740.png)

  这个`Condition`接口有一个`matches`方法，这个方法的返回值最终决定是否可以对当前类进行注册配置，如果同时有多个`Conditon`，则需要所有`Condition`返回`true`才能对当前类进行注册配置。

- 在创建`bean`的时候，会根据`shouldSkip`判断是否进行`bean`的初始化和注册：

  ![](https://gitee.com/sysker/picBed/raw/master/blog/20210922084524.png)

  如果`shouldSkip`返回`true`，则会直接跳过该类的初始化。

  #### 条件配置实例

  下面我们通过一个具体实例来演示下条件配置的具体用法。

  ##### 定义条件

  首先我们需要定义一个条件，也就是实现`Conditon`接口：

  ```java
  public class ResultCondition implements Condition {
      @Override
      public boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata) {
          Boolean matches = true;
          System.out.println("ResultCondition matches =" + matches);
          return matches;
      }
  }
  ```

  这里为了演示方便，我直接返回`true`。

  ##### 增加配置类

  ```java
  @Configuration
  public class ConditionConfig {
      private final Logger logger = LoggerFactory.getLogger(ConditionConfig.class);
  
      @Conditional(ResultCondition.class)
      @Bean
      public Result result() {
          logger.info("condition result");
          return new Result();
      }
  }
  ```

  

### 总结

