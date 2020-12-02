刚才看见一个兄弟在为Java的String传值/传引用问题困惑，翻箱倒柜找到了这篇我很久以前写的文章，发在这里，希望能对迷惑的朋友有些帮助。

提要：本文从实现原理的角度上阐述和剖析了：在Java语言中，以String作为类型的变量在作为方法参数时所表现出的“非对象”的特性。

### 一、最开始的示例

写代码最重要的就是实践，不经过反复试验而得出的说辞只能说是凭空遐想罢了。所以，在本文中首先以一个简单示例来抛出核心话题：

```java
public class StringAsParamOfMethodDemo {     

        public static void main(String[] args) { 

             StringAsParamOfMethodDemo StringAsParamOfMethodDemo =    

                     new StringAsParamOfMethodDemo(); 

             StringAsParamOfMethodDemo.testA(); 

        }     

        private void testA() { 

             String originalStr = "original"; 

             System.out.println("Test A Begin:"); 

             System.out.println("The outer String: " + originalStr); 

             simpleChangeString(originalStr); 

             System.out.println("The outer String after inner change: " + originalStr); 

             System.out.println("Test A End."); 

             System.out.println(); 

        }     

        public void simpleChangeString(String original) { 

             original = original + " is changed!"; 

             System.out.println("The changed inner String: " + original); 

        } 
} 
```

这段代码的逻辑是这样的：先赋值一个String类型的局部变量，然后把这个变量作为参数送进一个方法中，在这个方法中改变该变量的值。编译运行之后，发现输出结果是这样的：

``` 
Test A Begin:
The outer String: original
The changed inner String: original is changed!
The outer String after inner change: original
Test A End.
```

这个结果表明**在方法内部对String类型的变量的重新赋值操作并没有对这个变量的原型产生任何影响**。好了，这个示例的逻辑和运行结果都展示清楚了，接下来我们来对这个小程序进行分析。在这之前我们先来回顾下Java中所谓的“传值”和“传引用”问题。:yum:

### 二、Java中的“传值”和“传引用”问题

许多初学Java的程序员都在这个问题上有所思索，那是因为这是所谓的“C语言的传值和传指针问题”在Java语言上同类表现。

- 最后得出的结论是：

> 在Java中，当**基本类型**作为参数传入方法时，无论该参数在方法内怎样被改变，外部的变量原型总是不变的，代码类似上面的示例：

```java
int number = 0; 

changeNumber(number) {number++}; //改变送进的int变量 

System.out.println(number); //这时number依然为0

```

这就叫做“值传递”，即方法操作的是参数变量（也就是原型变量的一个值的拷贝）改变的也只是原型变量的一个拷贝而已，而非变量本身。所以变量原型并不会随之改变。
                  
但当方法传入的参数为非基本类型时（也就是说是一个对象类型的变量）， 方法改变参数变量的同时变量原型也会随之改变，代码同样类似上面的示例：

```java

StringBuffer strBuf = new StringBuffer(“original”); 

changeStringBuffer(strBuf) {strbuf.apend(“ is changed!”)} //改变送进的StringBuffer变量 

System.out.println(strBuf); //这时strBuf的值就变为了original is changed!    

```

这种特性就叫做“引用传递”，也叫做传址，即方法操作参数变量时是拷贝了变量的引用，而后通过引用找到变量（在这里是对象）的真正地址，并对其进行操作。当该方法结束后，方法内部的那个参数变量随之消失。但是要知道这个变量只是对象的一个引用而已，它只是指向了对象所在的真实地址，而非对象本身，所以它的消失并不会带来什么负面影响。回头来看原型变量，原型变量本质上也是那个对象的一个引用（和参数变量是一样一样的），当初对参数变量所指对象的改变就根本就是对原型变量所指对象的改变。所以原型变量所代表的对象就这样被改变了，而且这种改变被保存了下来。

了解了这个经典问题，很多细心的读者肯定会立刻提出新的疑问：“可是`String`类型在`Java`语言中属于非基本类型啊！它在方法中的改变为什么没有被保存下来呢！”的确，这是个问题，而且这个新疑问几乎推翻了那个经典问题的全部结论。真是这样么？好，现在我们就来继续分析。

### 三、关于String参数传递问题的曲解之一——直接赋值与对象赋值

> String类型的变量作为参数时怎么会像基本类型变量那样以传值方式传递呢？关于这个问题，有些朋友给出过解释，但可惜并不正确。

一种解释就是，对`String`类型的变量赋值时并没有new出对象，而是直接用字符串赋值，所以`Java`就把这个`String`类型的变量当作基本类型看待了。即，应该`String str = new String(“original”);`，而不是`String str = “original”;`。这是问题所在么？我们来为先前的示例稍微改造下，运行之后看看结果就知道了。改造后的代码如下：

```java
private void testB() { 

    String originalStr = new String("original"); 

    System.out.println("Test B Begin:"); 

    System.out.println("The outer String: " + originalStr); 

    changeNewString(originalStr); 

    System.out.println("The outer String after inner change: " + originalStr); 

    System.out.println("Test B End:"); 

    System.out.println(); 

} 

public void changeNewString(String original) { 

    original = new String(original + " is changed!"); 

    System.out.println("The changed inner String: " + original); 

} 
```

