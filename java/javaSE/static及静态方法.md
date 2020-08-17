### 一、static
- >#### 1、方法声明中用关键字static修饰的均为类方法或者静态方法，不用static修饰的方法称为实例方法；


- >#### 2、实例方法可以调用该类中的实例方法或者类方法，类方法只能调用该类的类方法或者静态方法，不能调用实例方法（静态方法只能调用静态方法，不能调用非静态方法）

- >#### 3、在成员变量前加static关键字，可以将其生命为静态成员变量；

- >#### 4、如果类中成员变量被定义为静态，那么不论有多少个对象，静态成员变量只有一份拷贝，即所有对象共享该成员变量；

- >#### 5、静态变量的作用域只在类内部，但其生命周期却贯穿整个程序；

- >#### 6、静态成员方法只能对类的静态成员变量进行操作；静态方法，没有this引用。


- #### 7、 ==为什么静态成员、静态方法中不能用this和super关键字?==


- - 1、在静态方法中是不能使用this预定义对象引用的,即使其后边所操作的也是静态成员也不行.
因为this代表的是调用这个函数的对象的引用,而静态方法是属于类的,不属于对象,静态方法成功加载后,对象还不一定存在

 

- - 2、 在问题之前先讲super的用法：

- - - 1.super的用法跟this类似，this代表对本类对象的引用，指向本类已经创建的对象；而super代表对父类对象的引用，指向父类对象；

- - - 2.静态优先于对象存在；

- - - 3.由上面的1.和2.知：
因为静态优先于对象存在，所以方法被静态修饰之后方法先存在，而方法里面要用到super指向的父类对象，但是所需的父类引用对象晚于该方法出现，也就是super所指向的对象没有，当然就会出错。<br>
综上，静态方法中不可以出现super关键字。

 

- - 3、首先你要明白对象和类的区别。

- - - this和super是属于对象范畴的东西，而静态方法是属于类范畴的东西

- - - 所有的成员方法都有一个默认的的参数this(即使是无参的方法),只要是成员方法,编译器就会给你加上this这个参数如:<br>

- - - > Class A中void method1(){}实际上是这样的--------> void method1(A this)

- - - > void method2(int x){}实际上是这样的--------> void method2(A this, intx)
而静态方法与对象无关,根本不能把对象的引用传到方法中,所以不能用this
 

- - 4、在一个类中定义一个方法为static，则为静态方法，那就是说，无需本类的对象即可调用此方法，调用一个静态方法就是“类名.方法名”<br>

既然"无需本类的对象即可调用静态方法"，而this和super关键字都是用于本类对象的－－－－－调用静态方法无需本类的对象这句话很清楚表明：静态方法中不能用this和super关键字

 

- - 5、静态方法是存放在内存中的数据段里，this和super调用的是堆空间里的应用对象不能调用数据段区域里的数据，因此静态方法中不能用this和super关键字

 

- - 6、静态方法和静态类不属于单个对象，而是类的所有对象共享使用
而this代表当前对象

 

- - 7、东西只属于类，不属于任何对象，所以不能用THIS和SUPER。

---

- #### 8、==静态属性和静态方法只是可以继承没有表现出多态性==；

- - 因为静态方法和静态属性没有采用动态绑定。具体表现就是，  将子类实例向上转型则会调用到基类中的静态方法和属性，不转型就调用子类自身的静态方法和属性。<br>

- - 编译器不推荐通过实例去调用静态方法和属性，因为这种调用方式容易造成混淆。 <br>

- - 实际上，在Java的规范中，Java对于类的方法和属性采用了两种完全不同的处理机制：对于方法，使用重载机制实现了多态性；对于属性，使用的是同名属性隐藏机制。所谓的同名属性隐藏机制是指：<br>

- - - 在具有父子关系的两个类中，子类中相同名字的属性会使得从父类中继承过来的同名属性变得不可见，不管类型是否一致，名称一致的两个属性就是同名属性。<br>

- - 在子类中，无法简单地通过属性名称来获取父类中的属性，而是必须通过父类名称加属性名称(super.变量名)的方法才可以访问父类中的该属性。一般而言，为了代码容易阅读，极其不建议在父类和子类中使用同名属性。

```
package day008;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Demo {
    public static void main(String[] args) {
        Collection<?>[] collections = { new HashSet<String>(),
                new ArrayList<String>(), new HashMap<String, String>().values() };
        Super subToSuper = new Sub();
        for (Collection<?> collection : collections) {
            System.out.println(subToSuper.getType(collection));
        }
    }

    abstract static class Super {
        public static String getType(Collection<?> collection) {
            return "Super:collection";
        }

        public static String getType(List<?> list) {
            return "Super:list";
        }

        public String getType(ArrayList<?> list) {
            return "Super:arrayList";
        }

        public static String getType(Set<?> set) {
            return "Super:set";
        }

        public String getType(HashSet<?> set) {
            return "Super:hashSet";
        }
    }

    static class Sub extends Super {
        public static String getType(Collection<?> collection) {
            return "Sub";
        }
    }
}

/**输出结果：
 *Super:collection
 *Super:collection
 *Super:collection
 *

```

- #### 9、静态方法可以通过==类名.方法名==调用；

- #### 10、Java中静态变量只能在类主体中定义，不能在方法中定义。 静态变量属于类所有而不属于方法。