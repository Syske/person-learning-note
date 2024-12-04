# spring-boot整合activeMQ实现异步延迟消费

### 前言

最近，有一个需求，就是在用户发起第一步操作之后，需要在一个固定时间之后触发另一个操作（比如半小时之后），虽然通过定时任务也能实现，但是考虑到用户数量庞大，每个用户的时间又不相同，同时考虑到服务重启之后数据不会丢失，所以几经权衡之后，我们最终决定采用`activeMQ`异步延迟的方式，其好处也很明显：

首先，原有系统中已经有了`MQ`异步处理业务的实现（不过延迟消费的还没有），不需要向系统中引入的新的组件，不会改变系统复杂程度，但是引入大规模的定时任务就很难说，而且考虑到线上的多节点部署，定时器也存在很多问题；

其次，`MQ`消息本身可以实现序列化，而且由于`ACK`（消息确认）的加持，可以确保消息不丢失，这样就算服务重启，相关业务也不会受到太大影响。

由于目前线上环境我们用的是`ActiveMQ`，所以今天我们就来通过一个简单的示例，来看下如何通过`ActiveMQ`来实现我们今天的需求。



### activeMQ

首先需要注意的是，`activeMQ`是从`5.4`才开始支持延迟消费的，所以想要实现今天的示例，你的`activeMQ`的版本至少是`5,4`，我本次示例用到的是`5.16.2`:

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220103221617.png)

#### 配置

确认`activeMQ`的版本之后，我们还需要修改`conf/activemq.xml`文件，修改的内容也很简单，只需要找到`broker`配置标签，在其中加入` schedulerSupport="true"`即可，不需要其他配置：

```xml
<broker xmlns="http://activemq.apache.org/schema/core" brokerName="localhost" dataDirectory="${activemq.data}" schedulerSupport="true">
<!-- 标签内配置不需要改动 -->
     ...

</broker>
```

完成该配置之后，重启`activeMQ`之后就可以创建我们的项目了。



### spring-boot

这里先要创建`spring boot`项目，然后还需要简单配置下`MQ`，具体的配置和整合就不再细说，不清楚的小伙伴可以看下我之前分享的内容：



https://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648418144&idx=1&sn=fd53a4456a246f3ee88d7de74f466cda&chksm=bea6c9ea89d140fc9cec281063442df7058e756fd3c87a31b30631aa67f823b452f2211c4cd5&token=1044120974&lang=zh_CN#rd

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/face-img-ae667680ae554f118f5d2f840442b43e.jpg)

这里的内容完成之后，我们就可以开始今天示例最核心的内容了。

#### 最原始方式

首先我们来看最原始的方式，当然这也不能算是最原始的方式，毕竟这里还是通过`jmsTemplate`获取了连接工厂，不过注释那里我也写了最原始的方式：

```java
public void sendDelayMessage(String queueName, String messageInfo) {
        Connection connection = null;
        Session session = null;
        MessageProducer producer = null;
        // ConnectionFactory connectionFactory = new ActiveMQConnectionFactory("tcp://127.0.0.1:61616");
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

这里最核心的操作是`setLongProperty`，也就是设置消息的延迟时间，这里我设置的延迟消费时间是`1`分钟，也就是说我通过该方法发送的消息会等待（延迟）一分钟之后被消费，流程简单描述如下：

- 通过`JmsMessagingTemplate`拿到`mq`的`ConnectionFactory`；

- 然后通过连接工厂拿到连接，从连接中拿到`session`信息；

- 再接着从会话中创建消息生产者，同时创建消息对象，并设置消息延迟时间；

- 最后通过生产者发送消息，提交会话事务并关闭资源。

这里可以看到，我们开启了`session`事务，这样可以确保同一个会话发送多个消息，最终会一起成功或者一起失败，和数据库事务类似。



#### JmsTemplate

`JmsTemplate`是`spring`提供的一套`mq`连接模板，我们可以通过它来操作常用的`MQ`。下面是基于`JmsTemplate`的延迟消息实现，相比上面这种原始的写法，这里的写法更简洁，也更优雅：

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

这里我们是通过调用了`JmsTemplate`的`send`方法实现的延迟消息的，只是需要我们自己通过`lambda`的方式创建`messageCreator`，并实现它的`createMessage`方法，在`messageCreator`的`createMessage`方法中，我们只需要像第一种方式一样指定消息的延迟时间即可。

```java
send(final Destination destination, final MessageCreator messageCreator)
```

这里之所以如此简洁优雅，其实是因为`JmsBaseTemplate`已经帮我们封装了`session`之外的其他操作，包括关闭资源等：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20220103185514.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20220103190057.png)

#### 消息消费者

消费者和普通消息没有任何区别，只需要配置对应的消息队列名称即可，不一样的是，延迟消息必须等待等到设定的延迟时间之后，才会被消费：

```java
@JmsListener(destination = "delay-message", containerFactory = "jmsListenerContainerFactory")
public void dealDelayMessage(String message) {
    SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS");
    logger.info("delay-message 收到消息： {}, timestamp：{}", message, dateFormat.format(new Date()));
}
```

如果还有疑问，后面看下示例运行结果。



### 测试

不论原始方式还是`JmsTemplate`，最终的运行效果都没有本质区别，运行效果大致如下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20220103174200.png)

在测试的开始，我把延迟消费的时间设置为`1min`，可以看到我们发送的消息在`1`分钟在之后才被消费，当我们将延迟时间改成`5min`，那么我们的消息会在发送`5`分钟后会被消费：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20220103191710.png)



### 结语

今天的内容，总体来说很简单，而且技术层面也没有特别高大上的实现，但是这种有别于定时器的解决方案还是特别值得推荐的，它特别适用于那些规模特别大的异步延迟回调场景，比如定时缓存清理，再比如免打扰消息的发送，当然更多业务场景可能还需要各位小伙伴结合自己的业务场景进行进一步的分析。



##### 简单总结

作为`2022`的第一次推送，我想简单说两句。

首先是想简单总结下自己的`2021`（后面细说），过去的一年，`3~9`总体学习的内容比较多，也有较多的输出，`9`月之后逐渐忙碌，所以也就疏于学习了，总体来说还是收获不小的，特别是换了新的工作，新的环境之后（后面再详细梳理下）。



##### 新年计划

再一个就是新的一年的计划，这一块计划春节之前完成更详细的计划，我目前的经验是，目标越明确，就越容易达成，所以新的一年目标会尽可能详细、明确。

很坦诚地说，我觉得我现在依然很菜鸡，有很多东西还要学习，有很多东西还要沉淀，哪怕是现在看着掌握得还可以的技术，其实也可能只是流于表面。

基于这样的原因，在新的一年里，我会朝着三个方向继续进发：

一个是继续深挖基础，扎实多线程、算法、`JVM`等相关知识点，这些可能才是真正能提升自己技术实力的关键；

另一个是广泛扩展自己的知识面，熟悉常见的组件、解决方案等，这些都是未来激发个人创造力的关键；

最后一个是软实力提升，这块主要包括自己的思维方式、做事方法、工作技巧、个人管理等方面的提升，这一块实力的提升，很大程度上决定了我前两个目标的完成效率，这块实力提升越快，前两个目标也可以更高效完成。

好了，今天就说这么多，希望各位小可爱在新的一年里，都能达成自己的目标……加油！晚安！