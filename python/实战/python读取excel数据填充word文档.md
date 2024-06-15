### 前言

最近，有个同事说他有个朋友让有偿写个程序将`excel`数据填充`word`文档，简单沟通之后，我做了几个示例，然后接下了这个需求，首先我的思路是：
- 读取`excel`：这个比较简单，我最后用的是`pandas`
- 生成`word`文档：因为他的文档格式是确定的，所以我最开始想的是模板替换，有一种解决方案是循环`word`的所有内容，在我们需要替换的地方，填入我们的模板标记，然后循环替换，但是由于他提供的文档是个表格，所以我又换了读取`word`中的表格，并填写表格中的数据

下面，我们就这个需要分享下我们的解决方案。

### 解决方案

开始之前，我们先看下`excel`的数据结构：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240615194914.png)

生成的`word`文档格式：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240615195023.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240615195128.png)

分析`word`文档之后，发现文档内容只有表格，但是表格内部又嵌套了表格，所以解决方案就是：
1. 设置`word`中表格的数据
2. 设置`word`中表格下的表格的数据
这其中有一个难点是，选择框设置的问题，最后我讨巧直接赋值勾选后的框解决，下面我们直接看代码：

```python
	# 加载Word文档
    document = Document('模板1.docx')
    # 定位到文档中的第一个表格
    table = document.tables[0]
    # 填充用户编号，其他字段类似
    table.cell(0, 1).text = '123'
```

这里表格的嵌套表格是个难点，但是实际搜索之后，发现还好：

```python
	# 获取附件二中嵌套的表格，证件信息
    child_table1 = table.cell(6, 0).tables[0]
    # 类似的，如果要获取联系人信息，直接获取对应单元格的第二个表格即可
    child_table2 = table.cell(6, 0).tables[1]
    # 设置嵌套表格的数据
    child_table1.cell(1, 1).text = "张三"
```

另外一个点就是我前面说的勾选问题，我用了比较讨巧的方式：

```python
child_table1.cell(4, 1).text = '☑'
```

还有一个注意的点是，`pandas`读取到的空数据，对应的值其实是`nan`，所以在空判断的时候要注意：

```python
if str(row['身份证']) != 'nan':
        child_table.cell(5, 3).text = str(row['身份证'])
```

#### pandas使用技巧

##### 数据的头名称替换

在通过`pandas`读取数据的时候，默认第一行为表头数据，如果表头数据为空，或者表头数据为多个单元格合并而成（除了第一个被合并的列），那么对应列的头就会变成`Unnamed: 数字`，这里的数字对应的就是索引，比如第一列的索引就是`0`，所以如果第一列没有头信息或者头信息为空，最终拿到的头信息就是`Unnamed: 0`，其他列依次类推

在实际做数据处理的时候，我们为了更好得核对数据，我们可以替换头信息，具体方式如下：
```python
df = pd.read_excel(f'{fileName}', sheet_name='Sheet1')
df = df.rename(columns={
    '非居民客户': '营业执照',
    'Unnamed: 8': '事业单位法人证书',
    'Unnamed: 9': '统一社会信用代码证',
    'Unnamed: 10': '税务登记证',
    'Unnamed: 11': '身份证'
})
```

##### 遍历数据

```python
# 舍弃前两行数据
df = df.iloc[2:]
# 循环遍历
for index, row in df.iterrows():
	print(row) 
```
其中`row`的数据类似是`'pandas.core.series.Series`，可以以类似字典的数据方式访问：
```python
# 获取身份证信息
id_num = row['身份证']
```

#### pyqt技巧

##### 选择文件并获取文件路径

```python
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建按钮来选择文件并解析内容
        self.choose_button = QPushButton('选择并解析文件', self)
        self.choose_button.clicked.connect(self.chooseAndParseFile)

        # 创建文本编辑框来显示文件内容
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.choose_button)
        layout.addWidget(self.text_edit)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle('文件解析器')
        self.show()

    def chooseAndParseFile(self):
        # 打开文件选择对话框
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*);;Text Files (*.txt);;CSV Files (*.csv)", options=options)

        # 如果用户选择了文件，则解析并显示内容
        if fileName:
            try:
                # 使用pandas读取文件内容（这里假设是CSV格式）
                print(fileName)
                # 业务操作
                # read_excel(fileName)
                QMessageBox.information(self, "提示", "执行完成！")
            except Exception as e:
                # 如果解析出错，显示错误消息
                self.text_edit.setText(str(e))
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
```

### 结语

好了，到这里，整个需求就结束了，只是为了让客户操作更便捷，这里我把`python`脚本打成`exe`文件了，具体参考 [pyqt5](../python图形GUI——Qt5.md)