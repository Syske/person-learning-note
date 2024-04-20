
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

### 变量和常量 

#### 常量

字面意思，不会发生变化的数据，例如：
```python
pi = 3.141592
```

#### 变量

不确定的数据，在程序运行时，其值才能确定，例如：
```python
y = 10
x = y + 1
```

### python代码规范

#### 注释

##### 单行注释

```python
# 我是一行注释，为了说明下面的代码，定义一个变量x，赋值为10
x = 10
```

##### 多行注释

多行注释有两种方式，一种是通过`'''`（三个单引号）包裹，另一种是通过`"""`（三个双引号）包裹：

单引号方式

```python
'''
我是多行注释
我是多行注释
我是多行注释
'''
y = 20
```

双引号方式
```python
"""
我也是多行注释
我也是多行注释
我也是多行注释
"""
z = 30
```


#### 缩进

`python`的代码基本结构就是缩进，通过缩进我们可以确认代码块和方法

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240420212418.png)

通过缩进来实现代码块的区分是`python`的一个特点，其他语言中，通常都是通过`{}`和`;`来区分代码块的，比如`java`和`c`:

`java`
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240420212812.png)

`c`
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240420212942.png)
