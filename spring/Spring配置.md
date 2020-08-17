### 1、Spring是什么

- 开元框架
- 轻量级控制反转（IoC）和面向切面（AOP）的容器框架
- - 大小与开销都是轻量的
- - 通过控制反转（IoC）的技术达到松耦合的目的
- - 提供了面向切面的丰富支持，允许通过分离应用的业务逻辑与系统级服务进行内聚性的开发
- - 包含并管理应用对象的配置和生命周期
- - 支持将简单的组件配置、组合成为复杂的应用

### 2、Spring配置

> 核心配置文件

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd">

	<bean id="user" class="com.javasm.user.entity.User" scope="prototype">
		<constructor-arg ref="role" />
		<property name="name" value="李四" ></property>
		<!-- <property name="name" value="张三"></property> <property name="role" 
			ref="role"></property> -->
	</bean>

	<bean id="role" class="com.javasm.role.entity.Role">
		<property name="name" value="项目经理"></property>
	</bean>

	<!-- more bean definitions go here -->

</beans>

```

### 3、创建JavaBean

```
 ApplicationContext context = new ClassPathXmlApplicationContext("com\\javasm\\user\\config\\beans.xml");
        User user = context.getBean(User.class);
```

### 4、bean生命周期

> 定义
> 初始化
> 使用
> 销毁


#### 4.1 初始化及销毁

> 初始化

- 实现org.springfromework.beans.factoty.InitialiZingBean接口，覆盖afterPropertiesSetfang方法
- 配置init-method

```
<bean id="exampleInitBean" class="examples.ExampleBean" init-method="init" />
```


> 初始化

- 实现org.springframework.beans.factory.DisposableBean，覆盖destroy方法
- 配置destroy-method
```
<bean id="exampleInitBean" class="examples.ExampleBean" destroy-methid="cleanup" />
```

> 配置全局默认初始化销毁方法，需要在bean配置文件中配置

```
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd" default-init-method="start2" default-destroy-method="stop2">
```

#### 4.2 ApplicationContext手动关闭

>  在非Web应用中，手工加载Spring IoC容器，不能用ApplicationContext，要用AbstractApplicationContext。用完以后要记得调用ctx.close()关闭容器。如果不记得关闭容器，最典型的问题就是数据库连接不能释放

```
 ((AbstractApplicationContext)context).close();
```
> 在bean配置scope="prototype"属性时，default-destroy-method、destroy-method是不能执行的


### 5、Bean的作用域

> singleton
 - 单例，指一个bean容器中只存在一份
 
> prototype
 - 每次请求（每次使用）创建新的实例，destroy方法不生效
 
> request
 - 每次http请求创建一个实例且仅当前request内有效
 
> session
 - 同上，每次http请求创建，当前session内有效
 
> global session
 - 基于portlet的web中有效（portlet定义了global session），如果是在web中，同session
 
 
 ### 6、依赖注入
 
 > Setter注入
 - 通过调用与bean的配置元数据中定义的所有属性相对应的setter方法注入这些属性，还可以注入其他Bean依赖项和简单值，如字符串、类、枚举等。
 - 可以通过使用<property>元素的ref特性指定对其他Bean的引用
 
 ```
 <bean id="user" class="com.javasm.user.entity.User">
		<property name="name" value="李四"></property>
		<property name="name" value="张三"></property>
		<property name="role" ref="role"></property>
	</bean>
 ```
 > 构造函数注入
 
 ```
 <bean id="user" class="com.javasm.user.entity.User">
		<constructor-arg ref="role" />
	</bean>
 ```
 
 ### 7、创建Bean的方式
 
 #### 使用构造器创建
 
 #### 使用静态工厂方法创建
 
 - 采用静态工厂方法创建Bean的<bean.../>元素时，需要指定如下连个属性：

 - -  **class:** 该属性的值为静态工厂类的类名
 
 - -  **factory-method:** 该属性指定静态工厂方法类生产Bean实例
 
 - 如果静态工厂方法需要参数，则使用<constructor-arg../>元素传入
 ```
 <bean id="dog" class="com.sysker.factory.BeingFactory" factory-method="getBeing">
    <constructor-arg value="dog" />
    <property name="msg" value="我是狗" />
 </bean>
 <bean id="cat" class="com.sysker.factory.BeingFactory" factory-method="getBeing">
    <constructor-arg value="cat" />
    <property name="msg" value="我是猫" />
 </bean>
 ```
 
 
 #### 调用实例工厂方法创建
 
 - 采实例工厂方法创建Bean的<bean.../>元素时，需要指定如下连个属性：
 
 - - factory-bean:该属性的值为工厂Bean的id
 
 - - factory-method:该属性指定实例工厂的工厂方法 
 
 - 与静态工厂方法相似，如果需要参数，则使用<constructor-arg../>元素传入 