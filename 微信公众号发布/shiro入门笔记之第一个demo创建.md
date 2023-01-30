# shiro入门笔记之第一个demo创建

tags: [#shiro, #demo]

#### 前言

看到这篇文章之前，可能很多小伙伴都没听过shiro，那么shiro是什么呢？shiro是Apache基金会下一个非常有名的开源项目（项目官网： http://shiro.apache.org/ ），官网是这样介绍的：

Apache Shiro™是一个功能强大且易于使用的Java安全框架，它执行身份验证、授权、加密和会话管理。使用Shiro易于理解的API，您可以快速轻松地保护任何应用程序—从最小的移动应用程序到最大的Web和企业应用程序。

接下来就让我们近距离地了解shiro吧。

#### 一、创建maven项目

##### 1.选择maven模板，填写项目信息

选择maven，这里我选择的模板是quickstart

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/1571455743716.png)

填写项目信息

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/1571455915103.png)

设置项目maven配置，如果没有特殊设置，直接下一步

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/1571456044986.png)

设置项目保存路径

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/1571456154116.png)

maven项目到此创建完成，下面开始shiro demo

#### 二、编写shiro demo

##### 1.导入依赖包

导入如下依赖

```xml
<dependency>
  <groupId>org.apache.shiro</groupId>
  <artifactId>shiro-core</artifactId>
  <version>1.2.6</version>
</dependency>
```

##### 2.编写java

```java
package io.github.syske;/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

import org.apache.shiro.SecurityUtils;
import org.apache.shiro.authc.*;
import org.apache.shiro.config.IniSecurityManagerFactory;
import org.apache.shiro.mgt.SecurityManager;
import org.apache.shiro.session.Session;
import org.apache.shiro.subject.Subject;
import org.apache.shiro.util.Factory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


/**
 * Simple Quickstart application showing how to use Shiro's API.
 *
 * @since 0.9 RC2
 */
public class Quickstart {

    private static final transient Logger log = LoggerFactory.getLogger(Quickstart.class);


    public static void main(String[] args) {

        // The easiest way to create a Shiro SecurityManager with configured
        // realms, users, roles and permissions is to use the simple INI config.
        // We'll do that by using a factory that can ingest a .ini file and
        // return a SecurityManager instance:

        // Use the shiro.ini file at the root of the classpath
        // (file: and url: prefixes load from files and urls respectively):
        Factory<SecurityManager> factory = new IniSecurityManagerFactory("classpath:shiro.ini");
        SecurityManager securityManager = factory.getInstance();

        // for this simple example quickstart, make the SecurityManager
        // accessible as a JVM singleton.  Most applications wouldn't do this
        // and instead rely on their container configuration or web.xml for
        // webapps.  That is outside the scope of this simple quickstart, so
        // we'll just do the bare minimum so you can continue to get a feel
        // for things.
        SecurityUtils.setSecurityManager(securityManager);

        // Now that a simple Shiro environment is set up, let's see what you can do:

        // get the currently executing user:
        Subject currentUser = SecurityUtils.getSubject();

        // Do some stuff with a Session (no need for a web or EJB container!!!)
        Session session = currentUser.getSession();
        session.setAttribute("someKey", "aValue");
        String value = (String) session.getAttribute("someKey");
        if (value.equals("aValue")) {
            log.info("Retrieved the correct value! [" + value + "]");
        }

        // let's login the current user so we can check against roles and permissions:
        if (!currentUser.isAuthenticated()) {
            UsernamePasswordToken token = new UsernamePasswordToken("lonestarr", "vespa");
            token.setRememberMe(true);
            try {
                currentUser.login(token);
            } catch (UnknownAccountException uae) {
                log.info("There is no user with username of " + token.getPrincipal());
            } catch (IncorrectCredentialsException ice) {
                log.info("Password for account " + token.getPrincipal() + " was incorrect!");
            } catch (LockedAccountException lae) {
                log.info("The account for username " + token.getPrincipal() + " is locked.  " +
                        "Please contact your administrator to unlock it.");
            }
            // ... catch more exceptions here (maybe custom ones specific to your application?
            catch (AuthenticationException ae) {
                //unexpected condition?  error?
            }
        }

        //say who they are:
        //print their identifying principal (in this case, a username):
        log.info("User [" + currentUser.getPrincipal() + "] logged in successfully.");

        //test a role:
        if (currentUser.hasRole("schwartz")) {
            log.info("May the Schwartz be with you!");
        } else {
            log.info("Hello, mere mortal.");
        }

        //test a typed permission (not instance-level)
        if (currentUser.isPermitted("lightsaber:wield")) {
            log.info("You may use a lightsaber ring.  Use it wisely.");
        } else {
            log.info("Sorry, lightsaber rings are for schwartz masters only.");
        }

        //a (very powerful) Instance Level permission:
        if (currentUser.isPermitted("winnebago:drive:eagle5")) {
            log.info("You are permitted to 'drive' the winnebago with license plate (id) 'eagle5'.  " +
                    "Here are the keys - have fun!");
        } else {
            log.info("Sorry, you aren't allowed to drive the 'eagle5' winnebago!");
        }

        //all done - log out!
        currentUser.logout();

        System.exit(0);
    }
}

```

