# java EE学习流程（更新）

这周有点堕落了，这两天啥都没写，就顾上刷《庆余年》了😂，今天拿还没完成的javaEE的学习流程来充个数，这个是我在原来基础上增加和更新后的学习流程。里面增加了现有的一些新技术，同时也增加了我了解到的技术和框架。希望能够帮助到正在学习的你，资源链接如下：

链接: https://pan.baidu.com/s/1XSyene6Fva6jrqaiH1s8bQ 提取码: 53qr

图片版本的我放在文末了，比较长，以下是内容大纲：

## 第一阶段

### 计算机基础知识

- 计算机基本构成

	- 硬件
	- 软件

- 基本架构

	- 硬件层
	- 操作系统层
	- 软件层

- 基本运行原理

### web前端基础

- HTML

	- 基础知识

		- 概念
		- 注释
		- 标签
		- 元素
		- 网页结构

	- H5新特性

		- 新元素
		- 新标签
		- video和Audio
		- 2D/3D制图
		- 其他新特性

- CSS

	- 基本语法

		- 基本构造
		- 选择器

			- 标签选择器
			- 类选择器
			- ID选择器

		- 样式表插入方式

			- 外部样式表

			  ```
			  <link rel="stylesheet" type="text/css" href="mystyle.css">
			  ```

			- 内部样式表

			  ```
			  <style>
			  hr {color:sienna;}
			  p {margin-left:20px;}
			  body {background-image:url("images/back40.gif");}
			  </style>
			  ```

			- 内联式

			  ```
			  <p style="color:sienna;margin-left:20px">这是一个段落。</p>
			  ```

			- 优先级

			  内联样式）Inline style > （内部样式）Internal style sheet >（外部样式）External style sheet > 浏览器默认样式

		- 注释

		  ```js
		  /*这是个注释*/
		  p
		  {
		  text-align:center;
		  /*这是另一个注释*/
		  color:black;
		  font-family:arial;
		  }
		  ```

	- 常用库

		- bootsrap

- javascript

	- 基本语法

		- 运算符
		- 数据

			- 变量
			- 常量
			- 类型转换
			- 对象

				- 内置对象

					- prototype
					- Number
					- String
					- Date
					- Array
					- Boolean
					- Math
					- RegExp

				- 自定义对象

		- 流程控制

			- 条件控制

				- if
				- switch
				- 三元运算

			- 循环

				- for
				- while

			- 其他

				- Break
				- continue

		- 异常处理
		- 函数/方法

			- 定义
			- 参数
			- 调用

	- dom的基本操作
	- 异步请求
	- json

		- 语法规则

			- 数据为 键/值 对。
			- 数据由逗号分隔。
			- 大括号保存对象
			- 方括号保存数组

		- json解析

			- JSON.parse(text)
			- eval()

	- 常用库

		- Jquery
		- vue
		- react
		- Angular

- 集成框架

	- Amaze UI
	- Vali Admin
	- EasyUI 
	- AdminLTE
	- Element

## 第二阶段

### java基础语法

- 语法格式
- 数据

	- 变量

		- 成员变量
		- 局部变量

	- 常量
	- 作用域

- 数据类型

	- 基本数据类型

		- 数字

			- 整数

				- byte
				- short
				- int
				- long

			- 浮点数

				- float
				- double

		- 字符

			- char

		- 逻辑

			- boolean

	- 拆箱和装箱

		- Byte
		- Short
		- Integer
		- Long
		- Double
		- Float
		- Character
		- Boolean

	- 引用类型

		- 对象
		- 接口
		- 枚举类型
		- 数组

			- 一维数组
			- 多维数组

		- 注解类型

- 方法

	- 定义
	- 分类

		- 类方法/静态方法
		- 实例方法
		- 构造方法

	- 调用

- 运算符

	- 赋值
	- 自增/自减
	- 算术运算符
	- 逻辑运算符
	- 位运算符
	- 比较运算

- 流程控制

	- 条件控制

		- if语句
		- switch语句

	- 循环语句

		- for循环
		- while循环
		- do-while循环

	- break

		- 跳出当前循环

	- continue

		- 跳出本轮循环

- 访问控制

	- private
	- 无修饰/包访问（默认）
	- protected
	- public

### 面向对象

- 基本特性

	- 封装
	- 继承

		- 方法重写
		- 方法重载
		- super关键字
		- this关键字
		- final关键字
		- abstract关键字
		- static关键字

	- 多态

- 高级特性

	- 反射
	- 正则表达式

- 接口
- 抽象类
- 设计模式

	- 观察者模式
	- 中介者模式
	- 单例模式
	- 工厂模式
	- 策略模式

### javaAPI

- 常用工具类/接口

	- 容器

		- 泛型
		- 常用容器

			- Collection

				- Set

					- HashSet

				- List

					- Vector
					- ArrayList
					- LinkedList

				- Queue

			- Map

				- HashMap
				- HashTable

					- 线程安全

	- String
	- Date
	- DateFormat

- 其他类

	- 内部类
	- 匿名类
	- Class类
	- Object类

- 动态代理
- 空对象
- 注解

### 异常处理

