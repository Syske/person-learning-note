# kuboard简单使用

### 前言

昨天我们分享了本地`springboot`项目构建`docker`镜像的内容，详细介绍了`springboot`项目打包、镜像构建、基于`docker`启动运行的全过程，这个技术虽然不是特别难，但是很实用，因为镜像构建完成后，我们不仅可以让我们的服务在`docker`中运行，也可以让它在`k8s`中运行，今天我们就来看下如何通过`kuboard`在`k8s`上部署我们的服务。

今天的内容以图片为主，文字说明为辅，只有大家按照我的操作流程进行操作，一定也可以部署成功。好了，话不多说，让我们直接开始吧。

### kuboard

#### 登录kuboard控制台

在开始之前，我们要先登录`kuboard`的控制台，然后选择需要部署服务的`k8s`集群：

![](https://gitee.com/sysker/picBed/raw/master/images/20210630130746.png)

选择登录角色，这里我们直接以管理员角色登录：

![](https://gitee.com/sysker/picBed/raw/master/images/20210630130822.png)

进入对应集群后，选择要部署服务的命名空间。在`k8s`中，所有的`pod`、`service`都是基于命名空间进行管理的，而且一个工作空间下的服务可以直接通过负载名称进行访问，如果跨命名空间访问服务，需要加上对应的命名空间名称。

这里我们选的是默认的工作空间`default`，点击命名空间即可进入命名空间内部：

![](https://gitee.com/sysker/picBed/raw/master/images/20210630130858.png)

#### 创建服务

在命名空间内部，我们可以构建我们的工作负载（大家要慢慢习惯这个叫法）。点击中间的悬浮菜单`常用操作`

![](https://gitee.com/sysker/picBed/raw/master/images/20210630130948.png)

在展开的选项中选择`创建工作负载`菜单，进入工作负载创建页面

![](https://gitee.com/sysker/picBed/raw/master/images/20210630131016.png)

##### 填写负载基本信息

首先填写工作负载的基本信息。工作负载类型我们选择第一个`部署`，通常我们的服务和组件都选择这个；工作负载分层可以根据自己的服务类型进行选择，这个选项只是为了方便管理，分层之后会在控制面板的不同区域显示

![](https://gitee.com/sysker/picBed/raw/master/images/20210630131104.png)

工作负载的名称要唯一，不能重复，而且不能有中文，后面我们访问服务的时候就是通过`负载名称+端口`进行访问的，描述信息可以随便填写

![](https://gitee.com/sysker/picBed/raw/master/images/20210630131202.png)

##### 填写容器信息

基本信息填写完成后，切换到容器信息填写页面。这里创建容器，经过我的试验，初始化容器可以不创建，但是工作容器必须创建，否则无法提交表单

![](https://gitee.com/sysker/picBed/raw/master/images/20210630131246.png)

我们直接创建工作容器，然后填写容器信息。这里的容器名称，一般和基本信息保持一致就行了，虽然没有要求，但是不一致的话，不利于后期管理；这一块的配置中，容器镜像是最重要的内容，而且要确保镜像存在，否则在后面容器启动的时候会报错。

![](https://gitee.com/sysker/picBed/raw/master/images/20210630132047.png)



这里的镜像配置的内容和我们`docker pull 镜像名称`的镜像名称是一样的，我们以`zookeeper`为例，我们拉取镜像的命令是这样的：

```
docker pull zookeeper:latest
```

所以我们这里配置的就是`zookeeper:latest`；大家注意右侧的`imagePullSecret`配置，这个配置是方便我们配置私有镜像仓库，例如很多公司都基于`harbor`搭建了私有的镜像仓库，这里就配置`harbor`的配置。

![](https://gitee.com/sysker/picBed/raw/master/images/20210630132906.png)

然后，记得指定下容器的端口，否则我们是服务访问容器中的服务或组件的。

镜像的拉取策略，设置的是拉取的条件，第一个选项始终拉取新镜像，表示任何时候只要你重启了容器都会从镜像仓库拉取镜像，不论本地是否已经有镜像；第二个选项表示当本地没有镜像的时候，才拉取镜像；第三个选项表示从不拉取镜像，但当镜像不存在则会报错。大家可以根据自己的需要设置，一般对于第三方组件，或者不经常变更的镜像，我们都选择第二个。

![](https://gitee.com/sysker/picBed/raw/master/images/20210630132002.png)

##### 配置服务路由

这里也是很关键的一步，如果不设置路由的话，我们是没办法通过负载名称访问服务的，虽然通过`ip`地址也能访问，但是容器重启后，`ip`地址会发生变化，所以必须配置路由。

这里只需要选择`clusterIP`，然后指定端口映射即可

![](https://gitee.com/sysker/picBed/raw/master/images/20210630143649.png)

##### 服务控制面板

点击保存后，会进入服务的控制面板，控制面板处理常用的操作菜单外，还会显示服务的运行状况信息：

![](https://gitee.com/sysker/picBed/raw/master/images/20210630132344.png)

如果在右侧事件显示区域，有如下显示，表明你的服务镜像配置有误，可以点击编辑菜单进行修改：

![](https://gitee.com/sysker/picBed/raw/master/images/20210630135059.png)

有时候页面内容长时间为变化，可以点击上部的刷新菜单进行刷新。如果提示容器已就绪，说明我们的服务已经部署启动成功，这时候我们可以点击容器下部的菜单对容器进行管理。

![](https://gitee.com/sysker/picBed/raw/master/images/20210630132516.png)

追踪日志菜单可以实时展示容器中服务的日志信息，点击后会打开新页面，内容显示如下，页面支持搜索，还可以设置是否滚动

![](https://gitee.com/sysker/picBed/raw/master/images/20210630132557.png)

`bash`和`sh`没有本质区别，都是进入容器的`linux`控制台，点击对应菜单后，会打开如下页面

![](https://gitee.com/sysker/picBed/raw/master/images/20210630132639.png)

下载日志菜单，可以下载容器中的日志文件，也就是我们跟踪日志显示的日志，可以根据自己的需要进行下载：

![](https://gitee.com/sysker/picBed/raw/master/images/20210630132703.png)

##### 补充内容

下面这张图片很好地展示了配置路由器和配置路由后的访问情况，配置路由前，我们访问`activemq-k8s`，提示无法解析主机，但当我们添加路由配置后，再次访问，发现这时候`activemq-k8s`已经可以正常解析了，而且返回了页面内容。![](https://gitee.com/sysker/picBed/raw/master/images/20210630143827.png)

为了更好地测试命名空间内服务间的通信，我这里构建了两个服务，一个是`zk`，一个是`mq`，然后在`mq`的控制台访问`zookeeper-k8s`，虽然无法正常访问，但可以看到名称已经被正常解析，说明路由是没有问题的

![](https://gitee.com/sysker/picBed/raw/master/images/20210630144151.png)

在`zk`控制台访问`activemq-k8s`效果也是一样的，由于容器的`linux`没有`ping`和`curl`，我只能用`wget`命令了：

![](https://gitee.com/sysker/picBed/raw/master/images/20210630144518.png)

#### 容器配置导出

最后，我们再讲一下容器的导出。导出主要是为了备份，如果特殊原因导致`k8s`崩溃（前段时间，我们测试环境就发生过，有人把`k8s`集群搞坏了，然后集群被删除了），这时候如果从头再配置，不仅浪费时间，而且好多配置你也记不清楚了。

但如果你之前备份过，那直接可以通过备份的`yaml`文件重新构建容器，这样效率更高，而且不容器出错。上次一也是因为我提前备份过，所以除了我们项目，其他组都花了好久才把环境重新部署好。

备份的方式也很简单，首先命名空间首页，点击悬浮菜单，选择导出工作负载

![](https://gitee.com/sysker/picBed/raw/master/images/20210630133014.png)

![](https://gitee.com/sysker/picBed/raw/master/images/20210630133058.png)

选择需要导出的负载

![](https://gitee.com/sysker/picBed/raw/master/images/20210630133117.png)

下一步，然后选择需要导出的服务

![](https://gitee.com/sysker/picBed/raw/master/images/20210630133204.png)

然后一直下一步，最后点击确认，到这里负载文件就导出完成了。

![](https://gitee.com/sysker/picBed/raw/master/images/20210630133255.png)

导出的文件长这个样子，是标准的`yaml`文件

![](https://gitee.com/sysker/picBed/raw/master/images/20210630133343.png)

#### 导入负载

导入负载也很简单，导入方式有两种，第一种直接点击左侧导入工作负载菜单，然后选择导入文件，点击确定就可以了，剩下的就是等待，等待容器启动完成。

![](https://gitee.com/sysker/picBed/raw/master/images/image-20210630133433834.png)

另一种方式是点击左侧从`yaml`创建菜单，这里主要是针对单个负载，多个负载我没有试过。

![](https://gitee.com/sysker/picBed/raw/master/images/20210630133451.png)

然后把我们负载`yaml`内容赋值进去，点击确定即可，然后也是漫长的等待。

![](https://gitee.com/sysker/picBed/raw/master/images/20210630133541.png)

好了，到这里，今天的内容就全部结束了，图片虽然多，但是都是实打实的干货，有条件的小伙伴自己动手试下吧。

### 总结

今天我们主要分享了基于`kuboard`管理`k8s`容器的一些基本的常用操作，包括服务部署、日志查看、负载导入导出等，虽然简单但是很实用。

总体来说，`kuboard`确实比`k8s`官方的控制台体验要好，除了颜值高，功能也很强大，而且又是原生的中文支持，确实很香。

最后我想说，`k8s`确实要比`docker`优秀，这个最大的体会来源于`k8s`的伸缩特性，在`docker`中，创建第一个容器和创建第二个容器一样复杂，一样的麻烦，但是在`k8s`中，创建第二个容器只需要把副本数改为`2`，想创建多少个都可以，既简单又方便，而且很灵活，反正就是很强。更多特性，后面有机会的话再来分享，今天就到这里吧！

