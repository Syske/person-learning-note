# pi Stream ended without finish_reason 排查记录

> 2026-08-20 · 环境：Windows · pi Coding Agent `0.84.2`
> 本次为**运行核查记录**（确认是否需要调整配置 → 结论：不需要），非故障处理。

## 现象

pi 会话工作过程中（大量工具调用 + web 搜索后）偶发报错：

```
Error: Stream ended without finish_reason
```

报错后任务**持续推进**（读取、发布 wiki、上传附件、替换链接等全部完成），
属**偶发可自愈**，未中断任何工作。

## 环境

| 项 | 值 |
|---|---|
| pi 版本 | `0.84.2`（当前最新，registry 一致） |
| PI_PROVIDER | `opencode-go`（OpenCode Go 内置 provider） |
| PI_MODEL | `deepseek-v4-flash` |
| provider baseUrl | `https://opencode.ai/zen/go/v1`，`api=openai-completions` |

## 错误本质

`Stream ended without finish_reason` 是 **pi 的 OpenAI 兼容流式解析层**报出的错误：
当模型服务端在**流结束或工具调用结束时未发送 `finish_reason` 标记**，pi 会认为
"流意外中断"。这是 pi 的**已知 issue**（earendil-works/pi#6226、#7062、#4345、
#4675 等），常见触发场景正是在**工具调用之后**（web_search / 工具返回后）。

pi 官方已确认部分厂商 OpenAI 兼容接口会省略该字段，并为此提供兼容配置
`compat.supportsFinishReason`。

## 核查结论：不需要调整配置

1. **pi 已是最新版本 `0.84.2`**，官方 CHANGELOG 已将「对省略 `finish_reason` 的
   兼容流自动推断 stop/toolUse」合入主线。本次会话已具备该推断能力，错误可自愈。
2. opencode-go 是**内置目录 provider**，其 `compat` 由内置模型目录持有；用户级
   `settings.json`（`~/.pi/agent/settings.json`）当前**无 provider 覆盖块**（也不需要）。
3. 本次实际运行中，错误出现后任务持续推进，属偶发噪音，未中断任何工作。

## 何时才需要动配置（当前不触发）

仅当观察到以下任一情况，才考虑为 `opencode-go` 覆盖 `compat.supportsFinishReason: false`
（让 pi 在流结束时自动推断 stop/toolUse，而非报错），或升级/provider 调整：

- 该错误**频繁出现且导致任务实际中断/失败**（非偶发自愈）；
- 需要**消除每条报错日志**（而非仅保证能完成工作）。

两者当前均不满足 → **保持配置不变**。

### 配置方法（如需使用）

在 provider 配置块的 `compat` 下（pi docs/models.md）：

```jsonc
{
  "providers": {
    "opencode-go": {
      "api": "openai-completions",
      "compat": {
        "supportsFinishReason": false
      }
    }
  }
}
```

参考：pi 官方文档 `docs/models.md` 中 `compat.supportsFinishReason` 字段定义——
"Whether streamed responses include `finish_reason`. When `false`, pi infers `stop`
or `toolUse` when the stream ends. Default: `true`."

## 相关已知坑（排查线索）

- `maxTokens` 若设得过大/未与模型 context window 对齐，可能在硬上限处截断开而
  表现为该类错误（issue #4675）。如自定义了很大的 max_tokens，建议校验。
- pi 的部分重试机制按错误字符串匹配；个别供应商错误串未匹配时不会自动重试
  （issue #4433，Anthropic 场景），需关注是否真正中断。

## 本次结论一句话

pi 已是最新版本且具备 finish_reason 兼容推断能力，该错误为 opencode-go 端点
省略字段所致的偶发自愈噪音，**无需调整配置**；仅在频繁中断或需消除报错时才按上述
方法覆盖 `compat.supportsFinishReason: false`。
