### 1、mybatis主配置（mybatis-config.xml）

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE configuration
  PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
  "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
<properties resource="jdbc.properties"></properties>
	<environments default="development">
		<environment id="development">
			<transactionManager type="JDBC" />
			<!-- 配置数据库连接信息 -->
			<dataSource type="POOLED">
				<property name="driver" value="${driver}" />
				<property name="url"
					value="${url}" />
				<property name="username" value="${username}" />
				<property name="password" value="${password}" />
			</dataSource>
		</environment>
	</environments>
	<mappers>
		<mapper resource="com/javasm/mapper/UserMapper.xml" />
	</mappers>
</configuration>
```

### 2、jdbc.properties文件配置

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd" >
<mapper namespace="com.javasm.dao.UserDao">
	<select id="listUsers" resultType="com.javasm.entity.User">
		SELECT * FROM user
	</select>

	<select id="getUser" parameterType="String"
		resultType="com.javasm.entity.User">
		select * from user where id=#{id}
	</select>
	<update id="updateUser">
		update user set username =
		#{userName},sex=#{sex},phone=#{phone},password=#{password},address =
		#{address},birth=#{birth} where id=#{id}
	</update>

	<insert id="insertUser">
		insert into user
		(id,username,sex,phone,password,address,birth)
		values
		(#{id},#{userName},#{sex},#{phone},#{password},#{address},#{birth})
	</insert>

	<delete id="deleteUser" parameterType="String">
		DELETE FROM user WHERE
		id=#{id}

	</delete>
</mapper>
```

### 4、数据库对象
```
package com.javasm.entity;
/**
 * 
 *TODO 用户表实体类
 * @author CaoLei 2018年6月26日上午10:50:12
 * ManagerUser
 */
public class User {
    // id
    private String id;
    // 用户名
    private String userName;
    // 密码
    private String password;
    // 电话
    private String phone;
    // 地址
    private String address;
    // 生日
    private String birth;
    // 性别
    private String sex;
    
    
    
    public User() {
        super();
    }
    public User(String id, String userName, String pssword, String phone,
            String address, String birth, String sex) {
        super();
        this.id = id;
        this.userName = userName;
        this.password = pssword;
        this.phone = phone;
        this.address = address;
        this.birth = birth;
        this.sex = sex;
    }
    public String getId() {
        return id;
    }
    public void setId(String id) {
        this.id = id;
    }
    public String getUserName() {
        return userName;
    }
    public void setUserName(String userName) {
        this.userName = userName;
    }
    public String getPassword() {
        return password;
    }
    public void setPssword(String password) {
        this.password = password;
    }
    public String getPhone() {
        return phone;
    }
    public void setPhone(String phone) {
        this.phone = phone;
    }
    public String getAddress() {
        return address;
    }
    public void setAddress(String address) {
        this.address = address;
    }
    public String getBirth() {
        return birth;
    }
    public void setBirth(String birth) {
        this.birth = birth;
    }
    public String getSex() {
        return sex;
    }
    public void setSex(String sex) {
        this.sex = sex;
    }
}

```

### 5、DAO层

```
package com.javasm.dao;

import java.util.List;

import com.javasm.entity.User;

/**
 * 
 *TODO 
 * @author CaoLei 2018年6月26日上午10:53:37
 * UserDao
 */
public interface UserDao {
    List<User> listUsers();
    
    User getUser(String id);
    
    int insertUser(User user);
    
    int deleteUser(String id);
    
    int updateUser(User user);
}

```

### 6、创建SqlSessionFactory

```
package test;

import java.io.IOException;
import java.io.Reader;
import java.util.List;
import java.util.Random;
import java.util.UUID;

import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;

import com.javasm.dao.UserDao;
import com.javasm.entity.User;
import com.javasm.utils.RandomString;
import com.javasm.utils.UUIDUtil;

public class MainTest {
    // mybatis的配置文件
    private static final String resource = "mybatis-config.xml";
    private static UserDao mapper;
    private static SqlSession session;
    static {

        // 使用MyBatis提供的Resources类加载mybatis的配置文件（它也加载关联的映射文件）
        try {
            Reader reader = Resources.getResourceAsReader(resource);
            SqlSessionFactory sessionFactory = new SqlSessionFactoryBuilder()
                    .build(reader);
            // 创建能执行映射文件中sql的sqlSession
            session = sessionFactory.openSession();
            // 获取dao实现的映射
            mapper = session.getMapper(UserDao.class);
            // 执行查询返回一个唯一user对象的sql
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

    }

    public static void main(String[] args) throws IOException {

       // insertMoreData(100);
//        User user = mapper.getUser("15AA3FD8A6764F7395081D66001CD37A");
//        System.out.println(user.getUserName());
        List<User> userList = mapper.listUsers();
        for (User user1 : userList) {
            System.out.println(user1.getId() + "," +user1.getUserName() + "," +user1.getPhone());
        }
//        int count = mapper.deleteUser("15AA3FD8A6764F7395081D66001CD37A");
//        session.commit();
//        System.out.println("删除了" + count + "条数据！");
        if(session != null) 
            session.close();

    }

    private static void insertMoreData(int count) {
        String[] location = { "陕西西安", "河南郑州", "甘肃兰州", "江苏南京", "湖北武汉", "江西南昌",
                "湖南长沙", "四川成都", "上海", "北京", "山东烟台", "山西太原" };
        String[] birth = { "1958-09-12", "1988-05-22", "1998-01-12", "2008-09-18", "2008-01-01", "1918-03-22",
                "1978-09-29", "1968-10-12", "2018-10-31", "1989-11-12", "2003-11-23", "2001-01-23" };
        String[] sex = {"男","女","未知"};
        for (int i = 0; i < count; i++) {
            int randomlocation = new Random().nextInt(location.length);
            int randombirth = new Random().nextInt(birth.length);
            int randomsex = new Random().nextInt(sex.length);
            int phone = 10912 + i;
            User user2 = new User(UUIDUtil.UUIDCreater(),
                    RandomString.chineseString(), UUID.randomUUID().toString(), "152596" + phone,
                    location[randomlocation], birth[randombirth], sex[randomsex]) ;
            mapper.insertUser(user2);
            session.commit();
        }

    }

}

```