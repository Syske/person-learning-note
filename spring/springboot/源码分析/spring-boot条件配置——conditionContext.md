# spring-boot条件配置——conditionContext

### 前言

前几天，我们在剖析`spring boot`启动过程的时候，提到了一个比较核心的组件——`conditionContext`，这个组件的作用是，根据特定的条件，对`bean`进行依赖配置。这么说有点拗口，下面我们同一些具体的实例看下`conditionCOntext`到底是如何工作的。

### 条件配置

#### conditionContext初始化

在开始实例之前，我们先看下`conditionContext`的初始化过程，首先它是在创建容器的时候被初始化化的，更准确地说是在创建`AnnotatedBeanDefinitionReader`实例的时候被初始的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210922080354.png)

这里实例化的是`ConditionContextImpl`，它是条件配置接口的实现类，它的初始化过程也就是一些基本属性的赋值，包括容器（`registry`）、`bean`工厂、环境配置（`environment`）、资源加载器（`resourceLoader`）、类加载器（`classLoader`），它的`5`个核心方法分别就是这`5`个属性的获取方法，所以我们也不再过多说明。

需要注意的是，这里的`ConditionContextImpl`实现类是一个内部实现类。

由于`ConditionContextImpl`中并没有条件配置的相关方法，所以我们需要研究另一个持有`ConditionContextImpl`的组件——`ConditionEvaluator`。这个类名的意思是条件评估者，官方注释的意思是：评估条件注解的内部类。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210922082549.png)

下面是这个类的核心方法`shouldSkip`：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210922085941.png)

从这个类的`shouldSkip`方法中，我们可以得到几个核心的内容：

- `@Conditional`注解：条件配置最核心的注解之一，这个注解需要一个或多个继承了`Condition`接口的参数

  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210922084740.png)

  这个`Condition`接口有一个`matches`方法，这个方法的返回值最终决定是否可以对当前类进行注册配置，如果同时有多个`Conditon`，则需要所有`Condition`返回`true`才能对当前类进行注册配置。

- 在创建`bean`的时候，会根据`shouldSkip`判断是否进行`bean`的初始化和注册：

  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20210922084524.png)

  如果`shouldSkip`返回`true`，则会直接跳过该类的初始化，`shouldSkip`要返回`true`，则`condition`的返回值必须为`false`:

  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210922131244.png)

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
  
  在配置类中，我加了一个`Result`的实例化配置，同时在它的配置上增加了` @Conditional(ResultCondition.class)`。
  
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
  
  加了这个注解之后，想要`Result`实例化成功，就要求`ResultCondition`的`matches`方法必须为`true`，也就是`shouldSkip`返回`false`。
  
  ##### 测试
  
  下面我们简单测试下，因为我已经在相关代码中加了打印输出，所以我们直接启动看效果即可，当`matches`方法返回`true`时，我们可以看到`Result`的实例化配置被执行了：
  
  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210922132004.png)
  
  然后我们把`matches`方法返回值改成`false`再看下，这时候我们会发现`Result`的实例化配置并没有被执行：
  
  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210922132402.png)
  
  综上，我们可以看出来，`conditionContext`其实就是通过`Condition`接口来实现有条件的配置，这样的好处是，可以动态地调整优化配置，即灵活又方便，更重要的是，这种方式还可以有效降低组件的耦合性，便于扩展，而且可以提高系统启动效率（`condition`可以直接过滤不需要实例化的组件）。
  
  举个栗子，比如你现在要开发一个集成组件，这个组件既可以发消息，又可以做`redis`的工具包，还可以做`zk`的客户端，这时候如果别人要用你这个集成组件中的某一个功能，比如发消息的功能，在没有条件配置的情况下，他不仅需要引入消息组件的依赖，还需要引入`zk`和`redis`的组件依赖，但是对他而言，后两种组件是非必要的，引入之后只会增加不必要的依赖和配置，但是没有这些依赖和配置又会报错，所以极其不灵活。
  
  但是如果你的组件才有的是条件配置的话，就不会存在这个问题，你可以通过条件配置的方式，来启用相关组件：他引入消息组件依赖，你启用消息组件配置；他启用`zk`依赖，你启用`zk`组件配置；他启用`redis`组件依赖，你启用`redis`组件配置。当不存在相关组件依赖时，相关组件配置并不会起作用。
  
  #### 知识扩展
  
  除了我们这里说的`@Conditional`注解外， `spring boot`还为我们提供了 `@ConditionalOnClass`注解，这个注解的作用是当指定的类的`class`存在于`classpath`中时，才会执行该配置，和我们`Conditional`注解差不多，他只是已经默认实现了`matches`方法，我们直接可以使用。
  
  类似的注解还有很多，有兴趣的小伙伴可以自己去看下：
  
  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210922140257.png)
  
  关于`@ConditionalOnClass`注解的用法，可以参考我们前面分享过的`spring-boot-starter`自定义相关内容：
  
  

### 总结

好了，关于`conditionContext`的相关内容我们就先讲到这里，感兴趣的小伙伴自己可以去看下我们今天提到的其他注解。

下面做一个简单小结，今天我们围绕着`conditionContext`的初始化过程，探讨了`spring boot`条件化配置的基本原理，然后我们还通过一个简单实例演示了条件配置的具体用法，最后我们还对`@Conditional`注解的基础上做了一点点引申和扩展，总体来说，条件配置的用法还是比较简单的，但是如果真正用起来，是可以有效降低你的系统的耦合性，极大提高系统扩展性。
