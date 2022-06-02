# manjaro搭建k8s集群环境

### 前言

最近西安疫情有点严重，现在已经是全城管控的局面了，这里要向奋战在抗疫一线的医务人员和各位大可爱和小可爱们，表达最衷心的感谢，这么冷的天，依然要坚守工作岗位，确实太不容易了，所以请一定要保护好自己哦！

居家办公最尴尬的一点是，在本地调试代码的时候，本地内存根本扛不住，一个操作卡半天，效率根本起不来，所以为了缓解这种比较尴尬的情况，我想在家里的旧电脑上搭建一套`k8s`集群，方便开发测试。废话不多说，下面我们直接开干！



### 搭建k8s集群

上次我们其实已经分享过在`wsl`环境构建`k8s`集群的内容了，有所不通的是，`manjaro`是纯正的`linux`环境，配置过程要简单一点。

#### 更新系统

首先将软件包更新到最新版本

```
sudo pacman -Syu 
```



![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/manjaro/image-20211225143139622.png)

#### 安装docker

`k8s`的镜像管理是要基于`docker`的，所以要先安装`docker`，简简单单一行命令搞定：

```
 sudo pacman -S docker
```

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/manjaro/20211225165714.png)

##### docker配置

这里主要是添加`daemon.json`文件

```sh
sudo vim /etc/docker/daemon.json
```

文件内容如下，主要是为了提高我们拉取镜像的速度:

```json
{
  "registry-mirrors": ["https://docker.mirrors.ustc.edu.cn/", "https://hub-mirror.c.163.com/", "https://reg-mirror.qiniu.com"],
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2"
}
```



##### 服务管理

这里是`docker`服务的一些常用操作，不想通过`sudo`操作的小伙伴可以自行百度处理。

```sh
# 启动 docker
sudo systemctl start docker 
# 重启 docker
sudo systemctl restart docker 
# 停止 dokcer
sudo systemctl stop docker 
# 查看docker服务的状态
sudo systemctl status docker
# 设置docker开机启动服务
sudo systemctl enable docker
```



#### 安装kubelet、kubeadm、kubectl

`kubelet`、`kubeadm`、`kubectl`都是`k8s`的核心组件，特别是`kubectl`，我们创建服务、管理服务都要用到它。

```
sudo pacman -S kubelet kubeadm kubectl
```

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/manjaro/20211225165803.png)

##### 下载安装kind

`kind`是一款比较流行的`k8s`集群管理工具，因为上次我用的它，所以这次依然用它。

首先，我们要下载`kind`，直接按照官网给的教程开始：

```sh
# 下载kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.11.1/kind-linux-amd64
# 添加执行权限
chmod +x ./kind
# 移动到
sudo mv ./kind /usr/local/kind
```

然后`kind`就安装完成了，详细官方文档地址如下

```
https://kind.sigs.k8s.io/
```

##### 配置镜像

在`ubuntu`环境下可以参考我们之前的内容，添加阿里云的镜像地址，这里我就用最原始的方式操作了。

首先我们创建一个`yaml`文件，名称可以随便起，我这里叫`kind.yaml`，填入如下内容：

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
networking:
  apiServerAddress: "192.168.0.102"
containerdConfigPatches:
- |-
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
    endpoint = ["https://tiaudqrq.mirror.aliyuncs.com"]
```

这里解释下，`apiServerAddress`配置的是当前机器的`ip`，其他的配置可以不用改，`endpoint`是我们镜像仓库的镜像地址。



##### 创建k8s集群

`k8s`的常用命令，可以看下之前的内容，链接我放在文末了。到这里，创建集群就很简单了，直接执行下面的命令即可：

```sh
sudo ./kind create cluster --name syske-k8s --config kind.yaml
```

这里的`kind.yaml`就是我们前面创建的文件，然后就是漫长的等待，如果不出意外，最后会显示创建成功，如果一直创建不成功，可以考虑换下仓库镜像地址：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/manjaro/20211225165503.png)

我们通过下面的命令看下节点信息：

```
kubectl cluster-info --context kind-wslk8s
```

显示信息如下：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211226224511.png)

然后我们访问如下地址看下

```
https://127.0.0.1:39879/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211226224621.png)

虽然显示结果有点问题，但是也说明集群创建成功，关于安装`kuboard`的操作可以直接看下之前的内容，链接如下：







### 结语

最近一周一直是居家办公，但是特别想吐槽的是，居家办公比上班累多了，因为在家办公除了办公还是办公，一天有开不完的会，而且周末还要帮其他项目救火，这就很离谱，所以也正因此，最近好多内容都没顾得上梳理，多线程这块的一些内容也没来得及总结，只能先放一下。

不过，在搭建`k8s`的过程中，顺手搭建了`harbor`平台，后面得空了分享下，这里简单解释下`harbor`，它是一个镜像的私服开源项目，通过在`harbor`我们可以构建自己的内网环境下的镜像服务器，比如公司自己的项目都可以放在上面管理，一方面更安全，另一方面拉取镜像更快，最后我们先放上`harbor`的靓照：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211226230559.png)![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211226230636.png)