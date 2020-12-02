tags: [#java, #学习]

## 其他知识点
### 1、String和char的区别：

(1)String是字符串类型，char是字符类型；

(2)char要用单引号，String要用双引号；

(3)String是一个类，具有面向对象的特性，可以调用方法

### 2、Switch条件语句：

```java
- Switch(表达式){
    case 值：代码；
        break;
        ...
    default:代码；
        break;    
}
```
(1)Switch后面小括号的表达式的值必须是整型或者字符型；

(2)case后面的值可以是常量数值，也可以是一个常量表达式；

(3)case匹配后，执行匹配块的程序代码，如果没有遇到break则会继续执行下一个case块的内容，直到遇到break语句或者Switch语句块结束；

### 3、while(判断条件){  循环操作   }，先判断，后执行

### 4、do {循环操作}while(判断条件),先执行，后判断，至少执行一次

### 5、当一个方法不需要返回数据时，返回类型(修饰符)必须是void；

### 6、多重for循环：外层循环控制行，内层循环控制列；

### 7、公共类（public 修饰的）文件名必须与类名保持一致（相同）

### 8、showSaveDialog()和showOpenDialog()方法决定文件对话框类型（JFileChooser对象）

### 9、一个Java文件中只能含有一个public类

### 10、增强for循环：（一般用于遍历数组）

 ```java
 for(循环变量类型 变量名称：要遍历的对象){
     循环语句；
 }
 ```
```java
//遍历Collection对象
//建立一个collection
String[] string = {"hello","how","are","you"};
Collection list = java.util.Arrays.asList(string);//将数组转换为List对象
//开始遍历
for(String str:list){
    System.out.println(str);
}

//遍历数组
int[] a = {1,5,3,7,6,0};
for(int i:a){
    System.out.println(i);
}
```

###  11、基本数据类型的自动装箱与拆箱：

- 基本类型数据和相应的对象之间互相自动转换；
- 拆箱过程



```mermaid
graph LR
数据类型-->相应的对象  
```
- 装箱过程

```mermaid
graph LR
数据对象-->数据类型
```
### 12、for循环的死循环：

```java
    for(;;){
        循环体；
    }
```


