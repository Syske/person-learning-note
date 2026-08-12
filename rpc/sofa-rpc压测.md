# SOFARPC HTTP 协议压测实战记录

> 本文档记录了使用 JMeter 对 SOFARPC `bindingType="http"` 接口进行压测的完整排查过程，包含问题定位、Arthas 诊断方法和最终解决方案，可作为后续类似任务的参考手册。

---

## 📌 目录

1. [背景与目标](#1-背景与目标)
2. [核心概念澄清](#2-核心概念澄清)
3. [完整排查过程](#3-完整排查过程)
4. [Arthas 诊断命令速查](#4-arthas-诊断命令速查)
5. [最终解决方案](#5-最终解决方案)
6. [JMeter 压测配置](#6-jmeter-压测配置)
7. [常见问题与解决方案](#7-常见问题与解决方案)
8. [总结与最佳实践](#8-总结与最佳实践)

---

## 1. 背景与目标

- **服务框架**：SOFARPC
- **协议类型**：`bindingType="http"`（注意：不是 `rest`）
- **压测工具**：Apache JMeter
- **目标接口**：`com.coolcollege.live.facade.LiveWatchDetailFacade`
- **目标方法**：`syncFeedWatchDetail`
- **核心目标**：成功发起 HTTP 调用并完成压测

---

## 2. 核心概念澄清

### 2.1 SOFARPC 三种常见协议对比

| 协议类型 (`bindingType`) | 默认端口 | 定位 | URL 格式 | 适用场景 |
| :--- | :--- | :--- | :--- | :--- |
| **`bolt`** | 12200 | SOFARPC 原生二进制协议（默认） | 不适用 HTTP 调用 | 服务间高性能内部调用 |
| **`http`** | 12300（可自定义） | 简单的基于 JSON 的 HTTP 调用通道 | `/{接口全类名}:{uniqueId}/{方法名}` | 快速测试、非核心轻量级调用 |
| **`rest`** | 8341 | 标准 RESTful API | 标准 REST 路径（如 `/api/user`） | 对外 API 网关、第三方调用 |

### 2.2 关键差异：`http` vs `rest`

- **`http` 协议**：URL 必须包含**完整的接口类名 + uniqueId + 方法名**，且必须添加 `serialize_type: json` Header。
- **`rest` 协议**：使用 JAX-RS 标准注解（`@Path`、`@POST` 等），路径更清晰，无需特殊 Header。

> ⚠️ **注意**：`http` 协议默认端口是 `12300`，但实际端口以服务端配置为准（本例中为 `12400`）。

---

## 3. 完整排查过程

### 3.1 问题现象

```bash
curl --request POST --url http://127.0.0.1:12300/... --data '...'
```

报错：
```
curl: (7) Failed connect to 127.0.0.1:12300; Connection refused
```

### 3.2 排查步骤

#### Step 1：确认服务端口

**问题**：`12300` 连接被拒绝，怀疑端口不正确。

**操作**：使用 Arthas 连接到服务进程，查找实际的 HTTP 服务端口。

```bash
# 连接 Arthas
java -jar arthas-boot.jar

# 查看所有 ServerConfig 实例
vmtool --action getInstances --className com.alipay.sofa.rpc.config.ServerConfig --limit 10
```

**发现**：实际 HTTP 端口是 **12400**，而非默认的 12300。

---

#### Step 2：确认服务注册信息

**问题**：改用 `12400` 端口后，报错：
```
RPC-02411: 未找到业务服务，服务名称：[com.coolcollege.live.facade.LiveWatchDetailFacade:v1]
```

**操作**：查看 Provider 实际注册的服务。

```bash
# 列出所有 ProviderConfig 实例
vmtool --action getInstances --className com.alipay.sofa.rpc.config.ProviderConfig --express 'instances.{#this.interfaceId + "|" + #this.uniqueId + "|" + #this.server}' --limit 10
```

**输出**：
```
@String[com.coolcollege.live.facade.LiveWatchDetailFacade|com.coolcollege.live.facade.impl.LiveWatchDetailFacadeImpl|[ServerConfig [protocol=http, port=12400, host=0.0.0.0]]],
@String[com.coolcollege.live.facade.LiveWatchDetailFacade|com.coolcollege.live.facade.impl.LiveWatchDetailFacadeImpl|[ServerConfig [protocol=bolt, port=12200, host=0.0.0.0]]],
```

**发现**：
- 服务接口：`com.coolcollege.live.facade.LiveWatchDetailFacade`
- 实际 `uniqueId`：`com.coolcollege.live.facade.impl.LiveWatchDetailFacadeImpl`（不是 `v1`）
- 该服务同时发布了 `http`（12400）和 `bolt`（12200）两种协议

---

## 4. Arthas 诊断命令速查

### 4.1 查看服务端口（ServerConfig）

```bash
# 查看所有 ServerConfig 实例
vmtool --action getInstances --className com.alipay.sofa.rpc.config.ServerConfig --limit 10

# 查看具体字段（如端口）
vmtool --action getInstances --className com.alipay.sofa.rpc.config.ServerConfig --express 'instances.{#this.port}' --limit 10
```

### 4.2 查看服务注册信息（ProviderConfig）

```bash
# 列出所有 ProviderConfig 实例（含接口名、uniqueId、协议）
vmtool --action getInstances --className com.alipay.sofa.rpc.config.ProviderConfig --express 'instances.{#this.interfaceId + "|" + #this.uniqueId + "|" + #this.server}' --limit 10

# 查找特定服务
vmtool --action getInstances --className com.alipay.sofa.rpc.config.ProviderConfig --express 'instances.{#this.interfaceId == "com.your.Interface" ? #this.uniqueId : null}' --limit 10
```

### 4.3 查看类字段信息

```bash
# 查看类的所有字段
sc -d com.alipay.sofa.rpc.config.ProviderConfig -f
```

### 4.4 常见 Arthas 错误处理

| 错误信息 | 原因 | 解决方案 |
| :--- | :--- | :--- |
| `ClassNotFoundException: ProviderConfig` | OGNL 类加载器上下文不对 | 使用 `vmtool` 替代 `ognl` |
| `NoSuchPropertyException: protocol` | 字段名不存在 | 字段可能是 `server`，通过 `server` 间接获取协议 |
| `getAllProviderConfigs()` 不存在 | SOFARPC 版本不支持 | 使用 `vmtool --action getInstances` |

---

## 5. 最终解决方案

### 5.1 正确的 curl 命令

```bash
curl --request POST \
  --url 'http://127.0.0.1:12400/com.coolcollege.live.facade.LiveWatchDetailFacade:com.coolcollege.live.facade.impl.LiveWatchDetailFacadeImpl/syncFeedWatchDetail' \
  --header 'content-type: application/json' \
  --header 'serialize_type: json' \
  --header 'user-agent: vscode-restclient' \
  --data '{
    "feedId": "1",
    "userId": "1",
    "enterpriseId": "1",
    "watchDuration": "10",
    "appId": "cool",
    "bizType": "wx_live",
    "corpId": "111"
  }'
```

### 5.2 URL 格式总结

```
http://{ip}:{port}/{接口全类名}:{uniqueId}/{方法名}
```

- **接口全类名**：`com.coolcollege.live.facade.LiveWatchDetailFacade`
- **uniqueId**：`com.coolcollege.live.facade.impl.LiveWatchDetailFacadeImpl`
- **方法名**：`syncFeedWatchDetail`

### 5.3 如何获取正确的 uniqueId

1. **查看服务启动日志**：搜索 `publish`、`provider` 等关键词。
2. **使用 Arthas**：执行 `vmtool` 查看 `ProviderConfig.uniqueId` 字段。
3. **咨询开发人员**：确认服务发布时配置的 `unique-id`。

---

## 6. JMeter 压测配置

### 6.1 HTTP Request 采样器配置

| 配置项 | 填写内容 |
| :--- | :--- |
| **协议** | `http` |
| **服务器名称或IP** | 服务 IP（如 `127.0.0.1`） |
| **端口号** | `12400`（以实际配置为准） |
| **方法** | `POST`（必须） |
| **路径** | `/com.coolcollege.live.facade.LiveWatchDetailFacade:com.coolcollege.live.facade.impl.LiveWatchDetailFacadeImpl/syncFeedWatchDetail` |
| **Body Data** | JSON 格式请求体 |

### 6.2 HTTP Header Manager 配置

| 名称 (Name) | 值 (Value) | 必填 |
| :--- | :--- | :--- |
| **Content-Type** | `application/json` | ✅ 是 |
| **serialize_type** | `json` | ✅ 是（`http` 协议必须） |

### 6.3 断言配置

建议添加 **响应断言**，检查返回结果中是否包含业务成功标识（如 `"code":0` 或 `"success":true`）。

---

## 7. 常见问题与解决方案

| 问题 | 可能原因 | 解决方案 |
| :--- | :--- | :--- |
| `Connection refused` | 端口不对或服务未启动 | 用 Arthas 确认实际端口，检查服务是否正常运行 |
| `RPC-02411: 未找到业务服务` | uniqueId 不匹配 | 用 Arthas 查看 ProviderConfig 确认正确的 uniqueId |
| `RPC-02412: 未找到业务方法` | 方法名错误或参数不匹配 | 确认方法名拼写，检查 JSON 参数结构是否匹配 |
| `serialize_type` 缺失 | http 协议未指定序列化方式 | 在 Header 中添加 `serialize_type: json` |
| 返回 400/500 错误 | 请求体格式问题 | 确认 JSON 格式合法，字段名与服务端 `@RequestBody` 匹配 |
| `NoSuchPropertyException` | Arthas 字段名拼写错误 | 先用 `sc -d 类名 -f` 确认正确的字段名 |

---

## 8. 总结与最佳实践

### 8.1 核心要点

1. **端口不一定默认**：`http` 协议默认 12300，但可自定义，务必以实际为准。
2. **uniqueId 是关键**：`http` 协议的 URL 必须包含正确的 `uniqueId`，它可能不是代码中配置的 `v1`，而是实现类名或其他值。
3. **Header 不能少**：`Content-Type: application/json` 和 `serialize_type: json` 缺一不可。
4. **必须用 POST**：`http` 协议不支持 GET 调用。

### 8.2 调试流程

```
1. 确认端口 → 2. 确认 uniqueId → 3. 确认方法名 → 4. 确认请求体格式
```

### 8.3 推荐工具

- **Arthas**：在线诊断服务端口和注册信息
- **curl**：快速测试接口连通性
- **JMeter**：正式压测

### 8.4 后续优化建议

- **统一 uniqueId**：与开发团队约定 `uniqueId` 规范（如 `v1`、`default`），便于 URL 管理。
- **增加健康检查**：在服务端增加 `/_health` 等端点，便于快速验证服务状态。
- **使用 REST 协议**：如果是对外 API，建议使用 `bindingType="rest"`，路径更清晰、更规范。

---

**文档版本**：v1.0  
**更新日期**：2026-08-11  
**适用版本**：SOFARPC 5.x、JMeter 5.x