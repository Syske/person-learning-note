# elasticsearch搜索的那些事

### 前言



### elastsearch搜索

#### 轻量搜索

```sh
curl -X GET "localhost:9200/megacorp/employee/_search?pretty"
```

返回结果如下：

```json
{
  "took" : 78,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "1",
        "_score" : 1.0,
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
    ]
  }
}

```

下面我们简单解释下搜索结果：

- `took`：这个应该搜索耗时时间，单位一般应该是毫秒，在测试过程中我发现每次的返回结果都会都差异

- `timed_out`：请求是否超时

- `_shards`：分片，应该和存储有关，类似于传统数据存储中的分库分表，应该就是存储分割的单位。这里返回的是我们分片的汇总信息

- `_shards.total`：总分片数

- `_shards.successful`：这个应该表示的是搜索到结果的分片数

- `_shards.skipped`：这个应该表示未搜索到数据的分片数

- `_shards.failed`：那这个就表示搜索失败的分片数了

- `hits`：这应该就是我们搜索到的结果

- `hits.total`：主要存放返回结果汇总信息

- `hits.total.value`：查询到的结果数量

- `hits.total.relation`：查询结果的关系，`eq`表示相等（应该是`equals`的简写），那`ne`应该就表示不相等，目前没找到官方给的说明，网上也没有比较靠谱的解释。

- `hits.max_score`：返回结果中`score`的最大值，这个`score`应该表示匹配度，因为没有文档，所以暂时只能推测

- `hits.hits`：这个就是最终的搜索结果了，所有的匹配结果都会在这里面显示。这底下的数据也和我们`get`返回的结果很类似。

- `hits.hits._index`：索引

- `hits.hits._type`：数据类型

- `hits.hits._id`：数据id

- `hits.hits._score`：这个就是我们刚说的匹配度

- `hits.hits._source`：最终的搜索结果

  ![](https://gitee.com/sysker/picBed/raw/master/20210827081432.png)

  #### 根据关键字搜索

  这种方式查询就比较灵活了，我们可以根据数据中的某个字段名进行查询，具体语法如下：

  ```
  索引/数据类型/_search?q=字段名:字段值
  ```

  下面是搜索样例：

  ```sh
  curl -X GET "localhost:9200/megacorp/employee/_search?q=name:syske&pretty"
  ```

  返回结果如下：

  ```json
  {
    "took" : 6,
    "timed_out" : false,
    "_shards" : {
      "total" : 1,
      "successful" : 1,
      "skipped" : 0,
      "failed" : 0
    },
    "hits" : {
      "total" : {
        "value" : 1,
        "relation" : "eq"
      },
      "max_score" : 0.2876821,
      "hits" : [
        {
          "_index" : "megacorp",
          "_type" : "employee",
          "_id" : "1",
          "_score" : 0.2876821,
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
      ]
    }
  }
  ```

  具体返回结果如下：

  ![](https://gitee.com/sysker/picBed/raw/master/20210827085515.png)

  查询不到结果时，返回结果如下：

  ![](https://gitee.com/sysker/picBed/raw/master/20210827085442.png)

### 总结