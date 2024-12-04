# nginx安装配置

## 安装

### linux

nginx可以使用各平台的默认包来安装，这里介绍的是使用源码编译安装，包括具体的编译参数信息。

正式开始前，编译环境gcc g++ 开发库之类的需要提前装好，这里默认你已经装好。

ububtu平台编译环境可以使用以下指令：

```sh
$ apt-get install build-essentialapt-get install libtool
```

centos平台编译环境使用如下指令

安装make：

```sh
$ yum -y install gcc automake autoconf libtool make
```

安装g++:

```sh
$ yum install gcc gcc-c++
```

下面正式开始
\---------------------------------------------------------------------------
一般我们都需要先装pcre, zlib，前者为了重写rewrite，后者为了gzip压缩。

#### 1.选定源码目录

可以是任何目录，本文选定的是/usr/local/src

```sh
$ cd /usr/local/src
```

#### 2.安装PCRE库

https://ftp.pcre.org/pub/pcre/ 下载最新的 PCRE 源码包，使用下面命令下载编译和安装 PCRE 包：

```sh
$ cd /usr/local/src
$ wget https://ftp.pcre.org/pub/pcre/pcre-8.44.tar.gz 
$ tar -zxvf pcre-8.44.tar.gzcd pcre-8.44
$ ./configure
$ make
$ make install
```

#### 3.安装zlib库

http://zlib.net/zlib-1.2.11.tar.gz 下载最新的 zlib 源码包，使用下面命令下载编译和安装 zlib包：

```sh
$ cd /usr/local/src 
$ wget http://zlib.net/zlib-1.2.11.tar.gz
$ tar -zxvf zlib-1.2.11.tar.gz
$ cd zlib-1.2.11
$ ./configure
$ make
$ make install
```

#### 4.安装ssl（某些vps默认没装ssl)

```sh
$ cd /usr/local/src
$ wget https://www.openssl.org/source/openssl-1.1.1g.tar.gz
$ tar -zxvf openssl-1.1.1g.tar.gz
```

#### 5.安装nginx

Nginx 一般有两个版本，分别是稳定版和开发版，您可以根据您的目的来选择这两个版本的其中一个，下面是把 Nginx 安装到 /usr/local/nginx 目录下的详细步骤：

```sh
$ cd /usr/local/src
$ wget http://nginx.org/download/nginx-1.18.0.tar.gz
$ tar -zxvf nginx-1.18.0.tar.gz
$ cd nginx-1.18.0 
$ ./configure --sbin-path=/usr/local/nginx/nginx \--conf-path=/usr/local/nginx/nginx.conf \--pid-path=/usr/local/nginx/nginx.pid \--with-http_gzip_static_module \--with-http_stub_status_module \--with-file-aio \--with-http_realip_module \--with-http_ssl_module \--with-pcre=/usr/local/src/pcre-8.44 \--with-zlib=/usr/local/src/zlib-1.2.11 \--with-openssl=/usr/local/src/openssl-1.1.1g 
$ make -j2
$ make install
```

- --with-pcre=/usr/local/src/pcre-8.44 指的是pcre-8.44 的源码路径。
- --with-zlib=/usr/local/src/zlib-1.2.11指的是zlib-1.2.11 的源码路径。

安装成功后 /usr/local/nginx 目录下如下:

```sh
fastcgi.conf            koi-win         		nginx.conf.default
fastcgi.conf.default    logs        			scgi_params
fastcgi_params     		mime.types     			scgi_params.default
fastcgi_params.default  mime.types.default 		uwsgi_params
html          			nginx        			uwsgi_params.default
koi-utf         		nginx.conf    		 	win-utf
```

#### 6.启动

启动就很简单了，linux环境下直接执行如下命令即可启动nginx：

```sh
$ nginx
```

如果提示不是有效的命令，你可以进入到nginx的安装目录下进行启动，比如我的路径`/usr/local/nginx `，然后执行如上命令即可启动，默认端口80，然后你就可以在在浏览器输入localhost或者127.0.0.1来访问nginx了，可以在浏览器看下效果：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200822092906.png)

### windows

相比linux，windows下相对简单，当然前提条件是你想开箱即用，而不是在本地编译。

#### 1.下载nginx

访问如下路径，选择对应的版本进行下载：

```html
http://nginx.org/en/download.html
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200822090741.png)

#### 2. 解压

解压刚刚下载的windows版本nginx，你可以看到如下目录结构：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200822091007.png)

目录与Linux下一致，这里就不做过多说明。

#### 3.启动

相比linux，Windows环境下就简单的多，直接双击nginx.exe文件即可启动。