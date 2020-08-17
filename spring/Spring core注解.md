### 1、@Autowired

- Autowired是用在JavaBean中的注解，通过byType形式，用来给指定的字段或方法注入所需的外部资源
- Autowired注解来指定自动装配，可以修饰setter方法、普通方法、实例变量和构造器等
- 当用来标注setter方法时，默认采用byType自动装配策略

```
@component
public class Chinese implments Person {
    @Autowried
    public void setAxe(Axe axe) {
        this.axe = axe;
    }
}
```
- 修饰带多个参数的普通方法时，Spring会自动到容器中寻找类型匹配的Bean，如果恰好为每个参数都找到一个类型匹配的Bean，Spring会自动以这些Bean作为参数来调用该方法
 ```
@component
public class Chinese implments Person {
    
    @Autowried
    public void setAxe(Axe axe, Dog dog) {
        this.axe = axe;
        this.dog = dog
    }
    ...
}
```

- 也可以用于修饰构造器和实例变量
- 修饰一个实例变量时，Spring将会把容器中与该实例变量匹配的Bean设置为该实例变量的值

```
@component
public class Chinese implments Person {
    @Autowried
    private Axe axe;
    @Autowried
    public Chinese(Axe axe, Dog dog) {
        this.axe = axe;
        this.dog = dog
    }
    ...
}
```

- 也可以用于修饰数组类型的成员变量，Spring会自动搜索容器中的所有Axe实例，并以这些Axe实例作为数组元素来创建数组，最后将该数组付给axes
```
@Component
public class Chinese implements Person {
    @Autowired
    private Axe[] axes;
    ...
}
```

- 与此类似的是，它也可以标注集合类型的实例变量，或者标注形参类型的集合方法，Spring对这种集合属性、集合形参的处理与上面对数组类型的处理是完全相同的

```
@Component
public class Chinese implements Person {
    
    private Set<Axe> axes;
    @Autowired
    public void setAxes(Set<Axe> axes) {
        this.axes = axes;
    }
    ...
}
```

- 对于集合类型的参数而言，程序代码中必须是泛型，如上代码所示，程序指定了该方法的参数书Set<Axe>类型，这表明Spring会自动搜索容器中的所有Axe实例，并将这些实例注入到axes实例变量中。如果程序没有使用泛型来指明集合元素的类型，则spring将会不知所措

```
public class BaseDaoImpl<T> implements BaseDaoImpl<T> {
    public void save(T e) {
        System.out.println("程序保存对象：" + e);
    }
}
```

### 2、@Component
-（把普通pojo实例化到spring容器中，相当于配置文件中的 <bean id="" class=""/>）

- 标注一个普通的Spring Bean类
- 泛指各种组件，就是说当我们的类不属于各种归类的时候（不属于@Controller、@Services等的时候），我们就可以使用@Component来标注这个类。
- 案例： 
```
<context:component-scan base-package=”com.*”> 
```
- 上面的这个例子是引入Component组件的例子，其中base-package表示为需要扫描的所有子包。 

### 3、@Controller

- 标注一个控制器组件类

### 4、@Service

- 标注一个业务逻辑组件类

### 5、@Repository

- 标注一个DAO组件类

### 6、@Scope

- 指定Bean实例的作用域，默认是singleton，当采用零配置方式来管理Bean实例是，可使用@Scope Annotation，只要在该Annotation中提供作用域的名称即可

### 7、@Resource

- 为目标Bean指定协作者Bean
```
@Component
public class Chinese implements Person {
    private Axe axe;
    
    @Resource(name="stoneAxe")
    public void setAxe(Axe axe) {
        this.axe = axe;
    }
}
```

### 8、@PostConstruct 和@PreDestroy

- 定制声明周期行为
- PostConstruct指定初始化行为
- PreDestroy指定销毁行为

### 9、@DependsOn

- 可以修饰Bean类或方法，使用时可以指定一个字符串数组作为参数，每个数组元素对应于一个强制初始化的Bean 

```
@DependsOn({"steelAxe","abc"})
@Component
pulic class Chinese implements Person {
    ...
}
```
### 10、@Lazy

- 修饰Spring Bean类用于指定该Bean的预初始化行为，使用时可以指定一个boolen类型的value值，该属性决定是否要预初始化该Bean

```
@Lazy(true)
@component
public class Chinese implements Person {
    
}
```

### 11、@Qualifier

- 允许根据Bean的id来执行自动装配
```
@Component
pulic class Chinese implements Person {
    @Autowired
    @Qualifier("steelAxe")
    private Axe axe;
    public void setAxe(Axe axe) {
        this.axe = axe;
    }
    
    public void useAxe() {
        System.out.println(axe.chop());
    }
}
```
- 上面的注解指定了axe实例变量将使用自动装配，且精确指定了被装配的Bean实例名称是steelAxe
- 如果使用@Autowired和@Quelifier实现精确的自动装配，还不如直接使用@Resource注解执行依赖注入


### 12、@RequestParam

- RequestParpm是传递参数的，用于将请求的参数区数据映射到功能处理方法的参数上
- 参数：
- - value：参数名字，即入参的请求参数名字，如username表示请求的参数区中的名字为username的参数的值将传入；

- - required：是否必须，默认是true，表示请求中一定要有相应的参数，否则将报404错误码；

- - defaultValue：默认值，表示如果请求中没有同名参数时的默认值，默认值可以是SpEL表达式，如“#{systemProperties['java.vm.version']}”。


```

public String queryUserName(@RequestParam String userName)

// 原子类型

public String queryUserName(@RequestParam(value="userName" ,required =false ) String userName)

public String requestparam5(  
@RequestParam(value="username", required=true, defaultValue="zhang") String username)   

```

- 原子类型：必须有值，否则抛出异常，如果允许空值请使用包装类代替。

- Boolean包装类型类型：默认Boolean.FALSE，其他引用类型默认为null。