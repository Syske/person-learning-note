#redis 

# Redis数据结构
## keys
-	keys [pattern]	– 匹配当前实例中的key.

-	keys *  -查询所有
-	keys user_* 	-查询key前缀为user_的所有key 
-	expire [key] [seconds]	– 设置key的过期时间
-	expire user_session_1 300 	-设置user_session_1的过期时间为300秒
-	ttl [key] 	– 获取key的过期时间
-	ttl user_session_1	-获取user_session的过期时间
-	del [key] 	-删除key

## 字符串(string)

-在工作中,字符串可以用来存放用户的json信息
- 字符串结构比较比较单一,在应用中,需要在Key上的组装规划合理.[ user_invit_count_20180805_1 表示2018年8月5号 用户id为1的访客数量]
[当用户信息被修改时,需要重新设置用户信息的json].
[配合expire可以完成session的模拟.]
[使用incr 完成记数相关的应用场景]
### 	数据类型介绍
- - 存储字符串类型的值,一般也可以做计数器使用
- -	单个String最多能存储512M

### 	语法介绍

-	SET [KEY] [VALUE] –新增或修改key的值
-	GET [KEY] – 获取key的值
-	INCR [KEY] – 将key中存储的value值做+1操作(仅数字)
-	INCRBY [KEY] [INCREMENT] – 将key中存储的value加上指定的增量值(increment) (仅数字)
-	DECR [KEY] – 将key中存储的value值做-1操作(仅数字)
-	DECRBY [KEY] [INCREMENT] – 将key中存储的value减去指定的增量值(increment) (仅数字)

## Hash

- Hash一般用来保存对象,保存对象的方式有两种.
-	将对象使用一个个的KEY去存储. key为具体对象的id,value为对象的属性值
- -	hset user_info_1 对象属性名 对象属性值
- - 可以精准的修改每一个对象的属性和获取.
- -	将多个对象保存至一个hash,hash中的field和value分别保存对象唯一ID和对象json字符串
- -	hset user_info_001 对象id 对象json字符串
- -	当对象的属性发生变化时,json数据需要重新更新.

### 数据类型介绍

-	一个String类型键值对映射表,一般用来存储对象
-	每个 hash 最多可以存储 232 - 1 键值对（40多亿）。

### 语法介绍

-	HSET [KEY] [FIELD] [VALUE] –将哈希表 key中的字段field的值设置为value
-	HGET [KEY] [FIELD] – 获取key 中 field的值
-	HMSET [KEY] [FIELD] [VALUE] [FIELD1] [VALUE1] – 同时将多个field-value设置到哈希表 key 中
-	HMGET [KEY] [FIELD] [FIELD1] – 获取所有给定字段的值
-	HGETALL [KEY] – 获取哈希表中所有的字段和值
-	HKEYS [KEY] – 获取哈希表中所有的字段
-	HEXISTS [KEY] [FIELD] – 查看哈希表中指定key中指定的字段是否存在
-	HDEL [KEY] [FIELD] – 删除哈希表中指定key中指定的字段

## List
-	List一般用来保存不常变动且没有查询条件的数据列表和消息队列奖池等等数据
-	不常变动的数据列表
-	使用lrange key 0 -1取列表所有的内容. 同时可以将开始和结束索引设计为分页
-	消息队列/奖池
-	rpop或lpop来做移除返回.

### 列表(List)

### 数据类型介绍
-	一个字符串列表,可从头/尾添加元素.一般用来存储经常访问的数据模型的ID列表/消息队列/红包奖池等等
-	每个列表最多可以存储232 - 1 个元素(40多亿)

### 语法介绍
- 	LPUSH [KEY] [VALUE] [VALUE1] – 将一个或多个值插入到列表头部
-	RPUSH [KEY] [VALUE] [VALUE1] – 将一个或多个值插入到列表尾部
-	LPOP [KEY] – 移除并获取列表的第一个元素
-	RPOP [KEY] – 移除并获取列表的最后一个元素
-	LINDEX [KEY] [INDEX] – 通过索引获取列表中的元素
-	LSET [KEY] [INDEX] [VALUE] – 通过索引设置列表元素的值
-	LRANGE [KEY] [START] [STOP] – 获取列表指定范围内的元素

