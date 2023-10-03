
### Qt5安装

```sh
 pip install PyQt5 -i https://mirrors.bfsu.edu.cn/pypi/web/simple/
```


### 打包exe文件

```sh
pip install pyinstaller

pip install auto-py-to-exe
```


打包命令

```sh
pyinstaller -w -F .\LiningExcelProcessor.py 
```

`-w`表示隐藏控制台窗口，当然你也可以通过`--windowed`和`-- noconsole`来达成相同的效果，但是`exe`在执行时可能会被`360`之类的安装软件拦截