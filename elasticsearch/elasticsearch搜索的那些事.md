# elasticsearch搜索的那些事

### 前言

`elasticsearch`本身就是为搜索而生的组件，所以搜索才是它的重头戏。从今天我们就学习`es`的各种检索语法了，但是我大概看了下官方文档，发现他对于各种检索语法的解释比较少，虽然也有好多示例，但是都比较零散，很难让我们看清楚它的语法规则。因此，我们今天也不会有太多内容分享，但是我这边会花两天时间梳理相关规则，争取未来两天整理出它的语法规则。

下面我们就先来看一些简单的检索规则。

### elastsearch搜索

#### 轻量搜索

这个检索语法类似于我们传统数据库中不加条件的查询语句，他会查询`megacorp`索引下所有`employee`的数据，然会返回

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

  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210827081432.png)

  #### 根据关键字搜索

  相比于前面的那种查询全部，这种方式查询就比较灵活了，我们可以根据数据中的某个字段名进行查询，具体语法如下：

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

  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210827085515.png)

  查询不到结果时，返回结果如下：

  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210827085442.png)
  
  #### 查询表达式搜索
  
  `Elasticsearch `提供一个丰富灵活的查询语言叫做 *查询表达式* ， 它支持构建更加复杂和健壮的查询。
  
  *领域特定语言* （`DSL`）， 使用 `JSON `构造了一个请求。
  
  查询语法也基本上和我们前面的查询一致，唯一的区别是，表达式搜索的时候，需要传一个`json`的表达式：
  
  ```sh
  curl -X GET "localhost:9200/megacorp/employee/_search?pretty" -H 'Content-Type: application/json' -d'
  {
      "query" : {
          "match" : {
              "name" : "syske"
          }
      }
  }
  '
  ```
  
  返回结果：
  
  ```json
  {
    "took" : 50,
    "timed_out" : false,
    "_shards" : {
      "total" : 1,
      "successful" : 1,
      "skipped" : 0,
      "failed" : 0
    },
    "hits" : {
      "total" : {
        "value" : 2,
        "relation" : "eq"
      },
      "max_score" : 0.18232156,
      "hits" : [
        {
          "_index" : "megacorp",
          "_type" : "employee",
          "_id" : "2",
          "_score" : 0.18232156,
          "_source" : {
            "name" : "syske",
            "age" : 18,
            "about" : "I love to read book",
            "interests" : [
              "sports",
              "music"
            ]
          }
        },
        {
          "_index" : "megacorp",
          "_type" : "employee",
          "_id" : "1",
          "_score" : 0.18232156,
          "_source" : {
            "name" : "syske",
            "age" : 15,
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
  
  关于表达式的写法，我们下面继续研究：
  
  ```json
  curl -X GET "localhost:9200/megacorp/employee/_search?pretty" -H 'Content-Type: application/json' -d'
  {
      "query" : {
          "bool": {
              "must": {
                  "match" : {
                      "name" : "syske" 
                  }
              },
              "filter": {
                  "range" : {
                      "age" : { "gt" : 15 } 
                  }
              }
          }
      }
  }'
  ```
  
  表达式中的`filter`，其实就是对我们前面查出来的结果进行过滤。关于表达式的逻辑关系，我们先补充一点内容：
  
  - `EQ `就是 `EQUAL`等于 
  - `NE`就是 `NOT EQUAL`不等于 
  - `GT` 就是 `GREATER THAN`大于　 
  - `LT `就是` LESS THAN`小于 
  - `GE `就是 `GREATER THAN OR EQUAL `大于等于 
  - `LE `就是 `LESS THAN OR EQUAL` 小于等于
  
  上面表达式最终查出的结果如下：
  
  ```json
  {
    "took" : 18,
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
      "max_score" : 0.18232156,
      "hits" : [
        {
          "_index" : "megacorp",
          "_type" : "employee",
          "_id" : "2",
          "_score" : 0.18232156,
          "_source" : {
            "name" : "syske",
            "age" : 18,
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
  
  在我们的`megacorp`索引下，名字为`syske`的`employee`数据有两条，年龄分别为`18`和`15`，因为我们过滤条件为年龄大于`15`，所以查出的结果只有年龄为`18`的。
  
  **注意**：实际在测试的时候，发现`range`表达之只支持`gt`和`lt`，其他都不支持。

### 总结

`elasticsearch`因为有自己特定的*领域特定语言* （`DSL`），所以我们真正想要用好`es`，还是要学好`DSL`相关语法的，这也是我截止到目前都没有通过`java`去访问`es`的一个重要原因。学东西有时候是不能探快的，学好基础才是关键，只有学好了基础内容，后面上手才会更容易，毕竟`java`操作`es`也是建立在`es`的各种基础语法之上的。

