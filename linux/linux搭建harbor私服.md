# linux搭建harbor私服

### 前言

昨天我们分享了`manjaro`环境下构建`k8s`集群的过程，其中我提到我顺手搭建了`harbor`环境，所以今天我想抽点时间来简单分享下如何在`linux`环境下搭建`harbor`平台。

### Harbor

我们先来看下`harbor`是什么？

`harbor`是一个容器镜像仓库的开源项目，它主要为我们提供了一套镜像存储管理的解决方案，我们简单将它理解为镜像仓库即可。它中文的意思是港口，也就是存放镜像的仓库，而`docker`是码头工人的意思，也就是镜像的搬运工，突然想起了某泉的广告词，对`docker`来说，也同样适用：我不生产镜像，我只是镜像的搬运工。

> `Harbor `是为企业用户设计的容器镜像仓库开源项目，包括了权限管理(`RBAC`)、`LDAP`、审计、安全漏洞扫描、镜像验真、管理界面、自我注册、HA 等企业必需的功能，同时针对中国用户的特点，设计镜像复制和中文支持等功能。

#### 准备工作

因为我们的`harbor`环境是基于`docker-compose`构建的，所以我们先要安装`docker-compose`，这里以`manjaro`为例，其他环境类似：

```sh
sudo pacman -S docker-compose
# ubuntu环境可有通过如下命令
sudo apt install sudo docker-compose
```

