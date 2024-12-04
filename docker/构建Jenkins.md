# 构建Jenkins

### 拉取镜像

```sh
docker pull jenkins/jenkins
```

### 启动

```sh
docker run -d -p 49001:8080 -v $PWD/jenkins:/var/jenkins_home -t jenkins/jenkins
```

