# pi 请求超时排查记录

> 2026-08-18 · 环境：Arch Linux（笔记本 WiFi，`wlo1`），移动宽带 + 光猫拨号 + TP-Link TL-WDR7661 二级路由

## 最终结论

根因是本机/网络**没有全局 IPv6**。最终通过**路由器后台开启 IPv6**（移动光猫拨号，路由器 IPv6 选 Native/DHCPv6）解决，本机拿到 `2409:`（移动）全局 IPv6 地址后，pi 恢复正常，不再需要任何 workaround。

## 现象

使用 `pi`（Pi Coding Agent，v0.81.0）发起 LLM 请求时，约 20 秒后报 `Request timed out.`。
默认 provider 为 `opencode-go`（baseUrl：`https://opencode.ai/zen/go/v1`，模型 `deepseek-v4-flash`）。

## 排查过程

### 1. 区分"服务端慢"还是"客户端连不上"

- `curl` 直接请求 OpenAI 兼容接口：`HTTP 200`，约 1~4s，**一直正常**。
- `pi` 请求：**必现超时**。
- `node fetch` 请求同一域名：**必现 `ETIMEDOUT`**。

结论：后端服务健康，问题在 **Node 客户端的网络连接**。

### 2. 缩小到 DNS / IPv6

- `opencode.ai`（Cloudflare CDN）同时解析出 IPv4 + IPv6（anycast 地址）。
- 本机只有 `fe80::` link-local IPv6，**没有全局 IPv6，无法路由 IPv6**。
- `curl -6` 立即失败（`Could not connect`）；`curl -4` 正常。
- `node net.connect` 按 IP 直连 IPv4：成功；但 `node tls.connect` 按主机名连接：`ETIMEDOUT`（约 1s，尝试了全部 IPv4/IPv6 地址）。

### 3. 定位 Node 侧的具体原因

Node 22 默认开启 happy-eyeballs（`autoSelectFamily`），会**按 250ms 间隔交错尝试所有解析出的地址**。IPv6 地址立即 `ENETUNREACH`，而 IPv4 的 TLS 握手在此网络下较慢（实测约 2s），在握手完成前就被当作失败放弃，最终整体报 `ETIMEDOUT`。

关键对比：

| 方式 | 结果 |
| --- | --- |
| `curl`（自带 happy-eyeballs，IPv4 优先） | 正常 |
| `openssl s_client` | 正常 |
| `node tls.connect` 直连 IPv4 地址 | 正常（约 2s） |
| `node tls.connect` 按主机名 | `ETIMEDOUT` |
| `node fetch` | `ETIMEDOUT` |

## 根因

本机无全局 IPv6 + 目标域名（Cloudflare）同时返回 IPv4/IPv6 + Node happy-eyeballs 会放弃"慢但可用"的 IPv4 TLS 连接，导致 Node 系工具（pi）对该域名请求超时；而 curl/openssl 不受影响。

## 解决方案

### 治标（workaround，IPv6 无法获取时用）

强制 Node 只用 IPv4 并关闭自动多地址重试：

```js
// /home/syske/.pi/ipv4-fix.cjs
const dns = require('dns');
const net = require('net');
try { net.setDefaultAutoSelectFamily(false); } catch {}
dns.setDefaultResultOrder('ipv4first');
```

在 shell 配置中注入（`~/.bashrc`）：

```sh
export NODE_OPTIONS="-r /home/syske/.pi/ipv4-fix.cjs"
```

> 需重开终端或 `source ~/.bashrc` 后生效。
> IPv6 恢复正常后该 workaround 可移除（留着也无害）。

### 治本（推荐）：路由器开启 IPv6

1. 登录路由器后台（本机网关 `192.168.0.1`，TL-WDR7661 千兆版）
2. **路由设置 → IPv6**，打开开关
3. **上网方式按宽带拓扑选**：
   - 光猫拨号、路由器自动获取 → **Native / 动态 IP（DHCPv6）** ← 本例（移动光猫拨号）
   - 路由器 PPPoE 拨号 → **PPPoE**
4. 保存重启，等 30 秒后本机验证：
   ```sh
   ip -6 addr show wlo1     # 应出现 2409:(移动)/240e:(电信)/2408:(联通) 开头全局地址
   ip -6 route show         # 应出现 default via fe80::... 路由
   ping -6 www.baidu.com    # 通即生效
   ```