我们来看看这次运行结果是怎么样的：

```
Test B Begin:
The outer String: original
The changed inner String: original is changed!
The outer String after inner change: original
Test B End.
```

实践证明，这种说法是错的。

实际上，字符串直接赋值和用new出的对象赋值的区别仅仅在于存储方式不同。

简单说明下：

字符串直接赋值时，`String`类型的变量所引用的值是存储在类的常量池中的。因为`original`本身是个字符串常量，另一方面`String`是个不可变类型，所以这个`String`类型的变量相当于是对一个常量的引用。这种情况下，变量的内存空间大小是在编译期就已经确定的。

而new对象的方式是将`original`存储到`String`对象的内存空间中，而这个存储动作是在运行期进行的。在这种情况下，`Java`并不是把`original`这个字符串当作常量对待的，因为这时它是作为创建`String`对象的参数出现的。
所以对`String`的赋值方式和其参数传值问题并没有直接联系。总之，这种解释并不是正解。

### 四、关于String参数传递问题的曲解之二——“=”变值与方法变值

又有些朋友认为，变值不同步的问题是处在改变值的方式上。

这种说法认为：“在Java 中，改变参数的值有两种情况，第一种，使用赋值号“=”直接进行赋值使其改变；第二种，对于某些对象的引用，通过一定途径对其成员数据进行改变，如通过对象的本身的方法。对于第一种情况，其改变不会影响到被传入该参数变量的方法以外的数据，或者直接说源数据。而第二种方法，则相反，会影响到源数据——因为引用指示的对象没有变，对其成员数据进行改变则实质上是改变的该对象。”
这种方式听起来似乎有些…，我们还是用老办法，编写demo，做个小试验，代码如下：

``` java
private void testC() { 

    String originalStr = new String("original"); 

    System.out.println("Test C Begin:"); 

    System.out.println("The outer String: " + originalStr); 

    changeStrWithMethod(originalStr); 

    System.out.println("The outer String after inner change: " + originalStr); 

    System.out.println("Test C End."); 

    System.out.println(); 

}     

private static void changeStrWithMethod(String original) { 

    original = original.concat(" is changed!"); 

    System.out.println("The changed inner String: " + original); 

}
```

结果如下：

```
Test C Begin:
The outer String: original
The changed inner String: original is changed!
The outer String after inner change: original
Test C End. 
```

怎么样，这证明了问题并不是出在这，又一个解释在实践论据下夭折了。
那到底是什么原因导致了这种状况呢？
好了，不卖关子了，下面说下我的解释。

### 五、String参数传递问题的症结所在

其实，要想真正理解一个类或者一个API/框架的最直接的方法就是看源码。
下面我们来看看new出String对象的那小段代码（String类中），也就是String类的构造函数：

```java
public String(String original) { 
    int size = original.count; 
    char[] originalValue = original.value; 
    char[] v; 
    if (originalValue.length > size) { 
        // The array representing the String is bigger than the new
        // String itself.    Perhaps this constructor is being called 
        // in order to trim the baggage, so make a copy of the array. 
        int off = original.offset; 
        v = Arrays.copyOfRange(originalValue, off, off+size); 
    } else { 
        // The array representing the String is the same 
        // size as the String, so no point in making a copy.
        v = originalValue; 
    } 
    this.offset = 0; 
    this.count = size; 
    this.value = v; 
} 
```

也许你注意到了里面的char[],这说明对String的存储实际上通过char[]来实现的。怎么样？其实就是一层窗户纸。不知道大家还记不记得在Java API中定义的那些基本类型的包装类。比如Integer是int包装类、Float是float的包装类等等。对这些包装类的值操作实际上都是通过对其对应的基本类型操作而实现的。是不是有所感悟了？对，String就相当于是char[]的包装类。包装类的特质之一就是在对其值进行操作时会体现出其对应的基本类型的性质。在参数传递时，包装类就是如此体现的。所以，对于String在这种情况下的展现结果的解释就自然而然得出了。同样的，Integer、Float等这些包装类和String在这种情况下的表现是相同的，具体的分析在这里就省略了，有兴趣的朋友可以自己做做试验。

这也就是为什么当对字符串的操作在通过不同方法来实现的时候，推荐大家使用StringBuffer的真正原因了。至于StringBuffer为什么不会表现出String这种现象，大家再看看的StringBuffer的实现就会明白了，在此也不再赘述了。

### 六、写在最后

由此String类型的参数传递问题的原理也就展现出来了。其实可以看出，只要分析方式正确，思考终究得出正确结论的。
正确分析方法的基础有二：
- 1、多实践：手千万不要犯懒，实践必会出真知。

- 2、基于原理：搞清楚程序逻辑的最直接最简单的方式就是看源码，这毋庸置疑。

  只要基于这两个基础进行分析，在很多情况下会达到事半功倍的效果。这算是经验之谈吧，也算是分析程序的“捷径”方式之一。