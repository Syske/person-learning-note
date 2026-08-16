### 停止Docker服务

```sh
sudo systemctl stop docker
sudo systemctl stop docker.socket
```

### 迁移存储

```sh
# 创建新的镜像目录
sudo mkdir -p /new/path/docker
# 迁移目录下文件，rsync工具可以确保复制时保留所有的文件属性和权限
sudo rsync -aP /var/lib/docker/ /new/path/docker
```
-a选项表示归档模式，会递归复制目录并保留所有文件属性；-P选项表示显示进度和保留部分硬链接。

### 修改配置
这里有两种方式，一种是修改`daemon.json`文件：
```sh
sudo vim /etc/docker/daemon.json
```
修改其中的`data-root`配置，改成我们迁移后的目录即可：
```json
{
    "data-root":"/mnt/upan/docker/storage",
    "registry-mirrors": [
        "https://docker.m.daocloud.io",
        "https://docker.1ms.run"
    ]
}
```

另一种方式是直接修改`docker.server`文件：
