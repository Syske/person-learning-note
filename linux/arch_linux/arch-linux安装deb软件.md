### 背景

由于公司出于安全考虑，需要通过阿里云`SASE`连接线上网络环境，但是并没有提供`arch`版本，于是我就想看下是否有方案可以解决，鬼使神差之下，竟然还真让我搞定了，下面分享下我的折腾过程。

### 安装过程

最开始问了通义千问，给的方案是`debtap`:
```sh
# 安装debtap
yay -S debtap
# 转换deb安装包
debtap your-package.deb
# 安装转换后的软件包
sudo pacman -U your-package.tar.zst
```

虽然通过上述方式安装成功了，但是不能正常启动，而且有一些问题：
1. 软件图标是空白
2. 直接执行`alisase`是可以正常执行的
于是我按照`alisase.desktop`文件的路径