# wsl2安装Linux原生Docker



其实`wsl`安装`Docker`相关内容我已经在`wsl`整合`k8s`的相关内容中分享过了，但是为了方便各位小伙伴和自己查阅，我今天又做一个一次整理汇总，形成一个专门的文档，算是对之前内容回顾和总结吧。

#### wsl的那些事

对`WSL`有所了解的小伙伴应该都知道，关于`wsl`其实是有两个版本的，而且官方文档也给出了详细的对比：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211014112138.png)

详细对比可以看下官方说明：

```
https://docs.microsoft.com/zh-cn/windows/wsl/compare-versions
```

简单总结下就是：

- `wsl2`有完整的`Linux`内核，可以支持原生的`Linux`应用，甚至是运行`Liunx GUI`应用
- `wsl2`相比`wsl`文件`IO`性能提升，在文件密集型操作（如 `git `克隆、`npm `安装、`apt `更新、`apt `升级等）中的速度都明显更快
- `wsl2`有一些缺点：
  - 不能访问从 `Windows `装载的文件
  - 不支持 同一个项目`Windows` 和 `Linux` 进行交叉编译
  - 不支持串行端口和`USB` 设备访问
  - `WSL 2 `的内存使用量会随使用而缩放

不过`windows`和`wsl2`之间是可以实现便捷的文件传输的，只是他们之间的传输类似于虚拟机的文件传输，是基于网络进行的。如果我们需要在`windows`访问`wsl`中的文件，直接通过文件管理器访问`\\wsl$`，然后选择对应的系统即可：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211014114204.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211014114313.png)

#### 准备工作

##### `daemonize`安装配置

安装`daemonize`是为了让我们的`wsl`支持`systemctl`命令，然后激活`Systemd `，这些命令在后面启动`docker`服务、创建集群的时候都要用到。

安装命令也很简单（我一直觉得`linux`安装软件比`windows`方便，一行命令就完成安装，它不香吗）：

```sh
sudo apt install daemonize #第二种方式执行
sudo apt install -yqq fontconfig daemonize # 第一种方式需要执行
```

因为我已经安装过了，显示得可能和你不一样：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210626175913.png)

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

我推荐第一种，第二种虽然第一次是`ok`的，但是在实际使用中发现，`wsl`重启后（或者电脑重启），第二种方式执行`docker`命令的时候，会报下面的错，而且我还没找到解决方案：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210626184940.png)



#### 安装原生Docker

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
  
  # 国内推荐通过阿里云的地址替换，官方地址超级慢，密钥的地址也可以替换
  http://mirrors.aliyun.com/docker-ce/linux/ubuntu
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
  "registry-mirrors": ["https://docker.mirrors.ustc.edu.cn/", "https://hub-mirror.c.163.com/", "https://reg-mirror.qiniu.com"]
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



#### 解决需要root运行docker的问题

创建`docker`组

```sh
sudo groupadd docker
```

将用户添加到`docker`组中：

```sh
sudo usermod -aG docker $USER
```

好了，以上就是`wsl2`安装原生`Linux Docker`的所有内容了，感兴趣的小伙伴，可以亲自动手实践下。 


### 安装方式补充

#### 配置仓库 

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

#### 开始安装
```sh
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```