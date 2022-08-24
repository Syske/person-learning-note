# 树莓派2b构建golang环境

### 前言

开始之前，我们先说点题外话。已经好久没有更新过技术内容了（认真脸）。一个原因是很长时间以来，一直感觉不在状态，迷茫、困惑，浑浑噩噩的，也没有分享的动力，虽然偶尔会记录一些技术总结或者遇到的问题，也提不起输出的欲望，所以就一直懒癌晚期；

另一个原因就是没时间、天气又热（准确说还是懒😳），学习也提不起兴趣，好多计划也没如期进行，所以也是一拖再多；

直到上个月10号，突然想明白不能再这样浑浑噩噩了（当然过程也不可能如此顺利🐶），然后硬着头皮开始运动，状态才开始慢慢好一点：
- 首先是把之前挂掉的科二科三（摩托车）考过了，然后又黑了一圈（话说科二的绕桩真的难，第一次两把都挂到这个上面了）
- 精神状态好了很多，执行力强了一丢丢
- 负面情绪少了好多，内心更加笃定​

当然还有一些其他变化，这里就不一一说了，只是觉得还得好好坚持。
我现在的想法就是，接受自己的平凡和普通，做一个热爱生活的普通人，做自己想做的事，做自己能做的事，用心去发现、感受、经历、体验周身的一切，美好的，不美好的，
这世界也许不如我们想象的那么美好，但也没我们想象的那么糟糕，“没有人在雨里”


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

参考内容 

1. https://blog.csdn.net/yinjl123456/article/details/118229692
2. https://learnku.com/docs/build-web-application-with-golang/032-go-builds-a-web-server/3169