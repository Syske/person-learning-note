### 简介

简单来说，它是一个功能强大的快捷键集成工具，通过它我们可以将一些快捷命令和对应的快捷键绑定，比如说按下某个快捷键，执行一个`python`脚本

- 官网：[AutoHotKey](https://www.autohotkey.com/)
- 文档：[docs](https://www.autohotkey.com/docs/)


### 基本用法和规则

#### 基本语法

- `^`表示快捷键的`Ctrl`
- `!`表示快捷键的`Alt`
- `+`表示快捷键的`Shift`
- `#`表示会计就的`Win`
- `<^`表示左侧的`Ctrl`
- `>^`表示右侧的`Ctrl`
更多按键的对应关系，查看这里：[KeyList](https://www.autohotkey.com/docs/v2/KeyList.htm)
#### 将指定内容发送到当前窗口

如果当前是输入框，或者可编辑的区域，就是将指定内容输入到当前区域

```sh
^1::SendText "To Whom It May Concern"
```

- `^1`表示快捷键是`Ctrl + 1`
- `SendText`表示执行的操作
- `To Whom It May Concern`表示发送的内容
