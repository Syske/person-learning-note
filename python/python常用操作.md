# python常用操作

#python

## 异常处理

### try

```python
try:
    # 需要捕获异常的代码
except Exception as re:
    # 发生异常时的操作
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

将对象序列化为`json`:

```python
data = ['syske', 'lei', 'yingying']
data_str = json.dumps(data)
```

#### list分割

```python
# 将list分割为200一组的小列表，类似java的Lists.partion(list, 200)
for i in range(0, len(eids), 200):
    # 分割后的list
    batch_data = eids[i:i + 200]
```