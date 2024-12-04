#### 1、基本结构
```js
<script type="text/javascript">
        // 创建XMLHttpRequest对象
		var request = new XMLHttpRequest();
		var id = '1';
		request.onreadystatechange = function() {
		// 如果请求成功，且获取响应，则返回响应数据
			if (request.readyState == 4 && request.status == 200) {
				document.getElementById("result").innerHTML = request.responseText;
			}
		}
		// 请求 open("method","url","async(true/false)")
		request.open("get", "index.jsp?id=" + id, true);
		// 设置请求头信息
		request.setRequestHeader("content-type",
				"application/x-www-for-urlencoded");
	    // 发送请求，当请求为post时，请求参数应该写在send()方法中
		request.send();
	</script>
```

#### 2、Http请求过程

- 建立TCP链接
- 浏览器向服务器发送请求命令
- 浏览器发送请求头信息
- 服务器响应（应答）
- 服务器发送应答头信息
- 服务器向浏览器发送数据
- TCP连接关闭

#### 3、Http请求

- 请求方法：GET/POST
- - GET：长度在200个字符；
- - POST：一般用于修改服务器上的资源，对所发送信息的数量无限制；

- 请求URL

- 请求头：包含一些客户端环境信息、身份验证信息等

- 请求体：包含客户提交的查询字符串信息、表单信息


#### 4、Http响应

- 一个数字和文字组成的状态码，用来显示请求是否成功
- 响应头：包含许多用户信息，入服务器类型，日期时间，内容类型和长度等
- 响应体
- 状态码：
- - 1XX：信息类，服务器正在进行进一步处理
- - 2XX：成功
- - 3XX：重定向
- - 4XX：客户端错误，请求有错误
- - 5XX：服务器错误

#### 5、XMLHttpRequest发送请求

-  request.open("get", "index.jsp?id=" + id, true)
- - 请求 open("method","url","async(true/false)")

- request.setRequestHeader("content-type",
				"application/x-www-for-urlencoded");
- - 设置请求头信息，写在open和send方法之间

- request.send();
- - 发送请求，当请求为post时，请求参数应该写在send()方法中

#### 6、XMLHttpRequest获取响应

- responseText：获取字符串形式的响应数据
- responseXML：获取xml形式的响应数据
- status和statusText：以数字和文本形式返回Http状态码
- getAllResponseHeader()：获取所有的响应报头
- getResponseHeader()：查询响应中的某个字段的值

- readyState属性：
- - 值为 0 ：请求初始化，open还没有调用
- - 值为 1：服务器连接已建立，open已经调用
- - 值为 2：请求已被接收，也就是连接到头信息了
- - 值为 3：请求处理中，也就是接收到响应头了
- - 值为 4：请求已完成，且响应已就绪，也就是响应完成了

- 常用方法：
```js
request.onreadystatechanage=function() {
    if(request.readystate === 4 && request.status === 200) {
        // 响应后的操作
    }
}
```


#### 7、JSon解析

##### 基本概念

- JSon是存储和交换文本信息的语法，类似XML，它采用键值对的方式来组织，易于阅读和编写，也易于机器解析和生成
- JSon是独立于语言的


##### JSon和xml的比较

- 长度比xml短小
- 读写速度比xml更快
- Json可以使用JavaScript内建的方法直接进行解析、转换成Javascript对象


##### JSon解析

- JSon.parse(Json_name)
- eval('('+ json_name +')')


##### 数据结构

- 1、 Object:使用花括号内含的键值对结构，key必须是String类型，value为任意基本类型或数据结构
- - {String：value}
- 2、Array：基本类型String、number，使用中括号括起来并用逗号分隔