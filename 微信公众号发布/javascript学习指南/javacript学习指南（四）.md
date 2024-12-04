tags: [#javascript]

#### **61、提取字符串substring()**

substring() 方法用于提取字符串中介于两个指定下标之间的字符。

**语法:**

```
stringObject.substring(startPos,stopPos) 
```

**参数说明:**

| 参数     | 描述                                                         |
| -------- | ------------------------------------------------------------ |
| startPos | 必需。一个非负的整数，开始位置                               |
| stopPos  | 可选。一个非负的整数，结束位置，如果省略该参数，那么返回的字串一直到字符串对象的结尾。 |

**注意：**

1. 返回的内容是从 start开始(包含start位置的字符)到 stop-1 处的所有字符，其长度为 stop 减start。

2. 如果参数 start 与 stop 相等，那么该方法返回的就是一个空串（即长度为 0 的字符串）。

3. 如果 start 比 stop 大，那么该方法在提取子串之前会先交换这两个参数。

使用 substring() 从字符串中提取字符串，代码如下：

```javascript
<script type="text/javascript">  

 var mystr="I love JavaScript";  

document.write(mystr.substring(7));  

document.write(mystr.substring(2,6));

</script>
```

**运行结果:**

```sh
JavaScript love
```

 

#### **62、提取指定数目的字符substr()**

substr() 方法从字符串中提取从 startPos位置开始的指定数目的字符串。

**语法:**

```javascript
stringObject.substr(startPos,length)
```

**参数说明:**

| 参数     | 描述                                                         |
| -------- | ------------------------------------------------------------ |
| startPos | 必需。要提取的字串的起始位置，必须是数值                     |
| stopPos  | 可选。提取字符串的长度。如果省略，返回从stringObject的开始位置startPos到stringObject的结尾字符 |

**注意：**如果参数startPos是负数，从字符串的尾部开始算起的位置。也就是说，-1 指字符串中最后一个字符，-2 指倒数第二个字符，以此类推。

如果startPos为负数且绝对值大于字符串长度，startPos为0。

使用 substr() 从字符串中提取一些字符，代码如下：

```javascript
<script type="text/javascript"> 

 var mystr="I love JavaScript!";

  document.write(mystr.substr(7));  

document.write(mystr.substr(2,4));

</script>
```

**运行结果：**

```
JavaScript! love
```

 

#### **63、Math对象**

Math对象，提供对数据的数学计算。

使用 Math 的属性和方法，代码如下：

```javascript
<script type="text/javascript">  

var mypi=Math.PI;   

var myabs=Math.abs(-15);  

document.write(mypi);  

document.write(myabs);

</script>
```

**运行结果:**

```
3.141592653589793 15
```

**注意：**Math 对象是一个固有的对象，无需创建它，直接把 Math 作为对象使用就可以调用其所有属性和方法。这是它与Date,String对象的区别。

Math 对象属性

| 属性    | 说明                                           |
| ------- | ---------------------------------------------- |
| E       | 返回算术常量e，即自然对数的底数（约等于2.718） |
| LN2     | 返回2的自然对数（约等于0.693）                 |
| LN10    | 返回10的自然对数（约等于2.302）                |
| LOG2E   | 返回以2为底数的e的对数（约等于1.442）          |
| LOG10E  | 返回以10为底数的e的对数（约等于0.434）         |
| PI      | 返回圆周率（约等于3.14159）                    |
| SQRT1_2 | 返回2的平方根的倒数（约等于0.707）             |
| SQRT2   | 返回2的平方根（约等于1.414）                   |

Math 对象方法

| 方法        | 描述                                       |
| ----------- | ------------------------------------------ |
| abs(x)      | 返回数的绝对值                             |
| acos(x)     | 返回数的反余弦值                           |
| asin(x)     | 返回数的反正弦值                           |
| atan(x)     | 返回数的反正切值                           |
| atan2(y, x) | 返回由x轴到点（x,y）的角度（以弧度为单位） |
| ceil(x)     | 对数进行上舍入                             |
| cos(x)      | 返回数的余弦                               |
| exp(x)      | 返回e的指数                                |
| floor(x)    | 对数进行下舍入                             |
| log(x)      | 返回数的自然对数（底数为e）                |
| max(x, y)   | 返回x和y中的最大值                         |
| min(x, y)   | 返回x和y中的最小值                         |
| pow(x, y)   | 返回x的y次幂                               |
| random()    | 返回0~1之间的随机数                        |
| round(x)    | 把数四舍五入为最接近的整数                 |
| sin(x)      | 返回数的正弦                               |
| tan(x)      | 返回角的正切                               |
| sqrt(x)     | 返回数的平方根                             |
| toSource()  | 返回该对象的源代码                         |
| valueOf()   | 返回Math对象的原始值                       |

以上方法不做全部讲解，只讲解部分方法。此节没有任务，快快进入下节学习。

 

#### **64、向上取整ceil()**

ceil() 方法可对一个数进行向上取整。

**语法:**

```
Math.ceil(x)
```

**参数说明:**

| 参数 | 描述                 |
| ---- | -------------------- |
| x    | 必需。必须是一个数值 |



**注意：**它返回的是大于或等于x，并且与x最接近的整数。

我们将把 ceil() 方法运用到不同的数字上，代码如下：

```javascript
<script type="text/javascript">  

document.write(Math.ceil(0.8) + "<br />")   ；

document.write(Math.ceil(6.3) + "<br />")   ；

document.write(Math.ceil(5) + "<br />")   ；

document.write(Math.ceil(3.5) + "<br />")   ；

document.write(Math.ceil(-5.1) + "<br />")   ；

document.write(Math.ceil(-5.9))；

</script>
```

**运行结果：**

```
1 7 5 4 -5 -5
```

 

#### **65、向下取整floor()**

floor() 方法可对一个数进行向下取整。

**语法:**

```
Math.floor(x)
```

**参数说明：**

| 参数 | 描述                 |
| ---- | -------------------- |
| x    | 必需。必须是一个数值 |

**注意：**返回的是小于或等于x，并且与 x 最接近的整数。

我们将在不同的数字上使用 floor() 方法，代码如下:

```javascript
<script type="text/javascript"> 

 document.write(Math.floor(0.8)+ "<br>") ；

document.write(Math.floor(6.3)+ "<br>")；

 document.write(Math.floor(5)+ "<br>")；

 document.write(Math.floor(3.5)+ "<br>")；

 document.write(Math.floor(-5.1)+ "<br>")；

 document.write(Math.floor(-5.9))；

</script>
```

**运行结果：**

```
0 6 5 3 -6 -6
```

 

#### **66、四舍五入round()**

round() 方法可把一个数字四舍五入为最接近的整数。

**语法:**

```
Math.round(x)
```

**参数说明：**

| 参数 | 描述             |
| ---- | ---------------- |
| x    | 必需。必须是数字 |

**注意：**

1. 返回与 x 最接近的整数。

2. 对于 0.5，该方法将进行上舍入。(5.5 将舍入为 6)

3. 如果 x 与两侧整数同等接近，则结果接近 +∞方向的数字值 。(如 -5.5 将舍入为 -5; -5.52 将舍入为 -6),如下图:

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/lip_image112.gif)

