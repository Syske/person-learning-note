# spring-boot整合activeMQ实现异步延迟消费

### 前言

最近，有一个需求，就是在用户发起第一步操作之后，需要在一个固定时间之后触发另一个操作，虽然通过定时任务也能实现，但是考虑到用户数量庞大，同时考虑到服务重启之后数据不会丢失，最终我们决定采用`activeMQ`异步延迟的方式

### activeMQ

#### 配置

首先要修改`conf/activemq.xml`，找到`broker`配置标签，在其中加入` schedulerSupport="true"`即可，不需要其他配置

```xml
<broker xmlns="http://activemq.apache.org/schema/core" brokerName="localhost" dataDirectory="${activemq.data}" schedulerSupport="true">
<!-- 标签内配置不需要改动 -->
     ...

</broker>
```



### spring-boot

这里先要创建`spring boot`项目，然后还需要简单配置下`MQ`，具体的配置和整合就不再细说，不清楚的小伙伴可以看下我之前分享的内容：

springboot整合ActiveMQ实现异步交易了解下？

https://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648418144&idx=1&sn=fd53a4456a246f3ee88d7de74f466cda&chksm=bea6c9ea89d140fc9cec281063442df7058e756fd3c87a31b30631aa67f823b452f2211c4cd5&token=1044120974&lang=zh_CN#rd

然后我们就可以开始今天示例内容了。

#### 最原始方式

首先我们来看最原始的方式：

```java
public void sendDelayMessage(String queueName, String messageInfo) {
        Connection connection = null;
        Session session = null;
        MessageProducer producer = null;
        // 获取连接工厂
        ConnectionFactory connectionFactory = jmsTemplate.getConnectionFactory();
        try {
            // 获取连接
            connection = connectionFactory.createConnection();
            connection.start();
            // 获取session，true开启事务，false关闭事务
            session = connection.createSession(Boolean.TRUE, Session.AUTO_ACKNOWLEDGE);

            // 创建一个消息队列
            producer = session.createProducer(new ActiveMQQueue(queueName));
            producer.setDeliveryMode(JmsProperties.DeliveryMode.PERSISTENT.getValue());
            ObjectMessage message = session.createObjectMessage(messageInfo);
            //设置延迟时间
            message.setLongProperty(ScheduledMessage.AMQ_SCHEDULED_DELAY, 60*1000L);
            // 发送消息
            producer.send(message);
            logger.info("发送消息：{}", messageInfo);
            session.commit();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (producer != null) {
                    producer.close();
                }
                if (session != null) {
                    session.close();
                }
                if (connection != null) {
                    connection.close();
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
```

这里最核心的操作是`setLongProperty`，也就是设置消息的延迟时间，这里我设置的延迟消费时间是`1`分钟，也就是说我通过该方法发送的消息会延迟一分钟之后才会被消费。

这里的原始写法是通过`JmsMessagingTemplate`拿到`mq`的`ConnectionFactory`，然后通过连接工厂拿到连接，从连接中拿到`session`信息，再接着从会话中创建消息生产者，同时创建消息对象，并设置消息延迟时间，最后通过生产者发送消息，提交会话事务并关闭资源。

这里可以看到，我们开启了`session`事务，这样可以确保同一个会话发送多个消息，最终会一起成功或者一起失败，和数据库事务类似。

#### JmsTemplate

下面是基于`JmsTemplate`的实现，相比上面这种原始的写法，这里的写法更简洁，也更优雅：

```java
public void sendDelayMessage2(String queueName, String messageInfo) {
        JmsBaseTemplate.send(new ActiveMQQueue(queueName), session -> {
            ObjectMessage message = session.createObjectMessage(messageInfo);
            //设置延迟时间
            message.setLongProperty(ScheduledMessage.AMQ_SCHEDULED_DELAY, 60*1000L);
            return message;
        });
}
```

只是这里的写法需要注入`JmsTemplate`:

```java
@Autowired
private JmsTemplate JmsBaseTemplate;
```

这里其实是调用了`JmsTemplate`的`send`方法实现的，只是我们自己通过`lambda`的方式创建了`messageCreator`，同时实现了它的`createMessage`方法，在`messageCreator`的`createMessage`方法中，我们只需要像第一种方式一样指定消息的延迟时间即可。

```java
send(final Destination destination, final MessageCreator messageCreator)
```

其实通过这个方式和我们上面原始的写法很类似，只是`session`之外的其他操作由`JmsBaseTemplate`已经帮我们封装了：

![](https://gitee.com/sysker/picBed/raw/master/images/20220103185514.png)

![](https://gitee.com/sysker/picBed/raw/master/images/20220103190057.png)

#### 消息消费者

消费者和普通消息没有任何区别，只需要配置对应的消息队列名称即可，然后在达到延迟时间时，消息就会被消费：

```java
@JmsListener(destination = "delay-message", containerFactory = "jmsListenerContainerFactory")
public void dealDelayMessage(String message) {
    SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS");
    logger.info("delay-message 收到消息： {}, timestamp：{}", message, dateFormat.format(new Date()));
}
```



### 测试

最终运行效果如下：

![](https://gitee.com/sysker/picBed/raw/master/images/20220103174200.png)

可以看到我发送的消息在`1`分钟在之后才被消费，当我们将时间改成`5`，那么我们的消息在发送`5`分钟后才会被消费：

![](https://gitee.com/sysker/picBed/raw/master/images/20220103191710.png)

### 结语