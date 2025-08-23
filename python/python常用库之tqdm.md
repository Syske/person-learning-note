#python #进度条
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
<<<<<<< HEAD
=======

# 使用range生成批次的起始索引
for start_idx in tqdm(
	range(0, len(data), batch_size),
	desc=desc,
	unit="batch",
	total=(len(data) + batch_size - 1) // batch_size  # 自动计算总批次数
):
	end_idx = start_idx + batch_size
	batch = data[start_idx:end_idx]
	# 在这里执行你的批处理逻辑
	process_batch(batch)

```


### 其他示例

```python
for i in trange(0, len(enterprises), 200):
	batch_data = enterprises[i:i + 200]
>>>>>>> 2b5c9fde2cfcfae33a64f4822874780e154c7961
```