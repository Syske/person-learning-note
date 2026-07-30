tags: #xstream

### 前言

第一次接触Xstream，是在做一个socket通信的项目，由于是二次重新开发，所以有部分代码沿用了原来的代码（改造前用的webservice），其中xml字符串转换为对象，以及对象转换为xml字符串的代码用到了这个包，所以我也就照葫芦画瓢，最终把项目顺利做完了，由于没有遇到什么问题，所以也就没有对Xstream做深入的了解和探索，直到前几天又接手到一个新的项目，里面接口调用涉及到同样的业务需求，然后就再次想到Xstream，然后很自然地遇到了一些问题，所以也就有了这篇文章，好了，废话少说，直接开始吧。

### 过程：我太难了^|^

由于上次用过，所以我就自以为轻车熟路的开始了，下面是收到的消息体（也就是需要转换成对象的xml字符串）：

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<result>
    <message>认证成功</message>
    <data>
        <AAC003>张三</AAC003>
        <AAC002>610123456789012345</AAC002>
    </data>
    <code>1</code>
</result>
```

然后我就按照自己的理解，创建了消息体对象：

```java
// 为了方便，我省略了get/set方法，一下同
// 文件名: MsgText.java
public class MsgText {
	private Result result;// 结果
}

// 文件名: Result.java
public class Result {
	private String message;// 消息
    private Data data; // 数据
    private String code; // 消息代码
}

// 文件名: Data.java
public class Data {
    private String AAC003;
    private String AAC002;
}
```

下面是业务代码，也是以及我的理解写：

```java
String result = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><result><message>认证成功</message><data><AAC003>张三</AAC003><AAC002>610123456789012345</AAC002></data><code>1</code></result>";

XStream xstream = new XStream(new StaxDriver());
xstream.alias("MsgText", MsgText.class);
MsgText fromXML = (MsgText)xstream.fromXML(result);
```

毫无疑问地报错，以下是报错信息：

```java
Security framework of XStream not initialized, XStream is probably vulnerable.
Exception in thread "main" com.thoughtworks.xstream.mapper.CannotResolveClassException: result
```

经过查找资料，第一行错误是初始化失败，查到的资料如下：

> 意思是：xstream 的安全框架没有初始化，xstream 容易受攻击。
>
> 解决方法：xStream对象设置默认安全防护，同时设置允许的类

解决代码如下：

```java
XStream.setupDefaultSecurity(xStream);  // 其中xStream是你实例的XStream的变量名，这是个静态方法
xStream.allowTypes(new Class[]{Test.class, Test1.class}); 
```

设置完成后，第二行依然报错，查了很多资料，问题依然没有解决，然后我打算按照自己的理解先做一些尝试，然后在设置别名那里增加了一行代码：

```java
xstream.alias("Result", Result.class);
```

错误依旧，然后我又加入了一行代码：

```java
xstream.alias("Data", Data.class);
```

可依然还是相同的错误，我都快疯了，但问题总是要解决吧，可能是运气好，我都不知道自己怎么想到的，觉得可能是alias方法的大小写有问题，然后就经过N次的尝试和摸索，终于报错变了，变成类转换异常：

代码如下：

```java
XStream xstream = new XStream(new StaxDriver());
xstream.alias("msgtext", MsgText.class);
xstream.alias("result", Result.class);
xstream.alias("data", Data.class);
Class<?>[] classes = new Class[] { MsgText.class, Result.class,Data.class };
XStream.setupDefaultSecurity(xstream);
xstream.allowTypes(classes);
		
MsgText fromXML = (MsgText)xstream.fromXML(result);
```

错误如下：

```sh
Exception in thread "main" java.lang.ClassCastException: lss.test.reckoner.util.Result cannot be cast to lss.test.reckoner.ejb.MsgText
	at lss.test.reckoner.ejb.Test.main(Test.java:20)
