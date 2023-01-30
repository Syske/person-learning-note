# power-shell美化

### 前言

喜欢折腾`linux`终端的铁子们应该都听说过`oh-my-zsh`，也一定喜欢`oh-my-zsh`那炫酷的效果和丰富的插件，当然也肯定对`windows`的终端工具（`cmd`或者`power shell`）有很多的诟病，当然我也是如此，前前后后体验了各种各样的终端工具，比如`hyper`，但是还是不满意，最后索性就不再折腾了。

然而，在最近一个机缘巧合的场景下，我遇到了`oh-my-posh`，看到它的第一眼我就知道这就是我期待的终端工具，至少我是满意的，颜值杠杆，所以今天我们要分享的内容就是基于`oh-my-posh`的`power shell`美化。



### power shell美化

#### oh-my-posh

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220111223348.png)

什么是`oh-my-posh`？它是一个自定义提示引擎，适用于任何能够使用函数或变量调整提示字符串的 `shell`，它一个开源项目，出了支持`windows`系统之外，它还支持`linux`和`mac`系统，从项目的代码占比中，我们可以发现`oh-my-posh`是主要基于`go`开发的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220111225100.png)

目前这个项目已经有`4k`的小星星了，感兴趣的小伙伴可以研究下，项目地址如下：

```
https://github.com/JanDeDobbeleer/oh-my-posh2
```



另外这里我也放上官方文档，方便给位小伙伴参考：

```
https://ohmyposh.dev/docs
```



#### 安装terminal

在开始美化之前，我们要先安装`windows terminal`，`Terminal`是微软开源的一个终端工具，据听说已经是`win11`的默认终端了。相比于系统自带的`power shell`和`CMD`，`terminal`颜值就高多了。安装方式也很简单，只需要在应用商店搜索`windows Terminal`，然后点击安装即可：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220111130257.png)

安装完成之后，它是这个样子的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220111224039.png)

虽然比`cmd`和`power shell`原生的终端好看了很多，而且支持很多自定义的美化设置，但是还是不是很好看，反正就是没有`oh-my-zsh`看着顺眼，所以下面我们就开始对它进行进一步的美化设置，让它比`oh-my-zsh`更好看。

关于`window Terminal`的设置和美化，可以看下官方文档，说得很是详细，包括我们今天的内容其中也有涉及：

```
https://docs.microsoft.com/zh-cn/windows/terminal/
```



#### 安装posh-git

`posh-git` 包含一组强大的 `PowerShell` 脚本，提供了 `Git `和 `PowerShell `的集成。`posh-git `还为常见的 `git` 命令、分支名称、路径等提供选项卡补全支持。例如，使用 `posh-git`，`PowerShell `可以`checkout`通过键入`git ch`和按键来完成 `git` 命令`tab`。这将完成选项卡`git checkout`，如果您继续按`tab`，它将在其他命令匹配项中循环，例如`cherry`和`cherry-pick`。

不过看了官方文档的安装步骤，是没有这步操作，`posh-git`可以让我们的`git`命令更好用，`posh-git`本身也是一个很火的开源项目，感兴趣的小伙伴可以去看下：

```
https://github.com/dahlbyk/posh-git/
```

##### 安装命令

打开`power shell`执行如下命令：

```
Install-Module posh-git -Scope CurrentUser
```

这行命令的作用是为当前用户安装`posh-git`

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220110233441.png)

执行完成后，根据提示输入对应的选项，然后默默等待安装完成。



#### 安装oh-my-posh

`post-git`安装完成后，就要开始安装我们的主角了——`oh-my-posh`，它的安装也很简单，一行命令搞定：

