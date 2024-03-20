#python #fastApi
### 安装依赖

```sh
# 核心依赖
 pip install fastapi

# 安装 uvicorn
 pip install "uvicorn[standard]"
```



### 编写demo

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def index():
    """
    注册一个根路径
    :return:
    """
    return {"message": "Hello World"}


@app.get("/info")
async def info():
    """
    项目信息
    :return:
    """
    return {
        "app_name": "FastAPI框架学习",
        "app_version": "v0.0.1"
    }
```

### 运行

```sh
 uvicorn fast-api-test:app --reload
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240204180926.png)