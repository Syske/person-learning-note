# 基于FileBrowser搭建轻量级文件服务器

`File Browser`是一款使用`Golang`开发的文件管理器，跨平台，费开源，功能强大。今天我们分享下手动安装`File Browser`的方法，熟悉下`File Browser`运作流程，当然最重要的是，希望它能够成为你的生产力工具，如果你有一台外网服务器，那你可以用它来搭建一个简易版的个人网盘，就算没有外网，在局域网环境下，你甚至可以用它来替代`samba`文件服务器或者`webdav`服务。
好了，下面我们就一起来看下详细的安装过程。

### 下载File Browser
首先我们要下载`File Browser`的安装包，直接下载对应平台的软件包即可，当然熟悉`go`的小伙伴可以自行编译。

 下载地址：
```
https://github.com/filebrowser/filebrowser/releases
```

下载地址中作者提供了各平台编译好的二进制文件，根据自己的平台下载解压即可，无需自行编译。

```bash
#下载File Browser
wget https://github.com/filebrowser/filebrowser/releases/download/v2.1.0/linux-amd64-filebrowser.tar.gz
#解压
tar -zxvf linux-amd64-filebrowser.tar.gz
#移动位置
mv filebrowser /usr/sbin
```

### 创建配置文件

`File Browser`支持`json`, `toml`, `yaml`, `yml`格式的配置文件，以`json`格式为例，命令如下：

```bash
#先创建一个目录用来存放数据库和配置文件
mkdir /etc/filebrowser/
#新建配置文件
vi /etc/filebrowser/config.json
```

`windows`环境下可以通过文本工具直接新建配置文件，配置内容是一样的，当然其中的路径需要改成`windows`的路径

复制下面的内容保存到`/etc/filebrowser/config.json`

```json
{
    "address":"0.0.0.0",
    "database":"/etc/filebrowser/filebrowser.db",
    "log":"/var/log/filebrowser.log",
    "port":8080,
    "root":"/home",
    "username":"admin"
}
```

上面参数含义为如下，请根据自身情况修改。

- address：监听地址
- database：数据库地址
- log：日志文件路径
- port：需要监听的端口
- root：需要读取哪个目录下的文件
- username：用户名

### 运行File Browser

参数`-c`是指定`File Browser`配置文件路径，请根据自身情况填写路径，命令如下：

```bash
#常规运行
filebrowser -c /etc/filebrowser/config.json
#如果需要保持在后台运行，执行
nohup filebrowser -c /etc/filebrowser/config.json &
```

配置文件中我们设置的监听端口为`8080`，不要忘记防火墙或安全组中放行这个端口。

```bash
#iptables放行端口
iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
service iptables save
#firewalld放行端口
firewall-cmd --zone=public --add-port=8080/tcp --permanent
firewall-cmd --reload
```

### 访问File Browser

如果一切顺利，未出现报错的情况下，访问`http://IP:8080`可看到File Browser登录界面，默认用户名为`admin`、密码为`admin`，**注意：登录后请自行修改密码**

### 扩展

创建配置数据库：

```
filebrowser -d /etc/filebrowser.db config init
```

设置监听地址：

```
filebrowser -d /etc/filebrowser.db config set --address 0.0.0.0
```

设置监听端口：

```
filebrowser -d /etc/filebrowser.db config set --port 8088
```

设置语言环境：

```
filebrowser -d /etc/filebrowser.db config set --locale zh-cn
```

设置日志位置：

```
filebrowser -d /etc/filebrowser.db config set --log /var/log/filebrowser.log
```

添加一个用户：

```
filebrowser -d /etc/filebrowser.db users add root password --perm.admin
```

其中的`root`和`password`分别是用户名和密码，根据自己的需求更改。

有关更多配置的选项，可以参考官方文档：https://docs.filebrowser.xyz/

配置修改好以后，就可以启动 `File Browser` 了，使用`-d`参数指定配置数据库路径。示例：

```
filebrowser -d /etc/filebrowser.db
```

启动成功就可以使用浏览器访问 `File Browser` 了，在浏览器输入 `IP`:端口，示例：
```
http://192.168.1.1:8088
```

#### 效果预览
登录之后的效果：
![](https://gitee.com/sysker/picBed/raw/master/images/20211111132747.png)

修改语言：
![](https://gitee.com/sysker/picBed/raw/master/images/20211111132927.png)
还可以对文件进行管理，包括分享、重命名、移动、删除、下载、上传等操作：
![](https://gitee.com/sysker/picBed/raw/master/images/20211111133024.png)
如果当作简易版的网盘来用也还不错