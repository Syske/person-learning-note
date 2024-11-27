
### 安装Armbian系统

#### 下载
```
https://github.com/ophub/amlogic-s9xxx-armbian/releases?page=1
```

下载的时候选择`s905d`的版本
### 刻录系统


### 安装

将`U`盘插入靠近`HDMI`接口的`USB`，然后插电启动


然后，通过`ssh`工具远程连接`N1`盒子，默认账号密码是：`root/1234`


### 安装casaos

```sh
wget -qO- https://get.casaos.io | sudo bash
```
然后静静等待安装完成：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/243eac96-8917-48f2-9d72-10675aeb3044.jpg)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/22f542a8-ef27-400b-9d7f-c9d42a41e0da.jpg)

然后通过`N1`盒子的`ip`地址访问即可，比如我的`ip`地址是`192.168.0.101`，紧接着注册账号登录即可，颜值还是嘎嘎的
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/0e4b5cc3-1830-4b7f-9169-489e36950273.jpg)
参考文档：
1. https://baijiahao.baidu.com/s?id=1797388138356939249&wfr=spider&for=pc