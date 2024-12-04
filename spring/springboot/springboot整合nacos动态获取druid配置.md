# springboot整合nacos动态获取druid配置

## 前言

是不是还有好多小伙伴不知道`nacos`是啥？其实，我也是从上一次`nacos`爆出漏洞，才知道还有`nacos`这个组件，而且目前这个组件应用很广泛，很多项目都用它来做配置中心和注册中心，今天我们分享的内容就是`nacos`作为配置中心使用的一个小`demo`。

在完成这个小`demo`之前，我查了好多示例和博客，但是都没有找到符合我需求的，所以走了好多弯路，才让这个`demo`完整的跑起来，现在我们就来看下如何实现`springboot`+`nacos`+`druid`动态获取数据库配置信息。

今天的`demo`内容比较多，如果你恰好在学习`nacos`，认真看完，肯定会有收获。

## 正文

### nacos是什么

在开始讲解这个`demo`之前，我们先看下什么是`nacons`。`nacos`是阿里巴巴的一个开源项目，官网给它的定义是：

> 一个更易于构建云原生应用的动态服务发现、配置管理和服务管理平台。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228145418.png)

也就是说，它可以实现动态的服务发现，能够实现配置管理，可以作为服务管理平台，简介就到这里，更多信息直接去看官方文档：

```
https://nacos.io/zh-cn/docs/what-is-nacos.html
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228145802.png)

### 如何使用nacos

了解它的目的，主要还是为了在我们的项目中使用它，所以我们直接来看如何使用它。

#### 下载nacos

进入官网，点击前往`github`，你需要去`nacos`的`GitHub`发布列表中下载，不清楚的小伙伴直接访问下面的网址进入下载页：

```
https://github.com/alibaba/nacos/releases
```

最新版本是`2.0.0-BETA`，是个测试版本，目前最新的稳定版本是`1.4.0`，本次示例也是这个版本![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228150337.png)

点击`Assets`，选择`.zip`文件，然后应该就开始下载了，下载可能比较慢

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228150634.png)

#### 解压zip文件

`zip`文件结构是这样的，直接解压就行，也不需要配置环境变量

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228151253.png)

#### 运行启动nacos服务

进入`nacos`的`bin`目录，打开`cmd`窗口，`linux`打开`sh`窗口，执行如下命令：

`windos`环境:

```shell
cmd startup.cmd -m standalone
```

`linux`环境：

```shell
sh startup.sh -m standalone
```

如果您使用的是ubuntu系统，或者运行脚本报错提示[[符号找不到，可尝试如下运行：

```shell
bash startup.sh -m standalone
```

其中，`standalone`表示单机模式，如果不加这个参数，默认是以集群模式运行的（`cluster`）

#### 关闭nacos服务

##### Linux/Unix/Mac

```sh
sh shutdown.sh
```

##### Windows

```sh
cmd shutdown.cmd
```

或者双击shutdown.cmd运行文件。

#### 服务注册&发现和配置管理

这里的内容，我直接`copy`的官网文档，大概看一下就可以了，和示例关系不大。下面的命令就是通过`http`接口的方式，注册服务、发现服务、发布配置和获取配置。

##### 服务注册

```
curl -X POST 'http://127.0.0.1:8848/nacos/v1/ns/instance?serviceName=nacos.naming.serviceName&ip=20.18.7.10&port=8080'
```

##### 服务发现

```
curl -X GET 'http://127.0.0.1:8848/nacos/v1/ns/instance/list?serviceName=nacos.naming.serviceName'
```

##### 发布配置

```
curl -X POST "http://127.0.0.1:8848/nacos/v1/cs/configs?dataId=nacos.cfg.dataId&group=test&content=HelloWorld"
```

##### 获取配置

```
curl -X GET "http://127.0.0.1:8848/nacos/v1/cs/configs?dataId=nacos.cfg.dataId&group=test"
```

#### 修改`nacos`服务端配置信息

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228153436.png)

这个配置文件里面还可以设置`nacos`的数据存储，默认的数据存储是`derby`，这是个完全用java编写的数据库，非常小巧，核心部分*derby*.jar只有2M，所以既可以做为单独的数据库服务器使用，也可以内嵌在应用程序中使用。如果要启用`mysql`，可以修改相关配置文件，进行启用：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228153637.png)

#### 访问nacos服务

如果没有修改`nacos`的配置，直接浏览器打开如下地址即可，如果修改了端口，需要把端口改成你修改的端口：

```
http://127.0.0.1:8848/nacos
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228155254.png)

