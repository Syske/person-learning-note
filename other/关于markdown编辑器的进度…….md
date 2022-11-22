# 关于markdown编辑器的进度……

前几天说要自己开发一款`markdown`编辑器，功能层面要保持`typora`的简洁和优雅，功能方面要实现`markdown`编辑、预览，同时还要支持主题的自定义，上次给各位小可爱展示了预览`markdown`的效果，今天我们也算取得了阶段性进展：已经可以完美实现`markdwon`文档的编辑和保存，阶段效果我也比较满意，所以今天再和各位小伙伴同步下：



由于最近一直在搞这个`markdown`编辑器，公众号也没顾不上更新新内容了，所以想着尽快搞出一个`deta`版本，然后慢慢更新。

其实过去这几天，我是一直在搜集各类关于`markdown`的开源项目，看能否可以从中找到可以借鉴的点，但是实际情况真的是一言难尽，感觉比我搞`java`还累（可能是前端这块比较杂，而且很多开源项目文档不够翔实，当然也可能是我的接口），我搜集了如下项目：

#### `vue-markdown`

本来打算以此作为最终的编辑器实现的，但是经过几天的研究，发下这玩意不好搞，由于它本身就是左右分屏的`markdown`编辑器，所以最后只好放弃了。

#### `marked`：

`marked`属于比较老牌的`markdown`解析工具，目前市面上很多`markdown`编辑器都是基于他进行开发的，在`markdwon`解析方面还是很强的，新版本号称速度 比`C`语言写的`Markdown`转换工具`Discount` 还要快。我最开始的`markdown`预览就是基于它实现的，用它来做`markdown`博客解析应该不错。

#### `highlightjs`

``highlightjs`是一款代码高亮的插件，通常不会单独使用，比如`marked`中就可以集成它，我们之前的代码高亮就是通过它来实现的。

#### `jquery-note`

一款轻量级的编辑器，原本是打算将他作为我的`markdown`编辑器的，但是发现用它实现的话，难度巨大，遂放弃。

#### `codemirror`：

大名鼎鼎的前端代码编辑器，很多`IDE`工具都集成了他，比如`IDEA`，`typora`编辑器在编辑`markdown`源码时，也用的它，当时我用它实现了`markdown`的源码编辑，但是考虑到反向解析不好做，最后也放弃了，有考虑做在线编辑器的小伙伴可以了解下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211212225321.png)

#### `turndown`

`turndown`是和`marked`正相反的工具，它是一个将`html`转为`markdown`的工具，原本打算将它和`marked`组合成使用的，但是考虑到更精细的操作和解析，最后也放弃了。

#### `vditor`

一款**所见即所得**编辑器，支持 *`Markdown`*。有三种解析方式，所见即所得、即时渲染和分屏预览，即时渲染和`typora`很类似，最终我的编辑器方案就选了这个，但是要吐槽的是，项目文档写的太差，我研究了好几天才写出`demo`，而且接口不够灵活，很多接口没有对外暴露。

但是有这么一个开源项目已经是谢天谢地了，毕竟即时预览的`markdown`编辑器太难得了。

这个开源项目是国内一家叫链滴的公司开源的，他们公司有一款`markdown`产品——思源笔记，有兴趣的小伙伴可以去下载看看。

可能因为这个开源项目脱胎于公司的产品，所以我觉得在使用上感觉过于臃肿，而且接口文档确实写的太差了。



#### 工具安利

最后再安利两款及时渲染的`markdown`编辑器，毕竟`typora`开始收费了，白嫖的小伙伴该找新的出路了。

##### Mark Text

`mark text`是一款开源的`markdown`编辑器，号称永远开源，界面也很简洁，可能是用惯了`typora`这样的`markdown`编辑器，我觉得还是差点感觉，而且软件启动很慢：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211212231552.png)

下载地址：

```
https://marktext.app/
```

官网也很简洁：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211212231925.png)



#### 思源笔记

也就是我上面说的链滴的产品，这款软件对我来说有点臃肿，感觉有点像`notion`，而且创建的文档并不是原生的`markdown`（不过提供了导出功能）

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211212232328.png)

我还是比较追求轻量级的`markdown`编辑器，喜欢那种沉浸式的感觉，所以我觉得思源笔记并不适合我。

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211212232905.png)

下载地址：

```
https://b3log.org/siyuan/
```

好了，今天的内容就先到这里，如果有小伙伴对这款正在开发中的编辑器感兴趣，可以先去`github`了解下，项目地址：
```
https://github.com/Syske/syskedown
```

最后我放上试用视频：