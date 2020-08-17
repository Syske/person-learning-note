### 1、SpringBootApplication
Spring Boot项目的核心注解，主要目的是开启自动配置

### 2、@Configuration
- 通过该注解来表明该类是一个Spring的配置类，相当于一个xml文件

### 3、@ComponentScan(basePackages="com.example.javaconfig")
- 配置扫描包

### 4、@propertySource(value={"classpath:jdbc.properties","classpath:xxxx"}, ignoreResourceNotFound = true) 
- 配置jdbc.properties文件
