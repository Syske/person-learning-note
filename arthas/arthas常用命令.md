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


### trace

根据耗时跟踪方法：
```sh
 trace net.coolcollege.training.service.rpc.StudyProjectFacadeServiceImpl loadStudyProject "#cost>3000"
```

### 特殊用法

[Arthas的一些特殊用法文档说明](https://github.com/alibaba/arthas/issues/71)