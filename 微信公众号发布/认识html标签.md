tags: [#html]

#### 示例

让我们通过一个网页的学习，来对html标签有一个初步理解。平常大家说的上网就是浏览各种各式各样的网页，这些网页都是由**html标签**组成的。下面就是一个简单的网页。效果图如下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/1077694-20161209113848147-981300864.png)

我们来分析一下，这个网页由哪些html标签组成：

“勇气”是网页内容文章的标题，`<h1></h1>`就是**标题标签**，它在网页上的代码写成`<h1>勇气</h1>`。

“三年级时...我也没勇气参加。” 是网页中文章的段落，**`<p></p>`**是**段落标签**。它在网页上的代码写成 `<p>三年级时...我也没勇气参加。</p>`

网页上那张小女生的图片，由`img`标签来完成的，它在网页上的代码写成`<img src="1.jpg">`

网页的完整代码如下图： 

 ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/1077694-20161209113924538-87687929.jpg)

#### HTML 基本文档

```html
<!DOCTYPE html>
<html>
	<head>
		<title>文档标题</title>
	</head>
	<body>
	可见文本...
	</body>
</html>
```

#### 基本标签（Basic Tags）

```html
<h1>最大的标题</h1>
<h2> . . . </h2>
<h3> . . . </h3>
<h4> . . . </h4>
<h5> . . . </h5>
<h6>最小的标题</h6>
<p>这是一个段落。</p>
<br> （换行）
<hr> （水平线）
<!-- 这是注释 -->
```

#### 文本格式化（Formatting）

```html
<b>粗体文本</b>
<code>计算机代码</code>
<em>强调文本</em>
<i>斜体文本</i>
<kbd>键盘输入</kbd> 
<pre>预格式化文本</pre>
<small>更小的文本</small>
<strong>重要的文本</strong>

<abbr> （缩写）
<address> （联系信息）
<bdo> （文字方向）
<blockquote> （从另一个源引用的部分）
<cite> （工作的名称）
<del> （删除的文本）
<ins> （插入的文本）
<sub> （下标文本）
<sup> （上标文本）
```

#### 链接（Links）

```html
普通的链接：<a href="http://www.example.com/">链接文本</a> 
图像链接： <a href="http://www.example.com/"><img src="URL" alt="替换文本"></a> 
邮件链接： <a href="mailto:webmaster@example.com">发送e-mail</a> 书签： <a id="tips">提示部分</a> <a href="#tips">跳到提示部分</a>
```

------

#### 图片（Images）

```html
<img src="URL" alt="替换文本" height="42" width="42">
```

------

#### 样式/区块（Styles/Sections）

```html
<style type="text/css">

    h1 {color:red;} 
    p {color:blue;}

</style> 
<div>文档中的块级元素</div> 
<span>文档中的内联元素</span>
```

------

#### 无序列表

```html
<ul>     
    <li>项目</li>     
    <li>项目</li> 
</ul>
```

------

#### 有序列表

```html
<ol>     
    <li>第一项</li>     
    <li>第二项</li> 
</ol>
```

------

#### 定义列表

```html
<dl>
  <dt>项目 1</dt>
    <dd>描述项目 1</dd>
  <dt>项目 2</dt>
    <dd>描述项目 2</dd>
</dl>
```

------

#### 表格（Tables）

```html
<table border="1">
  <tr>
    <th>表格标题</th>
    <th>表格标题</th>
  </tr>
  <tr>
    <td>表格数据</td>
    <td>表格数据</td>
  </tr>
</table>
```

------

#### 框架（Iframe）

```html
<iframe src="demo_iframe.htm"></iframe>
```

------

#### 表单（Forms）

```html
<form action="demo_form.php" method="post/get">

    <input type="text" name="email" size="40" maxlength="50">

    <input type="password">   

    <input type="checkbox" checked="checked">

    <input type="radio" checked="checked">

    <input type="submit" value="Send">

    <input type="reset">

    <input type="hidden">

    <select>

        <option>苹果</option>

        <option selected="selected">香蕉</option>

        <option>樱桃</option>

    </select>

    <textarea name="comment" rows="60" cols="20"></textarea>

</form>
```

------

#### 实体（Entities）

```
&lt; 等同于 < 
&gt; 等同于 > 
&#169; 等同于 ©
```

总结一下，可以这么说，网页中每一个内容在浏览器中的显示，都要存放到各种标签中。HTML 是一种在 Web 上使用的通用标记语言。HTML 允许你格式化文本，添加图片，创建链接、输入表单、框架和表格等等，并可将之存为文本文件，浏览器即可读取和显示。

HTML 的关键是标签，其作用是指示将出现的内容。

[^参考1]: HTML 教程|菜鸟教程

