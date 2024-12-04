	
### python的历史



`Python`由荷兰国家数学与计算机科学研究中心的吉多·范罗苏姆于`1990`年代初设计，作为一门叫做`ABC`语言的替代品

`Python`已经成为最受欢迎的程序设计语言之一。自从`2004`年以后，`python`的使用率呈线性增长。

`Python 2`于`2000`年`10`月`16`日发布，稳定版本是`Python 2.7`。

`Python 3`于`2008`年`12`月`3`日发布，不完全兼容`Python 2`。

`2011`年`1`月，它被`TIOBE`编程语言排行榜评为`2010`年度语言。

截止到今天，`python`已经是最流行的编程语言。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240408221557.png)

[来源](https://www.tiobe.com/tiobe-index/)

### python的应用场景

#### 脚本

- 处理数据：汇总统计数据、处理表格、文档等
- 自动化办公

#### 爬虫

- 爬取网络上免费合法的数据和资料
- 抢票

#### 视觉开发

- 人脸识别：比对
- 图像识别
- ocr

#### web开发

- 网站后端系统开发

#### GUI应用开发

- 视图操作软件开发


#### 数据分析

- 房价分析



### 办公自动化应用


#### 操作pdf

##### 合并

```python
import PyPDF2

local = './'

pdf_files = ['1.pdf', '2.pdf']
output_pdf = PyPDF2.PdfWriter()
for pdf_file in pdf_files:
    # 循环读取需要合并pdf文件
    with open(local+pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
    # 遍历每个pdf的每一页
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            if pdf_file == '1.pdf':
                # 旋转90度
                page.rotate(90)
            output_pdf.add_page(page)
with open(local+'装修图2.pdf', 'wb') as file:
    output_pdf.write(file)
```
##### 分割

```python
import PyPDF2

local = './'

pdf_file = '1.pdf'
output_pdf = PyPDF2.PdfWriter()
  # 循环读取需要合并pdf文件
with open(local+pdf_file, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
# 遍历每个pdf的每一页
    for page_num in range(len(pdf_reader.pages)):
	    # 截取第三页
        if page_num == 2:
            page = pdf_reader.pages[page_num]
            output_pdf.add_page(page)
            
with open(local+'3.pdf', 'wb') as file:
  output_pdf.write(file)
```


#### pdf转word

```python
# 导入pdf2docx模块
from pdf2docx import parse

pdf_file = '1.pdf'

docx_file = '1.docx'

# convert pdf to docx

parse(pdf_file, docx_file)
```

#### word转pdf

```python
# pip install python-docx docx2pdf unoconv -i https://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
# 需要安装LibreOffice/OpenOffice
import docx2pdf

conversion = docx2pdf.convert("2.docx", "2.pdf")
```
#### pptx转pdf

```python

#  pip install pypandoc -i https://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
# 需要安装 pandoc https://pandoc.org/
import pypandoc  
  
def ppt_to_pdf_with_pandoc(ppt_path, pdf_path):  
    output = pypandoc.convert_file(ppt_path, 'pdf', outputfile=pdf_path)  
    return output  
  
# 使用函数进行转换  
ppt_to_pdf_with_pandoc('123.pptx', '123.pdf')
```

#### pdf转图片

```python
# coding=utf-8
#安装库 pip install pymupdf
import fitz
import os

def convert_pdf2img(file_relative_path):

    """

    file_relative_path : 文件相对路径

    """

    page_num = 1

    filename = file_relative_path.split('.')[-2]

    if not os.path.exists(filename):

        os.makedirs(filename)

    pdf = fitz.open(file_relative_path)

    for page in pdf:

        rotate = int(0)

        # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高4的图像。

        # 此处若是不做设置，默认图片大小为：792X612, dpi=96

        zoom_x = 2 # (2-->1584x1224)

        zoom_y = 2

        mat = fitz.Matrix(zoom_x, zoom_y)

        pixmap = page.get_pixmap(matrix=mat, alpha=False)

        pixmap.pil_save(f"{filename}/{page_num}.png")

        print(f"{filename}.pdf 第{page_num}页保存图片完成")

        page_num = page_num + 1


if __name__ =="__main__":

    # 文件夹中文件名

    file_list = os.listdir('./')

    for file in file_list:

        #print(file)

        if os.path.isfile(file) and file.endswith('.pdf'):

            convert_pdf2img(file)
```


### 操作图片

#### 图片格式转换

```python
import rawpy

import os

import imageio

file_path = ".\\100D5300\\"

file_list = os.listdir(file_path)

for file in file_list:

    print(file, str(file).endswith('.NEF'))

    if file.endswith('.NEF'):

       with rawpy.imread(file_path + file) as raw:

          rgb = raw.postprocess()

          #print(rgb)

          filename = file.split('.')[-2]

          imagename = file_path + filename+".jpg"

          imageio.imsave(imagename, rgb)
```


