# 树莓派2b构建golang环境

### 前言

开始之前，我们先说点题外话。已经好久没有更新过技术内容了（认真脸）。一个原因是很长时间以来，一直感觉不在状态，迷茫、困惑，浑浑噩噩的，也没有分享的动力，虽然偶尔会记录一些技术总结或者遇到的问题，也提不起输出的欲望，所以就一直懒癌晚期；

另一个原因就是没时间、天气又热（准确说还是懒😳），学习也提不起兴趣，好多计划也没如期进行，所以也是一拖再多；
当然，你们今天既然能看到这篇更新，就说明我已经基本调整过来了，关于这段时间的感悟我放在结语了，后面的话，会尽可能抽时间更新的。

下面我们来看下今天的技术更新，今天的更新没啥干货，其实就是我前天下班没啥事，就在树莓派上构建了`golang`的开发环境，然后记录了整个过程，以下内容同样适用于`linux`环境，但是需要选择系统对应的软件版本。


### 下载安装

#### 下载
国内可以访问`go`语言中文网进行下载
```
https://studygolang.com/dl
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20220822215305.png)

这里可以通过`uname`查看我们的主机信息，选择对应的版本：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20220822215527.png)

从上面的图片中我们可以看到，`2b`的`cpu`架构是`armv7l`，但是`go`安装包并没有针对`v7l`的版本。
查询了`armv6l`和`armv7l`的区别之后，可以得知`armv7l`是兼容`armv6l`的，所以这里我们直接选择`armv6l`版本（先试试看嘛，有问题再说呗）

我们直接通过`wget`命令下载
```
wget https://studygolang.com/dl/golang/go1.19.linux-armv6l.tar.gz
```

#### 解压
解压很简单，直接`tar`命令就行：
```
 tar -vxf go1.19.linux-armv6l.tar.gz
```


#### 配置环境变量

解压之后可以把`go`文件夹移动到其他目录下，比如`/usr/local`、`/apt`等，根据自己的需求，这里我就不挪位置了，直接配置：
```sh
sudo vim /etc/profile
```
在文件末尾直接加入配置：
```sh
# go path config
export GOROOT=/home/pi/go
export GO_HOME=$GOROOT
export GOPATH=/home/pi/go-lang
export PATH=$GO_HOME/bin:$PATH

# enable go modules
export GO111MODULE=on

# config GOPROXY proxy env
export GOPROXY=https://goproxy.io
```
上述路径需要根据自己的路径进行修改，我的`go`路径如下：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20220822222144.png)

然后重启或者通过`source /etc/profile`，让我们的配置文件生效。

#### 测试
完成上面配置之后，我们来进行简单测试：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20220822222649.png)

至此，我们树莓派`2b`的`go`环境就构建完成了，然后我们就可以愉快地在树莓派上使用`go`语言了


### 创建项目
`go`语言创建项目比较简单。
第一步，我们需要创建项目文件夹，然后在项目文件夹下通过`go mod init`命令进行项目初始化：
```sh
$ mkdir go-web-test
$ cd go-web-test
$ go mod init github.io/syske/go/web-test
```
`go mod init`需要指定我们的模块名称，类似`java`的`package`，如果不指定的话，会有错误提示
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20220823080343.png)
执行完`go mod init`命令后，会在当前文件夹下生成一个名为`go.mod`文件，文件内容如下：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20220823081519.png)
从这个文件内容，我们可以看出，主要是项目的一些配置信息，包括当前项目的`module`和`golang`的版本信息。

下面我们来开始写代码吧。
关于`go`的语法和基础的知识，我们这里就不做过多说明了，有兴趣的小伙伴可以自己研究，需要学习资料的小伙伴也可以私信我。

#### go web简单示例
下面这段代码构建了一个简易的`web`服务器，端口是`9090`，我们可以通过浏览器访问，程序控制台会打印请求信息，同时会给客户端返回响应结果

```go
package main

import (
      "fmt"
      "net/http"
      "strings"
      "log"
)

func sayhelloName(w http.ResponseWriter, r *http.Request) {
    r.ParseForm()
    fmt.Println(r.Form)
    fmt.Println("path", r.URL.Path)
    fmt.Println("scheme", r.URL.Scheme)
    fmt.Println(r.Form["url_long"])
    for k, v := range r.Form {
        fmt.Println("key", k)
        fmt.Println("val", strings.Join(v, ""))
    }
    fmt.Fprintf(w, "Hello astaxie!")
}

func main() {
    http.HandleFunc("/", sayhelloName)
    err := http.ListenAndServe(":9090", nil)
    if err != nil {
        log.Fatal("ListenAndServe:", err)
    }
}
```
客户端：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20220823083138.png)

控制台输出：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20220823083040.png)

好了，到这里，我们整个内容就结束了，后面有时间我们再继续分享

### 结语
接着前言部分继续说。直到上个月10号，突然想明白不能再这样浑浑噩噩了（当然过程也不可能如此顺利，自然也是经历了各种摇摆不定🐶），然后硬着头皮开始运动（目前频率是隔天跑），状态才开始慢慢好一点：
- 首先是把之前挂掉的科二科三（摩托车）考过了，然后又黑了一圈（话说科二的绕桩真的难，第一次两把都挂到这个上面了）
- 控制力强了一点，执行力和行动力也强了一丢丢
- 负面情绪少了好多，内心更加笃定​
- 更有精神了，反正现在上班不瞌睡了😂，早上起床状态也稍微好了一点


当然还有一些其他变化，这里就不一一说了，只是觉得还得好好坚持，真的是越坚持越想去坚持，因为能看见成长和改变，所以你就越有动力去行动。

这里再提一些我觉得比较适合低谷期做的事情，我是觉得挺有用的：

- 刷纪录片：特别是那种慢节奏的记录片，真的可以让你的生活节奏慢下来，会让你思考生活和人生的意义，会让你从不同的视角重新审视人生，比如《人生第一次》、《人生第二次》（第一次的第二季）、《一百年很长吗》、《历史那些事》（第一季、第二季，苏东坡那一集最喜欢）、《大唐帝陵》、《大明宫》、《英雄之路》（每集都有独立的片尾曲）、《河西走廊》（`bgm`超好听，超震撼）
- 运动：汗流浃背的疲惫，急促短暂的呼吸，虽然会让你露出痛苦面具，但是同样也让你真实地感受到自己的存在，真的是既痛苦又快乐，运动完后那种酣畅淋漓的感觉，真爽！
- 产出：产出准确地说就是去做一些具体而且有收获的事情
- 记录：记录就是记录自己的日常生活，可以是记账，平时的收支流水，也可以是记录自己的感受感悟，类似日记。

我现在的想法就是，接受自己的平凡和普通，做一个热爱生活的普通人，做自己想做的事，做自己能做的事，用心去发现、感受、经历、体验周身的一切，美好的，不美好的， 对我们来说都是收获。
这世界也许不如我们想象的那么美好，但也没我们想象的那么糟糕，“没有人在雨里，没有人不在雨里”，“你不可能什么都有，你不可能什么都没有”……

以上共勉，感谢各位小伙伴的支持，感谢，比心❤

参考内容 

1. https://blog.csdn.net/yinjl123456/article/details/118229692
2. https://learnku.com/docs/build-web-application-with-golang/032-go-builds-a-web-server/3169