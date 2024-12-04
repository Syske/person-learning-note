#### 1、备份文件

备份如下文件

``` sh
%DOMAIN_HOME%/security/DefaultAuthenticatorInit.ldift
```
#### 2、重置密码

进入`%DOMAIN_HOME%/security`目录，执行下列命令：

```sh
java -classpath D:/bea10/wlserver_10.0/server/lib/weblogic.jar weblogic.security.utils.AdminAccount <NewAdminUserName> <NewAdminPassword> .
```
　　特别注意最后有个“ .”，一个空格和一个点。

#### 3、重命名data文件夹

将`%DOMAIN_HOME%/servers/AdminServer`下的`data`目录重命名，如：`data_old`。或者备份到别的地方。

#### 4、修改配置文件

打开`boot.properties`文件，将`usernmae`和`password`重设为明文，如：

```sh
password=weblogic
username=weblogic
```

　　其中的用户名和密码与第二步中一致。

#### 5、重启`weblogic`即可。