默认用户名和密码都是`nacos`，登陆成功之后就可以发布你的配置信息了。

#### 发布配置信息

因为我已经加过配置信息了，如果是第一次访问，应该是没有配置信息的。点击右边的`+`号进行创建

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228155428.png)

输入`data-id`，必须唯一，类似于主键，不能重复；选择配置格式，这里我选择`properties`；然后点击发布，一个配置信息就发布成功了

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228160100.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228160246.png)

我们现在来测试下，我们用如下命令：

```sh
curl -X GET "http://127.0.0.1:8848/nacos/v1/cs/configs?dataId=nacos-test-demo&group=DEFAULT_GROUP"
```

返回结果：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228160639.png)

### springboot整合nacos和druid

这里才是今天的重点，但是我还是想直接上代码，需要解释的地方，我会补充说明的。

#### 创建springboot项目

引入如下依赖：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jdbc</artifactId>
    <exclusions>
        <exclusion>
            <groupId>com.zaxxer</groupId>
            <artifactId>HikariCP</artifactId>
        </exclusion>
    </exclusions>
</dependency>

<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>druid-spring-boot-starter</artifactId>
    <version>1.1.21</version>
</dependency>

<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <scope>runtime</scope>
</dependency>
```

除了`spring-boot-start-web`外，我们引入了`spring-cloud-starter-alibaba-nacos-config`，这个是`nacos`的依赖，剩下的就是数据库哈数据源相关的依赖了。



#### 增加nacos配置文件

```yaml
spring:
  cloud:
    nacos:
      config:
        server-addr: 127.0.0.1:8848
        prefix: springboot-nacos-demo
        file-extension: yaml
        username: nacos
        password: nacos

  profiles:
    active: dev
```

其中，`server-addr`是`nacos`的服务地址，如果要修改服务端口的话，可以进入`conf`找到`application.properties`进行修改，详细修改过程看前面的内容；

`prefix`是`nacos`服务中配置的`data-id`的前缀，和`file-extension`、`profiles.active`最终组合成`data-id`；

`file-extension`表示文件扩展名，目前支持`propeties`、`YAML`，因为`springboot`目前只支持这两种配置文件，当然`nacos`本身支持多种配置文件：`TEXT`、`JSON`、`XML`、`YAML`、`HTML`、`Properties`；

`username`是`nacos`服务端的登陆用户名；`password`是`nacso`服务端的登陆密码。`profiles`是`springboot`的配置，这里不讲。



#### 发布数据源配置

我这里的数据源密码是加密的，如果你不想加密，删除`connection-properties`配置，`password`改成明文密码就可以了，如果你也想加密，可以参考我之前发过的文章：[spring boot基于DRUID数据源密码加密及数据源监控实现](https://www.cnblogs.com/caoleiCoding/p/12000926.html)

```yaml
spring:
  #阿里巴巴druid数据源配置
  datasource:
    type: com.alibaba.druid.pool.DruidDataSource
    sql-script-encoding: utf-8
    druid:
      driver-class-name: com.mysql.cj.jdbc.Driver
      username: root
      url: jdbc:mysql://127.0.0.1:3307/userlogin?characterEncoding=UTF-8&zeroDateTimeBehavior=convertToNull&allowMultiQueries=true&serverTimezone=Asia/Shanghai
      password: Y2YOft/vPjw/JFPkevqZZKi8pCHu5ambR2ivSxgipTbL76pOoxNw3Un5Hcarbe9AqUImr+wS7YI6TjJZOVYjzA==
      connection-properties: config.decrypt=true;config.decrypt.key=MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJI/xqbyvpVttxfAKulKeSTIb7tZAGaFcPyTnE2r7AHTQ8kOnqKXDda4u59umt9XBFxi7db28KxeVooB138zuRUCAwEAAQ==
      filter:
        config:
          enabled: true
      # 连接池的配置信息
      # 初始化时建立物理连接的个数
      initial-size: 3
      # 连接池最小连接数
      min-idle: 3
      # 连接池最大连接数
      max-active: 20
      # 获取连接时最大等待时间，单位毫秒
      max-wait: 60000
      # 申请连接的时候检测，如果空闲时间大于timeBetweenEvictionRunsMillis，执行validationQuery检测连接是否有效。
      test-while-idle: true
      # 既作为检测的间隔时间又作为testWhileIdel执行的依据
      time-between-connect-error-millis: 60000
      # 销毁线程时检测当前连接的最后活动时间和当前时间差大于该值时，关闭当前连接
      min-evictable-idle-time-millis: 30000
      # 用来检测连接是否有效的sql 必须是一个查询语句
      # mysql中为 select 'x'
      # oracle中为 select 1 from dual
      validationQuery: select 'x'
      # 申请连接时会执行validationQuery检测连接是否有效,开启会降低性能,默认为true
      test-on-borrow: false
      # 归还连接时会执行validationQuery检测连接是否有效,开启会降低性能,默认为true
      test-on-return: false
      # 是否缓存preparedStatement,mysql5.5+建议开启
      pool-prepared-statements: true
      # 当值大于0时poolPreparedStatements会自动修改为true
      max-pool-prepared-statement-per-connection-size: 20
      # 合并多个DruidDataSource的监控数据
      use-global-data-source-stat: false
      # 配置扩展插件
      #监控统计拦截的filters
      filters: stat,wall,slf4j
      # 通过connectProperties属性来打开mergeSql功能；慢SQL记录
      connect-properties: druid.stat.mergeSql=true;druid.stat.slowSqlMillis=5000
      # 定时输出统计信息到日志中，并每次输出日志会导致清零（reset）连接池相关的计数器。
      time-between-log-stats-millis: 300000
      # 配置DruidStatFilter
      web-stat-filter:
        enabled: true
        url-pattern: '/*'
        exclusions: '*.js,*.gif,*.jpg,*.bmp,*.png,*.css,*.ico,/druid/*'
      # 配置DruidStatViewServlet
      stat-view-servlet:
        # 是否启用StatViewServlet（监控页面）默认值为false（考虑到安全问题默认并未启动，如需启用建议设置密码或白名单以保障安全）
        enabled: true
        url-pattern: '/druid/*'
        # IP白名单(没有配置或者为空，则允许所有访问)
        allow: 127.0.0.1,192.168.0.1
        # IP黑名单 (存在共同时，deny优先于allow)
        deny: 192.168.0.128
        # 禁用HTML页面上的“Reset All”功能
        reset-enable: false
        # 登录名
        login-username: admin
        # 登录密码
        login-password: admin
