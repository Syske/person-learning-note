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

，其中的`root`和`password`分别是用户名和密码，根据自己的需求更改。



配置修改好以后，就可以启动 File Browser 了，使用`-d`参数指定配置数据库路径。示例：

```
filebrowser -d /etc/filebrowser.db
```

