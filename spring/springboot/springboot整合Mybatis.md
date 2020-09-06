
代码中用到的连接池为阿里巴巴的druid

### 1、引入依赖

```
<!-- 数据库连接配置 -->
        <!-- mysql数据库连接jar包 -->
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>5.1.46</version>
        </dependency>
        
        <!-- 数据库jdbc驱动 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-jdbc</artifactId>
            <optional>true</optional>
        </dependency>

        <!-- https://mvnrepository.com/artifact/com.alibaba/druid -->
        <!-- 阿里巴巴druid -->
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>druid-spring-boot-starter</artifactId>
            <version>1.1.10</version>
        </dependency>
        
        <!-- mybatis -->
        <dependency>
            <groupId>org.mybatis.spring.boot</groupId>
            <artifactId>mybatis-spring-boot-starter</artifactId>
            <version>1.3.2</version>
        </dependency>

```

### 2、配置datasource

> 配置文件采用的yaml，如果不懂得话可以看一下Spring boot官方文档

```
#阿里巴巴druid数据源配置
spring:
  datasource:
    druid:
            #监控统计拦截的filters
            filters: stat
            driver-class-name: com.mysql.jdbc.Driver
            #基本属性
            url: jdbc:mysql://localhost:3306/test?characterEncoding=UTF-8&amp;useSSL=false
            username: root
            password: root
mybatis:
  #mpper路径，这里需要根据你具体的路径配置
  mapper-locations: classpath:mybatis/mapper/*.xml
  #mybatis配置文件路径，这里需要根据你具体的路径配置
  config-location: classpath:mybatis/mybatis-config.xml
  #MybatisMapper映射路径
  type-aliases-package: io.github.syske.springboot31.entity

```

### 3、entity

```

public class User {
    // 用户id，采用UUID
    private String id;
    // 用户名
    private String username;
    // 用户昵称
    private String nickName;
    // 用户密码，采用MD5加密
    private String password;
    // 手机号
    private String phone;
    // 地址
    private String addr;
    // 注册日期
    private String rdate;
    // 用户状态,1-可用，0-禁用
    private String status;


    public User() {
        super();
    }


    //getter setter方法省略了
    
}
```

### 4、DAO

```
import java.util.List;

public interface UserDAO {
    /**
     * 查询所有用户
     * @return
     */
    List<User> listUsers();
}

```

### 5、Usermapper.xml

```
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="io.github.syske.springboot31.dao.UserDAO">

    <select id="listUsers" resultType="user">
        select *  from user
    </select>

</mapper>

```

### 6、Service和ServiceImpl

- 接口

```

import java.util.List;

public interface UserService {
    /**
     * 查询所有用户
     *
     * @return
     */
    List<User> listUsers();
}

```
- 服务接口实现类
```

import javax.annotation.Resource;
import java.util.List;

@Service
public class UserServiceImpl implements UserService {

    @Resource
    private UserDAO userDAO;

    @Override
    public List<User> listUsers() {
        return userDAO.listUsers();
    }
}

```

### 7、测试类

```
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

import javax.annotation.Resource;
import javax.sql.DataSource;
import java.util.List;

@RunWith(SpringRunner.class)
@SpringBootTest
public class SpringBoot31ApplicationTests {


    @Resource
    private UserService userService;


    @Test
    public void listuser() {
        List<User> userList = userService.listUsers();
        for(User user : userList) {
            System.out.println(user);
        }
    }

}
```

- 本次示例中mybatis配置文件为空：
```
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <!-- 方便后续设定mybatis的配置-->
</configuration>
```

- 这里要补充一下，需要在Spring boot启动类中标注mapper路径

```
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.Banner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Configuration;

@Configuration
@SpringBootApplication
//指定mapper的扫描路径
@MapperScan("io.github.syske.springboot31.dao")
public class SpringBoot31Application {

    public static void main(String[] args) {

        //SpringApplication.run(SpringBoot31Application.class, args);
        SpringApplication application = new SpringApplication(SpringBoot31Application.class);
        //关闭banner，也可以通过在resouces文件夹下添加banner.txt替换banner，banner生成网站
        // http://patorjk.com/software/taag/#p=testall&h=0&f=Chiseled&t=syske
        application.setBannerMode(Banner.Mode.OFF);
        application.run(args);
    }
}

```

- 从上面可以看出来，核心的点如下
- - 引入jar包
- - 配置datasource及mybatis
- - 指定mapper(DAO)的路径
- 其余的和我们在ssm中基本没有区别