![](https://gitee.com/sysker/picBed/raw/master/images/20211227230115.png)

版本没有要求，我目前安装的是`2.2.2`:

![](https://gitee.com/sysker/picBed/raw/master/images/20211227225514.png)

安装完成后可以通过下面的命令测试下：

```
docker-compose -v
```

执行结果类似上图，则表明安装成功。

#### 下载安装

##### 下载脚本

`harbor`本身是开源项目，可以直接访问项目`github`仓库进行下载，项目地址如下：

```
https://github.com/goharbor/harbor
```

不喜欢自己动手的小伙伴可以直接通过如下命令下载：

```
wget https://github.com/goharbor/harbor/releases/download/v2.4.1/harbor-offline-installer-v2.4.1.tgz
```

下载完成后直接解压即可，命令如下：

```
tar -zxvf harbor-offline-installer-v2.4.1.tgz
```

![](https://gitee.com/sysker/picBed/raw/master/images/20211227230348.png)

解压之后文件目录如下：

![](https://gitee.com/sysker/picBed/raw/master/images/20211227230507.png)

下面我们只需要修改配置文件即可。

##### 配置

解压之后的`harbor`目录下有一个名为`harbor.yml.tmpl`的配置文件模板，我们需要基于这个文件构建我们的配置文件（配置模板），这里直接复制即可，复制之后的目标文件名为`harbor.yml`（强制，如果要用其他名称，就需要修改`intall.sh`脚本）。

下面我们看下如何配置，这里我直接放上我的配置和各个配置的作用：

```yaml
# Configuration file of Harbor

# 这里配置的是我们harbor服务的访问ip，管理端也是通过这个地址访问的，不要使用localhost 或者 127.0.0.1，因为Harbor是需要外部客户端访问的
hostname: 192.168.0.102

# http的访问配置
http:
  # http访问端口, 默认80. 如果启用了https协议, 则会通过这个端口重定向到https端口
  port: 88

# harbor管理端的登录密码，默认账户是admin
harbor_admin_password: Harbor12345

# Harbor DB设置
database:
  # 数据库
  password: root123
  # idle最大连接数
  max_idle_conns: 50
  # 数据库最大连接数，默认1024（postgres）
  max_open_conns: 100

# 默认数据卷（）
data_volume: /data
# 以下数据我没有改动
trivy:
  ignore_unfixed: false

  skip_update: false
  #
  # insecure The flag to skip verifying registry certificate
  insecure: false

jobservice:
  # Maximum number of job workers in job service
  max_job_workers: 10

notification:
  # Maximum retry count for webhook job
  webhook_job_max_retry: 10

chart:
  # Change the value of absolute_url to enabled can enable absolute url in chart
  absolute_url: disabled

# Log configurations
log:
  # options are debug, info, warning, error, fatal
  level: info
  # configs for logs in local storage
  local:
    rotate_count: 50
    rotate_size: 200M
    # The directory on your host that store log
    location: /var/log/harbor

_version: 2.4.0
proxy:
  http_proxy:
  https_proxy:
  no_proxy:
  components:
    - core
    - jobservice
    - trivy
```

除了上面的`ip`、端口以及连接数，其他的配置我都用的是默认配置，修改完成之后，我们就可以安装了。



##### 安装

安装也很简单，我们直接执行`install.sh`脚本即可，为了保险起见，推荐使用`sudo`操作：

```
sudo ./install.sh
```

然后静静等待安装完成即可：

![](https://gitee.com/sysker/picBed/raw/master/images/20211227233109.png)

![](https://gitee.com/sysker/picBed/raw/master/images/20211227233207.png)

看到`started successfully`，就说明`harbor`已经安装完成了，我们可以通过浏览器访问下。

##### 测试

用浏览器打开我们刚才配置的地址和端口，可以看到如下页面：

![](https://gitee.com/sysker/picBed/raw/master/images/20211227233426.png)

至此，我们的`harbor`就安装完成了，是不是很简单呢？



#### 使用

下面我们再来看下具体如何使用`harbor`。

通过我们前面配置的密码和用户名（默认`admin`），登录之后我们会看到如下页面：

![](https://gitee.com/sysker/picBed/raw/master/images/20211227233639.png)

正常情况下，你应该只能看到`library`这个项目，你可以在这里创建自己的项目，然后后面我们可以通过`docker`往`harbor`的项目中推送镜像。



#### 镜像操作

在通过`docker`向`harbor`推送镜像之前，我们先要在`docker`中配置本地仓库，首先我们要打开`docker`的配置文件:

```sh
sudo vim /etc/docker/daemon.json
```

向其中增加`insecure-registries`的配置信息：

```
 "insecure-registries":["http://192.168.0.102:88"]
```

最终配置完的效果如下：

![](https://gitee.com/sysker/picBed/raw/master/images/20211227234347.png)

这里的`http://192.168.0.102:88`就是我前面配置的`harbor`的地址和端口，配置完成后我们才能通过`docker`正常登录，否则会报错。

##### 登录

登录命令如下：

```sh
sudo docker login -u admin -p Harbor12345 192.168.0.102:88
```

这里简单解释下，`-u`后面是登录用户名，`-p`是登录密码，再后面是地址和端口

![](https://gitee.com/sysker/picBed/raw/master/images/20211227234941.png)

正常情况下，最后会提示`Login Succeeded`，表明配置都是`ok`的，这时候我们就可以通过`dokcer`命令向`harbor`中推送镜像了。

#### 推送镜像

关于`spring boot`项目构建`docker`镜像的相关内容可以参考之前我们分享的内容：

https://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648419079&idx=1&sn=077f24cdd1308041e238ffa4705b5bb1&chksm=bea6c58d89d14c9b4cb4a1eea431c81af338c534dcaf01a827b7511815f8a7f5e69f20e91a35&token=1495367877&lang=zh_CN#rd

首先我们通过`docker build`构建镜像：

![](https://gitee.com/sysker/picBed/raw/master/images/20211228000244.png)

然后通过`tag`命令创建标签，再通过`push`命令将镜像推送到`harbor`仓库中，这里以我刚创建的`syske`项目为例。其实，`harbor`的项目下面是有镜像推送命令的，我们只需要复制出来替换其中的`REPOSITORY`和`TAG`即可：

![](https://gitee.com/sysker/picBed/raw/master/images/20211228001040.png)

##### tag命令

复制出来的`tag`命令如下：

```sh
docker tag SOURCE_IMAGE[:TAG] 192.168.0.102:88/syske/REPOSITORY[:TAG]
```

替换之后如下：

```sh
docker tag springboot-learning:v1 192.168.0.102:88/syske/springboot-learning:v1
```

如果在执行`tag`命令过程中提示权限不足，可以通过`sudo`操作：

![](https://gitee.com/sysker/picBed/raw/master/images/20211228001432.png)

操作不报错，则表明操作成功。

##### push命令

复制出来的`push`命令如下：

```sh
docker push 192.168.0.102:88/syske/REPOSITORY[:TAG]
```

替换之后如下：

```sh
docker push 192.168.0.102:88/syske/springboot-learning:v1
```

和`tag`命令类似，这个命令也是有权限要求的：

![](https://gitee.com/sysker/picBed/raw/master/images/20211228001702.png)

然后换成`sudo`重新操作即可：

![](https://gitee.com/sysker/picBed/raw/master/images/20211228001800.png)

推送成功后，我们可以登录`harbor`看下：

![](https://gitee.com/sysker/picBed/raw/master/images/20211228001853.png)

可以看到`harbor`中已经有了我们刚刚推送的镜像，这样我们就可以在`k8s`、`docker`等环境使用我们的镜像了

![](https://gitee.com/sysker/picBed/raw/master/images/20211228002013.png)

##### 拉取镜像

拉取镜像的命令，我们同样也可以在`harbor`页面复制：

![](https://gitee.com/sysker/picBed/raw/master/images/20211228002136.png)

然后我们就可以通过复制到的命令拉取我们的镜像

```
docker pull 192.168.0.102:88/syske/springboot-learning:v1
```

或者在`k8s`直接使用：

![](https://gitee.com/sysker/picBed/raw/master/images/20211228002637.png)

### 结语