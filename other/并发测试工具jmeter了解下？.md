# 并发测试工具jmeter了解下？

## 前言

随着互联网规模的不断发展壮大，系统接口的并发要求也是越来越高了，虽然现在已经有了很多技术可以提升系统的并发性能，但是测试又遇到了新的问题，我们该如何模拟线上环境的并发量呢？

今天我们推荐的这款测试利器，就可以很好地解决你的问题，一起来看看吧。

## Jmeter

### jmeter是什么

这一款工具是`Apache`开源基金会下的一个开源项目，是由纯`java`开发的，在测试圈比较知名，对于做过测试工作的小伙伴，这个工具应该不陌生。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529084622.png)

百度百科的解释：

> `Apache JMeter`是`Apache`组织开发的基于`Java`的压力测试工具。用于对软件做压力测试，它最初被设计用于`Web`应用测试，但后来扩展到其他测试领域。 它可以用于测试静态和动态资源，例如静态文件、`Java `小服务程序、`CGI `脚本、`Java `对象、数据库、`FTP `服务器， 等等。`JMeter `可以用于对服务器、网络或对象模拟巨大的负载，来自不同压力类别下测试它们的强度和分析整体性能。另外，`JMeter`能够对应用程序做功能/回归测试，通过创建带有断言的脚本来验证你的程序返回了你期望的结果。为了最大限度的灵活性，`JMeter`允许使用正则表达式创建断言。
>
> `Apache jmeter` 可以用于对静态的和动态的资源（文件，`Servlet`，`Perl`脚本，`java `对象，数据库和查询，FTP服务器等等）的性能进行测试。它可以用于对服务器、网络或对象模拟繁重的负载来测试它们的强度或分析不同压力类型下的整体性能。你可以使用它做性能的图形分析或在大并发负载测试你的服务器/脚本/对象。

简单来说，他就是一款压测工具，可以对我们的接口进行压力测试，找到接口高并发场景下可能存在的系统缺陷。

### 它能干什么

根据官网给出的说明，它可以完成以下工作：

- 能够加载和性能测试许多不同的应用程序/服务器/协议类型：
  - 网络协议-`HTTP`，`HTTPS`（`Java`，`NodeJS`，`PHP`，`ASP.NET`等）
  - `SOAP`/`REST` 网络服务
  - `FTP`服务
  - 通过`JDBC`连接的数据库
  - `LDAP`
  - 通过`JMS`的面向消息的中间件（`MOM`）
  - 邮件协议-`SMTP（S）`，`POP3（S）`和`IMAP（S）`
  - 本机命令或`Shell`脚本
  - `TCP`协议
  - `Java`对象
- 功能齐全的`Test IDE`，可进行快速的`Test Plan`**记录（来自浏览器或本机应用程序），构建和调试**。
- **`CLI `模式（命令行模式（以前称为非 `GUI`）/无头模式）**从任何 `Java `兼容操作系统（`Linux`、`Windows`、`Mac OSX` 等）加载测试
- 完整且可**随时呈现的动态 HTML 报告**
- 通过从大多数流行的响应格式，**HTML，JSON，** **XML**或**任何文本格式中**提取数据的能力，轻松实现关联
- `100%`基于` Java`，具有完全的可移植性 。
- 完整的**多线程**框架允许通过多个线程进行并发采样，并通过单独的线程组同时对不同的函数进行采样。
- 缓存和脱机分析/重放测试结果。
- 高度可扩展的核心：
  - 可插拔采样器允许无限的测试功能。
  - **可脚本化的采样器**（与`Groovy`和`BeanShell`等`JSR223`兼容的语言）
  - 可以使用**可插入计时器**选择几个负载统计信息。
  - 数据分析和**可视化插件**可实现出色的可扩展性和个性化。
  - 函数可用于为测试提供动态输入或提供数据操作。
  - 通过针对`Maven`，`Gradle`和`Jenkins`的第三方开源库，轻松进行持续集成。

从上面的说明来看，`Jmeter`支持的协议很丰富，同时具备了极强的可扩展性和可移植性，因为是基于`java`开发的，所以它本身也是跨平台的，同时还可以集成到`maven`、`Gradle`和`Jenkins`中，可以实现自动化测试，这一点就很强了。

### 开箱

接下来，我们就看下如何使用`jmeter`来完成我们的接口测试。

#### 下载

首先，我们先去官网下载最新版本`jmeter`：

```
https://jmeter.apache.org/download_jmeter.cgi
```

最新版本是`5.4.1`，运行环境基于`jdk1.8+`

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529090333.png)

