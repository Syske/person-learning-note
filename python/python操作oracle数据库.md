## python操作Oracle数据库

#python #oracle



利用这漫长的假期，我又一次拾起来已经放弃了很多次的python，开始了一波新的尝试，不过庆幸的是，这一次好像多少有了一点眉目，感觉开始入门了（我承认，我一开始对python有成见），所以我就开始了新的尝试，也有了新的收获，也有了今天这两篇博客。

### 安装cx_Oracle

cx_Oracle相当于python的Oracle数据库的驱动，必须有驱动才能连接Oracle数据库，具体方法如下：

#### 方法一：直接在官方网站下载，然后安装

```url
https://pypi.org/project/cx-Oracle/
```

选择对应的系统及版本，然下载安装

#### 方法二：通过pip安装

```sh
pip install cx-Oracle
```

我是同第二种方式安装，可以通过如下方式检查自己是否已经安装，以及安装的版本信息：

```sh
 pip show -f cx-Oracle
```

### 添加Oracle客户端配置

#### 下载Oracle数据库对应的客户端

##### 查看数据库版本

可以通过如下sql查看版本信息：

```mssql
select * from v$version;
```

比如我的Oracle数据库版本号为：

```
1	Oracle Database 11g Enterprise Edition Release 11.2.0.4.0 - 64bit Production
2	PL/SQL Release 11.2.0.4.0 - Production
3	"CORE	11.2.0.4.0	Production"
4	TNS for Linux: Version 11.2.0.4.0 - Production
5	NLSRTL Version 11.2.0.4.0 - Production
```

##### 下载数据库客户端

具体下载地址如下：

```
https://www.oracle.com/cn/database/technologies/instant-client/downloads.html
```

选择对应的操作系统和版本，当然必须得和你的python版本一致(64Bit/32Bit)

因为我的数据库版本是：11.2.0.4.0，所以我下载的客户端版本也是这个版本[instantclient-basic-windows.x64-11.2.0.4.0.zip](https://download.oracle.com/otn/nt/instantclient/11204/instantclient-basic-windows.x64-11.2.0.4.0.zip?AuthParam=1582884626_f7d9b0483b20967531cbe6f5f0bd24da)

然后解压，并将解压后的地址信息加入到操作系统环境变量中，比如我的文件夹路径为：

```
E:\app\myUserName\product\11.2.0_64bit
```

那么，我的环境变量设置如下：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20210128103625.png)

上面的环境变量是添加在path这个变量底下的。

#### 配置TNS

##### 创建tnsnames.ora

进入如下目录，并创建tnsnames.ora文件。如果没有可以手动创建(我是之前安装过完整版客户端，所以已经有了，我从已经安装过的目录下直接拷贝，之前安装的是32Bit)

```
E:\app\myUserName\product\11.2.0_64bit\network\admin
```

也有人说可以在上面添加的环境变量的目录下直接创建这个文件（即`E:\app\myUserName\product\11.2.0_64bit`），我没有尝试过，如果有小伙伴试过了可行，请告诉我，谢谢！

##### 配置数据库信息

打开刚刚创建的tnsnames.ora文件，加入你的数据库连接配置（TNS配置）：

```
ORCL =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = host)(PORT = 1522))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = orcl)
      (INSTANCE_NAME = orcl1)      
    )
  )
```

你如果有用`ql/sql`的话，对这个文件应该不陌生，`host`就是你的数据库`ip`地址，`PORT`就是数据库端口，`SERVER`一般应该都一样（我猜的），`SERVICE_NAME`和`INSTANCE_NAME`应该是你创建数据库的时候设置的，没创建过Oracle数据库，我只负责用😂。

添加完以上配置信息，然后就该开始编写我们的测试脚本了

### 编写python脚本

脚本很简单，就几行代码：

```python
#!/usr/bin/env python
import cx_Oracle
# 格式：用户名/密码@主机:端口/SERVICE_NAME
con = cx_Oracle.connect('userName/Password@host:1522/orcl') 
# 格式：用户名，密码，主机:端口/SERVICE_NAME
con2 = cx_Oracle.connect('userName', 'Password', 'host:1522/orcl') 
print(con.version)
print(con2.version)
```

这里解释下，其实也不用解释，因为确实很简单。引入`cx_Oracle`，然后获取数据库连接，打印数据库版本。获取数据库有两种方式，区别不大，都是将用户名、密码、主机、端口、服务传入，然后获取数据库连接。

#### 遇到的问题

如果你能正常打印数据库版本信息，那么恭喜你，第一次就如此完美的取得成功。很多人，包括我，在进行以上步骤都遇到了很多问题，说下我的问题，报错信息如下：

```sh
cx_Oracle.DatabaseError: DPI-1047: 64-bit Oracle Client library cannot be loaded:  "libclntsh.so: cannot open shared object file: No such file or directory". See https://oracle.github.io/odpi/doc/installation.html#linux for help
```

和以上错误很类似，因为没保留错误信息，所以我大概根据浏览器历史记录查了下。我查询的结果是说`python`版本和`Oracle`数据库客户端版本不一致，因为我的`python`是64位的，数据库客户端版本是32位，然后我下载64位客户端，并替换了环境变量，重启了电脑，依然不行，几经折腾，最后我发现有篇博客说是需要在`python`安装根目录下复制`Oracle`配置的`dll`文件，想尝试的时候，发现文件夹没权限，最后忍无可忍，我把`python`重新安装（3.8），然后安装pip并重新安装`cx-Oracle`（cx_Oracle-7.3.0，pip直接安装）,竟然神奇的好了，嗯~ o(*￣▽￣*)o还好我没放弃😂

### 完善脚本，执行查询

完成以上步骤，说明我们已经完成了`python`连接`Oracle`数据库的配置工作，接下来我们将了解如何执行`sql`语句，并获取返回结果。其实，也很简单，参照如下代码即可。

```python
	# 获取数据库游标对象
    cursor= connection.cursor()
    # sql参数集
    params = {'aapid': aapid,'yearMonth':'2020-02'}
    # sql
    sql = '''SELECT * FROM log WHERE CreateTime like :yearMonth||'%'
    AND aapid=:aapid '''
    # 执行sql
    query = cursor.execute(sql, params)
	# 获取查询结果集
    rows = cursor.fetchall()  
	# 获取结果列（数据库字段名）
    titles = cursor.description 
    print(rows)
    print(titles)
```

执行以上代码，即可打印sql查询到的结果集。需要注意的是，`sql`查询参数集是通过字典的形式导入的，然后在`sql`中通过`:` + 键名的方式传入参数。

当然能执行`sql`的方法不止上面的一种，比如你需要入参的时候，可以通过如下方式执行查询：

```python
sql = "select * from test limit 10"  # 在test表中取出十条数据
search_count = cursor.execute(sql)
```

有关其他的插入、更新、删除、建表等操作，后续再继续进行深入探索，主要是我现在也不会啊😂好了，今天就到这里吧，不早了，早点休息吧，晚安，好梦！

