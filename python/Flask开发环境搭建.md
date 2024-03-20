# Flask开发环境搭建

#python #flask

#### 创建虚拟环境

```sh
> mkdir myproject
> cd myproject
> py -3 -m venv venv 
# linux/Mac环境通过如下命令
 python3 -m venv venv
```

#### 激活虚拟环境

```sh
> venv\Scripts\activate
# linux/mac
. venv/bin/activate
```

#### 安装 Flask

```
$ pip install Flask
```



#### 编写项目代码

```python
from flask import Flask,render_template,url_for

app = Flask(__name__)

@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/index") 
def index(name=None):
    return render_template('index.html', name=name)
```



#### 设置项目入口

这里的`hello`指的是项目主入口的文件名，这里我们的文件名为`hello.py`

```sh
 $env:FLASK_APP = "hello"
 # bash
 export FLASK_APP=hello
```



#### 运行

通过如下命令即可运行项目：

```sh
 flask run -h 0.0.0.0
```

