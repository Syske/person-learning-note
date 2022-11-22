# NGINX本地目录映射

今天推送给一个小的知识点，感觉在日常开发中可能比较有用：NGINX本地目录映射。如果遇到类似需求的时候。各位小伙伴可以参考。

## window

因为每天都要发布每日读书札记，所以需要图片的`http`地址，但是有时候我对随机获取的图片不满意，但是`gitee`图床又限制大小，直接使用网页上的地址又不行（`wallhave`网站的壁纸真的美），所以我就把图片保存到本地，然后在本地启动`nginx`服务器，然后访问对应的图片，所以也就有了今天的这个小小的学习笔记。

首先我增加了一个`location`节点增加如下配置：

```nginx
location /images/ {
			root /;
			rewrite ^/images/(.*)$ \Users\Administrator\Pictures\wallhave\$1 break;
        }
```

我的`nginx`安装目录：

```
D:\software\server\nginx-1.17.9
```

根据我的试验，得出一下结论：

- 在`windows`环境下，`\`指的就是当前安装磁盘的根目录

- `rewrite`就是要拿到你的请求地址，然后重新定向到你指的的目录下，比如我要映射的目录是：

  ```
  D:\Users\Administrator\Pictures\wallhave\
  ```

  如果我要访问这个目录下的图片（图片名`wallhaven-y8m9ox.png`），那我的请求链接是这样的：

  ```
  http://localhost:80/images/wallhaven-y8m9ox.png
  ```

  访问效果如下：
  
  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20210225203822.png)

 `nginx`完整配置如下：

```nginx
#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;

events {
    worker_connections  1024;
}


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
        
        location /images/ {
			root /;
			rewrite ^/images/(.*)$ \Users\Administrator\Pictures\wallhave\$1 break;
        }

        location / {
            root   html;
            index  index.html index.htm;
        }
        
        location /wx {
            proxy_pass http://127.0.0.1:8081;
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
   
    }

}
```

