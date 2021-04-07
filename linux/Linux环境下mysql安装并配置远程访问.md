### 1、下载mysql安装文件
```
[root@localhost ~]# wget http://dev.mysql.com/get/mysql-community-release-el7-5.noarch.rpm
```

### 2、安装下载的rpm文件

```
[root@localhost ~]# rpm -ivh mysql-community-release-el7-5.noarch.rpm
```

### 3、安装mysql服务

```
[root@localhost yum.repos.d]# yum install mysql-server

```
- 安装依赖文件可能需要花费很长时间，耐心等待，同时一路输入【Y】就好

### 3、修改mysql配置文件

```
[root@localhost yum.repos.d]# vim /etc/my.cnf
```
- 配置文件和windows环境无区别

```
# For advice on how to change settings please see
# http://dev.mysql.com/doc/refman/5.6/en/server-configuration-defaults.html

[mysqld]
#
# Remove leading # and set to the amount of RAM for the most important data
# cache in MySQL. Start at 70% of total RAM for dedicated server, else 10%.
# innodb_buffer_pool_size = 128M
#
# Remove leading # to turn on a very important data integrity option: logging
# changes to the binary log between backups.
# log_bin
#
# Remove leading # to set options mainly useful for reporting servers.
# The server defaults are faster for transactions and fast SELECTs.
# Adjust sizes as needed, experiment to find the optimal values.
# join_buffer_size = 128M
# sort_buffer_size = 2M
# read_rnd_buffer_size = 2M
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock

# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0

# Recommended in standard MySQL setup
sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES

[mysqld_safe]
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
```
- 修改完成后别忘记重启mysql服务
```
[root@localhost yum.repos.d]# service mysql restart
```

### 4、设置mysql远程访问

- 修改root密码
```
mysql> use mysql

mysql> update user set password=password('root') where user='root';

mysql> exit
```
- 修改完成后重启服务
```
[root@localhost yum.repos.d]# service mysql restart
```
- 通过用户名密码登录
```
[root@localhost yum.repos.d]# mysql -u root -p
```

- 修改主机限制，让mysql可以远程访问

```
mysql> grant all privileges on *.* to 'root'@'%' identified by 'password';

mysql> flush privileges;

mysql> exit;
```

- 重启mysql服务

```
[root@localhost yum.repos.d]# service mysql restart
```

- 开启端口
- - 经常用linux小伙伴肯定知道，linux很多端口默认是关闭，我们需要根据自己的需要进行开启，这里没有修改端口，按默认3306开启的，这个命令是通用的，要开启某个端口只需要将端口号改成对应的即可
```
[root@localhost yum.repos.d]# /sbin/iptables -I INPUT -p tcp --dport 3306 -j ACCEPT
```
- 然后就可远程连接我们linux环境下的mysql了
