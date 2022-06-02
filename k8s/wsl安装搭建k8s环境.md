# wsl安装搭建k8s环境

### 前言

最近一周，一直在捣鼓基于`wsl2`搭建`k8s`集群的问题，试了好久才终于把集群环境搞好，然后又花了两天时间，才搞清楚服务如何访问，感觉这应该是我工作以来，摸索问题最久的一次了，这两天更是肝到一点（忙起来。感觉时间过的好快），这执着的精神是值得肯定，但是也说明我确实对`k8s`还处在初学阶段，未来可能还有好多坑要踩，不过能走出这第一步，我觉得未来的困难也会被我踩在脚下的。

不过，通过昨天晚上和今天集群的创建，我发现`k8s`集群创建这块的经验和思路已经很成熟了，所以就想趁着这股热劲，把自己的经验分享下，供大家参考，为了搞清楚`k8s`，连`ubuntu`我都安装了好几个：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210626172621.png)

今天我们演示内容是基于`ubuntu 20.04`展开的，内容有点多，我们直接开始正文吧。



### 正文

#### 启用wsl

关于`wsl`的启用，我们上次（前天）已经分享过了，不清楚的小伙伴爬楼看下，后期考虑把这一块的内容再细化下。暂时可以参考微软官方文档：

```
https://docs.microsoft.com/zh-cn/windows/wsl/
```

启用成功后，打开我们的`wsl`：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210626173445.png)

后期，我们分享如何美化这里的终端窗口。

#### 配置系统

##### 修改系统更新源

经常使用`Linux`的小伙伴应该知道，我们在安装完`Linux`第一步都是修改更新源。所以`wsl`安装完成后，我们首先也是要修改系统更新源的地址，官方默认地址国内更新比较慢，我们改成阿里巴巴的镜像地址，就快多了。

我们要把如下地址添加到`/etc/apt/sources.list`文件中，并将原来的地址注释掉：

```sh
deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
```

编辑命令我们直接用`vim`，默认已经安装好了：

```sh
sudo vim /etc/apt/sources.list
```

这里用`sudo`是因为当前用户不是`root`账户，如果登录的是`root`账户，就不需要加`sudo`，不过加了也不影响，下面的命令也是一样的，后面就不再说明了，`#`表示注释该行数据。

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210626174648.png)

修改完镜像后，我们通过如下命令更新下系统：

```sh
sudo apt update & sudo apt upgrade
```

前面的命令是更新软件列表，后面的命令是安装更新，也可以分开执行（感觉我说的好细呀），然后静静等待更新完成：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210626175103.png)

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210626175201.png)

##### `daemonize`安装配置

安装`daemonize`是为了让我们的`wsl`支持`systemctl`命令，然后激活`Systemd `，这些命令在后面启动`docker`服务、创建集群的时候都要用到。

安装命令也很简单（我一直觉得`linux`安装软件比`windows`方便，一行命令就完成安装，它不香吗）：

```sh
sudo apt install daemonize #第二种方式执行
sudo apt install -yqq fontconfig daemonize # 第一种方式需要执行
```

因为我已经安装过了，显示得可能和你不一样：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210626175913.png)

这里有两种方式。需要注意的是第一种方式需要多安装一个软件包：`fontconfig`

###### 第一种方式

第一种方式需要创建一个脚本，我们直接通过`vim`创建：

```sh
sudo vim /etc/profile.d/00-wsl2-systemd.sh
```

然后将如下内容写入，保存

```sh
# Create the starting script for SystemDvi /etc/profile.d/00-wsl2-systemd.sh
SYSTEMD_PID=$(ps -ef | grep '/lib/systemd/systemd --system-unit=basic.target$' | grep -v unshare | awk '{print $2}')
if [ -z "$SYSTEMD_PID" ]; then   
  sudo /usr/bin/daemonize /usr/bin/unshare --fork --pid --mount-proc /lib/systemd/systemd --system-unit=basic.target   
  SYSTEMD_PID=$(ps -ef | grep '/lib/systemd/systemd --system-unit=basic.target$' | grep -v unshare | awk '{print $2}')
fi
if [ -n "$SYSTEMD_PID" ] && [ "$SYSTEMD_PID" != "1" ]; then 
   exec sudo /usr/bin/nsenter -t $SYSTEMD_PID -a su - $LOGNAME
fi
```

然后关闭当前`Terminal`，重新打开。

###### 第二种方式

下面是第二种方式，这行命令是为了激活我们的`systemd`命令

```sh
sudo daemonize /usr/bin/unshare --fork --pid --mount-proc /lib/systemd/systemd --system-unit=basic.target
```

###### 注意

我推荐第一种，第二种虽然第一次是`ok`的，但是在实际使用中发现，`wsl`重启后（或者电脑重启），第二种方式执行`docker`和`k8s`命令的时候，会报下面的错，而且我还没找到解决方案：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210626184940.png)

具体情况，各位小伙伴可以自己试验下。

#### 安装Docker

这里安装的是`Linux`原生的`docker`，并非是基于`windows`环境的，安装完成后，你就可以在`wsl`使用原生的`docker`了

##### 安装依赖

安装软件包以允许 `apt `通过 `HTTPS `使用存储库

```sh
# 安装 Docker CE
## 设置仓库
### 安装软件包以允许 apt 通过 HTTPS 使用存储库
sudo apt-get update && sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
```

这里是安装多个软件的方式，上面总共安装了四个软件包，软件包直接用空格分割。

