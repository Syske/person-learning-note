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