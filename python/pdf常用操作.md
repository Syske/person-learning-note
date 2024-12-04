#python
### PyPDF2

提取`pdf`中的部分页面

```python
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(file_path, output_prefix):
    pdf = PdfReader(file_path)
    output_pdf = PdfWriter()
    pageNum = 1
    for page in pdf.pages:
        # 提取5页以后的内容
        if pageNum > 5:
            output_pdf.add_page(page)
        pageNum += 1

    with open(output_prefix, "wb") as output_file:
        output_pdf.write(output_file)

# 使用函数来分割PDF
split_pdf('test1.pdf', 'test2.pdf')
```


### FPDF

图片转`pdf`

```python
from PIL import Image
from fpdf import FPDF
import os

def images_to_pdf(images_paths, output_pdf):
    """
    将多个图片合并成一个PDF文件，每个图片占据一页。
    :param images_paths: 图片文件路径列表
    :param output_pdf: 输出PDF文件的路径
    """
    pdf = FPDF()
    
    for image_path in images_paths:
        with Image.open(image_path) as img:
            # 获取图片尺寸
            img_width, img_height = img.size
            # 将图片尺寸转换为PDF单位（毫米），假设分辨率为72dpi
            pdf_width = img_width / 85 * 25.4
            pdf_height = img_height / 85 * 25.4
            
            # 将图片添加到PDF中，每个图片一页
            pdf.add_page()
            pdf.image(image_path, x=0, y=0, w=pdf_width, h=pdf_height)
    
    # 保存PDF文件
    pdf.output(output_pdf, "F")

# 使用示例
#images_to_merge = ['image1.jpg', 'image2.jpg', 'image3.jpg']  # 图片文件路径列表
images_to_merge = os.listdir('./2pdf')
#print(type(images_to_merge))

for i in range(len(images_to_merge)):
    images_to_merge[i] =  f'./2pdf/page_{i + 1}.png'
output_file = 'merged.pdf'  # 输出PDF文件的路径
images_to_pdf(images_to_merge, output_file)
```


### pdf增加电子签章

```python
import PyPDF2
from PIL import Image
file_path = "D:\\workspace\\个人文件"
# 打开要签字的PDF文件并创建PDF reader对象
pdf_file = open(f'{file_path}\\民事起诉状.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)

# 获取第一页的PDF page对象
page = pdf_reader.pages[1]

# 打开要签字的图片文件并转换为PDF兼容的格式
signature_image = Image.open(f'{file_path}\\sign-leicao.png')
signature_image = signature_image.convert('RGB')

# 创建PDF模板对象并设置签名的位置和大小
template = page.extract_text_box()
template.rect.x = 100  # 签名的x坐标
template.rect.y = 500   # 签名的y坐标
template.rect.width = 200  # 签名的宽度
template.rect.height = 100  # 签名的的高度

# 将签名图片转换为PDF兼容的格式并添加到PDF模板中
signature_image_pdf = PyPDF2.utils.ImageReader(signature_image.fp)
template.merge(signature_image_pdf, template.rect)

# 创建PDF writer对象并写入输出PDF文件
pdf_writer = PyPDF2.PdfFileWriter()
pdf_writer.addPage(template)
output_pdf = open(f'{file_path}\\output.pdf', 'wb')
pdf_writer.write(output_pdf)

# 关闭文件
pdf_file.close()
output_pdf.close()
```