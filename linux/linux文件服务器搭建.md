### 配置信息

#### 配置文件保存路径

```sh
/usr/local/httpd/apache2/conf/httpd.conf
```

#### 资源文件存放路径

```shell
/medicare_files_server/szyb/    # 省医保资源存放路径
/medicare_files_server/ydjy/    # 异地就医资源存放路径
```

#### 账户配置

| 用户名    | sfp密码  | 备注 |
| --------- | -------- | ---- |
| szyb      | 2gjpd6tr |      |
| ydjy      | 2gjpd6tr |      |
| apmonitor | zmcdgppn |      |

####    服务重启

```sh
[root@trustsftp bin]# service apache stop
[root@trustsftp bin]# service apache start
[root@trustsftp bin]# service apache restart
```

