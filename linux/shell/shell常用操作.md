# shell常用操作

#### if判断

```shell
if [command];then
  符合条件执行的语句
elif [];then
  符合条件执行的语句
else
   符合条件执行的语句
fi
```

示例：

```sh
# 判断eid是否为空
## 第一种写法
 eid=$1
 if  test -z "$eid" ;then
   echo "execute error: eid can not be null"
   exit;
 fi
## 第二种写法
#!/bin/sh
eid=$1
if [ ! $eid ]; then
  echo "execute error: eid can not be null"
  exit;
fi
```

#### 判断是否相等

```sh
# 假设 eid 是通过某种方式设置的
eid="hls"  # 示例赋值

# 使用 [[ ]] 进行判断
if [[ "$eid" == "hls" ]]; then
    echo "eid 等于 hls"
else
    echo "eid 不等于 hls"
fi

# 单括号写法
# 判断 eid 是否等于 hls
if [ "$eid" = "hls" ]; then
    echo "eid 等于 hls"
else
    echo "eid 不等于 hls"
fi
```

#### 常用逻辑关系

##### 且

第一种方式`and`：`-a`

```shell
if [c1 -a c2]; then
...
fi
```

第二种方式：`&&`

```shell
if [c1] && [c2]; then
...
fi
```

##### 或

第一种方式`or`：`-o`

```shell
if [c1 -o c2]; then
...
fi
```

第二种方式：`||`

```shell
if [c1] || [c2]; then
...
fi
```
