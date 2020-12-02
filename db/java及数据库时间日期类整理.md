#### java中常用的日期类：

 > java.util.Date
 
 - 一个包装了毫秒值的瘦包装器 (thin wrapper)，它允许 JDBC 将毫秒值标识为 SQL DATE 值。毫秒值表示自 1970 年 1 月 1 日 00:00:00 GMT 以来经过的毫秒数。 
 - 为了与 SQL DATE 的定义一致，由 java.sql.Date 实例包装的毫秒值必须通过将时间、分钟、秒和毫秒设置为与该实例相关的特定时区中的零来“规范化”。  
 
 - **常用方法**（已过时的方法除外）
 
 - >public long getTime()
 
 - >public long setTime(long)
 
 - > public static Date valueOf(String s)

 - 使用给定毫秒时间值设置现有 Date对象。如果给定毫秒值包含时间信息，则驱动程序会将时间组件设置为对应于零 GMT 的默认时区（运行应用程序的 Java 虚拟机的时区）中的时间。

 - > public String toString()
 - 格式化日期转义形式 yyyy-mm-dd 的日期。 
 - - 注：要为 SimpleDateFormat 类指定一个日期格式，可以使用 "yyyy.MM.dd" 格式，而不是使用 "yyyy-mm-dd" 格式。在 SimpleDateFormat 的上下文中，"mm" 表示分钟，而不是表示月份。例如： 
```
  格式模式                                结果
  --------------                         -------
        "yyyy.MM.dd G 'at' hh:mm:ss z"    ->>  1996.07.10 AD at 15:08:56 PDT

```

 > java.text.SimpleDateFormat

 - SimpleDateFormat 是一个以与语言环境相关的方式来格式化和分析日期的具体类（DateFormat的直接实现类）。它允许进行格式化（日期 -> 文本）、分析（文本 -> 日期）和规范化。 
 



字母 | 日期或时间元素 | 表示 | 示例  
---|---|---|---
G | Era 标志符|  Text|  AD  
y | 年 | Year|  1996; 96  
M | 年中的月份|  Month | July; Jul; 07  
w | 年中的周数|  Number | 27  
W | 月份中的周数|  Number | 2  
D | 年中的天数|  Number | 189  
d | 月份中的天数|  Number | 10  
F | 月份中的星期|  Number | 2  
E | 星期中的天数|  Text | Tuesday; Tue  
a | Am/pm 标记 | Text | PM  
H | 一天中的小时数（0-23）|  Number | 0  
k | 一天中的小时数（1-24）|  Number | 24  
K | am/pm 中的小时数（0-11）|  Number | 0  
h | am/pm 中的小时数（1-12）|  Number | 12  
m | 小时中的分钟数 | Number | 30  
s | 分钟中的秒数 | Number | 55  
S | 毫秒数 | Number |  978  
z | 时区|  General time zone | Pacific Standard Time; PST; GMT-08:00  
Z | 时区|  RFC 822 time zone | -0800  

模式字母通常是重复的，其数量确定其精确表示： 
 - **Text:** 对于格式化来说，如果模式字母的数量大于或等于 4，则使用完全形式；否则，在可用的情况下使用短形式或缩写形式。对于分析来说，两种形式都是可接受的，与模式字母的数量无关。 
 - **Number:** 对于格式化来说，模式字母的数量是最小的数位，如果数位不够，则用 0 填充以达到此数量。对于分析来说，模式字母的数量被忽略，除非必须分开两个相邻字段。 
 - **Year:** 对于格式化来说，如果模式字母的数量为 2，则年份截取为 2 位数,否则将年份解释为 number。 
对于分析来说，如果模式字母的数量大于 2，则年份照字面意义进行解释，而不管数位是多少。因此使用模式 "MM/dd/yyyy"，将 "01/11/12" 分析为公元 12 年 1 月 11 日。 <br/>

在分析缩写年份模式（"y" 或 "yy"）时，SimpleDateFormat 必须相对于某个世纪来解释缩写的年份。这通过将日期调整为 SimpleDateFormat 实例创建之前的 80 年和之后 20 年范围内来完成。例如，在 "MM/dd/yy" 模式下，如果 SimpleDateFormat 实例是在 1997 年 1 月 1 日创建的，则字符串 "01/11/12" 将被解释为 2012 年 1 月 11 日，而字符串 "05/04/64" 将被解释为 1964 年 5 月 4 日。在分析时，只有恰好由两位数字组成的字符串（如 Character.isDigit(char) 所定义的）被分析为默认的世纪。其他任何数字字符串将照字面意义进行解释，例如单数字字符串，3 个或更多数字组成的字符串，或者不都是数字的两位数字字符串（例如"-1"）。因此，在相同的模式下， "01/02/3" 或 "01/02/003" 解释为公元 3 年 1 月 2 日。同样，"01/02/-3" 分析为公元前 4 年 1 月 2 日。 

 - **Month:** 如果模式字母的数量为 3 或大于 3，则将月份解释为 text；否则解释为 number。 
 - **General time zone:** 如果时区有名称，则将它们解释为 text。对于表示 GMT 偏移值的时区，使用以下语法： 
