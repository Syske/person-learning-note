# python多线程使用

#python #多线程

示例代码：

```python
from concurrent.futures import ThreadPoolExecutor

def testThread(name: str):
    print(name)


if __name__ == "__main__":

    with ThreadPoolExecutor(max_workers=5) as threadPool:
        for i in range(10):
            threadPool.submit(testThread, str(i) + ".hello")
```
