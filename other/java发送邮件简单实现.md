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

端口和服务器校验通过之后，还需要通过发送测试邮件的方式来测试用户名和邮箱账号是否正确，这里自己写了一个发送邮件的方法，需要用到`javax.mail`的`mail`包，本次示例用的版本是`1.4`，在实际测试中发现，相同的代码，用不同的版本可能会报错。

```java

    /**
     * 发送邮件的方法
     *
     * @param host    :邮件服务器地址
     * @param account :账户（发送方）
     * @param password :账户密码（发送方）
     * @param port    :邮箱服务器端口（发送方）
     * @param toUser  :收件人
     * @param title   :标题
     * @param content :内容
     */
    public static void sendMail(String host, String account, String password, String port, String toUser, String title, String content) throws Exception {

        Properties props = System.getProperties();
        props.setProperty("mail.host", host);
        props.setProperty("mail.smtp.port", port);
        props.put("mail.smtp.auth", "true");
        props.put("mail.smtp.starttls.enable", "false");
        props.put("mail.smtp.socketFactory.fallback", "false");
        props.put("mail.smtp.socketFactory.class", "javax.net.ssl.SSLSocketFactory");
        props.put("mail.smtp.socketFactory.port", port);
        // 发送邮件超时时间
        props.put("mail.smtp.writetimeout", 1000);
        // 连接超时时间
        props.put("mail.smtp.connectiontimeout", 1000);

        Session session = Session.getInstance(props, new Authenticator() {
            @Override
            protected PasswordAuthentication getPasswordAuthentication() {
                return new PasswordAuthentication(account, password);
            }
        });

        Message msg = new MimeMessage(session);

        msg.setFrom(new InternetAddress(account));
        msg.setRecipients(Message.RecipientType.TO, InternetAddress.parse(toUser));
        msg.setContent(content, "text/html;charset=utf-8");
        msg.setSubject(title);
        msg.setSentDate(new Date());
        Transport.send(msg);
    }
```

这里比较繁琐的就是邮箱服务器的配置了：

- `mail.host`：这个不用说，就是邮件服务的服务器地址（域名或者`IP`）

- `mail.smtp.port`：这个就是邮件服务器的端口，通常是`465`（`SSL`），当然你也可以用非`SSL`的端口，但是你需要移除`mail.smtp.socketFactory.class`的相关配置，否则会报错（不过这里还是推荐大家使用`SSL`协议，毕竟比较安全）：

  ![](https://gitee.com/sysker/picBed/raw/master/2022/20220404112819.png)

- `mail.smtp.auth`：`smtp`验证，这个配置项是必须的，且值必须是`true`，否则会报错：

  ![](https://gitee.com/sysker/picBed/raw/master/2022/20220404140214.png)

- `mail.smtp.starttls.enable`：设置`TLS`是否启用，如果是`SSL`通信协议，该设置项必须未设置或者值为`flase`，否则也会报错：![](https://gitee.com/sysker/picBed/raw/master/2022/20220404140850.png)

- `mail.smtp.socketFactory.class`：设置`socket`工厂，`SSL`通信的话，必须设置为`javax.net.ssl.SSLSocketFactory`，否则会报错：

  ![](https://gitee.com/sysker/picBed/raw/master/2022/20220410134326.png)

- `mail.smtp.socketFactory.port`：设置`socket`的端口，实际测试中发现该配置参数可以省略

#### java发送邮件

其实在上面发送测试邮件那里，我们已经展示了发送邮件的方式，这里我们直接调用那个方法即可。在开始发送邮件之前，我们先来看下如何获取方法的参数，也就是邮件服务器的相关配置信息，这里我们以`163`邮箱为例，其他邮箱大同小异。

首先登录到`163`邮箱网页端，点击顶部的设置菜单，选择`POP3/SMTP/IMAP`那个选项

![](https://gitee.com/sysker/picBed/raw/master/2022/20220410140317.png)

开启`IMAP/SMTP`或者`POP3/SMTP`服务中的任意一个，因为我们主要是为了实现发送邮件的需求，所以只要我们开启了`SMTP`服务即可。

前面我们说了，`POP3`或者`IMAP`协议都是接收邮件的协议，发送邮件的协议是`SMTP`，所以开启其中一个，`SMTP`协议都会开启。

![](https://gitee.com/sysker/picBed/raw/master/2022/20220410140428.png)

开通时要求用邮箱绑定的手机号发送一行验证码，然后系统会生成一个授权码，这个授权码就是我们后面发送邮件的密码，因为只展示一次，所以务必保存下。

![](https://gitee.com/sysker/picBed/raw/master/2022/20220410140934.png)

然后根据我们前面说的`SMTP`的服务器和端口，既可以实现邮件发送功能，这里我主要是用于测试邮箱配置是否正确，所以我直接给自己发的邮件：

![](https://gitee.com/sysker/picBed/raw/master/2022/20220410141243.png)

发送成功后，我们可以在接收方邮箱中看到该邮件：

![](https://gitee.com/sysker/picBed/raw/master/2022/20220410141419.png)
至此，我们发送邮件的需求就实现了。



### 结语

就整个需求的实现来说，其实代码层面还是比较简单的，真正的难点是邮件服务器配置的相关内容，由于前期对邮件服务的相关协议和配置不了解，所以踩了很多坑，当然也正是有了这样一个踩坑的过程，也才让我对邮件服务配置有了一个更全面的了解和认识。好了，今天的内容就先到这里，感兴趣的小伙伴可以自己动手实践下。