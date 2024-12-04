#python #excel

## 操作excel

### csv转excel

```python
import os, csv, sys, openpyxl
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

def csv2excel(csv_filename, excel_filename):
  # new work book
  wb2 = Workbook()
  # active sheet
  ws2 = wb2.active
  #Copy in csv
  f = open(csv_filename, encoding='utf-8',errors='ignore')
  reader = csv.reader(f)
  for row_index, row in enumerate(reader):
    for column_index, cell in enumerate(row):
      column_letter = get_column_letter((column_index + 1))
      ws2.cell(row_index + 1, (column_index + 1)).value = cell
    print('line:' + str(row_index+1))

  wb2.save(filename = excel_filename)
  print("new Cashflow created")
```