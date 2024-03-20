# elasticsearch搜索语法梳理

### 前言

`elasticsearch`的核心在搜索，搜索的核心在搜索语法，所以今天我们来梳理下`elasticsearch`的一些搜索语法，今天主要探讨搜索，主要包括两方面的内容，一方面是普通的`query`，也就是数据的检索，另一方面就是内容的聚合，也就是传统`sql`中的分组。

好了，下面我们就来看下这两种搜索查询的具体操作吧。

### 搜索语法

#### 全文搜索

全文搜索的规则是会匹配凡是包括我们检索内容的任一单词，都会将结果予以展示，它并不关系单词顺序。对于下面我们的搜索表达式，它会搜索`about`中包括`go`和`reading`的所有内容。

搜索语法：

```sh
curl -X GET "localhost:9200/megacorp/employee/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query" : {
        "match" : {
            "about" : "go reading"
        }
    }
}
'
```

返回结果：

```json
{
  "took" : 220,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 7,
      "relation" : "eq"
    },
    "max_score" : 0.9161128,
    "hits" : [
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "1",
        "_score" : 0.9161128,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 15,
          "about" : "I love to go reading",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "6",
        "_score" : 0.9161128,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to reading go",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "7",
        "_score" : 0.8500352,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to reading and go",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "8",
        "_score" : 0.8500352,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to go and reading",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "5",
        "_score" : 0.6706225,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to reading",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "2",
        "_score" : 0.2761543,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to climbing go rock",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "3",
        "_score" : 0.2761543,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to go rock climbing",
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

从结果中，我们可以看到，`go reading`和`reading go`这样的内容都被匹配到了，同时他们的匹配度都是相同的，当然他们也是匹配度最高的。而且检索内容还匹配到了包含`go`和`reading`的内容，但是包含`reading`匹配项的匹配度比包含`go`匹配项的匹配度要高。

目前还不清楚它这个匹配度是如何计算的，现在只要知道`_score`越高，表示匹配度越高就行了。



#### 短语搜索

相比于全文搜索，短语搜索属于更精确的搜索。我们前面刚说过，全文搜索会将内容拆分之后进行搜索，属于更模糊的搜索，但是短语搜索必须匹配到完整的短语才算。所以对于下面的检索语句，它只会匹配包含`go reading`的内容：

```
curl -X GET "localhost:9200/megacorp/employee/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query" : {
        "match_phrase" : {
            "about" : "go reading"
        }
    }
}
'
```

返回结果：

```json
{
  "took" : 5,
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
    "max_score" : 1.1097687,
    "hits" : [
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "1",
        "_score" : 1.1097687,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 15,
          "about" : "I love to go reading",
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

从结果我们可以看出来，最终结果只匹配到了包括`go reading`这个短语的内容，包含其中任一单词的并没有被匹配到。这也说明，短语匹配必须匹配完整短语

#### 高亮搜索

高亮搜索简单来说，就是将我们检索到的内容进行高亮处理，默认情况下，会将检索到的内容加上`em`标签：

```sh
curl -X GET "localhost:9200/megacorp/employee/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query" : {
        "match_phrase" : {
            "about" : "rock climbing"
        }
    },
    "highlight": {
        "fields" : {
            "about" : {}
        }
    }
}
'
```

返回结果：

```json
{
  "took" : 116,
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
    "max_score" : 1.8434994,
    "hits" : [
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "4",
        "_score" : 1.8434994,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to rock climbing",
          "interests" : [
            "sports",
            "music"
          ]
        },
        "highlight" : {
          "about" : [
            "I love to <em>rock</em> <em>climbing</em>"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "3",
        "_score" : 1.7099125,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to go rock climbing",
          "interests" : [
            "sports",
            "music"
          ]
        },
        "highlight" : {
          "about" : [
            "I love to go <em>rock</em> <em>climbing</em>"
          ]
        }
      }
    ]
  }
}
```

当然，高亮样式是支持自定义的：

```sh
curl -X GET "localhost:9200/megacorp/employee/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query" : {
        "match_phrase" : {
            "about" : "rock climbing"
        }
    },
    "highlight": {
         "pre_tags" : ["<p style=\"color:red\">"],
        "post_tags" : ["</p>"],
        "fields" : {
            "about" : {}
        }
    }
}
'
```

返回结果：

```json
{
 ...
  "hits" : {
    ...
    "hits" : [
      {
       ...
        },
        "highlight" : {
          "about" : [
            "I love to <p style=\"color:red\">rock</p> <p style=\"color:red\">climbing</p>"
          ]
        }
      },
      {
       ...
        },
        "highlight" : {
          "about" : [
            "I love to go <p style=\"color:red\">rock</p> <p style=\"color:red\">climbing</p>"
          ]
        }
      }
    ]
  }
}
```

#### 数据分析

下面我们就来看下简单的数据统计，下面的表达式是按`age`进行分组，统计数据。这在`es`的专业术语叫聚合查询，类似于传统`SQL`中的`group by`，和传统的`SQL`很像：

```
curl -X GET "localhost:9200/megacorp/employee/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "aggs": {
    "all_interests": {
      "terms": { "field": "age" }
    }
  }
}
'
```

返回结果：

```json
{
  "took" : 3,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 9,
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
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 15,
          "about" : "I love to go reading",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "2",
        "_score" : 1.0,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to climbing go rock",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "3",
        "_score" : 1.0,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to go rock climbing",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "4",
        "_score" : 1.0,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to rock climbing",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "5",
        "_score" : 1.0,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to reading",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "6",
        "_score" : 1.0,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to reading go",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "7",
        "_score" : 1.0,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to reading and go",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "8",
        "_score" : 1.0,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to go and reading",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "9",
        "_score" : 1.0,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to do something",
          "interests" : [
            "sports",
            "music"
          ]
        }
      }
    ]
  },
  "aggregations" : {
    "all_interests" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 0,
      "buckets" : [
        {
          "key" : 25,
          "doc_count" : 8
        },
        {
          "key" : 15,
          "doc_count" : 1
        }
      ]
    }
  }
}
```

从返回结果中，我们可以看出，`age` 为`25`的数据有`8`条，`age`为`15`的数据有`1`条。

##### query和aggs组合使用

这里的聚合查询`aggs`是可以和`query`同时存在的,，就和`select name, count(*) from user group by name`一样：

```sh
curl -X GET "localhost:9200/megacorp/employee/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query" : {
        "match" : {
            "about" : "go reading"
        }
    },
    "aggs": {
    "all_interests": {
      "terms": { "field": "age" }
    }
  }
}
'
```

返回结果：

```json
{
  "took" : 10,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 7,
      "relation" : "eq"
    },
    "max_score" : 1.1097689,
    "hits" : [
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "1",
        "_score" : 1.1097689,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 15,
          "about" : "I love to go reading",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "6",
        "_score" : 1.1097689,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to reading go",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "7",
        "_score" : 1.0293508,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to reading and go",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "8",
        "_score" : 1.0293508,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to go and reading",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "5",
        "_score" : 0.7753851,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to reading",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "2",
        "_score" : 0.36634043,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to climbing go rock",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "3",
        "_score" : 0.36634043,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to go rock climbing",
          "interests" : [
            "sports",
            "music"
          ]
        }
      }
    ]
  },
  "aggregations" : {
    "all_interests" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 0,
      "buckets" : [
        {
          "key" : 25,
          "doc_count" : 6
        },
        {
          "key" : 15,
          "doc_count" : 1
        }
      ]
    }
  }
}
```

在返回结果中`aggregations`就是聚合查询的结果，`buckets`（桶）表示最后聚合结果，每个通（`bucket`）表示一条聚合结果。

##### 更多集合检索用法

聚合查询的规则本身也是支持多个规则组合使用的，我们在上面的聚合查询中又加入了平均值的计算：

```sh
curl -X GET "localhost:9200/megacorp/employee/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query" : {
        "match" : {
            "about" : "go reading"
        }
    },
    "aggs": {
    "all_interests": {
      "terms": { "field": "age" }
    },
     "avg_age" : {
                    "avg" : { "field" : "age" }
                }
  }
}
'
```

返回结果：

```json
{
  "took" : 16,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 7,
      "relation" : "eq"
    },
    "max_score" : 1.1097689,
    "hits" : [
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "1",
        "_score" : 1.1097689,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 15,
          "about" : "I love to go reading",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "6",
        "_score" : 1.1097689,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to reading go",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "7",
        "_score" : 1.0293508,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to reading and go",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "8",
        "_score" : 1.0293508,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to go and reading",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "5",
        "_score" : 0.7753851,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to reading",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "2",
        "_score" : 0.36634043,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to climbing go rock",
          "interests" : [
            "sports",
            "music"
          ]
        }
      },
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "3",
        "_score" : 0.36634043,
        "_source" : {
          "first_name" : "John",
          "last_name" : "Smith",
          "age" : 25,
          "about" : "I love to go rock climbing",
          "interests" : [
            "sports",
            "music"
          ]
        }
      }
    ]
  },
  "aggregations" : {
    "avg_age" : {
      "value" : 23.571428571428573
    },
    "all_interests" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 0,
      "buckets" : [
        {
          "key" : 25,
          "doc_count" : 6
        },
        {
          "key" : 15,
          "doc_count" : 1
        }
      ]
    }
  }
}
```

### 总结

实话实说，`elasticsearch`的搜索语法确实还是很复杂的，截止到今天，按照官方文档内容的章节安排，搜索部分的入门内容已经结束了，但是我怎么觉得我像刚入门一样，还是对`elasticsearch`没有全面的认识。我看了下剩余的内容，咋感觉现在才算正式开始了——深入搜索、处理人类语言、聚合、地理位置、数据建模、监控等都没开始学习呢？

好吧，我承认以前对`elasticsearch`的认知太浅显了，它确实是一套独立的知识体系（而不是一门语言），从某种程度上说，`elasticsearch`重新定义了搜索，所以还是好好学习吧，干就对了！

今天周末，稍微放纵了下，刷了半天的剧，然后快到晚上才开始梳理相关内容，不过某种程度上我觉得我们还是比较自觉的，任务也算顺利完成了，明天得早点开始了。加油吧，少年！

最后，预告下明天要更新的内容，除了我们既定的`elasticsearch`之外，我还要完成`7`月份内容的更新，所以明天的内容还是比较多的

好了，大家伙晚安吧！