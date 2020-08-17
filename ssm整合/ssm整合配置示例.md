# 1、web.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://java.sun.com/xml/ns/javaee" xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_3_0.xsd" id="WebApp_ID" version="3.0">
 <display-name>transactionDome</display-name>
 <welcome-file-list>
   <welcome-file>index.html</welcome-file>
   <welcome-file>index.htm</welcome-file>
   <welcome-file>index.jsp</welcome-file>
   <welcome-file>default.html</welcome-file>
   <welcome-file>default.htm</welcome-file>
   <welcome-file>default.jsp</welcome-file>
 </welcome-file-list>
 <listener>
       <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
   </listener>

   <context-param>
       <param-name>contextConfigLocation</param-name>
       <param-value>classpath:spring-mybatis.xml</param-value>
   </context-param>

   <servlet>
       <servlet-name>springServlet</servlet-name>
       <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
       <init-param>
           <param-name>contextConfigLocation</param-name>
           <param-value></param-value>
       </init-param>
       <load-on-startup>1</load-on-startup>
   </servlet>

   <servlet-mapping>
       <servlet-name>springServlet</servlet-name>
       <url-pattern>/</url-pattern>
   </servlet-mapping>
</web-app>
```

# 2、spring-mybatis.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns:p="http://www.springframework.org/schema/p"
	xmlns:context="http://www.springframework.org/schema/context"
	xmlns:mvc="http://www.springframework.org/schema/mvc"
	xsi:schemaLocation="http://www.springframework.org/schema/beans    
                       http://www.springframework.org/schema/beans/spring-beans.xsd    
                       http://www.springframework.org/schema/context    
                       http://www.springframework.org/schema/context/spring-context.xsd    
                       http://www.springframework.org/schema/mvc    
                       http://www.springframework.org/schema/mvc/spring-mvc.xsd">
	<!-- 自动扫描 -->
	<context:component-scan
		base-package="com.sysker.shopping" />
	<!-- 开启注解 -->
	<mvc:annotation-driven />
	<!-- 配置静态资源 -->
	<mvc:resources mapping="/resources/**"
		location="/WEB-INF/resources/" />

	<mvc:default-servlet-handler />

	<!-- 配置simpledateformat -->
	<bean id="simpleDateFormat" class="java.text.SimpleDateFormat">
		<constructor-arg value="yyyy-MM-dd HH:mm:ss"></constructor-arg>
	</bean>
	<!-- 引入配置文件 -->
	<bean id="propertyConfigurer"
		class="org.springframework.beans.factory.config.PropertyPlaceholderConfigurer">
		<property name="location" value="classpath:jdbc.properties" />
	</bean>
	<!-- 连接池配置 -->
	<bean id="dataSource"
		class="org.apache.commons.dbcp.BasicDataSource" destroy-method="close">
		<property name="driverClassName" value="${driver}" />
		<property name="url" value="${url}" />
		<property name="username" value="${username}" />
		<property name="password" value="${password}" />
		<!-- 初始化连接大小 -->
		<property name="initialSize" value="${initialSize}"></property>
		<!-- 连接池最大数量 -->
		<property name="maxActive" value="${maxActive}"></property>
		<!-- 连接池最大空闲 -->
		<property name="maxIdle" value="${maxIdle}"></property>
		<!-- 连接池最小空闲 -->
		<property name="minIdle" value="${minIdle}"></property>
		<!-- 获取连接最大等待时间 -->
		<property name="maxWait" value="${maxWait}"></property>
	</bean>

	<!-- spring和MyBatis完美整合，不需要mybatis的配置映射文件 -->
	<bean id="sqlSessionFactory"
		class="org.mybatis.spring.SqlSessionFactoryBean">
		<property name="dataSource" ref="dataSource" />
		<!-- 引入mybatis配置文件 -->
		<property name="configLocation"
			value="classpath:mybatis-config.xml"></property>
				<!-- 引入分页插件 -->
		<property name="plugins">
			<array>
				<bean class="com.github.pagehelper.PageHelper">
				</bean>
			</array>
		</property>

		<!-- 自动扫描mapping.xml文件 -->
		<property name="mapperLocations"
			value="classpath:com/sysker/shopping/**/mapper/*.xml"></property>
		<property name="typeAliasesPackage"
			value="com.sysker.shopping.product.entity,
												   com.sysker.shopping.user.entity,
												   com.sysker.shopping.muser.entity,
												   com.sysker.shopping.category.dto.entity,
												   com.sysker.shopping.category.entity"></property>

	</bean>

	<!-- DAO接口所在包名，Spring会自动查找其下的类 -->
	<bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
		<property name="basePackage" value="com.sysker.**.dao" />
		<property name="sqlSessionFactoryBeanName"
			value="sqlSessionFactory"></property>
	</bean>

	<!-- (事务管理)transaction manager, use JtaTransactionManager for global tx -->
	<bean id="transactionManager"
		class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
		<property name="dataSource" ref="dataSource" />
	</bean>

	<!-- 配置事务管理模板：Spring为了简化事务管理的代码而提供的类 -->
	<bean id="transactionTemplate"
		class="org.springframework.transaction.support.TransactionTemplate">
		<property name="transactionManager" ref="transactionManager"></property>
	</bean>
	<!-- configure the InternalResourceViewResolver -->
	<bean
		class="org.springframework.web.servlet.view.InternalResourceViewResolver"
		id="internalResourceViewResolver">
		<!-- 前缀 -->
		<property name="prefix" value="/WEB-INF/view/" />
		<!-- 后缀 -->
		<property name="suffix" value=".jsp" />
	</bean>

</beans>  
```

# 3、mybatis-config.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
	<settings>
		<!-- 打印查询语句 -->
		<setting name="logImpl" value="STDOUT_LOGGING" />
	</settings>
	
	<!-- <plugins>
		com.github.pagehelper为PageHelper类所在包名
		<plugin interceptor="com.github.pagehelper.PageInterceptor">
			使用下面的方式配置参数，后面会有所有的参数介绍
			<property name=" reasonable" value="true" />
		</plugin>
	</plugins> -->
</configuration>
```