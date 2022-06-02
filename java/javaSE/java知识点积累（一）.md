# 知识点积累

tags: [#java, #学习]

### 1、关于final的重要知识点：

- final关键字可以用于成员变量、本地变量、方法以及类；

- final修饰的成员变量必须在声明时被初始化，或者在构造器中初始化，否则就会报编译错误；

- 不能够对final变量再次赋值；

- 本地变量必须在声明时赋值；

- 在匿名类中所有变量都必须是final变量；

- final修饰的方法不能被重写；

- final修饰的类不能被继承；

- 没有在声明时初始化的final变量称为空白final变量（blank final variable），他们必须在构造器中初始化，或者调用this进行初始化，不然编译器会报错

- 对于一个final变量，如果是基本数据类型的变量，则其数值一旦在初始化之后便不能更改；如果是引用类型的变量，则在对其初始化之后便不能再让其指向另一个对象。 



### 2、操作数据类型为byte、short、int 、char时，两个数都会被转换成int类型，并且结果也是int类型（在进行+，-，*，/，%运算操作时）

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210131115546.png)

### 3、方法入参：

- 方法入参是基本类型时，传递的是值，方法内对传递值进行修改时不会影响调用是的变量 **(包装类、String和基本数据类型相似，传递的也是值的拷贝,也就是值的传递)** ；

- 方法入参是引用类型时，传递的是引用地址，方法内对传递值进行修改时会影响调用时的变量；

```java
package com.javasm.work3;

import java.util.Arrays;

public class TestMethod {
	public static void main(String[] args) {
		TestMethod method=new TestMethod();
		int b = 1;
		b = method.test1(b);
		System.out.println(b);
		
		int[] arr = {1,2,3};
		method.test2(arr);
		System.out.println(arr[0]);
		System.out.println(arr);
		Arrays.sort(arr);
	}
	
	/**
	 * 方法入参是基本数据类型时,传递的是值
	 * 方法内对传递的值进行修改时不会影响调用时的变量
	 * @param a
	 */
	public int test1(int a){
		a=2;
		return a;
	}
	
	/**
	 * 方法入参是引用数据类型时,传递的是内存地址引用
	 * 方法内对传递的引用进行修改时会影响调用时的变量
	 * @param arr1
	 */
	public void test2(int[] arr1){
		System.out.println(arr1);
		arr1[0] = 4;
	}
}
```


