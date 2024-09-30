### 准备工作
工欲善其事必先利其器，所以要学号`smail`语法，好的工具是必须的，这里推荐两个工具，一个是`Smali2Java`，也就是将`smail`文件转换成`java`的工具；另一个工具是`J2S2J1.3`，这个工具可以将简单的`java`或者`smail`代码进行转换。

### 案例
因为我是一开始直接看源码的，所以我们今天也是直接从源码开始：
```java
.super Ljava/lang/Object;
.source "Test.java"


# instance fields
.field private name:Ljava/lang/String;


# direct methods
.method public constructor <init>()V
    .registers 2

    .prologue
    .line 1
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 2
    const-string v0, "test"

    iput-object v0, p0, LTest;->name:Ljava/lang/String;

    return-void
.end method

.method public static main([Ljava/lang/String;)V
    .registers 4

    .prologue
    const/4 v2, 0x1

    .line 14
    sget-object v0, Ljava/lang/System;->out:Ljava/io/PrintStream;

    const-string v1, "Hello World!"

    invoke-virtual {v0, v1}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V

    .line 15
    new-instance v0, LTest;

    invoke-direct {v0}, LTest;-><init>()V

    invoke-virtual {v0, v2, v2}, LTest;->test(IZ)Ljava/lang/String;

    move-result-object v0

    .line 16
    sget-object v1, Ljava/lang/System;->out:Ljava/io/PrintStream;

    invoke-virtual {v1, v0}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V

    .line 17
    return-void
.end method


# virtual methods
.method public test(IZ)Ljava/lang/String;
    .registers 4

    .prologue
    .line 21
    const-string v0, "test"

    return-object v0
.end method

```
上面这些代码其实很简单，就是创建一个`Test`类，定义了一个私有成员属性`name`，并进行了赋值，然后定义了一个`main`方法，`main`方法中进行了`Hello World!`打印输出操作，对应的`java`代码：
```java
import java.io.PrintStream;

public class Test{

    public Test()    {
        name = "test";
        id = 1;
    }

    public static void main(String args[]){
        System.out.println("Hello World!");
String result = new Test().test(1, true);
System.out.println(result);
    }

    public String test(int i, boolean flag) {
return "test";
    }

    private int id;
    private String name;
}
```

### 代码拆解

下面我们来逐步讲解下`smail`的语法，方便大家建立它与`java`代码语法直接的关系。

`smail`文件，我的理解是它其实就类似于`java`编译之后的`.class`文件，也是一种字节码文件。

#### 基本信息
我们先看前三行：
```java
.super Ljava/lang/Object;
.source "Test.java"


# instance fields
.field private name:Ljava/lang/String;
```
目前没有找到官方的相关文档，只能结合网上的资料和自己的推测进行分析，如果有不合理的地方，希望大家不吝指教。

第一行`.super`表示当前类的父类，表示继承关系的

第二行`.source`表示当前字节码文件对应的源码文件名

第三行`.field`表示定义一个属性（字段），具体语法是
```
.field 访问权限 字段名:字段类型;
```
字段类型的取值范围如下：
| Dalvik字节码类型 | java基本数据类型 |
| ---------------- | ---------------- |
| V                | void             |
| Z                | boolean          |
| B                | byte             |
| C                | char             |
| S                | short            |
| I                | int              |
| J                | long             |
| F                | float            |
| D                | double           |
| L                | java类类型       |
| [                | 数组类型         |

我们这里的`Ljava/lang/String`就表示`String`类型的数据，如果是`int`类型，那语法应该是这样的：
```java
.field private id:I
```
这里的对照关系，和`class`字节码绝大部分都一样

#### 构造方法
紧接着，下面是构造方法对应的`smail`代码
```
# direct methods
.method public constructor <init>()V
    .registers 2

    .prologue
    .line 1
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 2
    const-string v0, "test"

    iput-object v0, p0, LTest;->name:Ljava/lang/String;

    return-void
.end method
```

##### .method
其中`.method`表示方法的开始，具体语法是：
```
.method 访问权限 方法名()返回结果
```
这里的返回结果和字段的类型取值一样，可以参考上面的表格

`.end method`表示方法的结束，与`.method`相对应，两者之间的内容为方法体

##### .registers
`.registers 2`用于声明当前方法的寄存器个数，寄存器是用来存放方法的入参和方法的局部变量的，具体语法为：
```java
.registers N
```
N代表需要的寄存器的总个数

同时，还有一个关键字`.locals`，它用于声明非参数的寄存器个数（也就是举报变量的个数，包含在registers声明的个数当中），也叫做本地寄存器，语法是一样的。

##### .prologue
`.prologue`表示方法代码的开始处，所以在方法中增加代码，只能在`.prologue`下面的区域进行

##### .line
`.line 1`用于标记`java`代码中的行数，没有实际含义

##### .invoke-direct
`invoke-direct {p0}, Ljava/lang/Object;-><init>()V`表示调用`private`或`init`方法，`p0`表示`java`中的`this`，所以这个方法的含义是调用`Object`的`init`方法，并把返回值赋给`p0`，这里需要补充一个小知识点：

在smali里的所有操作都必须经过寄存器来进行，本地寄存器用`v`开头数字结尾的符号来表示，如`v0`、`v1`、`v2`、...

参数寄存器则使用`p`开头数字结尾的符号来表示，如`p0`、`p1`、`p2`、...特别注意的是，`p0`不一定是函数中的第一个参数，在非`static`函数中， `p0`代指“`this`”，`p1`表示函数的第一个参数，`p2`代表函数中的第二个参数…，而在`static`函数中`p0`才对应第一个参数（因为`Java`的`static`方法中没有`this`方法）。

本地寄存器没有限制，理论上是可以任意使用的。

这里需要注意的是，再使用`vx`和`px`的时候一定不要超过定义的限制（也就是`.registers`和`.locals`），虽然超过代码编译时不会报错，但是在运行时会报错，而且在代码反编译的时候也会报错：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221016211145.png)
虽然这种报错不一定是参数个数超了，但如果之前反编译正常，修改之后不正常，这块可以作为一个检查点


