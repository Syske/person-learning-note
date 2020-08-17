### 1、创建maven项目
- 按照步骤一步一步来
- - 创建项目
![image](https://note.youdao.com/yws/api/personal/file/518B34A3DC1D4606AC1B997C6D1F0A1E?method=download&shareKey=e394f1aec92abbf81cc9691f10ce9cdf)

- - 这里选择maven的模板

![image](https://note.youdao.com/yws/api/personal/file/0067AF5ACF0B441CB92D40410A4FDD53?method=download&shareKey=c1926b8a4998e97dc20564f0bd70784f)

- - 设置包名

![image](https://note.youdao.com/yws/api/personal/file/5A68C5645C924596978FDBC5AB022467?method=download&shareKey=c6712a814e6c0267ffb00e318d5e3d62)

- - 设置项目的maven的配置信息、maven仓库路径（会从maven配置文件中获取）

![image](https://note.youdao.com/yws/api/personal/file/BD4C0C7B6E464926A55B73272A619DB8?method=download&shareKey=fd88702ec2ab1d8f124f1669574fe168)

- - 这里设置项目名、项目保存路径

![image](https://note.youdao.com/yws/api/personal/file/E513D5C8AC394900A43147F5BAF586EB?method=download&shareKey=65d6354600dec83722af1a3e3f440bd0)

- - 在main文件夹下创建java文件夹并标记为sources Root，以同样的方式创建test文件夹，并标记为test root

![image](https://note.youdao.com/yws/api/personal/file/8077F06D3DE14A7E81AFDA852AD16E30?method=download&shareKey=a723526edde5c60dccc21a14ac2a40c9)

### 2、配置pom.xml

```
<?xml version="1.0" encoding="UTF-8"?>

<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>io.github.syske</groupId>
  <artifactId>springDemo3</artifactId>
  <version>1.0-SNAPSHOT</version>
  <packaging>war</packaging>

  <name>springDemo Maven Webapp</name>
  <!-- FIXME change it to the project's website -->
  <url>http://www.example.com</url>

  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.source>1.8</maven.compiler.source>
    <maven.compiler.target>1.8</maven.compiler.target>
    <spring.version>5.0.8.RELEASE</spring.version>
  </properties>

  <dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>4.12</version>
      <scope>test</scope>
    </dependency>

    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-core</artifactId>
      <version>${spring.version}</version>
    </dependency>

    <!-- pring IOC的基础实现，包含访问配置文件、创建和管理bean等 -->
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-beans</artifactId>
      <version>${spring.version}</version>
    </dependency>

    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-context</artifactId>
      <version>${spring.version}</version>
    </dependency>

    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-context-support</artifactId>
      <version>${spring.version}</version>
    </dependency>

    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-web</artifactId>
      <version>${spring.version}</version>
    </dependency>

    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-webmvc</artifactId>
      <version>${spring.version}</version>
    </dependency>

    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-tx</artifactId>
      <version>${spring.version}</version>
    </dependency>

    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-aop</artifactId>
      <version>${spring.version}</version>
    </dependency>


    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-aspects</artifactId>
      <version>${spring.version}</version>
    </dependency>

    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-jdbc</artifactId>
      <version>${spring.version}</version>
    </dependency>

    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-test</artifactId>
      <version>${spring.version}</version>
    </dependency>

      <dependency>
          <groupId>org.aspectj</groupId>
          <artifactId>aspectjweaver</artifactId>
          <version>1.8.13</version>
      </dependency>


    <!-- https://mvnrepository.com/artifact/com.alibaba/fastjson -->
    <dependency>
      <groupId>com.alibaba</groupId>
      <artifactId>fastjson</artifactId>
      <version>1.2.49</version>
    </dependency>


    <!-- https://mvnrepository.com/artifact/javax.websocket/javax.websocket-api -->
    <dependency>
      <groupId>javax.websocket</groupId>
      <artifactId>javax.websocket-api</artifactId>
      <version>1.1</version>
      <scope>provided</scope>
    </dependency>

    <!-- https://mvnrepository.com/artifact/javax.servlet/javax.servlet-api -->
    <dependency>
      <groupId>javax.servlet</groupId>
      <artifactId>javax.servlet-api</artifactId>
      <version>3.1.0</version>
      <scope>provided</scope>
    </dependency>

    <!-- 数据库依赖 -->
    <!-- https://mvnrepository.com/artifact/commons-dbcp/commons-dbcp -->
    <dependency>
      <groupId>commons-dbcp</groupId>
      <artifactId>commons-dbcp</artifactId>
      <version>1.4</version>
    </dependency>

    <!-- https://mvnrepository.com/artifact/org.mybatis/mybatis-spring -->
    <dependency>
      <groupId>org.mybatis</groupId>
      <artifactId>mybatis-spring</artifactId>
      <version>1.3.2</version>
    </dependency>

      <!-- https://mvnrepository.com/artifact/mysql/mysql-connector-java -->
      <dependency>
          <groupId>mysql</groupId>
          <artifactId>mysql-connector-java</artifactId>
          <version>5.1.46</version>
      </dependency>

    <!-- https://mvnrepository.com/artifact/org.mybatis/mybatis -->
    <dependency>
      <groupId>org.mybatis</groupId>
      <artifactId>mybatis</artifactId>
      <version>3.4.6</version>
    </dependency>
    <!-- https://mvnrepository.com/artifact/org.apache.poi/poi-ooxml -->
    <dependency>
      <groupId>org.apache.poi</groupId>
      <artifactId>poi-ooxml</artifactId>
      <version>3.12</version>
    </dependency>


  </dependencies>

  <build>

    <resources>
      <resource>
        <directory>src/main/java</directory>
        <excludes>
          <exclude>**/*.java</exclude>
        </excludes>
      </resource>
    </resources>

    <finalName>springDemo</finalName>
    <pluginManagement><!-- lock down plugins versions to avoid using Maven defaults (may be moved to parent pom) -->
      <plugins>
        <plugin>
          <artifactId>maven-clean-plugin</artifactId>
          <version>3.0.0</version>
        </plugin>
        <!-- see http://maven.apache.org/ref/current/maven-core/default-bindings.html#Plugin_bindings_for_war_packaging -->
        <plugin>
          <artifactId>maven-resources-plugin</artifactId>
          <version>3.0.2</version>
        </plugin>
        <plugin>
          <artifactId>maven-compiler-plugin</artifactId>
          <version>3.7.0</version>
        </plugin>
        <plugin>
          <artifactId>maven-surefire-plugin</artifactId>
          <version>2.20.1</version>
        </plugin>
        <plugin>
          <artifactId>maven-war-plugin</artifactId>
          <version>3.2.0</version>
        </plugin>
        <plugin>
          <artifactId>maven-install-plugin</artifactId>
          <version>2.5.2</version>
        </plugin>
        <plugin>
          <artifactId>maven-deploy-plugin</artifactId>
          <version>2.8.2</version>
        </plugin>
      </plugins>
    </pluginManagement>
  </build>
</project>



```

### 3、配置web.xml
```
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://java.sun.com/xml/ns/javaee" xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_3_0.xsd" id="WebApp_ID" version="3.0">
  <display-name>springMVC</display-name>
  <welcome-file-list>
    <welcome-file>index.html</welcome-file>
    <welcome-file>index.htm</welcome-file>
    <welcome-file>index.jsp</welcome-file>
    <welcome-file>default.html</welcome-file>
    <welcome-file>default.htm</welcome-file>
    <welcome-file>default.jsp</welcome-file>
  </welcome-file-list>
  <!-- 过滤器 -->
  <listener>
    <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
  </listener>

  <context-param>
    <param-name>contextConfigLocation</param-name>
    <param-value>classpath:spring-applicat-context.xml</param-value>
  </context-param>
  <!-- DispatcherServlet配置-->
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

### 4、spring核心配置spring-applicat-context.xml
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
            base-package="io.github.sysker" />
    <!-- 开启注解 -->
    <mvc:annotation-driven />
    <!-- 配置静态资源 -->
   <!-- <mvc:resources mapping="/resources/**"
                   location="/WEB-INF/resources/" />-->

    <mvc:default-servlet-handler />

    <!-- 配置simpledateformat -->
    <bean id="simpleDateFormat" class="java.text.SimpleDateFormat">
        <constructor-arg value="yyyy-MM-dd HH:mm:ss"/>
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

        <!-- 自动扫描mapping.xml文件 -->
        <property name="mapperLocations"
                  value="classpath:io/github/sysker/mapper/DanmuInfo.xml"></property>
        <property name="typeAliasesPackage"
                  value="io.github.sysker.entity"></property>

    </bean>

    <!-- DAO接口所在包名，Spring会自动查找其下的类 -->
    <bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
        <property name="basePackage" value="io.github.sysker.dao" />
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

### 5、mybatis.xml配置
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

### 6、jdbc.properties
```
driver=com.mysql.jdbc.Driver

url=jdbc:mysql://localhost:3307/spring?characterEncoding=UTF-8&amp;useSSL=false

username=root

password=root


initialSize=0

maxActive=20

maxIdle=20

minIdle=1

maxWait=60000
```

### 7、log4j.properties配置文件(这里需要在pom的依赖中引入log4j的依赖包)
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

### 8、项目结构
- 这里要格外注意spring核心配置的路径
![image](https://note.youdao.com/yws/api/personal/file/1444A1C277164F2C87B513CB371E960B?method=download&shareKey=5e4bbc074ad77c399b8795d67e95a97e)

### 9、项目部署
- 这里指示够清晰了，不做过多说明

![image](https://note.youdao.com/yws/api/personal/file/D122B6E8916B4C75B5088DDFBD7C0CAC?method=download&shareKey=740557b2fe07cfaa4ed6ecb91063222d)

- 添加新的配置，选择tomcat

![image](https://note.youdao.com/yws/api/personal/file/55C8EDC29EE84BBF959F4F4530DD0383?method=download&shareKey=1c06d0f8ce55097b8deba0c3decb6fd0)

- 配置tomcat服务器的基本信息

![image](https://note.youdao.com/yws/api/personal/file/14F9004DAB80411CAEB847EE777500BD?method=download&shareKey=5d8013121cffb2893d543b157a131ef4)

- 部署项目

![image](https://note.youdao.com/yws/api/personal/file/4D841E1923164DC4AA5F83B420B4E3C2?method=download&shareKey=e9905c845c69e7e7283a23995e64f579)

- 选择部署形式

![image](https://note.youdao.com/yws/api/personal/file/F23F3ED34BB04F9FBFDD9480AE018D75?method=download&shareKey=7dcc0da73ed57ec9572a4d9a11655707)

- 运行

![image](https://note.youdao.com/yws/api/personal/file/6F79FE55EEC7432AB635EE8DAEDC597A?method=download&shareKey=112cc24afec1abd65bf245c792d9e01d)