```

然后，这时候我才恍然大悟，原来报文根对象必须是根节点（result），接着我把最后一行代码改成如下:

```sh
Result fromXML = (Result)xstream.fromXML(result);
```

然后就再也不报错了，接着我觉得那应该和msgtext和data都没有关系，然后删除了下面的代码：

```sh
xstream.alias("msgtext", MsgText.class);
xstream.alias("data", Data.class);
```

也把这里：

```java
Class<?>[] classes = new Class[] { MsgText.class, Result.class,Data.class };
```

改成：

```java
Class<?>[] classes = new Class[] { Result.class};
```

到此问题已经完美解决了

### 总结

- xml对象对应的是xml字符串的根节点，本例中就是Result，而不是我理解的MsgText

- `xstream.alias("msgtext", MsgText.class)`这个方法设置别名对应是xml的节点名，大小写要一致

### 拓展

这里再拓展些xstream的知识点

#### 关于XStream

XStream是一个简单的库，用于将对象序列化为XML并再次返回。

#### 特征

- **使用方便。**提供高级外观，简化了常见用例。
- **不需要映射。**大多数对象都可以序列化，而无需指定映射。
- **性能。**速度和低内存占用是设计的关键部分，使其适用于具有高消息吞吐量的大型对象图或系统。
- **清洁XML。**没有重复的信息可以通过反射获得。这导致XML更容易为人类阅读，并且比本机Java序列化更紧凑。
- **不需要修改对象。**序列化内部字段，包括私有和最终字段。支持非公开和内部类。类不需要具有默认构造函数。
- **完整对象图支持。**将维护在对象模型中遇到的重复引用。支持循环引用。
- **与其他XML API集成。**通过实现接口，XStream可以直接与任何树结构（而不仅仅是XML）进行串行化。
- **可定制的转换策略。**可以注册策略，允许自定义特定类型如何表示为XML。
- **安全框架。**对未编组类型进行精细控制，以防止受操纵输入的安全问题。
- **错误消息。**当由于格式错误的XML而发生异常时，会提供详细的诊断信息以帮助隔离和修复问题。
- **替代输出格式。**模块化设计允许其他输出格式。XStream目前提供JSON支持和变形。



#### 使用

##### 创建XStream 对象

有两种创建方式：

- 第一种：不需要XPP3库 开始使用Java6

```java
XStream xstream = new XStream(new StaxDriver());
```

- 第二种：需要XPP3库

```java
XStream xstream = new XStream();//需要XPP3库
```

**注意：** Xstream序列化XML时需要引用的jar包：xstream-[version].jar、xpp3-[version].jar、xmlpull-[version].jar。Xstream序列化Json需要引用的jar包：jettison-[version].jar。

使用Xstream序列化时，对JavaBean没有任何限制。JavaBean的字段可以是私有的，也可以没有getter或setter方法，还可以没有默认的构造函数。

##### 1. 序列化对象

**(1) Xstream序列化XML**

```java
public class Test
{
    public static void main(String[] args)
    {
        Person bean=new Person("张三",19);
        //XStream xstream = new XStream();//需要XPP3库
        //XStream xstream = new XStream(new DomDriver());//不需要XPP3库
        XStream xstream = new XStream(new StaxDriver());//不需要XPP3库开始使用Java6
        xstream.alias("人",Person.class);//为类名节点重命名
        //XML序列化
        String xml = xstream.toXML(bean);
        System.out.println(xml);
        //XML反序列化
        bean=(Person)xstream.fromXML(xml);
        System.out.println(bean);
    }
}
```

**(2) Xstream序列化Json**

Xstream序列化Json与序列化XML类似，例如：

```java
public class Test
{
    public static void main(String[] args)
    {
        Person bean=new Person("张三",19);
        XStream xstream = new XStream(new JettisonMappedXmlDriver());//设置Json解析器
        xstream.setMode(XStream.NO_REFERENCES);//设置reference模型,不引用
        xstream.alias("人",Person.class);//为类名节点重命名
        //Json序列化
        String xml = xstream.toXML(bean);
        System.out.println(xml);
        //Json反序列化
        bean=(Person)xstream.fromXML(xml);
        System.out.println(bean);
    }
}
```



##### 2. 反序列化XML获得对象。

```java
public class Test {
	public static void main(String[] args) {
		String msgtext = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><result><message>认证成功</message><data><AAC003>张三</AAC003><AAC002>610123456789012345</AAC002></data><code>1</code></result>";
		XStream xstream = new XStream(new StaxDriver());		
		xstream.alias("result", Result.class);
		Class<?>[] classes = new Class[] { Result.class};
		XStream.setupDefaultSecurity(xstream);
		xstream.allowTypes(classes);
		
		Result fromXML = (Result)xstream.fromXML(msgtext);
		System.out.println(fromXML);
	}
}


