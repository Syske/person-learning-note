### 常用方法

#### getName()方法

该方法的作用使用返回此class对象所表示的实体（类、接口、数组类、基元类型或void）的名称的String；如果该类对象表示的引用类型不是数组类型，则返回类基于Java&trade；语言规范所指定的二进制名称；如果该类对象表示基元类型或void，则返回的名称是等价于Java语言与基元类型或void对应的关键字的string；如果这个类对象表示一类数组，名称的形式由元素类型的名称加上表示数组深度的一个或多个`[`字符。元素类型名称的编码如下：

<blockquote><table summary="Element types and encodings">
    <tr><th align=center> Element Type </th> &nbsp;&nbsp;&nbsp; <th align=center> Encoding</th></tr>
    <tr><td align=center> boolean      </td> &nbsp;&nbsp;&nbsp; <td align=center> Z</td></tr>
    <tr><td align=center> byte         </td> &nbsp;&nbsp;&nbsp; <td align=center> B</td></tr>
    <tr><td align=center> char         </td> &nbsp;&nbsp;&nbsp; <td align=center> C</td>
    <tr><td align=center> class or interface</td>
      &nbsp;&nbsp;&nbsp; <td align=center> L<i>classname</i>;</td></tr>
<tr><td align=center> double       </td> &nbsp;&nbsp;&nbsp; <td align=center> D</td></tr>
<tr><td align=center> float        </td> &nbsp;&nbsp;&nbsp; <td align=center> F</td></tr>
<tr><td align=center> int          </td> &nbsp;&nbsp;&nbsp; <td align=center> I</td></tr>
<tr><td align=center> long         </td> &nbsp;&nbsp;&nbsp; <td align=center> J</td></tr>
<tr><td align=center> short        </td> &nbsp;&nbsp;&nbsp; <td align=center> S</td></tr>
</table></blockquote>


**注意：**对于数组，该方法获取到的值为`[[[Ljava.lang.Object`，其中`[`表示数组，`[`的数量表示数组的维度，一维数组一个，二位数组为两个，如上显示的时三维数组

下面是我演示的结果：

```java
*********************Object************************
ClassName:java.lang.Object
--------------------------------------------
*********************字符串************************
ClassName:java.lang.String
--------------------------------------------
*********************包装类************************
ClassName:java.lang.Integer
--------------------------------------------
ClassName:java.lang.Byte
--------------------------------------------
ClassName:java.lang.Double
--------------------------------------------
ClassName:java.lang.Float
--------------------------------------------
ClassName:java.lang.Long
--------------------------------------------
*********************基本类型************************
ClassName:int
--------------------------------------------
ClassName:long
--------------------------------------------
ClassName:double
--------------------------------------------
ClassName:void
--------------------------------------------
*********************数组************************
ClassName:[Ljava.lang.Object;
--------------------------------------------
ClassName:[[Ljava.lang.Object;
--------------------------------------------
ClassName:[[[Ljava.lang.Object;
--------------------------------------------
ClassName:[[[[Ljava.lang.Object;
--------------------------------------------
*********************集合************************
ClassName:java.util.ArrayList
--------------------------------------------
ClassName:java.util.List
--------------------------------------------
*********************枚举类型************************
ClassName:java.lang.Enum
--------------------------------------------
ClassName:io.github.syske.MyEnum
--------------------------------------------
*********************注解类型************************
ClassName:java.text.Annotation
--------------------------------------------
ClassName:io.github.syske.MyAnnotation
--------------------------------------------
*********************接口类型************************
ClassName:io.github.syske.MyInterface
--------------------------------------------
*********************Void************************
ClassName:java.lang.Void
```



#### toString()方法

我们先看下源码，方法实现很简单。isInterface是判断是否是接口，isPrimitive判断是否是基本数据类型，然后调用我们前面说到的getName方法。

```java
public String toString() {
        return (isInterface() ? "interface " : (isPrimitive() ? "" : "class "))
            + getName();
    }
```

toString演示效果如下：

