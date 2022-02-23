# docker构建python项目镜像

### 前言

原本今天是要分享我最近刚刚搞完的一个智（`hen`）能（`low`）家居控制系统的，但是今天开始复工之后，稍微有点忙，相关内容忘记同步了，所以今天就分享点`python`的相关内容，今天要分享的内容也是智能家居控制系统的一部分，也就是控制部分的`web`服务，当然内容比较简单，就是构建`python`项目`docker`镜像的完整过程。



### 构建python项目镜像

之前对于`python`的应用，基本上都是作为脚本在使用，很少有想法说通过它做一个具体的项目，但是本次这个项目，我本着项目尽可能简洁的原则，就想着通过`python`来构建项目的`web`服务端（目前`web`服务端只有一个页面），这个服务的作用主要是控制具体的`arduino`设备，后续考虑增加设备的增删改查操作。

这个智能家居控制系统，简单来说，就是一个轻量级的远程开关系统，就是我可以在上面开灯/关灯，当然目前也就只有这一个功能，不过你可以根据自己的需求进行扩展，我这里就不多说了，感兴趣的小伙伴，期待明天的分享。

整个`python`项目，我用到了`Flask`框架，因为这个框架我也是最近才开始接触，大部分的`code`都是参照文档完成的，所以关于这块我就不在这里班门弄斧了，有兴趣的小伙伴可以去看下官方文档：

```
https://dormousehole.readthedocs.io/en/latest/
```

整个项目其实很简单，我就是通过`Flask`构建了一个`web`服务，`web`服务只有一个页面，然后通过这个页面来控制`arduino`，对这个项目感兴趣的小伙伴可以参考下，文末我会放上项目地址。

#### 项目结构

项目的结构也很简单：

![](https://gitee.com/sysker/picBed/raw/master/blog/20220125223717.png)

其中，`static`存放的是`js`、`css`以及图片等静态资源；`templates`就是`html`的模板文件，和`spring boot`的`templates`类似；`venv`是`python`的虚拟环境；`arduino-index.py`是项目的主入口，其中代码很简单就是一个`controller`，也就是说，这个项目就只有一个页面：

```python
from flask import Flask,render_template,url_for

app = Flask(__name__)

@app.route("/index") 
def index(name=None):
    return render_template('index.html', name=name)
```

`Dockerfile`算是我们今天的主角；

`run.sh`是我写的`python`项目启动脚本，也是镜像的启动命令；

```sh
#!/bin/bash
# 初始话虚拟环境
. venv/bin/activate
# 设置Flask项目的环境变量，也就是我们入口的文件名
export FLASK_APP=arduino-index
# 启动 flask服务，-h 0.0.0.0 表示可以通过机器的任意ip访问flask服务，如果没有这个默认只能通过127.0.0.1或者localhost访问，另外这里需要说明的是，flask服务默认的端口是5000（更多信息可以参考官方文档）
flask run -h 0.0.0.0
```

`ZookeeperService.py`是`zookeeper`的一些简单操作，包括服务注册和发现，原本打算将`arduino`设备的一些信息注册到`zk`的，后来发现没必要了，这里可以忽略。

下面详细介绍下`Dockerfile`的相关内容，我们先看下`Dockerfile`的文件内容：

```dockerfile
# 基于pyhon基础镜像
FROM python:3.7
# 创建code文件夹
RUN mkdir /code
# 将run.sh脚本复制到code文件夹下
COPY ./run.sh /code
# 将arduino-index.py脚本复制到code文件夹下
COPY ./arduino-index.py /code
# 将static文件夹复制到code文件夹下
COPY ./static /code/static
# 将templates文件夹复制到code文件夹下
COPY ./templates /code/templates
# 将venv文件夹复制到code文件夹下
COPY ./venv /code/venv
# 设置code文件夹为工作目录
WORKDIR /code

# 安装支持
RUN pip install flask
# 进入到code文件夹中
RUN cd /code
# 执行启动命令
CMD ["/bin/bash", "run.sh"]
```

以前，特别不理解为什么`Dockerfile`要这么写，不过今天搞完这个`python`项目的`Dockerfile`之后，我觉得我已经对`Dockerfile`有了更深入的理解：

`Dockerfile`其实就是为了告诉`Docker`构建镜像的具体步骤，比如我们这里的`Dockerfile`，第一步就是先去拉取`python:3.7`的镜像，然后第二步是创建`code`文件夹，再然后是把我们要打包的文件复制到`code`文件夹下，接着设置工作目录，最后就是设置我们项目的启动命令，而且按照上面这些步骤，你一样可以通过手动的方式启动我们的项目：

![](https://gitee.com/sysker/picBed/raw/master/blog/docker-file.png)

完成上面的`Dockerfile`编写之后，我们直接通过下面的命令来构建我们的镜像即可：

```sh
docker build -t arduino-control-center .
```

项目构建完成后，我们可以启动测试下，首先确保镜像构建成功：

```
docker images
```

![](https://gitee.com/sysker/picBed/raw/master/blog/20220125231340.png)

然后通过`docker run`运行我们构建成功后的镜像即可：

```
run -p 5000:5000 -d arduino-control-center:latest
```

我们还可以通过`docker ps`看下镜像的运行信息，可以看到我这里的端口指定的是`5000`：

![](https://gitee.com/sysker/picBed/raw/master/blog/docker-file1.png)

最后再通过浏览器访问下我们的服务：

![](https://gitee.com/sysker/picBed/raw/master/blog/20220125232030.png)

效果很完美，当然唯一的不足是，这个镜像稍微有点大，后面看下如何缩减镜像尺寸。



### 结语

今天我们通过一个具体实例，演示了`python`项目构建`docker`镜像的完整流程，虽然整个流程对于熟悉`python`和`docker`的小伙伴来说，可能就是小菜一碟，但对于像我这样对`docker`和`python`还存在着很多知识盲区的小可爱来说，我觉得还是很有意义的，毕竟又一次加深了我对于`docker`相关知识的认知，这可能就是学习的学习的意义。

最后，再说几句废话。相比于`java`，`python`在很多地方应用起来更方便，毕竟短短几行代码就可以代替`java`几十行甚至上百行的代码，这一点就很奈斯，特别是最近通过`python`完成了解析`json`数据，刷`token`过期时间等一系列繁琐操作时，我更是越来越喜欢`python`了，当然，语言本身只是一种工具和手段，并没有任何优劣之分，具体在何种场景下使用何种语言，是需要结合具体的场景和需求来说的，毕竟最合适的才是最好的。好了，今天的内容就到这里吧，各位小伙伴，晚安吧！