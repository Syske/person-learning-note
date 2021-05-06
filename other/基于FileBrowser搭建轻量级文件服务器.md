# 基于FileBrowser搭建轻量级文件服务器

File Browser是一款使用Golang开发的文件管理器，跨平台，免费开源，功能强大。这篇文章分享下CentOS 7手动安装File Browser的方法，熟悉下File Browser运作流程，不至于后期出现问题不知所措。

### 下载File Browser

- 下载地址：https://github.com/filebrowser/filebrowser/releases

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

File Browser支持json, toml, yaml, yml格式的配置文件，以`json`格式为例，命令如下：

```bash
#先创建一个目录用来存放数据库和配置文件
mkdir /etc/filebrowser/
#新建配置文件
vi /etc/filebrowser/config.json
```

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

参数`-c`是指定File Browser配置文件路径，请根据自身情况填写路径，命令如下：

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

配置修改好以后，就可以启动 File Browser 了，使用`-d`参数指定配置数据库路径。示例：

```
filebrowser -d /etc/filebrowser.db
```

启动成功就可以使用浏览器访问 File Browser 了，在浏览器输入 IP:端口，示例：http://192.168.1.1:8088