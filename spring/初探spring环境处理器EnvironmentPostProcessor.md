# 初探环境处理器
### 前言


### 处理器
配置文件
需要在`spring.factories`文件中增加如下配置

```
org.springframework.boot.env.EnvironmentPostProcessor=io.github.syske.springbootbeanlisttest.environment.SyskeEnvironmentPostProcessor

```

后置处理器实现
```java
public class SyskeEnvironmentPostProcessor implements EnvironmentPostProcessor {
    @Override
    public void postProcessEnvironment(ConfigurableEnvironment environment, SpringApplication application) {
        System.out.println("syske postProcessEnvironment ");
    }
}
```

### 结语