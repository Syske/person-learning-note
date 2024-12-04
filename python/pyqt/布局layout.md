#### 垂直布局

```python
# 创建布局用于放置单选框
radio_layout = QVBoxLayout()

# 创建单选框
radio1 = QRadioButton('radio1')
radio2 = QRadioButton('radio2')

# 将单选框添加到布局中
radio_layout.addWidget(radio1)
radio_layout.addWidget(radio2)
```

效果预览

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240620160704.png)

#### 水平布局

```python
# 创建布局用于放置单选框
radio_layout = QHBoxLayout()

# 创建单选框
radio1 = QRadioButton('radio1')
radio2 = QRadioButton('radio2')

# 将单选框添加到布局中
radio_layout.addWidget(radio1)
radio_layout.addWidget(radio2)
```

效果预览
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240620160937.png)


#### 多个布局嵌套

```python
# 创建垂直布局：主布局
main_layout = QVBoxLayout()

# 创建布局用于放置单选框
radio_layout = QHBoxLayout()
# 创建单选框
radio1 = QRadioButton('radio1')
radio2 = QRadioButton('radio2')

# 设置单选框的互斥性（即一次只能选择一个）
radio1.setChecked(True)  # 默认选中选项1

# 将单选框添加到布局中
radio_layout.addWidget(radio1)
radio_layout.addWidget(radio2)

# 垂直布局
input_layout = QVBoxLayout()
label = QLabel('ID:')
input_layout.addWidget(label)
 # 创建数字输入框
lineEdit = QLineEdit(self)
input_layout.addWidget(lineEdit)

main_layout.addLayout(input_layout)
main_layout.addLayout(radio_layout)
```


效果预览
垂直布局 + 水平布局 放入父级布局中（垂直布局）
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240620161424.png)


#### 格栅布局

```python
grid_layout = QGridLayout()
names = ['格子1', '格子2', '格子3', '格子4', '格子5', '格子6', '格子7', '格子8', '格子9']
for i in range(3):
	for j in range(3):
		index = i * 3 + j
		button = QPushButton(names[index])  # 也可以使用QLabel显示图片
		button.setFixedWidth(100)
		button.setFixedHeight(100)
		grid_layout.addWidget(button, i, j)
# 设置窗口的布局
self.setLayout(grid_layout)
```

效果预览
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240620162312.png)


#### 表单布局

```python
# 创建垂直布局
main_layout = QFormLayout()

lineEdit = QLineEdit(self)
label = QLabel('account:')
main_layout.addRow(label, lineEdit)

lineEdit1 = QLineEdit(self)
label1 = QLabel('passwd:')
main_layout.addRow(label1, lineEdit1)        # 创建垂直布局
main_layout = QFormLayout()

lineEdit = QLineEdit(self)
label = QLabel('account:')
main_layout.addRow(label, lineEdit)

lineEdit1 = QLineEdit(self)
label1 = QLabel('passwd:')
main_layout.addRow(label1, lineEdit1)
```

预览效果
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240620163334.png)