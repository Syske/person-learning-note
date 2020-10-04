# 还在用if-else，新的解耦方式你确定不了解下？

## 前言

不知道各位小伙伴有没有这样的困惑，就是很多时候我们的业务实现很多，但是对外接口只有一个，这时候对于具体的业务我们需要根据业务编码进行判断，然后再根据不同的业务编码调用我们的具体业务，这时候我们会用到`if-else`或者`swatch`进行判断，大概就是这样：

```java
public class MyserviceImpl implements Myservice {
    
    @Autowired
    private Hadler01001ContentService service1;
    @Autowired
    private Hadler01002ContentService service2;
    @Autowired
    private Hadler01003ContentService service3;
    
    @Override
    public WrapperResponse handler(WrapperRequest request) {
        RequestHeader header = request.getHeader();
        if(header != null) {
            String businessCode = header.getBusinessCode();
            if("01001".equals(businessCode)) {
                // 处理业务01001
               return service1.handler(request);
            } else if("01002".equals(businessCode)) {
                // 处理业务01002
                return service2.handler(request);
            } else if("01003".equals(businessCode)) {
                //  处理业务01001
                return service3.handler(request);
            }

        }
        return new WrapperResponse();
    }
}
```

当然，你说上面这样写有什么问题吗，我觉没有，都很ok，但你说有没有改进的空间，我觉得有，为什么要改进主要有如下两个原因：

1. 耦合性太高，当增加新的业务类型时，需要修改实现的接口，不够优雅；
2. 当业务数量增多，`if-else`太多，不够美观

基于上面个原因，以及我爱折腾、爱探索的个性，我想改善这种状况，当然也从侧面说明我的工作不够量，竟然还有时间探索折腾😂😂，好了，皮一下就可以了。

今天没什么核心技术点，主要有两个：一个是**自定义注解**，另一个是**策略模式**



## 正文

### 创建项目

今天的项目毫无疑问是`springboot`项目，具体创建过程就不赘述了，如果觉得`spring`官方的创建地址太慢，可以使用阿里巴巴的地址创建：

```http
https://start.aliyun.com/
```

