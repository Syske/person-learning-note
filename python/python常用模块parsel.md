#python #html

`parsel`是一个流行的`html`解析库，可以用于解析`html`的内容
- [官方地址](https://pypi.org/project/parsel/)
- [文档地址](https://parsel.readthedocs.io/en/latest/usage.html)
### 基本示例

```python
import parsel
import requests


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53'
    }

url = f'https://baidu.com' 

response = requests.get(url=url, headers=headers)
# 将html内容传入parsel.Selector，然后就可以像前端jquery的选择器一样，操作html了
selector_1 = parsel.Selector(response.text)
# 解析页面的标题：
title = selector_1.css('head > title::text').get() 
# 结果:百度一下，你就知道
print(title)
```

对应的html内容大致如下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240514103932.png)