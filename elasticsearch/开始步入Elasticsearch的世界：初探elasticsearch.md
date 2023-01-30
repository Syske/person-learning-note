# 开始步入Elasticsearch的世界：初探elasticsearch

### 前言

最近我参与了一个重构项目，由于这个下项目并发量比较大，而且经常出现`MQ`丢数据的问题，所以工单特别多，为了解决这个历史遗留问题，我们开启了为期两个月的重构之旅。

目前，这个项目刚刚启动，现在的核心架构，主要依托于`redis`，总的来说就是，所有的数据交互均依托于`redis`，不管是新增、查询、更新、删除等，都在`redis`上操作，然后通过一个`DAL`组件完成数据库数据同步。就是这样的架构，让我们在开发的时候简直要抓狂了，为了一个在数据库层面带索引的查询，我们需要从`redis`中拿出所有数据，然后从`list`中拿出我们需要的数据，感觉操作太复杂了，但是没办法呀，架构师就是这么定的。

因为后期要把`redis`换成`ES`，所以我就提前把相关内容学起来，以备不时之需。



### elasticsearch

#### 简介

`elasticsearch`是什么？根据它的字面意思，我们知道它和搜索有关，官方给出的解释是：

> `Elasticsearch `是一个分布式的免费开源搜索和分析引擎，适用于包括文本、数字、地理空间、结构化和非结构化数据等在内的所有类型的数据。`Elasticsearch `在 `Apache Lucene `的基础上开发而成，由 `Elasticsearch N.V.`（即现在的 Elastic）于 `2010` 年首次发布。`Elasticsearch `以其简单的 `REST` 风格 `API`、分布式特性、速度和可扩展性而闻名，是 `Elastic Stack `的核心组件；`Elastic Stack `是一套适用于数据采集、扩充、存储、分析和可视化的免费开源工具。人们通常将` Elastic Stack` 称为 `ELK Stack`（代指` Elasticsearch`、`Logstash `和 `Kibana`），目前 `Elastic Stack `包括一系列丰富的轻量型数据采集代理，这些代理统称为 `Beats`，可用来向 `Elasticsearch `发送数据。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210825125256.png)

简单来说，`elasticsearch`可以用以下几个关键字概括：

- 分布式
- 开源
- 搜索和分析引擎

做后端开发的小伙伴应该都清楚，在我们所有的系统中，基本上都是读多写少，所以真正制约一个系统性能是查询，是搜索，如果有一款组件可以解决数据搜索的问题，那系统的性能肯定会得到飞速提升，而`elasticsearch`就是这样一款组件。现阶段，很多企业都在用`es`，目前被提及最多的是携程，携程是大规模在使用，单日索引数据条数`600`亿，这就有点强了。

好了，关于简介就先到这里，更多信息各位小伙伴可以自己检索，下面我们看下如何安装使用`es`。

#### 下载

访问官方网站，选择对应版本，然后下载。官方地址如下：

```
https://www.elastic.co/cn/downloads/elasticsearch
```

这里我直接选择`windows`，各位小伙伴根据自己的操作系统进行选择。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210825083231.png)

#### 安装

下载过程还是很快的，下载完成后直接解压压缩文件即可：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210825083652.png)

下面我们简单介绍下，`elasticsearch`的文件结构：

- `bin`：存放可执行文件，包括脚本等，一般我们用的第三方组件都是这样的结构，比如`zk`、`nacos`等

- `config`：`elasticsearch`的配置文件

- `jdk`：这个各位小伙伴应该很熟悉，目前`elasticsearch-7.14.0`下的`jdk`版本比较高是`16.0.1`

  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210825084335.png)

  

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

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210825085557.png)

按照提示信息，`elasticsearch`的`JAVA_HOME`需要设置未`ES_JAVA_HOME`，`JAVA_HOME`不推荐使用，应该是怕和`jdk`冲突吧。

从启动日志我们看出以下几点：

- 启动的时候会加载`modules`的文件，具体各个模块的用途，我们暂时先不研究

- `elasticsearch`服务默认情况下会用到`9300`和`9200`，其中`9300`的端口协议未知，但是肯定不是`http`协议，`9200`是可以直接访问的：

  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210825123436.png)

  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210825123552.png)

- 访问`127.0.0.1:9200`，如果返回值结果如上，则表明`elasticsearch`启动成功。

#### 测试

安装启动完成后，`127.0.0.1:9200`访问也`ok`，说明`es`已经部署`ok`，下面我们对它进行一些简单测试。

在前面的简介中，我们知道`es`对外提供了 `REST` 风格 `API`，所以我们下面的测试都是基于`REST`接口进行的，为了方便我们后面就直接用`curl`工具（ 或者你也可以用`postman`）进行操作了。

##### REST

下面是`rest`协议的几种常用请求类别以及他们表示的含义，我们对`es`的操作也就是基于他们进行的：

- `PUT`请求：表示更新
- `POST`请求：表示写
- `DELETE`请求：表示删除
- `GET`请求：表示查询
- `HEAD`请求：与`GET`类似，但是不返回消息体
- `OPTIONS`请求：获取服务器支持的`HTTP`请求方法
- `TRACE`请求：用来调试`web`服务器连接的`HTTP`方式
- `CONNECT `请求：把服务器作为跳板，让服务器代替用户去访问其它网页，之后把数据原原本本的返回给用户

关于`Rest`协议我们暂时先说这么多，明天我们再详细说明。

以上这些请求中，`es`只支持`GET`,  `PUT`,  `DELETE`,  `HEAD`，其他的是不支持的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210825132837.png)

##### 创建索引

```sh
curl -X PUT 127.0.0.1:9200/syske
```

返回结果：

```json
{
    "acknowledged":true,
    "shards_acknowledged":true,
    "index":"syske"
}
```

##### 访问索引

```
curl -X GET 127.0.0.1:9200/syske
```

返回结果：

```json
  {
	"syske": {
		"aliases": {},
		"mappings": {},
		"settings": {
			"index": {
				"routing": {
					"allocation": {
						"include": {
							"_tier_preference": "data_content"
						}
					}
				},
				"number_of_shards": "1",
				"provided_name": "syske",
				"creation_date": "1629869376742",
				"number_of_replicas": "1",
				"uuid": "cFI0E1VxQrKyxNiH1qZBfA",
				"version": {
					"created": "7140099"
				}
			}
		}
	}
}
```



##### 删除索引

```sh
curl -X DELETE 127.0.0.1:9200/syske
```

返回结果

```json
{
    "acknowledged":true
}
```

**说明**：索引就类似于我们传统数据库中的库，一个索引就对应一个数据库。



### 总结

今天我们主要分享了`es`的下载、安装和测试，整体内容很简单，也不需要任何复杂的配置，只要确保`es`可以在本地正常启动即可。好了，`es`的简单入门我们今天就先到这里，我们从明天开始学习`es`的其他基本术语和用法。