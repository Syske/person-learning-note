# Doker部署springBoot项目

今天我们分享一个小知识点——`docker`部署`springboot`项目，之所以说它是个小知识点，是因为内容不多，而且也很简单，内容主要包含两个方面，一个是基于`docker`构建`springboot`项目的镜像，一个就是用`docker`启动我们的`springboot`项目镜像。

#### 编写Dockerfile文件

首先，我们要编写这样一份`Dockfile`，文件名就就是`Dockerfile`，没有后缀名，这个文件在项目的根目录下，可以先看我的项目结构：

![](https://gitee.com/sysker/picBed/raw/master/images/20210629130049.png)

然后在`Dockerfile`中写入如下内容，项目不同，配置有所不同，可根据自己的需要进行修改：

```yml
# Docker image for springboot file run
# VERSION 0.0.1
# Author: eangulee
# 基础镜像使用java
FROM java:8
# 作者
MAINTAINER syske <715448004@qq.com>
# VOLUME 指定了临时文件目录为/tmp。
# 其效果是在主机 /var/lib/docker 目录下创建了一个临时文件，并链接到容器的/tmp
VOLUME /tmp 
# 将jar包添加到容器中并更名为springboot-learning.jar
ADD target/springboot-learning-0.0.1-SNAPSHOT.jar /springboot-learning.jar 
# 运行jar包
RUN bash -c 'touch /springboot-learning.jar'
ENV TZ 'Asia/Shanghai'
EXPOSE 8089
ENTRYPOINT ["java","-jar","/springboot-learning.jar"]
```

这里简单介绍下这个文件的结构。

`FROM`的作用是指定项目的运行环境，这里我们指定的是`java8`;

`VOLUME` 指定了临时文件目录为`/tmp`。其效果是在主机 `/var/lib/docker `目录下创建了一个临时文件，并链接到容器的`/tmp`。该步骤是可选的，如果涉及到文件系统的应用就很有必要了。

`/tmp`目录用来持久化到 `Docker` 数据文件夹，因为 `Spring Boot` 使用的内嵌 `Tomcat` 容器默认使用`/tmp`作为工作目录
 项目的 `jar` 文件作为 `springboot-learning.jar`添加到容器的
 `ENTRYPOINT` 执行项目 `springboot-learning.jar`。为了缩短 `Tomcat `启动时间，添加一个系统属性指向 `/dev/./urandom`作为 `Entropy Source`。

`ADD`就是将我们编译的`jar`文件添加到容器中，这里可以知道加入容器的文件名；

`RUN bash -c`就是运行`shell`命令；

`ENV`作用是这是环境变量，这里设置的是时区；

`EXPOSE`的作用是指定容器运行端口；

`ENTRYPOINT`的作用是指定容器运行命令，指定之后，容器运行的时候就会执行我们指定的命令；

关于`Dockerfile`编写，可以参考菜鸟教程：

```
https://www.runoob.com/docker/docker-dockerfile.html
```

#### 项目打包

在编写`Dockerfile`的时候，我们指定了`jar`文件的名字，所以在运行`Dockerfil`之前，我们要先打包好项目的`jar`文件，确保`Dockerfile`中指定的`jar`文件已经编译好：

![](https://gitee.com/sysker/picBed/raw/master/images/20210629130232.png)

打包完成后，我们就可以制作我们的`springboot`项目的镜像了。

#### 制作镜像

首先确保本地`docker`已经启动，然后在项目根目录，即`Dockerfile`所在目录

![](https://gitee.com/sysker/picBed/raw/master/images/20210629130912.png)

执行如下命令：

```sh
docker build -t springboot-learning:v1 .
```

​	`-t` 参数是指定此镜像的`tag`名，一般通常就是`项目名:版本号`。注意最后面的`.`，不要忘记了。

如果有如下提示，则表面`springboot`项目的镜像构建完成，如果你是第一次构建，要拉取`java8`的镜像，所以时间可能会比较长：

![](https://gitee.com/sysker/picBed/raw/master/images/20210629131144.png)

然后我们可以通过下面的命令查看本地镜像:

```
docker images
```

其中就有我们刚刚构建完成的镜像：

![](https://gitee.com/sysker/picBed/raw/master/images/20210629131510.png)

#### 启动springboot镜像

启动我们构建的镜像与启动其他镜像没有本质区别，只是我们在指定端口的时候，容器的端口就是我们前面构建时指定的端口：

```
docker run --rm --name springboot-learning -p 8089:8089 springboot-learning:v1
```

另外这里的镜像版本号，也要和构建文件保持一致。回车之后，你就会看到熟悉的`springboot`启动日志信息：

![](https://gitee.com/sysker/picBed/raw/master/images/20210629132036.png)

这里我为了方便查看，没有加`-d`（后台运行），所以你`ctrl+c`后，容器会自动停止，一般我们线上运行都是后台运行的。

#### 测试

我的项目中有测试的`controller`，我们浏览器访问下看看：

![](https://gitee.com/sysker/picBed/raw/master/images/20210629132317.png)

![](https://gitee.com/sysker/picBed/raw/master/images/20210629132430.png)

和我们直接在本地`java -jar`启动一样，没有任何区别。

最后，简单总结下，最近一段时间，我们分享了很多云生态相关的知识，包括`dokcer`、`k8s`等比较主流的技术，让包括我在内的各位小伙伴对`java`云生态有了一些初步的认识和了解。

然后再加上我们今天分享的`springboot`项目镜像构建，现在这一连串的技术已经差不多全都被我们串起来了，可以这样说，如果这些知识你自己都有动手做过，都有实践过，那你对目前主流的云生态应该已经有了最基本的认知，至少在使用和应用方面没有太多的问题。
后面我们再分享下`kuboard`的用法，我们的`springboot`项目就可以运行在`k8s`中了，然后剩下的更细节的知识点就靠各位小伙伴自己去探索学习了。好了，今天的内容就到这里了。

