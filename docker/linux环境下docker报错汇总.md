### 1. 问题1

`linux`环境下执行`docker`命令，提示如下错误：

```sh
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```

#### 解决方法

```shell
sudo groupadd docker          #添加docker用户组
sudo gpasswd -a $XXX docker   #检测当前用户是否已经在docker用户组中，其中XXX为用户名，例如我的，liangll
sudo gpasswd -a $USER docker  #将当前用户添加至docker用户组
newgrp docker #更新docker用户组
```

### 2.问题2

执行`docker`命令报错

```sh
$ docker config ls                              
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```

#### 解决方法

在`/etc/docker/`下创建`daemon.json`文件，并添加如下配置：

```json
{
 "registry-mirrors": [
     "https://registry.docker-cn.com"
 ]
}
```

然后重启`docker`服务：

```sh
systemctl restart docker.service
```