`windows`环境下选择`zip`那个版本，不过也不影响，都是`java`开发的，解压工具能解压就行。

#### 解压运行

直接解压，然后进入`bin`目录，然后运行`jmeter.bat`脚本就可以了，当然前提条件是你要先配置本地的`JDK`环境，不会的小伙伴自行百度。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529090913.png)

打开之后，它是这样的

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529091112.png)

不习惯英文界面的小伙伴可以修改成中文

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529091447.png)

我不喜欢深色主题，所以我把它改成浅色了，想改的小伙伴自己改：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529091626.png)

### 开始测试

在开始测试之前，我们先要启动一个接口服务，我本地启动了一个`springboot`项目，就是上周的那个项目。单个`springboot`，内置的`Tomcat`是支持`10000`并发的，这一点还是很强的。

打开之后，默认已经创建了一个测试计划，我们可以直接用，修改相应配置即可

#### 配置测试计划

设置名称和注释，这里的配置主要是方便你管理测试计划，你不设置也不影响

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529102848.png)

#### 创建线程组

选中测试计划，右键选择添加`->`线程`->`线程组

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529103247.png)

#### 设置线程组配置

这里设置的就是我们的并发量，包括线程数、单个线程循环次数、延迟时间、持续时间等

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529103622.png)

#### 添加测试请求

选中线程组，右键选择添加`->`取样器`->`HTTP请求。这里需要注意的是添加的时候必须在线程组下创建，否则是没法测试的，因为所有的测试请求都是通过线程组发起的。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529103916.png)

#### 配置测试请求

这里就是配置我们接口的请求参数，包括协议、接口地址、请求方式、请求参数等

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529104519.png)

这时候就可以选中测试计划开始测试了，运行之前会提示我们保存测试计划：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529104858.png)

保存完成后，测试自动运行，这时候测试虽然启动了，但是是不会显示测试报告的，所以我们还需要增加报告。

#### 增加报告

同样是选中线程组，右键选择添加`->`监听器`->`选择需要的报告。这里我添加了两个报告，一个是汇总图，一个是汇总报告，你也可以根据自己的需要选择。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529105252.png)

然后再次运行，我们会发现汇总图和汇总报告这里就有结果了：

##### 汇总报告

报告里面包含了接口响应时间的统计，包括平均响应时间、最大响应时间、异常率、系统吞吐量、发送/接受数据的统计等，还是比较详细的。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529105711.png)

##### 汇总图

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529105850.png)

图表是支持配置的，你可以根据自己的需要进行设置，选择图形左上角的设置菜单即可

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529110118.png)

图表和数据都是可以保存的

##### 其他图表

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529110722.png)

#### 增加断言

写过单元测试的小伙伴肯定听过或者写过断言这个东西，断言简单来说就是我们在测试程序的时候，需要对某一段代码或方法运行结果进行比对，以判断程序业务逻辑是否正常，也就是做输入输出对比的。

比如我们将`2`传入一个方法，根据我们的预期，应该是`5`，如果处理之后结果与预期一致则断言通过，否则不通过，单元测试的断言这里就不说了，有兴趣的小伙伴自己去看看。

`jmeter`添加断言很简单，选中线程组，右键选择添加`->`断言`->`选择你需要的断言方式。这里我们选择`json`断言

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529111052.png)

##### 简单配置

`Assert josn path exists`设置`json`中你也校验的`key`，如果你只校验`key`存在即可，那可以去掉`Additionally assert value`的勾，这个配置勾选的话，会校验上面配置的`key`的值，而且你需要在`expected value`设置预期的值。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529112520.png)

这时候直接运行的话，是看不到断言结果的，我们还需要增加断言报告：

直接在监听器下选择断言结果就可以了。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529113036.png)

然后再次运行，断言结果这里就有数据了，断言如果通过是没有数据显示的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529113310.png)

但如果你指定的`key`不存在，就会有错误提示了，提示结果中不存在这个字段：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529113424.png)

如果你的返回值与断言预期结果不一致，则会提示，结果不匹配：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210529113610.png)

### 补充

`jmeter`的测试计划是支持多线程组的，也就是说你的一个测试计划可以配置多个接口，同时测试。

## 总结

`jmeter`作为一款流行的压测工具，从上手体验来看，还是很不错的，操作没有特别复杂，只需要简单配置就可以完成系统压测，这也可能是它比较流行的原因。目前，很多公司，系统上线前都是用`jmeter`进行压测的，这也从侧面体现了它稳定、强大的压测功能。

今天的内容依然是干货满满，让你直接可以开箱即用，而且也满足了你绝大多数的测试场景，有接口压测需要的小伙伴可以用起来了。