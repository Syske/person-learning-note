# docker入门

## 基本操作

### 一、基本命令

### 1 拉取镜像

```sh
$ docker pull ubuntu:latest
#或者
$ docker pull ubuntu
```

### 2 查看本地镜像

```sh
$ docker images
```

### 3 运行容器

```sh
$ docker run -itd --name ubuntu-test ubuntu
```

