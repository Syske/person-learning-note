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
	//  "cool:Cx111111@@tcp(10.30.1.89:3306)/coolcollege"
	dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s", user, passwd, host, port, dbName)
	fmt.Println(dsn)
	db, err := sql.Open("mysql", dsn)
	if err != nil {
		panic(err)
	}
	return db
}

func GetCoolPdbConnection(host string, port string) *sql.DB {
	dbUser := "cool"
	dbPassWd := "Cx111111@"
	dbName := "coolcollege"
	return GetDbConnection(host, port, dbUser, dbPassWd, dbName)
}

func TestPdb() {
	host := "10.30.1.89"
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
	host := "10.30.1.89"
	post := "3306"
	dbUser := "cool"
	dbPassWd := "Cx111111@"
	dbName := "coolcollege"
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