把不同的数舍入为最接近的整数,代码如下：

```javascript
<script type="text/javascript">

document.write(Math.round(1.6)+ "<br>");  

document.write(Math.round(2.5)+ "<br>");

document.write(Math.round(0.49)+ "<br>");

document.write(Math.round(-6.4)+ "<br>");

document.write(Math.round(-6.6));

</script>
```

**运行结果：**

```
2 3 0 -6 -7
```

 

#### **67、随机数 random()**

random() 方法可返回介于 0 ~ 1（大于或等于 0 但小于 1 )之间的一个随机数。

**语法：**

```
Math.random();
```

**注意：**返回一个大于或等于 0 但小于 1 的符号为正的数字值。

我们取得介于 0 到 1 之间的一个随机数，代码如下：

```javascript
<script type="text/javascript">  

document.write(Math.random());

</script>
```

**运行结果：**

```
0.190305486195328 
```

**注意:**因为是随机数，所以每次运行结果不一样，但是0 ~ 1的数值。

获得0 ~ 10之间的随机数，代码如下:

```javascript
<script type="text/javascript">  

document.write((Math.random())*10);

</script>
```

**运行结果：**

```
8.72153625893887
```

 

#### **68、Array 数组对象**

数组对象是一个对象的集合，里边的对象可以是不同类型的。数组的每一个成员对象都有一个“下标”，用来表示它在数组中的位置，是从零开始的

