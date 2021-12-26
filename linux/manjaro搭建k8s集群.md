# manjaro搭建k8s集群环境

### 前言

最近西安疫情有点严重，现在已经是全城管控的局面了，只能居家办公，但是在本地调试代码的时候，本地内存根本扛不住，所以为了缓解这种比较尴尬的情况，我想在家里的旧电脑上搭建一套`k8s`集群，方便开发测试。废话不多说，下面我们直接开干！



### 搭建k8s集群

#### 更新系统

首先将软件包更新到最新版本

```
sudo pacman -Syu 
```



![](https://gitee.com/sysker/picBed/raw/master/manjaro/image-20211225143139622.png)

#### 安装docker

```
 sudo pacman -S docker
```

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211225165714.png)

##### 服务管理

```sh
sudo systemctl start docker 
sudo systemctl restart docker 
sudo systemctl stop docker 
# 查看docker服务的状态
sudo systemctl status docker

# 设置docker开机启动服务
sudo systemctl enable docker
```



#### 安装kubelet、kubeadm、kubectl

```
sudo pacman -S kubelet kubeadm kubectl
```

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211225165803.png)

##### 下载安装kind

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

```
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
networking:
  apiServerAddress: "192.168.0.102"
containerdConfigPatches:
- |-
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
    endpoint = ["https://tiaudqrq.mirror.aliyuncs.com"]
```



##### 创建k8s集群

`k8s`的常用命令，今天就不讲了，后面梳理下再分享，今天只分享流程。

到这里，创建集群就很简单了，直接执行下面的命令即可：

```
sudo ./kind create cluster --name syske-k8s --config kind.yaml
```

然后就是漫长的等待，如果不出意外，最后会显示创建成功：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211225165503.png)

我们通过下面的命令看下节点信息：

```
kubectl cluster-info --context kind-wslk8s
```

显示信息如下：![](https://gitee.com/sysker/picBed/raw/master/images/20210626193717.png)

然后我们访问如下地址看下

```
https://127.0.0.1:45187/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```

![](https://gitee.com/sysker/picBed/raw/master/images/20210626193814.png)

![](https://gitee.com/sysker/picBed/raw/master/images/image-20210626193842066.png)

虽然显示结果有点问题，但是也说明集群创建成功，下面我们安装`k8s`控制台。