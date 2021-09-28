# rocketMQ简单示例

## 前言

在微服务遍地开花的今天，消息队列的应用特别广泛，但在此之前，我对消息队列的认知仅仅停留在是什么和能干什么的认知，没有使用过任何一款消息队列，对它的实际应用也没有任何认知，但是从现在市场上的技术情况来说，消息队列已经是一个`web`后端开发必须掌握的核心组件之一，所以我就利用空闲时间来了解下，今天我们分享的是`rocketMQ`，同样也是阿里巴巴开源的一个组件，2016年阿里巴巴把它捐赠给了`Apache`开源基金会，目前是该基金会的顶级项目之一。



## 正文

在开始正文之前，我们先来看下消息队列的一些知识。

### 什么是消息队列

消息队列简单来讲，它就类似于存放消息的容器，消息生产者将消息放入消息队列中，消费者从消息队列中拿出消息进行消费（比如写订单）。消息队列是分布式系统中重要的组件，使用消息队列主要是为了通过异步处理提高系统性能和削峰、降低系统耦合性。目前使用较多的消息队列有`ActiveMQ`，`RabbitMQ`，`Kafka`，`RocketMQ`。

### 为什么需要消息队列

#### 削峰填谷，降低系统瞬时峰值并发量

随着互联网业务需求的不断发展，传统的架构模式已经无法满足需求，特别是在电商业务大发展的当下更是如此。为了应对这种百万并发、千万并发甚至亿级数量的并发，这种并发模式的特点是并发量集中出现在某一时间段，比如双十一、双十二或者促销、打折日，而其他时间的并发量是峰值并发量的十分之一，甚至百分之一，如果按照峰值的并发量来设计系统架构，不仅初投资大耗费巨资，而且在日常运行维护也很烧钱。为了平衡这两种情况下的并发量，同时降低系统建设成本，消息队列这样的系统组件应运而生。

简单来说，消息队列就是一种平衡系统并发量的系统组件，主要的作用就是削峰填谷。我们假设这张图中红色表示没有加入消息队列组件的系统并发时序图（这里的图是随意画的，只是为了说明问题），蓝色表示架构中加入了消息队列组件：