**数组定义的方法：**

1. 定义了一个空数组:

var  数组名= new Array();

2. 定义时指定有n个空元素的数组：

var 数组名 =new Array(n);

3. 定义数组的时候，直接初始化数据：

var  数组名 = [<元素1>, <元素2>, <元素3>...];

我们定义myArray数组，并赋值，**代码如下：**

```
var myArray = [2, 8, 6];
```

**说明：**定义了一个数组 myArray，里边的元素是：

```
myArray[0] = 2; myArray[1] = 8; myArray[2] = 6。
```

**数组元素使用：**

```
数组名[下标] = 值;
```

**注意**: 数组的下标用方括号括起来，从0开始。

**数组属性：**

length 用法：<数组对象>.length；返回：数组的长度，即数组里有多少个元素。它等于数组里最后一个元素的下标加一。

**数组方法：**

| 方法             | 描述                                                         |
| ---------------- | ------------------------------------------------------------ |
| contcat()        | 连接两个或者更多的数组，并返回结果                           |
| join()           | 把数组的所有元素放入一个字符串。元素通过指定的分隔符进行分割 |
| pop()            | 删除并返回数组的最后一个元素                                 |
| push()           | 向数组的末尾添加一个或更多元素，并返回新的长度               |
| reverse()        | 颠倒数组中元素的顺序                                         |
| shift()          | 删除并返回数组的第一个元素                                   |
| slice()          | 从某个已有的数组返回选定的元素                               |
| sort()           | 对数组的元素进行排序                                         |
| splice()         | 删除元素，并向数组添加新元素                                 |
| toSource()       | 返回该对象的源代码                                           |
| toString()       | 把数组转换为字符串，并返回结果                               |
| toLocaleString() | 把数组转换为本地数组，并返回结果                             |
| unshift()        | 向数组的开头添加一个或更多元素，并返回新的长度               |
| valueOf()        | 返回数组对象的原始值                                         |

以上方法不做全部讲解，只讲解部分方法。此节没有任务，快快进入下节学习。

 

#### **69、数组连接concat()**

concat() 方法用于连接两个或多个数组。此方法返回一个新数组，不改变原来的数组。

**语法**

```
arrayObject.concat(array1,array2,...,arrayN)
```

**参数说明：**

| 参数   | 说明               |
| ------ | ------------------ |
| array1 | 要连接的第一个数组 |
| ……     | ……                 |
| arrayN | 第N个数组          |

**注意:**  该方法不会改变现有的数组，而仅仅会返回被连接数组的一个副本。

我们创建一个数组，将把 concat() 中的参数连接到数组 myarr 中，代码如下：

```javascript
<script type="text/javascript">  

 var mya = new Array(3);   mya[0] = "1";  

mya[1] = "2";   mya[2] = "3";  

document.write(mya.concat(4,5)+"<br>");  

document.write(mya);

</script>
```

**运行结果：**

```
1,2,3,4,5 1,2,3
```

我们创建了三个数组，然后使用 concat() 把它们连接起来，代码如下：

```javascript
<script type="text/javascript">  

var mya1= new Array("hello!")；

var mya2= new Array("I","love");   

var mya3= new Array("JavaScript","!");   

var mya4=mya1.concat(mya2,mya3);   

document.write(mya4);

</script>
```

**运行结果：**

```
hello!,I,love,JavaScript,!
```

 

#### **70、指定分隔符连接数组元素join()**

join()方法用于把数组中的所有元素放入一个字符串。元素是通过指定的分隔符进行分隔的。

**语法：**

```
arrayObject.join(分隔符)
```

**参数说明:**

| 参数      | 描述                                                         |
| --------- | ------------------------------------------------------------ |
| separator | 可选。指定要使用的分隔符。如果省略该参数，则使用逗号作为分隔符。 |

注意：返回一个字符串，该字符串把数组中的各个元素串起来，用<分隔符>置于元素与元素之间。这个方法不影响数组原本的内容。 我们使用join（）方法，将数组的所有元素放入一个字符串中，代码如下：

