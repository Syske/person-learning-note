### 连接
```
mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
```

-   **mongodb://** 这是固定的格式，必须要指定。
    
-   **username:password@** 可选项，如果设置，在连接数据库服务器之后，驱动都会尝试登录这个数据库
    
-   **host1** 必须的指定至少一个host, host1 是这个URI唯一要填写的。它指定了要连接服务器的地址。如果要连接复制集，请指定多个主机地址。
    
-   **portX** 可选的指定端口，如果不填，默认为27017
    
-   **/database** 如果指定username:password@，连接并验证登录指定数据库。若不指定，默认打开 test 数据库。
    
-   **?options** 是连接选项。如果不使用/database，则前面需要加上/。所有连接选项都是键值对name=value，键值对之间通过&或;（分号）隔开


### 使用

#### 查看数据库

```
show dbs
```

#### 切换数据库

```
use dbNam
```

### 查看数据集合

```
show collections
```

### 切换数据集合

```
use collectionNam
```


## 查询操作

### and

```mongo
db.thirdOaSyncRecordPo.find({$and:[{"sync_detail._id":{$eq: "yh0310011"}},{"enterprise_id":NumberLong("1456280502230192192")}]})
```

数据结构如下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221213162746.png)

## 报错梳理

执行查询时提示没有权限，通常是由于配置了多个节点，我们连接到的节点没有权限，在shell脚本中建议链接主节点

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240401110839.png)