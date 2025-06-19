## 操作流程

### 安装

安装`kt-connect`，选择适合自己的版本，然后解压

```
https://github.com/alibaba/kt-connect/releases/tag/v0.3.7
```

![](https://cdn.nlark.com/yuque/0/2025/png/2672304/1746671453643-44cfd5a9-46c0-4de1-b1ae-a9c5e5a30fc3.png)

安装 kubectl，建议和`kt-connect`放在同一个目录下

`Windows`环境

```
curl.exe -LO "https://dl.k8s.io/release/v1.25.0/bin/windows/amd64/kubectl.exe"
```

详细的可以参考这个文档：[安装工具 | Kubernetes](https://kubernetes.p2hp.com/docs/tasks/tools/_print/index.html#pg-2cc93d3011d707aeb6564bab02048f7a)

### 配置环境变量：

1. 将kubectl的路径加入本地path
2. ![](https://cdn.nlark.com/yuque/0/2025/png/2672304/1746671489695-a331904d-4aa2-41bb-bb9c-08bb62b5518e.png)![](https://cdn.nlark.com/yuque/0/2025/png/2672304/1746671541672-82d9e3d4-00f3-4946-a1b6-3f52c37f64ad.png)
3. 然后在终端执行下述命令，确认是否配置成功：

```
kubectl version --client
```

![](https://cdn.nlark.com/yuque/0/2025/png/2672304/1746671577355-0809f13e-ac45-4df8-93d6-562f5cb6daa2.png)

### 生成`kubeconfig`

如果没有`.kube`文件夹先手动创建文件夹，`win`环境下路径在`C:\Users\用户名\`，`mac`和`linux`就是用户的`home`目录

![](https://cdn.nlark.com/yuque/0/2025/png/2672304/1746671594751-95f40aa5-6c04-442b-afee-35cd878429cb.png)

然后通过下述命令，初始化配置

```
kubectl config view > $HOME\.kube\config
```

之后，从阿里云k8s复制连接信息，覆盖上述文件内容（每个人的信息不一样，建议自行复制）

![](https://cdn.nlark.com/yuque/0/2025/png/2672304/1746671634742-8447ec07-d22c-4dc5-89ea-1fdcddd8c0fa.png)

### 启动连接

这里需要以管理员方式运行，`win`环境下要以管理员方式启动终端，`mac`和`linux`需要以`sudo`方式运行

```
ktctl -n t2 connect --dnsMode hosts --excludeIps '10.30.119.90,10.30.118.200' --reuseShadow
```

![](https://cdn.nlark.com/yuque/0/2025/png/2672304/1746671657782-53ea2ff6-cdcb-41f6-b47e-0ee36b9f99ae.png)

说明：

- `-n t2`表示指定集群`k8s`集群为`t2`，新测试环境就是这个集群

- `--dnsMode hosts`是将`dns`解析模式设置为`hosts`文件模式，这种模式下会自动将`k8s`集群中的服务和`ip`映射加入本地`hosts`文件。每次启动会重新生成，结束运行后会自动清理。默认是`localDNS`，实测发现该模式下，会导致所有请求流量转发到`k8s`，会导致本地外网访问不用
- `--excludeIps`表示不需要转发的集群地址，现在排除的`apollo`地址，如果本地能正常访问可以不排除
- `--reuseShadow`作用是复用pod，减少Pod数量，不加这个参数，每个connect都会创建一个pod

**注意！！！**：为了避免系统资源占用过多，建议大家在`connect`时，都带上`--reuseShadow`，这样就不会每个人都创建一个pod

如下提示则表示启动成功

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/2511c15e-5d34-4506-8559-641bd1d38480.jpg)

### 设置本地代理

#### **选项1：全局代理**

```
# 临时设置终端代理（Mac/Linux）
export http_proxy=socks5://127.0.0.1:2223
export https_proxy=socks5://127.0.0.1:2223

# Windows (PowerShell)
$env:HTTP_PROXY="socks5://127.0.0.1:2223"
$env:HTTPS_PROXY="socks5://127.0.0.1:2223"
```

#### **选项2：Java应用单独代理**

在 **IDEA 的 VM Options** 中添加：

```
-DsocksProxyHost=127.0.0.1 -DsocksProxyPort=2223
```

或代码中设置：

```
System.setProperty("socksProxyHost", "127.0.0.1");System.setProperty("socksProxyPort", "2223");
```

之后在本地启动服务即可

工具文档：[kt-connect](https://github.com/alibaba/kt-connect)

## 服务启动

### 本地配置

将下述内容复制到本地application-local.properties，建议直接覆盖（删除其他配置），然后按照服务修改namespaces（后面考虑将相关改动直接提交）

```
# 新测试环境apollo地址
apollo.meta=http://192.168.0.90:8080
# 默认不注册服务，确保不影响测试环境
rpc_register_registry_ignore=true
# cool-dev-local中配置的是特有的配置，目前只有rocketMq地址，后续按需增加
apollo.refreshInterval=1
apollo.bootstrap.enabled=true
apollo.bootstrap.namespaces=cool-dev-local,cmn-aliyun,user-center-api-t2,user-center-api-application,cool-common-dev
```

### 服务注册

默认情况，本地服务会自动注册到测试环境zk。非必要情况，建议各位小伙伴尽量不要注册本地服务到测试环境zk，可以通过在本地增加如下配置取消注册：

```
rpc_register_registry_ignore=true
```