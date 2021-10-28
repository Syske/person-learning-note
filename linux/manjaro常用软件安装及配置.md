# manjaro安装常用软件安装配置

### 前言

昨天我们主要分享了`manjaro gnome`环境下搜狗输入法的安装过程，但是真正想把`manjaro`打造成生产工具，只有输入法还是不够的，所以我们今天来看下如何在`manjaro gnome`环境下安装微信、网易云、`picGo`图床工具、`typora`编辑器以及截图工具等软件。

### 常用软件

#### 安装picGo

经常写博客的小伙伴应该都知道图床，我们这里安装的`picGo`就是一个图床工具，而且我们之前也分享过关于利用 `picGo`搭建基于`gitee`和`github`搭建个人图床，感兴趣的小伙伴可以去看下：

![](https://gitee.com/sysker/picBed/raw/master/blog/face-img-a5baeb44acd2480e94278a7580c979f6.jpg)

http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648421467&idx=1&sn=9d37abe76ed2f61ab1df1a9a0507e07f&chksm=bea6dad189d153c733901ce3669411a6ae06e9327cd62f6d1824a936118a80d67efa0b818b13#rd

下面我们就来看下如何在`manjaro`环境下安装`picGo`这款工具。

首先去这款软件的`github`首页下载安装包：

```
https://github.com/Molunerfinn/PicGo/releases
```

这里我们下载`AppImage`格式的安装文件，因为这个版本的可以直接在`manjaro`环境下运行：

![](https://gitee.com/sysker/picBed/raw/master/images/20211027131953.png)

下载完成后，将下载文件移动到目标文件夹下，然后授予软件运行权限就行了：

```sh
sudo chmod u+x ./PicGo-2.3.AppImage
```

然后直接执行`./PicGo-2.3.AppImage`即可运行`picGo`：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027221317.png)

安装了`manjaro`之后，电脑基本上不关机，所以我就没有设置`picGo`的自动启动，所以下面的方式来源于网络，而且我并没有验证，感兴趣的小伙伴可以自己试下。

如果你需要开启启动，通过增加开机自动启动脚本来执行如上命令即可：

1. 创建一个启动`service`脚本

   ```sh
   sudo vim /etc/systemd/system/rc-local.service
   ```

   向文件中添加如下内容：

2. 创建` /etc/rc.local` 文件

   ```sh
   sudo vim /etc/rc.local
   ```

   然后添加如下内容

   ```sh
   #!/bin/sh
   # /etc/rc.local
   if test -d /etc/rc.local.d; then
       for rcscript in /etc/rc.local.d/*.sh; do
           test -r "${rcscript}" && sh ${rcscript}
       done
       unset rcscript
   fi
   ```

   

3. 添加执行权限

   ```sh
   chmod a+x /etc/rc.local
   ```

   

4. 添加`/etc/rc.local.d`文件夹

   ```sh
   mkdir /etc/rc.local.d
   ```

   

5. 设置开机自启

   ```sh
   systemctl enable rc-local.service
   ```

   

#### 安装nodeJs

这里安装`nodeJs`是为了后面安装`picGo`的`gitee`插件，没有`nodeJs`插件是装不上的，而且提示信息会告知你安装`nodeJs`：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027221542.png)

这里推荐手动下载病配置环境变量，命令行安装的方式好像没有用，当然也可能是我这边没有设置好。

##### 下载安装

首先，官网下载对应系统的`tar`压缩文件：

```
http://nodejs.cn/download/
```

这里我下载的是`v14`，这个是长期支持版本，属于比较稳定的版本：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027221855.png)

下载完成后，直接解压

```sh
tar -vxf node-v14.18.1-linux-x64.tar.xz  
```

然后移动到目标路径，这里我直接放在了`opt`文件夹下：

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

然后再次启动`picGo`，安装`github-plus`插件就可以安装成功，图床配置可以参考`picGo`安装那块留的链接内容，过程比较详细。



#### 安装微信

关于`linux`的生态，我特别想吐槽腾讯，作为一个大厂，没有拿得出手的`linux`项目，而且连自家的产品都没有`linux`版本，比如微信，`QQ`虽然有，但是好久都不更新了；网易云就做的比较好了，网易云音乐直接就有`linux`版本。

对于这种非`manjaro`官方的包，我们通常都是通过`yay`来安装，如果你不确定的话，可以先用`sudo pacman -S`试着安装下，如果提示不存在，就可以用`yay`工具进行安装了：

```
yay deepin-wine-wechat
```

从下面的截图中可以看到，我这里就是先试了`pacman`的方式，然后又用了`yay`工具：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027213321.png)

如果安装过程中报类似我这里的报错：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027214739.png)

可以试着将软件源的`SigLevel`限制放开，这里我只是将`multilib`的`SigLevel`改成了`Optional TrustAll`然后就好了。如果你改完还不行，可以试着也将其他的也改成`Optional TrustAll`试下：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027214843.png)

