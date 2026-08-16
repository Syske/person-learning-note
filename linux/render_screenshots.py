# -*- coding: utf-8 -*-
"""把终端命令输出渲染成终端风格截图 PNG(PIL)"""
from PIL import Image, ImageDraw, ImageFont
import os

FONT = r"C:\Windows\Fonts\msyh.ttc"   # 微软雅黑,支持中文
FONT_SMALL = r"C:\Windows\Fonts\msyh.ttc"
IMG_DIR = r"D:\workspace\learning\person-learning-note\linux\images"

def render(name, title, lines, bg=(18, 24, 34), fg=(220, 225, 232), accent=(94, 188, 108), prompt=(80, 170, 255)):
    """lines: list of (type, text)  type in {cmd, out, accent, comment}"""
    font = ImageFont.truetype(FONT, 17)
    # char_w = font.getbbox("W")[2]  # 中文用getlength计算宽度
    line_h = 30
    title_h = 40
    pad = 16
    # 计算宽度
    max_w = 0
    for _, t in lines:
        max_w = max(max_w, font.getlength(t))
    max_w = max(max_w, font.getlength(title))
    W = int(max_w) + pad * 2 + 20
    H = title_h + line_h * len(lines) + pad * 2

    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)

    # 标题栏(仿终端窗口)
    d.rectangle([0, 0, W, title_h], fill=(38, 46, 60))
    for i, (cx, col) in enumerate([(10, (255,95,86)), (34, (255,189,46)), (58, (39,201,63))]):
        d.ellipse([cx, 12, cx+12, 24], fill=col)
    title_font = ImageFont.truetype(FONT, 14)
    d.text((86, 10), title, font=title_font, fill=(160, 168, 180))

    y = title_h + pad
    for typ, t in lines:
        color = fg
        if typ == "cmd":
            color = prompt
        elif typ == "accent":
            color = accent
        elif typ == "comment":
            color = (140, 150, 165)
        d.text((pad, y), t, font=font, fill=color)
        y += line_h

    out = os.path.join(IMG_DIR, name)
    img.save(out)
    print("已生成:", out, f"{W}x{H}")

# ===== 1. DNS 污染解析 =====
render("dns-pollution.png", "syske@ubuntu:~", [
    ("cmd", "$ nslookup www.google.com"),
    ("out", "Server:    127.0.0.1"),
    ("out", "Address:   127.0.0.1#53"),
    ("out", ""),
    ("out", "Non-authoritative answer:"),
    ("out", "Name:  www.google.com"),
    ("accent", "Address: 157.240.7.20      # 污染!非Google官方IP"),
    ("accent", "Address: 2001::1           # 异常IPv6(loopback)"),
    ("comment", "真实 Google IP 应为 142.250.x.x / 172.217.x.x 网段"),
])

# ===== 2. 各上游对比 =====
render("dns-upstream-compare.png", "syske@ubuntu: 上游DNS质量对比", [
    ("cmd", "$ dig @223.5.5.5 www.google.com +short"),
    ("accent", "157.240.7.20              # 阿里 污染"),
    ("cmd", "$ dig @119.29.29.29 www.google.com +short"),
    ("accent", "185.45.5.35               # 腾讯 污染"),
    ("cmd", "$ dig @114.114.114.114 www.google.com +short"),
    ("out", "142.251.150.119            # 114 真实IP ✅"),
    ("cmd", "$ dig @8.8.8.8 www.google.com +short"),
    ("accent", "157.240.7.20              # 谷歌 被墙干扰"),
    ("cmd", "$ dig @1.1.1.1 www.google.com +short"),
    ("accent", "157.240.7.20              # CF 被墙干扰"),
    ("comment", "结论: 8.8.8.8 / 1.1.1.1 在国内直连 DNS 查询不稳定, 是解析偶尔失效的元凶"),
])

