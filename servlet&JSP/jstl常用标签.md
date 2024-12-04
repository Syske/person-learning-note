### 1、forEach

```
<body>
	<%
		List<User> userList = new ArrayList<User>();
		User user1 = new User("张三", "admin", "云中帆", 18);
		User user2 = new User("李四", "user", "舞帆", 19);
		User user3 = new User("王五", "test", "云梦瑶", 24);
		User user4 = new User("张帆", "java", "霍尼韦尔", 25);
		User user5 = new User("江云", "adste", "该账号已注销", 16);
		userList.add(user1);
		userList.add(user2);
		userList.add(user3);
		userList.add(user4);
		userList.add(user5);
		session.setAttribute("userList", userList);
	%>
	<ul>
		<c:forEach items="${userList}" var="user">
			<li>${user.username}</li>
		</c:forEach>
	</ul>
</body>
```

### 2、if

```
	<%
		List<User> userList = new ArrayList<User>();
		User user1 = new User("张三", "admin", "云中帆", 18);
		User user2 = new User("李四", "user", "舞帆", 19);
		User user3 = new User("王五", "test", "云梦瑶", 24);
		User user4 = new User("张帆", "java", "霍尼韦尔", 25);
		User user5 = new User("江云", "adste", "该账号已注销", 16);
		userList.add(user1);
		userList.add(user2);
		userList.add(user3);
		userList.add(user4);
		userList.add(user5);
		session.setAttribute("userList", userList);
	%>
	<ul>
		<c:forEach items="${userList}" var="user">
			<li>${user.username}</li>
			<c:set var="name" value="${user.username}"></c:set>
			<c:if test="${name=='张帆'}">
				<p><c:out value="${user.nickname}"/></p>
			</c:if>

		</c:forEach>
		
		
	</ul>
```