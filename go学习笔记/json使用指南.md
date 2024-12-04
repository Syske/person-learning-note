# go之json

`go`语言默认是有`json`包的，包路径是`encoding/json`，下面我们直接通过具体示例来看下如何使用：

#### 封装对象

首先，我们要封装一个对象：

```go
type Person struct {
    Name string `json:"name"`
    Age int `json:"age"`
}
```

这里字段的`json:"name"`标记的就是字段反序列化和序列化的字段名称，类似`fastJson`的`JsonFeild`注解。
这里还有一个点要注意，对象的字段首字母必须大写，否则序列化和反序列化无法被识别，会有如下编译错误：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20231217182327.png)

这是因为`go`语言中，是通过首字母控制属性可见性的，小写只能在当前包下使用


#### 反序列化

这里我们直接用`json`包下的`Unmarshal`方法

```go
jsonStr := `{ "name": "Alice", "age": 25 }`

 var person Person // 定义Person结构体变量

 err := json.Unmarshal([]byte(jsonStr), &person) // 将JSON字符串转换为struct对象
 if err != nil {
  panic(err)
 }
```

因为这里要复制，所以需要将`person`的地址传入


#### 序列化

序列化直接调用`json`的`Marshal`方法，返回结果是`byte`数组

```go
personStr, _ := json.Marshal(person)

fmt.Println(string(personStr))
```

#### 完整实现

下面是完整的代码，包括序列化和反序列化

```go
package main

import (
 "encoding/json"
 "fmt"
)

type Person struct {
 Name string `json:"name"`
 Age  int    `json:"age"`
}

func main() {
 // JSON字符串
 jsonStr := `{ "name": "Alice", "age": 25 }`

 var person Person // 定义Person结构体变量

 err := json.Unmarshal([]byte(jsonStr), &person) // 将JSON字符串转换为struct对象
 if err != nil {
  panic(err)
 }

 fmt.Println("Name: ", person.Name)
 fmt.Println("Age: ", person.Age)

 personStr, _ := json.Marshal(person)

 fmt.Println(string(personStr))
}
```
