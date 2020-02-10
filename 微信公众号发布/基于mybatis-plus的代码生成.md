# 基于mybatis-plus的代码生成

##### 前言

随着敏捷开发模式的推广，伴着日益增长的需求，日常工作中我们越来越注重效率和便捷性。今天我们就来探讨下如何自动生成代码，准确地说是如何依赖数据库生成我们的entity、mapper、mybatis xml、service、serviceImpl、controller，搭建我们的项目模板，提高我们的开发效率。这里我们的实现方式是基于mybatis-plus来实现的，废话少说，直接开始吧。

##### 创建项目

这里创建的maven项目，核心依赖如下：

```xml
  <properties>
        <mybatis-plus.version>2.1.9</mybatis-plus.version>
        <mybatis-plus-generator.version>2.1.9</mybatis-plus-generator.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>com.baomidou</groupId>
            <artifactId>mybatis-plus-generate</artifactId>
            <version>${mybatis-plus-generator.version}</version>
        </dependency>

        <dependency>
            <groupId>com.baomidou</groupId>
            <artifactId>mybatis-plus</artifactId>
            <version>${mybatis-plus.version}</version>
        </dependency>
```

这里需要还需要引入slf4j-log4j12和slf4j-api的依赖，否则会报找不到org/slf4j/LoggerFactory的错误：

```xml
   <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-log4j12</artifactId>
            <version>1.7.12</version>
        </dependency>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
            <version>1.6.1</version>
        </dependency>
```

因为要通过数据库自动构建代码，所以数据库驱动必不可少，这里演示用的是mysql数据库：

```xml
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>8.0.16</version>
        </dependency>
```

项目创建完后，下面我们要编写代码自动生成器。

##### 导入代码模板

在编写自动生成器之前，更重要的工作是导入代码模板，模板决定了后续你代码生成后的样式，如果第一次接触，先不要考虑如何自己构建模板，我们先照猫画虎改一个呗：

**entity.java的模板：**

文件名及路径：

- mybatis-templates/entity.java.vm

```java
package ${package.Entity};

#if(${activeRecord})
import java.io.Serializable;
#end

#foreach($pkg in ${table.importPackages})
import ${pkg};
#end

#if(${entityLombokModel})
import com.baomidou.mybatisplus.annotations.Version;
import lombok.Data;
import lombok.experimental.Accessors;
import java.io.Serializable;
#end

/**********************************************
 * 描述：$!{table.comment}
 *
 * @author ${author}
 * @version 1.0
 * @date： ${date}
 *********************************************/
#if(${entityLombokModel})
@Data
@Accessors(chain = true)
#end
#if(${table.convert})
@TableName("${table.name}")
#end
#if(${superEntityClass})
public class ${entity} implements Serializable {
#elseif(${activeRecord})
public class ${entity} extends Model<${entity}> {
#else
public class ${entity} implements Serializable {
#end

    private static final long serialVersionUID = 1L;

## ----------  BEGIN 字段循环遍历  ----------
#foreach($field in ${table.fields})
#if(${field.keyFlag})
#set($keyPropertyName=${field.propertyName})
#end
#if("$!field.comment" != "")
    /**
     * ${field.comment}
     */
#end
#if(${field.keyFlag})
## 主键
#if(${field.keyIdentityFlag})
	@TableId(value="${field.name}", type= IdType.AUTO)
#elseif(${field.convert})
    @TableId("${field.name}")
#end
## 普通字段
#elseif(${field.fill})
## -----   存在字段填充设置   -----
#if(${field.convert})
	@TableField(value = "${field.name}", fill = FieldFill.${field.fill})
#else
	@TableField(fill = FieldFill.${field.fill})
#end
#elseif(${field.convert})
	@TableField("${field.name}")
#end
## 乐观锁注解
#if(${versionFieldName}==${field.name})
	@Version
#end
## 逻辑删除注解
#if(${logicDeleteFieldName}==${field.name})
    @TableLogic
#end
	private ${field.propertyType} ${field.propertyName};
#end
## ----------  END 字段循环遍历  ----------

#if(!${entityLombokModel})
#foreach($field in ${table.fields})
#if(${field.propertyType.equals("boolean")})
#set($getprefix="is")
#else
#set($getprefix="get")
#end

	public ${field.propertyType} ${getprefix}${field.capitalName}() {
		return ${field.propertyName};
	}

#if(${entityBuilderModel})
	public ${entity} set${field.capitalName}(${field.propertyType} ${field.propertyName}) {
#else
	public void set${field.capitalName}(${field.propertyType} ${field.propertyName}) {
#end
		this.${field.propertyName} = ${field.propertyName};
#if(${entityBuilderModel})
		return this;
#end
	}
#end
#end

#if(${entityColumnConstant})
#foreach($field in ${table.fields})
	public static final String ${field.name.toUpperCase()} = "${field.name}";

#end
#end

#if(!${entityLombokModel})
	@Override
	public String toString() {
		return "${entity}{" +
#foreach($field in ${table.fields})
#if($!{velocityCount}==1)
			"${field.propertyName}=" + ${field.propertyName} +
#else
			", ${field.propertyName}=" + ${field.propertyName} +
#end
#end
			"}";
	}
#end
}
```

