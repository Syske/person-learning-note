
## 前言

由于大家之前都没有计算机基础，对编程本身没有太多的认知，所以在开始`python`学习之前，先给大家介绍一些基本的计算机基础知识。

## 计算机基础


### 关键词和概念

#### 环境变量

这个就是字面意思，“环境”指的就是我们的计算机环境，“变量”属于计算机领域的抽象概念，大家可以将“变量”理解为一个标记或者符号，用来指代某个有意义的值，比如我们说苹果的价格是`5`元/斤，那么在后续谈话中，我们再次谈到“苹果的价格”，那我们就知道它指的是`5`元/斤。
计算机的环境变量也有着类似的逻辑，比如我们定义了一个变量，这个变量的含义是一个路径，将变量名称设置为`PYTHON_HOME`，将它的值设置为我们的`python`安装路径，那在这台计算机的运行环境中，`PYTHON_HOME`就指向了我们的`python`安装路径：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240406224129.png)

#### 命令行/CMD

通常我们使用一个软件的时候，都是通过图形界面的，但是在图形界面诞生之前，我们和计算机只能通过命令行交互，虽然计算机发展很迅速，已经经历了几十年的发展，但命令行交互并没有被废除，而且很多时候命令行比图形化界面交互更方便。

这里我们以`windows`操作系统为例，命令行工具启动快捷键为`Ctrl+R`，然后输入`cmd`，回车即可启动命令行工具：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240406224605.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240406224630.png)



#### 文件路径

文件路径，通常指的是一个文件或者文件夹在计算机上的存放地址，比如下面这个地址：

```
D:\workspace\dev-tools\python\python39
.\python\python39
```

我们把文件路径类比为家庭住址，比如陕西省西安市雁塔区丈八六路`001`号。
程序在处理一个文件或者文件夹时，通常支持两种路径：

- 绝对路径：就类似我们上面的完整地址，包括省市区等完整地址
- 相对路径：当我们同处一个城市的时候，我们可以省略省份和城市，直接说某某区某某路



#### 文件属性

- **只读**：只能对文件内容进行读取，无法写入
- **读写**: 可以对文件内容进行读取或者写入


#### 文件后缀

常见的文件后缀有 *.jpg, *.txt, *.exe, *.xls, *.doc, *.py

展示文件后缀的方式

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240407143348.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240407143334.png)


### python环境安装

#### 下载安装

下载地址：

```
https://www.python.org/downloads/
```

国内推荐下面的地址：

```sh
https://mirrors.huaweicloud.com/python/3.9.9/python-3.9.9-amd64.exe
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240407143854.png)



#### 配置环境变量

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240408210911.png)

#### 编写第一个脚本

```python
print("hello word")
```


