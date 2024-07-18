### 基本示例

#### 读取图片

```python
import cv2

# 读取图片
img = cv2.imread('../2pdf/page_1.png', cv2.IMREAD_GRAYSCALE)

# 显示图像
cv2.imshow('image', img)
# 没有这个窗口会直接关闭
cv2.waitKey(0)
```

`IMREAD_GRAYSCALE`表示读入灰度图片，默认参数是`IMREAD_COLOR`，表示读入一副彩色图片，忽略`alpha`通道

`v2.waitKey()`指定当前的窗口显示要持续的毫秒数，比如`cv2.waitKey(1000)`就是显示一秒，然后窗口就关闭了。比较特殊的是`cv2.waitKey(0)`，并不是显示`0`毫秒的意思，而是一直显示，直到有键盘上的按键被按下，或者鼠标点击了窗口的小叉子才关闭。`cv2.waitKey()`的默认参数就是`0`，所以对于图像展示的场景，`cv2.waitKey()`或者`cv2.waitKey(0)`是最常用的