5. 若路由器开了仍拿不到 → 进光猫后台（一般 `192.168.1.1`）检查 WAN 侧 IPv6 已启用、LAN 侧 RA/DHCPv6 下发；仍不行则把光猫改**桥接**、路由器 PPPoE 拨号。

## 验证

```sh
# 修复前
pi --print -nt "reply exactly with: OK"   # Request timed out.

# workaround 验证
NODE_OPTIONS="-r /home/syske/.pi/ipv4-fix.cjs" pi --print -nt "reply exactly with: OK"   # OK

# 治本后（路由器开 IPv6，无需任何环境变量）
pi --print -nt "reply exactly with: OK"   # OK
```

## 经验总结

1. **排超时先区分端侧**：`curl` 通不代表应用能通，同一域名要分别验证 `curl` / `node fetch` / SDK 三种客户端。
2. **Node 的 happy-eyeballs 有坑**：无 IPv6 环境下，Node 对同时有 A/AAAA 记录的域名（尤其 Cloudflare anycast）可能因 IPv6 快速失败而拖垮慢速 IPv4 连接。排查时用 `tls.connect` 按主机名 vs 按 IP 直连做对照即可复现。
3. **快速判定本机 IPv6 是否可用**：`ip -6 addr show` 看是否有全局地址（`fe80::` 是 link-local，不可路由）；`curl -6 https://example.com` 看是否通。
4. **通用兜底方案**：无 IPv6 的网络可全局给 Node 加 `NODE_OPTIONS="--dns-result-order=ipv4first"`；若仍超时再叠加关闭 `autoSelectFamily` 的 preload。
5. 顺带发现：`--provider deepseek`（DeepSeek 官方 API 直连）返回 `402 Insufficient Balance`——账户余额不足与超时是两回事，注意区分。pi 的默认 provider 走的是 opencode.ai 的 `opencode-go` 代理，并非 DeepSeek 官方直连。

---

## 附：deepseek-v4 thinking 参数实测（2026-08-18 补充）

### 背景

社区流传通过 system prompt（如 `thought in ENGLISH, start with "We need..."`）能改变 DeepSeek 思考链。实测验证。

### 测试环境

- 模型：`deepseek-v4-flash`（经 opencode-go 网关 `https://opencode.ai/zen/go/v1`）
- 网关不暴露思考链：无论怎么传参数，`reasoning_content` 均为 `null`/空（流式时字段出现 61 次但全是 null）

### 测试矩阵

| 测试 | 结果 |
|------|------|
| 非流式 + 默认 | `reasoning_content` 字段存在但为空 |
| 非流式 + `thinking:true` | 思考链仍为空，回答 2172 字符 |
| 非流式 + `thinking:false` | 思考链为空，回答 2075 字符 |
| 流式 + `thinking:true` | `reasoning_content` 出现 61 次但全 null |
| 陷阱题 9.11 vs 9.8 + `thinking:false` | ✅ 答对（当小数比较，百分位 1>0） |
| 陷阱题 9.11 vs 9.8 + `thinking:true` | ❌ 两次都错/自相矛盾（把 9.11 当版本号或结论与推理矛盾） |

### 结论

1. **opencode-go 网关不返回思考链**——`reasoning_content` 永远是 null，拿不到 DeepSeek 思考过程，这是网关层限制，不是模型不支持。
2. **`thinking` 参数在该网关下没有质量增益**，陷阱题上甚至更不稳定（两次都错）。
3. **提示词影响的是输出语言/风格**（英文开头、行动式表达），不是思考链开关。真正的 thinking 是模型请求参数，且取决于网关是否透传。
4. **pi 的 models-store.json 配置**：已把 `opencode-go/deepseek-v4-flash` 的 `reasoning` 从 `true` 改为 `false`（避免网关层进入不稳定的处理路径）。其他模型未动。

### 操作记录

```bash
# 备份 + 修改默认模型的 reasoning 配置
cp ~/.pi/agent/models-store.json ~/.pi/agent/models-store.json.bak-$(date +%Y%m%d)
# 编辑: opencode-go → deepseek-v4-flash → reasoning: false
# 重启 pi 生效
```
