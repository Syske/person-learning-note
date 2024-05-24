# 函数/方法

### 什么是函数/方法
 
函数是组织好的，可重复使用的，用来实现单一，或相关联功能的代码段。

### 语法

```python
def 函数名（参数列表）:
    函数体
```

默认情况下，参数值和参数名称是按函数声明中定义的顺序匹配起来的。

```python
def hello() :  
    print("Hello World!")
```


![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240524160506.png)
简单的规则

- 函数代码块以 **def** 关键词开头，后接函数标识符名称和圆括号 **()**。
- 任何传入参数和自变量必须放在圆括号中间，圆括号之间可以用于定义参数。
- 函数的第一行语句可以选择性地使用文档字符串—用于存放函数说明。
- 函数内容以冒号 : 起始，并且缩进。
- **return \[表达式]** 结束函数，选择性地返回一个值给调用方，不带表达式的 return 相当于返回 None。

### 函数/方法调用

语法：

```python
方法名(参数1, 参数2)
```


### 进阶

#### 不按参数顺序传参

正常情况下，我们都需要按参数顺序传参，但是如果你不想按参数顺序传参，可以通过如下方式调用函数：

```python
test1(b= 3, a= 4)
```

这种用法也叫关键字参数

#### 必须参数和非必须参数

必须参数示例
```python
def test1(a, b):
    print(a + b)

test1(1, 2)
```

非必须参数示例(有默认值的参数)
```python
def test1(a, b=1):
    print(a + b)

test1(1)
```

**注意**：这里需要注意的是，非必须参数在函数定义时，要放在参数列表的最后面，否则会报错
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240524161605.png)

这个其实很好理解，如果不把非必须参数放在最后面，在不指定参数名的时候，函数是不确定你传的值是给谁的

#### 不定长参数

基本语法如下：

```python 
def functionname([formal_args,] *var_args_tuple ):
   "函数_文档字符串"
   function_suite
   return [expression]
```

加了星号 `*` 的参数会以元组`(tuple)`的形式导入，存放所有未命名的变量参数。

```python
#!/usr/bin/python3
  
# 可写函数说明
def printinfo( arg1, *vartuple ):
   "打印任何传入的参数"
   print ("输出: ")
   print (arg1)
   print (vartuple)
 
# 调用printinfo 函数
printinfo( 70, 60, 50 )
```
#### 可更改(mutable)与不可更改(immutable)对象

- **不可变类型：** 变量赋值 **a=5** 后再赋值 **a=10**，这里实际是新生成一个 `int` 值对象 `10`，再让 `a` 指向它，而 `5` 被丢弃，不是改变 `a` 的值，相当于新生成了 `a`。
    
- **可变类型：** 变量赋值 **la=\[1,2,3,4\]** 后再赋值 **la\[2\]=5** 则是将 `list` `la` 的第三个元素值更改，本身`la`没有动，只是其内部的一部分值被修改了。
    

python 函数的参数传递：

- **不可变类型：** 类似 `C++` 的值传递，如整数、字符串、元组。如 `fun(a)`，传递的只是 `a` 的值，没有影响 `a` 对象本身。如果在 `fun(a)` 内部修改 `a` 的值，则是新生成一个 `a` 的对象。
    
- **可变类型：** 类似 `C++` 的引用传递，如 列表，字典。如 `fun(la)`，则是将 `la` 真正的传过去，修改后 `fun` 外部的 `la` 也会受影响

在 `python` 中，`strings`, `tuples`, 和 `numbers` 是不可更改的对象，而 `list`,`dict` 等则是可以修改的对象。

#### 匿名函数

匿名函数也叫`lambda`表达式

##### 语法

`lambda` 函数的语法只包含一个语句，如下：

```
lambda [arg1 [,arg2,.....argn]]:expression
```

示例：

```python
x = lambda a : a + 10 
print(x(5))
```

#### 特殊的函数调用

```python
def test1(a):
    print("test1", a)
    

eval(f"test1({10})")
```

参考资料：[菜鸟教程](https://www.runoob.com/python3/python3-function.html)