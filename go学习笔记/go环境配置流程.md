# golang环境配置流程

## 下载安装

### linux

如果是`linux`环境，直接通过命令行安装即可，也免去了环境变量配置的繁琐过程，这里以`ubuntu`为例：

```sh
sudo apt install golang
```
然后等待安装完成，安装完成后，输入`go`有如下输出，则表示安装完成：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202312150752586.png)

### win

相比而已`win`环境更繁琐一些，需要我们手动下载对应的版本，然后安装或者解压，之后要配置环境变量。

下载地址如下：

```url
https://golang.google.cn/dl/
```
然后选择对应的版本：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202312150756293.png)

之后拿到安装路径，配置环境变量

## 修改配置

默认`GoPROXY`配置是：

```sh
GOPROXY=https://proxy.golang.org,direct
```

由于国内访问不到，所以我们需要换一个`PROXY`，这里推荐使用
```sh
https://goproxy.io或https://goproxy.cn
```

可以执行下面的命令修改`GOPROXY`：

```sh
go env -w GOPROXY=https://goproxy.cn,direct
```

## 安装gopls

`gopls`是`go`官方维护的工具，提供代码提示、补全、格式化等诸多功能，方便我们编写

```sh
go install -v golang.org/x/tools/gopls@latest
```
这里我们推荐的`IED`是`VS code`，正常用`vs code`打开`go`项目就会提示我们安装`go`的插件和`gopls`