- try/catch
- finally

### 多线程

- 多线程

	- 创建方式

		- Runnable
		- Thread

	- 线程状态
	- 常用方法
	- 线程管理

- 并发

### IO基础

- 类

	- File
	- 压缩

		- GZIP
		- Zip

- 流

	- 输入流
	- 输出流
	- 缓冲流
	- 字节流
	- 字符流

### 网络编程

- 通信协议

	- TCP/IP
	- UDP

- 应用层协议

	- HTTP
	- FTP

- socket编程

### 图形化界面

- applet
- Swing
- AWT

### JKD新特性

- 1.8

	- 接口增加default方法
	- Lambda表达式

## 第三阶段

### web后端

- 基础知识

	- JSP/Servlet
	- Linstener
	- Filter
	- jstl和EL
	- Ajax
	- XML
	- JSON

- 数据库

	- 关系型数据库

		- Mysql
		- Orcale
		- 基本语法

			- 操作类型

				- 增（insert）
				- 删（delete）
				- 改（upadte）
				- 查（selecet)

			- 多表连接和子查询

		- 数据库连接池

			- DRUID
			- HikariCp
			- dbcp
			- c3p0

		- JNDI
		- JDBC
		- 数据库设计优化
		- 数据库存储过程
		- sql调优

	- 非关系型数据库

		- Redis
		- mongoDB

- 架构

	- 逻辑与页面分离

		- JSP/Servlet

	- MVC
	- SSH架构
	- SSM架构
	- 微服务

- 服务器

	- linux

		- shell脚本
		- 常用命令

	- docker
	- 运行容器

		- Tomcat
		- JBoss
		- Weblogic

			- domin创建
			- 服务器内存设置
			- 数据源配置
			- 项目部署
			- classpath设置

- 日志管理

	- JDKLog
	- Log4j
	- LogBack
	- SLF4J

- 单元测试

	- Junit

- 应用及接口

	- 接口

		- webservice

			- SOAP

				- XML交互

			- 第三方解决方案

				- CXF
				- axis

		- json

			- RESTFUL

				- JSON交互

- 包管理工具

	- maven

		- 生成可执行jar、理解Scope生成最精确的jar
		- 类冲突、包依赖NoClassDefFoundError问题定位及解决
		- 全面理解Maven的Lifecycle、Phase、Goal
		- 架构必备之Maven生成Archetype
		- Maven流行插件实战、手写自己的插件
		- Nexus使用、上传、配置
		- 对比Gradle

	- grable

- 版本管理工具

	- git

		- git的基本知识与原理
		- 常用命令
		- Git冲突解决
		- 架构师职责：Git flow规范团队git使用规程
		- 团队案例分享

	- SVN
	- starTeam

- 项目管理工具

	- 禅道

- 热门框架

	- 视图层及控制层

		- Spring

			- spring MVC
			- Spring Boot

		- Struts

	- 数据库交互

		- Mybatis
		- Hibernate

	- 前端模板引擎

		- Thymeleaf

	- 前后端开发对接

		- Swagger

	- 代码自动生成

		- MybatisPlus

## 第四阶段

### 技术

- 微服务

	- dubbo
	- Spring Cloud
	- ServiceMesh

- 报表技术

	- 润乾报表
	- FineReport
	- UReport2

- lucene搜索引擎
- 缓存技术

	- redis
	- echace

- 工作流
- Excel技术

	- EasyExcel
	- poi Excel

- Fckeditor编辑器
- 中间件

	- 消息队列
	- Zookeeper

### 项目

- 电商项目

	- 用户认证

		- 用户注册
		- sso单点登录
		- 第三方登录
		- 业务拦截
		- 权限

	- 店铺、商品

		- 聚合检索
		- 动静分离
		- 店铺管理
		- 商品管理

	- 订单、支付

		- 订单号统一生成规则
		- 下单流程管理
		- 库存管理
		- 购物车
		- 优惠券支付
		- 积分支付
		- 第三方支付

	- 数据统计分析

		- 用户行为分析
		- 行业分析
		- 区域分析

	- 消息推送

		- 融云推送
		- 消息中间件
		- 用户群聊
		- 点对点聊天
		- 文件断点续传

- 微信公众号

## 第五阶段

### 读写分离

### 分布式架构

### 性能优化

- JVM调优
- 中间件调优

### 高级工具

- Jenkins

  可以更好地持续编译，集成，发布你的项目

	- 搭建自动部署环境
	- 继承maven、git实现自动部署
	- test\pre\production多环境发布
	- 多环境配置、权限管理及插件使用

- Sonar

  一个开源的代码质量分析平台，便于管理代码的质量，可检查出项目代码的漏洞和潜在的逻辑问题(提升代码的质量，更加高效地提升开发效率)。

	- 使用Sonar进行代码质量管理
	- 关于代码检查工具FIndBugs/PMD的运用
	- SonarQube代码质量管理平台安装及使用
	- 使用Jenkins与Sonar集成对代码进行持续检测
	- Idea与Sonar集合的使用

![](E:\workSpeace\learning_files\note\微信公众号发布\java EE学习流程.png)

