### 基本配置

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns:context="http://www.springframework.org/schema/context"
	xmlns:aop="http://www.springframework.org/schema/aop"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
	http://www.springframework.org/schema/beans/spring-beans-4.0.xsd
	http://www.springframework.org/schema/context
	http://www.springframework.org/schema/context/spring-context-4.0.xsd
	http://www.springframework.org/schema/aop
	http://www.springframework.org/schema/aop/spring-aop-4.0.xsd">
	<!-- 启动@AspectJ支持 -->
	<!-- <bean class="org.springframework.aop.aspectj.annotation.AnnotationAwareAspectJAutoProxyCreator" 
		/> -->
	<aop:config>

		<aop:pointcut
			expression="execution(* service.impl.*.*(..))" id="testbefore" />

		<aop:aspect id="afterAdviceAspect" ref="afeterAdviceBean">
			<aop:before method="beforeMe" pointcut-ref="testbefore" />
		</aop:aspect>
	</aop:config>
	<bean id="afeterAdviceBean" class="lee.AfterAdviceTest" />
	<bean id="hello" class="service.impl.HelloImpl" />
	<bean id="world" class="service.impl.WorldImpl" />
</beans>

```

 配置增强处理：

 ```
 <aop:config>
		<aop:aspect id="afterAdviceAspect" ref="afeterAdviceBean">
			<aop:before method="beforeMe" pointcut="execution(* service.impl.*.*(..))" />
		</aop:aspect>
	</aop:config>
 ```

 配置切入点，并在增强处理中使用该切点：

 ```
 <aop:config>

		<aop:pointcut
			expression="execution(* service.impl.*.*(..))" id="testbefore" />

		<aop:aspect id="afterAdviceAspect" ref="afeterAdviceBean">
			<aop:before method="beforeMe" pointcut-ref="testbefore" />
		</aop:aspect>
	</aop:config>
 ```
