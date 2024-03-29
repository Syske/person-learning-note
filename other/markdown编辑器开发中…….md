# markdown编辑器开发中……

最近因为`Typora`这款流行的`markdown`编辑器开始收费了，我以前一直以为它是开源的免费软件，直到最近才知道真相——之前竟然一直是测试版本，无形中竟然充当了小白鼠。当然，对于`Typora`收费这件事本来没有什么吐槽的，但是它之前用了那么多开源软件，然后让大家免费帮他推广安利，然后看行情好了，开始收费，这就有点吃相难看了。

另外，`98`的价格买一个可替代的编辑工具，我觉得不值，而且根据它的凭证说明，购买之后可能大版本还有继续收费，这就说不过去，而且连数据同步的功能都没有，直接把我劝退。

所以，最近我又一次萌发了自己手写一款`markdown`工具，之所以是又，是因为之前有过，但是后来都不了了之了，而且对于`nodejs`我确实也不熟悉，而这一次我是打算做下去的，打算作为一个长期打磨的产品，截至今天已经取得了一定的进展。



目前我的想法是，`markdown`编辑方面和`Typora`要尽可能保持一致（毕竟我已经习惯了`typora`），功能上我会加上`git`同步，其他的的看后续开发情况，下面是最开始做的功能计划：

##### 核心功能

- `markdown`编辑（快捷键支持）
- `markdown`预览（实时编辑实时预览）
- 代码高亮（行号）

##### 重要模块

- `git`同步
- 自定义主题支持
- 国际化支持
- 图床支持

##### 技术方案

目前`markdown`编辑器的核心技术解决方案是`electron`，这是目前比较流程的桌面端应用开发解决方案，基于`nodejs`实现，跨平台，而且降低了桌面应用开发难度，感兴趣的小伙伴可以自己去研究下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211204235614.png)

##### 目前进展

经过最近几天的摸索实践，今天终于实现了`markdown`文件的预览、代码高亮等功能，下面是半成品截图：

- 首页截图

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211204234611.png)

- 打开文件（支持快捷键操作）

  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211204234653.png)

  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211204234757.png)

- `markdown`预览效果

  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211204235118.png)

  关于编辑器的话，后面考虑用下面这款，但是还需要进一步改造（毕竟和我想要的所见即所得还有差距）：

  ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211205000049.png)

  好了，今天就先分享这么多，等后面编辑这块解决了，可以分享出来让各位小伙伴体验下。