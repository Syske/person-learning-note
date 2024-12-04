# elasticsearch专用术语及基本用法

### 前言

根据官方对`elasticsearch`的定位，我们可以说`elasticsearc`是一套面向文档（`json`）的解决方案。

### 专用术语

#### 索引

索引我们昨天已经说过了，它其实就相当于传统的关系型数据库，一个 *索引* 类似于传统关系数据库中的一个 *数据库* ，是一个存储关系型文档的地方。 *索引* (*`index`*) 的复数词为 *`indices`* 或 *`indexes`* 。

除此自外，索引还可以当作动词来使用。*索引一个文档* 就是存储一个文档到一个 *索引* （名词）中以便被检索和查询。这非常类似于 `SQL `语句中的 `INSERT` 关键词，除了文档已存在时，新文档会替换旧文档情况之外。

##### 倒排索引

关系型数据库通过增加一个 *索引* 比如一个 `B`树（`B-tree`）索引 到指定的列上，以便提升数据检索速度。`Elasticsearch `和 `Lucene `使用了一个叫做 *倒排索引* 的结构来达到相同的目的。

默认的，一个文档中的每一个属性都是 *被索引* 的（有一个倒排索引）和可搜索的。一个没有倒排索引的属性是不能被搜索到的。



### 基本用法

#### 新增数据（创建索引）

关于创建索引其实我们昨天已经演示过了，但是昨天是为了测试，所以今天我们还需要再次补充说明下。

首先创建所以的语法如下：

```sh
curl -X PUT "localhost:9200/megacorp/employee/1?pretty" -H 'Content-Type: application/json' -d'
{
    "name" :  "syske",
    "age" :        25,
    "about" :      "I love to read book",
    "interests": [ "sports", "music" ]
}'
```

这里我们简答介绍下上面的请求参数：

- `megacorp`：表示索引名称，也就相当于我们传统关系型数据库中的数据库，可以根据自己的需要指定
- `employee`：官方给出的说明是类型名称，但我觉得应该叫子索引更合理，就类似于传统数据库下面的数据表
- `1`：表示我们当前数据的`id`，也就是这条数据对应的唯一索引
- 请求体：下面的`json`表示我们的请求体

昨天我们说了，`es`本身只支持`GET`,  `PUT`,  `DELETE`,  `HEAD`，这里的`PUT`既可以表示新增，也可以表示更新，如果记录存在，则进行更新操作，否则进行新增操作。关于这一点我们昨天也已经演示过了，这里就不再赘述。



为了方便测试，我们后期的内容直接在`git bash`下执行`curl`命令了，`windows`下`cmd`体验太差：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210826085728.png)

从上面返回结果来看，当文档（`json`数据）不存在的时候，它返回的`result`是`created`，但如果文档已经存在，它返回的结果是`updated`:

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210826085916.png)

#### 数据检索

数据检索也很简单，直接发送`GET`请求即可：

```sh
curl -X GET "localhost:9200/megacorp/employee/1?pretty"
```

返回结果如下：

```json
{
  "_index" : "megacorp",
  "_type" : "employee",
  "_id" : "1",
  "_version" : 1,
  "_seq_no" : 0,
  "_primary_term" : 1,
  "found" : true,
  "_source" : {
    "name" : "syske",
    "age" : 25,
    "about" : "I love to read book",
    "interests" : [
      "sports",
      "music"
    ]
  }
}
```

我们先解释下返回结果：

- `_index`：索引
- `_type`：数据类型
- `_id`：数据`id`，这个是我们新增数据的时候指定的
- `_version`：数据版本，新增之后默认版本号为`1`，每更新一次，数据库版本加一
- `_seq_no`：序号，主要用来记录新增、更新和删除的操作顺序，对数据而言，通过这个字段可以确定数据创建顺序（我自己觉得可以）
- `_primary_term`：和集群相关的一个数据，应该主要是为了标记节点号，根据资料显示，这个数据在重启后会发生变化。这个参数后面再研究吧。
- `found`：表示是否有搜索到数据，如果未搜索到结果为`false`
- `_source`：查询到的结果

这里说下请求地址后面这个参数`pretty`，这个参数的意思是对请求参数和返回结果进行美化，如果没有这个参数，我们看到的数据就会是一坨，不方便查看：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210826131422.png)

加了这个参数，返回结果就好看多了：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210826131505.png)

#### 数据更新

更新操作和新增是一模一样的，这里我们就不做过多说明，唯一的区别是，如果返回结果`result`为`updated`，则表示数据更新成功：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210826133705.png)



#### 数据删除

删除数据和查询数据很像，只需要把`GET`替换成`DELETE`即可：

```sh
 curl -X DELETE "localhost:9200/megacorp/employee/4?pretty" -H 'Content-Type: application/json'
```

返回结果`result`为`deleted`表示删除成功。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210826133845.png)

如果数据不存在，则返回结果为`not_found`:

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210826134215.png)

### 总结

由于时间的关系，今天暂时先分享这么多，更多内容我们明天再来分享。想了解更多知识点的小伙伴可以自己看官方文档：

```
https://www.elastic.co/guide/cn/elasticsearch/guide/current/index.html
```

