经常用markdown写博客的你，一定因为图片的管理感到头疼，当然不管你头不头疼，反正我觉得图片管理很麻烦，很不方便，然后突然有一天我发现了一款图床神器——picGo，配合上snipaste，从此写markdown溜到飞起……下来我们就看看如何搭建自己的博客图床吧！

### 安装picGo

首先要安装picGo这个软件，这个软件的作用就是将我们的图片上传到图床仓库，然后生成图片的路径，路径可以是markdown格式，也可以是html格式，当然也支持自定义。这是一个开源项目，项目地址如下：

```
https://github.com/Molunerfinn/PicGo
```

github国内访问比较慢，我放下自己的百度云下载地址链接: https://pan.baidu.com/s/1_GzSqspxLgiCfgX1o4RLBQ 提取码: vtau

下载完，双击安装，然后打开，软件大概长这样：

![](https://gitee.com/sysker/picBed/raw/master/images/20200330234921.png)

安装完以后，先不要管，我们稍后再讲如何配置图床，先往下看。

### 创建github图床仓库

打开github或者gitee，如果没有账户先注册一个账户，然后创建一个仓库：

这里先演示github的创建流程

#### 创建仓库

![](https://gitee.com/sysker/picBed/raw/master/images/20200331214136.png)

#### 填写仓库信息

![](https://gitee.com/sysker/picBed/raw/master/images/20200331214644.png)

#### 创建token

点击github头像，找到settings

![](https://gitee.com/sysker/picBed/raw/master/images/20200331215523.png)

找到开发者设置（Developer settings）

![](https://gitee.com/sysker/picBed/raw/master/images/20200331215603.png)

找到个人访问token，然后点击创建新的token

![](https://gitee.com/sysker/picBed/raw/master/images/20200331215624.png)

填写token描述，设置token权限，然后点击最下面的创建按钮，这里需要注意的是，token只会显示一次，你最好复制保存下，丢失了需要重新生成，很麻烦

![](https://gitee.com/sysker/picBed/raw/master/images/20200331220213.png)

到这里githu图床仓库就创建完成了，接下来我们来配置图床软件。

#### 配置图床信息

打开刚刚安装的picGO，点到picGo设置，确保github图床开启，然后回到图床设置，点击GitHub图床

![](https://gitee.com/sysker/picBed/raw/master/images/20200331221211.png)

#### 设置图床信息

![](https://gitee.com/sysker/picBed/raw/master/images/20200331222217.png)

这是我的图床仓库

![](https://gitee.com/sysker/picBed/raw/master/images/20200331221616.png)

#### 测试

在上传区，可以测试下，看是否可以正常上传，一般没什么问题。

由于GitHub国内访问不咋行，图片经常加载不出来，下来我们来看下gitee（码云，类似国内github）如何创建图床。



### 创建gitee图床仓库

#### 创建仓库

和GitHub类似，先创建仓库，当然首先你要有个账户，没有的话先注册，然后登陆，创建仓库：

![](https://gitee.com/sysker/picBed/raw/master/images/20200331223649.png)

#### 填写仓库信息

和GitHub类似，这里就不赘述了，而且是中文环境

![](https://gitee.com/sysker/picBed/raw/master/images/20200331223834.png)

和前面一样，创建完成后，我们要创建token

![](https://gitee.com/sysker/picBed/raw/master/images/20200331224152.png)

设置权限，和前面一样，token只显示一次，所以保存好

![](https://gitee.com/sysker/picBed/raw/master/images/20200331224300.png)

#### 安装gitee插件

根据我们创建的仓库和token，配置我们gitee的图床，和GitHub不一样的是，gitee图床需要安装一个插件，安装这个插件前，本地要先配置npm环境。搜索gitee，我安装的是gitee，当然你也可以选另一个，没有太大区别。

![](https://gitee.com/sysker/picBed/raw/master/images/20200331224959.png)

安装完成后，我们接下来开始配置图床

#### 配置图床信息

根据我们的创建的仓库和token，配置我们的图床服务器，和GitHub类似

![](https://gitee.com/sysker/picBed/raw/master/images/20200331225446.png)

#### 测试

这里我就不测试了，因为本篇文章就是通过gitee图床完成的，用起来很爽，图片加载很快

### 补充更新

最近因为个人原因导致picGO不可用，我一直以为是软件的问题，卸载安装，来回折腾了好多遍，最后发现是安全软件防火墙的锅，当时心里真的MMP，浪费我时间🤣。当然这一次的事情还是有收获的，我在安装gitee插件的时候发现github-plus已经完美支持gitee了，不需要再单独安装gitee插件了。可以再插件里面直接搜索github-plus，找不到的话，也可以手动安装。

#### 安装github-plus

![](https://gitee.com/sysker/picBed/raw/master/20210123131600.png)

手动安装命令：

```sh
npm install picgo-plugin-github-plus
```

当然手动安装的前提是你要有哦node.js的环境，具体的百度吧

#### 配置githubplus

配置方法大同小异，根据类型选择origin

![](https://gitee.com/sysker/picBed/raw/master/20210123132246.png)

### 总结

之前图片一直是存在本地的，每次发博客的时候都需要上传图片，很麻烦，后来用了GitHub图床，网络太卡也放弃了，现在用了gitee图床，我只能说真香😂😂😂，赶紧用起来吧，真的很爽