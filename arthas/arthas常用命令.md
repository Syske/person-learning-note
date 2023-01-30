# arthas常用命令


官方文档：[点击这里](https://arthas.aliyun.com/doc/)

### monitor
#### 描述
方法执行监控
#### 命令示例
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
观察函数调用返回时的参数、this 对象和返回值
#### 命令示例
##### 查看方法入参及返回值
```
watch net.coolcollege.user.service.impl.UserServiceImpl getUserDetail "{params,target,returnObj}" -x 2 -b
```