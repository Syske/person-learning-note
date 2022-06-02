# docker部署RocketMq

### 前言

最近公司在搞`ActiveMQ`切换到`rocketMq`的事，虽然不是特别紧急的事，而且好像已经给出切换的文档了，但是本着自己动手丰衣足食的想法，我还是打算把之前发过的`rocketMq`的相关内容，再好好回顾下，毕竟知其然且知其所以然，才能更好地处理（装）问题（逼）。

不过今天的内容暂时还不涉及`RocketMq`的相关技术知识，只是一次简单的环境搭建，关于技术层面的知识，我们后面继续探讨。



### RocketMQ部署

#### 部署namesrv

`namesrv`就类似于消息队列的注册中心，因为`rocketmq`原生支持集群，所以`namesrv`就显得很重要。

##### 拉取镜像

首先是拉取镜像，这里拉取的是`rocketMQ`的核心镜像

```
docker pull rocketmqinc/rocketmq
```



##### 启动namesrv

启动过程也很简单，主要是`docker`的一些参数和配置指定

```sh
# 后台运行，并映射端口
docker run -d -p 9876:9876 \
# 设置容器名称
--name rmqnamesrv \
# 设置重启策略
--restart=always \
# 映射日志文件夹（前面的为本地路径）
-v /home/syske/docker/mq/data/namesrv/logs:/root/logs \
# 映射书籍存在文件夹（同上）
-v /home/syske/docker/mq/namesrv/store:/root/store \
# 指定环境变量
-e "MAX_POSSIBLE_HEAP=100000000" \
# 指定镜像版本，这里建议指定具体版本，否则在和java交互的时候会报错，目前最新版本是4.4.0，所以maven的依赖也必须对应，否则会报错
rocketmqinc/rocketmq:latest \
# 启动命令
sh mqnamesrv
```



#### 部署broker

由于`broker`和`namesrv`是同一个镜像，所以这里不需要再拉取镜像



##### 创建broker配置

除了最后两行配置，其他的配置都是系统默认的，具体说明可以参考官方文档

```properties
# broker集群名称
brokerClusterNam = DefaultCluster
# broker节点名称
brokerName = broker-a
# broker节点id
brokerId = 0
# 删除条件？这个还不清楚用途，后续研究下
deleteWhen = 04
# 文件保留时间（单位小时），默认为3天
fileReservedTime = 48
# broker角色
brokerRole = ASYNC_MASTER
# 磁盘同步方式：同步，异步
flushDiskType = ASYNC_FLUSH
# 类似注册中心
namesrvAddr=192.168.0.103:9876
# 当前broker监听的IP(主)
brokerIP1 = 192.168.0.103
```



##### 启动broker

这里的启动命令最核心的其实就是最后`sh`操作，这里制定了配置文件的路径。

```sh
 # 后台运行
 docker run -d \
 # 映射端口
-p 10911:10911 \
# 映射端口
-p 10909:10909 \
# 容器名称
--name rmqbroker \
# 重启策略
--restart=always \
# 映射日志路径
-v /home/syske/docker/mq/data/broker/logs:/root/logs \
# 映射文件存储路径
-v /home/syske/docker/mq/data/broker/store:/root/store \
# 映射配置文件
-v /home/syske/docker/mq/conf/broker.conf:/opt/rocketmq-4.4.0/conf/broker.conf \
# 链接namesrv
--link rmqnamesrv:namesrv \
# 指定环境设置
-e "NAMESRV_ADDR=namesrv:9876" \
# 指定环境设置，指定镜像
-e "MAX_POSSIBLE_HEAP=200000000" rocketmqinc/rocketmq:latest \
# 启动命令（指定配置启动）
sh mqbroker -c /opt/rocketmq-4.4.0/conf/broker.conf
```

由于这里我们把`rocketmq`的日志映射到了本机目录，所以我们可以直接通过`tail`查看`broker`的启动日志，比如`broker.log`:

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220306212426.png)

