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