```javascript
<script type="text/javascript">  

var myarr = new Array(3);  

myarr[0] = "I";  

myarr[1] = "love";  

myarr[2] = "JavaScript";  

document.write(myarr.join());

</script>
```

**运行结果：**

```
I,love,JavaScript
```

我们将使用分隔符来分隔数组中的元素，代码如下：

```javascript
<script type="text/javascript">  

var myarr = new Array(3)；

myarr[0] = "I"; 

myarr[1] = "love"; 

myarr[2] = "JavaScript"; 

document.write(myarr.join("."));

</script>
```

**运行结果：**

```
I.love.JavaScript
```

 

#### **71、颠倒数组元素顺序reverse()**

reverse() 方法用于颠倒数组中元素的顺序。

**语法：**

```
arrayObject.reverse()
```

**注意：**该方法会改变原来的数组，而不会创建新的数组。

定义数组myarr并赋值，然后颠倒其元素的顺序：

```javascript
<script type="text/javascript">

var myarr = new Array(3) ；

myarr[0] = "1" ；

myarr[1] = "2"  ；

myarr[2] = "3"  ；

document.write(myarr + "<br />") ；

document.write(myarr.reverse())；

</script>
```

**运行结果：**

```
1,2,3 3,2,1
```

 

#### **72、选定元素slice()**

slice() 方法可从已有的数组中返回选定的元素。

**语法**

```
arrayObject.slice(start,end)
```

**参数说明：**

| 参数  | 描述                                                         |
| ----- | ------------------------------------------------------------ |
| start | 必须。规定从何处开始选取。如果是负数，那么它规定从数组尾部开始算起的位置。也就是说，-1指最后一个元素，-2指倒数第二个元素，以此类推 |
| end   | 可选。规定从何处结束选取。该参数是数组片段结束处的数组下标。如果没有指定该参数，那么切分的数组包含从start到数组结束的所有元素。如果这个参数是负数，那么它规定的是从数组尾部开始算起的元素 |

1. 返回一个新的数组，包含从 start 到 end （不包括该元素）的 arrayObject 中的元素。

2. 该方法并不会修改数组，而是返回一个子数组。

**注意：**

1. 可使用负值从数组的尾部选取元素。
2. 如果 end 未被规定，那么 slice() 方法会选取从 start 到数组结尾的所有元素。

3. String.slice() 与 Array.slice() 相似。

我们将创建一个新数组，然后从其中选取的元素，代码如下：

```javascript
<script type="text/javascript">  

var myarr = new Array(1,2,3,4,5,6); 

document.write(myarr + "<br>"); 

document.write(myarr.slice(2,4) + "<br>"); 

document.write(myarr);

</script>
```

**运行结果：**

```
1,2,3,4,5,6 3,4 1,2,3,4,5,6
```

 

#### **73、数组排序sort()**

**sort()**方法使数组中的元素按照一定的顺序排列。

**语法:**

```
arrayObject.sort(方法函数)
```

**参数说明：**

| 参数     | 描述                           |
| -------- | ------------------------------ |
| 方法函数 | 可选。规定排序顺序。必须是函数 |

1.如果不指定<方法函数>，则按unicode码顺序排列。

2.如果指定<方法函数>，则按<方法函数>所指定的排序方法排序。

```
myArray.sort(sortMethod);
```

**注意:** 该函数要比较两个值，然后返回一个用于说明这两个值的相对顺序的数字。比较函数应该具有两个参数 a 和 b，其返回值如下： 

  若返回值<=-1，则表示 A 在排序后的序列中出现在 B 之前。

  若返回值>-1 && <1，则表示 A 和 B 具有相同的排序顺序。

  若返回值>=1，则表示 A 在排序后的序列中出现在 B 之后。

1.使用sort()将数组进行排序，代码如下：

```javascript
<script type="text/javascript">

 var myarr1 = new Array("Hello","John","love","JavaScript");  

var myarr2 = new Array("80","16","50","6","100","1");   document.write(myarr1.sort()+"<br>");

document.write(myarr2.sort());

</script>
```

**运行结果：**

```
Hello,JavaScript,John,love 1,100,16,50,6,80
```

**注意:上面的代码没有按照数值的大小对数字进行排序。**

