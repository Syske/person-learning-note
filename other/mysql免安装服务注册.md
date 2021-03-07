# mysql服务注册

1. 管理员身份运行`cmd`，进入解压后的`mysql`的`bin`文件夹，比如我的安装目录如下：

   ```sh
   cd D:\workspace\tools\mysql-5.7.19-winx64\bin
   ```

2. 安装`mysql`服务运行如下命令：

   ```sh
   mysqld --install mysql3307
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

4. 启动服务：

   ```sh
   net start mysql3307
   ```

   其中`mysql3307`是服务名

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

