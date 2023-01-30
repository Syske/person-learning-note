# spring-boot源码分析之BeanFactory · 壹

### 前言

今天原本是打算分析`beanFactory`的，但由于昨天我们有一部分内容还没有分享完，所以今天就先开个倒车，把做昨天的内容先将清楚，所以今天的内容主要就是对昨天分享内容的的补充。

当然，昨天我们分享的内容`beanDefinitionNames`也算是`BeanFactory`的核心属性，所以也不能说完全没有关系：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210903201214.png)

而且从源码中我们可以看出来，`beanDefinitionNames`、`beanDefinitionMap`这些属性的初始化大小，这也算是在学习`beanFactory`的相关知识吧。

### BeanFactory

#### `beanDefinitionNames`内容补充

正式开始之前，我们先把昨天遗留的问题解决了。昨天，我们分享了一张`beanDefinitionNames`初始化的时序图，但是由于有一些内容没有梳理清楚，所以这里先做个补充。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/%E5%AE%B9%E5%99%A8%E5%88%B7%E6%96%B0%E5%90%AF%E5%8A%A8%E6%97%B6%E5%BA%8F%E5%9B%BE.svg)

##### 调用过程各方法作用

`SpringApplication`这里就不做过多说明了，我们在前面最开始的时候就已经分析过这个类的`run`方法，当时也已经介绍过这个类的这些方法，他们的主要作用就是为了初始化容器，在`SpringApplication`的最后一个`refresh`方法中，最后会调用`AbstractApplicationContext`自身的`refresh`方法，这里的`AbstractApplicationContext`是`ApplicationContext`的抽象实现，它实现了`ConfigurableApplicationContext`接口（`ConfigurableApplicationContext`继承了`ApplicationContext`），我们的`AnnotationConfigReactiveWebServerApplicationContext`（默认容器）就是继承自它，不过并不是直接继承，它的父类继承了`AbstractApplicationContext`，关于容器这块的继承关系，我们改天抽个时间，专门分析下。

大部分继承了`AbstractApplicationContext`的容器都没有重写`refresh`方法，就算重写了这个方法，其内部也是调用了父类的`refresh`方法：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210903084223.png)

我们看下`refresh`的实现源码：

```java
	public void refresh() throws BeansException, IllegalStateException {
		synchronized (this.startupShutdownMonitor) {
			// Prepare this context for refreshing.
			prepareRefresh();

			// Tell the subclass to refresh the internal bean factory.
			ConfigurableListableBeanFactory beanFactory = obtainFreshBeanFactory();

			// Prepare the bean factory for use in this context.
			prepareBeanFactory(beanFactory);

			try {
				// Allows post-processing of the bean factory in context subclasses.
				postProcessBeanFactory(beanFactory);

				// Invoke factory processors registered as beans in the context.
				invokeBeanFactoryPostProcessors(beanFactory);

				// Register bean processors that intercept bean creation.
				registerBeanPostProcessors(beanFactory);

				// Initialize message source for this context.
				initMessageSource();

				// Initialize event multicaster for this context.
				initApplicationEventMulticaster();

				// Initialize other special beans in specific context subclasses.
				onRefresh();

				// Check for listener beans and register them.
				registerListeners();

				// Instantiate all remaining (non-lazy-init) singletons.
				finishBeanFactoryInitialization(beanFactory);

				// Last step: publish corresponding event.
				finishRefresh();
			}

			catch (BeansException ex) {
				if (logger.isWarnEnabled()) {
					logger.warn("Exception encountered during context initialization - " +
							"cancelling refresh attempt: " + ex);
				}

				// Destroy already created singletons to avoid dangling resources.
				destroyBeans();

				// Reset 'active' flag.
				cancelRefresh(ex);

				// Propagate exception to caller.
				throw ex;
			}

			finally {
				// Reset common introspection caches in Spring's core, since we
				// might not ever need metadata for singleton beans anymore...
				resetCommonCaches();
			}
		}
	}
```

`refresh`方法内部，调用了很多其他方法，其中`prepareRefresh`的作用是为我们下面的刷新操作做准备，其内部主要是对配置的一些初始化操作：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210903084709.png)

`obtainFreshBeanFactory`方法的作用是刷新`beanFactory`，主要是对`beanFactory`进行一些初始化操作，如果`beanFactory`已经存在，会将已有的`beanFactory`销毁，然后重新创建，最后将`beanFactory`返回：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210903085118.png)

`prepareBeanFactory`方法的作用是对`BeanFactory`进行一些赋值和设置，为容器初始化操作做准备：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210903085640.png)

`postProcessBeanFactory`方法就是我们昨天提到的会进行包扫描的那个方法，但由于`basePackages`和`annotatedClasses`都是空，所以其中的`scan`方法并不会被执行。这个方法实际的作用是，后置处理`BeanFactory`

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210903125146.png)

`invokeBeanFactoryPostProcessors`方法的作用是，实例化并调用所有注册的`BeanFactory`的后置处理器。我们昨天说的`beanDefinitionNames`和`beanDefinitionMap`就是通过这个方法最终完成初始化的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210903130342.png)

`registerBeanPostProcessors`方法和它名字一样，它的作用就是注册`bean`的后置处理器：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210903131858.png)

`initMessageSource`方法是进行消息源初始化的，主要是对`web`应用消息国际化提供支持的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210903132410.png)

`initApplicationEventMulticaster`，这个方法是初始化`spring boot`应用时间广播的，如果不指定的话，默认情况下为我们指定的是`SimpleApplicationEventMulticaster`：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210903132723.png)

`onRefresh`，这个方法是提供给子类初始化其他特殊`bean`对象的，默认实现为空，子类可根据需要重写：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210903132942.png)

`registerListeners`方法是用来注册事件监听器的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210903133324.png)

`finishBeanFactoryInitialization`，完成`beanFactory`初始化，同时在方法内部会实例化剩余的单例类（不包括懒加载部分）：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210903134535.png)

`finishRefresh`，完成刷新，主要进行一些清理、刷新、事件推送等操作：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210903134722.png)

### 总结

经过今天的补充之后，我相信各位小伙伴一定也对`spring boot`的启动和初始化过程有了更深刻的认识，因为我就是这样的感受。相比于昨天分享完内容的感受，今天我感觉整体来说要更好。一方面感觉`spring boot`启动和初始化的流程更清晰了，而且由于最近这几天一直在看`spring boot`的源码，看的多了感觉就没有那么难了，毕竟书读百遍其意自现，代码也是大同小异；另一方面在梳理分析的过程中，让我也能够清晰地看到下一步要分享的内容，明确后面地前进方向，这也算是意外的收获吧。