当然你也可以直接导入shiro官方的示例代码，以上代码就是来源于官方示例

##### 3.导入配置文件

日志配置文件，文件名log4j.properties

```properties
log4j.rootLogger=INFO, stdout

log4j.appender.stdout=org.apache.log4j.ConsoleAppender
log4j.appender.stdout.layout=org.apache.log4j.PatternLayout
log4j.appender.stdout.layout.ConversionPattern=%d %p [%c] - %m %n

# General Apache libraries
log4j.logger.org.apache=WARN

# Spring
log4j.logger.org.springframework=WARN

# Default Shiro logging
log4j.logger.org.apache.shiro=INFO

# Disable verbose logging
log4j.logger.org.apache.shiro.util.ThreadContext=WARN
log4j.logger.org.apache.shiro.cache.ehcache.EhCache=WARN

```

shiro配置文件，文件名shiro.ini

```ini
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# =============================================================================
# Quickstart INI Realm configuration
#
# For those that might not understand the references in this file, the
# definitions are all based on the classic Mel Brooks' film "Spaceballs". ;)
# =============================================================================

# -----------------------------------------------------------------------------
# Users and their assigned roles
#
# Each line conforms to the format defined in the
# org.apache.shiro.realm.text.TextConfigurationRealm#setUserDefinitions JavaDoc
# -----------------------------------------------------------------------------
[users]
# user 'root' with password 'secret' and the 'admin' role
root = secret, admin
# user 'guest' with the password 'guest' and the 'guest' role
guest = guest, guest
# user 'presidentskroob' with password '12345' ("That's the same combination on
# my luggage!!!" ;)), and role 'president'
presidentskroob = 12345, president
# user 'darkhelmet' with password 'ludicrousspeed' and roles 'darklord' and 'schwartz'
darkhelmet = ludicrousspeed, darklord, schwartz
# user 'lonestarr' with password 'vespa' and roles 'goodguy' and 'schwartz'
lonestarr = vespa, goodguy, schwartz

# -----------------------------------------------------------------------------
# Roles with assigned permissions
# 
# Each line conforms to the format defined in the
# org.apache.shiro.realm.text.TextConfigurationRealm#setRoleDefinitions JavaDoc
# -----------------------------------------------------------------------------
[roles]
# 'admin' role has all permissions, indicated by the wildcard '*'
admin = *
# The 'schwartz' role can do anything (*) with any lightsaber:
schwartz = lightsaber:*
# The 'goodguy' role is allowed to 'drive' (action) the winnebago (type) with
# license plate 'eagle5' (instance specific id)
goodguy = winnebago:drive:eagle5

```

这里依然放上官方示例的配置文件

#### 三、运行

直接运行java中的main方法即可，这里需要注意的是shiro项目的日志需要slf4j，所以要导入slf4j的依赖，依赖如下：

```xml
    <!-- configure logging -->
    <dependency>
      <groupId>org.slf4j</groupId>
      <artifactId>jcl-over-slf4j</artifactId>
      <version>1.7.24</version>
      <scope>runtime</scope>
    </dependency>
    <dependency>
      <groupId>org.slf4j</groupId>
      <artifactId>slf4j-log4j12</artifactId>
      <version>1.7.24</version>
      <scope>runtime</scope>
    </dependency>
    <dependency>
      <groupId>log4j</groupId>
      <artifactId>log4j</artifactId>
      <version>1.2.17</version>
      <scope>runtime</scope>
    </dependency>

    <dependency>
      <groupId>org.slf4j</groupId>
      <artifactId>slf4j-nop</artifactId>
      <version>1.7.24</version>
    </dependency>
```

然后，你就能看到控制台打印如下日志信息：

```verilog
2019-10-19 12:00:04,751 INFO [org.apache.shiro.session.mgt.AbstractValidatingSessionManager] - Enabling session validation scheduler... 
2019-10-19 12:00:05,508 INFO [io.github.syske.Quickstart] - Retrieved the correct value! [aValue] 
2019-10-19 12:00:05,512 INFO [io.github.syske.Quickstart] - User [lonestarr] logged in successfully. 
2019-10-19 12:00:05,512 INFO [io.github.syske.Quickstart] - May the Schwartz be with you! 
2019-10-19 12:00:05,513 INFO [io.github.syske.Quickstart] - You may use a lightsaber ring.  Use it wisely. 
2019-10-19 12:00:05,514 INFO [io.github.syske.Quickstart] - You are permitted to 'drive' the winnebago with license plate (id) 'eagle5'.  Here are the keys - have fun! 
```

