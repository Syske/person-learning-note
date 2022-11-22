tags: [#javascript]

1、**`document.write()`  **：可用于直接向 HTML 输出流写内容。简单的说就是直接在网页中输出内容。

2、**`alert`(字符串或变量)** **：**警告（alert 消息对话框）

3、**确认（confirm 消息对话框）**

`confirm` 消息对话框通常用于允许用户做选择的动作，如：“你对吗？”等。弹出对话框(包括一个确定按钮和一个取消按钮)。

- **语法:**

```
onfirm(str);
```

- **参数说明:**
  - **str：**在消息对话框中要显示的文本**返回值:** Boolean值
  - **返回值：**当用户点击"确定"按钮时，返回true  当用户点击"取消"按钮时，返回false

**注:** 通过返回值可以判断用户点击了什么按钮

 

4、**提问（prompt 消息对话框）**

`prompt`弹出消息对话框,通常用于询问一些需要与用户交互的信息。弹出消息对话框（包含一个确定按钮、取消按钮与一个文本输入框）。

- **语法:**

```html
prompt(str1, str2);
```

- **参数说明:**
  - **str1**: 要显示在消息对话框中的文本，不可修改  str2：文本框中的内容，可以修改

- **返回值:**
  - 点击确定按钮，文本框中的内容将作为函数返回值  
  - 点击取消按钮，将返回**null**

 

5、**打开新窗口（window.open）**

`open()` 方法可以查找一个已经存在或者新建的浏览器窗口。

- **语法：**

```
window.open([URL], [窗口名称], [参数字符串])
```

- **参数说明:**

  - **URL：**可选参数，在窗口中要显示网页的网址或路径。如果省略这个参数，或者它的值是空字符串，那么窗口就不显示任何文档。

  - **窗口名称：**可选参数，被打开窗口的名称。

    - 1.该名称由字母、数字和下划线字符组成。     

    - 2."_top"、"_blank"、"_self"具有特殊意义的名称。       

      _blank：在新窗口显示目标网页       

      _self：在当前窗口显示目标网页       

      _top：框架网页中在上部窗口中显示目标网页      

    - 3.相同 name 的窗口只能创建一个，要想创建多个窗口则 name 不能相同。    

    - 4.name 不能包含有空格。

  - **参数字符串：**可选参数，设置窗口参数，各参数用逗号隔开。

- **参数表:**

  | 参数       | 值      | 说明                         |
  | ---------- | ------- | ---------------------------- |
  | top        | Number  | 窗口顶部距离屏幕顶部的像素数 |
  | left       | Number  | 窗口左边距离屏幕顶部的像素数 |
  | width      | Number  | 窗口宽度                     |
  | height     | Number  | 窗口高度                     |
  | menubar    | yes, no | 窗口是否有菜单               |
  | toolbar    | yes, no | 窗口是否有工具条             |
  | scrollbars | yes, no | 窗口是否有滚动条             |
  | status     | yes, no | 窗口是否有状态栏             |

例如:打开http://www.imooc.com网站，大小为300px * 200px，无菜单，无工具栏，无状态栏，有滚动条窗口：

```javascript
<script type="text/javascript">

window.open(

'http://www.imooc.com',

'_blank','

width=300,

height=200,

menubar=no,

toolbar=no,

status=no,

scrollbars=yes') 

</script>
```

***注意：***运行结果考虑浏览器兼容问题。

 

6、**闭窗口（window.close）**

`close()`关闭窗口

- **用法：**

```
window.close();   //关闭本窗口
```

或

```
<窗口对象>.close();   //关闭指定的窗口
```

例如:关闭新建的窗口。

```js
<script type="text/javascript">      

 var mywin=window.open('http://www.imooc.com'); //将新打的窗口对象，存储在变量mywin中

mywin.close(); 

</script>
```

**注意:上面代码在打开新窗口的同时，关闭该窗口，看不到被打开的窗口。**

7、**通过ID获取元素**

学过`HTML/CSS`样式，都知道，网页由标签将信息组织起来，而标签的id属性值是唯一的，就像是每人有一个身份证号一样，只要通过身份证号就可以找到相对应的人。那么在网页中，我们通过id先找到标签，然后进行操作。

- **语法:**

```
document.getElementById(“id”)
```

**看看下面代码:**

```html
<!DOCTYPE HTML>
<html>
  <head>
   <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
   <title>获取元素</title>
    <script type="text/javascript">
      var mye= document.getElementById("con") // 通过ID获取元素对象
      document.writre(mye); // 输出变量e
    </script>
   </head>
   <body>
    <h3>
        Hello
    </h3>
    <p id = "con">
        I love Javascript
    </p>
    </body>
</html>
```

**结果：**null或[object HTMLParagraphElement]

**8、innerHTML 属性**

`innerHTML` 属性用于获取或替换 HTML 元素的内容。

- **语法:**

```
Object.innerHTML
```

**注意:**

1.Object是获取的元素对象，如通过document.getElementById("ID")获取的元素。

2.注意书写，innerHTML区分大小写。

**9、改变 HTML 样式**

`HTML DOM `允许` JavaScript` 改变 `HTML `元素的样式。如何改变 `HTML` 元素的样式呢？

- **语法:**

  ```
  Object.style.property=new style;
  ```



**注意：**Object是获取的元素对象，如通过`document.getElementById("id")`获取的元素。

- **基本属性表（property）:**

  | 属性            | 描述                                 |
  | --------------- | ------------------------------------ |
  | backgroundColor | 设置元素的背景颜色                   |
  | height          | 设置元素的高度                       |
  | width           | 设置元素的宽度                       |
  | color           | 设置文本颜色                         |
  | font            | 在一行设置所有的字体属性             |
  | fontFamily      | 设置元素字体名称（黑体、微软雅黑等） |
  | fontSize        | 设置元素字体大小                     |

**注意:**该表只是一小部分CSS样式属性，其它样式也可以通过该方法设置和修改。

**10、显示和隐藏（display属性）**

网页中经常会看到显示和隐藏的效果，可通过display属性来设置。

- **语法：**

```
Object.style.display = value  // value 表示值
```



**注意:**Object是获取的元素对象，如通过`document.getElementById("id")`获取的元素。

- **value取值:**

| 值    | 描述                             |
| ----- | -------------------------------- |
| none  | 此元素不会被显示（隐藏）         |
| block | 此元素将显示为块级元素（即显示） |



**11、控制类名（className 属性）**

className 属性设置或返回元素的class 属性。

- **语法：**

```
object.className = classname
```



- **作用:**
  - 获取元素的class 属性
  - 为网页内的某个元素指定一个css样式来更改该元素的外观

**12、定义变量**

**变量名字可以任意取，**只不过取名字要遵循一些规则:

- 必须以字母、下划线或美元符号开头，后面可以跟字母、下划线、美元符号和数字。如下:

  ```
  正确:    mysum   
  		_mychar
  		$numa1         
  
  错误:   6num  //开头不能用数字  
         %sum //开头不能用除(_ $)外特殊符号,如(%  + /等) 
         sum+num //开头中间不能使用除(_ $)外特殊符号，如(%  + /等)
  ```



- 变量名区分大小写，如:A与a是两个不同变量。

- 不允许使用JavaScript关键字和保留字做变量名。

  | 关键字  |            |        |       |
  | ------- | ---------- | ------ | ----- |
  | break   | else       | new    | var   |
  | case    | finally    | return | void  |
  | catch   | for        | switch | while |
  | default | if         | throw  |       |
  | delete  | in         | try    |       |
  | do      | instanceof | typeof |       |

  | 保留字   |            |           |              |
  | -------- | ---------- | --------- | ------------ |
  | abstract | enum       | int       | short        |
  | boolean  | export     | interface | static       |
  | byte     | extends    | long      | super        |
  | char     | final      | native    | synchronized |
  | class    | float      | package   | throws       |
  | const    | goto       | private   | transient    |
  | debugger | implements | protected | volatile     |
  | double   | import     | public    |              |



**声明变量语法:** **var 变量名;**   

var就相当于找盒子的动作，在JavaScript中是关键字（即保留字），这个关键字的作用是声明变量，并为"变量"准备位置(即内存）。

```
var mynum ; //声明一个变量mynum
```

当然，我们可以一次找一个盒子，也可以一次找多个盒子，所以Var还可以一次声明多个变量，变量之间用","逗号隔开。

```
var num1,mun2 ; //声明一个变量num1
```

**注意：**变量也可以不声明，直接使用，但为了规范，需要先声明，后使用。

 

**13、多样化的我(变量赋值）**

我们可以把变量看做一个盒子,盒子用来存放物品,那如何在变量中存储内容呢?

我们使用"="号给变量存储内容,看下面的语句:

```
var mynum = 5 ; //声明变量mynum并赋值。
```

这个语句怎么读呢？ 给变量mynum赋值，值为5。我们也可以这样写:

```
var mynum; //声明变量mynum 
mynum = 5 ; //给变量mynum赋值
```

**注：**这里"="号的作用是给变量赋值，不是等于号。

盒子可以装衣服、玩具、水果...等。其实，变量是无所不能的容器，你可以把任何东西存储在变量里，如数值、字符串、布尔值等，例如：

```
var num1 = 123;       // 123是数值 
var num2 = "一二三";    //"一二三"是字符串 
var num3=true;    //布尔值true（真），false(假)
```

其中，num1变量存储的内容是数值；num2变量存储的内容是字符串，字符串需要用一对引号""括起来，num3变量存储的内容是布尔值(true、false)。

 

**14、表达出你的想法(表达式)**

表达式与数学中的定义相似，表达式是指具有一定的值、用操作符把常数和变量连接起来的代数式。**一个表达式可以包含常数或变量。**

我们先看看下面的JavaScript语句：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/ip_image012.jpeg)

生活中“再见”表达方法很多，如:英语(goodbye）、网络语（88）、肢体语（挥挥手）等。在JavaScript表达式无处不在，所以一定要知道可以表达哪些内容，看看下面几种情况:

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/ip_image014.jpeg)

注意:串表达式中mychar是变量

 

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/ip_image016.jpeg)

注意:数值表达式中num是变量

 

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/ip_image018.jpeg)

