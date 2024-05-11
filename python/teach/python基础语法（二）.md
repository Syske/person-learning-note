
### 基本数据类型
#### 字符串

字符串是 Python 中最常用的数据类型。我们可以使用引号( ' 或 " )来创建字符串。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240510205640.png)

定义一个字符串：

```python
name = 'python'
print(name)
```

##### len()

这里我们先分享一个特别常用的方法`len()`，这个方法用的特别广泛，用于获取字符串长度或者集合的大小，具体用法如下：

```python
name = 'python'
print(len(name))
```

##### 访问字符串中的元素

```python
name = 'python'
# | p | y | t | h | o | n |
# | 0 | 1 | 2 | 3 | 4 | 5 |
# 打印结果：p
print(name[0])
# 结果：y
print(name[1])
```

截取某段字符串

```python
name = 'python'
# 从0开始，截取到下标为3（不包括3）的字符串，结果：pyt
print(name[0:3])
# 如果不指定结束则默认到结束，结果：python
print(name[0:]) # 等同 print(name[:])
# 还可以是负数，表示从尾部开截取（倒着），结果：pyt
print(name[0:-3]) # 等同于 print(name[:-3])
# 从尾部开始截取，等同于舍弃末尾三个字符，结果：hon
print(name[-3:])
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240510205706.png)

**包前不包后**：包括开始下标的字符，不包括结束下标的字符

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240511171303.png)

更多方法，参考文档：[菜鸟驿站](https://www.runoob.com/python3/python3-string.html)
#### 数字

包括整数（正/负数）、小数（浮点数）、复数
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240510200825.png)

```python
x = 10
y = 1.66
z = -134
```

#### 运算

##### 加

```python
x = 10
y = 1.66
z = 110

t = x + x + y
# 结果 21.66
print(t)

u = x + z
# 结果 120
print(u)
```

##### 减

```python
a = 16
b = 23
c = a - b
# 结果 -7
print(c)
```

##### 乘

```python
a = 10
b = 23
c = a * b
# 结果 230
print(c)
```


##### 其他运算

- 取余
	```python
	a = 12
	b = 10
	c = 12 %% 10
	# 结果 2
	print(c)
	
	```
- 幂运算
	```python
	a = 2
	b = 3 
	c = 2 ** 3
	# 结果 8
	print(c)
	```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240510201555.png)
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240510201640.png)
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240510201702.png)

更多内容，参考如下文档：[菜鸟教程](https://www.runoob.com/python3/python3-number.html)

#### 数据类型转换

这里先说一个方法（函数），通过这个函数我们能够确定某个数据的具体类型：

```python
s = '123123'
s_type = type(s)
# 打印结果：<class 'str'>
print(s_type)

a = 10
# 结果：<class 'int'>
print(type(a))

a = 10。0
# 结果：<class 'float'>
print(type(a))

 a = 10/77
 # 结果：<class 'float'>
 print(type(a))
```

- 数字类型转换
	![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240510201846.png)
- 字符串转数字：
	```python
	 s = "1232"
	 s1 = int(s)
	 print(s1)	

	s2 = '1.111'
	 # int(s2)会报错，小数类型不能转成整数，否则会报错：ValueError: invalid literal for int() with base 10: '1.111'
	 print(float(s2))	
	
	```

### 布尔类型

逻辑类似，只有两种值：`True`/`Flase`

布尔类型只能进行逻辑运算：

- `not`：非
- `and`：且
- `or`：或

### 容器

#### list

有序列表，类似数组

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240510205551.png)
定义一个`list`:

```python
list1 = [1, 2, 5, 9, 0]
# 结果：[1, 2, 5, 9, 0]
print(list1)
```

##### 访问元素

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240510205612.png)

```python
item1 = list1[0]
# 结果：1
print(item1)

# 结果：5
print(list1[2])
```

##### 截取

这里和字符串的逻辑是一样的

```python
list2 =  list1[0:3]
# 结果：[1, 2, 5]
print(list2)
# 结果：[1, 2, 5]
print( list1[:3])
# 这里可以理解为舍弃后面三个元素，结果：[1, 2]
print(list1[:-3])
```

参考文档：[菜鸟教程](https://www.runoob.com/python3/python3-list.html)

#### 元组

`Python` 的元组与列表类似，不同之处在于元组的元素不能修改。

- 元组使用小括号 ( )，列表使用方括号 \[ \]。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240510205507.png)

```python
tup1 = ('Google', 'Runoob', 1997, 2000)
print(tup1)
```

元组中只包含一个元素时，需要在元素后面添加逗号 , ，否则括号会被当作运算符使用：

```python
tup1 = (50)
# 结果：<class 'int'>
print(type(tup1))     # 不加逗号，类型为整型


tup1 = (50,)
# 结果：<class 'tuple'>
print(type(tup1))     # 加上逗号，类型为元组

```
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240510205443.png)

更多内容，参考文档：[菜鸟教程](https://www.runoob.com/python3/python3-tuple.html)

#### set(集合)

集合（set）是一个无序的不重复元素序列。

```python
set1 = {1, 2, 3, 4}            # 直接使用大括号创建集合
set2 = set([4, 5, 6, 7])      # 使用 set() 函数从列表创建集合
```

##### 添加元素

```python
set1.add( x )
# 可以添加元素，且参数可以是列表，元组，字典等
s.update( x )
```

更多内容，参考文档：[菜鸟教程](https://www.runoob.com/python3/python3-set.html)
#### 字典

```python
d = {key1 : value1, key2 : value2, key3 : value3 }
```

访问字典元素：

```python
d = {"name" : "syske", "age" : 18, "sex" : "男" }
# 结果：syske
print(d["name"])
```

更多内容，参考文档：[菜鸟教程](https://www.runoob.com/python3/python3-dictionary.html)