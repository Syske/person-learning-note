# docker入门
tags: [#docker]

## 前言

`Docker`作为一个重要的云容器，在目前的线上部署环境中被广泛应用，甚至很多公司已经在用`K8S`了，但是我们绝大多数后端开发小伙伴可能连`Docker`这样的容器都还没有真正使用过，今天我们就简单的开箱一下这一款迷之容器，揭开它神秘的面纱。

最近又开始上手折腾`Docker`，是因为新公司的应用都是部署在云环境的，而且服务比较多，为了快速搭建本地开发环境，所以我就又一次拾起了尚未入门的`docker`，探索一下它真实的面目，今天讲的内容会比较浅显，保证你上手能用，高级用法等我研究透了再说，另外最近我也接触了`ES`的一些内容，后面应该会抽时间研究琢磨，等到我觉得时候分享的时候，我会发出来的。

另外说一句，最近一直没有更新什么技术内容，原因之前说过了，现在所有的事情都很顺利，所以技术学习更新从这周开始恢复正常，后面就开始漫长的、无止境的学习之路，让我们一起进步吧！！！！

<img src="
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210406224856.png" style="zoom:33%;" />

## Docker安装

### 下载

直接访问`docker`官网进行下：

```
https://www.docker.com/products/docker-desktop
```

选择选择对应的版本，这里我的操作系统是`windows`：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210406212217.png)

### 安装

安装过程很简单，双击下载好的`exe`文件，其他操作系统类似，然后等待安装完成，因为当前系统已经安装过了，所以我就没法演示了，网上爬了一张图：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210406213701.png)

### 启停docker服务

一般安装成功后会自动启动docker服务，如果没有启动，你可以手动启动，这里以`win10`为例：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210406214226.png)

在任务栏右边找到`docker`的小图标，右键选择自己需要的操作，即可对`docker`服务进行启停。如果任务栏没有`docker`的小图标，可以在桌面双击运行`docker`应用快捷方式进行启动

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210406214606.png)



## docker简单配置

因为`docker`并非国内产物，所以在下载相关镜像资源的时候特别慢，为了提高我们资源的下载速度，我们需要配置`docker`的镜像信息，右键任务栏`docker`小图标，打开`docker`的控制面板（或者双击小图标）：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210406215055.png)

点击设置按钮，选择`docker Engine`，修改其中`registry-mirrors`的配置信息：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210406215358.png)

配置信息是`json`格式：

```json
"registry-mirrors": [
    "https://reg-mirror.qiniu.com/",
    "https://docker.mirrors.ustc.edu.cn/",
    "https://hub-mirror.c.163.com/"
  ]
```

其中第一个地址是七牛的镜像，第二个是中科大的镜像，最后一个是网易的镜像。配置完成后，下载资源速度会特别快，不信的小伙伴可以对比下。



## 基本操作

下面是一些常用的操作，小伙伴们可以参考下：

### 基本命令

#### 1. 拉取镜像

```sh
$ docker pull ubuntu:latest
#或者
$ docker pull ubuntu
```

解释下上面的命令，`ubuntu`表示镜像资源的名称，`latest`表示版本信息，如果不加版本信息，一般会默认拉取最新版本，也就是`latest`，当然你也可以根据自己的需要指定版本信息。

所以，上面命令的作用就是将`ubuntu`的最新镜像拉至本地仓库，一般在拉取镜像资源之前，我们都会先通过`docker search`搜索一下镜像资源，确保资源存在。

#### 2. 查看本地镜像

```sh
$ docker images
```

上面这个命令就很简单，就是展示本地已经拉取的镜像资源：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210406220312.png)

#### 3. 运行容器

```sh
$ docker run -itd --name ubuntu-test ubuntu
```

这个命令应该是最常用的，表示运行某个镜像，但是针对不同的镜像指令可能会有差异，我们在具体使用的时候根据自己的需要进行添加，相信的指令我们后面在详细研究。

上面命令的作用是，启动`ubuntu`的镜像，镜像实例的名称为`ubuntu-test`，因为我们没有加版本号，所以默认使用的镜像资源是`latest`，如果`latest`版本不存在，就会报错

#### 4. 搜索镜像

```sh
$ docker search image-name
```

例如：

```sh
$ docker search redis
```

#### 5. 常用操作

下面是一些常用组件在`docker`中的部署、启动操作命令，各位小伙伴可以参考下：