**注意：**布尔表达式中num是变量

**15、我还有其它用途( +号操作符）**

操作符是用于在JavaScript中指定一定动作的符号。

- （1）操作符

看下面这段JavaScript代码。

```js
sum = numa + numb;
```

其中的"="和"+"都是操作符。

JavaScript中还有很多这样的操作符，例如，算术操作符(`+、-、*、/`等)，比较操作符(`<、>、>=、<=`等)，逻辑操作符(`&&、||、！`)。

**注意：**“=” 操作符是赋值，不是等于。

- (2) "+"操作符

算术运算符主要用来完成类似加减乘除的工作，在JavaScript中，“+”不只代表加法，还可以连接两个字符串，例如：

```js
mystring = "Java" + "Script"; // mystring的值“JavaScript”这个字符串
```

 

**16、自加一，自减一 ( ++和- -)**

算术操作符除了(`+、-、*、/`)外，还有两个非常常用的操作符，自加一`“++”`；自减一`“--”`。首先来看一个例子：

```
mynum = 10; mynum++; //mynum的值变为11 
mynum--; //mynum的值又变回10
```

上面的例子中，mynum++使mynum值在原基础上增加1，mynum--使mynum在原基础上减去1,其实也可以写成:

```
mynum = mynum + 1;//等同于mynum++
mynum = mynum - 1;//等同于mynum--
```

 

**17、较量较量(比较操作符)**

我们先来做道数学题，数学考试成绩中，小明考了90分，小红考了95分，问谁考的分数高? 答: 因为“95 > 90”，所以小红考试成绩高。

其中大于号">" 就是比较操作符，小红考试成绩和小明考试成绩就是操作数，并且是两个操作数。

也就是说两个操作数通过比较操作符进行比较，得到值为真（true）和假(false)。

在JavaScript中，这样的比较操作符有很多，这些操作符的含义如下: 

| 操作符 | 描述     |
| ------ | -------- |
| <      | 小于     |
| >      | 大于     |
| <=     | 小于等于 |
| \>=    | 大于等于 |
| ==     | 等于     |
| !=     | 不等于   |

 

看看下面例子:

```js
var a = 5;//定义a变量，赋值为5

var b = 9; //定义b变量，赋值为9

document.write (a<b); //a小于b的值吗? 结果是真(true)

document.write (a>=b); //a大于或等于b的值吗? 结果是假(false)

document.write (a!=b); //a不等于b的值吗? 结果是真(true)

document.write (a==b); //a等于b的值吗? 结果是假(false)
 
```



**18、我与你同在(逻辑与操作符）**

数学里面的“a>b”，在JavaScript中还表示为a>b；数学中的“b大于a，b小于c”是“a<b<c”，那么在JavaScript中可以用&&表示，如下：

```
b>a && b<c    //“&&”是并且的意思, 读法"b大于a"并且" b小于c "
```



好比我们参加高考时,在进入考场前,必须出示准考证和身份证,两者缺一不可，否则不能参加考试，表示如下:

```js
if(有准考证 &&有身份证)  {    进行考场考试 }
```



 “&&”是逻辑与操作符，只有“&&”两边值同时满足(同时为真)，整个表达式值才为真。

**逻辑与操作符值表:**

| A     | B     | A\&\&B |
| ----- | ----- | ------ |
| true  | true  | true   |
| true  | flase | false  |
| false | true  | false  |
| false | false | false  |

**注意:** 如果A为假，A && B为假，不会在执行B; 反之，如果A为真，要由 B 的值来决定 A && B 的值。

 

**19、我或你都可以 (逻辑或操作符）**

`"||"`逻辑或操作符，相当于生活中的“或者”，当两个条件中有任一个条件满足，“逻辑或”的运算结果就为“真”。

例如：本周我们计划出游,可是周一至周五工作,所以周六或者周日哪天去都可以。即两天中只要有一天有空，就可以出游了。

```js
var a=3; 
var b=5; 
var c; 
c=b>a ||a>b;  //b>a是true，a>b是false，c是true
```

**逻辑或操作符值表:**

| A     | B     | A\|\|B |
| ----- | ----- | ------ |
| true  | true  | true   |
| true  | flase | ture   |
| false | true  | true   |
| false | false | false  |

**注意:** 如果A为真，A || B为真，不会在执行B; 反之，如果A为假，要由 B 的值来决定 A || B 的值。

 

**20、是非颠倒(逻辑非操作符）**

"!"是逻辑非操作符，也就是"不是"的意思,非真即假，非假即真。好比小华今天买了一个杯子，小明说:"杯子是白色的"，小亮说:“杯子是红色的”，小华说："小明说的不是真话，小亮说的不是假话"。猜猜小华买的什么颜色的杯子，答案：红色杯子。

**逻辑非操作符值表:**

| A     | !A    |
| ----- | ----- |
| true  | false |
| false | true  |



看看下面代码，变量c的值是什么:

```js
var a=3; 
var b=5; 
var c; 
c=!(b>a);  // b>a值是true,! (b>a）值是false

c=!(b<a);  // b<a值是false, ! (b<a）值是true
```

 

**21、保持先后顺序(操作符优先级）**

我们都知道，除法、乘法等操作符的优先级比加法和减法高，例如：

```js
var numa=3; 
var numb=6 
jq= numa + 30 / 2 - numb * 3;  // 结果为0
```

如果我们要改变运算顺序，需添加括号的方法来改变优先级:

```js
var numa=3; 
var numb=6 
jq= ((numa + 30) / (2 - numb)) * 3; //结果是-24.75
```



**操作符之间的优先级（高到低）:**

```
算术操作符 → 比较操作符 → 逻辑操作符 → "="赋值符号
```

如果同级的运算是按从左到右次序进行,多层括号由里向外。

```js
var numa=3; 
var numb=6; 
jq= numa + 30 >10 && numb * 3<2;  //结果为false
```

[^注]: 部分内容来源网络，寝删
[^参考]: 慕课网|菜鸟笔记

