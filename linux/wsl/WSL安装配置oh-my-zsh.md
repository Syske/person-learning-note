# WSL安装配置oh-my-zsh

想必每一个使用`linux`的小伙伴，都希望自己的终端看起来炫酷高端上档次，所以这个美化操作肯定是少不了的。今天我们就来看下如何来通过`oh-my-zsh`来美化我们的`linux`终端，让它更炫酷。

#### 安装zsh

```
sudo apt-get install zsh
```

#### 安装oh-my-zsh

```
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

#### 配置主题

##### 自定义主题

这里是复制`agnoster`主题，然后修改其中的配色：

```
cp ~/.oh-my-zsh/themes/agnoster.zsh-theme ~/.oh-my-zsh/custom/themes/agnoster_wsl.zsh-theme
```

修改配色，这里改的是文件夹的颜色，原来的颜色是`blue`，但是在黑色背景下看着极其不友好：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20211008233850.png)

#### 修改主题

```
vim ~/.zshrc
```

找到`ZSH_THEME`，修改皮肤：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20211008234232.png)

#### 重载配置

```
source ~/.zshrc
```

至此大功告成！

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20211008234414.png)

如果你的终端修改之后，显示异常，可能是这样：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20211010224641.png)

那大概率是你的字体没有修改，这里推荐使用更纱黑体

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20211010224807.png)

这是一款开源字体，是可以商用的，下载地址如下：

```
https://github.com/lekoOwO/Sarasa-Cascadia
```

