# manjaro安装常用软件安装配置

### 前言



### 常用软件

#### 安装picGo

经常写博客的小伙伴应该都知道图床，我们这里安装的`picGo`就是一个图床工具，而且我们之前也分享过关于利用 `picGo`搭建基于`gitee`和`github`搭建个人图床，感兴趣的小伙伴可以去看下：

http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648421467&idx=1&sn=9d37abe76ed2f61ab1df1a9a0507e07f&chksm=bea6dad189d153c733901ce3669411a6ae06e9327cd62f6d1824a936118a80d67efa0b818b13#rd

下面我们就来看下如何在`manjaro`环境下安装`picGo`这款工具。

首先去这款软件的`github`首页下载安装包：

```
 https://github.com/Molunerfinn/PicGo
```

这里我们下载`AppImage`格式的安装文件，因为这个版本的可以直接在`manjaro`环境下运行：



#### 安装nodeJs

这里安装`nodeJs`是为了后面安装`picGo`的`gitee`插件，没有`nodeJs`插件是装不上的。

首先，官网下载对应系统的`tar`压缩文件，下载完成后解压

```sh
tar -vxf node-v14.18.1-linux-x64.tar.xz  
```

移动到目标路径，这里我直接放在了`opt`文件夹下：

```sh
sudo mv node-v14.18.1-linux-x64 /opt 
```

##### 建立链接

这里其实就是讲`npm`和`node`映射到`usr/local/bin`目录下，这样我们就可以在任意路径下执行`nmp`和`node`命令了，类似于配置环境变量。

```
sudo ln -s /opt/node-v14.18.1-linux-x64/bin/npm /usr/local/bin/ 
sudo ln -s /opt/node-v14.18.1-linux-x64/bin/node /usr/local/bin/
```

##### 修改更新源

```sh
npm config set registry https://registry.npm.taobao.org
```



#### 安装typora





#### 安装chrome





#### 安装截图工具



