 server {
			  listen 8080;
			  server_name 127.0.0.1:8080;
			  
				underscores_in_headers on;
			  
			  location /syb/ {			
			    proxy_redirect off;
				proxy_set_header Host $host;
				proxy_set_header X-Real-IP $remote_addr;
				proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
				proxy_pass http://127.0.0.1:8083;
				}
				
				location /syb-pc/ {				
			    proxy_redirect off;
				proxy_set_header Host $host;
				proxy_set_header X-Real-IP $remote_addr;
				proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
				proxy_pass http://127.0.0.1:8083;
				}
				
				location /sso/ {				
			    proxy_redirect off;
				proxy_set_header Host $host;
				proxy_set_header X-Real-IP $remote_addr;
				proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
				proxy_pass http://127.0.0.1:8088;
				}
				
				location /api/ {
				 if ( $request_method = 'OPTIONS' ) { 
					add_header Access-Control-Allow-Origin $http_origin; 
					add_header Access-Control-Allow-Headers Authorization,access-token,Content-Type,Accept,Origin,User-Agent,DNT,Cache-Control,X-Mx-ReqToken,X-Data-Type,X-Requested-With; 
					add_header Access-Control-Allow-Methods GET,POST,OPTIONS,HEAD,PUT; 
					add_header Access-Control-Allow-Credentials true; 
					add_header Access-Control-Allow-Headers X-Data-Type,X-Auth-Token;
					return 200;
	    }
				proxy_next_upstream http_502 http_504 error timeout invalid_header;				
			    proxy_redirect off;
				proxy_set_header Host $host;
				proxy_set_header X-Real-IP $remote_addr;
				proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
				proxy_pass http://127.0.0.1:8081;
				}		
			}
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

如下配置就是将`10.190.147.31:8720`服务器上的所有服务以`syb`开头的服务，将通过`10.189.139.35`来访问，如`10.189.139.35/syb`，实际访问的就是`http://10.190.147.31:8720/syb`，`10.189.139.35/syb-pc`实际访问的是

```
http://10.190.147.31:8720/syb-pc
```



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



#### 单点登陆token共享配置

```nginx
 server {
			  listen 8080;
			  server_name 127.0.0.1:8080;
			  
				underscores_in_headers on;
			  
			  location /syb/ {			
			    proxy_redirect off;
				proxy_set_header Host $host;
				proxy_set_header X-Real-IP $remote_addr;
				proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
				proxy_pass http://127.0.0.1:8083;
				}
				
				location /syb-pc/ {				
			    proxy_redirect off;
				proxy_set_header Host $host;
				proxy_set_header X-Real-IP $remote_addr;
				proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
				proxy_pass http://127.0.0.1:8083;
				}
				
				location /sso/ {				
			    proxy_redirect off;
				proxy_set_header Host $host;
				proxy_set_header X-Real-IP $remote_addr;
				proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
				proxy_pass http://127.0.0.1:8088;
				}
				
				location /api/ {
				 if ( $request_method = 'OPTIONS' ) { 
					add_header Access-Control-Allow-Origin $http_origin; 
					add_header Access-Control-Allow-Headers Authorization,access-token,Content-Type,Accept,Origin,User-Agent,DNT,Cache-Control,X-Mx-ReqToken,X-Data-Type,X-Requested-With; 
					add_header Access-Control-Allow-Methods GET,POST,OPTIONS,HEAD,PUT; 
					add_header Access-Control-Allow-Credentials true; 
					add_header Access-Control-Allow-Headers X-Data-Type,X-Auth-Token;
					return 200;
        }
				proxy_next_upstream http_502 http_504 error timeout invalid_header;				
			    proxy_redirect off;
				proxy_set_header Host $host;
				proxy_set_header X-Real-IP $remote_addr;
				proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
				proxy_pass http://127.0.0.1:8081;
				}		
			}
```

