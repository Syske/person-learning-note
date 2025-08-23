# 工具类封装流程

### 封装流程

例如我这里封装了一个`db`工具类，文件的路径是`util/db_util`（相对于`main`方法的路径），源代码如下：

```go
package db_util

import (
	"database/sql"
	"fmt"

	_ "github.com/go-sql-driver/mysql"
)

func GetDbConnection(host string, port string, user string, passwd string, dbName string) *sql.DB {
<<<<<<< HEAD
	//  "cool:Cx111111@@tcp(10.30.1.89:3306)/coolcollege"
=======
	//  "test:test@tcp(192.168.0.1:3306)/test"
>>>>>>> 2b5c9fde2cfcfae33a64f4822874780e154c7961
	dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s", user, passwd, host, port, dbName)
	fmt.Println(dsn)
	db, err := sql.Open("mysql", dsn)
	if err != nil {
		panic(err)
	}
	return db
}

func GetCoolPdbConnection(host string, port string) *sql.DB {
<<<<<<< HEAD
	dbUser := "cool"
	dbPassWd := "Cx111111@"
	dbName := "coolcollege"
=======
	dbUser := "test"
	dbPassWd := "test"
	dbName := "test"
>>>>>>> 2b5c9fde2cfcfae33a64f4822874780e154c7961
	return GetDbConnection(host, port, dbUser, dbPassWd, dbName)
}

func TestPdb() {
<<<<<<< HEAD
	host := "10.30.1.89"
=======
	host := "192.168.0.1"
>>>>>>> 2b5c9fde2cfcfae33a64f4822874780e154c7961
	port := "3306"
	db := GetCoolPdbConnection(host, port)
	querySql := "select count(*) from enterprise"
	rows, err := db.Query(querySql)
	if err != nil {
		panic(err)
	} else {
		defer rows.Close()
		for rows.Next() {
			var count int
			err := rows.Scan(&count)
			if err != nil {
				panic(err)
			} else {
				fmt.Printf("count: %d", count)
			}
		}
	}
}

func TestDb() {
<<<<<<< HEAD
	host := "10.30.1.89"
	post := "3306"
	dbUser := "cool"
	dbPassWd := "Cx111111@"
	dbName := "coolcollege"
=======
	host := "192.168.0.1"
	post := "3306"
	dbUser := "test"
	dbPassWd := "test"
	dbName := "test"
>>>>>>> 2b5c9fde2cfcfae33a64f4822874780e154c7961
	db := GetDbConnection(host, post, dbUser, dbPassWd, dbName)
	querySql := "select id, original_name from enterprise limit 10"
	rows, err := db.Query(querySql)
	if err != nil {
		panic(err)
	} else {
		defer rows.Close()
		var enterpriseList [10]Enterprise
		i := 0
		for rows.Next() {
			// var id int
			// var name string
			var enterprise Enterprise
			err := rows.Scan(&enterprise.id, &enterprise.name)
			if err != nil {
				panic(err)
			} else {
				fmt.Printf("id: %d, name: %s\n", enterprise.id, enterprise.name)
				enterpriseList[i] = enterprise
				i++
			}
		}
		fmt.Println(len(enterpriseList))
		for i := 0; i < len(enterpriseList); i++ {
			fmt.Println(enterpriseList[i])
		}
	}
}

type Enterprise struct {
	id   int
	name string
}
```

调用方如下：

```go
package main

import (
	"syske.github.io/test/util/db_util"
)

func main() {

	db_util.TestDb()
	// db_util.TestPdb()

}
```
这里引入的就是`db_util`的包，项目的`go.mod`如下：

```sh
module syske.github.io/test

go 1.21.4

require github.com/go-sql-driver/mysql v1.7.1
```

综上过程，我们可以知道`go`本身是可以直接封装函数的（函数的集合），而文件名在实际引用中不需要关注的

### 注意事项

`go`语言中，方法名通常是首字母大写的，虽然首字母小写不会编译报错，且可以在同一个文件中调用，但是当跨文件调用时，就会提示找不到方法：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20231212111724.png)

上面这个问题其实不算问题，是因为`GO`语言本身是通过方法名称来控制可见性的（就类似`java`的`public/private`这些）：

> 标识符（包括常量、变量、类型、函数名、结构字段等等）以一个大写字母开头，如：Group1，那么使用这种形式的标识符的对象就可以被外部包的代码所使用（客户端程序需要先导入这个包），这被称为导出（像面向对象语言中的 public）；标识符如果以小写字母开头，则对包外是不可见的，但是它们在整个包的内部是可见并且可用的（像面向对象语言中的 private ）
>变量本身的可见性也遵循同样的规则

