

### 创建excel并写入数据

```python
	# 创建工作表
    wb = Workbook()
    # 获取激活的sheet
    ws = wb.active
    # 写入数据
    ws['A1'] = '租户id'
    ws['B1'] = '媒资大小'
    ws['C1'] = '媒资数量'
    ws['D1'] = '媒资时长'
    dataList = []
    for i in range(len(dataList)):
        data = dataList[i]
        ws['B{}'.format(i + 2)] = data[0]
        ws['C{}'.format(i + 2)] = data[1]
        ws['D{}'.format(i + 2)] = data[2]

    wb.save('vod_count.xlsx')
    wb.close()
```