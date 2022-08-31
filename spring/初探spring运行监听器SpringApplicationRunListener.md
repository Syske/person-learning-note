# spring运行监听器
### 前言


### 运行监听器
```properites
org.springframework.boot.SpringApplicationRunListener=io.github.syske.springbootbeanlisttest.listener.MySpringRunListener
```
运行监听器实现
```java
/**
 * @program: springboot-bean-list-test
 * @description:
 * @author: syske
 * @date: 2022-06-06 18:39
 */
public class MySpringRunListener implements SpringApplicationRunListener {

    private final SpringApplication application;

    private final String[] args;

    public MySpringRunListener(SpringApplication application, String[] args) {
        this.application = application;
        this.args = args;
    }

    @Override
    public void starting() {
        System.out.println("MySpringRunListener starting");
    }

    @Override
    public void environmentPrepared(ConfigurableEnvironment environment) {
        System.out.println("MySpringRunListener environmentPrepared");
    }

    @Override
    public void contextPrepared(ConfigurableApplicationContext context) {
        System.out.println("MySpringRunListener contextPrepared");
    }

    @Override
    public void contextLoaded(ConfigurableApplicationContext context) {
        System.out.println("MySpringRunListener contextLoaded");
    }

    @Override
    public void started(ConfigurableApplicationContext context) {
        System.out.println("MySpringRunListener started");
    }

    @Override
    public void running(ConfigurableApplicationContext context) {
        System.out.println("MySpringRunListener running");
    }

    @Override
    public void failed(ConfigurableApplicationContext context, Throwable exception) {
        System.out.println("MySpringRunListener failed");
    }
}
```