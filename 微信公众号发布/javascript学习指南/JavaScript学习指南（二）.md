tags: [#javascript]

**21、一起组团（什么是数组）**

我们知道变量用来存储数据，一个变量只能存储一个内容。假设你想存储10个人的姓名或者存储20个人的数学成绩，就需要10个或20个变量来存储，如果需要存储更多数据，那就会变的更麻烦。我们用数组解决问题，一个数组变量可以存放多个数据。好比一个团，团里有很多人，如下我们使用数组存储5个学生成绩。

![](https://gitee.com/sysker/picBed/raw/master/images/image-20200209224526969.png)

数组是一个值的集合，每个值都有一个索引号，从0开始，每个索引都有一个相应的值，根据需要添加更多数值。

 

**22、组团，并给团取个名（如何创建数组）**

使用数组之前首先要创建，而且需要把数组本身赋至一个变量。好比我们出游，要组团，并给团定个名字“云南之旅”。

- **创建数组语法：**

```
var myarray=new Array();
```

  

![](https://gitee.com/sysker/picBed/raw/master/images/image-20200209224636717.png)

​        

 我们创建数组的同时，还可以为数组指定长度，长度可任意指定。

```js
var myarray= new Array(8); //创建数组，存储8个数据。
```



- **注意：**
  - 1.创建的新数组是空数组，没有值，如输出，则显示undefined。
  - 2.虽然创建数组时，指定了长度，但实际上数组都是变长的，也就是说即使指定了长度为8，仍然可以将元素存储在规定长度以外。

 

**23、谁是团里成员（数组赋值）**

数组创建好，接下来我们为数组赋值。我们把数组看似旅游团的大巴车，大巴车里有很多位置，每个位置都有一个号码，顾客要坐在哪个位置呢？ 

第一步：组个大巴车 第二步：按票对号入座         大巴车的1号座位是张三         大巴车的2号座位是李四

- **数组的表达方式：**

第一步：创建数组

```js
var myarr=new Array();  
```



第二步：给数组赋值     

```    js
myarr[1]=" 张三";         myarr[2]=" 李四";
```



下面创建一个数组，用于存储5个人的数学成绩。

```js
var myarray=new Array(); //创建一个新的空数组

myarray[0]=66; //存储第1个人的成绩

myarray[1]=80; //存储第2个人的成绩

myarray[2]=90; //存储第3个人的成绩

myarray[3]=77; //存储第4个人的成绩

myarray[4]=59; //存储第5个人的成绩
```



**注意：**数组每个值有一个索引号，从0开始。

我们还可以用简单的方法创建上面的数组和赋值：

第一种方法：

```js
var myarray = new Array(66,80,90,77,59);//创建数组同时赋值
```



第二种方法：

```js
 var myarray = [66,80,90,77,59];//直接输入一个数组（称 “字面量数组”）
```

**注意：**数组存储的数据可以是任何类型（数字、字符、布尔值等）

 

**24、团里添加新成员（向数组增加一个新元素）**

上一节中，我们使用myarray变量存储了5个人的成绩，现在多出一个人的成绩，如何存储呢？ 

![](https://gitee.com/sysker/picBed/raw/master/images/image-20200209224701329.png)

只需使用下一个未用的索引，任何时刻可以不断向数组增加新元素。

```js
myarray[5]=88; //使用一个新索引，为数组增加一个新元素
```



- 任务

数组中已有三个数值88，90，68，为数组新增加一个元素（第四个），值为99。

 

**25、呼叫团里成员(使用数组元素)**

我们知道数组中的每个值有一个索引号，从0开始，如下图， myarray变量存储6个人的成绩：

 

![](https://gitee.com/sysker/picBed/raw/master/images/image-20200209224723832.png)

 

要得到一个数组元素的值，只需引用数组变量并提供一个索引，如：

**第一个人的成绩表示方法：**myarray[0]

**第三个人的成绩表示方法:** myarray[2]

 

**26、了解成员数量(数组属性length)**

如果我们想知道数组的大小，只需引用数组的一个属性length。Length属性表示数组的长度，即数组中元素的个数。

- **语法：**

```js
myarray.length; //获得数组myarray的长度
```

**注意：**因为数组的索引总是由0开始，所以一个数组的上下限分别是：0和length-1。如数组的长度是5，数组的上下限分别是0和4。

```js
var arr=[55,32,5,90,60,98,76,54];//包含8个数值的数组arr  

document.write(arr.length); //显示数组长度8

document.write(arr[7]); //显示第8个元素的值54

同时，JavaScript数组的length属性是可变的，这一点需要特别注意。

arr.length=10; //增大数组的长度

document.write(arr.length); //数组长度已经变为10
```

数组随元素的增加，长度也会改变，如下:

```js
var arr=[98,76,54,56,76]; // 包含5个数值的数组

document.write(arr.length); //显示数组的长度5

arr[15]=34;  //增加元素，使用索引为15,赋值为34

alert(arr.length); //显示数组的长度16
```

 

**27、二维数组**

一维数组，我们看成一组盒子，每个盒子只能放一个内容。

一维数组的表示: myarray[ ]

二维数组，我们看成一组盒子，不过每个盒子里还可以放多个盒子。

二维数组的表示: myarray[ ][ ]

**注意:** 二维数组的两个维度的索引值也是从0开始，两个维度的最后一个索引值为长度-1。 

- **二维数组的定义方法一**

```js
var myarr=new Array();  //先声明一维 

for(var i=0;i<2;i++){   //一维长度为2   

	myarr[i]=new Array();  //再声明二维   

 	for(var j=0;j<3;j++){   //二维长度为3   

	myarr[i][j]=i+j;   // 赋值，每个数组元素的值为i+j 
	
  } 

}
```

 

**注意:** 关于for 循环语句，请看第四章4-5 。



- **二维数组的定义方法二**

```
var Myarr = [[0 , 1 , 2 ],[1 , 2 , 3]]
```

**3. 赋值**

```
myarr[0][1]=5; //将5的值传入到数组中，覆盖原有值。
```

**说明:** myarr[0][1] ,0 表示表的行，1表示表的列。

 

**28、做判断（if语句）**

if语句是基于条件成立才执行相应代码时使用的语句。

- **语法:**

```
if(条件) { 
条件成立时执行代码
}
```

**注意：if小写，大写字母（IF）会出错！**

假设你应聘web前端技术开发岗位，如果你会HTML技术，你面试成功，欢迎加入公司。代码表示如下:

```js
<script type="text/javascript">  

var mycarrer = "HTML";  

if (mycarrer == "HTML")   {

​    document.write("你面试成功，欢迎加入公司。");  

}

</script>
```

 

**29、二选一 （if...else语句）**

if...else语句是在指定的条件成立时执行代码，在条件不成立时执行else后的代码。

- **语法:**

```
if(条件) { 条件成立时执行的代码} else {条件不成立时执行的代码}
```

假设你应聘web前端技术开发岗位，如果你会HTML技术，你面试成功，欢迎加入公司，否则你面试不成功，不能加入公司。

- **代码表示如下:**

```js
<script type="text/javascript"> 

 var mycarrer = "HTML"; //mycarrer变量存储技能  

if (mycarrer == "HTML")     {

 document.write("你面试成功，欢迎加入公司。");

  }  else { //否则，技能不是HTML

 document.write("你面试不成功，不能加入公司。");

}

</script>
```

 

**30、多重判断（if..else嵌套语句）**

要在多组语句中选择一组来执行，使用if..else嵌套语句。

- **语法:**

```
if(条件1){ 
	条件1成立时执行的代码
}else  if(条件2){
	条件2成立时执行的代码
} ...else  if(条件n){ 
	条件n成立时执行的代码
}else{ 
	条件1、2至n不成立时执行的代码
}
```

假设数学考试，小明考了86分，给他做个评价，60分以下的不及格，60(包含60分)-75分为良好，75(包含75分)-85分为很好，85(包含85分)-100优秀。

**代码表示如下:**

![](https://gitee.com/sysker/picBed/raw/master/images/image-20200209224801275.png)

**结果:**

```
成绩优秀，超级棒
```

**31、多种选择（Switch语句)**

当有很多种选项的时候，switch比if else使用更方便。

**语法:**

```js
switch(表达式){
case值1:
	执行代码块 1  
	break;
case值2:  
	执行代码块 2   
	break;
...case值n:
	执行代码块 n   
	break;
default:
	与 case值1 、 case值2...case值n 不同时执行的代码 
}
```

**语法说明:**

Switch必须赋初始值，值与每个case值匹配。满足执行该 case 后的所有语句，并用break语句来阻止运行下一个case。如所有case值都不匹配，执行**default**后的语句。

假设评价学生的考试成绩，10分满分制，我们按照每一分一个等级将成绩分等，并根据成绩的等级做出不同的评价。

- **代码如下:**

![](https://gitee.com/sysker/picBed/raw/master/images/image-20200209224854626.png)

**执行结果:**

```
评语: 及格，加油!
```

**注意:**记得在case所执行的语句后添加上一个break语句。否则就直接继续执行下面的case中的语句，看以下代码:

![](https://gitee.com/sysker/picBed/raw/master/images/image-20200209224922586.png)

- **执行结果:**

```
评语: 继续努力! 评语: 及格，加油! 评语: 凑合，奋进 评语: 很棒，很棒 评语: 高手，大牛
```

在上面的代码中，没有break停止语句，如果成绩是4分，则case 5后面的语句将会得到执行，同样，case6、7-10后面的语句都会得到执行。

 

**32、重复重复（for循环）**

很多事情不只是做一次，要重复做。如打印10份试卷，每次打印一份，重复这个动作，直到打印完成。这些事情，我们使用循环语句来完成，循环语句，就是重复执行一段代码。

- **for语句结构：**

```js
for(初始化变量;循环条件;循环迭代) {
循环语句   
}
```

假如，一个盒子里有6个球，我们每次取一个，重复从盒中取出球，直到球取完为止。

```js
<script type="text/javascript">

var num=1;

for (num=1;num<=6;num++)  {    //初始化值；循环条件；循环后条件值更新

document.write("取出第"+num+"个球<br />");

}

</script>
```

- **结果:**

![](https://gitee.com/sysker/picBed/raw/master/images/image-20200209224959927.png)

- **执行思路:**

![](https://gitee.com/sysker/picBed/raw/master/images/image-20200209225027023.png)

 

**33、反反复复(while循环)**

和for循环有相同功能的还有while循环, while循环重复执行一段代码，直到某个条件不再满足。

- **while语句结构：**

```js
while(判断条件){     
循环语句  
}
```

使用while循环，完成从盒子里取球的动作，每次取一个，共6个球。

```js
<script type="text/javascript">

var num=0;  //初始化值

 while (num<=6)   { //条件判断   

document.write("取出第"+num+"个球<br />");  

num=num+1;  //条件值更新

}

</script>
```

 

**34、来来回回(Do...while循环)**

do while结构的基本原理和while结构是基本相同的，但是它保证循环体至少被执行一次。因为它是先执行代码，后判断条件，如果条件为真，继续循环。

- **do...while语句结构：**

```js
do{     
循环语句  
}while(判断条件)
```

我们试着输出5个数字。

```js
<script type="text/javascript">   

num= 1;   

 do    {     

document.write("数值为:" +  num+"<br />");     

num++; //更新条件  

 }   while (num<=5)

</script>
```

- **执行结果:**

![](https://gitee.com/sysker/picBed/raw/master/images/image-20200209225052371.png)

为什么呢?我们来看下执行思路：

![](https://gitee.com/sysker/picBed/raw/master/images/image-20200209225106258.png)

 

**35、退出循环break**

在while、for、do...while、while循环中使用break语句退出当前循环，直接执行后面的代码。

- **格式如下：**

```js
for(初始条件;判断条件;循环后条件值更新) {
    if(特殊情况)   {
    break;
    }   
循环代码
}
```

当遇到特殊情况的时候，循环就会立即结束。看看下面的例子，输出10个数，如果数值为5，就停止输出。

 

![](https://gitee.com/sysker/picBed/raw/master/images/image-20200209225126946.png)

- **执行结果:**

![](https://gitee.com/sysker/picBed/raw/master/images/image-20200209225143476.png)

**注:**当num=5的时候循环就会结束，不会输出后面循环的内容。

 

**36、继续循环continue**

continue的作用是仅仅跳过本次循环，而整个循环体继续执行。

- **语句结构：**



```js
for(初始条件;判断条件;循环后条件值更新) {  
    if(特殊情况)   { 
        continue; 
    }  
    循环代码 
}
```

上面的循环中，当特殊情况发生的时候，本次循环将被跳过，而后续的循环则不会受到影响。好比输出10个数字，如果数字为5就不输出了。

![](https://gitee.com/sysker/picBed/raw/master/images/image-20200209225206096.png)

- **执行结果:**

![](https://gitee.com/sysker/picBed/raw/master/images/image-20200209225221047.png)

**注:**上面的代码中，num=5的那次循环将被跳过。

 

**37、什么是函数**

函数的作用，可以写一次代码，然后反复地重用这个代码。

如:我们要完成多组数和的功能。



```js
var sum;    
sum = 3+2; 
alert(sum); 
sum=7+8 ; 
alert(sum);   ....  //不停重复两行代码
```

如果要实现8组数的和，就需要16行代码，实现的越多，代码行也就越多。所以我们可以把完成特定功能的代码块放到一个函数里，直接调用这个函数，就省去重复输入大量代码的麻烦。

- **使用函数完成:**

```js
function add2(a,b){ sum = a + b;  alert(sum); } //  只需写一次就可以

 add2(3,2);

add2(7,8); ....  //只需调用函数就可以
```



**38、定义函数**

如何定义一个函数呢？看看下面的格式：

```js
function 函数名( ){     
函数体;
}
```

function定义函数的关键字，“函数名”你为函数取的名字，“函数体”替换为完成特定功能的代码。

我们完成对两个数求和并显示结果的功能。并给函数起个有意义的名字：“add2”，代码如下：

```js
<script type="text/javascript">  

function add2(){    

    sum = 3 + 2;    

    alert(sum);  

}  

add2();

</script>
```

- **结果:** 

![](https://gitee.com/sysker/picBed/raw/master/images/image-20200209225247357.png)

 

**39、函数调用**

函数定义好后，是不能自动执行的，需要调用它,直接在需要的位置写函数名。

**第一种情况**:在`<script>`标签内调用。

```js
 <script type="text/javascript">   

 function add2()     {         

sum = 1 + 1;        

 alert(sum); 

   } 

 add2();//调用函数，直接写函数名。

</script>
```

**第二种情况:**在HTML文件中调用，如通过点击按钮后调用定义好的函数。

```html
<html>

<head>

    <script type="text/javascript">   

    function add2()    {          sum = 5 + 6;          alert(sum);    }

    </script>

</head>

<body>

    <form>

    <input type="button" value="click it" onclick="**add2()**">  //按钮,onclick点击事件，直接写函数名

    </form>

</body>

</html>
```

注意:鼠标事件会在后面讲解。

 

**40、有参数的函数**

上节中add2()函数不能实现任意指定两数相加。其实，定义函数还可以如下格式：

```js
function 函数名(参数1,参数2) {      
函数代码
}
```

**注意:参数可以多个，根据需要增减参数个数。参数之间用(逗号，）隔开。**

按照这个格式，函数实现任意两个数的和应该写成：

```js
function add2(x,y) {
    sum = x + y;    
    document.write(sum); 
}
```

x和y则是函数的两个参数，调用函数的时候，我们可通过这两个参数把两个实际的加数传递给函数了。

例如，add2(3，4)会求3+4的和，add2(60,20)则会求出60和20的和。

[^1]: 部分内容来源网络侵删
[^2]: 参考内容：慕课网|菜鸟教程

