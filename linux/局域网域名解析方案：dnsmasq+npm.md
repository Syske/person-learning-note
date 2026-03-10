### 前言

自从买了`N1`盒子之后，我就开始了`DIY`自己的`NAS`之旅，但是随着玩法的升级，发现`N1`盒子的配置还是太低了，于是我便开始想着换配置更好的设备，刚好自己的第一台笔记本电脑还能开机启动（戴尔`N4010`），于是我便给老笔记本升级了内存，从之前的`6G`（`2G+4G`），升级为`8G`（`4G x 2`），虽然配置也不高，但是相比于`N1`盒子的`2G`，可玩性高了很多，客户部署更多的应用。

把玩过程中，发现所有服务都需要通过`ip` + 端口的方式访问，及其不方便，后来接触到`homepage`，基本能满足我的诉求，但是我还是想通过域名方式访问，主要是想学习下网络相关的知识，于是在`AI`的加持下，我了解到`dnsmasq`，最开始把玩并不顺利，踩了很多坑，也一直没有搞定，直到昨天，鬼使神差之下，我又想尝试下，然后很幸运地搞定了，于是就有了今天的分享。

因为`dnsmasq`服务需要用`53`端口，而`systemd-resolved`默认情况会占用这个端口， 所以如果机器本身有运行`systemd-resolved`，还需要禁用`systemd-resolved`的`dns`解析，方式也很简单，只需要修改配置，并重启`systemd-resolved`:

```ini
DNS=127.0.0.1
DNSStubListener=no
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/ec1114f8-e902-4501-a4a4-bf9069165752.jpg)

然后重启服务即可：
```sh
sudo systemctl restart systemd-resolved
```
### dnsmasq

`docker`直接运行：
```sh
docker run -d \
  --name dnsmasq \
  --restart unless-stopped \
  -p 53:53/udp \
  -p 53:53/tcp \
  -v /DATA/AppData/dnsmasq/conf/dnsmasq.conf:/etc/dnsmasq.conf \
  -v /DATA/AppData/dnsmasq/conf/resolv.dnsmasq.conf:/etc/resolv.dnsmasq.conf \
  -v /DATA/AppData/dnsmasq/conf/hosts:/etc/hosts \
  -v /DATA/AppData/dnsmasq/conf/dnsmasq.d:/etc/dnsmasq.d \
  --network=host \
  --cap-add=NET_ADMIN \
  andyshinn/dnsmasq:2.80
```
这里需要注意两个核心配置，一个是`network`要是`host`，另一个是容器的能力要`NET_ADMIN`

`compose`方式：

```yaml
name: vigilant_jaco
services:
  main_app:
    cap_add:
      - NET_ADMIN
    cpu_shares: 10
    command: []
    container_name: dnsmasq
    deploy:
      resources:
        limits:
          memory: 256M
    hostname: dnsmasq
    image: jpillora/dnsmasq:latest
    ports:
      - target: 53
        published: "5353"
    restart: unless-stopped
    volumes:
      - type: bind
        source: /DATA/AppData/dnsmasq/conf/dnsmasq.conf
        target: /etc/dnsmasq.conf
      - type: bind
        source: /DATA/AppData/dnsmasq/conf/resolv.dnsmasq.conf
        target: /etc/resolv.dnsmasq.conf
      - type: bind
        source: /DATA/AppData/dnsmasq/conf/hosts
        target: /etc/hosts
      - type: bind
        source: /DATA/AppData/dnsmasq/conf/dnsmasq.d
        target: /etc/dnsmasq.d
    devices: []
    environment: []
    network_mode: host
    privileged: false
```

下面解释下上面几个核心的配置：

#### dnsmasq.conf

`dnsmasq.conf`是最核心的配置，配置内容如下：
```ini
# 基本配置
# 只监听本机的网络接口，不监听公网
listen-address=127.0.0.1,192.168.0.103  # 请将 192.168.1.100 替换为你宿主机的局域网 IP

# 从这个文件读取局域网域名解析记录
addn-hosts=/etc/hosts

# 其他配置
conf-dir=/etc/dnsmasq.d

