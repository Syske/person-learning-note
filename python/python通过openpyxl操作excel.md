## Python操作Excel

### 缘由

故事要从一个统计表格说起😂，我手里有个项目，每个月28号需要提供各个接口的访问次数的统计数据，之前都是通过`sql`统计查询，然后汇总成`excel`。因为我比较懒，老想走捷径，喜欢折腾，同时也想着能不能通过`python`做点啥，正好这个假期又从头学了一次`python`，所以就想实践下。

我先查了`python`使用`Oracle`数据库的资料，发现很简单，然后开始尝试配置环境，安装库文件，折腾了好久，终于一切都顺利了，然后又去查了执行`sql`、获取结果集，一切都是很顺其自然的发生。然后我又有了新的想法，我在床上查询了`python`操作`Excel`的相关资料，紧接着今天起床后开始实践、实验、查资料，最后完美达到结果，当然最大的守护是对`python`有了新的认知和理解，我能深切体会到她会在以后的工作和生活中，成为我的有一个新的得力助手，让我前进，这简直完美，也让人觉得内心愉悦。

为啥学`python`老是没坚持学完，没有什么结果，主要是没搞清楚，没用明白，当然也是因为没有真正实践去做项目，经常练的都是一些基本的简单操作。今天之前，准确的说应该是搞这个项目之前，我对`python`都是由偏见的，最不喜欢的就是他的缩进，但是通过此次项目，我明显感觉到自己对`python`有了新的认知和见解，忽然觉得豁然开朗了，这种感觉很神奇，就像顿悟一样。和当时学java的时候很像，前前后后自学了很多，但一直是从自学到放弃，一直在门外徘徊，直达后来，我试着去多写，多实验，多琢磨，尽可能把课后的代码示例都敲一遍，时间久了，忽然有一天就和今天的感觉一样，我觉得自己入门了。

我对入门的定义是会用，能够用一种语言来完成一些工作，做一些小东西，今天我就是做到了，从有想法，到搜索资料，到实验，通过不断地尝试和查询资料，我做到了，我也收获了。

### 准备工作

#### 安装openpyxl

##### pip安装

```sh
pip install openpyxl
```

##### 离线安装

下载网址：

```
https://www.lfd.uci.edu/~gohlke/pythonlibs/
```

下载如下文件：

```
et_xmlfile-1.0.1-py2.py3-none-any.whl
jdcal-1.4-py2.py3-none-any.whl
openpyxl-2.6.0-py2.py3-none-any.whl
```

将上述三个文件拷贝到`python`安装目录中的`scripts`文件夹下，并通过一下方式安装：

```
pip install 文件名
```

完成以上工作，我们就可以开始写脚本了

### 

### 引入包资源

```python
from openpyxl import Workbook
或者
import openpyxl
```

两种方式的区别就是，下面的这种方式需要在调用方法的时候加上`openpyxl.`，后面还会提到

### 创建工作表

如果是第一种引包的方式，写法是这样的：

```python
# 创建一个Workbook对象
wb = Workbook()
```

如果是第二种则是这样的：

```python
wb = openpyxl.Workbook()
```

后面就不再说明了，默认用第一种方式

### 操作sheet

#### 创建sheet

```python
# 创建一个Sheet对象
ws1 = wb.create_sheet(index=0, title="Mysheet")
或者
ws2 = wb.create_sheet("Mysheet", 0) 
或者
ws3 = wb.create_sheet("Mysheet")  
```

- `index`指的是`sheet`的位置，0表示第一个，如果省略的话，默认是在已有的`sheet`后面进行追加
- `title`就是`sheet`的名字

**注意：**需要注意的是`sheet`的名字如果是中文的话，必须是`Unicode`编码

```python
ws2.title = (u"你好")    #设定一个sheet的名字 必须是Unicode
```

#### 获取sheet

##### 获取活动的sheet

```python
# 获取活动的sheet
activeSheet = wb.active
```

##### 根据名字获取sheet

```python
#获取某个sheet对象
print (wb.get_sheet_by_name(u"你好"  ))
```

##### 获取所有sheet

```python
#获取全部sheet 的名字，遍历sheet名字
print (wb.sheetnames)
for sheet_name in wb.sheetnames:
    print (sheet_name)
# 遍历wb中的sheet
for sheet in wb:
    print (sheet.title)
```

##### 编辑sheet标签背景颜色

```python
# 设置活动表颜色
activeSheet.sheet_properties.tabColor = "205EB2"
#设定sheet的标签的背景颜色
ws1.sheet_properties.tabColor = "1072BA"   
```

#### 复制sheet

```python
#复制一个sheet
wb["New Title" ]["A1"]="zeke"
source = wb["New Title" ]
target = wb.copy_worksheet(source)
```

#### 单元格操作

##### 读取数据

```python
print(mySheet['B4'].value)
```

##### 赋值

下面这几种操作方式，本质上一样

```python
mySheet['B4'].value = 'hello world'
或者
wb["New Title" ]["A1"]="zeke"
或者
tableNameCell = activeSheet.cell(row = 1, column = 1, value = 'hello')
```

##### 单元格合并

