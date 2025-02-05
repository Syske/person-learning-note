## nested数据类型

在 Elasticsearch 中，`nested` 数据类型与其他数据类型（如 `object`、`keyword`、`text` 等）的核心区别在于**数据存储和查询的独立性**。

### **1. `object` 类型 vs `nested` 类型**

#### **(1) 数据存储方式**

- **`object` 类型**（默认的 JSON 对象）：
    
    - **扁平化存储**：Elasticsearch 会将 JSON 对象中的字段“打平”存储为键值对。例如：
        
        json
        
        复制
        
        {
          "resource_field": [
            { "title": "A", "sort": 1 },
            { "title": "B", "sort": 2 }
          ]
        }
        
        实际存储为：
        
        复制
        
        resource_field.title: ["A", "B"]
        resource_field.sort: [1, 2]
        
        - **问题**：无法区分数组中不同对象的字段关联性（例如 `title: "A"` 和 `sort: 2` 可能被错误关联）。
            
- **`nested` 类型**：
    
    - **独立存储**：数组中的每个对象会被存储为独立的隐藏文档（Lucene Document），保留字段间的关联性。
        
        - 上述示例会被存储为两个独立的 Lucene 文档：
            
            复制
            
            { "resource_field.title": "A", "resource_field.sort": 1 }
            { "resource_field.title": "B", "resource_field.sort": 2 }
            
        - 父文档通过内部机制关联这些子文档。
            

---

#### **(2) 查询行为**

- **`object` 类型**：
    
    json
    
    复制
    
    {
      "query": {
        "bool": {
          "must": [
            { "term": { "resource_field.title": "A" } },
            { "term": { "resource_field.sort": 2 } }
          ]
        }
      }
    }
    
    - **可能错误匹配**：即使 `title: "A"` 和 `sort: 2` 不属于同一个子对象，也会匹配成功（因为字段值被扁平化为数组）。
        
- **`nested` 类型**：
    
    json
    
    复制
    
    {
      "query": {
        "nested": {
          "path": "resource_field",
          "query": {
            "bool": {
              "must": [
                { "term": { "resource_field.title": "A" } },
                { "term": { "resource_field.sort": 2 } }
              ]
            }
          }
        }
      }
    }
    
    - **精确匹配**：只有当 `title: "A"` 和 `sort: 2` 属于同一个子对象时才会匹配。
        

---

### **2. `nested` 类型的核心特点**

#### **(1) 适用场景**

- 当 JSON 对象是**数组**，且需要**独立查询数组中的每个对象**时。
    
- 示例：商品的多规格属性（不同规格有不同价格、库存）、订单中的多个子订单。
    

#### **(2) 性能开销**

- **写入开销**：每个 `nested` 对象会生成独立的 Lucene 文档，写入性能比 `object` 类型低。
    
- **查询开销**：`nested` 查询需要处理父子文档的关联，性能低于普通查询。
    

#### **(3) 查询限制**

- 必须使用 `nested` 查询或 `nested` 聚合，否则无法正确检索子对象。
    
- 不支持跨 `nested` 对象的关联查询（如跨两个子对象做条件判断）。
    

---

### **3. 操作示例**

#### **(1) 定义 `nested` 字段**

json

复制

PUT /authority_resource_data
{
  "mappings": {
    "properties": {
      "resource_field": {
        "type": "nested",  // 显式声明为 nested 类型
        "properties": {
          "title": { "type": "text" },
          "sort": { "type": "integer" }
        }
      }
    }
  }
}

#### **(2) 查询 `nested` 字段**

json

复制

```json
{
  "query": {
    "nested": {
      "path": "resource_field",
      "query": {
        "bool": {
          "must": [
            { "match": { "resource_field.title": "公告" } },
            { "range": { "resource_field.sort": { "gte": 1 } } }
          ]
        }
      },
      "inner_hits": {}  // 返回匹配的子对象详情
    }
  }
}
```


### **4. 性能优化建议**

1. **控制嵌套深度**：避免多层 `nested`（如 `nested` 内再嵌套 `nested`），会显著增加复杂度。
    
2. **限制 `nested` 数组长度**：单个文档的 `nested` 对象数不宜过多（如不超过几百个）。
    
3. **使用 `doc_values`**：对 `nested` 字段中需要聚合或排序的字段启用 `doc_values: true`。
    
4. **必要时使用父子文档**：如果跨文档关联查询较多，考虑改用 `join` 类型（但性能也有代价）。
    

---

### **5. 常见误区**

- **误用 `object` 类型**：若对数组对象进行精确查询，但未声明 `nested`，会导致错误匹配。
- **忽略 `inner_hits`**：通过 `inner_hits` 可以明确知道哪些子对象满足了条件。
- **未优化映射**：对 `nested` 字段中的子字段未合理设置类型（如 `text` vs `keyword`）。

---

### **总结**

|特性|`object` 类型|`nested` 类型|
|---|---|---|
|数据存储方式|扁平化数组|独立子文档|
|查询关联性|跨对象字段可能错误匹配|精确匹配同一子对象字段|
|性能|高|低（写入和查询）|
|适用场景|无需独立查询子对象|需要精确匹配子对象|