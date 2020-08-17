### 基础语法

#### 1、对比

> > JSP：java平台安全性高，适合开发大型的、企业级的web应用程序；

> > ASP.net：.NET平台简单易学，安全性和跨平台性差；

> > PHP:简单高效，成本低，开发周期短，适合中小型企业的web应用开发（LAMP）


#### 2、JSP页面元素构成

> > 静态内容

> > 注释

> > 指令

> > 声明

> > 小脚本

> > 表达式

##### (1)JSP指令

> > page指令

> > include指令：将外部文件嵌入到当前JSP文件中

> > taglib指令：自定义标签

###### page指令：

 - 语法：
 
```
<% @page 属性1 = "属性值" ... 属性n = "属性值" %>

```
- - 属性language， 指定脚本语言，默认java；

- - 属性import ，导入JSP页面需要用到的jar包，默认无；

- - 属性extends,指定JSP页面编译所产生的java类所继承的父类，或实现的接口

- - 属性session，设定这个JSP页面是否需要HTTP Session

- - 属性buffed， 指定输出缓冲区的大小，默认值为8kB,可以设置为none，也可以设置为其他的值，单位为KB

- - 属性autoFlush，当输出缓冲区即将溢出时，是否需要强制输出缓冲区的内容，若果设置为false时，则会在buffer溢出产生一个异常

- - 属性info，设置该JSP程序的信息，也可以看作其说明，可以通过Servlet.getServletInfo()方法获取该值。在JSP页面中，可以直接调用getSevletInfo()方法获取该值

- - 属性errorPage，指定错误处理页面

- - 属性isErrorPage，设置本JSP页面是否为错误处理程序，若该页面本身是错误处理页面，则无需指定errorPage属性

- - 属性pageEncoding，指定生成网页的编码字符集

- - 属性contentType，指定页面编码，默认text/html;charset = ISO-8859-1，可以更改为国际编码（text/html;charset = utf-8) 

###### include指令：

- 语法：

```
<%@include file="relativeURLLSpec" %>

```

- - include既可以包含静态的文本，也可以包含动态的jsp页面

###### 注释

> > >html注释：

```
<!-- html注释 -->
```

> > >JSP注释：

```
<%-- JSP注释 --%>
```

> > >JSP脚本注释：

```
// 单行

/*
多行注释
*/
```