
### 镜像下载刻录



### 系统分区

```sh
fdisk /dev/sda
```

### 安装




#### 配置网络

```sh
# 直接进入无线网络管理工具
iwctl
# 连接指定的wifi
station wlan0 connect syske-wifi
# 然后输入wifi密码
```

#### 挂载目录

```
# root分区挂载
mount /dev/nvme0n1p6 /mnt

# EFI 分区挂载
mount --mkdir /dev/nvme0n1p1 /mnt/boot
# home分区挂载
mount --mkdir /dev/sda3 /mnt/home
```

### 安装桌面环境

```sh
sudo pacman -S plasma kde-applications packagekit-qt5
```


### 安装中文输入法

#### 安装核心依赖

```sh
sudo pacman -S fcitx5 fcitx5-gtk fcitx5-configtool fcitx5-qt fcitx5-chinese-addons fcitx5-material-color kcm-fcitx5 fcitx5-lua

```

#### 配置环境

```sh
sudo vim /etc/environment 
```

```sh
# sougou pin yin input config
GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS=@im=fcitx
```

### 安装常用应用

#### 知识库软件

强烈推荐，我觉得很好用

```sh
yay -S obsidian
```

#### 国内常用软件

##### google chrome

```sh
yay -S google-chrome
```

##### dingtalk

```sh
yay -S dingtalk-bin
```

##### wechat

目前可以安装最新版本的原生`linux`版本微信，是基于`qt`开发的
```sh
yay -S wechat
```