##### 安装并运行nginx

```sh
# 拉取最新版本
$ docker pull nginx:latest
# 启动运行
$ docker run --name nginx-test -p 8080:80 -d nginx
```

其中，`name`和前面一样，表示启动的实例名称；`p`表示端口号，`8080:80`表示将本地的`8080`端口映射到`docker`的`80`端口，这时候我们就可以通过当前主机de`8080`端口来访问我们`docker`中的`nginx`；`d`表示在后台运行，这时候就算你关闭了启动的命令行窗口，容器依然会正常运行；最后面的`nginx`其实是我们偷懒省略了`:latest`，它等同于`nginx:latest`

##### 安装并运行mysql

```sh
# docker 中下载 mysql
$ docker pull mysql

#启动
$ docker run --name mysql-test -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -d mysql:5.7.19

#进入容器
$ docker exec -it mysql bash

#登录mysql
mysql -u root -p
ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';

#添加远程登录用户
CREATE USER 'syske'@'%' IDENTIFIED WITH mysql_native_password BY '123456';
GRANT ALL PRIVILEGES ON *.* TO 'syske'@'%';
```

这里大部分的参数都和前面的作用一样，唯一不同的是多了`e`，这里`-e`的作用是设置环境变量，也就是说`MYSQL_ROOT_PASSWORD=root`是要设置的环境变量，作用就是设置`root`用户的密码。

**这里再增加另一个版本：**

```sh
$ docker run --rm --name mysqlTemp -it -v /usr/local/mysql/:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456  mysql:5.7 /bin/bash

$ cp /etc/mysql/my.cnf /var/lib/mysql
```

`-- rm` 退出后就删除该容器

`-v /usr/local/mysql/:/var/lib/mysql` 装主机目录`/usr/local/mysql/`映射`Docker`中的`/var/lib/mysql`目录

`-it` 交互模式

`/bin/bash` 进入 `bash` 命令模式

上面这几种启动方式，在实际使用中重启`docker`容器之后，数据都会丢失，为了能够在下次启动容器的时候数据还在，我们要用下面的启动命令：

```sh
$ docker run -p 3306:3306 -d -e MYSQL_ROOT_PASSWORD=密码 -v /windows盘符/指定的文件夹路径:/var/lib/mysql    mysql:5.7
```



##### 安装并运行redis

```sh
# 拉取最新版本镜像
$ docker pull redis:latest
# 启动运行
$ docker run -itd --name redis-test -p 6379:6379 redis
$ docker run --name redis -p 6380:6379 redis-test --requirepass 123456
#前边是宿主机端口 后面是docker使用的端口
```

参数大部分都和前面一致，`--requirepas`是这只`redis`的访问密码

和上面`mysql`一样，为了确保存储数据下次可以被加载，我们要用下面的启动命令

```sh
docker run -p 6379:6379 -d  -v /windows盘符/指定的文件夹路径:/data    redis:5.0 redis-server --appendonly yes
```



##### 安装activemq

```sh
$ docker run -d --name myactivemq -p 61616:61616 -p 8162:8161 docker.io/webcenter/activemq:latest
```

这里没什么特殊的参数，不做过多说明

##### 安装zookeeper

```sh
$ docker run -d --name zookeeper-test -p 2181:2181 zookeeper
```



#### 查看所有容器

```sh
$ docker ps -a
```

这里就是查看`docker`的进程，和`linux`的`ps`命令类似，看到这个命令我就猜到她肯定还有另一个命令：

```sh
$ docker kill pid
```

然后我试了下，果然有效，依然和`linux`类似

#### 启动已存在容器

```sh
$ docker start 容器ID
```



## 结语

原本打算通过`docker`搭建本地开发测试环境的，但是新公司采用的都是线上集成开发环境，所以目前这块仅用于日常学习和练习。虽然这次了解的不多，但是我还是发现用`docker`搭建本地开发测试环境简直美滋滋，而且美的不要不要的，你想想原来你每次搞个测试环境要安装这个组件，又要安装那个组件，有了`docker`一行命令一个组件就可以搞定了，而且如果环境出现问题了，还可以把容器删除了重头再来，而不像本地，搞坏了，重新安装还会出现各种问题，所以小伙伴们，赶紧把`docker`用起来，开发真的美滋滋！😉

好了，大家晚安哦！

