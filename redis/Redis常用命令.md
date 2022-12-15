# Redis常用命令

### set常用操作

#### 元素是否存在

判断 member 元素是否是集合 key 的成员

```
SISMEMBER key member
```

#### 获取集合的成员数

```
SCARD key
```

#### 获取所有成员

```
SMEMBERS key
```

#### 删除元素

移除集合中一个或多个成员

```
SREM key member1 [member2]
```

#### 添加元素

向集合添加一个或多个成员

```
SADD key member1 [member2]
```

### Hash常用操作

#### 删除

删除一个或多个哈希表字段

```
HDEL key field1 [field2]
```

#### 元素是否存在

查看哈希表 key 中，指定的字段是否存在。

```sh
HEXISTS key field
```

#### 获取元素

获取存储在哈希表中指定字段的值。

```sh
HGET key field
```

获取所有元素

```sh
HGETALL key
```

### list常用操作

获取指定范围资源：

```sh
lrange key 0 -1
```

删除资源

```
LREM key count value
```

### 其他操作

#### 查询key剩余过期时间

```sh
ttl key
```