##### 添加docker官方发密钥

```sh
### 新增 Docker 的 官方 GPG 秘钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

##### 添加`docker`镜像地址

```sh
### 添加 Docker apt 仓库
add-apt-repository \
  "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) \
  stable"
```

这里会把它添加进`/etc/apt/sources.list`文件中。

##### 安装docker

和上面一样，安装多个软件。

```sh
## 安装 Docker CE
sudo apt-get update && sudo apt-get install containerd.io   docker-ce   docker-ce-cli -y
```

##### 配置docker

这里主要是设置`docker`的镜像仓库的镜像地址（有点绕，主要是国内下载镜像慢，所以需要改成网易等国内的镜像地址）

```sh
sudo vim /etc/docker/daemon.json
```

前面忘记说了，加`sudo`就是以管理员运行，因为`/etc`文件夹权限比较高，普通用户是没法修改的。然后加入如下内容：

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

##### 启动docker

如果前面安装`daemonize`采用的第一种方式，就通过下面的方式启动`docker`：

```sh
# 启动
service docker start
# 重启
service docker restart
# 停止
service docker stop
```

否则下面的命令，如果上面这种方式无法启动，也可以通过下面的命令试下（万一好了呢，病急乱投医呗）：

```sh
mkdir -p /etc/systemd/system/docker.service.d

# 重启 docker.
systemctl daemon-reload
# 重启
systemctl restart docker
# 启动
systemctl start docker
```



#### 安装 kubelet、kubeadm、kubectl

##### 添加官方 GPG 秘钥

这里添加的是阿里巴巴的镜像密钥

```sh
sudo apt-get update && sudo apt-get install -y apt-transport-https
curl https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | sudo apt-key add -
```

然后把下面的地址加到我们的软件更新列表中：

```sh
sudo vim /etc/apt/sources.list.d/kubernetes.list
```

第一次打开应该是空的，因为这个文件是我们刚创建的:

```sh
deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
```

添加完成后，我们更新下软件列表数据：

```sh
sudo apt-get update
```

更新完成后，安装`k8s`软件包：

```sh
sudo apt-get install -y kubelet kubeadm kubectl
```

因为我已经安装过了，所以提示已经安装过了，根据提示信息我们发现安装的版本应该是`1.21.1`，应该是最新版本了。

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210626191049.png)

#### 创建k8s集群

创建集群的方式有多种，目前我了解到的有两种，一种是用`kubeadm `，一种是用`kind`，经过多次尝试，我发现第一种方式在`wsl`下始终无法成功，刚开始是不支持`swap`交换分区，忽略这个错误后，又有其他错误，一直没跑通，所以本文我们采用后一种，即`kind`。

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210626191506.png)

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

##### 创建k8s集群

`k8s`的常用命令，今天就不讲了，后面梳理下再分享，今天只分享流程。

到这里，创建集群就很简单了，直接执行下面的命令即可：

```
kind create cluster --name wslk8s
```

然后就是漫长的等待，如果不出意外，最后会显示创建成功：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210626193509.png)

我们通过下面的命令看下节点信息：

```
kubectl cluster-info --context kind-wslk8s
```

显示信息如下：![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210626193717.png)

然后我们访问如下地址看下

```
https://127.0.0.1:45187/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210626193814.png)

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/image-20210626193842066.png)

虽然显示结果有点问题，但是也说明集群创建成功，下面我们安装`k8s`控制台。

#### 安装图形化控制面板

执行如下命令创建`Dashboard`节点

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.1/aio/deploy/recommended.yaml
```

上面的命令就是根据`yaml`构建我们的`k8s`节点

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210626194249.png)

然后通过`kubectl describe pod -n kubernetes-dashboard`查看创建日志：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/image-20210626194414457.png)

如上显示表明，我们的节点创建成功，然后运行如下命令：

```sh
kubectl proxy
```

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210626194924.png)

再访问如下地址：

```
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/error?namespace=kuboard
```

如果是这样的，表面我们控制面板安装成功：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210626194950.png)

但是真正要访问，还需要配置个用户信息，生成一个`token`。

##### 创建管理用户配置

创建`yaml`文件

```shell
vim adminuser.yaml
```

添加文件内容，下面内容就是我们要创建的节点信息

```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
```

然后在`k8s`中创建：

```sh
kubectl apply -f adminuser.yaml
```

正常情况下，会提示创建成功

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210626195618.png)

然后获取授权`token`

```shell
 kubectl -n kubernetes-dashboard describe secret $(kubectl -n kubernetes-dashboard get secret | grep admin-user | awk '{print $1}')
```

下面显示的就是`token`信息，直接复制即可：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210626195800.png)

然后我们把`token`填入页面，即可访问：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210626200108.png)

然后，我们就可以通过`kubernetes-dashboard`管理我们的`k8s`了，可以看日志，管理服务节点等，具体各位小伙伴自己摸索吧。

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210626200318.png)

### 总结

今天的内容长度已经完全超出我的预期了，本来想着把主要流程梳理下就可以，但是实际总结过程发现，需要注意的点还是挺多的，而且有好多原计划的内容也没有加上，后面有时间梳理下再来分享。

总的来说，`k8s`相关知识点确实还是挺多的，除了基础命令，还有网关相关配置，`Linux`相关知识点，但只要你掌握了今天的大部分知识点，我相信对你使用`k8s`部署应用应该是有帮助的。好了，今天就到这里吧！
