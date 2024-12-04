# ActiveMQ简单示例



## 前言

随着互联网开发模式的不断普及，同时也伴随着移动互联网的不断发展，给用户发送消息成为每一款应用都必不可少的组件之一，想想你的淘宝、微信、钉钉，你日常生活中肯定收到过很多很多的消息。当然，这也是为了提高用户体验，及时告知用户业务办理结果，给用户推送消息这样的功能需求自然也是必不可少（但是现在垃圾信息确实太多了）。正是在这样的背景之下，消息队列这样的组件应运而生，这样的组件不仅满足多端消息发送的需求，同时还可以作为服务器削峰去谷，降低系统压力。今天我们就来简单了解一端广泛应用的消息队列组件——`ActiveMQ`。



## ActiveMQ

### ActiveMq什么

百度百科的介绍很简单，但也说明了`activeMq`的特性：

> **Apache ActiveMQ**是[Apache软件基金会](https://baike.baidu.com/item/Apache软件基金会)所研发的开放源代码[消息中间件](https://baike.baidu.com/item/消息中间件)；由于ActiveMQ是一个纯[Java](https://baike.baidu.com/item/Java)程序，因此只要[操作系统](https://baike.baidu.com/item/操作系统)支持[Java虚拟机](https://baike.baidu.com/item/Java虚拟机)，ActiveMQ便可执行。
>
> - 支持[Java消息服务](https://baike.baidu.com/item/Java消息服务)(JMS) 1.1 版本
> - [Spring Framework](https://baike.baidu.com/item/Spring Framework)
> - 集群 (Clustering)
> - 支持的[编程语言](https://baike.baidu.com/item/编程语言)包括：[C](https://baike.baidu.com/item/C)、[C++](https://baike.baidu.com/item/C%2B%2B)、[C#](https://baike.baidu.com/item/C%23)、[Delphi](https://baike.baidu.com/item/Delphi)、[Erlang](https://baike.baidu.com/item/Erlang)、[Adobe Flash](https://baike.baidu.com/item/Adobe Flash)、[Haskell](https://baike.baidu.com/item/Haskell)、[Java](https://baike.baidu.com/item/Java)、[JavaScript](https://baike.baidu.com/item/JavaScript)、[Perl](https://baike.baidu.com/item/Perl)、[PHP](https://baike.baidu.com/item/PHP)、[Pike](https://baike.baidu.com/item/Pike)、[Python](https://baike.baidu.com/item/Python)和[Ruby](https://baike.baidu.com/item/Ruby)
> - 协议支持包括：OpenWire、[REST](https://baike.baidu.com/item/REST)、STOMP、WS-Notification、MQTT、[XMPP](https://baike.baidu.com/item/XMPP)以及AMQP [1]

当然，作为一个开发组件，对我们而言最重要的就是如何使用它，至于它的特性以及底层的原理，不再我们目前的讨论范围，下来我们来看下如何安装、部署它。

### 安装

这一块的内容就太简单了，但由于这是一篇科普类文字，所以我就稍微罗嗦一点。但是我个人觉得，只要你个人动手能力不是特别弱鸡，那你大概看下官方文档，应该都可以安装好，而且现在的组件都大同小异，不用看文档你也能大概部署起来，无非就是找到`bin`文件夹，找到启动脚本，找到`config`文件夹，看下配置，然后先试启动下，一般都可以正常启动了，这些我觉得应该是作为一个开发人员的最基本修养，如果还不具备的小伙伴该好好面壁反思下了。

#### 下载

访问官方网站，选择对应的版本，然后下载

```
https://activemq.apache.org/
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210424121057.png)

这里我选择`classic`，也就是主流版本，`Artemis`是下一代的`ActiveMQ`，类似于开发版。



#### 安装

现在的开发组件，都是解压即用的

#### 启动

进入`bin`目录，直接双击运行，这时候我们会看到，有个`cmd`窗口一闪而过，说明报错了，这时候我们打开`cmd`，这里有个小技巧，在当前文件夹直接输入`cmd`即可打开`cmd`窗口：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210424121819.png)

然后我们在`cmd`中再次执行`activemq.bat`，这时候会发现，`cmd`中回显如下提示信息

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210424122125.png)

根据提示信息，我们知道之前没有添加参数(`Usage`才是最好的文档，一定要习惯命令行，没看明白的小伙伴继续面壁)，这时候我们知道启动的命令应该是这样的：

```
activemq.bat start
```

回车键入，完美启动：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210424122545.png)

#### 测试

我们在浏览器打开如下地址，如果正常访问，说明`ActiveMQ`启动没有任何问题：

```
localhost:8161
```

用户名和密码都是`admin`，如何修改我们后面再说：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210424122724.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210424122927.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210424122956.png)

这时候，我们的`ActiveMQ`就正常启动了。

#### docker安装activemq

这里我们再补充下`docker`环境下，如何安装`activemq`，很简单只需要两行命令即可：

```sh
$ docker pull webcenter/activemq:latest # 拉取最新版本的activemq
$ docker run -d --name myactivemq -p 61616:61616 -p 8161:8161 webcenter/activemq:latest # 启动
```

关于`docker`的使用，我们前面已经讲过了，还想要了解的小伙伴可以翻一下前面的内容。

### java整合ActiveMQ

#### 创建java项目

这里我们创建一个`java`项目，简单测试下`ActiveMQ`，创建`maven`项目，引入如下依赖：

```XML
<dependency>
    <groupId>org.apache.activemq</groupId>
    <artifactId>activemq-all</artifactId>
    <version>5.13.4</version>
</dependency>
```

#### 创建消息生产者

下面代码中的注释已经够详细了，需要注意的是`session.createQueue("test-queue")`中的`test-queue`是我们要发送消息的目标队列的名称，消费者也必须是一样的名称，才能正常消费消息，否则是没有办法消费的。

`session.createTextMessage("hello!test-queue")`是发送消息，这里的`"hello!test-queue`是我们发送的消息内容。

```java
/**
 *
 * 消息生产者
 *
 * @author syske
 * @version 1.0
 * @date 2021-04-24 10:20:22
 */
public class ActiveMqProducer {

    public void mQProducerQueue() throws Exception{
        //1、创建工厂连接对象，需要制定ip和端口号，这里的端口就是activemq的端口，后面我们再来说如何配置
        ConnectionFactory connectionFactory = new ActiveMQConnectionFactory("tcp://127.0.0.1:61616");
        //2、使用连接工厂创建一个连接对象
        Connection connection = connectionFactory.createConnection();
        //3、开启连接
        connection.start();
        //4、使用连接对象创建会话（session）对象
        Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        //5、使用会话对象创建目标对象，包含queue和topic（一对一和一对多）
        Queue queue = session.createQueue("test-queue");
        //6、使用会话对象创建生产者对象
        MessageProducer producer = session.createProducer(queue);
        //7、使用会话对象创建一个消息对象
        TextMessage textMessage = session.createTextMessage("hello!test-queue");
        //8、发送消息
        producer.send(textMessage);
        //9、关闭资源
        producer.close();
        session.close();
        connection.close();
    }
}
```

#### 创建消息消费者

基本上和消息生产的代码一致，最大的区别在于消费者这里创建的是消费者`session.createConsumer(queue)`，同时启动了一个消息监听器，实时监听指定队列，只要队列中有消息进来，消费者就会执行`MessageListener`中的操作，将消息消费掉，这里的写法采用了兰姆达表达式

```java
**
 *
 * 消息消费者
 *
 * @author syske
 * @version 1.0
 * @date 2021-04-24 10:22:21
 */
public class ActiveMqConsumer {
    public void mQConsumerQueue() throws Exception{
        //1、创建工厂连接对象，需要制定ip和端口号
        ConnectionFactory connectionFactory = new ActiveMQConnectionFactory("tcp://127.0.0.1:61616");
        //2、使用连接工厂创建一个连接对象
        Connection connection = connectionFactory.createConnection();
        //3、开启连接
        connection.start();
        //4、使用连接对象创建会话（session）对象
        Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        //5、使用会话对象创建目标对象，包含queue和topic（一对一和一对多）
        Queue queue = session.createQueue("test-queue");
        //6、使用会话对象创建生产者对象
        MessageConsumer consumer = session.createConsumer(queue);
        //7、向consumer对象中设置一个messageListener对象，用来接收消息
        consumer.setMessageListener(message-> {
            // TODO Auto-generated method stub
            if(message instanceof TextMessage){
                TextMessage textMessage = (TextMessage)message;
                try {
                    System.out.println("消息内容：" + textMessage.getText());
                } catch (JMSException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
        });
        //8、程序等待接收用户消息
        System.in.read();
        //9、关闭资源
        consumer.close();
        session.close();
        connection.close();
    }
}
```

#### 测试

##### 生产者测试

首先我们启动消费者，生产消息

```java
/**
     * 生产消息
     *
     * @throws Exception
     */
    @Test
    public void produceMessage() throws Exception {
        new ActiveMqProducer().mQProducerQueue();
    }    
```

运行上面的测试代码，然后打开`ActiveMQ`的管理页面，我们会看到，多了一个消息队列：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210424142711.png)

消息队列名称就是我们上面指定的`test-queue`，待消费消息（`pending`）数量`1`，因为我们暂时没有启动消费者（`consumer`），所以消费者数量是`0`，队列中排队的消息（`enqueued`）数量`1`，被消费消息（`dequeued`）数量`0`。如果你再次启动生产者，消息队列中的数据会变成`2`:

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210424143521.png)

##### 消费者测试

这时候，我们启动消费者

```java
/**
    * 消费消息
    * @throws Exception
    */
    @Test
    public void testConsumeMessage() throws Exception {
        new ActiveMqConsumer().mQConsumerQueue();
    }
```

然后我们会看到控制台输出如下信息：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210424143725.png)

这些消息就是我们在生产者中发送的消息。我们再访问队列管理页面看一下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210424143937.png)

和上面消费者启动之前相比，消息已经被消费，未消费消息数量`0`，以消费`2`，消费者数量`1`。

#### 扩展

一般在实际项目中，我们会启动异步线程发送消息（消息生产者），然后由消息中心集中对消息进行消费，并将消息推送至客户端，比如微信公众号、钉钉、安卓端、`IOS`端等。需要注意的是，不要在循环中调用异步线程，否则会导致线程池资源耗尽报错，而且这种错误本地和测试环境很难复现。

我最近刚处理和优化的一个问题就是`for`循环中调用了异步发送消息的方法，导致线程池资源耗尽报错，但是本地和测试一直无法复现错误，直到最后在异步线程方法中加了`sleep`之后`bug`才复现，当然也说明线上环境复杂，消息队列响应慢，所以为了避免这类情况出现，一定在写代码的时候要尽可能规范合理，毕竟本地没问题不代表线上没问题，并发量为`10`的时候，接口一切响应正常，但是如果并发量发生量级变化，变成`100`甚至`1000`，性能问题就出现了。

### 配置

这里我们再简单说下`activemq`的配置，进入`conf`文件夹，可以看到如下文件：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210424145808.png)

