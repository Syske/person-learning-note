# k8s整合kuboard，让我们更愉快地进行k8s管理

### 前言

最近几天，我们一直都在和`k8s`打交道，前天分享了`wsl`搭建`k8s`集群的完整过程，昨天我们补充了一些`k8s`的基础命令，今天我们继续来介绍`k8s`，今天分享的就是我们昨天安利的`k8s`的管理工具`kuboard`。前面说，`kuboard`不能通过代理的方式访问，所以没法正常登录，但是今天我又看了下`kuboard`的官方文档，发现可以通过`docker`的方式运行`kuboard`，下面我们就看下具体如何操作。

### kuboard

#### 安装kuboard

我们直接打开`wsl`，启动`docker`服务，然后在`docker`中安装`kuboard`，开始前建议你先拉取`kuboard`的镜像，具体命令如下：

```sh
# 拉取kuboard镜像
docker pull eipwork/kuboard:v3
# 启动kuboard
sudo docker run -d \
  --restart=unless-stopped \
  --name=kuboard \
  -p 80:80/tcp \
  -p 10081:10081/tcp \
  -e KUBOARD_ENDPOINT="http://内网ip:80" \
  -e KUBOARD_AGENT_SERVER_TCP_PORT="10081" \
  -v /root/kuboard-data:/data \
  eipwork/kuboard:v3
```

大家注意下面启动命令中的内网`ip`，根据官方文档说明，这个`ip`不建议使用 `127.0.0.1` 或者 `localhost` ，所以我用的`ip`地址是`127.0.0.2`，你可以和我保持一致

![](https://gitee.com/sysker/picBed/raw/master/images/20210628125008.png)

然后运行上面的脚本，建议将上面的脚本存储成`sh`脚本，方便后续启动使用，这是我的`sh`脚本内容：

![](https://gitee.com/sysker/picBed/raw/master/images/20210628125225.png)

#### 测试

启动成功后，我们可以在`wsl`控制台通过如下命令测试`kuboard`启动是否成功：

```sh
curl 127.0.0.2:80
```

这里的`127.0.0.2`就是我们前面配置的内网`ip`，如果启动正常，应该会返回这样的内容：

![](https://gitee.com/sysker/picBed/raw/master/images/20210628125605.png)

这时候如果你`curl 127.0.0.1:80`也是可以正常返回的，而且返回内容和上面的是一样的：

![](https://gitee.com/sysker/picBed/raw/master/images/20210628130148.png)

到这里`kuboard`就启动成功了，这时候我们就可以在`windows`的浏览器中通过`127.0.0.1:80`访问`kuboard`：

![](https://gitee.com/sysker/picBed/raw/master/images/20210628095610.png)

默认的登录信息如下：

- 用户名： `admin`
- 密 码： `Kuboard123`

第一次访问因为我们还没有添加`k8s`集群信息，控制台是没有任何数据展示的，所以我们要先添加`k8s`集群

![](https://gitee.com/sysker/picBed/raw/master/images/20210628133051.png)

#### 添加k8s配置

点击添加集群，然后填入集群信息，点击确认：

![](https://gitee.com/sysker/picBed/raw/master/images/20210628133211.png)

然后复制下面的命令，先复制第一行：

![](https://gitee.com/sysker/picBed/raw/master/images/20210628133329.png)

在`k8s`集群的集群上执行：

```sh
curl -k 'http://127.0.0.2:80/kuboard-api/cluster/wsl-k8s/kind/KubernetesCluster/wsl-k8s/resource/installAgentToKubernetes?token=BpLnfgDsc2WD8F2qNfHK5a84jjJkwzDk' > kuboard-agent.yaml
```

这里其实就是生成了一个探针文件，然后我们需要把这个探针文件导入到`k8s`中，在导入之前我们需要先修改下这个`yaml`文件：

```
vim kuboard-agent.yaml
```

在文件中找到`KUBOARD_ENDPOINT`和`KUBORAD_AGENT_HOST`，把下面的`value`中的`ip`改成我们`wsl`中`docker`的地址，具体如何获取，后面有说明。

![](https://gitee.com/sysker/picBed/raw/master/images/20210628151309.png)

`KUBOARD_ENDPOINT`和`KUBORAD_AGENT_HOST`有两处，都要修改，否则在创建探针服务的时候会报错，创建探针服务的命令如下，也就是页面上的第二行命令：

```sh
kubectl apply -f kuboard-agent.yaml
```

如果不修改上面的地址，回报下面的错，也就是获取`TOKEN`的时候，地址访问不到：

![](https://gitee.com/sysker/picBed/raw/master/images/20210628150355.png)

为什么要改成`docker`的地址，因为我们的`kuboard`部署在`dokcer`环境下，下面我们看下如何查看`wsl`环境下`docker`的`ip`地址。

#### 查看wsl的docker内网ip

因为`wsl`默认是不支持`ifconfig`命令的，我们可以使用下面的命令看下`linux`主机的`ip`:

```sh
ip addr
```

在显示结果中，找到`docker0`网卡，其中的`ip`地址就是我们需要的`ip`，如下图，我的`docker ip`是`172.18.0.1`

![](https://gitee.com/sysker/picBed/raw/master/images/20210628110355.png)

然后把`kuboard-agent.yaml`修改后，重新执行创建命令：

```
kubectl apply -f kuboard-agent.yaml
```

再次访问`kuboard`，你会发现我们的集群已经导入成功：

![](https://gitee.com/sysker/picBed/raw/master/images/20210628152402.png)

这时候，我们在面板的右侧选择管理角色后，就可以进入我们的`k8s`集群管理中心了：

![](https://gitee.com/sysker/picBed/raw/master/images/20210628153125.png)

![](https://gitee.com/sysker/picBed/raw/master/images/20210628153155.png)

到这里我们今天的内容就结束了，关于`kuboard`的使用，我们下次再说。

### 总结

今天，我们主要分享了如何通过`kuboard`来管理我们`wsl`环境下的`k8s`集群，过程还算顺利，之前无法访问是因为`windows`的网络与`k8s`集群无法通信，所以我们无法通过浏览器直接访问`k8s`中的应用，现在我们把`kuboard`部署在`docker`中，这个问题自然而然就解决了。至于网络无法互通的问题，我打算通过`nginx`来解决，这块的问题一定要解决，否则我们只能通过代理的方式来访问，但问题是有些服务还不支持代理访问，比如`kuboard`，这两天有时间先试下，如果搞定了，到时候再来分享。

 `kuboard`作为一款`k8s`管理工具，单从`UI`层面来说，已经比官方提供的`board`优秀了很多，当然主要是`kuboard`本身就很优秀，截至到目前，这个项目`github`已经有`10K+`的`start`，有兴趣的小伙伴可以自己先去了解下，我们后面再将`kuboard`的一些基本用法。