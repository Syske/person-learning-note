### 1、项目目录

![image](https://note.youdao.com/yws/api/personal/file/AF6937906CEA451C9E98C1486CC48C78?method=download&shareKey=6082ab607c62fa1f6c9f5f1f15ec7dc8)

### 2、jar包

![image](https://note.youdao.com/yws/api/personal/file/5C15917CCBFC4B058067AFEB004B7700?method=download&shareKey=9d21585196db5eaa6dab8dacba9d4fd3)

- dbcp:连接池
- pool：连接池
- logging:日志
- log4j:日志
- mybatis-spring：用于SqlSession等相关操作
- spring相关包
- mybatis

 ### 3、web.xml配置
 - 可以删除本配置文件，本次测试用的是JUnit，不涉及网络访问，所有该配置文件并不需要
 
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
 
 ### 4、spring-mybatis.xml配置
 
 - 注释已经够详细，不再详细说明
 
 ```
 <?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"  
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:p="http://www.springframework.org/schema/p"  
    xmlns:context="http://www.springframework.org/schema/context"  
    xmlns:mvc="http://www.springframework.org/schema/mvc"  
    xsi:schemaLocation="http://www.springframework.org/schema/beans    
                        http://www.springframework.org/schema/beans/spring-beans-3.1.xsd    
                        http://www.springframework.org/schema/context    
                        http://www.springframework.org/schema/context/spring-context-3.1.xsd    
                        http://www.springframework.org/schema/mvc    
                        http://www.springframework.org/schema/mvc/spring-mvc-4.0.xsd">  
    <!-- 自动扫描 -->  
    <context:component-scan base-package="com.sysker.spring.dome" />  
    <!-- 引入配置文件 -->  
    <bean id="propertyConfigurer"  
        class="org.springframework.beans.factory.config.PropertyPlaceholderConfigurer">  
        <property name="location" value="classpath:jdbc.properties" />  
    </bean>  
   <!-- 连接池配置 -->  
    <bean id="dataSource" class="org.apache.commons.dbcp.BasicDataSource"  
        destroy-method="close">  
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
    <bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">  
        <property name="dataSource" ref="dataSource" />  
        <!-- 自动扫描mapping.xml文件 -->  
        <property name="mapperLocations" value="classpath:com/sysker/spring/dome/mapping/*.xml"></property>  
    </bean>  
  
    <!-- DAO接口所在包名，Spring会自动查找其下的类 -->  
    <bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">  
        <property name="basePackage" value="com.sysker.spring.dome.dao" />  
        <property name="sqlSessionFactoryBeanName" value="sqlSessionFactory"></property>  
    </bean>  
  
    <!-- (事务管理)transaction manager, use JtaTransactionManager for global tx -->  
    <bean id="transactionManager"  
        class="org.springframework.jdbc.datasource.DataSourceTransactionManager">  
        <property name="dataSource" ref="dataSource" />  
    </bean>  
    
    <!-- 配置事务管理模板：Spring为了简化事务管理的代码而提供的类 -->
    <bean id="transactionTemplate" class="org.springframework.transaction.support.TransactionTemplate">
    	<property name="transactionManager" ref="transactionManager"></property>
    </bean>
  
</beans>  

 ```
 
 ### 5、jdbc.properties配置
 
 ```
 driver=com.mysql.jdbc.Driver

url=jdbc:mysql://localhost:3306/spring?characterEncoding=UTF-8&amp;useSSL=false 

username=root

password=root

 
initialSize=0  

maxActive=20  
 
maxIdle=20  
  
minIdle=1  

maxWait=60000 

 ```
 
 ### 6、log4j配置（日志）
 
 ```
#定义LOG输出级别  
log4j.rootLogger=INFO,Console,File  
#定义日志输出目的地为控制台  
log4j.appender.Console=org.apache.log4j.ConsoleAppender  
log4j.appender.Console.Target=System.out  
#可以灵活地指定日志输出格式，下面一行是指定具体的格式  
log4j.appender.Console.layout = org.apache.log4j.PatternLayout  
log4j.appender.Console.layout.ConversionPattern=[%c] - %m%n  
  
#文件大小到达指定尺寸的时候产生一个新的文件  
log4j.appender.File = org.apache.log4j.RollingFileAppender  
#指定输出目录  
log4j.appender.File.File = logs/ssm.log  
#定义文件最大大小  
log4j.appender.File.MaxFileSize = 10MB  
# 输出所以日志，如果换成DEBUG表示输出DEBUG以上级别日志  
log4j.appender.File.Threshold = ALL  
log4j.appender.File.layout = org.apache.log4j.PatternLayout  
log4j.appender.File.layout.ConversionPattern =[%p] [%d{yyyy-MM-dd HH\:mm\:ss}][%c]%m%n

 ```

### 7、entity及mapping.xml

```
package com.sysker.spring.dome.entity;

public class Account {
    // 账户id
    private String id;
    // 账号名
    private String name;
    // 余额
    private String money;

    public Account() {
        super();
    }

    public Account(String id, String name, String money) {
        super();
        this.id = id;
        this.name = name;
        this.money = money;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getMoney() {
        return money;
    }

    public void setMoney(String money) {
        this.money = money;
    }

}

```
- 由于直接mapping中直接用的是穿进来的参数，所以实体类也没有用到
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd" >
<mapper namespace="com.sysker.spring.dome.dao.AccountDao">
    <update id="inMoney">
    	update account set
    	money = money + #{arg1}
    	where name = #{arg0}
    </update>
    
    <update id="outMoney">
    	update account set
    	money = money - #{arg1}
    	where name = #{arg0}
    </update>
</mapper>
```


### 8、Dao

```
package com.sysker.spring.dome.dao;

public interface AccountDao {
    void outMoney(String out, String money);

    void inMoney(String in, String money);
}

```

### 9、service及serviceImpl

```
package com.sysker.spring.dome.service;

public interface AccountService {
    
    void transfer(String out, String in, String money);
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

### 10、测试类

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


### 总结

- 今天在慕课网学习，本来是打算实现事务管理的，但发现视频中老师采用的是jdbc连接，所以就参考老师的思路，实现了mybatis-spring整合，过程虽然艰难，但确实收获满满：
- - 1、对依赖注入有了更深的理解和认知，对spring有了更全面的认知，当然更多的还是发现自己了解的太浅；
- - 2、多练习，多尝试，多思考，多琢磨，多总结，当你踩完所有的坑，你就离成神之路不远了
- - 3、我始终比较喜欢在bug中学习，每填掉一个坑都让人感到兴奋，同时也会收获很多