```python
mySheet.merge_cells('a1:d1')
```

上面的操作就是合并`a1`到`d1`之间的单元格

##### 设置行高

```python
mySheet.row_dimensions[1].height = 55
```

##### 设置列宽

```python
# 设置列宽度
mySheet.column_dimensions['A'].width = 36
```

##### 单元格求和

```python
sum = 0
for cellssss in mySheet['B4:B20']:
    for cell in cellssss:
        co = cell.value
        if not co is None:
            sum = sum + cell.value
print("求和结果：", sum)
```

这里我写了一个方法，用于单元格求和：

```python
# 求和    
# cells 取值为sheet的切片，如：mySheet['B4:B20']
def sum(cells):    
    sum = 0
    for cellssss in cells:
        for cell in cellssss:
            co = cell.value
            if not co is None:
                sum = sum + cell.value
    print("求和结果：", sum)
    return sum
```

##### 批量操作单元格

比如操作`A3-D3`,`A7-D7`,`A14-D14`,`A18-D18`这些区域的单元格，我的解决方法如下：

```python
# 背景填充
for i in [3, 7, 10, 14, 18]:
    for cells in mySheet['A'+ str(i) +':D' + str(i)]:
        for cell in cells:
            cell.fill = fill
```

如果是操作某一范围内的单元格，这样这样操作，其实上面求和就是这么操作的：

```python
for cells in mySheet['D3:D21']:
    for cell in cells:
        valueC = mySheet['C' + str(cell.row)].value
        valueB = mySheet['B' + str(cell.row)].value
# 或者这样
# 获取单元格切片
cellsA = mySheet['B3:D21']
# 设置表格样式
for cellssss in cellsA:
    for cell in cellssss:
        cell.style = dataCellStyle
```

上面的操作其实大同小异，基本上都一样。需要提到的是

- `cell.row`获取到的是单元格的行号，比如`A20`，获取到的是`20`
- `cell.column_letter`获取到的是单元格的列，即字母，比如`B20`获取到的是`B`
- `cell.col_idex`获取到的是当前单元格列字母对应的序号，比如`A2`对应的是`1`，`E3`对应的是`5`,`Z4`对应的是`26`,`AA4`对应的是`27`，以此类推

#### 单元格样式操作

这里的内容就比较多了，因为sheet中表格的样式比较多，涉及到单元格合并、背景设置、字体设置、边框设置、尺寸设置等，所以内容也会比较多。

##### 引入包

```python
from openpyxl.styles import colors
from openpyxl.styles import NamedStyle,Alignment,Side,Border,Font,Color,PatternFill
```

其中，`NamedStyle`是其他所有样式的载体；`Alignment`是文本对齐样式（垂直/水平）；`Side`是边框样式，线条宽度，颜色，线条虚实等；`Border`是单元格边框样式，上、下、左、右等；`Font`是字体样式，包括字体、大小、颜色等；`PatternFill`是填充样式，包括填充颜色、填充样式等

##### 创建样式

指定样式名称，创建样式

```python
classopenpyxl.styles.named_styles.NamedStyle(name='Normal', font=<openpyxl.styles.fonts.Font object> Parameters: name=None, charset=None, family=None, b=False, i=False, strike=None, outline=None, shadow=None, condense=None, color=None, extend=None, sz=None, u=None, vertAlign=None, scheme=None, fill=<openpyxl.styles.fills.PatternFill object> Parameters: patternType=None, fgColor=<openpyxl.styles.colors.Color object> Parameters: rgb='00000000', indexed=None, auto=None, theme=None, tint=0.0, type='rgb', bgColor=<openpyxl.styles.colors.Color object> Parameters: rgb='00000000', indexed=None, auto=None, theme=None, tint=0.0, type='rgb', border=<openpyxl.styles.borders.Border object> Parameters: outline=True, diagonalUp=False, diagonalDown=False, start=None, end=None, left=<openpyxl.styles.borders.Side object> Parameters: style=None, color=None, right=<openpyxl.styles.borders.Side object> Parameters: style=None, color=None, top=<openpyxl.styles.borders.Side object> Parameters: style=None, color=None, bottom=<openpyxl.styles.borders.Side object> Parameters: style=None, color=None, diagonal=<openpyxl.styles.borders.Side object> Parameters: style=None, color=None, vertical=None, horizontal=None, alignment=<openpyxl.styles.alignment.Alignment object> Parameters: horizontal=None, vertical=None, textRotation=0, wrapText=None, shrinkToFit=None, indent=0.0, relativeIndent=0.0, justifyLastLine=None, readingOrder=0.0, number_format=None, protection=<openpyxl.styles.protection.Protection object> Parameters: locked=True, hidden=False, builtinId=None, hidden=False, xfId=None)
```

示例：

```python
headerCellStyle = NamedStyle(name = 'headerCellStyle')
```

##### 创建文本对齐样式

```python
classopenpyxl.styles.alignment.Alignment(horizontal=None, vertical=None, textRotation=0, wrapText=None, shrinkToFit=None, indent=0, relativeIndent=0, justifyLastLine=None, readingOrder=0, text_rotation=None, wrap_text=None, shrink_to_fit=None, mergeCell=None)
```

