## 常用操作

#### 表结构导出

```
cqlsh 127.0.0.1  -e 'desc keyspace  enterprise'  > enterprise.cql
```

#### 表结构导入

```
cqlsh 127.0.0.1 -f enterprise.cql
```



#### docker配置

##### 拉取镜像

```sh
docker pull cassandra
```

##### 启动

```sh
docker run --name some-cassandra --network some-network -v /my/own/datadir:/var/lib/cassandra -d cassandra:tag
# 例如
docker run -d -p 9042:9042 -v /my/own/datadir:/var/lib/cassandra cassandra
```

