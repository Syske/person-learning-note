# 记一次mybatis复杂动态sql拼接优化方案

### 前言

今天的内容是关于昨天优化的`mybatis`动态`sql`的一次简单总结，简单来说就是我通过`trim`实现了不确定参数`union all`的可变查询，让之前的动态`sql`逻辑更加简洁，内容当然算不上高大上，只能算是给可能遇到问题的小伙伴探个路，下面我们就来展开看下吧。



### 背景

最近开发的一个功能要用到用户中心的一个接口，原有接口无法满足我的需求，所以我需要自己扩展一个新的接口，这个接口的需要实现的功能也很简单，就是根据岗位`id`、用户`id`或者用户组`id`获取一批用户信息。

由于接口涉及到多个表的组合查询，包括用户信息表、岗位用户映射信息表、用户用户组映射信息表等，而且参数是可以为空的（至少有一个参数不为空，否则也不会调用接口），所以在实现的时候我就有考虑到多个查询通过`union all`来拼接。

但是由于参数可能为空，所以`union all`是通过动态拼接的，最开始我是通过`if`判断进行拼接的，刚开始接口一直都没有问题，但是昨天测试同学在测试的时候，发现如果单传用户组`id`的话，接口会报错，然后我就开始对这个接口的`sql`进行了优化，刚开始我是这么写的：

```xml
<select id="listUsersInfoIds" resultType="io.github.syske.user.UserInfo">
        select ui.id,
        ui.userId,
        ui.name,
        ui.active
        from (
        <if test="userIds != null and userIds.size > 0">
            select
            u.id,
            u.user_id as userId,
            u.name,
            u.active
            from user u
            where u.id in
            <foreach collection="userIds" item="userId" open="(" close=")" separator=",">
                #{userId, jdbcType=BIGINT}
            </foreach>
            and u.active = true
        </if>
        <if test="postIds != null and postIds.size > 0">
            <if test="userIds != null and and userIds.size > 0">
                union all
            </if>
            select
            u.id,
            u.user_id as userId,
            u.name,
            u.active
            from post_user_mapping m,
            user u
            where m.post_id in
            <foreach collection="postIds" item="postId" open="(" close=")" separator=",">
                #{postId, jdbcType=BIGINT}
            </foreach>
            and m.user_id=u.id
            and u.active = true
        </if>
        <if test="groupIds != null and groupIds.size > 0">
            <if test="(postIds != null and postIds.size > 0) or (userIds != null and userIds.size > 0)">
                union all
            </if>
            select
            u.id,
            u.user_id as userId,
            u.name,
            u.active
            from group_user_mapping m,
            user u
            where m.group_id in
            <foreach collection="groupIds" item="groupId" open="(" close=")" separator=",">
                #{groupId, jdbcType=BIGINT}
            </foreach>
            and m.user_id=u.id
            and u.active = true
        </if>
        ) ui group by ui.id

    </select>
```

但是上面的写法在只传`groupIds`的时候会报错，准确来说是`groupIds`这里拼接`union all`的语句会报错，应该是不支持`or`这种复杂语句的，之后我把这里的`if`条件语句改成这样：

```xml
 <if test="(postIds != null and postIds.size > 0) and (userIds == null or userIds.size == 0)">
     union all
</if>
<if test="(postIds == null or postIds.size == 0) and (userIds != null and userIds.size > 0)">
    union all
</if>
```

也就是分别判断`postIds`和`userIds`是不是有一个一个不为空，如果是则拼接`union all`，当然最后我测试了下发现确实解决了，但是我觉得这种方式不够优雅，而且不够灵活，特别是如果我后面还需要加入`union all`语句的时候，那就要再多判断一个字段，越往后需要判断的字段就越多，然后我再网上找了一圈并没有找到解决方法，最后我打算看下`mybatis`的文档，幸运的是我还真找到了自己想要的答案。

### 解决方案

今天的解决方案是基于`trim`标签实现的，所以下面我们先来看下`trim`的一些知识点。

#### trim标签

在我们大多数的需求场景下，`mybatis`提供的动态语句语法已经可以胜任了，比如`if`、`where`、`choose`、`when`、`otherwise`、`foreach`，再复杂一点的还有`set`，但是像我现在的需求他们都没办法完美解决（毕竟用`if`太过繁琐），于是我发现了一个灵活性更高的标签——`trim`。

##### 简单探索

`trim`标签的作用就是帮助我们生成更复杂的`sql`，关于它的具体作用官方文档并没有给出明确说明，但是根据它的几个参数以及示例，我们可以看出它的用法。我们先看下`trim`标签的几个属性：

*   `suffixOverrides`：要替换的后缀（被替换内容）

*   `suffix`：替换的后缀（替换内容）

*   `prefixOverrides`：要替换的前缀（被替换内容）

*   `prefix`：替换的前缀（替换内容）

但看这四个属性确实可能有点迷，下面我们通过几个实例来说明下`trim`的用法。

##### 前置用法

先看第一个，也是官方给出的示例——通过`trim`来实现`where`标签，用`where`标签我们通常是这么写的：

```xml
<select id="findActiveBlogLike"
     resultType="Blog">
  SELECT * FROM BLOG
  <where>
    <if test="state != null">
         state = #{state}
    </if>
    <if test="title != null">
        AND title like #{title}
    </if>
    <if test="author != null and author.name != null">
        OR author_name like #{author.name}
    </if>
  </where>
</select>
```

用`trim`实现的话，可以这样写：

