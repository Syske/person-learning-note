## 环境说明：
 - linux : centOS
 - jdk : 1.8
 - tomcat : 8.5
 - redis : 4.0

## jdk安装配置

### 1、下载jdk(这里下载的是jdk-8u181-linux-x64.tar.gz)
 - 当然你可以直接下载rpm格式的，这样更简单，一键安装
 - 压缩版的需要自己解压并已配置环境变量，不过对于喜欢折腾的小伙伴来说，这种方式更有趣
 
### 2、解压
```
tar -zxvf jdk-8u181-linux-x64.tar.gz
```

### 3、配置环境变量

- 将解压后的文件夹移动到想要存放的文件夹下，这里我放在了</usr/lib/>下

```
mv -r jdk1.8.0_181 /usr/lib/
```
- 配置环境变量

```
vim /etc/profile
```
- 将jdk环境变量添加至profile

```
JAVA_HOME=/usr/lib/jdk1.8.0_181

JRE_HOME=$JAVA_HOME/jre

CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib

export JAVA_HOME JRE_HOME PATH CLASSPATH

```

### 4、重新加载profile

```
source /etc/profile
```

## TOMCAT

### 1、下载
- 这里下载的是apache-tomcat-8.5.32.tar.gz，也是压缩包

### 2、解压
```
tar -zxvf apache-tomcat-8.5.32.tar.gz
```
### 3、配置环境变量

- 将解压后的文件夹移动到想要存放的文件夹下，这里我放在了</usr/lib/>下

```
mv -r apache-tomcat-8.5.32 /usr/lib/
```
- 配置环境变量

```
vim /etc/profile
```


- 将tomcat环境变量添加至profile
```
#tomcat
export CATALINA_HOME=/usr/lib/apache-tomcat-8.5.32

export CATALINA_BASE=/usr/lib/apache-tomcat-8.5.32

```

### 4、重新加载profile

```
source /etc/profile
```

## redis

### 1、下载

```
wget http://download.redis.io/releases/redis-4.0.2.tar.gz
```

### 2、解压
```
tar -zxvf redis-4.0.2.tar.gz
```
### 3、编译

- 进入redis-4.0.2.tar.gz解压后的文件夹

```
make
```

### 4、安装

- 同样的文件夹
```
make install
```
### 5、配置

- 配置这里就不再赘述了，和windows是一样的

### 6、启动

- 启动服务器
```
[root@localhost /]# redis-server
```

- 启动客户端
```
[root@localhost /]# redis-cli
```