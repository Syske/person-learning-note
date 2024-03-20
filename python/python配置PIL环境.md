
#python #pil
### 安装依赖

```shell
python3 -m pip install --upgrade Pillow
```


### 简单测试

```python
import PIL
from PIL import Image

image = Image.open("./test.jpg", mode='r')
print(f'format={image.format}, fromat_description={image.format_description}, size={image.size}')

```

