# springboot知识点

### 1、项目不需要加载数据库时，为避免启动报错，需在启动入口加上如下注解

```java
@SpringBootApplication(exclude={DataSourceAutoConfiguration.class,HibernateJpaAutoConfiguration.class})
```