```

这些配置文件发布到`nacos`中：

`data-id`我前面说了，已经很清楚了。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228161945.png)



#### 自定义DruidDatasouceWrapper

`DruidDatasouceWrapper`要继承`DruidDataSource`

`RefreshScope`的作用是实现配置、实例热加载，也就是我们重写修改配置信息后，`spring`会销毁当前类的实例，然后重新创建一个新的实例放到容器中，也是实现数据源配置实时更新的关键

```java
import com.alibaba.druid.pool.DruidDataSource;
import org.springframework.beans.factory.InitializingBean;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.context.annotation.Configuration;

/**
 * @program: springboot-nacos-demo
 * @description:
 * @author: syske
 * @create: 2021-02-28 11:33
 */
@Configuration
@RefreshScope
public class DruidDataSourceWrapper extends DruidDataSource implements InitializingBean {
    @Value("${spring.datasource.druid.url}")
    private String url;
    @Value("${spring.datasource.druid.username}")
    private String username;
    @Value("${spring.datasource.druid.password}")
    private String password;
    @Value("${spring.datasource.druid.driver-class-name}")
    private String driverClassName;
    @Value("${spring.datasource.druid.connection-properties}")
    private String connectionProperties;

    private String passwordCallbackClassName;

    public void setMaxWait(int maxWait) {
        this.maxWait = maxWait;
    }

    public void setTimeBetweenEvictionRunsMillis(long timeBetweenEvictionRunsMillis) {
        this.timeBetweenEvictionRunsMillis = timeBetweenEvictionRunsMillis;
    }

    public void setMinEvictableIdleTimeMillis(long minEvictableIdleTimeMillis) {
        this.minEvictableIdleTimeMillis = minEvictableIdleTimeMillis;
    }

    @Override
    public void setUrl(String url) {
        this.url = url;
    }

    @Override
    public void setDriverClassName(String driverClassName) {
        this.driverClassName = driverClassName;
    }

    @Override
    public void setConnectionProperties(String connectionProperties) {
        this.connectionProperties = connectionProperties;
    }