安装过程中根据提示信息选择即可，过程不是很复杂。

这里安装的`weChat`其实就是`windows`版本的微信，是通过`wine`技术实现的，这里安装的是`deppin`下的微信，`deepin`算是国产`linux`之光，之前比较火的`UOS`系统就是由他们公司发起的，玩`linux`的小伙伴应该比较熟悉。

经过漫长的等待，`manjaro`的程序列表会多出一个微信图标：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027215643.png)

运行之后，会弹出微信的安装界面，然后一直下一步，最终安装成功后效果如下：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027214620.png)

登录完成后的效果和`windows`的`PC`端没有本质区别：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027215956.png)



#### 安装chrome

`manjaro`默认带的是`fireFox`浏览器，但是我还是比较喜欢用`chrome`，如果有小伙伴觉得够用，可以不必安装。

安装`chrome`也很简单，只需要通过`yay`加上软件名称即可：

```sh
yay google-chrome
```

如果安装过程中提示“无效或已损坏的软件包”，可以参考微信安装那里的报错信息处理方式。这里我们选择第二个，其中`3`和`4`是测试版本，其他几个是`chrome`的驱动软件，这个驱动软件是给爬虫模拟`chrome`浏览器用的：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027220327.png)

提示是否显示差异，我一般直接输入`n`，因为看差异也看不出来啥：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027220848.png)

然后静静等待安装完成即可，安装过程中可能会让你输入密码，正常输入即可。

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027223113.png)

如果安装过程中报如下错误：

![](https://gitee.com/sysker/picBed/raw/master/images/20211028130249.png)

请先确认`base-devel`是否安装，如果没有安装，先通过如下命令进行安装：

```sh
sudo pacman -S base_devel
```

然后在重新安装

#### 安装网易云

网易云音乐安装就很简单了，直接执行如下命令即可：

```sh
sudo pacman -S netease-cloud-music 
```

安装完成后会多出网易云音乐的图标：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027222841.png)

界面效果和`win`环境下基本一致：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027223003.png)



#### 安装typora

`Typora`是一款特别好用的`markdown`编辑器，我现在基本上所有的博客都是通过它完成的，关于它的用法我之前有分享过它的内容，感兴趣的小伙伴可以去看看：

![](https://gitee.com/sysker/picBed/raw/master/blog/face-img-f6e5d3b18e2147fea7f296a0cf72c55f.jpg)

http://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648421449&idx=1&sn=e7efa7a9012579fda56b852f823572ec&chksm=bea6dac389d153d5c1d10f96a06183cc0982510dfaae825e9060032ff587a992e34bc3a854b8#rd

这款工具安装工程也很简单，通过如下命令安装即可：

```sh
sudo pacman -S typora
```

使用效果如下：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027223611.png)



#### 安装截图工具

关于截图工具，其实`manjaro`系统本身有自带的，但是系统自带的是没办法对图片做标记，而且没法贴图，真的是特别期待`snipaste`，目前`linux`版本还在开发：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027223942.png)

今天在写这篇文章的时候，我全程用的是系统自带的截图工具，虽然凑活能用，但是体验确实太差了。

目前我所知道的`linux`截图工具中，数`flameshot`还可以，可以实现标记注释等操作：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027224853.png)

刚刚又安装了，然后研究了下，发现它某些功能和`snipaste`还挺像的，而且已经支持贴图了，其他功能也基本上支持，具体后面研究下再说。

安装命令如下：

```sh
sudo pacman -S flameshot
```

可以在系统设置中的`keyboard`中添加`flameshot`的截图快捷键，点击`+`号新增，然后输入如下命令：

```
flameshot gui
```

然后制定快捷键即可：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027230300.png)

设置完之后就可以体验到类似于`snipaste`的截图快感，然后复制：![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027230117.png)

选择`picGo`的剪贴板图片，直接上传，简直不要太爽：

![](https://gitee.com/sysker/picBed/raw/master/manjaro/20211027230550.png)

好了，以后`linux`我就用`flameshot`截图了，总体体验还不错。

#### 其他软件

还有一些其他的软件在`manjaro`也是支持的，这里我们放出安装命令，各位小伙伴可以根据自己需要安装：

```sh
# wps office，与Windows相比，linux下的要清爽的多，没有烦人的广告
pacman -S wps-office
# post man，做后端开发的小伙伴比较熟悉
pacman -S postman-bin
# 深度的百度云盘
yay -S deepin-wine-baidupan
#迅雷
yay -S deepin.com.thunderspeed 
#思维导图
yay -S xmind 
```




### 结语

到这里我们`manjaro`安装日常常用软件基本就算结束了，以上软件基本上就满足了我们的大部分工作场景，感兴趣的小伙伴亲自动手整起来吧。好了，各位小伙伴晚安吧！