**mapper.java的模板：**

文件名及路径：

- mybatis-templates/mapper.java.vm

```java
package ${package.Mapper};


/**********************************************
 * 描述：$!{table.comment}
 *
 * @author ${author}
 * @version 1.0
 * @date： ${date}
 *********************************************/
public interface ${table.mapperName} {

}
```

**service.java的模板：**

文件名及路径：

- mybatis-templates/service.java.vm

```java
package ${package.Service};

import ${package.Entity}.${entity};

/**********************************************
 * 描述：$!{table.comment}
 *
 * @author ${author}
 * @version 1.0
 * @date： ${date}
 *********************************************/
#if(${kotlin})
interface ${table.serviceName}
#else
public interface ${table.serviceName} {

}
#end
```

**servicempl.java的模板：**

文件名及路径：

- mybatis-templates/serviceImpl.java.vm

```java
package ${package.ServiceImpl};

import ${package.Entity}.${entity};
import ${package.Mapper}.${table.mapperName};
import ${package.Service}.${table.serviceName};
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**********************************************
 * 描述：$!{table.comment}
 *
 * @author ${author}
 * @version 1.0
 * @date： ${date}
 *********************************************/
@Service("")
public class ${table.serviceImplName} implements ${table.serviceName} {

    private static Logger _log = LoggerFactory.getLogger(${table.serviceImplName}.class);
}
```

**controller.java的模板：**

文件名及路径：

- mybatis-templates/controller.java.vm

```java
package ${package.Controller};

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.beans.factory.annotation.Autowired;
import ${package.Service}.${table.serviceName};
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;

#if(${restControllerStyle})
import org.springframework.web.bind.annotation.RestController;
#else
import org.springframework.stereotype.Controller;
#end
#if(${superControllerClassPackage})
import ${superControllerClassPackage};
#end

/**********************************************
 * 描述：$!{table.comment}
 *
 * @author ${author}
 * @version 1.0
 * @date： ${date}
 *********************************************/
#if(${restControllerStyle})
@RestController
#else
@Controller
#end
@Api(value = "$!{table.comment}", description = "$!{table.comment}")
@RequestMapping("#if(${package.ModuleName})/${package.ModuleName}#end/#if(${controllerMappingHyphenStyle})${controllerMappingHyphen}#else${table.entityPath}#end")
#if(${superControllerClass})
public class ${table.controllerName} {
#else
public class ${table.controllerName} {
#end
    private static Logger _log = LoggerFactory.getLogger(${table.controllerName}.class);

    @Autowired
    private ${table.serviceName} service;
}
```

肯定有小伙伴在疑惑，上面的代码都是神马东西，我在了解mybatis-plus自动生成代码之前，第一次看到如上代码也是一脸懵逼。其实上面这些模板都是基于java的模板引擎  **Velocity** 编写的， Velocity是一个基于java的模板引擎（template engine）。它允许任何人仅仅简单的使用模板语言（template language）来引用由java代码定义的对象。  这里就不过多说明了，因为我也不是特别熟悉，有兴趣的小伙伴可以自行研究。

