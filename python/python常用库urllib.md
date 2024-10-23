#python #网络

`urllib`库用于操作网页 URL，并对网页的内容进行抓取处理。
是`python`标准库自带的，不需要额外安装，与三方库`requests`类似，只是使用上前者更繁琐
### 简单示例

```python
import urllib
req =urllib.request.urlopen(url='http://www.baidu.com')
# 读取网页内容
req.read()
```



1. [参考文档](https://www.runoob.com/python3/python-urllib.htmlhttps://www.runoob.com/python3/python-urllib.html)