#python #docker 
### Dockerfile

首先，编写我们基础镜像包含的内容，通常都是核心依赖和运行环境

```Dockerfile
# 基于pyhon基础镜像
FROM python:3.7
# 安装支持
RUN pip install flask
```


### 镜像构建

然后通过如下方式，构建我们的基础镜像，并将镜像推送到我们的仓库中

#### build

构建过程会将我们上面的依赖拉取到本地，并生成新的镜像文件

```sh
docker build -t python_flask .
```


#### login

这里登录是确保后面的`tage`和`push`可以正常进行

```sh
docker login -u harbor -p harbor harbor.syske.io
```

#### tag

```sh
docker tag python_flask:20240320 harbor.syske.io/test/python_flask:20240320
```


#### push

```sh
docker push harbor.syske.io/test/python_flask:20240320
```



#### 镜像使用

完成上面的镜像构建和`push`之后，我们就可以直接在我们其他项目中直接使用这个基础镜像：

```Dockerfile
# 基于pyhon基础镜像
FROM harbor.syske.io/test/python_flask:20240320

# 其他构建命令
```
这样我们就可以减少后续构建镜像的时间，也不需要每次都下载项目依赖。