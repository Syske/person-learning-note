## FastDFS文件服务器部署

#### 前言

　　FastDFS(Fast Distributed File System)是一款开源轻量级分布式文件系统，本文不讲解原理和架构，只是在个人使用部署过程中耗费了好长时间和精力，遇到了很多的坑，于是总结成了一篇详细的部署文档分享给大家。

#### 安装libfastcommon

1. 获取libfastcommon安装包：

   ```
   wget https://github.com/happyfish100/libfastcommon/archive/V1.0.38.tar.gz
   ```

2. 解压安装包：tar -zxvf V1.0.38.tar.gz

3. 进入目录：cd libfastcommon-1.0.38

4. 执行编译：./make.sh

5. 安装：./make.sh install
   ![img](https://www.cnblogs.com/handsomeye/p/media/15336343653165/15337305933144.jpg)￼![img](https://images2018.cnblogs.com/blog/872887/201808/872887-20180809201417899-464673029.jpg)

> 可能遇到的问题：
>
> ```
> -bash: make: command not found
> -bash: gcc: command not found解决方案：
> debian通过apt-get install gcc make安装
> centos通过yum -y install gcc make安装
> ```

#### 安装FastDFS

1. 获取fdfs安装包：

   ```
   wget https://github.com/happyfish100/fastdfs/archive/V5.11.tar.gz
   ```

2. 解压安装包：tar -zxvf V5.11.tar.gz

3. 进入目录：cd fastdfs-5.11

4. 执行编译：./make.sh

5. 安装：./make.sh install
   ![img](https://www.cnblogs.com/handsomeye/p/media/15336343653165/15337308994594.jpg)￼![img](https://images2018.cnblogs.com/blog/872887/201808/872887-20180809201558576-1766872984.jpg)

6. 查看可执行命令：ls -la /usr/bin/fdfs*
   ![img](https://www.cnblogs.com/handsomeye/p/media/15336343653165/15337309199921.jpg)￼![img](https://images2018.cnblogs.com/blog/872887/201808/872887-20180809201650045-2014679422.jpg)

#### 配置Tracker服务

1. 进入/etc/fdfs目录，有三个.sample后缀的文件（自动生成的fdfs模板配置文件），通过cp命令拷贝tracker.conf.sample，删除.sample后缀作为正式文件：
    ![img](https://www.cnblogs.com/handsomeye/p/media/15336343653165/15336945272527.jpg)￼![img](https://images2018.cnblogs.com/blog/872887/201808/872887-20180809201733659-143141345.jpg)

2. 编辑tracker.conf：vi tracker.conf，修改相关参数

   ```
   base_path=/home/mm/fastdfs/tracker  #tracker存储data和log的跟路径，必须提前创建好
   port=23000 #tracker默认23000
   http.server_port=80 #http端口，需要和nginx相同
   ```

3. 启动tracker（支持start|stop|restart）：

   ```
   /usr/bin/fdfs_trackerd /etc/fdfs/tracker.conf start
   ```

4. 查看tracker启动日志：进入刚刚指定的base_path(/home/mm/fastdfs/tracker)中有个logs目录，查看tracker.log文件
   ![img](https://www.cnblogs.com/handsomeye/p/media/15336343653165/15337310825651.jpg)￼![img](https://images2018.cnblogs.com/blog/872887/201808/872887-20180809201823407-1669604672.jpg)

5. 查看端口情况：netstat -apn|grep fdfs
   ![img](https://www.cnblogs.com/handsomeye/p/media/15336343653165/15337310995196.jpg)￼![img](https://images2018.cnblogs.com/blog/872887/201808/872887-20180809201847657-2001149194.jpg)

> 可能遇到的报错：
>
> ```
> /usr/bin/fdfs_trackerd: error while loading shared libraries: libfastcommon.so: cannot open shared object file: No such file or directory
> 解决方案：建立libfastcommon.so软链接
> ln -s /usr/lib64/libfastcommon.so /usr/local/lib/libfastcommon.so
> ln -s /usr/lib64/libfastcommon.so /usr/lib/libfastcommon.so
> ```

#### 配置Storage服务

1. 进入/etc/fdfs目录，有cp命令拷贝storage.conf.sample，删除.sample后缀作为正式文件;

2. 编辑storage.conf：vi storage.conf，修改相关参数：

   ```
   base_path=/home/mm/fastdfs/storage   #storage存储data和log的跟路径，必须提前创建好
   port=23000  #storge默认23000，同一个组的storage端口号必须一致
   group_name=group1  #默认组名，根据实际情况修改
   store_path_count=1  #存储路径个数，需要和store_path个数匹配
   store_path0=/home/mm/fastdfs/storage  #如果为空，则使用base_path
   tracker_server=10.122.149.211:22122 #配置该storage监听的tracker的ip和port
   ```

3. 启动storage（支持start|stop|restart）：

   ```
   /usr/bin/fdfs_storaged /etc/fdfs/storage.conf start
   ```

4. 查看storage启动日志：进入刚刚指定的base_path(/home/mm/fastdfs/storage)中有个logs目录，查看storage.log文件
   ![img](https://www.cnblogs.com/handsomeye/p/media/15336343653165/15337313133469.jpg)￼![img](https://images2018.cnblogs.com/blog/872887/201808/872887-20180809201921189-16317155.jpg)

5. 此时再查看tracker日志：发现已经开始选举，并且作为唯一的一个tracker，被选举为leader
   ![img](https://www.cnblogs.com/handsomeye/p/media/15336343653165/15337312505783.jpg)￼![img](https://images2018.cnblogs.com/blog/872887/201808/872887-20180809201950722-1959554309.jpg)

6. 查看端口情况：netstat -apn|grep fdfs
   ![img](https://www.cnblogs.com/handsomeye/p/media/15336343653165/15337313336921.jpg)￼![img](https://images2018.cnblogs.com/blog/872887/201808/872887-20180809202028138-670884814.jpg)

7. 通过monitor来查看storage是否成功绑定：

   ```
   /usr/bin/fdfs_monitor /etc/fdfs/storage.conf
   ```

   ![img](https://www.cnblogs.com/handsomeye/p/media/15336343653165/15337856394714.jpg)￼![img](https://images2018.cnblogs.com/blog/872887/201808/872887-20180809202102192-1479269612.jpg)

#### 安装Nginx和fastdfs-nginx-module模块

1. 下载Nginx安装包

   ```
   wget http://nginx.org/download/nginx-1.15.2.tar.gz
   ```

2. 下载fastdfs-nginx-module安装包

   ```
   wget https://github.com/happyfish100/fastdfs-nginx-module/archive/V1.20.tar.gz
   ```

3. 解压nginx：tar -zxvf nginx-1.15.2.tar.gz

4. 解压fastdfs-nginx-module：tar -xvf V1.20.tar.gz

5. 进入nginx目录：cd nginx-1.10.1

6. 安装依赖的库

   ```
   apt-get update
   apt-get install libpcre3 libpcre3-dev openssl libssl-dev libperl-dev
   ```

7. 配置，并加载fastdfs-nginx-module模块：

   ```
   ./configure --prefix=/usr/local/nginx --add-module=/usr/local/src/fastdfs-nginx-module-1.20/src/
   ```

8. 编译安装：

   ```
   make
   make install
   ```

9. 查看安装路径：whereis nginx
   ![img](https://www.cnblogs.com/handsomeye/p/media/15336343653165/15337133899604.jpg)￼![img](https://images2018.cnblogs.com/blog/872887/201808/872887-20180809202137626-1411197392.jpg)

10. 启动、停止：

    ```
    cd /usr/local/nginx/sbin/
    ./nginx 
    ./nginx -s stop #此方式相当于先查出nginx进程id再使用kill命令强制杀掉进程
    ./nginx -s quit #此方式停止步骤是待nginx进程处理任务完毕进行停止
    ./nginx -s reload
    ```

11. 验证启动状态：wget "[http://127.0.0.1](http://127.0.0.1/)"
    ![img](https://www.cnblogs.com/handsomeye/p/media/15336343653165/15337136494427.jpg)￼![img](https://images2018.cnblogs.com/blog/872887/201808/872887-20180809202214623-946184752.jpg)

12. 查看此时的nginx版本：发现fastdfs模块已经安装好了
    ![img](https://www.cnblogs.com/handsomeye/p/media/15336343653165/15337338955675.jpg)￼![img](https://images2018.cnblogs.com/blog/872887/201808/872887-20180809202240570-1449488718.jpg)

> 可能的报错：
>
> ```
> /usr/include/fastdfs/fdfs_define.h:15:27: fatal error: common_define.h: No such file or directory
> 解决方案：修改fastdfs-nginx-module-1.20/src/config文件，然后重新第7步开始
> ngx_module_incs="/usr/include/fastdfs /usr/include/fastcommon/"
> CORE_INCS="$CORE_INCS /usr/include/fastdfs /usr/include/fastcommon/"
> ```

#### 配置Nginx和fastdfs-nginx-module模块

1. 配置mod-fastdfs.conf，并拷贝到/etc/fdfs文件目录下

   ```
   cd fastdfs-nginx-module-1.20/src/
   cp mod_fastdfs.conf /etc/fdfs
   ```

2. 进入/etc/fdfs修改mod-fastdfs.conf：

   ```
   base_path=/home/mm/fastdfs
   tracker_server=10.122.149.211:22122 #tracker的地址
   url_have_group_name=true #url是否包含group名称
   storage_server_port=23000 #需要和storage配置的相同
   store_path_count=1  #存储路径个数，需要和store_path个数匹配
   store_path0=/home/mm/fastdfs/storage #文件存储的位置
   ```

3. 配置nginx，80端口server增加location如图：

   ```
   cd /usr/local/nginx/conf/
   vi nginx.conf
   ```

   ![img](https://www.cnblogs.com/handsomeye/p/media/15336343653165/15337371363160.jpg)￼![img](https://images2018.cnblogs.com/blog/872887/201808/872887-20180809202311512-242475061.jpg)

4. 最后需要拷贝fastdfs解压目录中的http.conf和mime.types：

   ```
   cd /usr/local/src/fastdfs-5.11/conf
   cp mime.types http.conf /etc/fdfs/
   ```

#### FastDFS常用命令测试

###### 上传文件

1. 进入/etc/fdfs目录，有cp命令拷贝client.conf.sample，删除.sample后缀作为正式文件;

2. 修改client.conf相关配置：

   ```
   base_path=/home/mm/fastdfs/tracker //tracker服务器文件路径
   tracker_server=10.122.149.211:22122 //tracker服务器IP地址和端口号
   http.tracker_server_port=80 # tracker服务器的http端口号，必须和tracker的设置对应起来
   ```

3. 新建一个测试文档1.txt，内容为abc

4. 命令：

   ```
   /usr/bin/fdfs_upload_file  <config_file> <local_filename>
   ```

5. 示例：

   ```
   /usr/bin/fdfs_upload_file  /etc/fdfs/client.conf 1.txt
   ```

   ![img](https://www.cnblogs.com/handsomeye/p/media/15336343653165/15337784246114.jpg)￼![img](https://images2018.cnblogs.com/blog/872887/201808/872887-20180809202336022-709784961.jpg)

   ```
   组名：group1 
   磁盘：M00 
   目录：00/00 
   文件名称：CnqV01trmeyAbAN0AAAABLh3frE677.txt
   ```

6. 查看结果，进入storage的data目录：
   ![img](https://www.cnblogs.com/handsomeye/p/media/15336343653165/15337784664094.jpg)￼![img](https://images2018.cnblogs.com/blog/872887/201808/872887-20180809202411258-781795640.jpg)

7. 通过wget和浏览器方式访问成功：

   ```
   wget http://10.122.149.211/group1/M00/00/00/CnqV01trmeyAbAN0AAAABLh3frE677.txt
   ```

   ![img](https://images2018.cnblogs.com/blog/872887/201808/872887-20180809202432874-797393323.jpg)![img](https://www.cnblogs.com/handsomeye/p/media/15336343653165/15337785584356.jpg)￼
   ![img](https://www.cnblogs.com/handsomeye/p/media/15336343653165/15337786914419.jpg)![img](https://images2018.cnblogs.com/blog/872887/201808/872887-20180809202458223-206849066.jpg)

###### 下载文件：

1. 命令：

   ```
   /usr/bin/fdfs_download_file <config_file> <file_id> [local_filename]
   ```

2. 示例：

   ```
   /usr/bin/fdfs_download_file /etc/fdfs/client.conf group1/M00/00/00/CnqV01trmeyAbAN0AAAABLh3frE677.txt a.txt
   ```

3. 查看结果：
   ![img](https://www.cnblogs.com/handsomeye/p/media/15336343653165/15337787854610.jpg)￼![img](https://images2018.cnblogs.com/blog/872887/201808/872887-20180809202520219-917840558.jpg)

###### 删除文件：

1. 命令：

   ```
   /usr/bin/fdfs_delete_file <config_file> <file_id>
   ```

2. 示例：

   ```
   /usr/bin/fdfs_delete_file /etc/fdfs/client.conf group1/M00/00/00/CnqV01trmeyAbAN0AAAABLh3frE677.txt
   ```

3. 查看结果，进入storage的data目录文件不存在，通过wget再次获取404：
   ![img](https://www.cnblogs.com/handsomeye/p/media/15336343653165/15337370913044.jpg)![img](https://images2018.cnblogs.com/blog/872887/201808/872887-20180809202556468-1477150959.jpg)