##### const-string
`const-string v0, "test"`表示定义一个`String`常量，并把值赋给`v0`，也就是第一个本地寄存器。

下面再补充一些和`const-string`相关的内容


##### const
  - 定义常量


  `const/4`，`4`代表`4`个字节，最大只允许存放4位数值(`4`个二进制位)，取值范围为 `-8 and 7`
  
  ```java
  # 定义常量2，并将值赋给v2寄存器，
  const/4 v2, 0x02
  ```

  `const/16` 同上，最大值允许存放`16`位数值 第一位默认为符号位，所以计算后`15`位的数值，比如`short`类型数据 取值范围为`-32768~32767`
  
  ```java
  # 定义定义一个容器，将数字123123赋给v0
  const/16 v0 , 0x123123
  ```

  `const` 最大只允许存放`32`位数据,比如int类型数据, 取值范围`-2147483647~2147483647`
  
  ```java
  # 定义一个容器 将数字10赋值给v0
  const v0 , 0x10
  ```
  `const/high16` 最大只允许存放高`16`位数值

```java
#定义一个容器  比如0xFFFF0000末四位补0 存入高四位0XFFFF
const/high16 v0,0xFFFF0000

```

 `const-wide` 占用两个寄存器`vx`和`vx+1`，共`64`位，数值必须以`L`结尾，否则编译不通过

```java
const-wide v0,30 #占用v0和v1
```

`const-wide/16` 定义两个相连容器，最大只允许存放`16`位数据
`const-wide/32` 定义两个相连容器，最大只允许存放`32`位数据
`const-wide` 定义两个相连容器，最大只允许存放`64`位数据
`const-wide/high16` 定义两个相连容器，只允许存放高`16`位数据

##### iput-object
`iput-object v0, p0, LTest;->name:Ljava/lang/String;`表示把`v0`的值（也就是字符串常量`test`）赋给`p0`(也就是`this`)的`name`字段，`Ltest`标记的是`p0`的类型，`:Ljava/lang/String`是标记`name`的类型。

具体语法是：
```java
iput-object 要设置的值, 要设置值的对象, 对象类型;->字段名:字段类型;
```

这里的`iput`表示设置非静态成员变量，设置静态变量要用`sput`，语法如下
```java
sput-object 要设置的值, 类型;->字段名:字段类型;
```
这里的`-object`表示对非基本类型赋值，如果是基本类型可以通过`iput`、`sput`、`iput-boolean`、`sput-boolean`进行设置，语法是一样的。

##### iget-obejct
与`iput-object`对应，`iget-object`是为了获取数据，具体语法是：
```
iget-object 接收值的寄存器, 接受值来源对象（谁的字段）, 对象类型;->字段名:字段类型;
```
例如：
```
iget-object v0, p0, Lcom/syske/android/Activity;->_view:Lcom/syske/common/View;
```
静态变量的字段也是一样的：
```
sget-object 接收值的寄存器, 静态对象类型;->字段名:字段类型;
```
基本类型的字段也是类似的，需要通过`iget`、`sget`、`iget-boolean`、s`get-boolean`来获取

###### return-void
`return-void`表示方法没有返回值，也就是`void`，同时返回值还可以是:

- `return vx`：返回 `vx` 寄存器中的值。
- `return-wide  vx`：返回在 `vx,vx+1` 寄存器的 `doubl e/long` 值。
- `return-object vx`：返回在 vx 寄存器的对象引用。

| smali方法返回关键字 | java    |
| ------------------- | ------- |
| return              | byte    |
| return              | short   |
| return              | int     |
| return-wide         | long    |
| return              | float   |
| return-wide         | double  |
| return              | char    |
| return              | boolean |
| return-void         | void    |
| return-object       | 数组    |
| return-object       | object  |

#### 静态方法
自此，构造方法相关方法我们算是基本讲解完了，下面我们分析下静态`main`方法的源码，前面已经分享的内容这里直接忽略了。