如果你不知道该如何改，那就先别动，等我们写完了自动生成器，你自然就知道咋改了，就算不知道，你也可以改着试呀。

##### 编写代码自动生成器

我们的传统是先写代码，后解释，代码如下：

```java
package io.github.syske.mybatisplus;

import com.baomidou.mybatisplus.generator.AutoGenerator;
import com.baomidou.mybatisplus.generator.InjectionConfig;
import com.baomidou.mybatisplus.generator.config.*;
import com.baomidou.mybatisplus.generator.config.rules.DbType;
import com.baomidou.mybatisplus.generator.config.rules.NamingStrategy;
import io.github.syske.mybatisplus.util.PropertiesFileUtil;

import java.io.File;
import java.util.HashMap;
import java.util.Map;

/**
 * @program: mybatisPlus
 * @description: 代码生成器
 * @author: liu yan
 * @create: 2019-11-30 12:13
 */
public class MybatisPlusGenerator {
    private static String JDBC_DRIVER = PropertiesFileUtil.getInstance("generator").get("generator.jdbc.driver");
    private static String JDBC_URL = PropertiesFileUtil.getInstance("generator").get("generator.jdbc.url");
    private static String JDBC_USERNAME = PropertiesFileUtil.getInstance("generator").get("generator.jdbc.username");
    private static String JDBC_PASSWORD = PropertiesFileUtil.getInstance("generator").get("generator.jdbc.password");
    private static String PROEJCT_NAME = "mybatisplus";//项目文件夹名称，我的项目名称就是mybatisplus
    private static String BASE_PACKAGE_NAME="io.github.syske"; // 包前缀，也就是你的代码要生成在那个包底下

    public static void main(String[] args) {

        String[] table = {"user"}; // 表名称，也就是你要生成那些表的代码，我这里配置了一个表
        String modelPath = "./"; // 模块路径，因为我就一个模块所以路径就是./，如果你的项目有多个模块，那就要指定你的模块名称
        for(int i = 0 ; i<table.length;i++) {
            shell(modelPath, table[i]);
        }
    }

    private static void shell(String modelPath, String tabName){

        File file = new File(modelPath);
        String path = file.getAbsolutePath();
        AutoGenerator mpg = new AutoGenerator();
        // 全局配置
        GlobalConfig gc = new GlobalConfig();
        gc.setOutputDir(path+"/src/main/java");
        gc.setOpen(false);
        gc.setFileOverride(true);
        gc.setActiveRecord(true);
        gc.setEnableCache(true);// XML 二级缓存
        gc.setBaseResultMap(true);// XML ResultMap
        gc.setBaseColumnList(true);// XML columList
        gc.setAuthor("syske");

        // 自定义文件命名，注意 %s 会自动填充表实体属性！
        gc.setMapperName("%sMapper");
        gc.setXmlName("%sMapper");
        gc.setServiceName("%sService");
        gc.setServiceImplName("%sServiceImpl");
        gc.setControllerName("%sController");
        mpg.setGlobalConfig(gc);

        // 数据源配置
        DataSourceConfig dsc = new DataSourceConfig();
        // 数据源类型orcale和mysql是不一样的
        dsc.setDbType(DbType.MYSQL);

        dsc.setDriverName(JDBC_DRIVER);
        dsc.setUsername(JDBC_USERNAME);
        dsc.setPassword(JDBC_PASSWORD);
        dsc.setUrl(JDBC_URL);
        mpg.setDataSource(dsc);

        // 策略配置
        StrategyConfig strategy = new StrategyConfig();
        strategy.setNaming(NamingStrategy.underline_to_camel);// 表名生成策略
        strategy.setInclude(new String[] {tabName}); // 需要生成的表
        mpg.setStrategy(strategy);

        // 包配置
        PackageConfig pc = new PackageConfig();
        pc.setParent(BASE_PACKAGE_NAME);
        pc.setController("controller");
        pc.setEntity("dao.model");
        pc.setMapper("dao.mapper");
        pc.setService("service");
        pc.setServiceImpl("service.impl");
        pc.setXml("dao.mapper");
        pc.setModuleName(PROEJCT_NAME);
        mpg.setPackageInfo(pc);

        // 注入自定义配置，可以在 VM 中使用 cfg.abc 【可无】
        InjectionConfig cfg = new InjectionConfig() {
            @Override
            public void initMap() {
                Map<String, Object> map = new HashMap<String, Object>();
                map.put("abc", this.getConfig().getGlobalConfig().getAuthor() + "-mp");
                this.setMap(map);
            }
        };
        mpg.setCfg(cfg);
        //多模块
        TemplateConfig tc = getTemplateConfig(gc,pc,modelPath,tabName, false);
        if (tc.getMapper() == null && tc.getXml() == null && tc.getService() == null &&
                tc.getServiceImpl() == null && tc.getController() == null && tc.getEntity(false) == null) {
            return;
        }
        // 关闭默认 xml 生成，调整生成 至 根目录（单模块）
        mpg.setTemplate(tc);

        // 自定义模板配置，可以 copy 源码 mybatis-plus/src/main/resources/template 下面内容修改，
        // 放置自己项目的 src/main/resources/template 目录下, 默认名称一下可以不配置，也可以自定义模板名称

        // 如上任何一个模块如果设置 空 OR Null 将不生成该模块。

        // 执行生成
        mpg.execute();
        // 打印注入设置【可无】
        System.err.println(mpg.getCfg().getMap().get("abc"));
    }


    /**
     * 控制包生成的路径与是否覆盖生成
     * @param gc // 全局配置
     * @param pc 包配置
     * @param model model名
     * @param tabName 表名
     * @param isCover 是否覆盖生成代码
     * @return TemplateConfig
     */
    private static TemplateConfig getTemplateConfig(GlobalConfig gc, PackageConfig pc, String model, String tabName, boolean isCover) {
        TemplateConfig tc = new TemplateConfig();
        String entity = getName(tabName,"_");
        String path = model + "/src/main/java/" +replace( pc.getParent());
        if (!isCover) {
            if (model.endsWith("dao")) {
                String mapperPath =path + "/" + replace(pc.getMapper()) + "/" + gc.getMapperName().replace("%s",entity) + ".java";
                if (isExists(mapperPath)) {
                    tc.setMapper(null);
                    System.out.println(gc.getMapperName().replace("%s",entity) + ".java 文件已存在");
                }

                String modelPath = path + "/" + replace(pc.getEntity()) + "/" + entity + ".java";
                if (isExists(modelPath)) {
                    tc.setEntity(null);
                    System.out.println(entity + ".java 文件已存在");
                }
                tc.setController(null);
                tc.setXml(null);
                tc.setService(null);
                tc.setServiceImpl(null);
            } else if (model.endsWith("api")) {
                String servicePath = path + "/" +replace(pc.getService()) + "/" +  gc.getServiceName().replace("%s",entity) + ".java";
                if (isExists(servicePath)) {
                    tc.setService(null);
                    System.out.println(gc.getServiceName().replace("%s",entity) + ".java 文件已存在");
                }
                tc.setController(null);
                tc.setEntity(null);
                tc.setServiceImpl(null);
                tc.setMapper(null);
                tc.setXml(null);
            }  else if (model.endsWith("service")) {
                String serviceImplPath = path + "/" +replace(pc.getServiceImpl()) + "/" +  gc.getServiceImplName().replace("%s",entity) + ".java";
                if (isExists(serviceImplPath)) {
                    tc.setServiceImpl(null);
                    System.out.println(gc.getServiceImplName().replace("%s",entity) + ".java 文件已存在");
                }
                String mapperXmlPath =path + "/" + replace(pc.getXml()) + "/" + gc.getXmlName().replace("%s",entity) + ".xml";
                if (isExists(mapperXmlPath)) {
                    tc.setXml(null);
                    System.out.println(gc.getXmlName().replace("%s",entity) + ".xml 文件已存在");
                }
                tc.setController(null);
                tc.setService(null);
                tc.setMapper(null);
                tc.setEntity(null);
            }else if (model.endsWith("web")) {
                String controllerPath = path + "/" +replace(pc.getController()) + "/" + gc.getControllerName().replace("%s",entity) + ".java";;
                if (isExists(controllerPath)) {
                    tc.setController(null);
                    System.out.println(gc.getControllerName().replace("%s",entity) + ".java 文件已存在");
                }
                tc.setMapper(null);
                tc.setXml(null);
                tc.setService(null);
                tc.setServiceImpl(null);
                tc.setEntity(null);
            }
        } else {
            if (model.endsWith("dao")) {
                tc.setController(null);
                tc.setService(null);
                tc.setXml(null);
                tc.setServiceImpl(null);
            } else if (model.endsWith("api")) {
                tc.setController(null);
                tc.setEntity(null);
                tc.setServiceImpl(null);
                tc.setMapper(null);
                tc.setXml(null);
            }  else if (model.endsWith("service")) {
                tc.setController(null);
                tc.setService(null);
                tc.setMapper(null);
                tc.setEntity(null);
            } else if (model.endsWith("web")) {
                tc.setMapper(null);
                tc.setXml(null);
                tc.setService(null);
                tc.setServiceImpl(null);
                tc.setEntity(null);
            }
        }
        return tc;
    }


    /**
     * 将点替换为斜杠
     * @param name
     * @return
     */
    private static String replace(String name) {
        return name.replace(".","/");
    }

    /**
     * 判断文件是否存在
     * @param path 路径
     * @return
     */
    private static boolean isExists(String path) {
        File file = new File(path);
        return file.exists();
    }

    /**
     * 根据驼峰命名，首字母大写
     * @param tabName 原名
     * @return 返回生成后的名字
     *  例如：user_info 返回 UserInfo
     */
    public static String getName(String tabName, String reChar) {
        String[] arr = tabName.split(reChar);
        String str = "";
        for (int i = 0; i < arr.length; i++ ) {
            String startChar = arr[i].substring(0,1).toUpperCase();
            String lastChar = arr[i].substring(1, arr[i].length());
            String newStr = startChar + lastChar;
            str += newStr;
        }
        return str;
    }
}
```

