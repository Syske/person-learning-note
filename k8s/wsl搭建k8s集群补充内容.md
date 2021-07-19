## wsl搭建k8s集群补充内容

### 前言

昨天我们分享了如何在`wsl`上搭建`k8s`集群，但是由于内容多，昨天时间也比较紧促，所以好多知识点并没有覆盖到，考虑到好多小伙伴可能也是第一次使用`k8s`，我们今天把一些基础知识再补充下，一方面是为了让大家清楚每一步操作的目的，清楚每一个命令的作用，另外一方面就是我自己确实也需要把这这两天积累的基础知识整理下，理清楚思路，便于知识积累。

### k8s补充知识

#### 查看基本信息

```sh
kubectl get option optionName [-n][-namespace] [namespaceName]
```

![](https://gitee.com/sysker/picBed/raw/master/20210627132002.png)

这个命令的作用是获取`option`的信息，`option`可以是`node`、`pod`、`service`，在获取`pod`和`service`的时候，是需要通过`－namespace`指定命名空间的;

`service`和`namespace`可以写成简写的：

```sh
kubectl svc -n 命名空间名称
```

如果要获取具体的`option`，可以指定`optionName`

![](https://gitee.com/sysker/picBed/raw/master/20210627134949.png)

如果要获取所有命名空间下的`svc`或者`pod`，可以通过：

```sh
kubectl get svc -A
# 或者
kubectl get pod -A
```

![](https://gitee.com/sysker/picBed/raw/master/20210627132707.png)

![](https://gitee.com/sysker/picBed/raw/master/20210627132927.png)

![](https://gitee.com/sysker/picBed/raw/master/20210627133004.png)

我们通常访问的是`service`，所以最常用的是`kubectl get svc -n kubernetes-dashboard`通过这个命令，我们可以查看服务对外提供的端口。

#### 查看详细信息

```sh
kubectl describe option [-n][-namespace] [namespaceName]
```

这里的参数和前面`kubectl get`是一样的，只是`describe`获取到的信息更详细，包括日志信息，所以在实际使用过程中，我们经常用这个命令查看日志信息：

![](https://gitee.com/sysker/picBed/raw/master/20210627134130.png)

![](https://gitee.com/sysker/picBed/raw/master/20210627135229.png)

![](https://gitee.com/sysker/picBed/raw/master/20210627135404.png)

#### 创建服务

```
kubectl apply -f 你的yaml文件
```

比如创建`kuboard`

```sh
kubectl apply -f https://addons.kuboard.cn/kuboard/kuboard-v3.yaml
```

上面这种方式是通过线上`yaml`文件，你也可以用本地`yaml`文件创建：

```sh
kubectl apply -f kuboard/kuboard-v3.yaml
```

`yaml`文件结构如下：

![](https://gitee.com/sysker/picBed/raw/master/20210627145111.png)

对于`k8s`的`yaml`文件，我目前只了解常用的节点的作用，还不知道如何编写一个`yaml`文件，但是如果你用了`kuboard`这样的管理工具之后，是不需要自己编写`yaml`文件的。

#### 删除服务

删除服务也很简单，只需要把上面的命令改成`delete`即可：

```sh
kubectl delete -f https://addons.kuboard.cn/kuboard/kuboard-v3.yaml
```

如果没有`yaml`文件，删除起来确实繁琐了很多

#### `k8s`代理

昨天我们访问`kubernetes-dashboard`就是通过代理的方式，启用代理的方式也很简单，直接执行下面的命令就好了：

```sh
kubectl proxy
```

![](https://gitee.com/sysker/picBed/raw/master/20210627141018.png)

`k8s`代理启动后，我们就可以通过代理服务访问我们`k8s`里面的服务了，访问地址如下：

```
http://localhost:8001/api/v1/namespaces/[Namespace]/services/[Name]:[Port]/proxy/
```

我们把将地址中的`[namespace]`、`[name]`和`[port]`替换成我们自己的服务就可以了。我们可以通过`describe`命令获取这些信息：

![](https://gitee.com/sysker/picBed/raw/master/20210627142456.png)

所以上面图片中的服务，访问地址是这样的：

```
http://localhost:8001/api/v1/namespaces/kuboard/services/kuboard-v3:80/proxy/
```

![](https://gitee.com/sysker/picBed/raw/master/kuboard-login.png)

这个服务也是一个控制台，这个控制台是国人开发的，很多公司线上环境就用的这款管理工具，我们公司也是刚刚切换到`k8s`，也用的是`kuboard`，从体验上来说，确实比官方的控制台好用，可能也是我用官方的管理工具时间短。

![](https://gitee.com/sysker/picBed/raw/master/20210627143544.png)

关于`kuboard`的使用，今天我们就不分享了，因为`kuboard`本身不支持代理访问，虽然能登陆上，但是后面访问的时候，会报404的错误：

![](https://gitee.com/sysker/picBed/raw/master/20210627150451.png)

主要还是地址的问题，我们代理之后服务的根目录应该是：

```
http://localhost:8001/api/v1/namespaces/kuboard/services/kuboard-v3:80/proxy/服务资源
```

但是`kuboard`要求的服务根目录是：

```
http://localhost:8001/服务资源
```

所以会报`404`错误，后面我们解决了`windows`外网直接访问`wsl`中的`k8s`集群服务的问题，再来分享。

#### 关于k8s

现阶段`k8s`应该算是云原生比较主流的技术，得益于`Go`语言和`Linux`加持，`k8s`确实比`docker`更适合企业大型应用的集群部署，因为`k8s`有着`docker`无法替代的功能，比如`k8s-dns`，虽然`k8s`要依赖`docker`进行镜像管理，但是比`docker`更庞大。

这里有一个形象的例子，可以说明我对`k8s`和`docker`的理解。`docker`中文的意思是码头工人，我们的系统镜像就好比货物，所以`docker`可以帮我们需要的系统镜像（货物），装卸到我们需要的地方，就类似于搬运工人；`k8s`就相当于自动化港口，一个是规模更大，可以停放更大船舶，更多的货物；一个是自动化程度更高，集成程度也更高，我们不需要像搬运工人再去手动（`docker pull`）搬运货物（系统镜像），只需要在`k8s`控制台操作一下，货物就会自动装卸，然后还可以实时监测各个系统状况，不仅效率高，而且容错机制还好，如果某个节点无响应或者响应数据不正常，`k8s`会根据重启机制，重启我们的`pod`节点，从这一点上说，`k8s`确实比`docker`优秀。

当然，任何事物都不可能完美，虽然`k8s`看起来无懈可击，但是在实际使用过程中，你可能会遇到各种各样的坑，比如如果你的服务启动时间比较长，`k8s`就以为你的服务假死，然后重启服务，这样你的服务会一直被重启，而且一直起不来。当然，这样说明确实`k8s`是为微服务量身打造的，因为如果你的服务启动时间长，就说明你的服务还不够微。

总之，`k8s`虽然有一些缺点，但是和它的优点相比，那确实比较优秀了，而且随着不断的深入了解，你会发现`k8s`很多地方设计的牛逼，对开发人员确实很友好。最后，感兴趣的小伙伴，好好去把玩下吧，我觉得你会喜欢上这个东东的……

### 总结

今天我们补充了`k8s`的一些常用命令，通过这些命令，我们可以管理我们`k8s`集群下的服务，查看服务的状态、日志等，虽然作为开发人员我们真正要用好的是像`kuboard`这样的工具，因为日常工作中我们一般并不会拥有`kubectl`控制台的权限，但是我还是建议各位小伙伴要学好`k8s`的基础知识，只有如此你才能更好地理解`k8s`的运行原理，才能站在更高的高度看问题，你说呢？

