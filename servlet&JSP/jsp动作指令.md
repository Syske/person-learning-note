#### jsp的7个动作指令

- jsp:forward：执行页面转向，将请求的处理转发到下一个页面

- jsp:param：用于传递参数，必须与其他支持参数的标签一起使用

- jsp:include：用于动态引入一个jsp页面

- jsp:plugin：用于下载JavaBean的实例或Applet到客户端执行

- jsp:useBean：创建一个JavaBean的实例

- jsp:setProperty：设置JavaBean实例的属性值

- jsp:getProperty：输出JavaBean实例的属性值

#### 1、forward指令
 
- 语法：

```
// 对于JSP1.0，使用如下语法：
<jsp:forward page="{relativeURL|<%=expression%>}"/>

// 对于JSP1.1以上规范，可以使用如下语法：
<jsp:forward page="{relativeRUL | <%=expression%>}">
    {<jsp:param.../>}
</jsp:forward>
```
- 第二种语法用于在转发时增加额外的请求参数，增加的请求参数可以通过HttpServletRequest类的getParameter()方法获取。

```
// 实例：
<jsp:forward page="forward-result.jsp">
    <jsp:param name="age" value="29"/>
</jsp:forward>
```
- 执行forward指令时，请求的地址不会发生变化，且客户端的请求参数不会丢失



#### 2、include指令 

- 语法：
 
```
<jsp:include page="{relativeURL | <%=expression%>}" flush="true" />
```
或

```
<jsp:include page="{relativeRUL | <%=expression%>}" flush="true" >
    {<jsp:param name="parameterName" value="patamterValue" />}
</jsp:include>
```

- include指令使用动态导入语法导入脚本

- 静态导入和动态导入的区别

- - 静态导入是将被导入页面的代码完全融入，两个页面融合成一个整体Servlet；而动态导入则在Servlet中使用include方法来引入被导入页面的内容；

- - 静态导入时被导入页面的编译指令会起作用；而动态导入时被导入页面的编译指令则失去作用，只是插入被导入页面的body内容；

- - 动态包含还可以增加额外的参数；

#### 3、useBean、setProperty、getProperty指令

- useBean指令用于在JSP页面中初始化一个Java实例；setProperty指令用于为JavaBean实例的属性设置值；getProprety指令用于输出JavaBean实例的属性

- useBean的语法格式：

```
<jsp:useBean id="name" class="classname" scope="page|request|session|application" />
```
- 其中，id属性是JavaBean的实例名，class属性确定JavaBean的实现类。scope属性用于指定JavaBean实例的作用域；

- - page表示该JavaBean实例仅在该页面有效；

- - request表示该JavaBean实例在本次请求有效；

- - session表示该JavaBean在本次session内有效；

- - application表示该JavaBean实例在本应用内一直有效。




- setProperty指令的语法格式：

```
<jsp:setProperty name="BeanName" property="propertyName" vlaue="value" />
```
- 其中，name属性确定需要设定JavaBean的实例名；property属性确定需要设置的属性名；value属性则确定需要设置的属性值



- getProperty指令的语法格式：

```
<jsp:getProperty name="BeanName" property="propertyName" />
```
- 其中，name属性确定需要输出的JavaBean的实例名；property属性确定需要获取的属性名

#### 4、plugin指令

- plugin指令主要用于下载服务器端的JavaBean或applet到客户端执行。由于程序在客户端执行，因此客户端必须安装虚拟机。



#### 5、param指令

- param指令用于设置参数值，指令本身不能单独使用，通常与以下三个指令结合使用：

- - jsp:include 
- - - 用于将参数传入被导入的页面；

- - jsp:forward
- - - 用于将参数传入被转向的页面；

- - jsp:plugin
- - - 用于将参数传入页面的JavaBean实例或Applet实例


- 语法：
```
<jsp:param name="paramName" value="paramValue" />
```

