由于工作性质，加之个人喜好，我在日常工作中用到的`AI`工具主要是`CLI`类，下面就把我使用`AI`工具的一些经验和大家分享下，主要涉及如下内容：
- MCP组件配置
- 指令/技能（skill）
- 提示词
## MCP


## 指令/技能（skill）


## 提示词

根据角色划分，提示词主要分两类：
- 系统角色提示词：稳定、全局、长期有效的行为约束，推荐长度：**200～800 tokens**（最好 <500）
- 用户角色提示词：单次任务 / 意图 / 输入数据，推荐长度：尽量 < 2000 tokens

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/3bb93a06-41b8-4bbc-a019-da5329aea376.jpg)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/de8cd2bb-b5e1-4f8f-9a49-c164e41e3add.jpg)



## 个人体验

我用的比较多的`CLI`是`iflow-cli`和`codex-cli`，聊天`AI`主要是`Deepseek`和`chatgpt`，从个人体验方面来说（主要是编程技术相关），国内的`AI`和国外的`AI`工具还是存在不小的差异，差异点主要集中在下面几点：

### 输出质量
针对具体技术问题的方案，同样的提示词，特别是在用户提交的内容中存在错误时，`chatgpt`给出的方案更好，答案更准确，会指出错误，但是`deekseek`会顺着用户的错误给出方案，关于这一块，`iflow-cli`也存在同样的问题，我被坑过两次，都是到了自测阶段，发现实现方案行不通，以我最近一次关于`sofa-rpc`线程池`SERVER_BUSY`异常优化为例：
#### deepseek

没有指出我的错误，而且还信誓旦旦给出了推荐方案：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/875a7a6d-32bd-4981-8be4-ffc39a0edf34.jpg)

#### chatgpt

直接指出了方案的核心问题：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/fe381c5f-7b92-4e41-8ca5-1cda176994dd.jpg)

当然，我并不是捧一踩一，事实上，我在使用`codex-cli`的过程中，也出现过输出内容丢失的情况，我只是想从个人经验角度给出大家一些启示——使用`AI`工具要有自己的判断，同时不要过分相信单一`AI`工具给出的答案，特别是你自己无法判断答案是否准确时。

但是，不可否认的是，在编程领域，`chatgpt`和`codex-cli`给出的答案更准确，方案也更简洁。

### 交互体验

### 响应速度
`chatgpt`和`codex-cli`响应速度更快；`deepseek`和`iflow-cli`表现相对较差。


