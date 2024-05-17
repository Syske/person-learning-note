
### 条件控制

条件语句是通过一条或多条语句的执行结果（True 或者 False）来决定执行的代码块。

可以通过下图来简单了解条件语句的执行过程:

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240511164838.png)

#### if

```python
#!/usr/bin/python3
 
var1 = 100
if var1:
    print ("1 - if 表达式条件为 true")
    print (var1)
 
var2 = 0
if var2:
    print ("2 - if 表达式条件为 true")
    print (var2)
print ("Good bye!")
```


#### match...case

```python
 match status:  
        case 400:  
            print("Bad request")
        case 404:  
            print("Not found")
        case 418:  
            print("I'm a teapot") 
        case _:  
            print("Something's wrong with the internet")
```
`case _:` 类似于 `C` 和 `Java` 中的 `default:`，当其他 `case` 都无法匹配时，匹配这条，保证永远会匹配成功

### 循环语句

`Python` 中的循环语句有 `for` 和 `while`。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240511165738.png)

#### while 循环

```python
while 判断条件(condition)：
    执行语句(statements)……
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240511165830.png)

##### while 循环使用 else 语句

如果 while 后面的条件语句为 false 时，则执行 else 的语句块。

```python
while <expr>:
    <statement(s)>
else:
    <additional_statement(s)>
```

实例：
```python
#!/usr/bin/python3
 
count = 0
while count < 5:
   print (count, " 小于 5")
   count = count + 1
else:
   print (count, " 大于或等于 5")
```


#### for 语句

`Python for` 循环可以遍历任何可迭代对象，如一个列表或者一个字符串。

```python
for <variable> in <sequence>:
    <statements>
else:
    <statements>
```

示例代码：
```python
lists = [1, 3, 9,8, 4]
for i in lists:
    print(i)
```


##### for...else

```python
for item in iterable:
    # 循环主体
else:
    # 循环结束后执行的代码
```


#### 关键词

**break** 语句可以跳出 `for` 和 `while` 的循环体。如果你从 `for` 或 `while` 循环中终止，任何对应的循环 `else` 块将不执行。

**continue** 语句被用来告诉 `Python` 跳过当前循环块中的剩余语句，然后继续进行下一轮循环。
**range() 函数** 如果你需要遍历数字序列，可以使用内置 range() 函数。它会生成数列

```python
>>>for i in range(5):
...     print(i)
...
0
1
2
3
4
```


### 迭代器
迭代是 Python 最强大的功能之一，是访问集合元素的一种方式。

迭代器是一个可以记住遍历的位置的对象。

迭代器对象从集合的第一个元素开始访问，直到所有的元素被访问完结束。迭代器只能往前不会后退。

迭代器有两个基本的方法：`iter()` 和 `next()`。
```python
list=[1,2,3,4]
it = iter(list)    # 创建迭代器对象
# 结果：1
print (next(it))   # 输出迭代器的下一个元素
# 结果： 2
print (next(it))
```