```
     GMTOffsetTimeZone:
             GMT Sign Hours : Minutes
     Sign: one of
             + -
     Hours:
             Digit
             Digit Digit
     Minutes:
             Digit Digit
     Digit: one of
             0 1 2 3 4 5 6 7 8 9
```
Hours 必须在 0 到 23 之间，Minutes 必须在 00 到 59 之间。格式是与语言环境无关的，并且数字必须取自 Unicode 标准的 Basic Latin 块。<br/> 
对于分析来说，RFC 822 time zones 也是可接受的。 

- **RFC 822 time zone:** 对于格式化来说，使用 RFC 822 4-digit 时区格式： 
     RFC822TimeZone:
             Sign TwoDigitHours Minutes
     TwoDigitHours:
             Digit DigitTwoDigitHours 必须在 00 和 23 之间。其他定义请参阅 general time zones。 
对于分析来说，general time zones 也是可接受的。 

SimpleDateFormat 还支持本地化日期和时间模式 字符串。在这些字符串中，以上所述的模式字母可以用其他与语言环境有关的模式字母来替换。SimpleDateFormat 不处理除模式字母之外的文本本地化；而由类的客户端来处理。 

 > 示例
 
以下示例显示了如何在美国语言环境中解释日期和时间模式。给定的日期和时间为美国太平洋时区的本地时间 2001-07-04 12:08:56。 
日期和时间模式|  结果 
---|---
"yyyy.MM.dd G 'at' HH:mm:ss z" | 2001.07.04 AD at 12:08:56 PDT  
"EEE, MMM d, ''yy" | Wed, Jul 4, '01  
"h:mm a" | 12:08 PM  
"hh 'o''clock' a, zzzz" | 12 o'clock PM, Pacific Daylight Time  
"K:mm a, z" | 0:08 PM, PDT  
"yyyyy.MMMMM.dd GGG hh:mm aaa" | 02001.July.04 AD 12:08 PM  
"EEE, d MMM yyyy HH:mm:ss Z" | Wed, 4 Jul 2001 12:08:56 -0700  
"yyMMddHHmmssZ" | 010704120856-0700  
"yyyy-MM-dd'T'HH:mm:ss.SSSZ" | 2001-07-04T12:08:56.235-0700  


 > java.sql.Date

 - 继承至java.util.Date
 
 - **常用方法**

  - > public static Date valueOf(String s)
 
 - 将 JDBC 日期转义形式的字符串转换成 Date 值。
 - 参数：
 - - s - 表示 "yyyy-mm-dd" 形式的日期的 String 对象 
 - 返回：
 - - 表示给定日期的 java.sql.Date 对象 
 

 > java.sql.Time

 - 一个与 java.util.Date 类有关的瘦包装器 (thin wrapper)，它允许 JDBC 将该类标识为 SQL TIME 值。Time 类添加格式化和解析操作以支持时间值的 JDBC 转义语法。 

 - 应该将日期组件设置为 1970 年 1 月 1 日的 "zero epoch" 值并且不应访问该值。

 - 常用方法：
 - >public void setTime(long time) 
 - -  使用毫秒时间值设置 Time 对象。
 - >public static Time valueOf(String s)
 - - 将使用 JDBC 时间转义格式的字符串转换为 Time 值。 

 > java.sql.Timestamp

 - 一个与 java.util.Date 类有关的瘦包装器 (thin wrapper)，它允许 JDBC API 将该类标识为 SQL TIMESTAMP 值。它添加保存 SQL TIMESTAMP 毫微秒值和提供支持时间戳值的 JDBC 转义语法的格式化和解析操作的能力。
 - 继承至java.util.Date

 - 注：此类型由 java.util.Date 和单独的毫微秒值组成。只有整数秒才会存储在 java.util.Date 组件中。小数秒（毫微秒）是独立存在的。传递 java.util.Date 类型的值时，Timestamp.equals(Object) 方法永远不会返回 true，因为日期的毫微秒组件是未知的。因此，相对于 java.util.Date.equals(Object) 方法而言，Timestamp.equals(Object) 方法是不对称的。此外，hashcode 方法使用基础 java.util.Date 实现并因此在其计算中不包括毫微秒。 

- 鉴于 Timestamp 类和上述 java.util.Date 类之间的不同，建议代码一般不要将 Timestamp 值视为 java.util.Date 的实例。Timestamp 和 java.util.Date 之间的继承关系实际上指的是实现继承，而不是类型继承。 

#### 数据库常用时间及日期

 > Date
 
 - date是SQL Server 2008新引进的数据类型。它表示一个日子，不包含时间部分，可以表示的日期范围从公元元年1月1日到9999年12月31日。只需要3个字节的存储空间。

 > DateTime
 
  - DateTime 日期和时间部分，可以表示的日期范围从公元1753年1月1日00:00:00.000 到9999年12月31日23:59:59.997 ，精确到3.33毫秒，它需要8个字节的存储空间。