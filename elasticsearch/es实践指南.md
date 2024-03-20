### 常用查询

#### 查询分词结果

```json
GET _analyze

{
  "analyzer": "ik_smart",
  "text": "全文测试参股222过不长度测试的关键词搜索测试关键词再次长度"
}
```

其中，`analyzer`表示分词器，目前常用的分词器有两个，一个是**ik_smart**, 另一个是**ik_max_word**。

前者会将文本做最细粒度的拆分，比如会将“中华人民共和国人民大会堂”拆分为“中华人民共和国、中华人民、中华、华人、人民共和国、人民、共和国、大会堂、大会、会堂等词语。

后者会做最粗粒度的拆分，比如会将“中华人民共和国人民大会堂”拆分为中华人民共和国、人民大会堂。


### 进阶查询

下面这个查询语句可以实现分词匹配，同时针对特定字段做了加权处理(`fields`字段)

```json
GET /100101951057547274620933/_search

{

    "query": {
        "bool": {
            "must": {
                "multi_match": {
                    "query": "全文测试参股222过不长度测试的关键词搜索测试关键词再次长度",
                    "operator": "or",
                    "fields": [
                        "title^3",
                        "tag^2",
                        "summary^2",
                        "text"
                    ],
                    "minimum_should_match": "50%"
                }
            },
            "filter":{
              "term": {
                    "type": 1
                }
            }
        }
    },
    "highlight": {
        "fields": {
            "title": {},
            "text": {},
            "summary": {},
            "tag": {}
        }
    },
    "from": 0,
    "size": 1000
}
```
