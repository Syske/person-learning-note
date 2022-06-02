# [Windows下搭建Redis集群](https://www.cnblogs.com/tommy-huang/p/6240083.html)



###  [Redis集群](http://redis.cn/topics/cluster-tutorial.html)：

如果部署到多台电脑，就跟普通的集群一样；因为Redis是单线程处理的，多核CPU也只能使用一个核，所以部署在同一台电脑上，通过运行多个Redis实例组成集群，然后能提高CPU的利用率。

 

### 在Windows系统下搭建Redis集群：

需要4个部件：

- Redis

- Ruby语言运行环境
- Redis的Ruby驱动redis-xxxx.gem
- 创建Redis集群的工具redis-trib.rb

安装Redis，并运行3个实例(Redis集群需要至少3个以上节点，低于3个无法创建);

使用redis-trib.rb工具来创建Redis集群，由于该文件是用ruby语言写的，所以需要安装Ruby开发环境，以及驱动redis-xxxx.gem

### 1.下载并安装Redis

其GitHub路径如下：https://github.com/MSOpenTech/redis/releases/

Redis提供msi和zip格式的下载文件，这里下载zip格式 3.0.504版本

将下载到的Redis-x64-3.0.504.zip解压即可，为了方便使用，建议放在盘符根目录下，并修改目录名为Redis，如：C:\Redis 或者D:\Redis

通过配置文件来启动3个不同的Redis实例，由于Redis默认端口为6379，所以这里使用了6380、6381、6382来运行3个Redis实例。

**注意：为了避免不必要的错误，配置文件尽量保存为utf8格式，并且不要包含注释；**

**配置文件中以下两种保存日志的方式(保存在文件中、保存到System Log中)请根据需求选择其中一种即可：**

```
　　loglevel notice                       #日志的记录级别，notice是适合生产环境的
　　logfile "D:/Redis/Logs/redis6380_log.txt"      #指定log的保持路径,默认是创建在Redis安装目录下，如果有子目录需要手动创建，如此处的Logs目录
 　 syslog-enabled yes       #是否使用系统日志 　　　　syslog-ident redis6380   #在系统日志的标识名  这里使用了保存在文件中的方式，所以先在Redis目录D:/Redis下新建Logs文件夹
```

redis.6380.conf 内容如下：

```sh
port 6380      
loglevel notice    
logfile "D:/Redis/Logs/redis6380_log.txt"       
appendonly yes
appendfilename "appendonly.6380.aof"   
cluster-enabled yes                                    
cluster-config-file nodes.6380.conf
cluster-node-timeout 15000
cluster-slave-validity-factor 10
cluster-migration-barrier 1
cluster-require-full-coverage yes
```

 redis.6381.conf 内容如下：

```sh
port 6381       
loglevel notice   
logfile "D:/Redis/Logs/redis6381_log.txt"       
appendonly yes
appendfilename "appendonly.6381.aof"    
cluster-enabled yes                                    
cluster-config-file nodes.6381.conf
cluster-node-timeout 15000
cluster-slave-validity-factor 10
cluster-migration-barrier 1
cluster-require-full-coverage yes
```

redis.6382.conf 内容如下：

```sh
port 6382       
loglevel notice    
logfile "D:/Redis/Logs/redis6382_log.txt"         
appendonly yes
appendfilename "appendonly.6382.aof"    
cluster-enabled yes                                    
cluster-config-file nodes.6382.conf
cluster-node-timeout 15000
cluster-slave-validity-factor 10
cluster-migration-barrier 1
cluster-require-full-coverage yes
```

**配置内容的解释如下：**

将上述配置文件保存到Redis目录下，并使用这些配置文件安装3个redis服务，命令如下：

注意：redis.6380.conf等配置文件最好使用完整路径，避免重启Redis集群出现问题,博主的安装目录为D:/Redis