public class Result {
	private String message;
	private Data data;
	private String code;
	private String appmsg;
	private String appcode;
	
	public String getMessage() {
		return message;
	}
	public void setMessage(String message) {
		this.message = message;
	}
	public Data getData() {
		return data;
	}
	public void setData(Data data) {
		this.data = data;
	}
	public String getCode() {
		return code;
	}
	public void setCode(String code) {
		this.code = code;
	}
	public String getAppmsg() {
		return appmsg;
	}
	public void setAppmsg(String appmsg) {
		this.appmsg = appmsg;
	}
	public String getAppcode() {
		return appcode;
	}
	public void setAppcode(String appcode) {
		this.appcode = appcode;
	}
}

```



##### 3.Xstream序列化重命名

**(1)为包重命名：Xstream.aliasPackage()方法**

```java
public class Test
{
    public static void main(String[] args)
    {
        Person bean=new Person("张三",19);
        XStream xstream = new XStream();
        xstream.aliasPackage("com.lzw", "test");//为包名称重命名
        //序列化
        String xml = xstream.toXML(bean);
        System.out.println(xml);
        //反序列化
        bean=(Person)xstream.fromXML(xml);
        System.out.println(bean);
    }
}
```

**(2)为类重命名：Xstream.alias()方法**

```java
public class Test
{
    public static void main(String[] args)
    {
        Person bean=new Person("张三",19);
        XStream xstream = new XStream();
        xstream.alias("人", Person.class);//为类名节点重命名
        //序列化
        String xml = xstream.toXML(bean);
        System.out.println(xml);
        //反序列化
        bean=(Person)xstream.fromXML(xml);
        System.out.println(bean);
    }
}
```

**(3)为字段重命名：Xstream.aliasField()方法**

```java
public class Test
{
    public static void main(String[] args)
    {
        Person bean=new Person("张三",19);
        XStream xstream = new XStream();
        xstream.aliasField("姓名", Person.class,"name");//为类的字段节点重命名
        xstream.aliasField("年龄", Person.class,"age");//为类的字段节点重命名
        //序列化
        String xml = xstream.toXML(bean);
        System.out.println(xml);
        //反序列化
        bean=(Person)xstream.fromXML(xml);
        System.out.println(bean);
    }
}
```

**(4)省略集合根节点：Xstream.addImplicitCollection()方法**

```java
class Person
{
    private String name;
    private int age;
    private List friends;
    public Person(String name, int age, String... friends)
    {
        this.name = name;
        this.age = age;
        this.friends = Arrays.asList(friends);
    }
    @Override
    public String toString()
    {
        return "Person [name=" + name + ", age=" + age + ", friends=" + friends + "]";
    }
}
public class Test
{
    public static void main(String[] args)
    {
        Person bean =new Person("张三",19,"李四","王五","赵六");
        XStream xstream = new XStream();
        xstream.addImplicitCollection(Person.class, "friends");//省略集合根节点
        //序列化
        String xml = xstream.toXML(bean);
        System.out.println(xml);
        //反序列化
        bean=(Person)xstream.fromXML(xml);
        System.out.println(bean);
    }
}
```

**(5)把字段节点设置成属性：Xstream.useAttributeFor()方法**

```java
public class Test
{
    public static void main(String[] args)
    {
        Person bean =new Person("张三",19,"李四","王五","赵六");
        XStream xstream = new XStream();
        xstream.useAttributeFor(Person.class, "name");//把字段节点设置成属性
        //序列化
        String xml = xstream.toXML(bean);
        System.out.println(xml);
        //反序列化
        bean=(Person)xstream.fromXML(xml);
        System.out.println(bean);
    }
}
```

**(6)隐藏字段：xstream.omitField()方法**

```java
public class Test
{
    public static void main(String[] args)
    {
        Person bean =new Person("张三",19,"李四","王五","赵六");
        XStream xstream = new XStream();
        xstream.omitField(Person.class, "friends");//把字段节点隐藏
        //序列化
        String xml = xstream.toXML(bean);
        System.out.println(xml);
        //反序列化
        bean=(Person)xstream.fromXML(xml);
        System.out.println(bean);
    }
}
```

##### 4.Xstream注解的使用

**(1)设置Xstream应用注解**
使用Xstream注解前需要对Xstream进行配置，可以使用两种方式：应用某个JavaBean类的注解或自动使用JavaBean类的注解。代码如下：

```cpp
XStream xstream = new XStream();
xstream.processAnnotations(Person.class);//应用Person类的注解
xstream.autodetectAnnotations(true);//自动检测注解
```

**(2)重命名注解：@XStreamAlias()**

```java
@XStreamAlias("人")
class Person
{
    @XStreamAlias("姓名")
    private String name;
    @XStreamAlias("年龄")
    private int age;
    @XStreamAlias("朋友")
    private List friends;
    public Person(String name, int age, String... friends)
    {
        this.name = name;
        this.age = age;
        this.friends = Arrays.asList(friends);
    }
    @Override
    public String toString()
    {
        return "Person [name=" + name + ", age=" + age + ", friends=" + friends + "]";
    }
}
```

**(3)省略集合根节点：@XStreamImplicit**

```java
class Person
{
    private String name;
    private int age;
    //@XStreamImplicit//只隐藏集合根节点
    @XStreamImplicit(itemFieldName="朋友")//设置重复的节点名，可能会导致无法反序列化
    private List<String> friends;
    public Person(String name, int age, String... friends)
    {
        this.name = name;
        this.age = age;
        this.friends = Arrays.asList(friends);
    }
    @Override
    public String toString()
    {
        return "Person [name=" + name + ", age=" + age + ", friends=" + friends + "]";
    }
}
```

**(4)把字段节点设置成属性：@XStreamAsAttribute**

```java
class Person
{
    @XStreamAsAttribute
    private String name;
    @XStreamAsAttribute
    private int age;
    private List<String> friends;
    public Person(String name, int age, String... friends)
    {
        this.name = name;
        this.age = age;
        this.friends = Arrays.asList(friends);
    }
    @Override
    public String toString()
    {
        return "Person [name=" + name + ", age=" + age + ", friends=" + friends + "]";
    }
}
```

**(5)隐藏字段：@XStreamOmitField**

```java
class Person
{
    private String name;
    private int age;
    @XStreamOmitField
    private List<String> friends;
    public Person(String name, int age, String... friends)
    {
        this.name = name;
        this.age = age;
        this.friends = Arrays.asList(friends);
    }
    @Override
    public String toString()
    {
        return "Person [name=" + name + ", age=" + age + ", friends=" + friends + "]";
    }
}
```

**(6)设置转换器：@XStreamConverter()**

```java
class Person
{
    private String name;
    private int age;
    @XStreamConverter(value=BooleanConverter.class,booleans={false},strings={"男","女"})
    private boolean sex;
    public Person(String name, int age, boolean sex)
    {
        this.name = name;
        this.age = age;
        this.sex=sex;
    }
    @Override
    public String toString()
    {
        return "Person [name=" + name + ", age=" + age + ", sex=" + sex + "]";
    }
}
```

##### 5.Xstream自定义的转换器

**(1)Xstream自带的转换器**
Xstream内部有许多转换器，用于JavaBean对象到XML或Json之间的转换。这些转换器的详细信息网址：[http://xstream.codehaus.org/converters.html](https://link.jianshu.com/?t=http://xstream.codehaus.org/converters.html)
**(2)使用自定义的转换器**

```java
class Person
{
    private String name;
    private int age;
    public Person(String name, int age)
    {
        this.name = name;
        this.age = age;
    }
    public String getName()
    {
        return name;
    }
    public void setName(String name)
    {
        this.name = name;
    }
    public int getAge()
    {
        return age;
    }
    public void setAge(int age)
    {
        this.age = age;
    }
    @Override
    public String toString()
    {
        return "Person [name=" + name + ", age=" + age + "]";
    }
}
public class PersonConverter implements Converter
{
    @Override//定义转换器能转换的JavaBean类型
    public boolean canConvert(Class type)
    {
        return type.equals(Person.class);
    }
    @Override//把对象序列化成XML或Json
    public void marshal(Object value, HierarchicalStreamWriter writer,
            MarshallingContext context)
    {
        Person person = (Person) value;
        writer.startNode("姓名");
        writer.setValue(person.getName());
        writer.endNode();
        writer.startNode("年龄");
        writer.setValue(person.getAge()+"");
        writer.endNode();
        writer.startNode("转换器");
        writer.setValue("自定义的转换器");
        writer.endNode();
    }
    @Override//把XML或Json反序列化成对象
    public Object unmarshal(HierarchicalStreamReader reader,
            UnmarshallingContext context)
    {
        Person person = new Person("",-1);
        reader.moveDown();
        person.setName(reader.getValue());
        reader.moveUp();
        reader.moveDown();
        person.setAge(Integer.parseInt(reader.getValue()));
        reader.moveUp();
        return person;
    }
}
public class Test
{
    public static void main(String[] args)
    {
        Person bean =new Person("张三",19);
        XStream xstream = new XStream();
        xstream.registerConverter(new PersonConverter());//注册转换器
        //序列化
        String xml = xstream.toXML(bean);
        System.out.println(xml);
        //反序列化
        bean=(Person)xstream.fromXML(xml);
        System.out.println(bean);
    }
}
}
}
```

**(3)常用的转换器接口与抽象类**
`SingleValueConverter`：单值转换接口
`AbstractSingleValueConverter`：单值转换抽象类
`Converter`：常规转换器接口

##### 6.Xstream对象流的使用

**(1)Xstream对象输出流**

```csharp
class Person
{
    private String name;
    private int age;
    public Person(String name, int age)
    {
        this.name = name;
        this.age = age;
    }
}
public class Test
{
    public static void main(String[] args) throws IOException
    {
        XStream xstream = new XStream();
        ObjectOutputStream out = xstream.createObjectOutputStream(System.out);
        out.writeObject(new Person("张三",12));
        out.writeObject(new Person("李四",19));
        out.writeObject("Hello");
        out.writeInt(12345);
        out.close();
    }
}
```

**注意：** XStream对象流是通过标准`java.io.ObjectOutputStream`和`java.io.ObjectInputStream`对象。 因为XML文档只能有一个根节点,必须包装在一个序列化的所有元素 额外的根节点。 这个根节点默认 `< object-stream >`上面的例子所示。
**(2)Xstream对象输出流**

```csharp
class Person
{
    private String name;
    private int age;
    public Person(String name, int age)
    {
        this.name = name;
        this.age = age;
    }
    @Override
    public String toString()
    {
        return "Person [name=" + name + ", age=" + age + "]";
    }
}
public class Test
{
    public static void main(String[] args) throws IOException, ClassNotFoundException
    {
        String s="<object-stream><test.Person><name>张三</name><age>12</age></test.Person><int>12345</int></object-stream>";
        StringReader reader = new StringReader(s);
        XStream xstream = new XStream();
        ObjectInputStream in = xstream.createObjectInputStream(reader);
        System.out.println((Person) in.readObject());
        System.out.println(in.readInt());
    }
}
}
```

##### 7.Xstream持久化API

**(1)保存JavaBean对象**

```csharp
class Person
{
    private String name;
    private int age;
    public Person(String name, int age)
    {
        this.name = name;
        this.age = age;
    }
    @Override
    public String toString()
    {
        return "Person [name=" + name + ", age=" + age + "]";
    }
}
public class Test
{
    public static void main(String[] args) throws IOException, ClassNotFoundException
    {
        PersistenceStrategy strategy = new FilePersistenceStrategy(new File("D:\\tmp"));
        List list = new XmlArrayList(strategy);
        list.add(new Person("张三",13));//保存数据
        list.add(new Person("李四",21));
        list.add(new Person("王五",17));
    }
}
```

程序运行结果： 如果我们检查D:\tmp目录,有三个文件:int@0.xml、int@1.xml、int@2.xml；每个对象都被序列化到XML文件里。
**(2)读取并删除JavaBean对象**

```csharp
public class Test
{
    public static void main(String[] args) throws IOException, ClassNotFoundException
    {
        PersistenceStrategy strategy = new FilePersistenceStrategy(new File("D:\\tmp"));
        List list = new XmlArrayList(strategy);
        for (Iterator it = list.iterator(); it.hasNext();)
        {
            System.out.println((Person) it.next());
            it.remove();//删除对象序列化文件
        }
    }
}
```

##### 8.Xstream操作Json

**(1)Xstream序列化Json的重命名**

```java
@XStreamAlias("人")
class Person
{
    @XStreamAlias("姓名")
    private String name;
    @XStreamAlias("年龄")
    private int age;
    public Person(String name, int age)
    {
        this.name = name;
        this.age = age;
    }
    @Override
    public String toString()
    {
        return "Person [name=" + name + ", age=" + age + "]";
    }
}
public class Test
{
    public static void main(String[] args)
    {
        Person bean=new Person("张三",19);
        XStream xstream = new XStream(new JettisonMappedXmlDriver());//设置Json解析器
        xstream.autodetectAnnotations(true);
        //Json序列化
        String xml = xstream.toXML(bean);
        System.out.println(xml);
        //Json反序列化
        bean=(Person)xstream.fromXML(xml);
        System.out.println(bean);
    }
}
```

**注意：** Xstream序列化Json的重命名的方式与其序列化成XML的方式一样！
**(2)去掉序列化Json的根节点**

```csharp
class Person
{
    private String name;
    private int age;
    public Person(String name, int age)
    {
        this.name = name;
        this.age = age;
    }
    @Override
    public String toString()
    {
        return "Person [name=" + name + ", age=" + age + "]";
    }
}
public class Test00
{
    public static void main(String[] args)
    {
        Person bean=new Person("张三",19);
        XStream xstream = new XStream(new JsonHierarchicalStreamDriver()
        {
            public HierarchicalStreamWriter createWriter(Writer writer)
            {
                return new JsonWriter(writer, JsonWriter.DROP_ROOT_MODE);
            }
        });
        //Json序列化
        String xml = xstream.toXML(bean);
        System.out.println(xml);
    }
}
}
```

**注意：** 去掉根节点后的Json串是不能反序列化的，因为XStream 不知道它的类型。
**(3)Json的解析器区别**
前面两个例子使用了不同的Json解析器，这里说明他们的不同之处：
`JettisonMappedXmlDriver`：是支持序列化和反序列化Json的。
`JsonHierarchicalStreamDriver`：只支持序列化，不支持反序列化