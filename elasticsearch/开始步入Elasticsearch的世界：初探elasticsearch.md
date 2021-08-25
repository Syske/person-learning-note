# 开始步入Elasticsearch的世界：初探elasticsearch

### 前言

最近我参与了一个重构项目，由于这个下项目并发量比较大，而且经常出现`MQ`丢数据的问题，所以工单特别多，为了解决这个历史遗留问题，我们开启了为期两个月的重构之旅。

目前，这个项目刚刚启动，现在的核心架构，主要依托于`redis`，总的来说就是，所有的数据交互均依托于`redis`，不管是新增、查询、更新、删除等，都在`redis`上操作，然后通过一个`DAL`组件完成数据库数据同步。就是这样的架构，让我们在开发的时候简直要抓狂了，为了一个在数据库层面带索引的查询，我们需要从`redis`中拿出所有数据，然后从`list`中拿出我们需要的数据，感觉操作太复杂了，但是没办法呀，架构师就是这么定的。

因为后期要把`redis`换成`ES`，所以我就提前把相关内容学起来，以备不时之需。



### elasticsearch

#### 简介



#### 下载

访问官方网站，选择对应版本，然后下载。官方地址如下：

```
https://www.elastic.co/cn/downloads/elasticsearch
```

这里我直接选择`windows`，各位小伙伴根据自己的操作系统进行选择。

![](https://gitee.com/sysker/picBed/raw/master/20210825083231.png)

#### 安装

下载过程还是很快的，下载完成后直接解压压缩文件即可：

![](https://gitee.com/sysker/picBed/raw/master/20210825083652.png)

下面我们简单介绍下，`elasticsearch`的文件结构：

- `bin`：存放可执行文件，包括脚本等，一般我们用的第三方组件都是这样的结构，比如`zk`、`nacos`等

- `config`：`elasticsearch`的配置文件

- `jdk`：这个各位小伙伴应该很熟悉，目前`elasticsearch-7.14.0`下的`jdk`版本比较高是`16.0.1`

  ![](https://gitee.com/sysker/picBed/raw/master/20210825084335.png)

  

- ``lib`： `elasticsearch`本身应该是基于`java`开发的，所以`lib`就是`elasticsearch`要用到的包，其中也包括它自身应用的包
- `logs`：存放运行日志，目前是空的
- `modules`：这个应该是`elasticsearch`可以扩展的模块，默认情况下好多模块是不启用的
- `plugins`：这个应该是存放第三方扩展组件的，目前该文件夹是空的。

好了，`elasticsearch`的目录结构我们暂时就说这么多，下面看下如何启动`elasticsearch`。

#### 启动

启动`elasticsearch`也很简单，只需要执行`bin`文件夹下的脚本即可：

```
elasticsearch.bat
```

如果启动报错，检查下本地`jdk`版本，最好选择`16`及以上版本，因为我本地安装的就是`16`，所以启动没有报错，但是在控制台有如下提示：

![](https://gitee.com/sysker/picBed/raw/master/20210825085557.png)

按照提示信息，`elasticsearch`的`JAVA_HOME`需要设置未`ES_JAVA_HOME`，`JAVA_HOME`不推荐使用，应该是怕和`jdk`冲突吧。