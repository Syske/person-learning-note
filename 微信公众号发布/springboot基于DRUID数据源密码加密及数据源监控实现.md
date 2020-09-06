# spring boot基于DRUID数据源密码加密及数据源监控实现

##### 前言

随着需求和技术的日益革新，spring boot框架是越来越流行，她也越来越多地出现在我们的项目中，当然最主要的原因还是因为spring boot构建项目实在是太爽了，构建方便，开发简单，而且效率高。今天我们并不是来专门学习spring boot项目的，我们要讲的是数据源的加密和监控，监控到好说，就是不监控也没什么问题，但是数据源加密却涉及到我们的系统安全。对于平时的学习测试，我们在项目中配置数据库明文密码是没什么问题的，因为我们的数据不重要，也就无所谓，但是在现实环境下的生产平台，配置明文密码极有可能会造成我们数据库密码泄露，最终导致我们的生产数据泄露，这也就体现了生产环境数据源加密的必要性。下面我们就来看看如何实现数据源加密吧。

##### 创建spring boot项目

创建过程就不赘述了，下面是我的项目依赖：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.2.1.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>io.githu.syske</groupId>
    <artifactId>druid-datasouce-decrypt</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>druid-datasouce-decrypt</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>1.8</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.mybatis.spring.boot</groupId>
            <artifactId>mybatis-spring-boot-starter</artifactId>
            <version>2.1.1</version>
        </dependency>

        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <scope>runtime</scope>
        </dependency>

        <!-- 阿里巴巴druid -->
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>druid-spring-boot-starter</artifactId>
            <version>1.1.10</version>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
            <exclusions>
                <exclusion>
                    <groupId>org.junit.vintage</groupId>
                    <artifactId>junit-vintage-engine</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>
```

如果你的数据库是Oracle，那么你要把mysql的数据库驱动替换成Oracle驱动

##### 修改spring boot项目配置信息

```yaml
server:
  port: 8083
```

我采用的是yaml的方式，然后启动你的项目，因为没有controller和其他的代码，所以没什么效果，但是项目可以正常启动。

##### 加密数据源密码，创建publickey

这里没什么好讲的，我直接放代码：

```java
import org.junit.Test;

/**
 * @program: druid-datasouce-decrypt
 * @description:
 * @author: liu yan
 * @create: 2019-12-02 18:34
 */
public class DBencrydtTest {
    @Test
    public void test() {
        String[] args = {"root"};
        try {
            com.alibaba.druid.filter.config.ConfigTools.main(args);
        } catch (Exception e) {

        }

        System.out.println();
    }
}
```

需要说明的是，args数组中放置的是密码，直接运行上面的代码，你会看到控制台会打印如下信息：

```shell
privateKey:MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAqboz+iNXPv1jgKAhDW7W+L/NwqG6GDTo49BjmlMg3WxBg4w9h4RC3oRO40EOjL7+DtEBBlCZ6OHZfZWKh17FmwIDAQABAkA/azwQszPebX/IiAzRoCDjQYf4ucV3Vg3PUgZlm7okAbsXrxz2xrdnM8Er08YKm3vUOmWQmSvaOI3CqdrK1f2BAiEA4XbEkCOxWVxbDLihyudClvrgLbZZrqw2SDF4dsfgXMCIQDAtvMeJiXlGQBxFr/ci0r99FiYUeag/ZFwOjyhIzWBOQIgYg3bEqzTNn/aAUBS7QGCjlLxKDBD//7/L7nRwI9O6k0CIQCdBnUiY8MM4UpS206JzZXVR3vI4TMiinovD8THJ4E5QQIgRM1QlD1PG5YTxBxZMrLm2weBxsqXhvdJuTc1GXmoUxg=
publicKey:MFwwDQYJKoZIhvcNAWFS4dfBAKm6M/ojVz79Y4CgIQ1u1vi/zcKhuhg06OPQY5pTIN1sQYOMPYeEQt6ETuNBDoy+/g7RAQZQmejh2X2ViodexZsCAwEAAQ==
password:O9JBjc86r9IhEoIE6jevJtgsgCXZAKCWH2UtO0tbG62zqIK5G5qJOCm1u9ju+lnno15vmq+TO5WqEWGzvkDNGg==
```

privateKey是你的私钥，publicKey是公钥，password就是你加密后的密码。我们用到的配置有两个，一个是公钥，一个是密码，配置公钥的原因是要通过公钥进行解密。将如上信息保存好，后面再spring boot的配置中要用到。

##### 增加数据源相关配置

增加数据源配置信息：

```yaml
# 阿里巴巴druid数据源配置
spring:
  datasource:
  # 数据源驱动类型，这里是druid
    type: com.alibaba.druid.pool.DruidDataSource
    # sql脚本编码
    sql-script-encoding: utf-8
    druid:
    # 驱动的类名
      driver-class-name: com.mysql.cj.jdbc.Driver
      # 数据库连接密码
      username: root
      # 数据库地址
      url: jdbc:mysql://127.0.0.1:3307/spring?characterEncoding=UTF-8&zeroDateTimeBehavior=convertToNull&allowMultiQueries=true&serverTimezone=Asia/Shanghai
      # 这里配置的是前面我们生成的密码
      password: Y2YOft/vPjw/JFPkevqZZKi8pCHu5ambR2ivSxgipTbL76pOoxNw3Un5Hcarbe9AqUImr+wS7YI6TjJZOVYjzA==
      # 这里设置连接配置，key配置的是我们前面生成的publicKey
      connection-properties: config.decrypt=true;config.decrypt.key=MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJI/xqbyvpVttxfAKulKeSTIb7tZAGaFcPyTnE2r7AHTQ8kOnqKXDda4u59umt9XBFxi7db28KxeVooB138zuRUCAwEAAQ==
      filter:
        config:
        # 启用druid的拦截器
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

上面备注已经很详细了，这里要强调的有两个地方，一个是key那里配置的是publicKey，不要配错了，一个是要注意 validationQuery这里mysql和Oracle是不一样的，当然你要可以移除该配置。

上面还加了数据源监控的配置信息，注释已经够详细了。以上配置完成后就可以启动你的项目了，如果没有报错，那说明你的配置没有问题，如果启动的时候报错，说明你的配置有问题。

项目启动后，要进入druid数据源监控页面，只需要输入如下你的项目地址+/druid即可，比如我的地址：

```
http://localhost:8083/druid
```

然后输入你在配置信息里面加入的用户名和密码，你就可以看见监控页面了，如果要查看sql相关监控信息，你还要完善自己的项目，引入mybatis，配置你的sql。

##### 结语

至此，我们的项目就已经完成了，根据以上过程，我们发下数据源加密和监控的核心是要添加正确的配置信息。如果在实际开发过程中发下错误，最主要的还是要检查我们的配置是否正确。