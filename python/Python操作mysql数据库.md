## 安装mysql驱动

### mysql-connector

安装命令

```shell
python -m pip install mysql-connector
```

测试安装是否成功：

```python
import mysql.connector
```

### pymysql

安装命令

```shell
pip3 install PyMySQLpip3 install PyMySQL
```

测试是否安装成功

```python
import pymysql
```



## 连接数据库

### mysql-connrctor

```python
import mysql.connector
 
mydb = mysql.connector.connect(
  host="localhost",       # 数据库主机地址
  user="yourusername",    # 数据库用户名
  passwd="yourpassword"   # 数据库密码
)
 
print(mydb)
```

### pyMysql

```python
#!/usr/bin/python3
 
import pymysql
 
# 打开数据库连接
db = pymysql.connect("localhost","testuser","test123","TESTDB" )
 
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
 
# 使用 execute()  方法执行 SQL 查询 
cursor.execute("SELECT VERSION()")
 
# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()
 
print ("Database version : %s " % data)
 
# 关闭数据库连接
db.close()
```