```
Install-Module oh-my-posh -Scope CurrentUser
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220110233652.png)

操作类似，根据提示输入，然后静静等待安装完成。



#### 导入模块

这一步是将我们安装的`posh-git`和`oh-my-posh`加载到`powser shell`中：

```
Import-Module posh-git
Import-Module oh-my-posh
```

但是导入这两个模块之后，我们的终端还是不会有任何变化，因为我们还没有设置主题：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220110234517.png)



#### 设置主题样式

设置主题的方式很简单，只需要执行如下命令即可：

```
Set-PoshPrompt -Theme JanDeDobbeleer
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220110234621.png)

输完这个名称之后，可以看到终端的样式已经出来了，但是由于字体没有修改，所以看着还很怪异。

这里的`JanDeDobbeleer`是我们的主题名称，从名字可以看出来，这个主题应该就是官网现实的主题，因为它就是作者的名字。`oh-my-posh`的主题样式还是很丰富的，除了我这里选择的`JanDeDobbeleer`，它还支持很多其他的样式和风格，各位小伙伴可以根据自己的喜好选择，具体的可以看项目文档或者`github`：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220111134434.png)



##### 字体下载

`Oh My Posh `设计采用的是` Nerd Fonts`字体，所以这里我们先要下载`Nerd Fonts`，这样最终的效果才更好，在`oh-my-posh`的文档中也给出了字体资源地址，各位小伙伴可以根据自己的需求下载：

```
https://www.nerdfonts.com/
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220111134143.png)

这里我选择的是`DejaVuSansMono Nerd Font`，显示效果还行。

字体下载之后解压，然后安装即可：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220111231727.png)

##### 设置字体

字体的设置也很简单，点击`windows Terminal`标题栏的下拉菜单，然后点击设置即可：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220111231822.png)

然后选中`power shell`，选择外观，修改字体，选择我们刚刚安装的` Nerd Fonts`字体即可：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220111000002.png)

然后点击保存之后，就可以看到`oh-my-posh`的效果已经出来了，颜值真的杠杠的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220111000133.png)



#### 添加power shell配置

虽然完成上面的配置之后，我们的终端美化已经完成了，但是如果关闭当前窗口重新打开，或者重新打开一个新的终端窗口，是需要重新执行如下操作的：

```shell
Import-Module posh-git
Import-Module oh-my-posh
Set-PoshPrompt -Theme JanDeDobbeleer
```

这样就很繁琐，而且很低效，所以为了让我们在终端打开的时候就有效果，我们还需要增加一些配置。首先要执行如下命令：

```sh
if (!(Test-Path -Path $PROFILE )) { New-Item -Type File -Path $PROFILE -Force }
```

这行命令的作用是启用`power shell`的配置，执行完成后，会在`C:\Users\用户名\Documents\WindowsPowerShell`下生成一个`ps1`结尾的文件，然后我们通过如下命令编辑这个文件：

```
notepad $PROFILE
```

并在其中加入如下内容：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220111133313.png)

也就是我们上面说的三行配置命令，然后保存，这样在我们下次打开`power shell`的时候，就会自动进行配置了。

这个文件其实就相当于`linux`的`.profile`文件，就是在初始化终端的时候，会先执行这个文件。



#### 补充

当然，我们也可以不安装`windows Terminal`，不过需要修改`power shell`的显示字体：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220111232855.png)

另外在`windows Terminal`的官方文档中也介绍了`oh-my-post`的安装配置方式，各位小伙伴也可以参考下：

```
https://docs.microsoft.com/zh-cn/windows/terminal/tutorials/custom-prompt-setup
```



### 结语

关于`power shell`的美化，我觉得没有什么总结的，唯一想说的是，终于找到了一款自己满意的`windows`的终端美化，看来真的是颜值才是第一生产力呀，最后放上`power shell`美化成果：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20220111233349.png)

最后，再插播一个小小的好消息，就是我之前说的`markdown`编辑器第一个可用版本已经出来了，打包也基本完成，明天我打算分享出来，感兴趣的小伙伴可以先尝尝鲜，好了，今天就先这样吧，各位小伙伴，晚安！