示例：

```python
# 水平垂直居中
headerCellStyle.alignment = Alignment(horizontal = 'center', vertical = 'center') 
```

`horizontal`表示水平对齐方式，`vertical`表示垂直对齐方式，取值有`center`、`left`、`right`

##### 创建线框样式

这个样式是给单元格样式准备的，不是直接赋给`headerCellStyle`的，它的归属关系是：`openpyxl.styles.borders.Side`

```python
classopenpyxl.styles.borders.Side(style=None, color=None, border_style=None)
```

示例：

```python
# 线框样式
border = Side(border_style = 'thin', color = '000000') 
```

`border_style`取值范围如下：

```python
'slantDashDot', 
'medium', 
'hair', 
'mediumDashDotDot', 
'dashed', 
'dotted', 
'thick', 
'double', 
'dashDotDot', 
'thin', 
'mediumDashDot', 
'mediumDashed', 
'dashDot'
```

`color`取值是十六进制颜色

##### 创建单元格边框样式

设置单元格上下左右的边框样式，包信息：`openpyxl.styles.borders.Border`

```python
classopenpyxl.styles.borders.Border(left=<openpyxl.styles.borders.Side object> Parameters: style=None, color=None, right=<openpyxl.styles.borders.Side object> Parameters: style=None, color=None, top=<openpyxl.styles.borders.Side object> Parameters: style=None, color=None, bottom=<openpyxl.styles.borders.Side object> Parameters: style=None, color=None, diagonal=<openpyxl.styles.borders.Side object> Parameters: style=None, color=None, diagonal_direction=None, vertical=None, horizontal=None, diagonalUp=False, diagonalDown=False, outline=True, start=None, end=None)
```

示例：

```python
# 设置单元格边框样式
headerCellStyle.border = Border(left = border, top = border, right = border, bottom = border) 
```

`left`,`right`,`top`,`bottom`的取值，来源于我们前面定义的线框样式（`Side`）

##### 创建字体样式

```python
classopenpyxl.styles.fonts.Font(name=None, sz=None, b=None, i=None, charset=None, u=None, strike=None, color=None, scheme=None, family=None, size=None, bold=None, italic=None, strikethrough=None, underline=None, vertAlign=None, outline=None, shadow=None, condense=None, extend=None)
```

示例：

```python
# 大标题字体
    nameFont = Font(
    name = '等线',
    size = 16,
    bold = True,
    italic = False,
    vertAlign = None,
    underline = 'none',
    strike = False
    )
```

字体的相关属性都很简单，`vertAlign`是水平对齐，`strike`表示删除线

##### 创建填充样式

```python
classopenpyxl.styles.fills.PatternFill(patternType=None, fgColor=<openpyxl.styles.colors.Color object> Parameters: rgb='00000000', indexed=None, auto=None, theme=None, tint=0.0, type='rgb', bgColor=<openpyxl.styles.colors.Color object> Parameters: rgb='00000000', indexed=None, auto=None, theme=None, tint=0.0, type='rgb', fill_type=None, start_color=None, end_color=None)
```

示例：

```python
fill = PatternFill("solid", fgColor="E2EFDA")
```

**注意：**以上样式都可以通过如下方式直接赋值给单元格，比如：

```
cell.fill = fill
cell.font = normalfont
```

如果是单个样式，通过如上方式直接赋值给单元格即可，如果样式比较多，我个人觉是通过创建`NamedStyle`的方式比较合理。

```python
tableNameCell.style = tableNameStyle
```

其他样式目前没有用到，这里不介绍了，有需要的小伙伴可以去看文档：http://yumos.gitee.io/openpyxl3.0/index.html#document-styles

这里放一个比较完整的样式：

```python
    # 字体样式
    normalfont = Font(name = '等线',
    size = 11,
    italic = False,
    vertAlign = None,
    underline = 'none',
    strike = False
    )
    # 填充样式
    fill = PatternFill("solid", fgColor="E2EFDA")

    # 创建单元格样式对象
    headerCellStyle = NamedStyle(name = 'headerCellStyle')
    # 水平垂直居中
    headerCellStyle.alignment = Alignment(horizontal = 'center', vertical = 'center')  
    # 线框样式
    border = Side(border_style = 'thin', color = '000000') 
    # 设置单元格边框样式
    headerCellStyle.border = Border(left = border, top = border, right = border, bottom = border) 
    headerCellStyle.font = normalfont
    # 填充样式
    titleStyle.fill = fill
```

#### 保存数据

```python
# 保存数据
wb.save("python-first-excel.xlsx")
# 关闭工作表
wb.close()
```

好了，本次探讨到这里就结束了，如果你能掌握以上内容，你已经可以可以通过python创建一个excel文件，然后填充你的数据，美化调整单元格的样式。如果你配合我前一篇博客，已经已经可以生成简单的`excel`报表了，当然，这里只是简单演示了`openpyxl`操作单元格的基本方法，其实还有很多强大的功能没有展示，比如`excel`的各种图表的绘制等，一方面是由于篇幅的原因，另外一方面我还没想好，但主要还是因为我还没学😂