**2.如要实现这一点，就必须使用一个排序函数，代码如下：**

```javascript
<script type="text/javascript">  

function sortNum(a,b) {  

return a - b;  //升序，如降序，把“a - b”该成“b - a”

 } 

var myarr = new Array("80","16","50","6","100","1"); 

 document.write(myarr + "<br>");  

document.write(myarr.sort(sortNum));

</script>
```

**运行结果：**

```
80,16,50,6,100,1 1,6,16,50,80,100
```

 

#### **74、window对象**

window对象是BOM的核心，window对象指当前的浏览器窗口。

**window对象方法:**

| 方法            | 描述                                           |
| --------------- | ---------------------------------------------- |
| alert()         | 显示带有一段消息和一个确认按钮的警告框         |
| prompt()        | 显示可提示用户输入的对话框                     |
| confirm()       | 显示带有一段消息以及确认按钮和取消按钮的对话框 |
| open()          | 打开一个新的浏览器窗口或者查找一个已命名的窗口 |
| close()         | 关闭浏览器窗口                                 |
| print()         | 打印当前窗口的内容                             |
| focus()         | 把键盘焦点给予一个窗口                         |
| blur()          | 把键盘焦点从顶层窗口移开                       |
| moveBy()        | 可相对窗口的当前坐标把他移动指定的像素         |
| moveTo()        | 把窗口的左上角移动到一个指定的坐标             |
| resizeBy()      | 按照指定的像素调整窗口的大小                   |
| resizeTo()      | 把窗口的大小调整到指定的宽度和高度             |
| scorllBy()      | 按照指定的像素值来滚动内容                     |
| scrollTo()      | 把内容滚动到指定的坐标                         |
| setInterval()   | 每隔指定的时间执行代码                         |
| setTimeout()    | 在指定的延迟时间之后来执行代码                 |
| claerInterval() | 取消setInterval()的设置                        |
| claerTimeout()  | 取消setTimeout()的设置                         |

**注意:**在JavaScript基础篇中，已讲解了部分属性，window对象重点讲解计时器。

 

#### **75、JavaScript 计时器**

在JavaScript中，我们可以在设定的时间间隔之后来执行代码，而不是在函数被调用后立即执行。

**计时器类型：**

一次性计时器：仅在指定的延迟时间之后触发一次。

间隔性触发计时器：每隔一定的时间间隔就触发一次。

**计时器方法：**

| 方法            | 说明                         |
| --------------- | ---------------------------- |
| setTimeout()    | 指定的延迟时间之后来执行代码 |
| clearTimeout()  | 取消setTimeout()设置         |
| setInterval()   | 每隔指定的时间执行代码       |
| claerInterval() | 取消setInterval()设置        |

 

#### **76、计时器setInterval()**

在执行时,从载入页面后每隔指定的时间执行代码。

**语法:**

```
setInterval(代码,交互时间);
```

**参数说明：**

1. 代码：要调用的函数或要执行的代码串。

2. 交互时间：周期性执行或调用表达式之间的时间间隔，以毫秒计（1s=1000ms）。

**返回值:**

一个可以传递给 clearInterval() 从而取消对"代码"的周期性执行的值。

**调用函数格式(**假设有一个clock()函数**):**

setInterval("clock()",1000) 或 setInterval(clock,1000)

我们设置一个计时器，每隔100毫秒调用clock()函数，并将时间显示出来，**代码如下:**

```html
<!DOCTYPE HTML>
<html>
<head>

<meta http-equiv="Content-Type" content="text/html; charset=utf-8">

<title>计时器</title>
<script type="text/javascript">  

var int=setInterval(clock, 100)   ;

function clock(){    

var time=new Date();    

document.getElementById("clock").value = time;

 }

</script>

</head>

 <body> 

 <form>    

<input type="text" id="clock" size="50"  /> 

 </form>

</body>

 </html>
```

 

#### **77、取消计时器clearInterval()**

clearInterval() 方法可取消由 setInterval() 设置的交互时间。

**语法：**

```
clearInterval(id_of_setInterval)
```

**参数说明:**

id_of_setInterval：由 setInterval() 返回的 ID 值。

每隔 100 毫秒调用 clock() 函数,并显示时间。当点击按钮时，停止时间,代码如下:

