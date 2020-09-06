### 配置文件

打开conf下的nginx.conf配置文件，默认配置应该是这样的：

```nginx

http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;

    server {
        listen       80;
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            root   html;
            index  index.html index.htm;
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }

        # proxy the PHP scripts to Apache listening on 127.0.0.1:80
        #
        #location ~ \.php$ {
        #    proxy_pass   http://127.0.0.1;
        #}

        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        #
        #location ~ \.php$ {
        #    root           html;
        #    fastcgi_pass   127.0.0.1:9000;
        #    fastcgi_index  index.php;
        #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
        #    include        fastcgi_params;
        #}

        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #
        #location ~ /\.ht {
        #    deny  all;
        #}
    }


    # another virtual host using mix of IP-, name-, and port-based configuration
    #
    #server {
    #    listen       8000;
    #    listen       somename:8080;
    #    server_name  somename  alias  another.alias;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}


    # HTTPS server
    #
    #server {
    #    listen       443 ssl;
    #    server_name  localhost;

    #    ssl_certificate      cert.pem;
    #    ssl_certificate_key  cert.key;

    #    ssl_session_cache    shared:SSL:1m;
    #    ssl_session_timeout  5m;

    #    ssl_ciphers  HIGH:!aNULL:!MD5;
    #    ssl_prefer_server_ciphers  on;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}

}
```

#### nginx 文件结构

```nginx
...              #全局块

events {         #events块
   ...
}

http      #http块
{
    ...   #http全局块
    server        #server块
    { 
        ...       #server全局块
        location [PATTERN]   #location块
        {
            ...
        }
        location [PATTERN] 
        {
            ...
        }
    }
    server
    {
      ...
    }
    ...     #http全局块
}
```

- 1、**全局块**：配置影响nginx全局的指令。一般有运行nginx服务器的用户组，nginx进程pid存放路径，日志存放路径，配置文件引入，允许生成worker process数等。
- 2、**events块**：配置影响nginx服务器或与用户的网络连接。有每个进程的最大连接数，选取哪种事件驱动模型处理连接请求，是否允许同时接受多个网路连接，开启多个网络连接序列化等。
- 3、**http块**：可以嵌套多个server，配置代理，缓存，日志定义等绝大多数功能和第三方模块的配置。如文件引入，mime-type定义，日志自定义，是否使用sendfile传输文件，连接超时时间，单连接请求数等。
- 4、**server块**：配置虚拟主机的相关参数，一个http中可以有多个server。
- 5、**location块**：配置请求的路由，以及各种页面的处理情况。

其中基本的配置结构是这样的：

```nginx
server {
        listen       80;   # 监听的端口
        server_name  localhost; # 监听地址

        #charset koi8-r;  # 编码

        #access_log  logs/host.access.log  main; # 访问日志

        location / {  #转发规则
            root   html;
            index  index.html index.htm;
        }
```



### 路由配置

如当前nginx服务器地址如下：

```sh
127.0.0.35
```

#### 请求转发

如下配置就是将`127.0.0.31:8720`服务器上的所有服务以`test`开头的服务，将通过`127.0.0.35`来访问，如`127.0.0.35/test`，实际访问的就是`http://127.0.0.31:8720/test`，`127.0.0.35/test-pc`实际访问的是

```
http://127.0.0.31:8720/test-pc
```



```nginx
location /test {
        proxy_pass  http://127.0.0.31:8720;
  }
```

nginx中配置proxy_pass时，当在后面的url加上了"/"，相当于是绝对根路径，则nginx不会把location中匹配的路径部分代理走;如果没有"/"，则会把匹配的路径部分也给代理走。

如下面的配置，如果访问的是/test-query/user，跳转的真实路径应该是http://127.0.0.41:9902/user，而不会加上匹配值/test-query

```nginx
location /test-query {
      proxy_pass  http://127.0.0.41:9902/;
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
			  
			  location /test/ {			
			    proxy_redirect off;
				proxy_set_header Host $host;
				proxy_set_header X-Real-IP $remote_addr;
				proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
				proxy_pass http://127.0.0.1:8083;
				}
				
				location /test-pc/ {				
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

### 重启

```shell
nginx -s reload ## 重新载入配置文件
nginx -s reopen ## 重启 Nginx
nginx -s stop # #停止 Nginx
```

### 