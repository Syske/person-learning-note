tags: [#db, #mysql]

#### 1、规范：
  - （1）、关键字与函数名称全部大写
  
  - （2）、数据库名称、表名称、字段名称全部小写
  
  - （3）、SQL语句必须的分号结尾

##### 数据的定义

 -  **数据库**是长期存储在计算机内有组织、有共享、同一管理的数据集合；

 -  **数据库包含两层含义：** 保管数据的“仓库”；数据管理的方法和技术。

 #### 2、数据库操作

- 显示所有数据库
```
  SHOW {DATABASES | SCHEMAS}; 
```
- 创建数据库
```
  CREATE {DATABASE | SCHEMA} [IF NOT EXOSTS] db_name [DEFAULT] CHATABASER SET [=] charset_name;
```
- 打开数据库：

```
 use DATABASE db_name;
```
- 修改数据库
```  
 ALTER {DATABASE | SCHEMA} [IF NOT EXISTS] db_name [DEFAULT] CHARACTER SET [=] charset_name;
```

- 删除数据库
``` 
  DROP {DATABASE | SCHEMA } [IF EXISTS] db_name; 
```

#### 2、数据类型：

- （1）整数：
 - -   TINYINT

  - - - 有符号：-128到127（ -2^7 到 2^7-1 )

  - - - 无符号：0到255（ 0 到 2^8-1 )


 - - SMALLINT 

  - - - 有符号：-32768到32767（-2^15 到 2^15-1）

  - - - 无符号：0到65535（0 到 2^16-1）

 - - MEDIUMINT
  
  - - - 有符号：-8388608到8388607（-2^23 和 -2^23-1） 

  - - - 无符号：0到16777215（0 和 -2^24-1）  

 - - INT 

  - - - 有符号：-2147483648到2147483648（-2^31 到 2^31-1） 

  - - - 无符号：0到429867295（0 到 2^32-1）  

 - -  BIGINT

  - - -  有符号：-92337203685775808到92337203685775807（-2^63 到 2^63-1）

  - - -  无符号：0到18446744073709551615（0 到 2^64-1）

