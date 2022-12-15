# python常用操作

## 文件夹

### 创建文件夹

```python
import os
os.mkdir('folder')
```

### 获取当前位置

```python
import os
os.getcwd()
```

### 改变默认目录

```python
import os
os.chdir('../')
```

### 获取目录列表

```python
import os
os.listdir('./')
```

### 删除文件夹

```python
import os
os.rmdir('folder')
```


## 异常处理

### try

```python
try:
    # 需要捕获异常的代码
except Exception as re:
    # 发生异常时的操作
    print(re)
```

## 数据库增删改查

### 获取数据库连接

```python
import pymysql

def get_conn():
    conn = pymysql.connect(
            host= '192.168.0.100',  # mysql的主机ip
            port=3306,  # 端口
            user='root',  # 用户名
            passwd='root',  # 数据库密码
            db='user',
            charset='utf8',  # 使用字符集
    )
    return conn
```

### 查询

查询全部

```python
# 获取数据库连接
conn = get_conn()
# 获取数据库游标
cur=conn.cursor()

# 查询全部
# sql表示查询语句
def query_all(cur, sql, args):
    cur.execute(sql, args)
    return cur.fetchall()
```

查询单个，参数同上

```python
def query_one(cur, sql, args):
    cur.execute(sql, args)
    return cur.fetchone()
```


### 更新数据

更新数据，参数同上

```python

def update_data(cur, conn,sql, args):
  try:
      cur.execute(sql, args)
      conn.commit()
  except Exception as re:
      conn.rollback()
      print(re)
```

### 删除数据

参数同上

```python
def delete_data(cursor, conn, sql, args):
    try:
        cursor.execute(sql, args)
        conn.commit()
    except Exception as re:
        conn.rollback()
        print(re)
```

## csv操作

### 数据库导出csv

```python
import codecs,csv,pymysql

# 其中query_all方法参照操作数据库的查询

def read_mysql_to_csv(sql, filename):
    with codecs.open(filename=filename, mode='w', encoding='utf-8') as f:
        write = csv.writer(f, dialect='excel')
        conn = get_conn()
        cur = conn.cursor()
        results = query_all(cur=cur, sql=sql, args=None)
        for result in results:
            write.writerow(result)
```

## 操作excel

### csv转excel

```python
import os, csv, sys, openpyxl
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

def csv2excel(csv_filename, excel_filename):
  # new work book
  wb2 = Workbook()
  # active sheet
  ws2 = wb2.active
  #Copy in csv
  f = open(csv_filename, encoding='utf-8',errors='ignore')
  reader = csv.reader(f)
  for row_index, row in enumerate(reader):
    for column_index, cell in enumerate(row):
      column_letter = get_column_letter((column_index + 1))
      ws2.cell(row_index + 1, (column_index + 1)).value = cell
    print('line:' + str(row_index+1))

  wb2.save(filename = excel_filename)
  print("new Cashflow created")
```

## 其他常用

### 传参

```python
import sys

# args script
args = sys.argv[1:]
csv_filename = args[0] + ".csv"
out_filename = args[0] + ".xlsx"
```

`sys.argv`是用来存在传参参数的，第一个参数表示他自己的文件名，我们通过脚本传入的参数是从第二个开始的，所以我们需要截取下：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221125193411.png)

### 发送websocket请求

```python
from websocket import create_connection

ws = create_connection("ws://192.168.43.41:80")
print("Sending 'Hello, World'...")
ws.send("syske master\n ha ha ha ha......hello world!!!")
print("Sent")
print("Receiving...")
result = ws.recv()
print("Received '%s'" % result)
ws.close()
```

### json

读取文件，并将文件中的内容转为`json`

```python
f = open("./json.txt", encoding='utf-8',errors='ignore')
  content = f.read()
  text = json.loads(content)
```

