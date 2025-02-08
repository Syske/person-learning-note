以下是 `async_chat` 接口的调用实例。假设你已经按照前面的步骤部署了一个 FastAPI 服务，并且服务正在运行（例如在 `http://localhost:8000`）。

---

### **1. FastAPI 服务代码**
确保你的 FastAPI 服务代码如下：
```python
from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
import asyncio

app = FastAPI()

# 加载模型
llm = Llama(
    model_path="your_model.q4_K_M.gguf",
    n_gpu_layers=20,  # 使用 GPU 加速的层数
    n_threads=8       # CPU 线程数
)

# 定义请求体格式
class ChatRequest(BaseModel):
    messages: list[dict]
    max_tokens: int = 100
    temperature: float = 0.7

# 异步聊天接口
@app.post("/async_chat")
async def async_chat(request: ChatRequest):
    loop = asyncio.get_event_loop()
    # 异步执行模型推理
    response = await loop.run_in_executor(
        None, 
        lambda: llm.create_chat_completion(
            messages=request.messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
    )
    return {"response": response["choices"][0]["message"]["content"]}
```

---

### **2. 启动 FastAPI 服务**
在终端运行以下命令启动服务：
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

---

### **3. 调用 `async_chat` 接口**
你可以使用 `curl`、Python 脚本或其他 HTTP 客户端调用 `async_chat` 接口。

#### **使用 `curl` 调用**
```bash
curl -X POST http://localhost:8000/async_chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is the capital of France?"}
    ],
    "max_tokens": 50,
    "temperature": 0.7
  }'
```

#### **响应示例**
```json
{
  "response": "The capital of France is Paris."
}
```

---

#### **使用 Python 调用**
以下是一个 Python 脚本示例，使用 `requests` 库调用 `async_chat` 接口：
```python
import requests
import json

# 定义请求 URL 和参数
url = "http://localhost:8000/async_chat"
headers = {"Content-Type": "application/json"}
data = {
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ],
    "max_tokens": 50,
    "temperature": 0.7
}

# 发送 POST 请求
response = requests.post(url, headers=headers, data=json.dumps(data))

# 打印响应
if response.status_code == 200:
    print("Response:", response.json())
else:
    print("Error:", response.status_code, response.text)
```

#### **运行结果**
```plaintext
Response: {'response': 'The capital of France is Paris.'}
```

---

#### **使用异步 HTTP 客户端调用**
如果你需要异步调用 `async_chat` 接口，可以使用 `aiohttp` 库：
```python
import aiohttp
import asyncio
import json

async def call_async_chat():
    url = "http://localhost:8000/async_chat"
    headers = {"Content-Type": "application/json"}
    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ],
        "max_tokens": 50,
        "temperature": 0.7
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(data)) as response:
            if response.status == 200:
                result = await response.json()
                print("Response:", result)
            else:
                print("Error:", response.status, await response.text())

# 运行异步函数
asyncio.run(call_async_chat())
```

#### **运行结果**
```plaintext
Response: {'response': 'The capital of France is Paris.'}
```

---

### **4. 参数说明**
| 参数            | 说明                                                                 |
|-----------------|----------------------------------------------------------------------|
| `messages`      | 聊天消息列表，包含 `role`（`system`/`user`/`assistant`）和 `content` |
| `max_tokens`    | 生成的最大 token 数（默认 100）                                      |
| `temperature`   | 控制生成文本的随机性（0-1，默认 0.7）                                |

---

### **5. 扩展功能**
- **身份验证**：在 FastAPI 中添加 API Key 验证。
- **速率限制**：使用 `slowapi` 限制用户请求频率。
- **日志记录**：记录请求日志和性能指标。

---

通过以上方法，你可以轻松调用 `async_chat` 接口，并根据需求调整参数和实现方式。