## Set
- set一般用来做关系处理,或其他需要处理交并差集.
###	数据类型介绍
-	一个无序集合。集合成员是唯一的。可进行交集并集差集运算,一般用作关系处理,如:好友关系等
-	每个集合最多可以存储232 - 1 个元素(40多亿)
###	语法介绍
-	SADD [KEY] [MEMBER] [MEMBER1] – 向集合添加一个或多个成员
-	SMEMBERS [KEY]  - 获取集合中所有的成员
-	SPOP [KEY] – 删除并返回集合中的一个随机元素
-	SDIFF [KEY][KEY1] – 获取给定集合的差集 
-	SDIFFSTORE [DESTINATION] [KEY] [KEY1] – 获取指定的集合的差集并存储至destination指定的key中
•	SINTER [KEY][KEY1]  - 获取给定集合中的交集
•	SINTERSTORE [DESTINATION] [KEY] [KEY1]  - 获取指定集合的交集并存储至destination指定的key中
•	SUNION [KEY][KEY1] – 获取给定集合中的并集
•	SUNIONSTORE [DESTINATION] [KEY] [KEY1] – 获取指定集合中的并集并存储至destination指定的key中
## Sorted set
有序集合一般用来处理需要进行排序的列表,且列表的顺序会根据一定的权重值发生改变.
	初始化排行榜时,所有权重值默认设置为0
	ZADD top 0 1 0 2 0 3 – 向排行榜中插入1/2/3号用户,排序权重值分别为0
	当对应的列表需要调整权重时,使用zincrby来对对应的列表元素增加权重值
	zincrby top 10 2 – 向排行榜排行榜中 2号用户增加10个权重值

###	数据类型介绍
•	有序集合和集合一样也是string类型元素的集合,且不允许重复的成员。不同的是每个元素都会关联一个double类型的分数。可以通过分数进行排序。一般在排行榜、热度排序等业务场景中使用
•	每个集合最多可以存储232 - 1 个元素(40多亿)
###	语法介绍
•	ZADD [KEY] [SCORE] [MEMBER] [SCORE1] [MEMBER1] – 向集合添加一个或多个成员及分数,或者更新成员分数
•	ZINCRBY [KEY] [INCREMENT] [MEMBER] –有序集合中对指定成员增加increment值
•	ZRANGE [KEY] [START] [STOP] – 返回有序集合中指定索引区间的成员
•	ZRANGEBYSCORE [KEY] [MIN] [MAX] – 返回指定分数区间的成员升序排列
•	ZREVRANGE [KEY] [START] [STOP] – 返回指定索引区间的成员,降序排列
•	ZREVRANGEBYSCORE [KEY] [MAX] [MIN] – 返回指定分数区间的成员,降序排列
•	ZREVRANK [KEY] [MEMBER]  – 返回指定成员的排名,从0开始
•	ZSCORE [KEY] [MEMBER] – 返回指定成员的分数
## redis.conf配置文件详解
	bind 127.0.0.1
	绑定ip,只允许哪些IP访问本实例. 多个用空格隔开
	port 6379
	redis配置文件中默认的端口号
	loglevel notice
	日志级别,默认给的就是生产环境所需要使用的级别
	debug, verbose, notice, warning
	logfile ""
	日志文件目录.当声明了目录之后就不会在控制台显示.
	window中的路径 : logfile "D:/redis.log"
	saving
	当redis中的key发生改变时load到硬盘上的策略
	save 900 1  - 900秒至少有一个key发生改变
	save 300 10  - 300秒至少有10个key
	save 60 10000 – 60秒至少有10000个key
	dbfilename dump.rdb
	数据文件的名称. 当我们在同一个机器上启动多个redis实例时,更改dump的名字
	requirepass
	密码,redis模式是将密码注释的. 设置了密码之后,连接时需要指定参数-a 密码来连接
	maxclients
	当前redis实例的最大连接数量
	maxmemory
	设置当前redis实例的最大内存



## 过期策略

### 过期删除策略
	在redis中,开发者可以使用expire来对key进行有效期设定,redis的过期删除策略是每隔100ms对key进行随机扫描并删除,且在每次获取key时,redis也会对key的有效期进行检查.保证每一次拿到手的key是有效的.
	当然,除了上述的定期删除策略和懒惰删除策略以外,Redis还提供maxmemory-policy内存不足的过期策略配置.
•	Noeviction
•	allkeys-lru
•	volatile-lru
•	allkeys-random
•	volatile-random
•	volatile-ttl
### 内存不足删除策略
①	noenviction：禁止淘汰数据,写入直接报错
②	allkeys-lru：从数据集中挑选最近最少使用的数据淘汰
③	volatile-lru：从已设置过期时间的数据集中挑选最近最少使用的数据淘汰。
④	allkeys-random：从数据集中任意选择数据淘汰
⑤	volatile-random：从已设置过期时间的数据集中任意选择数据淘汰
⑥	volatile-ttl：从已设置过期时间的数据集中挑选将要过期的数据淘汰
