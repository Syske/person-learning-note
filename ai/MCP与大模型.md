## 概念

### 什么是 AI 模型

AI 是人工智能（Artificial Intelligence）的缩写，指通过计算机技术模拟人类智能的技术。通过机器学习、深度学习等方法，我们可以训练出能够完成特定任务的智能体，这就是 AI 模型。

### 什么是 MCP

MCP 的全称是 **Model Context Protocol**（模型上下文协议），由 Anthropic 提出并开源。它是一套标准协议，为 AI 模型与外部工具、数据源的交互提供了统一规范。

可以把 MCP 理解为 AI 应用的 **USB-C 接口**：
- 模型是"大脑"
- MCP 是"接口规范"
- 各种工具/数据源是"外设"

通过 MCP，AI 模型可以动态发现并使用外部工具、读取资源、访问数据源，而无需为每个集成单独适配。

### MCP 的核心角色

- **MCP 服务端（Server）**：提供工具（Tools）、资源（Resources）、提示词（Prompts）等能力的服务
- **MCP 客户端（Client）**：连接 AI 模型与 MCP 服务端，转发请求与响应
- **传输层（Transport）**：支持 Stdio（子进程通信）和 SSE（HTTP 流式）两种传输方式

### MCP 解决了什么问题

在没有 MCP 之前，每个 AI 应用集成外部工具都需要定制开发，切换模型或扩展能力时重复适配成本高。

有了 MCP 之后：
- 标准化接口，一次开发多处使用
- 模型无关，切换 LLM 无需改造工具
- 动态发现能力，服务端可随时增删工具
- 安全可控，通过权限控制限制模型行为

### 对比其他协议

| 特性 | MCP | Function Calling | Plugin |
|------|-----|-----------------|--------|
| 标准化 | 开放标准 | 厂商私有 | 厂商私有 |
| 动态发现 | ✅ | ❌ | 部分 |
| 模型无关 | ✅ | ❌ | ❌ |
| 资源访问 | ✅ | ❌ | ✅ |
| 流式响应 | ✅ | ✅ | ✅ |

### 相关笔记

- [MCP 资源汇总](../mcp/MPC资源.md) — 常用 MCP 服务器列表
- [MCP 简单示例代码](../mcp/简单示例代码.md) — Python 实现 MCP 服务端示例

### 参考

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)
