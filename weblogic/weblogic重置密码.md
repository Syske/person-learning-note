- 1、备份文件如下文件
``` 
%DOMAIN_HOME%/security/DefaultAuthenticatorInit.ldift
```
- 2、进入%DOMAIN_HOME%/security目录，执行下列命令：
```
　　java -classpath D:/bea10/wlserver_10.0/server/lib/weblogic.jar weblogic.security.utils.AdminAccount <NewAdminUserName> <NewAdminPassword> .
```
　　特别注意最后有个“ .”，一个空格和一个点。

- 3、将%DOMAIN_HOME%/servers/AdminServer下的data目录重命名，如：data_old。或者备份到别的地方。

- 4、修改boot.properties，将usernmae和password重设为明文，如：
```
password=weblogic
username=weblogic
```
　
　　其中的用户名和密码与第二步中一致。
- 5、重启weblogic即可。