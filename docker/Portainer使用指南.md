# Portainer使用指南

## 安装

创建卷文件

```sh
docker volume create portainer_data
```

启动

```sh
docker run -d -p 8000:8000 -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce
```

