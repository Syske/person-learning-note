## body请求太大导致报错

报错信息提示 ：

```
client intended to send too large chunked body
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/6f79ce02-af49-4f0e-94c3-8c7b09680743.jpg)
### 解决方案

```
http {
    # ...
    client_max_body_size 20M;  # Sets maximum body size to 20 megabytes
    # ...
}
```
或者

```
server {
    # ...
    client_max_body_size 50M;  # For this server only
    # ...
}

location /upload {
    client_max_body_size 100M;  # For this specific location
}
```