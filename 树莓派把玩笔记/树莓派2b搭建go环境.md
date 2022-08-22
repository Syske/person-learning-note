# 树莓派2b构建golang环境

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


### go web简单示例

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


参考内容 

1.  https://blog.csdn.net/yinjl123456/article/details/118229692