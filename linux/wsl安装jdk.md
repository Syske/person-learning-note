# wsl安装jdk

#### JDK下载链接

```
https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html
```
#### JDK加密限制策略文件下载链接（可省略）

```
https://www.oracle.com/technetwork/java/javase/downloads/jce-all-download-5170447.html
```
#### 解压tar.gz文件

```
tar -xzvf jdk-*.tar.gz
```
#### 移动解压文件

```
rm -fr jdk-*.tar.gz
mk the jvm dir
sudo mkdir -p /usr/lib/jvm
move the server jre
sudo mv jdk1.8* /usr/lib/jvm/oracle_jdk8
```

#### 解压jce_policy，并安装(可省略)

```
export JAVA_HOME=/usr/lib/jvm/oracle_jdk8
```

##### 重新加载配置文件

```
source ~/.profile
```

#### 测试下

```
java --version
```

![](https://gitee.com/sysker/picBed/raw/master/images/20200512110706.png)