#python 
## 简介

### 项目地址

```
https://tqdm.github.io/
```


## 安装

库官方地址

```
https://pypi.org/project/tqdm/
```

安装命令

```shell
pip install tqdm
```


## 常用示例

### 进度条效果

```python
from tqdm import tqdm
for i in tqdm(range(10000)):
    print(i)
```
效果

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/202403122333761.png)
我们还可以设置进度条的描述信息：
```python
for i in tqdm(range(len(eids)), desc='batch Processing'):
    print(eids[i])
```