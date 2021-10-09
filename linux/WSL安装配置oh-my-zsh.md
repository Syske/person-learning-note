# WSL安装配置oh-my-zsh

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

![](https://gitee.com/sysker/picBed/raw/master/blog/20211008233850.png)

#### 修改主题

```
vim ~/.zshrc
```

找到`ZSH_THEME`，修改皮肤：

![](https://gitee.com/sysker/picBed/raw/master/blog/20211008234232.png)

#### 重载配置

```
source ~/.zshrc
```

至此打工告成！

![](https://gitee.com/sysker/picBed/raw/master/blog/20211008234414.png)