```java
.method public static main([Ljava/lang/String;)V
    .registers 4

    .prologue
    const/4 v2, 0x1

    .line 14
    sget-object v0, Ljava/lang/System;->out:Ljava/io/PrintStream;

    const-string v1, "Hello World!"

    invoke-virtual {v0, v1}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V

    .line 15
    new-instance v0, LTest;

    invoke-direct {v0}, LTest;-><init>()V

    invoke-virtual {v0, v2, v2}, LTest;->test(IZ)Ljava/lang/String;

    move-result-object v0

    .line 16
    sget-object v1, Ljava/lang/System;->out:Ljava/io/PrintStream;

    invoke-virtual {v1, v0}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V

    .line 17
    return-void
.end method
```

##### invoke-virtual

`invoke-virtual {v0, v1}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V`表示
调用`protected`或`public`方法(非私有实例方法)，这里的`v0`就表示`java/lang/System`， `v1`表示方法的入参，具体语法如下：

```java
invoke-virtual {对象实例, 方法入参}, 实例类型;->方法名(入参类别;)返回值
```

如果参数是多参数则直接写多个参数即可，如上面的源码：

```java
invoke-virtual {v0, v2, v2}, LTest;->test(IZ)Ljava/lang/String;
```

另外与`invoke-virtual`类似的语句还有几个在，这里做一个简单的总结：
方法 | 说明
---|---
invoke-virtual | 用于非私有实例方法的调用
invoke-direct | 用于构造方法以及私有方法的调用
invoke-static | 调用静态方法
invoke-super | 调用父类的方法
invoke-interface | 调用接口方法

##### new-instance

`new-instance v0, LTest;`表示创建`LTest`的实例对象，并将对象引用赋值给`v0`寄存器
紧接着，调用`LTets`的实例化方法：

`invoke-direct {v0}, LTest;-><init>()V`表示调用实例化方法，并把返回值赋给`v0`

##### move-result-object

`move-result-object v0`表示将上一次（紧挨着的）方法执行结果指向`v0`，也就是接收方法返回值。

### 扩展知识

好了，至此我们已经把今天示例代码基本分析完了，同时也对`smail`的基本语法有了一些初步的认识，基于以上这些知识点，我们基本上已经可以阅读`smail`源码了，但是为了更全面地学习`smail`的语法，我觉得还是有必要补充一些额外的知识点，比如条件语句的语法：

#### 条件语句

| 语句                     | 说明                                      |
| ---------------------- | --------------------------------------- |
| if-eq vA, vB, :cond_** | 如果vA等于vB则跳转到:cond_** #equal             |
| if-ne vA, vB, :cond_** | 如果vA不等于vB则跳转到:cond_**  # not  equal     |
| if-lt vA, vB, :cond_** | 如果vA小于vB则跳转到:cond_**    #less than      |
| if-ge vA, vB, :cond_** | 如果vA大于等于vB则跳转到:cond_**  # greater equal |
| if-gt vA, vB, :cond_** | 如果vA大于vB则跳转到:cond_**  # greater than    |
| if-le vA, vB, :cond_** | 如果vA小于等于vB则跳转到:cond_** # less equal     |
| if-eqz vA, :cond_**    | 如果vA等于0则跳转到:cond_** #zero               |
| if-nez vA, :cond_**    | 如果vA不等于0则跳转到:cond_**                    |
| if-ltz vA, :cond_**    | 如果vA小于0则跳转到:cond_**                     |
| if-gez vA, :cond_**    | 如果vA大于等于0则跳转到:cond_**                   |
| if-gtz vA, :cond_**    | 如果vA大于0则跳转到:cond_**                     |
| if-lez vA, :cond_**    | 如果vA小于等于0则跳转到:cond_**                   |

其中，代码中`:cond_**`语句对应`if`条件中的`:cond_**`，表示该条件语句结束：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221016205841.png)



  #### 语法关键词
  下面是一些常用的语法关键词
  
| 关键词          | 说明                                 |
| --------------- | ------------------------------------ |
| .class          | 定义java类名                         |
| .super          | 定义父类名                           |
| .source         | 定义Java源文件名                     |
| .filed          | 定义字段                             |
| .method         | 定义方法开始                         |
| .end method     | 定义方法结束                         |
| .annotation     | 定义注解开始                         |
| .end annotation | 定义注解结束                         |
| .implements     | 定义接口指令                         |
| .local          | 指定了方法内局部变量的个数           |
| .registers      | 指定方法内使用寄存器的总数           |
| .prologue       | 表示方法中代码的开始处               |
| .line           | 表示java源文件中指定行               |
| .paramter       | 指定了方法的参数                     |
| .param          | 和.paramter含义一致,但是表达格式不同 |

### 总结
至此，我们的`smail`语法学习之路暂时告一段落，但是还是要多实践，多探索，毕竟学语法就是为了更好的实践，还是建议各位小伙伴找几个安卓项目亲自动手实践下，好了，今天的内容就到这里吧，感谢各位小伙伴的支持！！！

在梳理这些知识点的时候，我发现有位大佬的笔记写的很完整，感兴趣的小伙伴可以去看下：

[Android逆向开发之smali语言的学习](https://code.newban.cn/169.html)