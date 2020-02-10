#### 安装目录

```
/etc/nginx
```



### 重启

```shell
nginx -s reload ## 重新载入配置文件
nginx -s reopen ## 重启 Nginx
nginx -s stop # #停止 Nginx
```

### 路由配置

如当前nginx服务器地址如下：

```sh
10.189.139.35
```

#### 请求转发

如下配置就是将10.190.147.31:8720服务器上的所有服务以syb开头的服务，将通过10.189.139.35来访问，如10.189.139.35/syb，实际访问的就是http://10.190.147.31:8720/syb，10.189.139.35/syb-pc实际访问的是

http://10.190.147.31:8720/syb-pc

```
location /syb {
        proxy_pass  http://10.190.147.31:8720;
  }
```

inginx中配置proxy_pass时，当在后面的url加上了"/"，相当于是绝对根路径，则nginx不会把location中匹配的路径部分代理走;如果没有"/"，则会把匹配的路径部分也给代理走。

如下面的配置，如果访问的是/ydjy-query/user，跳转的真实路径应该是http://10.190.131.41:9902/user，而不会加上匹配值/ydjy-query

```
location /ydjy-query {
      proxy_pass  http://10.190.131.41:9902/;
}
```

####  开启状态页

```sh
location /status {  
  stub_status on;   	#表示开启stubStatus的工作状态统计功能。
  access_log off;   	#access_log off; 关闭access_log 日志记录功能。
  #auth_basic "status";   							#auth_basic 是nginx的一种认证机制。
  #auth_basic_user_file conf/htpasswd;	#用来指定密码文件的位置。
}
```

