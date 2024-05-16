tags: [#springboot, #日志]

### 1、默认实现的日志配置
Spring boot默认已经集成了logging，同时也是默认开启的，如果想根据自己的需求对日志进行配置，方法很简单——只需要在配置文件中进行相应设置，这里提供我自己的配置如下(配置文件采用了yml)：

```yml
logging:
  #指定日志的等级，可以对不同包采用不同的等级，比如如下配置就是将root的等级设置为info，将com.example设置为debug
  level: {root: info,com.example: debug}
  #file是设置日志的输出的路径，这里需要注意的是file和path属性只能选一个，不能同时存在
  file: log.log
```
- 更多配置文件请参考Spring boot的官方文档，说明很详细

### 2、自定义日志配置

- 使用默认的日志在实际开发中会存在很多问题，比如备份文件名称无法自动重命名、各个等级的日志被放在一个文件中等，所以实际开发中为了更好满足我们的需求，我们一般都会自定义采用配置的方式，日志自定配置步骤如下

#### 2.1 修改spring-boot-starter的dependency

```xml
<dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
            <exclusions>
                <exclusion>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-starter-logging</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
```
添加我们需要自定义的logging的dependency，这里用的是log4j2
```xml
 <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-log4j2</artifactId>
        </dependency>
```
修改之后我们就算移除了默认的日志配置，下面就可以自定义配置了

#### 2.2 自定义配置文件log4j2.xml

- Spring boot对自定义配置文件的名称是有要求的，对Login4j2而言必须为log4j2-spring.xml or log4j2.xml
- 关于配置文件中的参数，详细参考官方文档

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <appenders>
        <!-- 控制台输出 -->
        <console name="Console" target="SYSTEM_OUT">
            <PatternLayout pattern="%d{HH:mm:ss.SSS} %-5level %class %L %M - %msg%n"/>
        </console>

        <!-- fileName：输出路径  filePattern：命名规则 -->
        <RollingFile name="all" fileName="logs/allOut.log"
                     filePattern="logs/$${date:yyyy-MM-dd}/allOut-%d{yyyy-MM-dd}-%i.log">
            <Filters>
                <ThresholdFilter level="all" onMatch="ACCEPT" onMismatch="DENY"/>
            </Filters>
            <!-- 输出格式 -->
            <PatternLayout pattern="%d{HH:mm:ss.SSS} %-5level %class{36} %L %M - %msg%n"/>
            <Policies>
                <!-- SizeBasedTriggeringPolicy单个文件的大小限制 -->
                <SizeBasedTriggeringPolicy size="2 MB"/>
            </Policies>
            <!-- DefaultRolloverStrategy同一个文件下的最大文件数 -->
            <DefaultRolloverStrategy max="50"/>
        </RollingFile>

        <RollingFile name="err" fileName="logs/err.log"
                     filePattern="logs/$${date:yyyy-MM-dd}/err-%d{yyyy-MM-dd}-%i.log">
            <Filters>
                <ThresholdFilter level="error" onMatch="ACCEPT" onMismatch="DENY"/>
            </Filters>
            <!-- 输出格式 -->
            <PatternLayout pattern="%d{HH:mm:ss.SSS} %-5level %class{36} %L %M - %msg%xEx%n"/>
            <Policies>
                <!-- SizeBasedTriggeringPolicy单个文件的大小限制 -->
                <SizeBasedTriggeringPolicy size="10MB"/>
            </Policies>
            <!-- DefaultRolloverStrategy同一个文件下的最大文件数 -->
            <DefaultRolloverStrategy max="50"/>
        </RollingFile>
    </appenders>

    <loggers>
        <!--过滤掉spring无用的debug信息-->
        <logger name="org.springframework" level="error"></logger>

        <root level="debug">
            <appender-ref ref="Console"/>
            <appender-ref ref="all"/>
            <appender-ref ref="err"/>
        </root>
    </loggers>

</configuration>
```