#### 1、servlet输入出页面时，中文字符乱码
 - 解决方法：
 - - 在Writer之前设置请求头：
  ```
  response.setHeader("Content-type", "text/html;charset=UTF-8");  
  ```
  
#### 2、request请求中文乱码
 
 - 解决方法：
 - - 在调用getParameter(Str)方法后进行编码转换：
 ```
 new String(request.getParameter("username").getBytes("iso-8859-1"), "utf-8"))
 ```
