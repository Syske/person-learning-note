## 常用操作

#### 表结构导出

```
cqlsh 127.0.0.1  -e 'desc keyspace  enterprise'  > enterprise.cql
```

#### 表结构导入

```
cqlsh 127.0.0.1 -f enterprise.cql
```