##### 端口配置

其中，端口的配置在`jetty.xml`中：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210424150224.png)

##### 管理账户配置

管理用户配置在`jetty-realm.properties`中，配置规则也很简单:

用户名: 密码， 角色

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210424150554.png)

##### 其他配置

剩余的文件都是有关登录验证的配置，比如`jaas`、`credentials`，暂时未涉及，这里也就不做探讨，等后面了解之后再来分享。

## 结语

今天的内容已经比较完整地介绍了`activemq`的基础内容，包括下载、安装、配置以及项目整合，就算之前没接触过`activemq`的小伙伴，通过今天的内容，我想你也应该对`activemq`有了基本的认知，基本上可以确保在工作中用到`activemq`的时候，你可以很好地上手。当然，今天的内容，也算是我最近一段时间学习`activemq`的一个简单总结，后面还需要进一步的深入学习和探索。

最后，再给各个小伙伴一个建议，学习的时候要尽可能多看官方文档，多留意提示信息，多横向比较，多做延申，多积累，要慢慢培养自己系统的学习思维和习惯，提升自己知识横向扩展能力，定期做知识的归纳整理，将知识点连成知识链，再将知识链链接形成知识面，这样随着你知识面的不断扩展，你会发现你学东西的时候效率会更好，学东西会更快，而且学习质量也更高，毕竟大脑更擅长的是关联，而不是记忆。另外，就算大脑是个数据库，那你也应该知道，建立索引，我们的知识才可以更快速地被检索，所以管理知识，其实比学习知识更重要。