```sh
D:/Redis/redis-server.exe --service-install D:/Redis/redis.6380.conf --service-name redis6380
D:/Redis/redis-server.exe --service-install D:/Redis/redis.6381.conf --service-name redis6381
D:/Redis/redis-server.exe --service-install D:/Redis/redis.6382.conf --service-name redis6382
```

启动这3个服务，命令如下：

```sh
D:/Redis/redis-server.exe --service-start --service-name Redis6380
D:/Redis/redis-server.exe --service-start --service-name Redis6381
D:/Redis/redis-server.exe --service-start --service-name Redis6382
```

执行结果：       ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/578448-20170101000748273-1080049971-1616040007085.png)

### 2.下载并安装ruby

#### 　 2.1. 下载路径如下：

　　http://dl.bintray.com/oneclick/rubyinstaller/rubyinstaller-2.2.4-x64.exe

下载后，双击安装即可，同样，为了操作方便，也是建议安装在盘符根目录下，如： C:\Ruby22-x64 ，安装时这里选中后两个选项，

意思是将ruby添加到系统的环境变量中，在cmd命令中能直接使用ruby的命令

​    ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/578448-20161231232630711-211501252-1616040007087.png)

####    2.2.下载ruby环境下Redis的驱动，考虑到兼容性，这里下载的是3.2.2版本

https://rubygems.org/gems/redis/versions/3.2.2

注意：下载在页面右下角相关连接一项中

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/578448-20161231224127351-260128949-1616040007088.png)

​           

安装该驱动，命令如下：

```
gem install --local path_to_gem/filename.gem  
```

​       实际操作如下：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/578448-20161231233209898-1115746848-1616040007088.png)

####       2.3.下载Redis官方提供的创建Redis集群的ruby脚本文件redis-trib.rb，路径如下：

　　　　https://raw.githubusercontent.com/MSOpenTech/redis/3.0/src/redis-trib.rb

打开该链接如果没有下载，而是打开一个页面，那么将该页面保存为**redis-trib.rb**

建议保存到Redis的目录下。             

　　注意：因为redis-trib.rb是ruby代码，必须用ruby来打开，若redis-trib.rb无法识别，需要手动选择该文件的打开方式：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/QQ图片20170712112440-1616040007089.png)

​                  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/QQ图片20170712112842-1616040007089.png)

​	选择ruby为的打开方式后，redis-trib.rb的logo都会发生改变，如下图：

 ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/QQ图片20170712112431-1616040007090.png)

 

###   3.创建Redis集群  

​     CMD下切换到Redis目录，使用redis-trib.rb来创建Redis集群：

```
redis-trib.rb create --replicas 0 127.0.0.1:6380 127.0.0.1:6381 127.0.0.1:6382 
```

　　执行结果：

   ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/578448-20170103100940691-382820890-1616040007090.jpg)

​     当出现提示时，需要手动输入yes，输入后，当出现以下内容，说明已经创建了Redis集群

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/578448-20170103101131050-439447930-1616040007091.jpg)

​     检验是否真的创建成功，输入以下命令：

```
redis-trib.rb check 127.0.0.1:6380
```

​     出现以下信息，说明创建的Redis集群是没问题的

 ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/578448-20170103114028206-281352717-1616040007091.png)

   使用Redis客户端Redis-cli.exe来查看数据记录数，以及集群相关信息

```
D:/Redis/redis-cli.exe -c -p 6380
```

   -c 表示 cluster

   -p 表示 port 端口号

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/578448-20170105170548003-2022751429-1616040007091.png)

   输入dbsize查询 记录总数

```
dbsize
```

   或者一次输入完整命令：

```
D:/Redis/redis-cli.exe -c -p 6380 dbsize
```

​    结果如下：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/578448-20170105170856269-1044676861-1616040007092.png)

​    输入cluster info可以从客户端的查看集群的信息：

```
cluster info
```

　结果如下：

  ![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/578448-20170105171104691-1699042108.png)