resolv-file=/etc/resolv.dnsmasq.conf
```

#### resolv.dnsmasq

`resolv.dnsmasq.conf`的作用是指定上游 `DNS` 服务器，这样当遇到`dnsmasq`无法解析的域名是，可以通过这里配置的`dns`进行域名解析
```c
nameserver 8.8.8.8
nameserver 114.114.114.114
```
#### `hosts`

这个配置和我们电脑的`hosts`没什么区别，从这个文件中读取本地域名解析（类似于 `/etc/hosts`）
```
127.0.0.1      localhost.localdomain
```

#### `dnsmasq.d`

这个目录下存放的是域名解析的配置，目前只存放了`address`相关的配置文件名无所谓，文件后缀名`conf`，我的配置内容如下：
```c
address=/syske.local/192.168.0.103

address=/test1.syske.local/192.168.0.101
address=/test2.syske.local/192.168.0.103
```

这里解释下，第一条配置的含义是将`syske.local`这个域名解析到`192.168.0.103`上，其余配置类似。

#### 测试

完成上述配置，并启动服务后，我们的域名解析就完成了，下面我们简单测试下，命令如下：
```sh
 nslookup syske.local 192.168.0.103
```
返回结果如下说明`dns`解析已经生效了，这里的`192.168.0.103`就是我们部署`dnsmasq`的服务器：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/4075067a-5879-4af4-9f55-d78d27d0688a.jpg)

#### 路由器配置

完成上面这些操作之后，域名解析虽然可以了，但是各个设备想要真正实现域名解析，还需要客户端配置`dns`地址，这样很不方便，而且接入新设备后，也需要单独设置。
为了更好地解决这个问题，我想到可以通过修改路由器`dns`配置来实现，实际操作后发现是可行的，操作方式如下：

`WLN`口`DNS`设置：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/f917ccfb-d664-404b-a8eb-18972a4aaecb.jpg)
`DHCP`设置`DNS`
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/4307018e-6984-45de-b110-75a6075deb60.jpg)

至此，我们的域名解析完美解决，下面我们搞点有意思的——二级域名解析
### npm

这里我直接选择`Nginx Proxy Manager`，和`Nginx`没有区别，增加了`web`管理界面，可以更方便地管理`nginx`配置：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/82f450c3-d540-4725-89f1-0522bf5c2367.jpg)
docker compose 配置如下：
```yaml
name: nginxproxymanager
services:
  nginxproxymanager:
    container_name: nginxproxymanager
    deploy:
      resources:
        reservations:
          memory: "134217728"
        limits:
          memory: 7838M
    image: jc21/nginx-proxy-manager:2.12.3
    labels:
      icon: https://cdn.jsdelivr.net/gh/IceWhaleTech/CasaOS-AppStore@main/Apps/NginxProxyManager/icon.png
    ports:
      - target: 80
        published: "80"
        protocol: tcp
      - target: 443
        published: "443"
        protocol: tcp
      - target: 81
        published: "81"
        protocol: tcp
    restart: unless-stopped
    volumes:
      - type: bind
        source: /DATA/AppData/nginxproxymanager/data
        target: /data
      - type: bind
        source: /DATA/AppData/nginxproxymanager/etc/letsencrypt
        target: /etc/letsencrypt
    x-casaos:
      ports:
        - container: "80"
          description:
            zh_cn: Nginx HTTP 端口
        - container: "443"
          description:
            zh_cn: Nginx HTTPS 端口
        - container: "81"
          description:
            en_us: WebUI Port
            zh_cn: WebUI 端口
      volumes:
        - container: /data
          description:
            zh_cn: Nginx 代理管理器数据目录。
        - container: /etc/letsencrypt
          description:
            zh_cn: Nginx 代理管理器 letsencrypt 目录。
    devices: []
    cap_add: []
    command: []
    environment: []
    network_mode: bridge
    privileged: false
    hostname: nginxproxymanager
    cpu_shares: 90