# ===== 3. 修复前 tcpdump:5上游并发 =====
render("dns-tcpdump-before.png", "syske@ubuntu: tcpdump 修复前(5上游并发)", [
    ("cmd", "$ sudo tcpdump -i any -n port 53"),
    ("out", "IP 127.0.0.1.45915 > 127.0.0.1.53: 25318+ A? test.example.com"),
    ("accent", "IP 192.168.0.103.55540 > 223.5.5.5.53:      53739+ A? test.example.com"),
    ("accent", "IP 192.168.0.103.55540 > 119.29.29.29.53:   53739+ A? test.example.com"),
    ("accent", "IP 192.168.0.103.55540 > 114.114.114.114.53: 53739+ A? test.example.com"),
    ("accent", "IP 192.168.0.103.55540 > 8.8.8.8.53:        53739+ A? test.example.com"),
    ("accent", "IP 192.168.0.103.55540 > 1.1.1.1.53:        53739+ A? test.example.com"),
    ("comment", "dnsmasq 并发查询全部 5 个上游, 取第一个响应"),
    ("out", "IP 1.1.1.1.53 > 192.168.0.103.55540: 53739$ 0/1/1 (129)"),
    ("comment", "只有 1.1.1.1 返回, 其余 4 个超时 -> 偶发解析失败"),
])

# ===== 4. 修复后 tcpdump:仅国内 =====
render("dns-tcpdump-after.png", "syske@ubuntu: tcpdump 修复后(仅国内DNS)", [
    ("cmd", "$ sudo tcpdump -i any -n 'udp and port 53 and src 192.168.0.103'"),
    ("accent", "IP 192.168.0.103.45794 > 223.5.5.5.53:      3319+ A? verify.test.com"),
    ("accent", "IP 192.168.0.103.26895 > 223.5.5.5.53:      27137+ A? www.jd.com"),
    ("accent", "IP 192.168.0.103.13765 > 223.5.5.5.53:      5371+ A? down.huorong.cn"),
    ("accent", "IP 192.168.0.103.13765 > 119.29.29.29.53:   5371+ A? down.huorong.cn"),
    ("accent", "IP 192.168.0.103.13765 > 114.114.114.114.53: 5371+ A? down.huorong.cn"),
    ("comment", "8.8.8.8 / 1.1.1.1 已移除, 全部走国内 DNS"),
])

# ===== 5. Clash 502 对比 =====
render("clash-502-compare.png", "syske@Windows: 直连 vs 代理", [
    ("cmd", "$ curl --noproxy '*' -s -o /dev/null -w 'HTTP:%{http_code} %{time_total}s' -m 6 http://syske.local"),
    ("out", "HTTP:200 0.05s                    # 直连 正常 ✅"),
    ("cmd", "$ curl -x http://127.0.0.1:7897 -s -o /dev/null -w 'HTTP:%{http_code} %{time_total}s' -m 8 http://syske.local"),
    ("accent", "HTTP:502 0.03s                    # 走 Clash 代理 502 ❌"),
    ("comment", "根因: syske.local 是域名, 不匹配代理绕过列表(只有IP网段), 被转发到外网节点"),
])

# ===== 6. Beecount 健康检查 =====
render("beecount-health.png", "syske@ubuntu: beecount-cloud 验证", [
    ("cmd", "$ curl http://127.0.0.1:8869/healthz"),
    ("accent", '{"status":"ok"}'),
    ("cmd", "$ docker ps --filter name=beecount-cloud"),
    ("out", "stirring_hidenori-beecount-cloud-1 | Up 8 minutes (healthy) | 0.0.0.0:8869->8080/tcp"),
    ("cmd", "$ docker inspect stirring_hidenori-beecount-cloud-1 --format '{{range .Mounts}}{{.Source}}->{{.Destination}}{{end}}'"),
    ("accent", "/DATA/AppData/beecount-cloud/data->/data   # 持久卷 ✅"),
])

print("全部渲染完成")
