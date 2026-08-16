# BeeCount登录页访问慢：Google Fonts被墙排查与优化

> 背景：自部署 BeeCount-Cloud 后,浏览器访问 `http://192.168.0.103:8869/login` 很慢(白屏等待)。
> 本文记录排查过程与 Clash 规则优化方案。由 `doc-publish` skill 生成发布。

## 一、问题现象

浏览器打开登录页要等很久才显示(疑似白屏十几秒)。

## 二、排查过程

### 1. 服务端处理是否慢？—— 不慢

```bash
# Windows 侧计时
curl -w '总耗时:%{time_total}s' http://192.168.0.103:8869/login
# HTTP:200 总耗时:0.030s / 0.022s / 0.022s
```

![login页访问计时](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/dfc3eb9e-a54e-4132-820b-c6782f45326e.jpg)

容器日志显示 `/login` 处理仅 **3.8~5.5ms**,CPU 0.3%、内存 97MB——服务端和资源都正常。

### 2. 页面引用了什么外部资源？

抓 login 页 HTML,发现 **render-blocking 的 Google Fonts 引用**:

```html
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined...">
<link rel="preconnect" href="https://fonts.gstatic.com">
```

主 JS(856KB)下载只要 0.18s,HTML 才 5.3KB。**慢的不是页面本身,是外部字体 CSS**。

### 3. Google Fonts 直连 —— 被墙

```bash
curl -w '耗时:%{time_total}s' https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined
# 耗时:15.01s  (15s 超时, 连接未建立)
```

![Google Fonts直连超时](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/143c8ac3-f9e9-46df-980b-5df92292f863.jpg)

浏览器渲染被这个 CSS 阻塞,**直连超时 15 秒 → 页面白屏**。

### 4. 走 Clash 代理 —— 当前节点也不通

```bash
curl -x http://127.0.0.1:7897 https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined
# 超时 ×3(当前节点访问 fonts CDN 持续超时)
curl -x http://127.0.0.1:7897 https://www.google.com
# HTTP:302 1.3s(其他 Google 服务正常)
```

![fonts走代理超时](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/25407a0a-b2a0-43de-b4da-62be42bdf991.jpg)

订阅规则里 `DOMAIN-SUFFIX,googleapis.com,节点选择` 已覆盖,但**当前选中的节点访问 fonts.googleapis.com 不通**——这是节点问题,不是规则缺失。

## 三、解决方案：Clash REJECT 快速失败

与其让浏览器白屏等 15 秒,不如**让字体请求立即失败**,页面秒开(代价:Material 图标字体缺失,文字/功能不受影响)。

在 Clash Verge 的 `profiles/Merge.yaml` 添加 **prepend-rules**(优先于订阅规则匹配):

```yaml
prepend-rules:
  - DOMAIN-SUFFIX,fonts.googleapis.com,REJECT
  - DOMAIN-SUFFIX,fonts.gstatic.com,REJECT
```

![Merge REJECT规则](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/54d19813-5d35-4f1f-a8cb-fe02e53aea42.jpg)

> 💡 为什么用 `prepend-rules`?Clash Verge 的 Merge 配置中,`rules` 会**替换**订阅的全部规则(危险),
> 而 `prepend-rules` 只是**追加在最前**,不影响原订阅规则。

改完重启 Clash Verge 生效(或切换 profile 触发重载)。

## 四、验证

```bash
curl -x http://127.0.0.1:7897 -w '%{time_total}s' https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined
# 000 0.75s   ← REJECT 立即失败, 浏览器不再等 15 秒
curl -x http://127.0.0.1:7897 -w '%{http_code} %{time_total}s' https://www.google.com
# 302 2.1s    ← 其他流量不受影响
```

![修复后验证](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/4eadcf84-688b-4d96-8b90-eee702bb0f45.jpg)

浏览器刷新 `/login` 秒开。

## 五、经验总结

1. **Web 应用"打开慢"先看外部资源**:`curl -w` 分解 DNS/连接/首字节耗时,再抓 HTML 看引用
2. **render-blocking 的第三方 CSS/字体是白屏元凶**:尤其 Google Fonts(国内被墙)会导致页面等 15 秒+
3. **Clash 节点问题 vs 规则问题要区分**:`googleapis.com` 规则明明存在却超时,说明是节点问题;REJECT 是"不完美但立竿见影"的兜底
4. **恢复图标字体**:切换到能访问 Google Fonts 的节点后,删掉 Merge 里两行 REJECT 规则即可
5. 更彻底的方案:自建字体镜像/反代,或用国内 CDN 的图标字体(需改前端代码,容器镜像场景不适用)
