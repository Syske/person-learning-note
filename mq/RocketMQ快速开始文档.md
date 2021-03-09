# RocketMQ快速开始文档

解压压缩文件

```sh
  > unzip rocketmq-all-4.8.0-source-release.zip
  > cd rocketmq-all-4.8.0/
  > mvn -Prelease-all -DskipTests clean install -U
  > cd distribution/target/rocketmq-4.8.0/rocketmq-4.8.0
```

# Linux

## Start Name Server

```sh
  > nohup sh bin/mqnamesrv &
  > tail -f ~/logs/rocketmqlogs/namesrv.log
  The Name Server boot success...
```

## Start Broker

```sh
  > nohup sh bin/mqbroker -n localhost:9876 &
  > tail -f ~/logs/rocketmqlogs/broker.log 
  The broker[%s, 172.30.30.233:10911] boot success...
```

## Send & Receive Messages

Before sending/receiving messages, we need to tell clients the location of name servers. RocketMQ provides multiple ways to achieve this. For simplicity, we use environment variable `NAMESRV_ADDR`

```sh
 > export NAMESRV_ADDR=localhost:9876
 > sh bin/tools.sh org.apache.rocketmq.example.quickstart.Producer
 SendResult [sendStatus=SEND_OK, msgId= ...

 > sh bin/tools.sh org.apache.rocketmq.example.quickstart.Consumer
 ConsumeMessageThread_%d Receive New Messages: [MessageExt...
```

## Shutdown Servers

```sh
> sh bin/mqshutdown broker
The mqbroker(36695) is running...
Send shutdown request to mqbroker(36695) OK

> sh bin/mqshutdown namesrv
The mqnamesrv(36664) is running...
Send shutdown request to mqnamesrv(36664) OK
```

# Windows

The guide is working for windows 10 , please make sure you have powershell installed.

Download latest binary release. and extract zip file into your local disk. Such as: `D:\rocketmq`

## Add Environment Variables

You need set environment variables

1. From the desktop, right click the Computer icon.
2. Choose Properties from the context menu.
3. Click the Advanced system settings link.
4. Click Environment Variables.
5. Then add or change Environment Variables.

```sh
ROCKETMQ_HOME="D:\rocketmq"
NAMESRV_ADDR="localhost:9876"
```

Or just in the openning powershell, type the needed environment variables.

```sh
$Env:ROCKETMQ_HOME="D:\rocketmq"
$Env:NAMESRV_ADDR="localhost:9876"
```

If you choose the powershell way. you should do it for every new open powershell window.

## Start Name Server

Open new powershell window, after set the correct environment variable. then change directory to rocketmq type and run:

```sh
.\bin\mqnamesrv.cmd
```

## Start Broker

Open new powershell window, after set the correct environment variable. then change directory to rocketmq type and run:

```sh
.\bin\mqbroker.cmd -n localhost:9876 autoCreateTopicEnable=true
```

## Send & Receive Messages

### Send Messages

Open new powershell window, after set the correct environment variable. then change directory to rocketmq type and run:

```sh
.\bin\tools.cmd  org.apache.rocketmq.example.quickstart.Producer
```

### Receive Messages

Then you will see messages produced. and now we can try consumer messages.

Open new powershell window, after set the correct environment variable. then change directory to rocketmq type and run:

```sh
.\bin\tools.cmd  org.apache.rocketmq.example.quickstart.Consumer
```

## Shutdown Servers

Normally, you can just closed these powershell windows. (Do not do it at production environment)