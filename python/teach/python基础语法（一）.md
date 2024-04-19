
### 依赖安装

依赖安装方式：
```sh
pip install 依赖名
# 例如 excel的依赖
pip install openpyxl
```


#### 指定镜像路径

由于国内网络限制，某些依赖安装特别慢，为了解决这种问题，我们可以通过指定国内镜像的方式来提升下载安装效率：

```sh
pip install openpyxl -i https://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
```

#### 修改本地配置

如果觉得这种方式太繁琐，也可以直接修改本地的配置，让我们`pip`默认就通过镜像站来安装：
1. 首先找到本地当前用户的路径，通常都在`C:\Users\用户名`，看下对应目录下是否有`pip`这个目录，如果没有手动创建；
2. 新建一个名称为`pip.ini`的文件
3. 在其中添加如下内容：
```c
[global] 
index-url = http://mirrors.aliyun.com/pypi/simple/ 
[install] 
trusted-host=mirrors.aliyun.com
```