```xml
<select id="findActiveBlogLike"
     resultType="Blog">
  SELECT * FROM BLOG
 <trim prefix="where" prefixOverrides="AND | OR">
    <if test="state != null">
         state = #{state}
    </if>
    <if test="title != null">
        AND title like #{title}
    </if>
    <if test="author != null and author.name != null">
        OR author_name like #{author.name}
    </if>
  </trim>
</select>
```

这里`trim`标签的意思就是把`trim`标签中第一个`AND`或者`OR`替换为`where`，也就是说如果第一个条件为空，第二个条件中的`AND`会被替换成`where`，如果前两个条件都为空，第三个条件中的`OR`会被替换为`where`。

##### 后置用法

上面我们演示了前置替换的用法，下面我们来看下后置用法，后置用法是通过`trim`来实现`set`标签（话说我之前好像也用的不多，孤陋寡闻了），通常情况下的`set`是这么用的：

```xml
<update id="updateAuthorIfNecessary">
  update Author
    <set>
      <if test="username != null">username=#{username},</if>
      <if test="password != null">password=#{password},</if>
      <if test="email != null">email=#{email},</if>
      <if test="bio != null">bio=#{bio}</if>
    </set>
  where id=#{id}
</update>
```

`set`标签的作用就是当如上语句中，第四个更新语句为空的时候，会将`set`标签内末尾的`,`移除掉，并在标签内语句开始出加上`set`关键字。用`trim`标签的话，可以这么写：

```xml
<update id="updateAuthorIfNecessary">
  update Author
    <trim prefix="set" suffixOverrides=','>
      <if test="username != null">username=#{username},</if>
      <if test="password != null">password=#{password},</if>
      <if test="email != null">email=#{email},</if>
      <if test="bio != null">bio=#{bio}</if>
    </trim>
  where id=#{id}
</update>
```

好了，关于`trim`我们就演示这么多，下面我们做一个简单总结：

*   `prefix`：表示前置要插入的内容（这样看，前面说的替换有点不太合理），比如`where`、`set`，它可以单独使用

*   `suffix`：表示后置插入的内容（同`prefix`）

*   ` prefixOverrides  `：表示前置要移除的内容（中文翻译前置覆写）

*   `suffixOverrides`：表示后置要移除的内容（同`prefixOverrides`）

也就是说`trim`本质上就是通过这四个属性，实现在语句前后加上或者移除相关内容，来实现复杂的动态`sql`，在实现方面也很简单，但是灵活度更多。

##### 解决我的问题

最后让我们再回到我前面说的优化，我的这个`sql`如果用`trim`实现的话，可以这样写：

```xml
    <select id="listUsersInfoIds" resultType="net.coolcollege.user.facade.model.user.UserInfo">
        select ui.id,
        ui.userId,
        ui.name,
        ui.active
        from (
        <trim suffixOverrides="union all">
            <trim suffix="union all">
                <if test="userIds != null and userIds.size > 0">
                    select
                    u.id,
                    u.user_id as userId,
                    u.name,
                    u.active
                    from user u
                    where u.id in
                    <foreach collection="userIds" item="userId" open="(" close=")" separator=",">
                        #{userId, jdbcType=BIGINT}
                    </foreach>
                    and u.active = true
                </if>
            </trim>
            <trim suffix="union all">
                <if test="postIds != null and postIds.size > 0">
                    select
                    u.id,
                    u.user_id as userId,
                    u.name,
                    u.active
                    from post_user_mapping m,
                    user u
                    where m.post_id in
                    <foreach collection="postIds" item="postId" open="(" close=")" separator=",">
                        #{postId, jdbcType=BIGINT}
                    </foreach>
                    and m.user_id=u.id
                    and u.active = true
                </if>
            </trim>
            <if test="groupIds != null and groupIds.size > 0">
                select
                u.id,
                u.user_id as userId,
                u.name,
                u.active
                from group_user_mapping m,
                user u
                where m.group_id in
                <foreach collection="groupIds" item="groupId" open="(" close=")" separator=",">
                    #{groupId, jdbcType=BIGINT}
                </foreach>
                and m.user_id=u.id
                and u.active = true
            </if>
        </trim>
        ) ui group by ui.id
    </select>
```

首先我通过一个大的`trim`包装所有子查询（之前通过`union all`连接），条件是移除最后的`union all`，然后再用一个`trim`标签包装除最后一个子查询之外的其他子查询，条件是再语句末尾加上`union all`，这样前面需要通过复杂`if`判断的语句就直接省略了，而且好处也很明显：

后续不论我增加多少个子查询，我只需要给子查询加上`trim`标签即可（条件都一样），而不需要关心其他子查询是否为空，这样整个`sql`不仅更简洁，而且扩展性也很强，后期不论我增加多少个子查询，只需要给子查询加上`trim`标签即可，而不需要处理其他复杂判断。

### 结语

`mybatis`算是一个比较流行的`ORM`框架，应该说是国内最主流的数据库交互框架了，但是从我自身使用的情况来说，大多数复杂场景我好像只想到了`if`、`choose`、`when`、`where`、`foreach`等，甚至连`set`都没用过，这样不仅导致写出的动态`sql`逻辑复杂，不够简洁，不利于后期维护，而且很容易出错。

总之，我是觉得学习东西，我们不应该仅仅停留在够用和满足需求的程度，而应该养成多看官方文档、多探索的习惯，选择更适合、更优的解决方案，这样才不至于成为井底之蛙。好了，今天的内容就到这里吧！
