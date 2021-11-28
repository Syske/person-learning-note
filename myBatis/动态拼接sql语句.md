### 1、if标签

```
<if test="username != null">username = #{userName}</if>
```

### 2、choose、when、otherwise元素

```
<select id="listUsers" parameterType="user"
		resultMap="userResultMap">
		select * where 1=1
		<choose>
			<when test="id != null and id != ''">
			AND id = #{id}
			</when>
			<when test="username != null and username != ''">
			AND username  like concat('%', #{userName}, '%')
			</when>
			<otherwise>
			AND note is not null
			</otherwise>
		</choose>

	</select>
```


### 2、where标签

```
<select id="listUsers" parameterType="user"
		resultMap="userResultMap">
		select u.*,r.id roleId,r.name roleName from user u, role r,
		user_role
		ru
		<where>
			u.id = ru.uid
			and r.id = ru.rid
			<if test="name != null">
				and name = #{name}
			</if>
		</where>

	</select>
```

### 3、trim标签
```
<select id="listUsers" parameterType="user" resultType="user">
		<if test="userName != null">
			<bind name="uname" value="'%' + userName + '%'" />
		</if>
		select * from user

		<trim prefix="where" prefixOverrides="and|or">

			<if test="id != null">
				id = #{id}
			</if>
			<if test="userName != null">
				and userName like #{uname}
			</if>
		</trim>
	</select>
```

### 4、set标签

```
<update id="updateUser">
		update user
		<set>
			<if test="username != null">username = #{userName},</if>
			<if test="name != null">name = #{name},</if>
			<if test="sex != null">sex=#{sex},</if>
			<if test="phone != null">phone=#{phone},</if>
			<if test="password != null">password=#{password},</if>
			<if test="address != null">address = #{address},</if>
			<if test="birth != null">birth=#{birth}</if>
		</set>
		<if test="id != null">
			<where>
				where id=#{id}
			</where>
		</if>
	</update>
```

### 5、resultMap


```
<resultMap type="user" id="userResultMap">
		<id column="id" property="id" />
		<result column="name" property="name" />
		<result column="sex" property="sex" />
		<association property="role" javaType="role">
			<id column="roleId" property="id" />
			<id column="roleName" property="name" />
		</association>
	</resultMap>
```

### 6、forEach元素

> 遍历集合，可以很好的支持数组和List、set接口的集合

```

<select id="listUsers" parameterType="user"
		resultMap="userResultMap">
		select * from user where sex in
		<forech item="sex" inde="index" coolection="sexList" open="("
		    separator="," colse=")" >
		    #{sex}
		</foreach>

	</select>
	
```

- `collection`配置的是传递进来的参数名称，可以是数组或者`List`、`set`等集合

- `item`配置的是循环中当前的元素

- `indeX`配置的是当前元素在集合的位置下标 

- `open`和`close`配置的是以什么符号将这些集合元素包装起来

- `separator`是各个元素的间隔符