# nodejs搭建es6开发环境

#### 建立工程目录

先建立一个项目的工程目录，并在项目目录下创建`src`和`dist`文件夹。

- `src`：存放项目源文件
- `dist`：存放项目编译结果



#### 编写`index.html`

在项目根目录下创建`index.html`文件：

```html
<!DOCTYPE html>
<html>

<head>
  <meta charset="UTF-8">
  <script src="./dist/index.js"></script>
  <title>hello es6</title>
</head>

<body>
  hello es6 in nodejs
</body>
</html>
```

这里引入的是`dist`的`js`文件。



#### 编写`index.js`

在`src`目录下新建`index.js`文件，这里面写我们项目的`js`代码：

```js
let a = 1;
console.log(a);
```



#### 初始化项目

在开始项目代码编写之前，我们现要通过如下命令初始化项目：

```
npm init -y
```

其实也就是生成`package.json`文件，然后根据需要修改其中的内容。

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20211209222818.png)



#### 安装Babel-cli

这个安装是一个全局操作，也就是只需要安装一次，之后创建项目的时候不再需要安装。

```cmd
cnpm install -g bable-cli
```

这里的`cnpm`是一个镜像版的`npm`，和`npm`命令没有本质区别，安装方式如下：

```cmd
npm install -g cnpm --registry=https://registry.npm.taobao.org
```

`Babel-cli`我寻思就类似于`java`的编译命令，安装完成后通过如下命令进行文件编译（不知道前端是不是这么叫的）：

```
babel .\src\index.js -o .\dist\index.js
```

这时候你会发现`dist`文件夹下的文件和`src`文件夹下的源文件是没有任何区别：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20211209230141.png)

根据我查到的资料，但`babel-cli`是不够的，还需要安装`babel-preset-es2015`，安装这个依赖主要是为了兼容`es-2015`的语法（从这一点看，前端东西确实比较杂，也比较乱），当然也可以一步安装：

```
cnpm install --save-dev babel-preset-es2015 babel-cli
```

有所不同的是，上面的安装是针对项目安装的，也就是项目的依赖，所以建议先全局安装，然后再进入项目目录安装，安装之后，`package.json`会多出来两个依赖：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20211209224200.png)

感觉这个和`java`的`maven`依赖很像（更准确说是`gradle`）



#### 新建`.babelrc`

在根目录下创建`.babelrc`文件，由于`.`开头的文件是隐藏文件，所以建议在命令行下创建。当然，你也可以通过第三方编辑器创建，这里非常不建议通过记事本创建（`window`的记事本会存在编码问，会导致报错），然后在文件中添加如下内容：

```
{
  "presets": [
      "es2015"
  ], 
  "plugins": []
}
```

然后再次运行编译命令：

```cmd
babel .\src\index.js -o .\dist\index.js
```

这时候，编译之后的文件（`dist`下的文件）会多一行代码：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20211209230256.png)

如果编译过程中报如下错误，考虑`.babelrc`文件存在编码文件：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/blog/20211209230410.png)

更换编辑器就可以解决



#### 简化转化命令

和我们开发`java`一样，在实际开发中我们不可能手动转化（编译）每一个文件，所以为了简化流程，我们在进行`vue`等项目开发的时候，可以通过`npm run build`的方式进行转化，这里我们也可以通过类似的方式，只是需要修改`package.json`的配置：

```

```

