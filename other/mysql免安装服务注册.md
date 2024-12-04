# mysql服务注册

1. 管理员身份运行`cmd`，进入解压后的`mysql`的`bin`文件夹，比如我的安装目录如下：

   ```sh
   cd D:\workspace\tools\mysql-5.7.19-winx64\bin
   ```

2. 安装`mysql`服务运行如下命令：

   ```sh
   mysqld --install mysql3307
   mysqld --install mysql --defaults-file="D:\tools\mysql-8.0.23-winx64\my.ini"
   ```

   其中，`mysql3307`是你要安装的服务名称，你可以自己指定

   如果有如下提示则表示服务已经安装成功：

   ```
   Service successfully installed.
   ```

   

3. 卸载`mysql`服务

   ```sh
   mysqld --remove mysql3307
   ```

   其中，`mysql3307`是你的要删除的服务名称

   如果有如下提示，则表示删除成功：

   ```
   Service successfully removed.
   ```

4. 添加配置文件

   ```ini
   [mysql]
   # 设置mysql客户端默认字符集
   default-character-set=utf8
    
   [mysqld]
   # 绑定IPv4
   bind-address=0.0.0.0
   # 设置端口号
   port=3306
   # 设置mysql的安装目录，即解压目录
   basedir=D:\\tools\\mysql-8.0.23-winx64
   # 设置数据库的数据存放目录
   datadir=D:\\tools\\mysql-8.0.23-winx64\\data
   # 设置允许最大连接数
   max_connections=200
   # 设置允许连接失败次数
   max_connect_errors=10
   # 设置服务端的默认字符集
   character-set-server=utf8
   # 创建表使用的默认存储引擎
   default-storage-engine=INNODB
   # 使用“mysql_native_password”插件认证
   default_authentication_plugin=mysql_native_password
   ```

   

5. 启动服务：

   ```sh
   net start mysql3307
   ```

   其中`mysql3307`是服务名

（1）初始化mysql（记住随机密码）：

```
mysqld --initialize --console
```

随机密码为：%tbmq)f<;3jE

目录会多处data文件夹

（2）安装mysql服务：

```
mysqld --install mysql --defaults-file="D:\mysql-8.0.16-winx64\my.ini"
```

切换管理员身份运行

![img](https://img2018.cnblogs.com/blog/1627739/201906/1627739-20190620015148365-1323561363.png)

（3）启动mysql服务：

```
net start mysql
```



（4）登录mysql：

```
mysql -uroot -p
```

密码为之前的随机密码：：%tbmq)f<;3jE

（5）修改密码：

```
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '新密码';
```

![img](https://img2018.cnblogs.com/blog/1627739/201906/1627739-20190620020223252-138085659.png)

退出重新登录

![img](https://img2018.cnblogs.com/blog/1627739/201906/1627739-20190620021250850-1721675715.png)

这里附上一份之前写过的mysql的临时启动脚本：

```bash
Set MYSQL_HOME=%~sdp0mysql-5.7.19-winx64
Set PATH=%MYSQL_HOME%\bin;%path%
mysqld --remove
mysqld --install

net start mysql
mysql -u root -p
pause
```

服务停止脚本，并卸载服务

```bash
net stop mysql
sc delete mysql

pause
```

服务重启脚本

```bash
echo "stoping mysql"

net stop mysql

echo "deleting mysql sever"

sc delete mysql

echo "restarting mysql"

Set MYSQL_HOME=%~sdp0mysql-5.7.19-winx64
Set PATH=%MYSQL_HOME%\bin;%path%

mysqld --install

net start mysql
mysql -u root -p
pause
```

启动`mysql`服务，并启动`navcat`:

```bash
Set MYSQL_HOME=%~sdp0mysql-5.7.19-winx64
Set PATH=%MYSQL_HOME%\bin;%path%
mysqld --remove
mysqld --install

net start mysql
%~sdp0%Navicat_for_MySQL\navicat.exe
pause
```

