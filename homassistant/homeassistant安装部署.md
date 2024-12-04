# home assistant安装部署

## docker环境部署

### 安装
#### 拉取镜像
```
docker pull homeassistant/home-assistant:latest
```

#### 服务启动

```ssh
#创建容器并运行
docker run -d --name="hass" -v /home/hass/config:/config -p 8123:8123 homeassistant/home-assistant:latest
```


## Supervised安装

### 安装依赖

```
apt-get install \
apparmor \
jq \
wget \
curl \
udisks2 \
libglib2.0-bin \
network-manager \
dbus \
systemd-journal-remote -y
```

### 安装docker-ce

参考`dokcer`相关内容

### 安装os-agent

#### 下载安装包

下载路径
```
https://github.com/home-assistant/os-agent/releases/latest
```

然后通过如下命令进行安装：
```
sudo dpkg -i os-agent_1.0.0_linux_x86_64.deb
```
可以通过如下命令进行测试
```
gdbus introspect --system --dest io.hass.os --object-path /io/hass/os
```