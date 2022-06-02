# Spring boot 整合swagger初探指南

### SWAGGER是什么？

**OpenAPI规范**（以前称为Swagger规范）是REST API的API描述格式。OpenAPI文件允许您描述整个API，包括：

- 可用端点（`/users`）和操作上的每个端点（`GET /users`，`POST /users`）
- 操作参数每次操作的输入和输出
- 认证方式
- 联系信息，许可，使用条款和其他信息。

上面这些是swagger官方给出的说明，简单来说swagger就是接口文档生成工具，可以让你快速地生成接口文档，你需要做的只是在你的接口方法上增加相应的注解。这种文档生成方式，一方面可以让你不需要前端页面就可以测试自己的接口，提高开发效率；另外一方面，当你的接口开发完成后，前端工程师可以根据文档完成自己的开发，减少对接过程中的繁琐沟通，而且支持简单的调试。

我们先来预览下，swagger2长什么样：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200513222212.png)

### 如何使用

知道了swagger的优势，那么我们如何使用它呢，下来我们就看看具体的整合流程。这里我们用的是swagger2，项目架构spring boot。

#### 引入依赖文件

和swagger2相关的依赖有两个：`springfox-swagger2`和`springfox-swagger-ui`

```xml
<dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
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
        <!-- Swagger API文档 -->
        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger2</artifactId>
            <version>2.9.2</version>
        </dependency>

        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger-ui</artifactId>
            <version>2.9.2</version>
        </dependency>
```

#### 配置swagger2

这里是swaggerd的核心配置，包括标题、描述信息、版本信息等等，更多内容可以去查官方文档：

[官方文档](https://swagger.io/docs/specification/2-0/basic-structure/)

```java
@Configuration
@EnableSwagger2
public class Swagger2Config {

    @Bean
    public Docket createRestApi() {
        return new Docket(DocumentationType.SWAGGER_2)
                .apiInfo(apiInfo()) // 接口文档的基本信息
                .select()
                .apis(RequestHandlerSelectors.withMethodAnnotation(ApiOperation.class))
                .paths(PathSelectors.any())
                .build();
    }

    private ApiInfo apiInfo() {
        return new ApiInfoBuilder()
                .title("XXXX项目接口文档")
                .description("该接口用于展示本项目所有相关接口信息")
                .version("1.0")
                .build();
    }

}
```

#### 配置swagger2静态资源及跨域访问

如果没有静态资源配置，swagger的页面应该是不能能正常展示的。

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

    /**
     *  配置swagger静态资源
     * @param registry
     */
    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler("static/**").addResourceLocations("/static/");
        registry.addResourceHandler("swagger-ui.html").addResourceLocations("classpath:/META-INF/resources/");
    }

    /**
     * 跨域支持配置
     * @param registry
     */
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**").allowCredentials(true).allowedOrigins("*").allowedMethods("GET", "PUT", "DELETE", "POST", "OPTIONS").maxAge(3600);
    }
}
```

#### controller增加swagger注解

controller也就是我们的接口才是swagger真正要发挥的地方，在接口上增加swagger相应的注解，会让你的接口文档更丰富：

- @Api：这个注解用在controller上，作用不大，经过测试，就算不加这个注解，文档依然正常，唯一的作用是增加接口的描述信息；description就是接口的描述信息，value属性已经过期了，经过测试，发现没啥用（欢迎大家打脸）
- @ApiOperation：这个注解用在方法上（具体接口），没有这个注解，swagger就不会扫描这个方法，也不会在接口文档中体现。value是接口的描述信息；httpMethod是方法的请求方式，可以是get/post/put/delete，也就是restful请求类型；notes是也就是提示信息；response是响应的对象类型，目前感觉没啥用；
- @ApiParam：可以指定请求入参的各种属性，包括是否必须、示例、允许的值等等

```java
@Controller
@Api(description = "spring boot swagger demo22222")
@RequestMapping("/swagger/dome")
public class SwaggerDemoController {

    @ResponseBody
    @ApiOperation(value = "swagger2示例接口描述",httpMethod = "POST",
            notes = "这里是notes信息", response = TestEntity.class)
    @RequestMapping("/list")
    public TestEntity listTest(TestEntity testEntity) {
        return testEntity;
    }
    
     @RequestMapping("/list2")
    public String listTest2(@ApiParam(name = "name", value = "value",
            allowableValues = "test2",example = "小王", required = true) String name) {
        return name + ", hello";
    }
}
```

#### Entity实体增加swagger注解

@ApiModel注解是加在我们的出参或者入参对象上的，加上这个注解，表明这是我们的入参或者出参，@ApiModelProperty和@ApiParam类似，不做过多赘述

```java
@ApiModel("swaggerDome实体")
public class TestEntity implements Serializable {
    // 名称
    @ApiModelProperty(name = "name",value = "名称：用户名称", required =true, notes = "这个是提示信息")
    private String name;
    // id
    @ApiModelProperty(value = "用户id，默认为010001",
            allowableValues = "010001,020001,030001,040001,050001,060001,070001,080001,090001,100001,110001,120001,990001")

    private String id;

/*
为了便于展示，这里省略了getter和setter方法
*/
}
```

#### 总结

其实，swagger2还有很多内容，但我觉得都内容都不难，更多的内容需要各位小伙伴去探索实验，这里就算抛砖引玉了，你也可以当我偷懒。目前还有很多类似的文档工具，有时间研究下：

- knife4j
- api2doc

本次示例项目路径：https://github.com/Syske/learning-dome-code/tree/master/spring-boot-swagger2-demo