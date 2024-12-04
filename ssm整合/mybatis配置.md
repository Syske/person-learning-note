### 1、为mybatis设置别名：

```

<!-- spring和MyBatis完美整合，不需要mybatis的配置映射文件 -->
	<bean id="sqlSessionFactory"
		class="org.mybatis.spring.SqlSessionFactoryBean">
		<property name="dataSource" ref="dataSource" />
		<!-- 自动扫描mapping.xml文件 -->
		<property name="mapperLocations"
			value="classpath:com/sysker/shopping/**/mapper/*.xml"></property>
			<!-- 设置别名 -->
		<property name="typeAliasesPackage" value="com.sysker.shopping.user.entity"></property>
	</bean>
```