![](https://gitee.com/sysker/picBed/raw/master/images/20200912114510.png)

### 创建业务处理接口

这个接口并非是提供外部服务的接口，而是具体业务的接口，也就是我们的`01001`、`01002` 、`01003`要实现的接口：

```java
public interface HandlerContentService<T> {
    WrapperResponse<T> handler(WrapperRequest<Object> request);
}
```

当然，抽象类也是可以的，看个人喜好吧

### 实现业务处理接口

下来我们要继承业务处理接口，写具体的业务逻辑和业务处理过程：

```java
@Service
@BusinessType("01001")
public class Hadler01001ContentService implements HandlerContentService {
    @Override
    public WrapperResponse handler(WrapperRequest request) {
        WrapperResponse<String> stringWrapperResponse = new WrapperResponse<>();
        stringWrapperResponse.setMessage("01001");
        System.out.println("01001业务被调用");
        return stringWrapperResponse;
    }
}
```

其他业务接口类似，这里就不多说，其中`@BusinessType`是我们自定义的注解。

### 编写自定义注解

这里定义注解就是为了标记我们的业务实现类，然后从业务实现中拿到业务编号，需要注意的是因为我们需要拿到业务编号，所以定义的注解需要一个`value`，看下上面的业务实现你就懂了。

```java
@Inherited
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface BusinessType {
    String value();
}
```

接下来就是与springboot的整合了，也是今天讲的关键，我会尽可能讲的清楚



### 创建业务选择器

```java
public class HandlerContext {
    private Map<String,Class> handlerMap;

    public HandlerContext(Map<String, Class> handlerMap) {
        this.handlerMap = handlerMap;
    }

    public HandlerContentService getInstance(String type){
        Class clazz=handlerMap.get(type);
        if (clazz==null){
            throw new IllegalArgumentException("输入的参数类型有问题："+type);
        }
        return (HandlerContentService) BeanTool.getBean(clazz);
    }
}
```

这个选择器的作用就是根据我们的业务编码，返回对应编码的业务实现对象。这里比较重要的是我们的是`handlerMap`，它里面存放的是业务代码和业务代码对应的`class`，我们根据业务编码从`handlerMap`中拿出对应的`class`，根据`class`返回相应的业务处理实例，所以接下来我们看下如何根据`class`从`springboot`中拿到其实例，也就是我们的`BeanTool`。

### 从beanTool中获取业务实例

```java
@Component
public class BeanTool implements ApplicationContextAware {
    private static ApplicationContext applicationContext;
    //自动初始化注入applicationContext
    @Override
    public void setApplicationContext(ApplicationContext context) throws BeansException {
        if (applicationContext==null){
            applicationContext=context;
        }
    }

    /**通过bean的缩写的方式获取类型
     *
     * @param name
     * @return
     */
    public static Object getBean(String name){
        return applicationContext.getBean(name);
    }

    public static <T> T getBean(Class<T> clazz){
        return applicationContext.getBean(clazz);
    }
}
```

这里也没有特别复杂，就是从`spring`的`applicationContext`中直接获取，当然前提是你把你的类交给`spring`容器来管理。

当然还有一个更复杂的问题，就是`handlerMap`的初始化，即如何获取我们实现类和业务代码的`map`并把它注入到`springboot`中，接下来我们来解决这个问题



### handlerMap的初始化和注入

这里我们要用到`classScanner`，首先要定义自己的类扫描器，核心方法就是`scan`，其作用就是扫描我们的业务实现类，并返回`Set<Class<?>>`，这个类我们不需要做任何修改，可以直接使用，你也可以把它作为工具类，在后续项目中继续使用。

需要注意的是，除了依赖`org.apache.commons.lang3.ArrayUtils`外，其他的依赖都是`spring`包下的

```java
public class ClassScanner implements ResourceLoaderAware {
    private final List<TypeFilter> includeFilters=new LinkedList<>();
    private final List<TypeFilter> excludeFilters=new LinkedList<>();

    private ResourcePatternResolver resourcePatternResolver=new PathMatchingResourcePatternResolver();
    private MetadataReaderFactory metadataReaderFactory=new CachingMetadataReaderFactory(this.resourcePatternResolver);


    public static Set<Class<?>> scan(String[] basepackages, Class<? extends Annotation>...annoations) {
        ClassScanner cs=new ClassScanner();
        //需要扫描的注解
        if (ArrayUtils.isNotEmpty(annoations)){
            for (Class anno:annoations){
                cs.addIncludeFilter(new AnnotationTypeFilter(anno));
            }
        }
        Set<Class<?>> classes=new HashSet<>();
        for (String s:basepackages){
            classes.addAll(cs.doScan(s));
        }
        return classes;
    }
    public static Set<Class<?>> scan(String basePackage,Class<? extends Annotation> ...annoations){
        return scan(new String[]{basePackage},annoations);
    }

    private Set<Class<?>> doScan(String basePackage) {
        Set<Class<?>> classes=new HashSet<>();
        try {
            String packageSearchPath = ResourcePatternResolver.CLASSPATH_ALL_URL_PREFIX + ClassUtils.convertClassNameToResourcePath(SystemPropertyUtils.resolvePlaceholders(basePackage)) + "/**/*.class";
            Resource[] resources = this.resourcePatternResolver.getResources(packageSearchPath);
            for (Resource resource : resources) {
                if (resource.isReadable()){
                    MetadataReader metadataReader = this.metadataReaderFactory.getMetadataReader(resource);
                    if ((includeFilters.size()==0&&excludeFilters.size()==0)||matches(metadataReader)){
                        try {
                            classes.add(Class.forName(metadataReader.getClassMetadata().getClassName()));
                        } catch (ClassNotFoundException e) {
                            e.printStackTrace();
                        }
                    }
                }
            }
        }catch (IOException e){
            throw new BeanDefinitionStoreException("IO failure during classpath scanning",e);
        }
        return classes;
    }

    protected boolean matches(MetadataReader metadataReader) throws IOException {
        for(TypeFilter tf:this.excludeFilters){
            if (tf.match(metadataReader,this.metadataReaderFactory)){
                return false;
            }
        }
        for (TypeFilter tf:this.includeFilters){
            if (tf.match(metadataReader,this.metadataReaderFactory))
                return true;
        }
        return false;
    }

    /**
     * 设置解析器
     * @param resourceLoader
     */
    @Override
    public void setResourceLoader(ResourceLoader resourceLoader) {
        this.resourcePatternResolver= ResourcePatternUtils.getResourcePatternResolver(resourceLoader);
        this.metadataReaderFactory=new CachingMetadataReaderFactory(resourceLoader);
    }

    public void addIncludeFilter(TypeFilter typeFilter){
        this.includeFilters.add(typeFilter);
    }

    public void addExcludeFilter(TypeFilter typeFilter){
        this.excludeFilters.add(0,typeFilter);
    }

    public final ResourceLoader getResourceLoader(){
        return this.resourcePatternResolver;
    }

    public void resetResourceLoader(){
        this.includeFilters.clear();
        this.excludeFilters.clear();
    }
}
```

其实上面这里只完成了类的扫描，所以接下来就是拿到`Set<Class<?>>`，然后循环遍历，生成我们需要的`handlerMap`：

```java
@Component
public class HandlerProcessor implements BeanFactoryPostProcessor {

    /**
     * 扫描hanglerMap注解并注入容器中
     *
     * @param beanFactory
     * @throws BeansException
     */
    @Override
    public void postProcessBeanFactory(ConfigurableListableBeanFactory beanFactory) throws BeansException {
        Map<String, Class> handlerMap = new HashMap<>(3);
        ClassScanner.scan(Const.HANDLER_PACAGER, BusinessType.class).forEach(clazz -> {
            String type = clazz.getAnnotation(BusinessType.class).value();
            handlerMap.put(type, clazz);
        });
        HandlerContext context = new HandlerContext(handlerMap);
        beanFactory.registerSingleton(HandlerContext.class.getName(), context);
    }
}
```

这里继承了`BeanFactoryPostProcessor`接口，然后实现了`postProcessBeanFactory`方法，在方法内，我们调用了`ClassScanner.scan`，方法入参需要我们指定扫描的包路径（`Const.HANDLER_PACAGER`），这里我把它定义成静态代变量了。

重要的事说三遍！！！

**务必修改扫描的业务类的包路径！！！**

**务必修改扫描的业务类的包路径！！！**

**务必修改扫描的业务类的包路径！！！**

然后在创建业务选择器的实例时，将`handlerMap`作为参数传入，并通过`beanFactory.registerSingleton`将业务选择器注入`spring`容器中，这样`springboot`在启动的时候，我们的`handlerMap`就被初始化并连同选择器被注入到`spring`的容器中，然后我们就可以在公共接口实现类中直接使用业务选择器了，公共接口就再不需要`if-else`了：

```java
    @Autowired
    private HandlerContext handlerContext;

    @Override
    public WrapperResponse handler(WrapperRequest request) {
        RequestHeader header = request.getHeader();
        if(header != null) {
            String businessCode = header.getBusinessCode();          
            HandlerContentService instance = handlerContext.getInstance(businessCode);
            return instance.handler(request);

        }
        return new WrapperResponse();
    }
```

而且这时候你要增加新的业务实现就变得简单了，只需要编写你的业务实现了，然后增加`@BusinessType`注解即可，是不是很方便。

这里需要注意的是，`HandlerContext`上不需要任何`spring`的注解，因为我们是手动注入的，所以不需要`spring`再帮我们注入，如果加了，反而会有问题（亲测，不信你试下），虽然有提示，但并不影响。

![](https://gitee.com/sysker/picBed/raw/master/images/20200912132428.png)

### 测试

我这里写了一个`controller`进行简单测试：

```java
@Autowired
    private Myservice myservice;

    @RequestMapping("/test")
    public String test() {
        WrapperRequest<String> stringWrapperRequest = new WrapperRequest<>();
        RequestHeader requestHeader = new RequestHeader();
        requestHeader.setBusinessCode("01001");
        stringWrapperRequest.setHeader(requestHeader);
        myservice.handler(stringWrapperRequest);
        return "success";
    }

    @RequestMapping("/test2")
    public String test2() {
        WrapperRequest<String> stringWrapperRequest = new WrapperRequest<>();
        RequestHeader requestHeader = new RequestHeader();
        requestHeader.setBusinessCode("01002");
        stringWrapperRequest.setHeader(requestHeader);
        myservice.handler(stringWrapperRequest);
        return "success2";
    }

    @RequestMapping("/test3")
    public String test3() {
        WrapperRequest<String> stringWrapperRequest = new WrapperRequest<>();
        RequestHeader requestHeader = new RequestHeader();
        requestHeader.setBusinessCode("01003");
        stringWrapperRequest.setHeader(requestHeader);
        myservice.handler(stringWrapperRequest);
        return "success3";
    }
```

分别访问，控制台打印如下信息：

![](https://gitee.com/sysker/picBed/raw/master/images/20200912134331.png)

至此，今天的主要内容就结束了，整个过程比较顺利，下来我们做一个简单的总结。



## 总结

今天核心就讲了一个内容，就是通过策略模式消灭业务层中业务判断部分的`if-else`，实现代码的解耦。当然，这里只提供了一种思路，你也可以通过其他方式来达到相同的效果。

