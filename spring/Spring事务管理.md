### 1、概念

- **事务：** 逻辑上的一组操作，这组操作要么全部成功，要么全部失败。
- **特性：** 
- - 原子性：不可分割
- - 统一性：数据完整性要一致
- - 隔离线：线程安全（多个用户并发访问数据）
- - 持久性：事务被提交后，数据的改变就是永久性的，及时数据库发生故障也不能对其有任何影响


### 2、事务管理高层抽象接口

- **PlatformTransaction:**事务管理器
- - spring为不同的持久化框架提供了不同的PlatformTtansactionManager接口实现：

事务 | 说明
---|---
org.springframework.jdbc.datasource.DataSourceTransactionManager | 使用Spring JDBC或mybatis进行持久化数据时使用
org.springframework.orm.hibernate3.HibernateTransactionManager | 使用Hibernate3.0进行持久化数据时使用
org.springframework.jpa.JpaTransactionManager | 使用JPA进行持久化时使用
org.springframework.jdo.JdpTransactionManager | 当持久化机制是Jdo时使用
org.springframework.transaction.jta.JtaTransactionManager | 使用一个JTA实现来管理事务，在一个事务跨越多个资源时必须使用



- **TransactionDefinition：** 事务定义信息（隔离、传播、超时、只读）
- - 事务隔离级别：

隔离级别 | 说明
---|---
DEFAULT | 使用后端数据库默认的隔离级别（Spring中的选择项）
READ_UNCOMMITED | 允许 你读取还未提交的改变了的数据。可能导致脏、幻、不可重复读
REPEATABLE_READ | 对相同的字段的多次读取是一致的，除非数据被事务本身改变。可防止脏、不可重复读，但幻读仍有可能发生
SERIALIZABLE | 完全服从ACID的隔离级别，确保不发生脏、幻、不可重复读。这在所有隔离级别中是最慢的，它是典型的通过完全锁定在事务中涉及的数据表来完成的

- - 脏读：一个事务读取了另一个事务该写的但还未提交的数据，如果这些数据被回滚，则读到的数据时无效的。

- - 不可重复读：在同一事务中，多次读取同一数据返回的结果有所不同 


- - 幻读：一个事务读取了几行记录后，另一个事务插入一些记录，幻读就发生了，再后来的查询中，第一个事务就会发现有些原理没有的记录 

- - 事务传播行为

事务传播行为类型 | 说明
---|---
PROPAGATION_REQUIRED | 支持当前事务，如果不存在就新建一个
PROPAGATION_SUPPORTS | 支持当前事务，如果不存在，就不使用事务
PROPAGATION_MANDATORY| 支持当前事务，如果不存在，就抛出异常
PROPAGATION\_REQUIRES\_NEW | 如果有事务存在，挂起当前事务，创建一个新的事务
PROPAGATION\_NOT\_SUPPORTED| 以非事务方式运行，如果有事务存在，挂起当前事务
PROPAGATION_NEVER | 以非事务方式运行，如果有事务存在，抛出异常
PROPAGATION_NESTED | 如果当前事务存在，则嵌套事务执行

- **TransactionStatus:** 事务具体运行状态

### 3、事务管理方式

### 3.1、编程式事务管理（很少用到）

- 在AccountService中使用TransactionTemplate
- TransactionTemplate依赖DataSourceTransactionManager
- DataSourceTransactionManager依赖DataSource构造

```
  <!-- (事务管理)transaction manager, use JtaTransactionManager for global tx -->  
    <bean id="transactionManager"  
        class="org.springframework.jdbc.datasource.DataSourceTransactionManager">  
        <property name="dataSource" ref="dataSource" />  
    </bean>  
    
    <!-- 配置事务管理模板：Spring为了简化事务管理的代码而提供的类 -->
    <bean id="transactionTemplate" class="org.springframework.transaction.support.TransactionTemplate">
    	<property name="transactionManager" ref="transactionManager"></property>
    </bean>
```

