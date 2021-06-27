## wsl搭建k8s集群补充内容

### 前言

昨天我们分享了如何在`wsl`上搭建`k8s`集群，但是由于内容多，昨天时间也比较紧促，所以好多知识点并没有覆盖到，考虑到好多小伙伴可能也是第一次使用`k8s`，我们今天把一些基础知识再补充下，一方面是为了让大家清楚每一步操作的目的，清楚每一个命令的作用，另外一方面就是我自己确实也需要把这这两天积累的基础知识整理下，理清楚思路，便于知识积累。



















#### `k8s`代理

```
http://localhost:8001/api/v1/namespaces/[Namespace]/services/[Name]:[Port]/proxy/
```

![](https://gitee.com/sysker/picBed/raw/master/images/20210625174624.png)



```
kubeadm init --pod-network-cidr=10.244.0.0/16 --control-plane-endpoint=ubuntu.wsl --image-repository=gotok8s --v=5
```

![](https://gitee.com/sysker/picBed/raw/master/images/20210626112353.png)

`sudo`执行

![](https://gitee.com/sysker/picBed/raw/master/images/20210626112431.png)

```
kubeadm init --pod-network-cidr=10.244.0.0/16 --control-plane-endpoint=ubuntu.wsl --image-repository=gotok8s --ignore-preflight-errors=Swap  --v=5
```

```
https://www.cnblogs.com/xxred/p/13258347.html
```

```
wsl --shutdown
```

