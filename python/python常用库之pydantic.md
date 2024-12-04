
### 简介

`pydantic`是一个可以快速将字典数据转换为`python`对象的库。

### 使用指南

#### 要点

##### 必须要继承`BaseModel`

``` python
from pydantic import BaseModel

class AliyunPicUploader(BaseModel):
    bucket_name: str
    endpoint: str
    access_key: str
    secret_key: str
    region: str
    path: str
```


##### 传入字典数据时要指定为可变参数

也就是入参中的`**`必不可少，否则会报错
```python
config = {'endpoint': '111111', 'bucket_name': '11111', 'access_key': '1111', 'secret_key': '11111', 'region': 'cn-hangzhou', 'path': 'imgs'}

uploader = AliyunPicUploader(
        **config
    )
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/ae152a05-7df6-48e3-bfb8-0e215424fd5c.jpg)