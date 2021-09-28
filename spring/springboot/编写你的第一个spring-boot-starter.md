# 编写你的第一个spring-boot-starter
tags: [#springboot, #stater]

### 前言

我们在使用`spring-boot`的时候，会经常用到各种各样的`starter`，比如`spring-boot-starter-web`，不知道各个小伙伴有没有好奇过这些`starter`到底是怎么定义出来的，反正我好奇过，但是一直没有去深入了解过，最近在项目开发中，我们需要封装一个`mq`的通用组件，有个同事就封装成一个`starter`，然后就勾起了学习和研究的好奇心，所以想着趁今天的时间做一个小`demo`，写一个属于自己的`starter`。

下面我们就来看下具体如何实现。

### 手写spring-boot-starter

#### 创建项目

首先我们要创建一个`maven`项目，根据自己的需要引入项目依赖，因为我们要写的是`sprin-boot`的`starter`，所以`spring-boot-starter`的依赖必须引入：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter</artifactId>
    <version>2.3.7.RELEASE</version>
    <scope>compile</scope>
    <optional>true</optional>
</dependency>
```

因为`starter`的核心其实是配置类，而这些配置类注解都在`spring-boot-starter`包下。创建完成后的项目结构如下：

![](https://gitee.com/sysker/picBed/raw/master/20210718180009.png)

我的这个组件是一个通用的消息发送组件，所以我还引入`activemq`的相关包，对`demo`感兴趣的小伙伴可以直接去看项目源码，文末有地址。

#### 配置类

这里就是`starter`的核心了，这里我们要对组件进行配置，主要是`bean`的注入：

```java
@Configuration
@EnableJms
@ConditionalOnClass(JmsMessageServiceImpl.class)
public class AutoConfigurationClass {

    @Value("${spring.activemq.broker-url}")
    private String brokerURL;

    @ConditionalOnMissingBean
    @Bean
    public JmsMessageService jmsMessageService(JmsMessagingTemplate jmsTemplate){
        return new JmsMessageServiceImpl(jmsTemplate);
    }

    @ConditionalOnMissingBean
    @Bean
    public JmsMessagingTemplate jmsMessagingTemplate(ConnectionFactory connectionFactory) {
        return new JmsMessagingTemplate(connectionFactory);
    }

    @ConditionalOnMissingBean
    @Bean
    public ConnectionFactory connectionFactory() {
        return new ActiveMQConnectionFactory(brokerURL);
    }
}
```

前面说了我的组件是通用的消息组件，所以我这里主要是针对`ActiveMq`的一些配置，包括`JmsMessagingTemplate`、`JmsMessageService`和`ConnectionFactory`。

这里还通过`@Value`注解注入了`mq`的地址，这个地址需要在`starter`的使用项目中注入，后面我们会演示。

`@EnableJms`注解的作用是启用消息组件，如果没有这个注解，整个消息组件就没啥用了；

`@ConditionalOnClass`注解的作用是，只有在至指定的`class`（这里的`JmsMessageServiceImpl.class`）存在的时候（也就是依赖了这个类对应的包），配置才会生效（这样看我这里的这个配置没啥用），类似的配置还有好几个，后面研究下；

`@ConditionalOnMissingBean`注解起的是标记作用，通常和`@Bean`一起使用，如果加了这个注解，这个类就不允许重复注入了。

#### 业务实现

这里的业务实现就是普通的`java`实现，前面我们已经在配置类中以及注入过这个类的实例了，后面在引用当前`starter`的`spring-boot`项目中就可以直接通过`@AutoWired`注解使用了

```java
public class JmsMessageServiceImpl implements JmsMessageService {
    private final Logger logger = LoggerFactory.getLogger(JmsMessageServiceImpl.class);

    private JmsMessagingTemplate jmsTemplate;

    public JmsMessageServiceImpl(JmsMessagingTemplate jmsTemplate) {
        this.jmsTemplate = jmsTemplate;
    }



    @Override
    public void sendMessage(String mqQueueName, String message) {
        logger.info("method: [sendMessage] input parameter: mqQueueName = {}， message = {}", mqQueueName, message);
        jmsTemplate.convertAndSend(mqQueueName, message);
    }

    @Override
    public MessageReceiveVO sendAndReceive(String mqQueueName, String message) {
        logger.info("method: [sendMessage] input parameter: mqQueueName = {}， message = {}", mqQueueName, message);
        Message<?> messageBack = jmsTemplate.sendAndReceive(mqQueueName, new StringMessage(message));
        String payload = (String) messageBack.getPayload();
        logger.info("method: [sendMessage] return result: payload = {}", payload);
        return JSON.parseObject(payload, MessageReceiveVO.class);
    }

    class StringMessage implements Message<String> {

        private String payload;
        private MessageHeaders messageHeaders;

        public StringMessage(String payload) {
            this.payload = payload;
        }

        @Override
        public String getPayload() {
            return this.payload;
        }

        @Override
        public MessageHeaders getHeaders() {
            return this.messageHeaders;
        }
    }
}
```

#### META-INF文件编写

这里才是`starter`组件的重中之重，如果没有这里的配置文件，你的组件并不会被`spring-boot`发现。

我们创建一个名字叫`spring.factories`的文件，然后在文件中添加如下内容：

```properties
#-------starter自动装配---------
org.springframework.boot.autoconfigure.EnableAutoConfiguration=io.github.syske.starter.demo.config.AutoConfigurationClass
```

这里文件名字是固定的，其他名称是无法识别的，文件中的`org.springframework.boot.autoconfigure.EnableAutoConfiguration`也是固定的，就是一个键名，后面的`io.github.syske.starter.demo.config.AutoConfigurationClass`是我们配置类的名称，根据`spring-boot`使用经验，这个配置应该是支持多个类的，用逗号分隔应该就好了，我还没来得及试验，有兴趣的小伙伴自己尝试下。

然后到这里我们的`starter`就编写完成了，下面我们要打包，然后测试。

#### spring-boot-starter打包安装

这里打包也很简单，我们直接使用`maven`的`install`工具就可以，需要注意的是，我们要在`pom.xml`中指定打包类型：

![](https://gitee.com/sysker/picBed/raw/master/20210718183419.png)

点击`install`菜单后，我们的`start`会被安装到本地`maven`仓库中

![](https://gitee.com/sysker/picBed/raw/master/20210718183519.png)

#### 测试

因为`stater`是要引入`spring-boot`项目中才能使用的，所以我们要先创建一个`spring-boot`项目，然后引入我们刚才打的`starter`：

![](https://gitee.com/sysker/picBed/raw/master/20210718183957.png)

这里我们还要在配置文件中添加`mq`的地址：

![](https://gitee.com/sysker/picBed/raw/master/20210718184227.png)

然后我们直接在单元测试中测试下我们的`stater`:

```java
@SpringBootTest
class SpringBootSraterTestApplicationTests {

    @Autowired
    private JmsMessageService jmsMessageService;

    @Test
    void contextLoads() {
        jmsMessageService.sendMessage("spring_boot_starter", "hello spring-boot-start");
    }

}
```

直接运行这个方法，然后我们登录`mq`的管理台看下：

![](https://gitee.com/sysker/picBed/raw/master/20210718184502.png)

可以看到我们的消息已经成功发送到`mq`中了，说明我们的`starter`组件已经运行成功了。

### 总结

`spring-boot-starter`确实用起来很方便，感觉就像一个插座一样，随插即用，可以说通过`spring-boot-starter`我们可以真正做到组件化的模块编程，而且在我们的演示项目中，如果我们`mq`的地址也是固定的话，那我们甚至连配置文件都不需要了，只需要引入`starter`依赖即可使用其中的`spring-boot`组件，简直不要太方便。

好了，手写`starter`就到这里吧，踩坑过程确实比较费时间，所以今天也就更的有点晚了，不过还好，总算完了😂