```html
<!DOCTYPE HTML>
 <html>

<head>

<meta http-equiv="Content-Type" content="text/html; charset=utf-8">

<title>计时器</title>
<script type="text/javascript">   

function clock(){     

​      var time=new Date();                           

document.getElementById("clock").value = time;    }// 每隔100毫秒调用clock函数，并将返回值赋值给i

var i=setInterval("clock()",100);

</script>

</head>

<body>  

<form>    

<input type="text" id="clock" size="50"  />   

​                    <input type="button" value="Stop" onclick="clearInterval(i)"  />

</form>

 </body>

</html>
```

#### 78、计时器setTimeout()

setTimeout()计时器，在载入后延迟指定时间后,去执行一次表达式,仅执行一次。

**语法:**

```
setTimeout(代码,延迟时间);
```

**参数说明：**

1. 要调用的函数或要执行的代码串。

2. 延时时间：在执行代码前需等待的时间，以毫秒为单位（1s=1000ms)。

当我们打开网页3秒后，在弹出一个提示框，**代码如下:**

```html
<html>

 <head>

<script type="text/javascript">  

setTimeout("alert('Hello!')", 3000 );

</script>

</head>

<body>

</body>

</html>
```

当按钮start被点击时，setTimeout()调用函数，在5秒后弹出一个提示框。

```html
<!DOCTYPE HTML>

<html>



<head>

<script type="text/javascript">

function tinfo(){  

var t=setTimeout("alert('Hello!')",5000);

 }

</script>

 </head>

<body>

<form>  

<input type="button" value="start" onClick="tinfo()">

</form>

</body>

</html>
```

要创建一个运行于无穷循环中的计数器，我们需要编写一个函数来调用其自身。在下面的代码，当按钮被点击后，输入域便从0开始计数。

```html
<!DOCTYPE HTML>

<html>

<head>

<script type="text/javascript">

var num=0;

function numCount(){ 

document.getElementById('txt').value=num;

​             num=num+1; 

setTimeout("numCount()",1000);

 }

</script>

</head>

<body>

<form>

<input type="text" id="txt" />

<input type="button" value="Start" onClick="numCount()" />

</form>

</body>

</html>
```

 

#### **79、取消计时器clearTimeout()**

setTimeout()和clearTimeout()一起使用，停止计时器。

**语法:**

clearTimeout(id_of_setTimeout)

**参数说明:**

**id_of_setTimeout：**由 setTimeout() 返回的 ID 值。该值标识要取消的延迟执行代码块。

下面的例子和上节的无穷循环的例子相似。唯一不同是，现在我们添加了一个 "Stop" 按钮来停止这个计数器：

```html
<!DOCTYPE HTML>

<html>

<head>

<script type="text/javascript">  

var num=0,i;  

function timedCount(){    

document.getElementById('txt').value=num;    

num=num+1;    

i=setTimeout(timedCount,1000);  

 }    

setTimeout(timedCount,1000);  

function stopCount(){    

clearTimeout(i);  

 }

</script>

 </head>

 <body>  

<form>    

<input type="text" id="txt">    

<input type="button" value="Stop" onClick="stopCount()">  

</form>

</body>

</html>
```

 

#### 80、History 对象

history对象记录了用户曾经浏览过的页面(URL)，并可以实现浏览器前进与后退相似导航的功能。

**注意 : **从窗口被打开的那一刻开始记录，每个浏览器窗口、每个标签页乃至每个框架，都有自己的history对象与特定的window对象关联。

**语法：**

```
window.history.[属性|方法]
```

**注意：**window可以省略。

**History 对象属性**

| 属性   | 描述                          |
| ------ | ----------------------------- |
| length | 返回浏览器历史列表中的URL数量 |

**History 对象方法**

| 方法        | 描述                              |
| ----------- | --------------------------------- |
| back()      | 加载history列表中的前一个URL      |
| forward（） | 加载history列表中的下一个URL      |
| go()        | 加载history列表中的某个具体的页面 |

使用length属性，当前窗口的浏览历史总长度，**代码如下：**

```html
<script type="text/javascript"> 

​      var HL = window.history.length; 

​      document.write(HL);

</script>
```

[^1]: 部分内容来源网络，侵删
[^2]: 参考：慕课网|菜鸟教程