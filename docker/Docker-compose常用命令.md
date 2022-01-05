### Docker-compose常用命令

#### 1. Docker-compose命令格式

```sh
docker-compose [-f <arg>...] [options] [COMMAND] [ARGS...]
```

 　命令选项如下

```sh
-f --file # FILE指定Compose模板文件，默认为docker-compose.yml
-p --project-name NAME # 指定项目名称，默认使用当前所在目录为项目名
--verbose # 输出更多调试信息
-v，-version # 打印版本并退出
--log-level LEVEL # 定义日志等级(DEBUG, INFO, WARNING, ERROR, CRITICAL)
```

####  2. docker-compose up

```sh
docker-compose up [options] [--scale SERVICE=NUM...] [SERVICE...]
# 选项包括：
-d # 在后台运行服务容器
-no-color # 不是有颜色来区分不同的服务的控制输出
-no-deps # 不启动服务所链接的容器
--force-recreate #强制重新创建容器，不能与-no-recreate同时使用
-no-recreate # 如果容器已经存在，则不重新创建，不能与–force-recreate同时使用
-no-build # 不自动构建缺失的服务镜像
-build # 在启动容器前构建服务镜像
-abort-on-container-exit # 停止所有容器，如果任何一个容器被停止，不能与-d同时使用
-t, -timeout TIMEOUT # 停止容器时候的超时（默认为10秒）
-remove-orphans # 删除服务中没有在compose文件中定义的容器
```

####  3. docker-compose ps

```sh
docker-compose ps [options] [SERVICE...] # 列出项目中所有的容器
```

####  4. docker-compose stop

```sh
docker-compose stop [options] [SERVICE...]
#选项包括
-t, -timeout TIMEOUT # 停止容器时候的超时（默认为10秒）
docker-compose stop # 停止正在运行的容器，可以通过docker-compose start 再次启动
```

####  5. docker-compose -h

```sh
docker-compose -h #查看帮助
```

####  6. docker-compose down

```sh
docker-compose down [options] # 停止和删除容器、网络、卷、镜像。
# 选项包括：
-rmi type # 删除镜像，类型必须是：all，删除compose文件中定义的所有镜像；local，删除镜像名为空的镜像
-v, -volumes # 删除已经在compose文件中定义的和匿名的附在容器上的数据卷
-remove-orphans # 删除服务中没有在compose中定义的容器
docker-compose down # 停用移除所有容器以及网络相关
```

####  7. docker-compose logs

```sh
docker-compose logs [options] [SERVICE...] 
# 查看服务容器的输出。默认情况下，docker-compose将对不同的服务输出使用不同的颜色来区分。可以通过–no-color来关闭颜色。
docker-compose logs # 查看服务容器的输出
-f # 跟踪日志输出
```

####  8. docker-compose bulid

```sh
docker-compose build [options] [--build-arg key=val...] [SERVICE...] 
# 构建（重新构建）项目中的服务容器。选项包括：
-compress # 通过gzip压缩构建上下环境
-force-rm # 删除构建过程中的临时容器
-no-cache # 构建镜像过程中不使用缓存
-pull # 始终尝试通过拉取操作来获取更新版本的镜像
-m, -memory MEM # 为构建的容器设置内存大小
-build-arg key=val # 为服务设置build-time变量，服务容器一旦构建后，将会带上一个标记名。可以随时在项目目录下运行docker-compose build来重新构建服务
```

####  9. docker-compose pull

```sh
docker-compose pull [options] [SERVICE...]
# 拉取服务依赖的镜像。``选项包括：
-ignore-pull-failures # 忽略拉取镜像过程中的错误
-parallel # 多个镜像同时拉取
-quiet # 拉取镜像过程中不打印进度信息
docker-compose pull # 拉取服务依赖的镜像
```

####  10. docker-compose restart

```sh
docker-compose restart [options] [SERVICE...] 
# 重启项目中的服务。选项包括：
-t, -timeout TIMEOUT # 指定重启前停止容器的超时（默认为10秒）
docker-compose restart # 重启项目中的服务
```

####  11. docker-compose rm

```sh
docker-compose rm [options] [SERVICE...] 
# 删除所有（停止状态的）服务容器。选项包括：
-f, -force # 强制直接删除，包括非停止状态的容器
-v # 删除容器所挂载的数据卷
docker-compose rm # 删除所有（停止状态的）服务容器。推荐先执行docker-compose stop命令来停止容器。
```

####  12. docker-compose start

```sh
docker-compose start [SERVICE...]
docker-compose start # 启动已经存在的服务容器。
```

####  13. docker-compose run

```sh
docker-compose run [options] [-v VOLUME...] [-p PORT...] [-e KEY=VAL...] SERVICE [COMMAND] [ARGS...]
# 在指定服务上执行一个命令。
docker-compose run ubuntu ping www.baidu.com # 在指定容器上执行一个ping命令。
```

####  14. docker-compose scale

```sh
docker-compose scale web=3 db=2 # 设置指定服务运行的容器个数。通过service=num的参数来设置数量
```

####  15. docker-compose pause

```sh
docker-compose pause [SERVICE...] # 暂停一个服务容器
```

####  16. docker-compose kill

```sh
docker-compose kill [options] [SERVICE...] 
# 通过发送SIGKILL信号来强制停止服务容器。支持通过-s参数来指定发送的信号，例如通过如下指令发送SIGINT信号：
ocker-compose kill -s SIGINT
```

####  17. docker-compose config

```sh
docker-compose config [options] 
# 验证并查看compose文件配置。选项包括：
-resolve-image-digests # 将镜像标签标记为摘要
-q, -quiet # 只验证配置，不输出。 当配置正确时，不输出任何内容，当文件配置错误，输出错误信息
-services # 打印服务名，一行一个
-volumes # 打印数据卷名，一行一个
```

####  18. docker-compose create

```sh
docker-compose create [options] [SERVICE...]
# 为服务创建容器。选项包括：
-force-recreate # 重新创建容器，即使配置和镜像没有改变，不兼容–no-recreate参数
-no-recreate # 如果容器已经存在，不需要重新创建，不兼容–force-recreate参数
-no-build # 不创建镜像，即使缺失
-build # 创建容器前生成镜像
```

####  19. docker-compose exec

```sh
docker-compose exec [options] SERVICE COMMAND [ARGS...] 
# 选项包括：
-d # 分离模式，后台运行命令。
-privileged #获取特权。
-user USER # 指定运行的用户。
-T # 禁用分配TTY，默认docker-compose exec分配TTY。
-index=index # 当一个服务拥有多个容器时，可通过该参数登陆到该服务下的任何服务，例如：
docker-compose exec -index=1 web /bin/bash # web服务中包含多个容器
```

####  20. docker-compose port

```sh
docker-compose port [options] SERVICE PRIVATE_PORT
# 显示某个容器端口所映射的公共端口。选项包括：
-protocol=proto # 指定端口协议，TCP（默认值）或者UDP
-index=index # 如果同意服务存在多个容器，指定命令对象容器的序号（默认为1）
```

####  21. docker-compose push

```sh
docker-compose push [options] [SERVICE...]
# 推送服务依的镜像。选项包括：
-ignore-push-failures # 忽略推送镜像过程中的错误
```

####  22. docker-compose stop

```sh
docker-compose stop [options] [SERVICE...] # 停止运行的容器
```

####  23. docker-compose uppause

```sh
docker-compose unpause [SERVICE...] # 恢复处于暂停状态中的服务。
```