service实现，包含了事务管理
```
package com.sysker.spring.dome.service.impl;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.TransactionStatus;
import org.springframework.transaction.support.TransactionCallbackWithoutResult;
import org.springframework.transaction.support.TransactionTemplate;

import com.sysker.spring.dome.dao.AccountDao;
import com.sysker.spring.dome.service.AccountService;

@Service
public class AccountServiceImpl implements AccountService {
    
    @Autowired
    private AccountDao accountDao;
    
    @Autowired
    private TransactionTemplate transactionTemplate;
    
    @Override
    public void transfer(String out, String in, String money) {
        /**
         * 事务管理，execute()方法中创建了一个匿名内部类，在匿名内部类中操作业务，即可实现事务管理
         */
        transactionTemplate.execute(new TransactionCallbackWithoutResult() {
            
            @Override
            protected void doInTransactionWithoutResult(TransactionStatus transactionStatus) {
                accountDao.outMoney(out, money);
                int i = 1/0;
                accountDao.inMoney(in, money);
                
            }
        });
        
        
    }

}

```

测试类

```
package com.sysker.spring.dome.test;


import javax.annotation.Resource;

import org.apache.log4j.Logger;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import com.sysker.spring.dome.service.AccountService;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath:spring-mybatis.xml"})
public class TestMybatis {
    private static Logger logger = Logger.getLogger(TestMybatis.class);
    @Resource
    private AccountService accountService = null;
    
    @Test
    public void test1() {
        accountService.transfer("aaa", "bbb", "200");
        logger.info("success");
        
    }
    
}

```

- **缺点：** 在开发中需要修改过java代码，在实际开发中不会用到

#### 3.2、声明式事务事务管理

- 使用XML配置声明式事务（原始方式）（很少用到）
- - 使用TransactionProxyFactoryBean
```
<!-- 配置事务管理器 -->
<bean id="transactionManager"
		class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
		<property name="dataSource" ref="dataSource" />
	</bean>
<!-- 配置业务层的代理 -->
 <bean id="accountServiceProxy" class="org.springframework.transaction.interceptor.TransactionProxyFactoryBean" >
 <!-- 配置目标对象 -->
    <property name="transactionManager" ref="transactionManager"></property>
    <!-- 注入事务管理器 -->
    <property name="target" ref="accountService"></property>
    <!-- 注入事务属性 -->
    <property name="transactionAttributes">
        <props>
        <!-- 
        prop的格式:
            PROPAGATION : 事务的传播行为，必须有
            ISOLATION   : 事务的隔离级别
            readOnly    ：只读
            -Exception  :发生哪些异常回滚事务
            +Exception  :发生哪些异常不回滚事务
        
        -->
            <prop key="*">PROPAGATION_REQUIRED</prop>
        </props>
    </property>
 </bean>
```
- - prop格式：
- - - PROPAGATION,ISOLATION,readOnly,-Exception,+Exception
- - - 传播行为，隔离级别，只读事务，发生这些异常回滚事务，发生这些异常提交事务


测试类

```
package com.sysker.spring.dome.test;


import javax.annotation.Resource;

import org.apache.log4j.Logger;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import com.sysker.spring.dome.service.AccountService;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath:spring-mybatis.xml"})
public class TestMybatis {
    private static Logger logger = Logger.getLogger(TestMybatis.class);
    @Resource(name="accountServiceProxy")
    private AccountService accountService;
    
    @Test
    public void test1() {
        accountService.transfer("aaa", "bbb", "200");
        logger.info("success");
        
    }
    
}

``` 
service实现，包含了事务管理
```
package com.sysker.spring.dome.service.impl;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.TransactionStatus;
import org.springframework.transaction.support.TransactionCallbackWithoutResult;
import org.springframework.transaction.support.TransactionTemplate;

import com.sysker.spring.dome.dao.AccountDao;
import com.sysker.spring.dome.service.AccountService;

@Service
public class AccountServiceImpl implements AccountService {
    
    @Autowired
    private AccountDao accountDao;
    
    
    @Override
    public void transfer(String out, String in, String money) {
                accountDao.outMoney(out, money);
                int i = 1/0;
                accountDao.inMoney(in, money);
                
        
        
    }

}

```