当然，你也可以通过`docker exec`命令的方式查看日志，当然就是没有上面这种方式方便。



#### 安装console

`console`是`rocketmq`的扩展组件，`console`组件提供了图形化的界面，便于我们管理和监控`rocketmq`，界面截图如下：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220306203735.png)

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220306203802.png)

官方文档：

```
https://rocketmq-1.gitbook.io/rocketmq-connector/rocketmq-connect/rocketmq-console/an-zhuang-shi-yong
```



##### 拉取镜像

默认拉取最新版本镜像：

```sh
docker pull styletang/rocketmq-console-ng
```

##### 启动

启动命令也很简单，只是指定`rocketmq`的`namesrv`的地址，除了端口有修改，其他直接复制官方文档

```sh
docker run -e "JAVA_OPTS=-Drocketmq.namesrv.addr=192.168.0.103:9876 -Dcom.rocketmq.sendMessageWithVIPChannel=false" -p 8000:8080 -t styletang/rocketmq-console-ng
```

启动成功后直接访问我们配置的端口，即可看到如上截图。



#### 踩坑记录

由于是时候回顾总结，所以过程中的好多错误问题我已经复现不出来了，下面是印象比较深刻的几个问题，各位小伙伴可以参考下，少走一些弯路。

- 映射路径配置错误，导致容器无限重启。表现就是执行`docker ps`的时候，`mqbroker`服务状态一直是`Restarting`：

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220306195542.png)

  最后几经检查，发现是映射的本地文件夹不存在导致的。本地的路径是`/home/syske/docker/mq/data/broker`，但是启动命令里面映射的路径少了`docker`目录，所以导致日志和配置文件路径都错误了，所以报错了

- 版本问题导致配置文件读取不到：也就是在启动`boker`服务地时候，`broker.conf`的路径配置不正确，导致启动直接报错：

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220306200618.png)

  进入容器中查看了`rocketmq`的版本才知道这里的路径需要配置成`rocketmq-4.4.0`，所以各位小伙伴在拉取镜像的时候一定要指定版本，这样在设置配置的时候也就不会出错了。

- 如果你在客户端调用`rocketmq`时有如下错误：![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220306201826.png)

  你需要在`broker`的配置文件中指定`brokerIP1`的相关配置，因为`172.17.0.5`是`docker`的内网`ip`，我们需要在外部调用`broker`，所以需要配置一个外部`ip`（`docker`主机的局域网`ip`）

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220306201922.png)

- 如果客户端调用`rocketmq`报错的话，那大概率是因为`broker`服务没有正常启动导致的（我就是应为第一个坑导致的）![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220306201013.png)



### 结语

好了关于`docker`安装配置`rocketMq`的相关内容，我们就先到这里，下面我们聊点本次折腾的背景：

原本是打算在`manjaro`环境搞下`rocketMQ`的测试环境就可以了，但是在实际操作的时候，发现`manjaro`还没有配置过`JDK`环境，而且在我一通安装设置之后，`rocketMq`启动还是报错，具体报什么错我也记不清楚了，总之就是很恶心，最后我就放弃了这种原生的方式。

之后我又想到了可以在`k8s`环境搞一套，但是不幸的是，我发现`manjaro`的`k8s`集群也坏了，就是执行`kubectl`命令时候一直提示拒绝连接：

```
The connection to the server localhost:8080 was refused - did you specify the right host or port?
```

好吧，太浪费时间了，于是我觉定重新装个系统（一言不合就折腾），一顿操作之后，我安装了特别熟悉的`linux`系统——`ubuntu`，不过网络还算给力，`20m/s`的速度，系统很快就下载好了。之后经过两个小时的折腾，`docker`、`jdk`、`git`、`oh-my-zsh`都被我搞定了，然后今天又花了两三个小时折腾`rocketmq`的`docker`环境。

总体来说，我还是很喜欢这种排查并处理问题的感觉的，特别是解决完所有问题之后的酣畅感，这给了我极大的成就感，这也是我热爱折腾的原因吧！