至此，我们的第一个shiro demo已经正常运行了，下来让我们分析解释下上面的代码

#### 四、代码解析

这里只探讨shiro的相关代码，log4j配置这里不讨论，如果想了解的小伙伴可以自己查阅相关资料，当然也可以给我留言。

##### 1.shiro配置文件

我删除了官方英文注释，将核心的注释翻译成了中文，然后加入了比较详细的说明

```ini
[users]
# 用户root的密码为secret,角色为admin(也就是说配置的方法是：用户名=密码, 角色)
root = secret, admin
# 用户guest的密码为guest,角色为guest(同上)
guest = guest, guest
# 用户presidentskroob的密码为12345，用户角色president
presidentskroob = 12345, president
# 下面这个是给用户配置多角色，用户darkhelmet的密码为ludicrousspeed，角色为darklord和schwartz
darkhelmet = ludicrousspeed, darklord, schwartz
# 用户lonestarr的密码为vespa，角色为goodguy和schwartz
lonestarr = vespa, goodguy, schwartz

[roles]
# 这里是给角色设置权限，下面配置的意思是，角色admin可以访问所有资源(*标识匹配所有，具体的匹配规则后面会
#讲到)
admin = *
# 拥有lightsaber权限的角色可以访问所有资源（*）
schwartz = lightsaber:*
# 角色goodguy可以通过携带eagle5（实例特定ID）的方式访问winnebago类型的资源
goodguy = winnebago:drive:eagle5
```

##### 2.java代码

```java
public static void main(String[] args) {
       	// 创建SecurityManager工厂
        Factory<SecurityManager> factory = new IniSecurityManagerFactory("classpath:shiro.ini");
    	// 通过工厂创建SecurityManager实例
        SecurityManager securityManager = factory.getInstance();
        // 将securityManager传给SecurityUtils
        SecurityUtils.setSecurityManager(securityManager);
        // 从SecurityUtils中获取Subject实例
        Subject currentUser = SecurityUtils.getSubject();
        /* 从Subject实例中获取Session实例
        这里需要说明的是shiro的Session非常强大，不仅可以在web中使用，而且可以在J2SE项目中使用，更重要的是在web项目中使用时，他会自动将HttpServerletSession自动整合到自己的session，让你直接可以在Shiro的session中拿到你放在HttpServerletSession中的变量，这在非controller组件中非常有用
        */
        Session session = currentUser.getSession();
    	// 在session中放置变量
        session.setAttribute("someKey", "aValue");
    	// 从session中取出变量
        String value = (String) session.getAttribute("someKey");
        if (value.equals("aValue")) {
            log.info("Retrieved the correct value! [" + value + "]");
        }
        // 判断用户（Subject）是否经过授权（登录）
        if (!currentUser.isAuthenticated()) {
            // 如果未登录，创建包含用户名及密码的认证令牌：用户名，密码
            UsernamePasswordToken token = new UsernamePasswordToken("lonestarr", "vespa");
            // 设置记住我标识，如果该标识为true，对于运行记住我访问的资源，不用经过登录认证即可访问
            token.setRememberMe(true);
            try {
                // Subject认证授权
                currentUser.login(token);
            } catch (UnknownAccountException uae) {
                // 用户名未知
                log.info("There is no user with username of " + token.getPrincipal());
            } catch (IncorrectCredentialsException ice) {
                // 密码错误
                log.info("Password for account " + token.getPrincipal() + " was incorrect!");
            } catch (LockedAccountException lae) {
                // 用户被锁定
                log.info("The account for username " + token.getPrincipal() + " is locked.  " +
                        "Please contact your administrator to unlock it.");
            }
           
            catch (AuthenticationException ae) {
                // 其他认证错误，AuthenticationException为其他认证异常的父类
            }
        }

        //say who they are:
        //print their identifying principal (in this case, a username):
        log.info("User [" + currentUser.getPrincipal() + "] logged in successfully.");

        // 判断用户是否拥有schwartz角色
        if (currentUser.hasRole("schwartz")) {
            log.info("May the Schwartz be with you!");
        } else {
            log.info("Hello, mere mortal.");
        }

        // 判断用户是否拥有lightsaber:wield权限
        if (currentUser.isPermitted("lightsaber:wield")) {
            log.info("You may use a lightsaber ring.  Use it wisely.");
        } else {
            log.info("Sorry, lightsaber rings are for schwartz masters only.");
        }

        // 同上，只是这里权限比较特殊
        if (currentUser.isPermitted("winnebago:drive:eagle5")) {
            log.info("You are permitted to 'drive' the winnebago with license plate (id) 'eagle5'.  " +
                    "Here are the keys - have fun!");
        } else {
            log.info("Sorry, you aren't allowed to drive the 'eagle5' winnebago!");
        }

        // 用户退出登录
        currentUser.logout();

        System.exit(0);
    }
```