    @Override
    public void setPasswordCallbackClassName(String passwordCallbackClassName) {
        this.passwordCallbackClassName = passwordCallbackClassName;
    }

    @Override
    public void afterPropertiesSet() throws Exception {
        // 如果未找到前缀“spring.datasource.druid”JDBC属性，将使用“Spring.DataSource”前缀JDBC属性。
        super.setUrl(url);
        super.setUsername(username);
        super.setPassword(password);
        super.setDriverClassName(driverClassName);
        super.setInitialSize(initialSize);
        super.setMinIdle(minIdle);
        super.setMaxActive(maxActive);
        super.setMaxWait(maxWait);
        super.setTimeBetweenEvictionRunsMillis(timeBetweenEvictionRunsMillis);
        super.setMinEvictableIdleTimeMillis(minEvictableIdleTimeMillis);
        super.setValidationQuery(validationQuery);
        super.setTestWhileIdle(testWhileIdle);
        super.setTestOnBorrow(testOnBorrow);
        super.setTestOnReturn(testOnReturn);
        super.setPoolPreparedStatements(poolPreparedStatements);
        super.setMaxPoolPreparedStatementPerConnectionSize(maxPoolPreparedStatementPerConnectionSize);
        super.setConnectionProperties(connectionProperties);
        super.setDbType(dbType);
        super.setPasswordCallbackClassName(passwordCallbackClassName);
    }
}
```

#### 配置nacos

这里关键的配置就一个，`EnableAutoConfiguration`启动`springboot`的自动自动配置，下面的方法是在初始化的时候，创建数据源实例，同样也启用了热加载

```java
import com.alibaba.druid.pool.DruidDataSource;
import io.github.syske.springbootnacosdemo.druidconfig.DruidDataSourceWrapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Nacos配置
 */
@EnableAutoConfiguration
@Configuration
public class NacosConfigConfiguration {
    private final Logger LOGGER = LoggerFactory.getLogger(NacosConfigConfiguration.class);

    @Bean(initMethod = "init")
    @ConditionalOnMissingBean
    @RefreshScope
    public DruidDataSource dataSource() {
        LOGGER.info("Init DruidDataSource");
        return new DruidDataSourceWrapper();
    }
}
```

#### 测试

到这里，核心代码就全部完了，我们启动`demo`测试下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228163300.png)

如上日志信息，我们可以看到`springboot`启动的时候加载了`nacos`发布的配置信息，然后还会有数据源初始成功的提示信息：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228163557.png)

然后我们写一个`controller`测试下：

```java
@RestController
public class TestController {

    @Autowired
    private DruidDataSourceWrapper dataSourceWrapper;

    @RequestMapping("/test")
    public String testDruid() throws SQLException {
        DruidPooledConnection connection = dataSourceWrapper.getConnection();
        Statement statement = connection.createStatement();
        ResultSet  resultSet = statement.executeQuery("SELECT * from user;");
        System.out.println(resultSet);
        while(resultSet.next()){
            System.out.println(resultSet.getString("username"));
        }
        return "hello druid";
    }
}
```

我这里有两个数据库，都有`user`表，我现在的数据库地址配的是`userlogin`这个库，我先访问下，后台打印信息如下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228164430.png)

然后我们将数据库改成`my_db_test`，然后发布配置，再次访问：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228164752.png)

配置发布完成后，`springboot`后台已经打印了配置更新的日志，说明配置已经被刷新：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228164920.png)

然后我们再访问：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228165024.png)

从日志记录来看，我们再次访问的时候，数据源重新初始化，当然最后打印的结果也和我们预期的一样，打印了我们刚加的配置对应的数据表里面的用户信息。当然再改回，也是可以的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228164024.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228165314.png)

再次访问：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210228165437.png)

而且后台也有数据库`url`修改的提示信息



## 结语

好了，今天的内容就到这里吧，本次实例比较完整的介绍了`springboo` + `nacos` + `druid`实现动态获取数据库配置的构建过程，同时也比较详细的说明了`nacos`的相关配置，我觉得很完美，至少我很满意。关于这个`demo`，我上周就在弄，但是项目一直跑不起来，也没有参考的样例，所以就搁置着，今天总算搞定了，很奈斯哦。下面是`demo`的完整代码获取地址：

```
https://github.com/Syske/learning-dome-code/tree/dev/springboot-nacos-demo
```

