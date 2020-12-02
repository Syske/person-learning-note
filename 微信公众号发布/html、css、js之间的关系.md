学习web前端开发基础技术需要掌握：HTML、CSS、JavaScript语言。下面我们就来了解下这三门技术都是用来实现什么的：

如果把前端web比作一栋房子的话，那么html就好比房子的架构，类似房子的承重墙、柱子、屋顶、楼梯等，是最基本的必须元素；

![html_title](../images/20200123131944318_3895.png)

而css就好比房子的装修，类似房子的地砖、墙面、装饰面等的装饰材料，不是必须的，但如果合理使用的话，会让你的网页看起来很漂亮，当然如果使用不合理就适得其反。本质上来说，css就好比设计师的画笔，就看你如何发挥，取决于你的审美。（这里css修饰的网页就不放图片了，基本上我们平时看到的内容都是css修饰过的，放一张网上搞笑的对比图片大家感受下）

<img src="../images/20200123132009842_11928.png" alt="nocss" style="zoom:50%;" />

至于javascript，他的作用是赋予html和css活力，让他们每一个元素都可以移动、变化、甚至消失。想象一下，如果有一个工具，可以让你们家墙面改变颜色，让你们家地板改变样式，让你们家墙面自由移动，甚至可以动态地改变房子空间，是不是很炫酷。JavaScript做的就是这样的事，在javascript的世界，很多事都是可能的，有个叫法布里斯·贝拉（FabriceBellard）的大佬，2011年，他单用JavaScript写了一个PC虚拟机Jslinux   。这个虚拟机仿真了一个32位的x86兼容处理器，一个8259可编程中断控制器，一个8254可编程中断计时器，和一个16450 UART。让你可以在Web浏览器中启动Linux。

1. **HTML**是网页内容的载体。内容就是网页制作者放在页面上想要让用户浏览的信息，可以包含文字、图片、视频等。

   ```html
   <html><!-- 核心主标签 -->
       <head>
           <!-- 头部标签 -->
           <!-- 这里一般会放置网页引用的资源文件，比如css样式 -->
       </head>
       <body>
           <!-- 主体标签 -->
           <!-- 这里就是网页呈现给用户的内容 -->
       </body>    
   </html>
   ```

   

2. **CSS**样式是表现。就像网页的外衣。比如，标题字体、颜色变化，或为标题加入背景图片、边框等。所有这些用来改变内容外观的东西称之为表现。

   ```css
   <style type='text/css'>     
   	html { 
           font-size: 14px; 
           background-color: #ccc; color: #000; 
           font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
       }
   	body { 
           margin: 0px; 
           padding: 0px; 
           height: auto; 
           bottom: 0px; 
           top: 0px; 
           left: 0px; 
           right: 0px; 
           font-size: 1rem; 
           line-height: 1.42857; 
           overflow-x: hidden; 
           background: inherit; 
           tab-size: 4; 
       }
   </style>
   ```

   

3. **JavaScript**是用来实现网页上的特效效果。如：鼠标滑过弹出下拉菜单。或鼠标滑过表格的背景颜色改变。还有焦点新闻（新闻图片）的轮换。可以这么理解，有动画的，有交互的一般都是用JavaScript来实现的。

   ```html
   <script type="text/javascript">
           window.onload = function() {
               alert("hello html/ccs/javascript")
           }
   	// 这段代码的作用是网页加载完成后，弹窗显示hello html/ccs/javascript
   </script>
   ```

   