

### SQL 基础-->常用函数

一、函数的分类

- - SQL函数一般分为两种

- - 单行函数 基于单行的处理，一行产生一个结果

- - 多行函数 基于多行的处理，对多行进行汇总，多行产生结果

 

二、函数形式

```
    function_name [(arg1, arg2,...)]
```
 

三、常用的单行函数：

 1. 字符函数：

```
    lower(x)   转小写

   

    upper(x)   转大写

   

    initcap(x) 单词首字母转大写

   

    concat(x,y)   字符连接与| | 功能类似

   

    substr(x,start [,length])   取子串

        格式: substr('asdfasdfasdfasddf',1,3)

   

    length(x)  取字符串长度

   

    lpad | rpad(x,width [,pad_string]) 字符定长，（不够长度时，左｜右填充）

 

    trim([trim_charFROM] x)  删除首部、尾部字符

         格式：trim('h' from 'hello hello')

               trim 默认删除方式是both

               leading   只删首部   trim(leading 'h' from 'hello helloh')

               trailing  只删尾部   trim(trailing 'h' from 'hello helloh')

        

              ltrim(x[,trim_string])  从x右边删除字符  等价于使用trailing

              rtrim(x[,trim_string])  从x左边删除字符  等价于使用leading

        

    instr   返回子字符串在字符串中的位置

         格式：instr(string,substring,position,occurence)

   

    replace(x,search_string,replace_string)   字符替换

        格式：replace('字符', '字符' ,'字符')

         将字符中的字符，替换成字符
```
 

2.  数值函数：

```
    round(x [,y])      四舍五入

    trunc(x,[,y])       截断

    mod(m,n)            求余

    ceil(x)                 返回特定的最小数（大于等于x的最小整数）

    floor(x)            返回特定的最大数（小于等于x的最大整数）
```
 

 

3.  日期函数：

```
    sysdate    返回系统当前日期

       

    实际上ORACLE内部存储日期的格式是：世纪，年，月，日，小，分钟，秒。

    不管如何输入都这样

    9i开始，默认的日期格式是：DD-MON-RR,之前是DD-MON-YY

    RR 和YY 都是世纪后的两位，但有区别

    ORACLE的有效日期范围是：公元前年月日－年月日

 

 

    RR日期格式：

      1、如果当前年份最后两位是：－，并且指定年份的最后两位也为－，

        则返回本世纪

       例：当前年：， 01－－，表示2008 年

      2、如果当前年份最后两位是：－，指定年份最后两位为50－

        则返回上世纪。

       例：当前年：，01－－，表示1998

 

      3、如果当前年最后两位为：－，指定年份最后两位为0－，

        则返回下世纪。

       例：当前年：，－－表示的是年

 

      4、如果当前年最后两位是：－，指定年份最后两位为：－

        则返回本世纪。

       例：当前年：，－－表示的是年

 

 

    months_between(x，y） 两个日期之间相差的月数

       例：查询最近个月入职的员工

 

    add_months(x,y)      返回x上加上y个月后的结果

   

    last_day(x)           返回指定日期所在月最后一天的日期

   

    next_day(x，day)    返回指定日期的下一day的时间值，day是一个文本串，比如SATURDAY

   

    extract       提取日期

       select extract(day from sysdate) from dual

       select extract(month from sysdate) from dual;

       select extract(year from sysdate) from dual;

   

 
```

4.  转换函数：

```
    TO_DATE(char[, 'format_model']) TO_DATE函数将一个字符串转换成日期格式

                                    函数有个fx 修饰语。这个修饰语为TO_DATE函数的字符函

                                    数中的独立变量和日期格式指定精确匹配.

   

    TO_CHAR(date, 'format_model')   转换为CHAR类型，

                                    必须与单引号一起嵌入，区分大小写，

                                用逗号把日期数值分开，有一个fm 移除填补空白或者阻止零开头

    TO_CHAR(number, 'format_model')

   

    TO_NUMBER(char[, 'format_model'])  TO_NUMBER 函数将一个字符串转换成一个数字格式:

   

    select to_date('1999-09-23','yyyy-mm-dd') from dual;

   

    数据类型的转换分为隐式数据类型转换和显式数据类型转换

   

    在表达式中, Oracle服务器能自动地转换下列各项，即隐式转换:

     VARCHAR2 or CHAR  =====〉NUMBER

     VARCHAR2 or CHAR  =====〉DATE

 

    对表达式赋值, Oracle服务器能自动地转换下列各项，即隐式转换:

    NUMBER =======〉VARCHAR2 or CHAR

    DATE   =======〉VARCHAR2 or CHAR

   

   

    日期格式元素：

       YYYY   数字年份

       YEAR   英文年份

   

       MM  数字月

       MONTH  英文月

       MON 英文缩写

   

       DD  数字日

       DY  英文缩写

       DAY 英文

 ```

 

