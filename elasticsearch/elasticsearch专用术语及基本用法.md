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

#### 创建索引

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

为了方便测试，我们后期的内容直接在`git bash`下执行`curl`命令了，`windows`下`cmd`体验太差：

![](https://gitee.com/sysker/picBed/raw/master/20210826085728.png)

从上面返回结果来看，当文档（`json`数据）不存在的时候，它返回的`result`是`created`，但如果文档已经存在，它返回的结果是`updated`:

![](https://gitee.com/sysker/picBed/raw/master/20210826085916.png)



### 总结

