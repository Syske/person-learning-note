在JSP页面中使用标签库代替传统Java片段语文来实现页面显示逻辑已经不是新技术了，但是自定义的标签容易造成重复定义和非标准的实现，所以JSTL（JSP Standard Tag Library，JSP标准标签库)诞生了。JSTL是一个不断完善的开放源代码的JSP标签库，是由apache的jakarta小组来维护的（标准是SUN制定，apache实现的，SUN收录了apache的实现）。JSTL只能运行在支持JSP1.2和Servlet2.3规范的容器上。






Version	| JSTL version	| Requirements
---|--- | ---
Standard 1.2.3 |	JSTL 1.2 |	Servlet 2.5, JavaServer Pages 2.1
Standard 1.1 |	JSTL 1.1 |	Servlet 2.4, JavaServer Pages 2.0
Standard 1.0 |	JSTL 1.0 |	Servlet 2.3, JavaServer Pages 1.2

- Sun 发布的标准 JSTL1.1 标签库有以下几个标签：

- - 核心标签库：包含 Web 应用的常见工作，比如：循环、表达式赋值、基本输入输出等。
格式化标签库：用来格式化显示数据的工作，比如：对不同区域的日期格式化等。
- - 数据库标签库：可以做访问数据库的工作。
- - XML 标签库：用来访问 XML 文件的工作，这是 JSTL 标签库的一个特点。
- - 函数标签库：用来读取已经定义的某个函数。
- 使用JSTL的步骤：