x-casaos:
  architectures:
    - amd64
    - arm64
    - arm
  author: CasaOS Team
  category: Network
  description:
    zh_cn: Nginx 代理管理器是一个简单、强大的工具，可帮助您在单个服务器上托管多个网站。
  developer: Nginx Proxy Manager
  icon: https://cdn.jsdelivr.net/gh/IceWhaleTech/CasaOS-AppStore@main/Apps/NginxProxyManager/icon.png
  index: /
  is_uncontrolled: false
  main: nginxproxymanager
  port_map: "81"
  store_app_id: nginxproxymanager
  tagline:
    zh_cn: 通过简单、强大的界面管理 Nginx 代理主机。
  thumbnail: https://cdn.jsdelivr.net/gh/IceWhaleTech/CasaOS-AppStore@main/Apps/NginxProxyManager/thumbnail.png
  tips:
    before_install:
      zh_cn: |
        ⚠️ 警告！
        这是一个技术类应用，请确保你知道你在做什么。
        Nginx Proxy Manager 默认占用 80 和 443 端口给内置 Nginx 使用。占用 81 端口给管理页面。
        请将 CasaOS WebUI 端口改为非 80/81/443 的端口。并注意是否与其他应用冲突。否则可能导致你的 CasaOS 运行异常。

        默认管理员用户

        | 用户名 | 密码 |
        | -------- | -------- |
        | `admin@example.com` | `changeme` |
  title:
    zh_cn: Nginx 代理管理器
    custom: ""
  hostname: ""
  scheme: http
```
`npm`的默认账号和密码分别是`admin@example.com`和`changeme`。

服务启动后，我们直接增加代理配置即可，`Forward Hostname/IP`直接填写我们的二级域名，端口默认`80`:
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/41e29f37-bcad-44f0-9fe6-462d86c8bd76.jpg)

路径配置这里直接写具体的服务地址和端口即可

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/d3c88040-f3c5-416f-939c-db4ca0869d99.jpg)

至此，我们就可以直接通过二级域名访问我们的服务了。
有个点需要注意下，如果服务本身需要支持`websocket`，需要开启`Websockets Suppert`开关，否则会报错：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/a07d7941-d643-4ea7-98a8-d5d976abdd9b.jpg)

### 小结

简单小结一下，这个事情上次其实已经搞过一次，由于当时`dnsmasq`配置问题，域名解析一直不生效，所以就搁置了，然后刚好昨天没啥事，晚上回来就研究了下，终于搞定了。

现在回过头来看，其实问题就出在端口上，和`systemd-resolved`端口冲突了，当时虽然将端口修改为`5353`，但是由于`dns`服务默认服务端口是`53`，所以`dns`解析实际没生效。

另外一点是，当时一直依赖`AI`解决问题，并不清楚其中原理，所以疯狂踩坑，从这一点来说，我们其实也不能太过依赖`AI`工具，特别是我们不清楚不了解的情况下。

好了，今天的分享就到这里，给大家分享几款适合在`Casaos`跑的软件，有兴趣的小伙伴可以把玩下，后面我可以详细分享下：

- `homepage`：搭建自己的首页导航，颜值也是能打的
	![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/9108c83b-22ba-4b87-9326-c547554b60a1.jpg)

- Syncthing：贼好用的局域网数据备份软件，可以将手机数据同步并备份，而且还支持跨平台，安卓、 `windows`、苹果都可以
	![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/7738286d-7ac8-4192-8448-80d90ad72539.jpg)
- Emby：个人媒体解决方案的扛把子，实现在线追剧自由
	![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/6a70a0bc-7fb3-4634-a04e-fbc3ff5d14c5.jpg)
- PhotoPrism：如果你还在烦恼照片管理问题，那这个工具无疑是你最好的选择，支持按场景和任务、地点等管理图片，组合`syncthing`，简直不要太好
	![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/b5c37c21-6af5-4c8e-94ac-d5e1de01b761.jpg)
- Next Terminal：轻量级的堡垒机，方便管理多个资产
	![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/82236df1-be93-4822-98d3-68e6ec3ce5f5.jpg)
好了，今天的内容就分享到这里，感谢你看到这里，国庆节快乐呀~