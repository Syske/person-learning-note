tags: [#spring boot, #maven]

# 1、创建Maven项目
- 按照下面的步骤
![](https://images2018.cnblogs.com/blog/1077694/201807/1077694-20180730222542907-1030031109.png)
![](https://images2018.cnblogs.com/blog/1077694/201807/1077694-20180730222557879-1441267785.png)
![](https://images2018.cnblogs.com/blog/1077694/201807/1077694-20180730222607387-1095391968.png)
![](https://images2018.cnblogs.com/blog/1077694/201807/1077694-20180730222618148-2063604681.png)
- 项目创建完成后的目录结构
![](https://images2018.cnblogs.com/blog/1077694/201807/1077694-20180730222632056-1092370702.png)


# 2、 参照Spring boot官方文档修改pom.xml
- 修改 maven编译的jdk版本

![](https://images2018.cnblogs.com/blog/1077694/201807/1077694-20180730222733022-1987579903.png)

- 将spring boot设置为 parent

![](https://images2018.cnblogs.com/blog/1077694/201807/1077694-20180730222805583-1640891201.png)


- 修改后的pom
```xml
<?xml version="1.0" encoding="UTF-8"?>

<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>io.github.syske</groupId>
  <artifactId>firstspringbootdome</artifactId>
  <version>1.0-SNAPSHOT</version>
  <packaging>jar</packaging>
  
<!-- 这里将spring boot设置为父类 -->
  <parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>2.0.3.RELEASE</version>
  </parent>

  <name>firstspringbootdome Maven Webapp</name>
  <!-- FIXME change it to the project's website -->
  <url>http://www.example.com</url>

<!-- 这里要讲maven的编译的版本改为和我们环境对应的1.8 -->
  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.source>1.8</maven.compiler.source>
    <maven.compiler.target>1.8</maven.compiler.target>
  </properties>

  <dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>4.11</version>
      <scope>test</scope>
    </dependency>
    
<!-- 这里配置spring的jar包 -->
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
  </dependencies>

  <build>
    <finalName>firstspringbootdome</finalName>
    <!-- 这里设置Spring boot的插件 -->
      <plugins>
        <plugin>
          <groupId>org.springframework.boot</groupId>
          <artifactId>spring-boot-maven-plugin</artifactId>
        </plugin>
      </plugins>
  </build>
</project>


```

# 3、 创建Application

- 创建java文件夹，并设置为resource root

![](https://images2018.cnblogs.com/blog/1077694/201807/1077694-20180730223122579-1304577635.png)


```java
package io.github.syske;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class FirstSpringBootDome {
    public static void main(String[] args) {
        SpringApplication.run(FirstSpringBootDome.class, args);
    }

}
```

# 4、创建Controller

- 这里需要留意的是controller和Application的相对路径

```java
package io.github.syske.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class HelloController {
    @RequestMapping("/hello")
    @ResponseBody
    public String hello() {
        return "hello Spring boot";
    }
}
```
- 创建完后的项目结构
![](https://images2018.cnblogs.com/blog/1077694/201807/1077694-20180730223107373-505337335.png)



# 5、运行测试

![](https://images2018.cnblogs.com/blog/1077694/201807/1077694-20180730223214691-485365474.png)



# 6、打包
![](https://images2018.cnblogs.com/blog/1077694/201807/1077694-20180730223228646-1708303611.png)
![](https://images2018.cnblogs.com/blog/1077694/201807/1077694-20180730223241115-1689043832.png)
![](https://images2018.cnblogs.com/blog/1077694/201807/1077694-20180730223249100-197018426.png)


# 总结

- 我在踩坑的过程中发现，setting的设置可能会导致找不到类的错误，具体错误如下，仅供参考，楼主最后通过修改setting成功修复
```sh
java.lang.NoClassDefFoundError: ch/qos/logback/core/joran/spi/JoranException
```


