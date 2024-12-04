# go项目构建流程

#### 项目初始化

这里直接通过`go mod init`命令进行构建，需要说明项目的包名信息，类似于`java maven`项目的`groupId+ artifactId`(包名 + 项目名)

```sh
 go mod init syske.github.io/test
```
之后会在文件夹下生成`go.mod`文件：

```mod
module syske.github.io/test

go 1.21.4
```

#### 编写项目代码

这里我们以连接`mysql`数据库为例：

```go
import (
	"database/sql"
	"time"
	"log"
	_ "github.com/go-sql-driver/mysql"
)

func main() {
	db, err := sql.Open("mysql", "user:password@/dbname")
	if err != nil {
		panic(err)
	}
	conn, _ := db.Conn(ctx)
	conn.Raw(func(conn interface{}) error {
	  ex := conn.(driver.Execer)
	  res, err := ex.Exec(`
	  UPDATE point SET x = 1 WHERE y = 2;
	  UPDATE point SET x = 2 WHERE y = 3;
	  `, nil)
	  // Both slices have 2 elements.
	  log.Print(res.(mysql.Result).AllRowsAffected())
	  log.Print(res.(mysql.Result).AllLastInsertIds())
	})
}
```

#### 更新mod文件

编写代码过程中，我们引入了新的依赖，所以我们要通过如下命令来下载依赖并更新`mod`文件：

```sh
 go mod tidy
```

执行上述命令之后，会自动扫描我们的源码，下载项目用到的依赖包，并更新`mod`文件

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20231129110428.png)

自动更新后的`mod`文件：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20231129111345.png)


#### build

```sh
go build
```