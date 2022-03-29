# java发送邮件简单实现

### 前言

最近公司用一个发送邮件的需求，虽说通过`java`发送邮件本身也不是很复杂，但是本着学习积累的宗旨，我还是想做一个简单的总结，一个是方便自己后期遇到相同需求的时候查阅，另一个也是希望我的实践过程可以为各位正在做相关需求的小伙伴提供一点点帮助和借鉴。



### java发送邮件

#### 邮件服务的常见协议及区别

##### IMAP

关于`IMAP`的解释，我这里就直接引用百度百科解释了：

> IMAP（Internet Message Access Protocol）以前称作交互邮件访问协议（Interactive Mail Access Protocol），是一个[应用层协议](https://baike.baidu.com/item/应用层协议/3668945)。IMAP是[斯坦福大学](https://baike.baidu.com/item/斯坦福大学/278716)在1986年开发的一种邮件获取协议。它的主要作用是邮件[客户端](https://baike.baidu.com/item/客户端)可以通过这种协议从[邮件服务器](https://baike.baidu.com/item/邮件服务器/985736)上获取邮件的信息，下载邮件等。当前的权威定义是RFC3501。IMAP协议运行在[TCP/IP协议](https://baike.baidu.com/item/TCP%2FIP协议)之上，使用的端口是143。它与`POP3`协议的主要区别是用户可以不用把所有的[邮件](https://baike.baidu.com/item/邮件/3110293)全部下载，可以通过[客户端](https://baike.baidu.com/item/客户端/101081)直接对[服务器](https://baike.baidu.com/item/服务器/100571)上的邮件进行操作。

各位小伙伴需要注意的是，`IMAP`协议是针对接收邮件的（邮件获取协议），也就是客户端协议，通过它我们只能接收和管理邮件，但并不能发送邮件。另外还需要注意的是：

它与`POP3`协议的主要区别是用户可以不用把所有的邮件全部下载，可以通过客户端直接对服务器上的邮件进行操作



##### POP3

这里的`pop3`协议也是一种邮件客户端通信协议，所以也是不可以发送邮件的：

> **POP3**，全名为“Post Office Protocol - Version 3”，即“[邮局协议](https://baike.baidu.com/item/邮局协议)版本3”。是[TCP/IP](https://baike.baidu.com/item/TCP%2FIP)协议族中的一员，由[RFC](https://baike.baidu.com/item/RFC)1939 定义。本协议主要用于支持使用客户端远程管理在[服务器](https://baike.baidu.com/item/服务器/100571)上的电子邮件。提供了[SSL](https://baike.baidu.com/item/SSL)加密的POP3协议被称为POP3S。
>
> **POP 协议**支持“离线”邮件处理。其具体过程是：邮件发送到服务器上，电子[邮件客户端](https://baike.baidu.com/item/邮件客户端)调用邮件客户机程序以连接服务器，并下载所有未阅读的电子邮件。这种离线访问模式是一种存储转发服务，将邮件从[邮件服务器](https://baike.baidu.com/item/邮件服务器/985736)端送到个人终端机器上，一般是PC机或 MAC。一旦邮件发送到 PC 机或[MAC](https://baike.baidu.com/item/MAC)上，邮件服务器上的邮件将会被删除。但POP3邮件服务器大都可以“只下载邮件，服务器端并不删除”，也就是改进的POP3协议。

##### SMTP

`SMTP`协议主要就是用来发送邮件的，因为如果只是通过`IMAP`或者`POP3`协议的话，我们只能被动地接收邮件，而不能发送邮件，所以我们在邮箱服务商的配置文档中看到`POP3`和`IMAP`的配置通常是和`SMTp`成对出现的，因为只有配置了`SMTP`服务，才能确保我们的客户端可以发出邮件。

> SMTP是一种提供可靠且有效的[电子邮件传输](https://baike.baidu.com/item/电子邮件传输/22035911)的协议。SMTP是建立在FTP[文件传输服务](https://baike.baidu.com/item/文件传输服务/5389842)上的一种邮件服务，主要用于系统之间的邮件信息传递，并提供有关来信的通知。SMTP独立于特定的传输子系统，且只需要可靠有序的数据流信道支持，SMTP的重要特性之一是其能跨越网络传输邮件，即“SMTP邮件中继”。使用SMTP，可实现相同网络处理进程之间的邮件传输，也可通过[中继器](https://baike.baidu.com/item/中继器/1867747)或网关实现某处理进程与其他网络之间的邮件传输。

比如`163`邮箱：

![](https://gitee.com/sysker/picBed/raw/master/blog/20220323081134.png)

再比如`qq`邮箱：

![](https://gitee.com/sysker/picBed/raw/master/blog/20220329215944.png)

这里需要补充说明的是，`SMTP`的端口号是`25`和`465`，但是考虑到安全性，很多服务云服务商是不允许使用非`SSL`的端口的，也就是`25`端口，我在实际测试的时候，发现阿里云就不允许通过`25`端口发送邮件，所以通常我们用更安全的`SSL`端口就可以了，基本上大部分的邮件服务商都支持这个端口，比如`QQ`、`163`、阿里企业邮箱。

##### Exchange

> Exchange Server 是微软公司的一套[电子邮件](https://baike.baidu.com/item/电子邮件)服务组件，是个消息与协作系统。 简单而言，Exchange server可以被用来构架应用于[企业](https://baike.baidu.com/item/企业/707680)、学校的[邮件系统](https://baike.baidu.com/item/邮件系统/3609280)。Exchange是收费邮箱，但是国内微软并不直接出售Exchange邮箱，而是将Exchange、[Lync](https://baike.baidu.com/item/Lync)、[Sharepoint](https://baike.baidu.com/item/Sharepoint/4710853)三款产品包装成Office365出售。Exchange server还是一个协作平台。在此基础上可以开发工作流，[知识管理系统](https://baike.baidu.com/item/知识管理系统/2704468)，Web系统或者是其他消息系统。

#### 邮件地址校验

##### 端口、服务器校验

这里我自己写了一个`telnet`方法，用于检测服务器和端口是否联通，同时设置了超时时间

```java
public static boolean telnet(String host, Integer port, Integer timeout) {
    try {
        Socket socket = new Socket();
        SocketAddress socketAddress = new InetSocketAddress(host, port);
        socket.connect(socketAddress, timeout);
        if (socket.isConnected()) {
            return Boolean.TRUE;
        }
    } catch (IOException e) {
        logger.warning("telnet error" + e);
    }
    return false;
}

```



##### 发送测试邮件

端口和服务器校验通过之后，还需要通过发送测试邮件的方式来测试用户名和邮箱账号是否争取。



#### java发送邮件



#### java接收邮件





### 结语