### 1、[spring MVC]提示未找到No mapping found for...

- 具体错误：
 
```
七月 12, 2018 10:07:32 下午 org.springframework.web.servlet.PageNotFound noHandlerFound
警告: No mapping found for HTTP request with URI [/shopping/lgoin] in DispatcherServlet with name 'springServlet'

```

- 解决方式：
- - 如果采用个是注解的方式，在sppring配置文件添加如下代码:

```
<!-- 开启注解 -->
<mvc:annotation-driven />
```

- - 如果采用的是配置，请检查如下配置的base-package路径是否正确：

```
<!-- 自动扫描 -->  
   <context:component-scan base-package="com.sysker.shopping.controller" />
```

### 2、[spring MVC]提示找不到DAO中的方法

- 具体错误：

```
Invalid bound statement (not found): com.sysker.shopping.user.dao.UserDAO.ge tUserByUserName
```

- 解决方法：
- - 检查 Spring中sqlsessionFactoryBean中配置的mapper路径是否正确
```
<!-- spring和MyBatis完美整合，不需要mybatis的配置映射文件 -->
	<bean id="sqlSessionFactory"
		class="org.mybatis.spring.SqlSessionFactoryBean">
		<property name="dataSource" ref="dataSource" />
		<!-- 自动扫描mapping.xml文件 -->
		<property name="mapperLocations"
			value="classpath:com/sysker/shopping/**/mapper/*.xml"></property>
	</bean>
```