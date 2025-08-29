tags: #db #jndi

- 数据库连接有很多中方式，JDBC数据库的连接方式，前边我们已经介绍过了，而开发中我们经常使用的是DataBaseConnectionPool(数据库连接池,DBCP)。数据库连接池到底是什么？它比jdbc数据库连接有什么优势呢？它又怎么使用呢？

#### 一、JDBC连接 

- 先看一下JDBC连接，每次用户访问数据库时，需要JDBC为我们创建数据库连接，我们使用，然后关闭。而当我们加断点测试，可以发现这个过程中创建数据库连接这个过程是比较费时间的，而不是我们在数据库中操作数据费时间。所以JDBC这种方式的效率大大折扣。而且如果过多的人同时并发来访问数据库，连接数量创建过多，会导致性能降低，更严重可能会导致数据库崩溃。而，数据库连接池就是来解决这两种问题的。

 

#### 二、数据库连接池是什么？

- 顾名思义就是盛放多个数据库连接的一个池子！当我们访问数据库时我们直接从这个池子中拿连接对象即可，省去了初始化创建的过程，大大提高了效率。而且这个池子可以控制数据库连接的数量，我们里边可以至少放上几个，不够用了再进行创建，最多能够创建几个等等来控制连接的数量。它就是这么一个技术。准确一点说，连接池是一种缓存技术（cache）,因为这个池子是在缓存中存放的。



####  三、连接池的优势呢？

- 其实就是解决了JDBC的劣势。提前准备好连接对象，提高了访问效率，控制连接数量，防止同时过多用户访问导致性能大大降低，数据库崩溃。



#### 四、DBCP怎么使用？

- 编写数据库连接池是比较麻烦的，而且编写出来的效果如何另说。所以一般我们都使用现成的。各种服务器都为我们提供了，这里先看一下Tomcat服务器的数据库连接池如何使用。



-  1，在tomcat的catalina_home/webapps/webapp/meta-inf/目录下新建context.xml文件，来编写DBCP，这是针对此应用程序的（当然也可以之间在tomcat的catalina_home/conf/context.xml中编写，这个这个是针对这个tomcat服务器的），编写内容如下：

```
 <?xml version="1.0" encoding="GBK"?>  
    <!--这是数据连接池的配置文件，只有name可以自己定义 -->  
    <Context reloadable="true">  
        <Resource name="jdbc/ljh"   
                  auth="Container"   
                  type="javax.sql.DataSource"  
                  maxActive="100"   
                  maxIdle="30"   
                  maxWait="10000"   
                  username="ljh"   
                  password="ljh"  
                  driverClassName="oracle.jdbc.driver.OracleDriver"   
                  url="jdbc:oracle:thin:@192.168.1.27:1521:ljh"   
        />  
    </Context>  
 
```

- 大家可以通过名字看出，这都是在设置dbcp的各个属性，例如，最大连接数，最小连接数，最长等待时间等等，设置好以后我们就可以使用了。



 - 那么怎么使用呢?这里就涉及到了JNDI，JNDI是J2EE13个规范之一，也是非常重要的。这里我来先简单介绍一下JNDI：

##### JNDI（Java Naming and Directory Interface） 
- java命名和目录服务接口
- 降低程序和程序之间的耦合性
- 降低设备和设备的耦合性
- Tomcat服务器实现了JNDI服务，启动Tomcat服务器，等同于启动JNDI服务器
- JNDI是SUN制定的一套规范，这套规范可以和JDBC进行类比，JDBC也是一套规范，我们面向JDBC接口调用就可以获取数据库中的数据。同样，我们面向JNDI接口调用，可以获取“资源”，这个资源不是在底层数据库中。
- JNDI提供了一种服务，这个服务可以将“名称”和“资源”进行绑定，然后程序员通过面向JNDI接口调用方法lookup可以查找到相关的资源。
 

- 由于只是简单了解，要想了解更多关于JNDI的资料，请查看：JNDI是什么  JNDI简介  tomcat配置JNDI  

##### jboss配置JNDI
 

- 看我们怎么通过JNDI来获取连接池：

```
//获取JNDI的上下文对象Context  
        Context context = new InitialContext();  
        //根据名称和资源的绑定来获取数据源连接池，其中java:/com/env是tomcat实现JNDI的路径，后边是我们连接池名字  
        DataSource ds = (DataSource)context.lookup("java:/comp/env/jdbc/ljh");   
        /*get，获取一种的一个连接，当然下边的close就是返回一个连接给连接池，这里的连接池都对Connection中的方法进行重写，例如close，是返回给连接池，而不是关闭数据库连接。    */
         conn = ds.getConnection();  
 
```
- 这样我们就可以使用连接对象了。

 

- 综上为连接池DBCP和JNDI的联合使用访问数据库。在实际开发中我们经常使用C3P0连接池，因为它开源的，而且和各种框架一起使用非常方便，效率也更高。不过原理跟上边的差不多，都是依赖JDBC规范和JNDI规范，来实现的，这里看一些它的资料吧！  C3P0英文文档   C3p0百科

 

- 综上为数据库连接，顺便简单总结了一下JNDI。数据库连接在每个系统中都会使用，虽然可能就需要我们配置一次，编写一次，但是是非常重要的，因为数据的安全是非常重要的哈。所以还是需要我们好好掌握的。

