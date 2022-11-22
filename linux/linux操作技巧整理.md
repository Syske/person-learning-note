# linux操作技巧整理

#### 1. 启用ssh远程登录

```sh
# 启用服务
sudo systemctl enable sshd.service
# 启动服务
sudo systemctl start sshd.service
```

执行完如上命令之后，我们的`ssh`远程登录就启动成功了，我们就可以通过如下命令进行远程登录了：

```sh
ssh syske@192.168.0.101
```

其中`syske`是我的用户名，`@`后面是机器的`ip`地址：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20211106234705.png)

#### 2.关闭笔记本盒盖休眠

修改`logind.conf`中`[login]`下的`HandleLidSwitch`为 `lock`

```sh
sudo vim /etc/systemd/logind.conf
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20211106234408.png)

然后重启`systemd-logind`服务：

```sh
 sudo systemctl restart systemd-logind
```

