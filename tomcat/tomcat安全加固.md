# 记一次Tomcat一句话木马修复
tags: [#tomcat, #木马]

### 起因

近期，网络中心反馈，这边有一个服务器发现了一句话木马，我想着应该是我的服务，因为之前这个服务就中过一次毒，后来升级了`tomcat`，删除了无用的文件和配置。但是这次还是中毒了，查了一些资料，修改了配置，`Tomcat`也升级到最新版本，这次应该不会再有问题了，再有问题的话，我再来继续更新😂

### 版本信息

`Tomcat：9.0.34`

### 配置过程

#### 删除管理及示例项目

进入`Tomcat`安装目录

```
cd %tomcat_home% 
```

删除`webapps`下所有内容（当然自己的项目如果已经部署过了，别删除）

```shell
rm -rf *
```

为什么要删除，因为tomcat默认部署了项目管理服务和示例项目，特别是管理模块，很可能被非法利用

#### 配置server.xml

文件路径：

```sh
%tomcat_home%/config/server.xml
```



##### 1、修改服务器端口

下面是默认配置，改成你自己的端口号：

```xml
 <Connector port="8080" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="8443" />
```

比如

```xml
 <Connector port="9999" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="8443" />
```



##### 2、修改服务器关闭命令及端口

下面是默认配置，改成你自己的端口号和命令：

```xml
<Server port="8005" shutdown="SHUTDOWN">
```

比如

```XML
<Server port="9995" shutdown="AFADSLFJKDFJALSDF887676">
```

##### 3、关闭热部署

默认：

```xml
 <Host name="localhost"  appBase="webapps"
            unpackWARs="true" autoDeploy="true">
```

关闭：

```xml
 <Host name="localhost"  appBase="webapps"
            unpackWARs="false" autoDeploy="false">
```

我觉得，这里应该是很重要很关键的，之前我一直是启用热部署的，感觉很方便，但如果有人把恶意代码传到webapps下面，同样也会自动部署，这是很危险的。还有需要注意的是，如果`unpackWARs="false"`就意味着你要自己手动解压war包，tomcat不会自动解压，这样更安全，但是也有很多不变。linux环境的话，可以通过unzip解压：

```
unzip -op *.war 
```



##### 4、关闭用户配置

将如下配置注释掉即可

```xml
 <GlobalNamingResources>
    <!-- Editable user database that can also be used by
         UserDatabaseRealm to authenticate users
    -->
    <Resource name="UserDatabase" auth="Container"
              type="org.apache.catalina.UserDatabase"
              description="User database that can be updated and saved"
              factory="org.apache.catalina.users.MemoryUserDatabaseFactory"
              pathname="conf/tomcat-users.xml" />
  </GlobalNamingResources>
```

#### 修改web.xml

文件路径：

```
%tomcat_home%/config/web.xml
```

##### 1、增加错误处理页面

```
    <error-page>
	    <error-code>404</error-code>
		<location>/404.html</location>
	</error-page>
	<error-page>
	    <error-code>403</error-code>
		<location>/403.html</location>
	</error-page>
	<error-page>
	    <error-code>500</error-code>
		<location>/500.html</location>
	</error-page>
    ...
```

为什么要增加错误处理页面，我觉得第一个原因是避免泄露太多的错误信息，比如Tomcat的版本信息，以及不想暴露的错误信息；另一个原因是出于美观考虑，自带的错误页面太丑了

##### 2、修改tomcat版本信息

为什么要修改呢，因为如果你暴漏了自己的tomcat版本信息，而且你恰好有好多漏洞没修复，对方根据你的版本信息就能查到你可能有哪些潜在漏洞，但如果你隐藏了版本信息，想要发掘你的容器漏洞还是有很多难度的。下来，我们看下如何修改：

首先，进入Tomcat的lib目录：

```
cd %tomcat_home%/lib
```

找到catalina.jar，用压缩软件打开，在jar包的如下路径找到版本配置文件：ServerInfo.properties

```
org.apache.catalia.util
```

修改前的内容如下：

```properties
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

server.info=Apache Tomcat/9.0.33
server.number=9.0.33.0
server.built=Mar 11 2020 09:31:38 UTC
```

然后自己可以随意修改，比如：

```properties
server.info=Apache Tomcat/999999999999999
server.number=999999999999999999
server.built=999999999999999999999 UTC
```

然后再替换重新打包，当然如果用的是压缩软件的话直接保存就好了。linux环境的话，可以将对应的jar包拉下来，替换后再上传。

当你修改完版本信息，tomcat的错误页再也看不到正确的版本信息了。

##### 3、屏蔽jsp

之前项目有用到jsp，现在已经改成html了，所以我可以屏蔽jsp文件。但是本次我没有配置这个，如果后面还有问题的话，我会考虑这个方法。这次就不说了，我也还没查相关资料



### 总结

希望这次过后，服务不会再出现问题。这次的问题可能和三个月前刚发布的Tomcat漏洞有关系，因为说的是AJP服务，我看服务器的配置，没有开启这个配置，所以也就没有升级服务器。

漏洞编号：

- `CVE-2020-1938`
- `CNVD-202-1048`

受影响的版本如下：

- `Apache Tomcat6`
- `Apache Tomcat7 < 7.0.100`
- `Apache Tomcat8 < 8.5.51`
- `Apache Tomcat9< 9.0.31`

如果哪个小伙伴的服务器版本不幸在列的话，赶紧抓紧时间修复吧，别存在侥幸心理。