##### 解释

最前面的代码是获取数据库的配置，我是写在properties文件中的，当然你也可以直接写在代码中：

```properties
generator.jdbc.driver=com.mysql.cj.jdbc.Driver
generator.jdbc.url=jdbc:mysql://127.0.0.1:3307/test?characterEncoding=utf-8&zeroDateTimeBehavior=convertToNull&allowMultiQueries=true&serverTimezone=Asia/Shanghai
generator.jdbc.username=root
generator.jdbc.password=root
```

以上注释已经够详细了，我就不做过多说明，下来我说下我遇到的问题：

**第一个问题**

错误信息

```sh
java.sql.SQLException: The server time zone value '?й???????' is unrecognized or represents more than one time zone. You must configure either the server or JDBC driver (via the serverTimezone configuration property) to use a more specifc time zone value if you want to utilize time zone support.
```

刚开始我以为是编码问题，改了成utf-8，发现不行，然后上网查资料，发现是时区的问题，解决方法是在mysql url中加入如下参数：

```sh
zeroDateTimeBehavior=convertToNull&allowMultiQueries=true&serverTimezone=Asia/Shanghai
```

**第二个问题**

错误信息

```sh
java.sql.SQLSyntaxErrorException: Unknown error 1146
```

找了很多资料没有找到解决方法，然后在代码中找到如下设置：

```java
dsc.setDbType(DbType.ORACLE);
```

因为我是mysql数据库，所以要改成：

```java
dsc.setDbType(DbType.MYSQL);
```

如果你用的是orcale，记得改成orcale

##### 结语

如果没有报错，那你的代码模板已经完成了，如果你还想进一步定制完善，好好去研究 **Velocity** ，编写更符合自己需求的代码模板吧！

不知道各位小伙伴感觉怎么样，但我是真实地感受到用mybatis-plus构建项目的便利性，而且如果的模板够完善，生成基于单表的增删改查基本接口是没有什么压力的。好了，今天就到这里吧，我要去学习了😂