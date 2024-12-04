
### 安装铜豌豆应用市场

#### 安装依赖

 root 命令行添加（推荐方式）
```
请用 root 账号在命令行执行如下命令：
```sh
# 安装wget
$ sudo apt -y install wget
# 下载铜豌豆
$ wget -c -O atzlinux-v12-archive-keyring_lastest_all.deb https://www.atzlinux.com/atzlinux/pool/main/a/atzlinux-archive-keyring/atzlinux-v12-archive-keyring_lastest_all.deb
# 安装铜豌豆
$ sudo apt -y install ./atzlinux-v12-archive-keyring_lastest_all.deb
# 更新软件源
$ sudo apt update
```

部分系统，支持直接双击 deb 软件包安装，或者在右键菜单中安装，这类系统可以直接下载软件包并安装。  铜豌豆软件源安装包的下载地址为： [deb安装包](https://www.atzlinux.com/atzlinux/pool/main/a/atzlinux-archive-keyring/atzlinux-v12-archive-keyring_lastest_all.deb)


#### 安装铜豌豆应用市场
```sh
sudo apt install atzlinux-store-v12
```

市场文档：[软件列表](https://www.atzlinux.com/allpackages.htm)

### 安装微信

```sh
# 安装前最好先更新下软件库
sudo apt update
# 安装微信
sudo apt -y install wechat

# 启动
wechat
```

