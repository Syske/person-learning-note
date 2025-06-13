# arthas常用命令


官方文档：[点击这里](https://arthas.aliyun.com/doc/)


```
curl -O https://arthas.aliyun.com/arthas-boot.jar
java -jar arthas-boot.jar
```

### monitor
#### 描述
方法执行监控
#### 命令示例

##### monitor
监控方法执行情况
```
monitor -c 5 net.coolcollege.isv.api.controller.IsvController getSuiteToken
```
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20220726193243.png)
其中，
- `net.coolcollege.isv.api.controller.IsvController`表示全类名，
- `getSuiteToken`表示方法名，
- `-c`表示统计周期，默认是`120`秒，这里我们指定的是`5`秒

### wathch
#### 描述
查看方法入参、返回结果以及当前类的信息
```sh
watch demo.MathGame primeFactors "{params,returnObj}" -x 2 -s
```
其中，`primeFactors`表示方法名，`demo.MathGame`表示全类名

watch 的参数比较多，主要是因为它能在 4 个不同的场景观察对象

| 参数名称                | 参数说明                                    |
| ------------------- | --------------------------------------- |
| \_class-pattern\_   | 类名表达式匹配                                 |
| _method-pattern_    | 函数名表达式匹配                                |
| _express_           | 观察表达式，默认值：`{params, target, returnObj}` |
| _condition-express_ | 条件表达式                                   |
| [b]                 | 在**函数调用之前**观察                           |
| [e]                 | 在**函数异常之后**观察                           |
| [s]                 | 在**函数返回之后**观察                           |
| [f]                 | 在**函数结束之后**(正常返回和异常返回)观察                |
| [E]                 | 开启正则表达式匹配，默认为通配符匹配                      |
| [x:]                | 指定输出结果的属性遍历深度，默认为 1，最大值是 4              |

#### 将日志结果输出
```
options save-result true
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221122215837.png)


### 查看类的属性值

#### 查看类加载器的16进制值

```sh
sc -d net.coolcollege.incentive.service.business.restful.comment.CommentService
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240313203614.png)
#### 查看属性值

```sh
vmtool -c 117e0fe5 -a getInstances --className net.coolcollege.incentive.service.business.restful.comment.CommentService --express '#val=instances[0].resourceIds'
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240313203706.png)


```
# 获取本地缓存中的数据
 vmtool -c 1f2d2181 -a getInstances --className net.coolcollege.user.biz.cached.DepartmentCacheManager --express '#val=instances[0].DEPARTMENT_PARENT_CACHE.localCache.get(1878798350367723553L).value'
```

### trace

根据耗时跟踪方法：
```sh
 trace net.coolcollege.training.service.rpc.StudyProjectFacadeServiceImpl loadStudyProject "#cost>3000"
```

### 特殊用法

[Arthas的一些特殊用法文档说明](https://github.com/alibaba/arthas/issues/71)

### 其他异常
#### 提示地址被占用

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/52477a68-3ec9-42b8-8718-1eea2a2a6280.jpg)

```sh
[root@t2-cmdb-api-64c69b5b9f-5td6f java]# java -jar arthas-boot.jar 
Picked up JAVA_TOOL_OPTIONS: -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005
ERROR: transport error 202: bind failed: Address already in use
ERROR: JDWP Transport dt_socket failed to initialize, TRANSPORT_INIT(510)
JDWP exit error AGENT_ERROR_TRANSPORT_INIT(197): No transports initialized [debugInit.c:750]
```

解决方式：
```sh
# 指定环境变量，然后再再次运行
export JAVA_TOOL_OPTIONS="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5006"
```

#### 提示需要指定pid

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/bfa508d5-2d0d-4804-a32e-bdb27db6048e.jpg)

解决方法：
```sh
# 运行时指定pid
java -jar arthas-boot.jar 1
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/e4e04331-2214-48db-b417-9c282e632424.jpg)

## 监控MyBatis的SQL语句（推荐）

1. 首先找到MyBatis执行SQL的类：

```
sc *StatementHandler
```

2. 然后监控RoutingStatementHandler或PreparedStatementHandler：
```
watch org.apache.ibatis.executor.statement.PreparedStatementHandler query '{params, target.boundSql.sql, returnObj}' -x 3
```

## 筛选参数中符合条件的数据

```sh
watch net.coolcollege.usercenter.service.strategy.impl.ImportUserByUserIdStrategy parseUserImportDto 'params[2].{?#this.userId == "ou_67be58fd131ca84ea46213ea6896207b"}' -s -x 3
```

上面的示例，是筛选入参中第三个参数（`list`）中，`userId`为`ou_67be58fd131ca84ea46213ea6896207b`的数据