5.  通用函数

```
    decode 条件判断

    格式：decode (col|expression,search1,result1 [,search2,result2,...] [,default])

       判断col|exporession的值，当search1匹配时，则返回，result1,

       与search2匹配时，返回result2 ... 如果都不匹配，返回default。

 

 

    select EMPNO,ENAME,JOB,SAL,

    decode(job,'CLERK',SAL*1.15,'SALESMAN',SAL*1.1,SAL*1.12) NEW_SAL

    FROM SCOTT.EMP;

 

    if then else  条件判断

    case 表达式

       CASE expr WHEN comparison_expr1 THEN return_expr1

                 [WHEN comparison_expr2 THEN return_expr2

                 WHEN comparison_exprn THEN return_exprn

                 ELSE else_expr]

       END

 
```

四、演示*/ 

``` 

--lower函数

SQL> select lower('SQL') from dual;

 

LOW

---

sql

 

SQL> select EMPNO,ENAME,JOB from scott.emp where lower(ename) like 'a%';

 

     EMPNO ENAME      JOB

---------- ---------- ---------

      7499 ALLEN      SALESMAN

      7876 ADAMS      CLERK

 

SQL> insert into scott.emp(empno,ename) values(9999,'albert');

 

1 row created.

 

SQL> select * from scott.emp where lower(ename) like 'a%';

 

     EMPNO ENAME      JOB              MGR HIREDATE          SAL       COMM     DEPTNO

---------- ---------- --------- ---------- ---------- ---------- ---------- ----------

      9999 albert

      7499 ALLEN      SALESMAN        7698 1981-02-20       1600        300         30

      7876 ADAMS      CLERK           7788 1987-05-23       1100                    20

 

SQL> select * from scott.emp where ename like 'A%';

 

     EMPNO ENAME      JOB              MGR HIREDATE          SAL       COMM     DEPTNO

---------- ---------- --------- ---------- ---------- ---------- ---------- ----------

      7499 ALLEN      SALESMAN        7698 1981-02-20       1600        300         30

      7876 ADAMS      CLERK           7788 1987-05-23       1100                    20

 

--upper函数  

SQL> select upper('SQL Course') as Upper_Char from dual;

 

UPPER_CHAR

----------

SQL COURSE

 

--单词首子母转大写

SQL> select initcap(ename) as initcap_name scott.emp where ename = 'albert';

 

INITCAP_NAME

----------

Albert

 

--字符的拼接,||与concat等效

SQL> select ename || ' is an  ' || job from scott.emp where ename = 'SCOTT';

 

ENAME||'ISAN'||JOB

---------------------------

SCOTT is an  ANALYST

 

SQL> select concat(concat(ename,' is an '),job) as concat_str from scott.emp where ename = 'SCOTT';

 

CONCAT_STR

--------------------------

SCOTT is an ANALYST

 

--SUBSTR，截取子串，下面的例子从第个位置开始连续截取个字符

SQL> select substr('HelloWorld',2,3) from dual;

 

SUB

---

ell

 

--LENGTH 取字符串长度

SQL> select length('HelloWord') as String_length from dual;

 

STRING_LENGTH

-------------

            9

 

-- lpad | rpad 字符串的填充

-- lpad，左填充，直到达到指定长度为止

SQL> select lpad('salary',10,'*') as String_Lpad from dual;

 

STRING_LPA

----------

****salary

 

--指定长度为，多出的部分被截断

SQL> select lpad('salary',4,'*') as String_Lpad from dual;

 

STRI

----

sala

 

--rpad，右填充，直到达到指定长度为止

SQL>  select rpad('salary',10,'|') as String_Rpad from dual;

 

STRING_RPA

----------

salary||||

 

--指定长度为，多出的部分被截断

SQL>  select rpad('salary',5,'|') as String_Rpad from dual;

 

STRIN

-----

salar

 

-- trim 删除首尾字符，格式：trim('h' from 'hello hello')，默认的方式为both

SQL> select trim('h' from 'hello helloh') as String_Trim  from dual;

 

STRING_TRI

----------

ello hello

 

-- trim 删除首尾字符，指定leading只删首部

SQL> select trim(leading 'h' from 'hello helloh') as Trim_Leading from dual;

 

TRIM_LEADIN

-----------

ello helloh

 

-- trim 删除首尾字符，指定trailing只删尾部

SQL> select trim(trailing 'h' from 'hello helloh') as Trim_Trailling from dual;

 

TRIM_TRAILL

-----------

hello hello

 

--rtrim ,ltrim

SQL> select rtrim('hello helloh','h') as Rtrim_String ,        

  2  ltrim('hello helloh','h') as Ltrim_String

  3  from dual;

 

RTRIM_STRIN LTRIM_STRIN

----------- -----------

hello hello ello helloh

 

--replace 字符替换

SQL> select replace('Jack and Johnson','J','Bl') as String_Replace from dual;

 

STRING_REPLACE

------------------

Black and Blohnson

 

--instr 下面的示例从第个字符开始，返回第二个OR的位置

SQL> select instr('CORPORATE FOLLOR','OR',3,2) as Instring from dual;

 

  INSTRING

----------

        15

   

--round 四舍五入函数

SQL> select round(102.253,2)  as round_func from dual;

 

ROUND_FUNC

----------

    102.25

 

SQL> select round(102.253,0)  as round_func from dual;

 

ROUND_FUNC

----------

       102

 

SQL> select round(102.253,-1)  as round_func from dual;

 

ROUND_FUNC

----------

       100

 

--trunc 截断函数

SQL> select trunc(2010.328) as trunc_func_1,

  2  trunc(2010.328,1) as trunc_func_2,

  3  trunc(2010.328,-1) as trunc_func_3

  4  from dual;

 

TRUNC_FUNC_1 TRUNC_FUNC_2 TRUNC_FUNC_3

------------ ------------ ------------

        2010       2010.3         2010

 

--#MOD(m,n) 取余函数

SQL> select mod(2010,3) as mod_func from dual;

 

  MOD_FUNC

----------

         0

 

SQL> select mod(5,3) as mod_func from dual;

 

  MOD_FUNC

----------

         2

 

--ceil(x) 返回特定的最小数（大于等于x的最小整数）

SQL> select ceil(593.3) as ceil_func from dual;

 

 CEIL_FUNC

----------

       594

 

--floor(x)  返回特定的最大数（小于等于x的最大整数）    

SQL> select floor(593.4) as floor_func from dual;

 

FLOOR_FUNC

----------

       593

 

--month_between(日期，日期)两个日期相差的月数

SQL> select empno,ename,job,months_between(sysdate,hiredate) as diff_month from scott.emp;

 

     EMPNO ENAME      JOB       DIFF_MONTH

---------- ---------- --------- ----------

      9999 albert

      7369 SMITH      CLERK     351.370601

      7499 ALLEN      SALESMAN  349.273827

      7521 WARD       SALESMAN  349.209311

      7566 JONES      MANAGER   347.854472

      7654 MARTIN     SALESMAN         342

      7698 BLAKE      MANAGER    346.88673

      7782 CLARK      MANAGER   345.628666

      7788 SCOTT      ANALYST   275.306085

      7839 KING       PRESIDENT 340.370601

      7844 TURNER     SALESMAN  342.660924

 

SQL> select * from scott.emp where months_between(sysdate,hiredate) <= 300;

 

     EMPNO ENAME      JOB              MGR HIREDATE          SAL       COMM     DEPTNO

---------- ---------- --------- ---------- ---------- ---------- ---------- ----------

      7788 SCOTT      ANALYST         7566 1987-04-19       3000                    20

      7876 ADAMS      CLERK           7788 1987-05-23       1100                    20

     

--add_months(日期,n)  返回在指定的日期后，加上n个月后的日期

SQL> select add_months(sysdate,5) from dual;

 

ADD_MONTHS

----------

2010-08-28

 

--last_day(sysdate)      返回指定日期所在月最后一天的日期

SQL> select last_day(sysdate) from dual;

 

LAST_DAY(S

----------

2010-03-31

 

--next_day 返回指定日期的下一day的时间值，day是一个文本串，比如SATURDAY

SQL> select next_day('05-FEB-2005','TUESDAY') as nextday from dual;

 

NEXTDAY

---------

08-FEB-05

 

/*EXTRACT*/

 

SQL> select extract(day from sysdate) from dual;

 

EXTRACT(DAYFROMSYSDATE)

-----------------------

                     28

 

SQL> select extract(month from sysdate) from dual;

 

EXTRACT(MONTHFROMSYSDATE)

-------------------------

                        3

 

SQL> select extract(year from sysdate) from dual;

 

EXTRACT(YEARFROMSYSDATE)

------------------------

                    2010

 

--使用ROUND 和TRUNC函数处理日期

--round(sysdate,'MONTH') 当月第一天

--round(sysdate,'YEAR')  当年的第一天

--trunc(sysdate,'MONTH') 当月第一天

--trunc(sysdate,'YEAR')  当年的第一天

SQL> select sysdate,round(sysdate,'MONTH'),round(sysdate,'YEAR'),                           

  2  trunc(sysdate,'MONTH'),trunc(sysdate,'YEAR')

  3  from dual;

 

SYSDATE   ROUND(SYS ROUND(SYS TRUNC(SYS TRUNC(SYS

--------- --------- --------- --------- ---------

15-APR-10 01-APR-10 01-JAN-10 01-APR-10 01-JAN-10

          

 

--类型转换

-- to_char

SQL> select empno,ename,hiredate,to_char(hiredate,'fmDD Month YYYY') as hiredate2,

  2    to_char(hiredate,'DD MM YYYY') as hiredate3

  3  from scott.emp

  4  where sal > 2500;

 

     EMPNO ENAME      HIREDATE  HIREDATE2         HIREDATE3

---------- ---------- --------- ----------------- ----------

      7566 JONES      02-APR-81 2 April 1981      02 04 1981

      7698 BLAKE      01-MAY-81 1 May 1981        01 05 1981

      7788 SCOTT      19-APR-87 19 April 1987     19 04 1987

      7839 KING       17-NOV-81 17 November 1981  17 11 1981

      7902 FORD       03-DEC-81 3 December 1981   03 12 1981

 

SQL> select to_char(12345.67) as char1,to_char(12345.67,'99,999.99') as char2

  2  from dual;

 

CHAR1    CHAR2

-------- ----------

12345.67  12,345.67

 

--当被转换的数据位数超过格式指定位数，则出现错误。

SQL> select to_char(12345678.90,'99,999.99') as char1 from dual;

 

CHAR1

----------

##########

 

--to_number

SQL> select to_number('970.13') as number1,

  2    to_number('970.13') + 35.5 as nunber2,

  3    to_number('-$12,345.67','$99,999.99') as number3

  4  from dual;

 

   NUMBER1    NUNBER2    NUMBER3

---------- ---------- ----------

    970.13    1005.63  -12345.67

   

--to_date

--注意：最终日期采用默认格式DD-MON—YY显示

SQL> select to_date('05-JUL-2008') as date1,to_date('05-JUL-08') as date2,

  2  to_date('July 5,2008','MONTH DD,YYYY') as date3,

  3  to_date('7.4.08','MM.DD.YY') as date4

  4  from dual;

 

DATE1     DATE2     DATE3     DATE4

--------- --------- --------- ---------

05-JUL-08 05-JUL-08 05-JUL-08 04-JUL-08

 

--case when

SQL> select empno,ename,sal,deptno,case deptno when 20 then 1.10 * sal

  2    when 30 then 1.20 * sal

  3    else 1.30 * sal end as newsal

  4  from scott.emp order by deptno;

 

     EMPNO ENAME             SAL     DEPTNO     NEWSAL

---------- ---------- ---------- ---------- ----------

      7782 CLARK            2450         10       3185

      7839 KING             5000         10       6500

      7934 MILLER           1300         10       1690

      7566 JONES            2975         20     3272.5

      7902 FORD             3000         20       3300

      7876 ADAMS            1100         20       1210

      7369 SMITH             800         20        880

      7788 SCOTT            3000         20       3300

      7521 WARD             1250         30       1500

      7844 TURNER           1500         30       1800  

     

/*DECODE*/

SQL> select empno,ename,job,sal, decode(job,'CLERK',sal*1.5,'SALESMAN',sal*1.1,sal*1.2) as newsal from scott.emp;

 

     EMPNO ENAME      JOB              SAL     NEWSAL

---------- ---------- --------- ---------- ----------

      9999 albert

      7369 SMITH      CLERK            800       1200

      7499 ALLEN      SALESMAN        1600       1760

      7521 WARD       SALESMAN        1250       1375

      7566 JONES      MANAGER         2975       3570

      7654 MARTIN     SALESMAN        1250       1375

      7698 BLAKE      MANAGER         2850       3420

      7782 CLARK      MANAGER         2450       2940

      7788 SCOTT      ANALYST         3000       3600

      7839 KING       PRESIDENT       5000       6000

      7844 TURNER     SALESMAN        1500       1650
      
```      