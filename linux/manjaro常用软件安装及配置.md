#### 安装nodeJs

这里安装`nodeJs`是为了后面安装`picGo`的`gitee`插件，没有`nodeJs`插件是装不上的。

首先，官网下载对应系统的`tar`压缩文件，下载完成后解压

```sh
tar -vxf node-v14.18.1-linux-x64.tar.xz  
```

移动到目标路径，这里我直接放在了`opt`文件夹下：

```sh
sudo mv node-v14.18.1-linux-x64 /opt 
```

##### 建立链接

这里其实就是讲`npm`和`node`映射到`usr/local/bin`目录下，这样我们就可以在任意路径下执行`nmp`和`node`命令了，类似于配置环境变量。

```
sudo ln -s /opt/node-v14.18.1-linux-x64/bin/npm /usr/local/bin/ 
sudo ln -s /opt/node-v14.18.1-linux-x64/bin/node /usr/local/bin/
```

##### 修改更新源

```sh
npm config set registry https://registry.npm.taobao.org
```

