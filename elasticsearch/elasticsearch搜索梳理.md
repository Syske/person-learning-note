# elasticsearch搜索梳理



### 搜索类型

#### match_all

`match_all` 查询简单的匹配所有文档。在没有指定查询方式时，它是默认的查询：

```json
{ "match_all": {}}
```

它经常与 filter 结合使用—例如，检索收件箱里的所有邮件。所有邮件被认为具有相同的相关性，所以都将获得分值为 `1` 的中性 `_score`。

#### match

无论你在任何字段上进行的是全文搜索还是精确查询，`match` 查询是你可用的标准查询。

如果你在一个全文字段上使用 `match` 查询，在执行查询前，它将用正确的分析器去分析查询字符串：

```json
{ "match": { "tweet": "About Search" }}
```

如果在一个精确值的字段上使用它，例如数字、日期、布尔或者一个 `not_analyzed` 字符串字段，那么它将会精确匹配给定的值：

```json
{ "match": { "age":    26           }}
{ "match": { "date":   "2014-09-01" }}
{ "match": { "public": true         }}
{ "match": { "tag":    "full_text"  }}
```



#### multi_match

`multi_match` 查询可以在多个字段上执行相同的 `match` 查询：

```json
{
    "multi_match": {
        "query":    "full text search",
        "fields":   [ "title", "body" ]
    }
}
```



#### range

`range` 查询找出那些落在指定区间内的数字或者时间：

```json
{
    "range": {
        "age": {
            "gte":  20,
            "lt":   30
        }
    }
}
```



被允许的操作符如下：

- **`gt`**

  大于

- **`gte`**

  大于等于

- **`lt`**

  小于

- **`lte`**

  小于等于

#### term

`term` 查询被用于精确值匹配，这些精确值可能是数字、时间、布尔或者那些 `not_analyzed` 的字符串：

```json
{ "term": { "age":    26           }}
{ "term": { "date":   "2014-09-01" }}
{ "term": { "public": true         }}
{ "term": { "tag":    "full_text"  }}
```

`term` 查询对于输入的文本不 *分析* ，所以它将给定的值进行精确查询。

#### terms

从效果上来说，`terms`类似于`sql`的`in`，`term`就类似于`sql`中的`=`

```json
{ "terms": { "tag": [ "search", "full_text", "nosql" ] }}
```

和 `term` 查询一样，`terms` 查询对于输入的文本不分析。它查询那些精确匹配的值（包括在大小写、重音、空格等方面的差异）。

#### exists 和 missing

`exists` 查询和 `missing` 查询被用于查找那些指定字段中有值 (`exists`) 或无值 (`missing`) 的文档。这与SQL中的 `IS_NULL` (`missing`) 和 `NOT IS_NULL` (`exists`) 在本质上具有共性：

```json
{
    "exists":   {
        "field":    "title"
    }
}
```



#### 组合多查询（bool）

**`must`**

文档 *必须* 匹配这些条件才能被包含进来。

**`must_not`**

文档 *必须不* 匹配这些条件才能被包含进来。

**`should`**

如果满足这些语句中的任意语句，将增加 `_score` ，否则，无任何影响。它们主要用于修正每个文档的相关性得分。

**`filter`**

*必须* 匹配，但它以不评分、过滤模式来进行。这些语句对评分没有贡献，只是根据过滤标准来排除或包含文档。



```
{
    "bool": {
        "must":     { "match": { "title": "how to make millions" }},
        "must_not": { "match": { "tag":   "spam" }},
        "should": [
            { "match": { "tag": "starred" }},
            { "range": { "date": { "gte": "2014-01-01" }}}
        ]
    }
}
```

查询示例

```json
{
	"query": {
		"bool": {
			"must": [
                {"match": { "name": "syske"	}},
                {"term": {"age": 25}}
            ]
		}
	}
}
```



#### 增加带过滤器（filtering）的查询

如果我们不想因为文档的时间而影响得分，可以用 `filter` 语句来重写前面的例子：

```json
{
    "bool": {
        "must":     { "match": { "title": "how to make millions" }},
        "must_not": { "match": { "tag":   "spam" }},
        "should": [
            { "match": { "tag": "starred" }}
        ],
        "filter": {
          "range": { "date": { "gte": "2014-01-01" }} 
        }
    }
}
```

通过将 range 查询移到 `filter` 语句中，我们将它转成不评分的查询，将不再影响文档的相关性排名。由于它现在是一个不评分的查询，可以使用各种对 filter 查询有效的优化手段来提升性能。

所有查询都可以借鉴这种方式。将查询移到 `bool` 查询的 `filter` 语句中，这样它就自动的转成一个不评分的 filter 了。

如果你需要通过多个不同的标准来过滤你的文档，`bool` 查询本身也可以被用做不评分的查询。简单地将它放置到 `filter` 语句中并在内部构建布尔逻辑：

```json
{
    "bool": {
        "must":     { "match": { "title": "how to make millions" }},
        "must_not": { "match": { "tag":   "spam" }},
        "should": [
            { "match": { "tag": "starred" }}
        ],
        "filter": {
          "bool": { 
              "must": [
                  { "range": { "date": { "gte": "2014-01-01" }}},
                  { "range": { "price": { "lte": 29.99 }}}
              ],
              "must_not": [
                  { "term": { "category": "ebooks" }}
              ]
          }
        }
    }
}
```

通过混合布尔查询，我们可以在我们的查询请求中灵活地编写 scoring 和 filtering 查询逻辑。

#### constant_score 查询

```json
{
    "constant_score":   {
        "filter": {
            "term": { "category": "ebooks" } 
        }
    }
}
```