```
*********************Object************************
toString:class java.lang.Object
--------------------------------------------
*********************字符串************************
toString:class java.lang.String
--------------------------------------------
*********************包装类************************
toString:class java.lang.Integer
--------------------------------------------
toString:class java.lang.Byte
--------------------------------------------
toString:class java.lang.Double
--------------------------------------------
toString:class java.lang.Float
--------------------------------------------
toString:class java.lang.Long
--------------------------------------------
*********************基本类型************************
toString:int
--------------------------------------------
toString:long
--------------------------------------------
toString:double
--------------------------------------------
toString:void
--------------------------------------------
*********************数组************************
toString:class [Ljava.lang.Object;
--------------------------------------------
toString:class [[Ljava.lang.Object;
--------------------------------------------
toString:class [[[Ljava.lang.Object;
--------------------------------------------
toString:class [[[[Ljava.lang.Object;
--------------------------------------------
*********************集合************************
toString:class java.util.ArrayList
--------------------------------------------
toString:interface java.util.List
--------------------------------------------
*********************枚举类型************************
toString:class java.lang.Enum
--------------------------------------------
toString:class io.github.syske.MyEnum
--------------------------------------------
*********************注解类型************************
toString:class java.text.Annotation
--------------------------------------------
toString:interface io.github.syske.MyAnnotation
--------------------------------------------
*********************接口类型************************
toString:interface io.github.syske.MyInterface
--------------------------------------------
*********************Void************************
toString:class java.lang.Void
```



#### toGenericString()方法

这个方法相比于toString方法，可以显示更多的类信息，也就是在toString的基础上加上修饰信息。如果是基本类型（isPrimitive）则直接调用toStirng方法，对于其他类型，则会显示类的修饰信息（public、private等）、类型信息（如果是注解类型，会加上@，如果是接口，会加上interface，如果是枚举类型会加上enum，其他的则会加上class）。这里我也涨知识了，官方注释里面有这样一句话：所有的注解类都是接口。这一点我之前没注意，也不知道，算是意外的收获。

演示结果：

```
*********************Object************************
toGenericString:public class java.lang.Object
--------------------------------------------
*********************字符串************************
toGenericString:public final class java.lang.String
--------------------------------------------
*********************包装类************************
toGenericString:public final class java.lang.Integer
--------------------------------------------
toGenericString:public final class java.lang.Byte
--------------------------------------------
toGenericString:public final class java.lang.Double
--------------------------------------------
toGenericString:public final class java.lang.Float
--------------------------------------------
toGenericString:public final class java.lang.Long
--------------------------------------------
*********************基本类型************************
toGenericString:int
--------------------------------------------
toGenericString:long
--------------------------------------------
toGenericString:double
--------------------------------------------
toGenericString:void
--------------------------------------------
*********************数组************************
toGenericString:public abstract final class [Ljava.lang.Object;
--------------------------------------------
toGenericString:public abstract final class [[Ljava.lang.Object;
--------------------------------------------
toGenericString:public abstract final class [[[Ljava.lang.Object;
--------------------------------------------
toGenericString:public abstract final class [[[[Ljava.lang.Object;
--------------------------------------------
*********************集合************************
toGenericString:public class java.util.ArrayList<E>
--------------------------------------------
toGenericString:public abstract interface java.util.List<E>
--------------------------------------------
*********************枚举类型************************
toGenericString:public abstract class java.lang.Enum<E>
--------------------------------------------
toGenericString:public final enum io.github.syske.MyEnum
--------------------------------------------
*********************注解类型************************
toGenericString:public class java.text.Annotation
--------------------------------------------
toGenericString:public abstract @interface io.github.syske.MyAnnotation
--------------------------------------------
*********************接口类型************************
toGenericString:public abstract interface io.github.syske.MyInterface
--------------------------------------------
*********************Void************************
toGenericString:public final class java.lang.Void
```

#### forName(String className)方法

这个方法是个静态方法，该方法返回与具有给定字符串名称的类或接口对应的Class对象。在我们反射调用的时候经常用到这个方法。下面我们简单演示：

```java
Class<?> aClass = Class.forName("io.github.syske.ForNameTestObject");
// 获取公有字段属性（public修饰）
Field[] fields = aClass.getFields();
// 获取所有字段属性
Field[] declaredFields = aClass.getDeclaredFields();
for (Field field : declaredFields) {
    System.out.println("field: " + field);
    System.out.println("field.getName: " + field.getName());
}
Object o = aClass.newInstance();
ForNameTestObject o1 = (ForNameTestObject) o;
System.out.println(o1.getName());
```

结果：

```
field: private java.lang.String io.github.syske.ForNameTestObject.name
field.getName: name
ForNameTestObject
```

#### cast(Object obj)

将对象强制转换为此class对象表示的类或接口。