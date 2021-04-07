## weblogic修改密码方法：
## 1、正常修改方法：
#### 第一步

登录控制台–》安全领域–》用户和组里修改密码

![](https://gitee.com/sysker/picBed/raw/master/images/1568941214337.png)

![](https://gitee.com/sysker/picBed/raw/master/images/1568941347550.png)

![](https://gitee.com/sysker/picBed/raw/master/images/1568941564506.png)

#### 第二步

在域目录下`$BEA_BASE/user_projects/domains/{your domain name}/servers/AdminServer/security/ `修改`boot.properties`里的

```properties
username=新的用户名
password=新的密码
```

如下：

```sh
[root@pms22 security]# pwd
/home/weblogic/bea/user_projects/domains/sggis/servers/AdminServers/security
[root@pms22 security]# cat boot.properties
password={AES}adfpetqgjpqtojewp085oladfaldfladfl\=
username={AES}adfhfhtynbbmomflkhmlfhjoewyhsd6ser\=
```



保存后重启`weblogic`服务

```sh
[root@pms22 bin]# pwd
/home/weblogic/bea/user_projects/domains/sggis/bin
[root@pms22 bin]# ./startweblogic.sh
```



## 2、替换文件法:
我们知道`weblogic`有一个`adminaccount`工具，可以刷新账户密码，那么该怎么用呢?

```sh
java -cp $BEA_HOME/wlserver_10.3/server/lib/weblogic.jar weblogic.security.utils.AdminAccount username password . 
```

这里需要注意**结尾有个点**，然后将生成的文件替换掉域目录下的`DefaultAuthenticatorInit.idift`
如图：

```shell
[root@pms22 security]# pwd
/home/weblogic/bea/user_projects/domains/sggis/security
[root@pms22 security]# ll
total 36
-rwxr-xr-x 1 weblogic weblogic 3301 oct 29 2016 DefaultAuthenticatorInit.ldift
-rwxr-xr-x 1 weblogic weblogic 2398 oct 23 2015 DefaultRoleMapperInit.ldift
```

替换之后再修改`boot.properties`文件里的用户名和密码，再重启服务。

#### 3、特殊情况处理

如果确认密码修改没有问题，但启动服务却依然提示如下错误：

![](https://gitee.com/sysker/picBed/raw/master/images/1568994238747.png)

```sh
weblogic.security.SecurityInitializationException: Authentication denied: Boot identity not valid; The user name and/or password from the boot identity file (boot.properties) is not valid. The boot identity may have been changed since the boot identity file was created. Please edit and update the boot identity file with the proper values of username and password. The first time the updated boot identity file is used to start the server, these new values are encrypted.
	at weblogic.security.service.CommonSecurityServiceManagerDelegateImpl.doBootAuthorization(CommonSecurityServiceManagerDelegateImpl.java:960)
	at weblogic.security.service.CommonSecurityServiceManagerDelegateImpl.initialize(CommonSecurityServiceManagerDelegateImpl.java:1054)
	at weblogic.security.service.SecurityServiceManager.initialize(SecurityServiceManager.java:888)
	at weblogic.security.SecurityService.start(SecurityService.java:141)
	at weblogic.t3.srvr.SubsystemRequest.run(SubsystemRequest.java:64)
	Truncated. see log file for complete stacktrace
Caused By: javax.security.auth.login.FailedLoginException: [Security:090304]Authentication Failed: User weblogic javax.security.auth.login.FailedLoginException: [Security:090302]Authentication Failed: User weblogic denied
	at weblogic.security.providers.authentication.LDAPAtnLoginModuleImpl.login(LDAPAtnLoginModuleImpl.java:261)
	at com.bea.common.security.internal.service.LoginModuleWrapper$1.run(LoginModuleWrapper.java:110)
	at java.security.AccessController.doPrivileged(Native Method)
	at com.bea.common.security.internal.service.LoginModuleWrapper.login(LoginModuleWrapper.java:106)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	Truncated. see log file for complete stacktrace
> 
```

处理办法如下：

- 先考虑删除`servers/{服务名}/data/ldap`文件夹，然后重启服务，若问题为解决，请试下面的方法

- 检查启动脚本中是否配置如下参数（用户名及密码）：`bin/startManagedWebLogic.sh`、`bin/startWebLogic.sh`

- `WLS_USER`（用户名）及`WLS_PW`（密码）

  如果有以上配置，则需删除或注释掉以上配置后重启服务

**说明：**对于生产模式，在`boot.properties`文件中配置了用户名及密码后，不用再在启动脚本中配置用户名及密码，更重要的是容易泄露用户名及密码！！！！！