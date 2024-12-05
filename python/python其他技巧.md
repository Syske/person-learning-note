
#python

### 安装pip

#### 判断是否安装

```sh
pip --version
```

#### 安装

```sh
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py   # 下载安装脚本
$ sudo python get-pip.py    # 运行安装脚，如果是3.0以上的版本，直接通过python3执行即可
```
另外，还有一种安装方式：

```sh
# 如果是其他linux换对应的软件包管理工具即可
sudo pacman -S python-pip
```

#### 配置环境变量

添加如下环境变量

```sh
python安装目录\Scripts
```



### 虚拟环境

#### 创建

```sh
# 创建虚拟环境，这里的my-venv就是虚拟环境的名称
python3 -m venv my-venv
```

#### 激活

激活虚拟环境
```sh
source my-venv/bin/activate
```
激活后终端展示会有一些差异，前面会显示环境名称

### 配置国内镜像站

```sh
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple
pip config set install.trusted-host mirrors.aliyun.com
```