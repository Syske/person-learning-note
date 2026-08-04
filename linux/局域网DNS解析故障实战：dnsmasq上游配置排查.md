# 局域网DNS解析偶尔失效实战排查：dnsmasq上游配置

> 背景：局域网内域名解析（`*.syske.local`）偶尔不生效，个别域名解析缓慢或失败。
> 本文记录完整的排查思路、根因定位与修复过程，补充《局域网域名解析方案：dnsmasq+npm》的故障排查篇。

## 一、问题现象

- 局域网内通过 `192.168.0.103`（dnsmasq 服务器）解析域名**偶尔失败/超时**
- 部分国外域名（如 `www.google.com`）解析出异常 IP：`69.171.235.22`（Facebook 网段）、`174.132.167.252` 等
- 系统 DNS 指向 `192.168.0.103`

## 二、排查过程

### 1. 基础连通性检查

```bash
# 内网网关
ping 192.168.0.1            # 1ms 正常
# 公网 IP
ping 223.5.5.5              # 7ms 正常
# 域名解析
nslookup www.baidu.com      # 正常
nslookup www.google.com     # 返回可疑 IP: 185.45.5.35 / 2001::1
```

> 关键线索：`www.google.com` 解析出非 Google 官方 IP，说明上游 DNS 有污染或异常。

![DNS污染解析](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/0d724276-b7ec-4d5f-bfad-146672303248.jpg)

### 2. 确认 DNS 服务与配置

```bash
# 谁在监听 53 端口
ss -tlnp | grep ':53'

# 发现 webproc + dnsmasq 组合（webproc 是带 Web 管理界面的进程守护工具）
ps aux | grep -E 'webproc|dnsmasq'
# root 2014 webproc --config /etc/dnsmasq.conf -- dnsmasq --no-daemon
# root 2122 /usr/sbin/dnsmasq --no-daemon

# 配置文件实际位置（webproc 容器化部署，宿主 /etc 看不到，但 /DATA 卷在）
ls /DATA/AppData/dnsmasq/conf/
# dnsmasq.conf  resolv.dnsmasq.conf  dnsmasq.d/  hosts
```

### 3. 核心配置分析

`/DATA/AppData/dnsmasq/conf/resolv.dnsmasq.conf`（上游 DNS）：

```
nameserver 223.5.5.5        # 阿里
nameserver 119.29.29.29     # 腾讯
nameserver 114.114.114.114  # 114
nameserver 8.8.8.8          # 谷歌（国内被墙）
nameserver 1.1.1.1          # Cloudflare（国内被墙）
```

### 4. 抓包定位上游行为（关键一步）

```bash
sudo tcpdump -i any -n port 53
# 查询一个冷域名时，dnsmasq 并发向 5 个上游发查询：
# 192.168.0.103.55540 > 223.5.5.5.53
# 192.168.0.103.55540 > 119.29.29.29.53
# 192.168.0.103.55540 > 114.114.114.114.53
# 192.168.0.103.55540 > 8.8.8.8.53
# 192.168.0.103.55540 > 1.1.1.1.53
# 但最终只有 1.1.1.1 返回响应，其余全部超时
```

![5上游并发抓包](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/30c5600d-1e55-4d99-b8a5-8b5d1c900d81.jpg)

### 5. 上游质量对比测试

![各上游解析google对比](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/9da8a40e-0350-41a0-9961-fb5eb5a4278a.jpg)

```bash
# 查询 www.baidu.com 各上游延迟
dig @223.5.5.5 www.baidu.com      # 7ms ✅
dig @119.29.29.29 www.baidu.com   # 31ms ✅
dig @114.114.114.114 www.baidu.com# 35ms ✅
dig @8.8.8.8 www.baidu.com        # 59ms ⚠️
dig @1.1.1.1 www.baidu.com        # 63ms ⚠️

# 查询 www.google.com 各上游结果（污染对比）
dig @223.5.5.5 www.google.com     # 69.171.235.22（Facebook，污染）
dig @119.29.29.29 www.google.com  # 185.45.5.35（垃圾，污染）
dig @114.114.114.114 www.google.com# 142.251.156.119（真实 IP ✅）
dig @8.8.8.8 www.google.com       # 174.132.167.252（被墙干扰）
dig @1.1.1.1 www.google.com       # 174.132.167.252（被墙干扰）
```

## 三、根因分析

1. **dnsmasq 并发查询全部上游，取第一个返回的结果**。上游同时包含国内（快、准）和国外（被墙、慢、易丢包）DNS。
2. 8.8.8.8 / 1.1.1.1 直连 DNS 查询在国内经常被 GFW 丢弃或干扰：
   - 被丢弃 → 查询整体超时 → **解析偶尔失败（用户感知"不生效"）**
   - 被干扰 → 返回污染 IP → **解析出错误结果**
3. 国内 DNS 对 google 等国外域名的响应也被污染（返回 Facebook IP 等），只有 114 返回了真实 IP。

## 四、解决方案

### 1. 修改上游 DNS，去掉被墙的国外 DNS

`/DATA/AppData/dnsmasq/conf/resolv.dnsmasq.conf`：

```
# 国内 DNS（去掉被墙的 8.8.8.8 / 1.1.1.1，避免解析超时）
nameserver 223.5.5.5        # 阿里 DNS
nameserver 119.29.29.29     # 腾讯 DNS
nameserver 114.114.114.114  # 114 DNS
```

### 2. 热重载（无需重启，DNS 无中断）

```bash
# 备份
cp resolv.dnsmasq.conf resolv.dnsmasq.conf.bak
# 找到 dnsmasq PID（用 pgrep -x 而非 pgrep -f，避免误匹配）
pgrep -x dnsmasq            # 2122
sudo kill -HUP 2122         # SIGHUP 重新加载 resolv 配置并清缓存
```

> ⚠️ 注意：`pgrep -f 'dnsmasq --no-daemon'` 会误匹配到 shell 命令行本身，务必用 `pgrep -x dnsmasq`。

## 五、验证

```bash
# 抓包确认只发国内 DNS
sudo tcpdump -i any -n 'udp and port 53 and src 192.168.0.103'
# 输出只有 223.5.5.5 / 119.29.29.29 / 114.114.114.114

# 稳定性测试
for i in $(seq 1 30); do
  r=$(dig @127.0.0.1 www.baidu.com +time=2 +tries=1 +short | head -1)
  [ -z "$r" ] && FAIL=$((FAIL+1))
done
echo "失败: $FAIL/30"       # 0/30

# 局域网域名
dig @127.0.0.1 syske.local       # 192.168.0.103
dig @127.0.0.1 n1.syske.local    # 192.168.0.101
```

![修复后仅国内DNS](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/afb74954-efeb-4dc6-bc45-679b08278d6a.jpg)

## 六、经验总结

1. **dnsmasq 上游不要混搭被墙 DNS**——被墙 DNS 超时会拖垮整个解析链路
2. **定位 DNS 问题三件套**：`dig` 对比各上游、`tcpdump` 抓 53 端口看实际发往、`pgrep -x` 找进程
3. **SIGHUP 热重载** vs 重启：改 resolv 配置用 SIGHUP 即可，无中断
4. **容器化部署的配置位置**：宿主机的 `/DATA/AppData/*` 卷挂载到容器 `/etc`，修改卷文件即生效（`/proc/<pid>/root/etc/` 可验证容器内视角）
5. 国外域名（google 等）国内 DNS 会返回污染 IP，但走代理访问时由代理客户端自行解析，不受影响；如需真实 IP 可按域名分流：`server=/google.com/114.114.114.114`