-  基于AOP的事务管理（实际开发会经常用到）

```
<!-- (事务管理)transaction manager, use JtaTransactionManager for global tx -->
	<bean id="transactionManager"
		class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
		<property name="dataSource" ref="dataSource" />
	</bean>
	
	<!-- 基于aop的事务管理 -->
	<tx:advice id="txAdvice"
		transaction-manager="transactionManager">
		<tx:attributes>
		<!-- 
		    PROPAGATION : 事务的传播行为，必须有
            ISOLATION   : 事务的隔离级别
            readOnly    ：只读
            rollback-for  :发生哪些异常回滚事务
            no-rollback-for  :发生哪些异常不回滚事务
            timeout : 过期信息
		-->
			<tx:method name="transfer" />
		</tx:attributes>
	</tx:advice>
 <!-- 配置切面 -->
	<aop:config>
	<!-- 配置切点 -->
		<aop:pointcut id="fooServiceOperation"
			expression="execution(* com.sysker.spring.dome.service.impl.*.*(..))" />
			<!-- 配置切面 -->
		<aop:advisor advice-ref="txAdvice"
			pointcut-ref="fooServiceOperation" />
	</aop:config>

```

service实现，包含了事务管理

```
package com.sysker.spring.dome.service.impl;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.TransactionStatus;
import org.springframework.transaction.support.TransactionCallbackWithoutResult;
import org.springframework.transaction.support.TransactionTemplate;

import com.sysker.spring.dome.dao.AccountDao;
import com.sysker.spring.dome.service.AccountService;

@Service
public class AccountServiceImpl implements AccountService {
    
    @Autowired
    private AccountDao accountDao;
    
    
    @Override
    public void transfer(String out, String in, String money) {
                accountDao.outMoney(out, money);
                int i = 1/0;
                accountDao.inMoney(in, money);
                
        
        
    }

}

```

测试类

```
package com.sysker.spring.dome.test;


import javax.annotation.Resource;

import org.apache.log4j.Logger;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import com.sysker.spring.dome.service.AccountService;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath:spring-mybatis.xml"})
public class TestMybatis {
    private static Logger logger = Logger.getLogger(TestMybatis.class);
    @Resource(name="accountService)
    private AccountService accountService;
    
    @Test
    public void test1() {
        accountService.transfer("aaa", "bbb", "200");
        logger.info("success");
        
    }
    
}

``` 

- 基于注解的事务管理 （实际开发会经常用到）

```
<!-- 配置事务管理器 -->
<!-- (事务管理)transaction manager, use JtaTransactionManager for global tx -->
	<bean id="transactionManager"
		class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
		<property name="dataSource" ref="dataSource" />
	</bean>
	
	!-- 基于注解的事务管理 -->
	<tx:annotation-driven transaction-manager="transactionManager" />

```

service实现，包含了事务管理

```
package com.sysker.spring.dome.service.impl;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.TransactionStatus;
import org.springframework.transaction.support.TransactionCallbackWithoutResult;
import org.springframework.transaction.support.TransactionTemplate;

import com.sysker.spring.dome.dao.AccountDao;
import com.sysker.spring.dome.service.AccountService;

@Service
@Transactional
public class AccountServiceImpl implements AccountService {
    
    @Autowired
    private AccountDao accountDao;
    
    
    @Override
    public void transfer(String out, String in, String money) {
                accountDao.outMoney(out, money);
                int i = 1/0;
                accountDao.inMoney(in, money);
                
        
        
    }

}

```

测试类

```
package com.sysker.spring.dome.test;


import javax.annotation.Resource;

import org.apache.log4j.Logger;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import com.sysker.spring.dome.service.AccountService;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath:spring-mybatis.xml"})
public class TestMybatis {
    private static Logger logger = Logger.getLogger(TestMybatis.class);
    @Resource(name="accountService)
    private AccountService accountService;
    
    @Test
    public void test1() {
        accountService.transfer("aaa", "bbb", "200");
        logger.info("success");
        
    }
    
}

``` 
 