![](https://gitee.com/sysker/picBed/raw/master/20210309225021.png)



对比之后我们会发现，我们发现引入消息队列组件之后，降低了订单系统的峰值并发量，就相当于我们将一部分峰值请求的业务处理，放在系统压力小时去处理，当然实际过程中订单系统一直在有条不紊地处理消息队列中的订单信息，直到所有订单处理完成。当然，它主要是针对一些实时性要求不强但并发量大的业务，比如购票、抢购下单等允许稍后推送处理结果的业务。

#### 降低系统之间的耦合性，提高用户体验

我们来想象这样一个应用场景，我们要做一个购票系统，购票成功后要短信告知用户购票结果，如果采用串行方式（也就是同步调用），我们的调用方式是这样的：用户提交购票订单后，订单系统受理购票订单后，调用短信系统发送购票结果。这里我们放一个图，大家就更清楚了：

![](https://gitee.com/sysker/picBed/raw/master/20210310204920.png)

串行架构下系统的响应时间是`150ms` + `150ms`，需要`300ms`，从业务流程上来说，订单受理成功后发送购票结果，这没有什么问题，但是如果短信系统在某个时间段内系统宕机，短信服务不可用，购票短信无法发送，最终导致的结果是用户是无法下单的，不仅影响用户体验，也影响公司的业务受益。

而且再深入分析下这个业务流程，你会发现短信是否发送与用户提交订单的操作是没有关系的，用户需要知道的只是它的订单是否处理成功，至于发送购票成结果的短信，对整个业务而言并发核心业务，就算短信发送失败，也不应该影响购票业务。

所以，我们更合理的业务处理方式是，订单系统受理成功后，直接将受理结果返回给用户，至于订单的处理结果，可以等整个业务完成后生成，然后订单系统向短信系统发送订单处理结果的消息，短信系统收到消息后给给用户发购票结果，这里我们存放消息的容器就是消息队列，这时候我们的系统机构是这样的：

![](https://gitee.com/sysker/picBed/raw/master/20210310204748.png)

上面这种架构中，我们发送短信的业务是异步的，这样不仅可以减少用户等待的时间，提高服务的响应效率，如果省去短信系统的处理时间，那么最终业务的响应时间就缩减为`150ms`，而且这种架构下系统的耦合性更低，比如如果未来业务需求发送变化，不仅需要给用户发送短信，还要将结果推送到微信公众号，业务耗时`100ms`，甚至还需要将结果以邮件的方式发送到用户，业务耗时`150ms`，如果还是第一种架构模式，那用户要等待的响应时长是`150ms` + `150ms` + `100ms` + `150ms`，但对第二种架构，用户的响应时间始终是`150ms`：

![](https://gitee.com/sysker/picBed/raw/master/20210310210550.png)

### RocketMQ入门

#### rocketMQ是什么



#### 下载

目前最新的版本是`4.8`，下面传送门：

```
https://www.apache.org/dyn/closer.cgi?path=rocketmq/4.8.0/rocketmq-all-4.8.0-source-release.zip
```

![](https://gitee.com/sysker/picBed/raw/master/20210310225037.png)

点击上图的地址，红框内的地址是推荐的国内的镜像地址，下载比较快

#### 安装

解压下载的`zip`文件

##### windows

直接压缩软件解压即可

##### linux

```sh
> unzip rocketmq-all-4.8.0-source-release.zip
> cd rocketmq-all-4.8.0/
> mvn -Prelease-all -DskipTests clean install -U
> cd distribution/target/rocketmq-4.8.0/rocketmq-4.8.0
```

#### 设置环境变量

这里`windows`需要设置，`Linux`并不需要，当然我也没有在`Linux`环境下测试，有兴趣的小伙伴自己去试验。在`windows`添加如下环境变量：

```sh
ROCKETMQ_HOME="D:\workspace\tools\rocketmq-all-4.8.0-bin-release"
NAMESRV_ADDR="localhost:9876"
```

![](https://gitee.com/sysker/picBed/raw/master/20210310230554.png)

![](https://gitee.com/sysker/picBed/raw/master/images/20210928104351.png)

或者在启动前的`powershell`窗口里设置，这里是临时，每次都要设置，嫌麻烦的直接设置永久的:

```shell
$Env:ROCKETMQ_HOME="D:\workspace\tools\rocketmq-all-4.8.0-bin-release"
$Env:NAMESRV_ADDR="localhost:9876"
```



#### 启动

##### 启动Name服务

**linux**

```
  > nohup sh bin/mqnamesrv &
  > tail -f ~/logs/rocketmqlogs/namesrv.log
  The Name Server boot success...
```

**windows**

打开`powershell`，如果没有设置环境环境变量需要先执行下面的操作，进行环境变量设置

```sh
$Env:ROCKETMQ_HOME="D:\workspace\tools\rocketmq-all-4.8.0-bin-release"
$Env:NAMESRV_ADDR="localhost:9876"
```

然后进入`rocketMQ`安装目录，执行如下操作

```sh
cd D:\workspace\tools\rocketmq-all-4.8.0-bin-release
.\bin\mqnamesrv.cmd
```

![](https://gitee.com/sysker/picBed/raw/master/20210310231630.png)

![](https://gitee.com/sysker/picBed/raw/master/20210310231743.png)

##### 启动代理服务

**Linux**

```sh
  > nohup sh bin/mqbroker -n localhost:9876 &
  > tail -f ~/logs/rocketmqlogs/broker.log 
  The broker[%s, 172.30.30.233:10911] boot success...
```

**windows**

和上面启动`Name`服务一样，没设置环境需要先执行前面两行环境变量设置的操作

```sh
$Env:ROCKETMQ_HOME="D:\workspace\tools\rocketmq-all-4.8.0-bin-release"
$Env:NAMESRV_ADDR="localhost:9876"
```

然后执行启动操作

```sh
cd D:\workspace\tools\rocketmq-all-4.8.0-bin-release
.\bin\mqbroker.cmd -n localhost:9876 autoCreateTopicEnable=true
```

操作之前，一定要进入`rocketMQ`安装目录，否则回报如下红色错误

![](https://gitee.com/sysker/picBed/raw/master/20210310232411.png)



#### 接收&发送消息

##### 发送消息

**Linux**

```sh
> export NAMESRV_ADDR=localhost:9876
 > sh bin/tools.sh org.apache.rocketmq.example.quickstart.Producer
 SendResult [sendStatus=SEND_OK, msgId= ...
```

**windows**

同样的，没设置环境变量的记得先设置，嫌麻烦就直接设置永久的环境变量，参照**设置环境变量**

```sh
cd D:\workspace\tools\rocketmq-all-4.8.0-bin-release
.\bin\tools.cmd  org.apache.rocketmq.example.quickstart.Producer
```

执行命令后，会看到我们向消息队列中发送了很多消息

![](https://gitee.com/sysker/picBed/raw/master/20210310233023.png)

##### 接收消息

**Linux**

```sh
 > sh bin/tools.sh org.apache.rocketmq.example.quickstart.Consumer
 ConsumeMessageThread_%d Receive New Messages: [MessageExt...
```

**windows**

同样的，没设置环境变量的记得先设置

```sh
cd D:\workspace\tools\rocketmq-all-4.8.0-bin-release
.\bin\tools.cmd  org.apache.rocketmq.example.quickstart.Consumer
```

执行上面命令后，可以看到控制台接收到刚才发送的消息

![](https://gitee.com/sysker/picBed/raw/master/20210310233327.png)



#### Java简单demo

这里的`demo`在官网都可以看到，也都很简单，需要补充说明的，我会停下来解释。开始项目之前，先引入如下依赖：

```xml
<dependency>
	<groupId>org.apache.rocketmq</groupId>
	<artifactId>rocketmq-client</artifactId>
	<version>4.3.0</version>
</dependency>
```



##### 发送同步消息

```java
import org.apache.rocketmq.client.producer.DefaultMQProducer;
import org.apache.rocketmq.client.producer.SendResult;
import org.apache.rocketmq.common.message.Message;
import org.apache.rocketmq.remoting.common.RemotingHelper;

/**
 * @program: rocketmq-demo
 * @description: 发送同步消息
 * @author: syske
 * @create: 2021-03-09 20:24
 */
public class SyncProducer {
    public static void main(String[] args) throws Exception {
        // 实例化消息生产者Producer
        DefaultMQProducer producer = new DefaultMQProducer("please_rename_unique_group_name");
        // 设置NameServer的地址
        producer.setNamesrvAddr("localhost:9876");
        // 启动Producer实例
        producer.start();
        for (int i = 0; i < 100; i++) {
            // 创建消息，并指定Topic，Tag和消息体
            Message msg = new Message("TopicTest" /* Topic */,
                    "TagA" /* Tag */,
                    ("Hello RocketMQ " + i).getBytes(RemotingHelper.DEFAULT_CHARSET) /* Message body */
            );
            // 发送消息到一个Broker
            SendResult sendResult = producer.send(msg);
            // 通过sendResult返回消息是否成功送达
            System.out.printf("%s%n", sendResult);
        }
        // 如果不再发送消息，关闭Producer实例。
        producer.shutdown();
    }
}
```

##### 发送异步消息

```java
import org.apache.rocketmq.client.producer.DefaultMQProducer;
import org.apache.rocketmq.client.producer.SendCallback;
import org.apache.rocketmq.client.producer.SendResult;
import org.apache.rocketmq.common.CountDownLatch2;
import org.apache.rocketmq.common.message.Message;
import org.apache.rocketmq.remoting.common.RemotingHelper;

import java.util.concurrent.TimeUnit;

/**
 * @program: rocketmq-demo
 * @description: 异步消息生产者
 * @author: syske
 * @create: 2021-03-09 20:28
 */
public class AsyncProducer {
    public static void main(String[] args) throws Exception {
        // 实例化消息生产者Producer
        DefaultMQProducer producer = new DefaultMQProducer("please_rename_unique_group_name");
        // 设置NameServer的地址
        producer.setNamesrvAddr("localhost:9876");
        // 启动Producer实例
        producer.start();
        producer.setRetryTimesWhenSendAsyncFailed(0);

        int messageCount = 100;
        // 根据消息数量实例化倒计时计算器
        final CountDownLatch2 countDownLatch = new CountDownLatch2(messageCount);
        for (int i = 0; i < messageCount; i++) {
            final int index = i;
            // 创建消息，并指定Topic，Tag和消息体
            Message msg = new Message("TopicTest",
                    "TagA",
                    "OrderID188",
                    "Hello world".getBytes(RemotingHelper.DEFAULT_CHARSET));
            // SendCallback接收异步返回结果的回调
            producer.send(msg, new SendCallback() {
                @Override
                public void onSuccess(SendResult sendResult) {
                    System.out.printf("%-10d OK %s %n", index,
                            sendResult.getMsgId());
                }
                @Override
                public void onException(Throwable e) {
                    System.out.printf("%-10d Exception %s %n", index, e);
                    e.printStackTrace();
                }
            });
        }
        // 等待5s
        countDownLatch.await(5, TimeUnit.SECONDS);
        // 如果不再发送消息，关闭Producer实例。
        producer.shutdown();
    }
}
```



##### 发送单向消息

单向消息就是没有返回值的消息

```java
import org.apache.rocketmq.client.producer.DefaultMQProducer;
import org.apache.rocketmq.common.message.Message;
import org.apache.rocketmq.remoting.common.RemotingHelper;

/**
 * @program: rocketmq-demo
 * @description: 单向消息生产者
 * @author: syske
 * @create: 2021-03-09 20:30
 */
public class OnewayProducer {
    public static void main(String[] args) throws Exception{
        // 实例化消息生产者Producer
        DefaultMQProducer producer = new DefaultMQProducer("please_rename_unique_group_name");
        // 设置NameServer的地址
        producer.setNamesrvAddr("localhost:9876");
        // 启动Producer实例
        producer.start();
        for (int i = 0; i < 100; i++) {
            // 创建消息，并指定Topic，Tag和消息体
            Message msg = new Message("TopicTest" /* Topic */,
                    "TagA" /* Tag */,
                    ("Hello RocketMQ " + i).getBytes(RemotingHelper.DEFAULT_CHARSET) /* Message body */
            );
            // 发送单向消息，没有任何返回结果
            producer.sendOneway(msg);

        }
        // 如果不再发送消息，关闭Producer实例。
        producer.shutdown();
    }
}
```

##### 消息消费者

```java
import org.apache.rocketmq.client.consumer.DefaultMQPushConsumer;
import org.apache.rocketmq.client.consumer.listener.ConsumeConcurrentlyContext;
import org.apache.rocketmq.client.consumer.listener.ConsumeConcurrentlyStatus;
import org.apache.rocketmq.client.consumer.listener.MessageListenerConcurrently;
import org.apache.rocketmq.client.exception.MQClientException;
import org.apache.rocketmq.common.message.MessageExt;

import java.util.List;

/**
 * @program: rocketmq-demo
 * @description: 消息消费者
 * @author: syske
 * @create: 2021-03-09 20:26
 */
public class Consumer {
    public static void main(String[] args) throws InterruptedException, MQClientException {

        // 实例化消费者
        DefaultMQPushConsumer consumer = new DefaultMQPushConsumer("please_rename_unique_group_name");

        // 设置NameServer的地址
        consumer.setNamesrvAddr("localhost:9876");

        // 订阅一个或者多个Topic，以及Tag来过滤需要消费的消息
        consumer.subscribe("TopicTest", "*");
        // 注册回调实现类来处理从broker拉取回来的消息
        consumer.registerMessageListener(new MessageListenerConcurrently() {
            @Override
            public ConsumeConcurrentlyStatus consumeMessage(List<MessageExt> msgs, ConsumeConcurrentlyContext context) {
                System.out.printf("%s Receive New Messages: %s %n", Thread.currentThread().getName(), msgs);
                // 标记该消息已经被成功消费
                return ConsumeConcurrentlyStatus.CONSUME_SUCCESS;
            }
        });
        // 启动消费者实例
        consumer.start();
        System.out.printf("Consumer Started.%n");
    }
}
```

##### 发送顺序消息

顺序消息简单来说，就是消费者的消费顺序和生产者生产顺序是一致的，比如对下面代码中的`创建订单`，消费的时候肯定是先消费`创建1`，然后是`创建2`，再是`创建3`，这里的是区分是否是同一类消息，是通过`Message`的`tag`属性的值来判断的。关于顺序消息借用网上的一个图来说明吧：

![](https://gitee.com/sysker/picBed/raw/master/20210310234923.png)

```java
import org.apache.rocketmq.client.producer.DefaultMQProducer;
import org.apache.rocketmq.client.producer.SendResult;
import org.apache.rocketmq.common.message.Message;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

/**
 * @program: rocketmq-demo
 * @description: 顺序消息生产
 * @author: syske
 * @create: 2021-03-09 20:35
 */
public class Producer {
    public static void main(String[] args) throws Exception {
        DefaultMQProducer producer = new DefaultMQProducer("order_group_1");

        producer.setNamesrvAddr("127.0.0.1:9876");

        producer.start();

        String[] tags = new String[]{"TagA", "TagC", "TagD"};

        // 订单列表
        List<OrderStep> orderList = new Producer().buildOrders();

        Date date = new Date();
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        String dateStr = sdf.format(date);
        for (int i = 0; i < 10; i++) {
            // 加个时间前缀
            String body = dateStr + " Hello RocketMQ " + orderList.get(i);
            Message msg = new Message("TopicTest", tags[i % tags.length], "KEY" + i, body.getBytes());

            SendResult sendResult = producer.send(msg, (mqs, msg1, arg) -> {
                Long id = (Long) arg;  //根据订单id选择发送queue
                long index = id % mqs.size();
                return mqs.get((int) index);
            }, orderList.get(i).getOrderId());//订单id

            System.out.println(String.format("SendResult status:%s, queueId:%d, body:%s",
                    sendResult.getSendStatus(),
                    sendResult.getMessageQueue().getQueueId(),
                    body));
        }

        producer.shutdown();
    }

    /**
     * 订单的步骤
     */
    private static class OrderStep {
        private long orderId;
        private String desc;

        public long getOrderId() {
            return orderId;
        }

        public void setOrderId(long orderId) {
            this.orderId = orderId;
        }

        public String getDesc() {
            return desc;
        }

        public void setDesc(String desc) {
            this.desc = desc;
        }

        @Override
        public String toString() {
            return "OrderStep{" +
                    "orderId=" + orderId +
                    ", desc='" + desc + '\'' +
                    '}';
        }
    }

    /**
     * 生成模拟订单数据
     */
    private List<OrderStep> buildOrders() {
        List<OrderStep> orderList = new ArrayList<OrderStep>();

        OrderStep orderDemo = new OrderStep();
        orderDemo.setOrderId(15103111039L);
        orderDemo.setDesc("创建1");
        orderList.add(orderDemo);

        orderDemo = new OrderStep();
        orderDemo.setOrderId(15103111065L);
        orderDemo.setDesc("创建2");
        orderList.add(orderDemo);

        orderDemo = new OrderStep();
        orderDemo.setOrderId(15103111039L);
        orderDemo.setDesc("付款1");
        orderList.add(orderDemo);

        orderDemo = new OrderStep();
        orderDemo.setOrderId(15103117235L);
        orderDemo.setDesc("创建3");
        orderList.add(orderDemo);

        orderDemo = new OrderStep();
        orderDemo.setOrderId(15103111065L);
        orderDemo.setDesc("付款2");
        orderList.add(orderDemo);

        orderDemo = new OrderStep();
        orderDemo.setOrderId(15103117235L);
        orderDemo.setDesc("付款3");
        orderList.add(orderDemo);

        orderDemo = new OrderStep();
        orderDemo.setOrderId(15103111065L);
        orderDemo.setDesc("完成1");
        orderList.add(orderDemo);

        orderDemo = new OrderStep();
        orderDemo.setOrderId(15103111039L);
        orderDemo.setDesc("推送1");
        orderList.add(orderDemo);

        orderDemo = new OrderStep();
        orderDemo.setOrderId(15103117235L);
        orderDemo.setDesc("完成2");
        orderList.add(orderDemo);

        orderDemo = new OrderStep();
        orderDemo.setOrderId(15103111039L);
        orderDemo.setDesc("完成3");
        orderList.add(orderDemo);

        return orderList;
    }
}
```

##### 顺序消息消费者

```java

import org.apache.rocketmq.client.consumer.DefaultMQPushConsumer;
import org.apache.rocketmq.client.consumer.listener.ConsumeOrderlyContext;
import org.apache.rocketmq.client.consumer.listener.ConsumeOrderlyStatus;
import org.apache.rocketmq.client.consumer.listener.MessageListenerOrderly;
import org.apache.rocketmq.common.consumer.ConsumeFromWhere;
import org.apache.rocketmq.common.message.MessageExt;

import java.util.List;
import java.util.Random;
import java.util.concurrent.TimeUnit;

/**
 * @program: rocketmq-demo
 * @description: 顺序消息消费者
 * @author: syske
 * @create: 2021-03-09 20:37
 */
public class ConsumerInOrder {
    public static void main(String[] args) throws Exception {
        DefaultMQPushConsumer consumer = new DefaultMQPushConsumer("order_group_3");
        consumer.setNamesrvAddr("127.0.0.1:9876");
        /**
         * 设置Consumer第一次启动是从队列头部开始消费还是队列尾部开始消费<br>
         * 如果非第一次启动，那么按照上次消费的位置继续消费
         */
        consumer.setConsumeFromWhere(ConsumeFromWhere.CONSUME_FROM_FIRST_OFFSET);

        consumer.subscribe("TopicTest", "TagA || TagC || TagD");

        consumer.registerMessageListener(new MessageListenerOrderly() {

            Random random = new Random();

            @Override
            public ConsumeOrderlyStatus consumeMessage(List<MessageExt> msgs, ConsumeOrderlyContext context) {
                context.setAutoCommit(true);
                for (MessageExt msg : msgs) {
                    // 可以看到每个queue有唯一的consume线程来消费, 订单对每个queue(分区)有序
                    System.out.println("consumeThread=" + Thread.currentThread().getName() + "queueId=" + msg.getQueueId() + ", content:" + new String(msg.getBody()));
                }

                try {
                    //模拟业务逻辑处理中...
                    TimeUnit.SECONDS.sleep(random.nextInt(10));
                } catch (Exception e) {
                    e.printStackTrace();
                }
                return ConsumeOrderlyStatus.SUCCESS;
            }
        });

        consumer.start();

        System.out.println("Consumer Started.");
    }
}
```

 

## 结语

这篇文章，从昨天写到今天，今天在完善内容的时候，写到了我们最近服务升级的一次翻车事故，由于篇幅问题我把它单独抽出来了，有兴趣的小伙伴去看看吧，看我们咋翻车的，还有我们的血泪教训。

在今天的内容中，我们主要介绍了什么是消息队列、消息队列的作用，以及`rocketMQ`的安装部署和它的`java`示例。因为目前，我也在学习和研究，所以就先分享到这里，后面等我深入了解之后再来分享，主要是现在已经不早了，再六分钟午夜十二点，晚安吧！



[^参考1]: https://www.jianshu.com/p/36a7775b04ec
[^参考2]: http://www.dockone.io/article/9726

