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

然后我们就可以开始今天示例内容了。首先我们来看最原始的方式。这里最核心的操作是`setLongProperty`，也就是设置消息的延迟时间，这里我设置的延迟消费时间是`1`分钟，也就是说我通过该方法发送的消息会延迟一分钟之后才会被消费。

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



### 测试

![](https://gitee.com/sysker/picBed/raw/master/images/20220103174200.png)

### 结语