- 在项目中引入jstl的相关jar包，确保jar存在：jstl.jar、standard。
```
<dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>jstl</artifactId>
    <version>1.2</version>
</dependency>
<dependency>
    <groupId>taglibs</groupId>
    <artifactId>standard</artifactId>
    <version>1.1.2</version>
</dependency>
```
- 在需要使用标签的JSP页面上使用taglib指令引入标签库。
- 在需要使用标签的位置直接使用标签库。
#### 格式化标签：
```
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page import="java.util.*"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>JSTL_FMT</title>
</head>
<body>

<!-- ****格式化数字【fmt:formatNumber】****
    value="要显示的数字，必填项，默认为主体内容"
    type="类型（默认数字NUMBER、货币CURRENCY、百分比PERCENT）"
    pattern="格式模式"
    currencyCode="货币码，当type='CURRENCY'时，默认为当前区域"
    currencySymbol="货币符号，当type='CURRENCY'时，默认为当前区域"
    groupingUsed="是否对数字分组，默认为true"
    maxIntegerDigits="整型数最大位数，多余部分直接截取"
    minIntegerDigits="整型数最小位数，不足补0"
    maxFractionDigits="小数点后最大的位数，多余部分四舍五入"
    minFractionDigits="小数点后最小的位数，不足补0"
    var="存储格式化数字的变量，默认直接输出"
    scope="var属性的作用域(page request session application),默认为page"
    模式属性值：
        0   代表一位数字，没有则显示为0
        E   使用指数格式
        #   代表一个数字，前导零和追尾零不显示
        .   小数点
        ,   数字分组分隔符
        -   使用默认的负数前缀
        %   百分数
        ¤   货币符号
 -->
<fmt:formatNumber>123.456</fmt:formatNumber>
、
<fmt:formatNumber value="123.456" type="CURRENCY" currencySymbol="￥￥"/>
、
<fmt:formatNumber value="123.456" type="CURRENCY" currencyCode="EUR"/>
、
<fmt:formatNumber value="123.456" maxIntegerDigits="5" minIntegerDigits="3"/>
、
<fmt:formatNumber value="123.456" maxFractionDigits="3" minFractionDigits="2"/>
、
<fmt:formatNumber value="89765446123.456" pattern="#,###.00"/>
、
<fmt:formatNumber value="89765446123.456" pattern="#,###.00" groupingUsed="false"/>
、
<fmt:formatNumber value="0.44" pattern="#.##%"/>
、
<fmt:formatNumber value="0.44" type="PERCENT"/>
、
<fmt:formatNumber value="89765446123.456" pattern="###E0"/>
<!-- 输出：
123.456、￥￥123.46 、 EUR123.46 、 123.456 、 123.456 、 89,765,446,123.46 、 89765446123.46 、 44% 、 44% 、 89.8E9 
-->

<hr>
<!-- ****解析数字【fmt:parseNumber】****
    value="要解析的数字，默认为主体内容"
    type="类型（默认数字NUMBER、货币CURRENCY、百分比PERCENT）"
    parseLocale="解析数字时所用区域，默认为当前区域"
    integerOnly="是否只解析整型数(true)或浮点数(false)，默认为false"
    pattern="解析模式"
    timeZone="要显示日期的时区，默认为当前时区"
    var="存储解析数字的变量，默认为当前页面"
    scope="var属性的作用域(page request session application),默认为page"
 -->
<fmt:parseNumber>123.456</fmt:parseNumber>
、
<fmt:parseNumber value="￥123.46" type="CURRENCY"/>
、
<fmt:parseNumber value="$123.46" type="CURRENCY" parseLocale="en_US"/>
、
<fmt:parseNumber value="123.456" integerOnly="true"/>
、
<fmt:parseNumber value="89.8E9" pattern="###E0"/>
<!-- 输出：
123.456 、 123.46 、 123.46 、 123 、 89800000000 
-->

<hr>
<!-- ****格式化日期【fmt:formatDate】****
    value="要格式化的日期，必填项"
    type="类型（默认日期DATE、时间TIME、日期+时间BOTH）"
    dateStyle="FULL, LONG, MEDIUM, SHORT, 或默认DEFAULT"
    timeStyle="FULL, LONG, MEDIUM, SHORT, 或默认DEFAULT"
    pattern="格式模式"
    timeZone="要显示日期的时区，默认为当前时区"
    var="存储格式化日期的变量，默认为当前页面"
    scope="var属性的作用域(page request session application),默认为page"
    模式的属性：
        y   年份
        M   月份
        d   月中的某一天
        h   12小时制的小时
        H   24小时制的小时
        m   分钟
        s   秒
        S   毫秒
        E   周几
        D   一年中的第几天
        F   一月中的第几个周几
        w   一年中的第几周
        W   一月中的第几周
        a   a.m./p.m. 指示符
        k   小时（12小时制的小时）
        K   小时（24小时制的小时）
        z   时区
 -->
<c:set var="now" value="<%=new Date()%>" />
<fmt:formatDate value="${now}"/>
、
<fmt:formatDate value="${now}" type="TIME"/>
、
<fmt:formatDate value="${now}" type="BOTH"/>
、
<fmt:formatDate type="BOTH" dateStyle="FULL" timeStyle="FULL" value="${now}" />
、
<fmt:formatDate value="${now}" pattern="yyyy-MM-dd HH:mm:ss E Z a"/>
<!-- 输出：
2017-1-15 、 16:20:37 、 2017-1-15 16:20:37 、 2017年1月15日 星期日 下午04时20分37秒 CST 、 2017-01-15 16:20:37 星期日 +0800 下午  
-->

<hr>
<!-- ****解析日期【fmt:parseDate】****
    value="要显示的日期，必填项，默认为主体内容"
    type="DATE、TIME、BOTH，默认DATE"
    dateStyle="FULL, LONG, MEDIUM, SHORT, 或默认DEFAULT"
    timeStyle="FULL, LONG, MEDIUM, SHORT, 或默认DEFAULT"
    pattern="格式模式"
    timeZone="要显示日期的时区，默认为当前时区"
    var="存储解析日期的变量，默认为当前页面"
    scope="var属性的作用域(page request session application),默认为page"
 -->
<fmt:parseDate>2017-1-15 16:20:37</fmt:parseDate>
、
<fmt:parseDate type="BOTH">2017-1-15 16:20:37</fmt:parseDate>
、
<fmt:parseDate type="BOTH" dateStyle="FULL" timeStyle="FULL">2017年1月15日 星期日 下午04时20分37秒 CST</fmt:parseDate>
、
<fmt:parseDate pattern="yyyy-MM-dd HH:mm:ss E Z a">2017-01-15 16:20:37 星期日 +0800 下午</fmt:parseDate>
<!-- 输出：
Sun Jan 15 00:00:00 CST 2017 、 Sun Jan 15 16:20:37 CST 2017 、 Sun Jan 15 16:20:37 CST 2017 、 Sun Jan 15 16:20:37 CST 2017 
-->
</body>
</html>

```