![整型](https://images2015.cnblogs.com/blog/1077694/201703/1077694-20170311225051639-369807763.png)

- （2）浮点型：

![浮点型](https://images2015.cnblogs.com/blog/1077694/201703/1077694-20170311225139404-1349360575.png)

- （3）日期型：

![日期型](https://images2015.cnblogs.com/blog/1077694/201703/1077694-20170311225226498-906714820.png)

- （4）字符型：

![字符型](https://images2015.cnblogs.com/blog/1077694/201703/1077694-20170311225302154-1152169217.png)

> char(M)是定长字符，如果创建时为char(5),存储的数据为3位，则剩余2位会自动补0；

>  VARVHAR(M)是可变字符，如果创建时为 VARVHAR(5),存储的数据为3位，则存储的为3位；

#### 3、数据表操作：

##### （1）、创建表：

```sql

CREATE TABLE [IF NOT EXISTS] table_name(column_name1 data_type , column_name2 data_type , ……)ENGINE=InnoDB DEFAULT CHARSET=utf8;

```

##### （2）、查看当前数据库表列表：

```sql

SHOW TABLES [FROM db_name];
　　
```

##### （3）、查看表结构：

```sql
// 1、方式一
SHOW COLUMNS FROM table_name;

// 2、方式二
desc table_name;

```

##### （4）、向数据表中插入数据：

```sql
INSERT [INTO]  tb_name  [(col_name1,col_name2,……)]  VALUES(val1,val2,……);

```

##### （5）、查询表数据：

```sql
// 方法一 查询所有数据
SELECT * FROM tb_name;

// 方法二 查询部分数据
SELECT column_name1,column_name2,... FROM tb_name;


```
##### （6）、查看索引：

```sql
SHOW INDEXES FROM table_name \G;

```
##### （7）、修改表格的字符编码：

```
alter table {table_name} default character set utf8;
```
##### （8）、修改表格中字段的字符编码：

```
// 修改单个字段字符编码
alter table {table_name} change {字段名} {字段名} {字段定义 varchar(50)} character set utf8;

// 修改表格中所有的字段的字符编码
ALTER TABLE tbl_name CONVERT TO CHARACTER SET charset_name; 
ALTER TABLE pmy CONVERT TO CHARACTER SET utf8; 
```

- 警告： 

> 上述操作是在字符集中转换列值。如果用户在字符集（如 gb2312）中有一个列，但存储的值使用的是其它的一些不兼容的字符集（如 utf8），那么该操作将不会得到用户期望的结果。在这种情况下，用户必须对每一列操作

##### （9）、修改字段默认值

修改：

```sql
ALTER TABLE 表名 ALTER COLUMN 字段名 SET DEFAULT 默认值
```

删除：

```sql
ALTER TABLE 表名 ALTER COLUMN 字段名 DROP DEFAULT
```


####  4、约束：

　　（1）、非空约束：  NOT NULL;

　　（2）、自动编号： AUTO_INCREMENT（必须与主键约束组合使用）;

　　（3）、主键约束： PRIMARY KEY（保证数据的唯一性，主键自动为NOT NULL，每个数据表只能有一个主键）;

　　（4）、唯一约束： UNIQUE KEY（可以保证数据的唯一性，唯一约束的字段可以为空值，每一个数据表可以有多个唯一约束）;

　　（5）、默认值： DEFAULT.

　　（6）、外键约束： FOREIGN KEY（保证数据的一致性、完整性，实现一对一或一对多关系），需要满足以下4个条件：

①父表和子表必须使用相同的存储引擎，而且禁止使用临时表；

②数据表的存储引擎只能是InnoDB；

③外键和参照列必须具有相似的数据类型，其中数字的长度或者是否有符号位必须相同，而字符的长度则可以不同；

④外键列和参照列必须创建索引，如果外键列不存在索引的话，MYSQL将自动创建索引。

外键约束的操作：

```
　FOREIGN KEY (col_name) REFERENCES foreign_key_table_name(col_name)  [ON DELETE | UPDATE ]  [CASCADE | SET NULL | RESRTICT | NO ACTION]
```
   - 其中，CASCADE表示从父表中删除或更新且自动删除或更新子表中匹配的行，SET NULL表示从父表中删除或更新行并设置子表中的外键列位空（如果使用该选项必须保证子表外键列没有指定NOT NULL），RESTRICT表示拒绝对父表的删除或更新操作，NO ACTION表示无动作（标准的SQL的关键字，在mysql中和RESTRICT相同）。

  - 表级约束在列定义后声明，列约束前后声明均可

#### 5、数据表创建后的操作：

　　（1）、添加单列：

```sql
ALTER TABLE table_name ADD [COLUMN] col_name  column_definition [FIRST | AFTER col_name];
```

　　（2）、添加多列：

```sql
ALTER TABLE table_name ADD [COLUMN] (col_name column_definition,col_name2 column_definition,……);
```

　　（3）、删除列：

```sql
ALTER TABLE table_name DROP [COLUMN]  col_name;

```
　　（4）、删除多列：

```sql
ALTER TABLE tabla_name DROP [COLUMN] col_name1,DROP [COLUMN] col_name2,……;

```
　　（5）、添加主键约束（[constraint [symbol]]为约束的名字）：

```sql
ALTER TABLE talbe_name ADD [constraint [symbol]] PRIMARY KEY [index_type](index_col_name,……);
　　
```
　　（6）、添加唯一约束：

```sql
ALTER TABLE table_name ADD [constraint [symol]] UNIQUE [INDEXE | KEY] [index_name ] [index_type] (inde_col_name,……);
// inde_col_name字段名必须加括号
```
　　（7）、添加外键约束：

```sql
ALTER TABLE table_name ADD [COSTRAINT[symbol]] FOREIGN KEY [index_name] (index_col,……);
　　
```
　　（8）、添加、删除默认约束：

```sql
ALTER TABLE table_name ALTER [COLUMN] col_name {SET DEFAULT default_val | DROP PRIMARY KEY} ;
　　
```
　　（9）、删除主键约束：

```sql
ALTER TABLE table_name DROP PRIMARY KEY;
　　
```
　　（10）、删除唯一约束或索引：

```sql
ALTER TABLE table_name DROP {INDEX | KEY} index_name;
　　
```
　　（11）、删除外键约束：

```sql
ALTER TABLE table_name DROP FOREIGN KEY fk_symbol;
　　
```
　　（12）、修改列定义：

```sql
ALTER TABLE table_name MODIFY [COLUMN] col_name colum_definition [FIRSST | AFTER col_name];
　　
```
　　（13）、修改列名称（可以修改列名称）：

```sql
ALTER TABLE table_name CHANGE [COLUMN] old_col_name new_col_name column_definition [FIRST AFTER col_name];
　　　
```
　　　（14）、数据表更名：

```sql
//方法一：
 
ALTER TABLE table_name RENAME [TO | AS] new_table_name;
 
//方法二：
 
RENAME TABLE table_name1 TO new_table_name1 ,[table_name2 TO new_table_name2],……;

```
（15）、查询某一范围的记录：

```sql
// 查询某个表中，某列值在value1~value2范围间的记录
SELECT * FROM table_name WHERE column_name BETWEEN value1 AND value2;

// 例如： 查询student表的第2条到4条记录
SELECT * FROM student WHERE id BETWEEN 902 AND 904;
```
（16）、查询某匹配值的记录：

```sql
// 查询匹配值记录
SELECT * FROM table_name WHERE column_name IN( value1,value2,...);

```

（17）、查询某字段中各个值出现的次数：

```sql
SELECT column_name,COUNT(column_name) FROM table_name GROUP BY column_name;

// 例如：从student表中查询每个院系有多少人

SELECT department,COUNT(department) FROM student GROUP BY department;
```

（18）、查询某字段中最大值：

```sql
SELECT column_name,MAX(column_name) FROM table_name GROUP BY column_name;

// 例如：从score表中查询每个科目的最高分
SELECT c_name,MAX(grade) FROM score GROUP BY c_name;
```

（19）、查询某字段中最大值：

```sql
SELECT column_name,SUM(column_name) FROM table_name GROUP BY column_name;

// 例如：计算每个学生的总成绩
SELECT stu.name,SUM(s.grade) FROM score s,student stu WHERE stu.id = s.stu_id GROUP BY stu.name;
```

（20）、查询某字段中平均值：

```sql
SELECT column_name,AVG(column_name) FROM table_name GROUP BY column_name;

// 例如：计算每个考试科目的平均成绩
SELECT s.c_name,AVG(s.grade) FROM score s,student stu WHERE stu.id = s.stu_id GROUP BY s.c_name;
```

（21）、多表交叉查询：

```
SELECT table1_alias.column_name1,table1_alias.column_name2,...,
table2_alias.column_name1,table2_alias.column_name2,...
FROM table_name1 table1_alias, table2 table2_alias  
WHERE exp;

// 例如：查询李四的考试科目（c_name）和考试成绩（grade）
SELECT s.c_name,s.grade FROM score s,student stu WHERE stu.name='李四' AND stu.id = s.stu_id;
```
（22）、按某个字段进行排序：

```
SELECT table1_alias.column_name1,table1_alias.column_name2,...,
table2_alias.column_name1,table2_alias.column_name2,...
FROM table_name1 table1_alias, table2 table2_alias  
WHERE exp ORDER BY column_name;

 //核心代码
ORDER BY column_name

 // 例如： 将计算机考试成绩按从高到低进行排序
SELECT stu.id,stu.name,s.grade FROM score s,student stu 
WHERE s.c_name ='计算机' AND s.stu_id = stu.id
ORDER BY grade; 

```

（23）、按模糊查询某字段(一个字段多个匹配值)：

```
SELECT table1_alias.column_name1,table1_alias.column_name2,...,
table2_alias.column_name1,table2_alias.column_name2,...
FROM table_name1 table1_alias, table2 table2_alias  
WHERE SUBSTR(column_name,pos,len) IN (vaule1,value2,...);

 // 例如：查询姓张或者姓王的同学的姓名、院系和考试科目及成绩
SELECT stu.name,stu.department,s.c_name,s.grade FROM score s,student stu WHERE stu.id=s.stu_id AND SUNSTR(stu.name,1,1) IN('张','王');
SELECT stu.name,stu.department,s.c_name,s.grade FROM score s,student stu WHERE stu.id=s.stu_id AND (stu.name like'张%' or stu.name like '王');
 
```

（24）、知识点：
- || ：字符串拼接，相当于java中的+
- 字符串中含有单引号时，用两个单引号表示
- distinct:字段前加该关键字，消除该字段下的重复值（可以同时修饰多个字段，表示消除两个字段的组合的重复值）；
- escape : 通过该关键字自定义转义字符，如 name like '王%$%%'escape '$';
- SELECT LAST_INSERT(); 获取增长后的主键
- 分页操作：统一使用LIMIT进行，即：在所有查询语句的最后一块写上LIMIT，语法如下：
```
查询 LIMIT 开始行,长度

// 查询1~5条记录
SELECT * FROM news WHERE 1=1 LIMIT 0,5;
```
（25）、常用函数：

