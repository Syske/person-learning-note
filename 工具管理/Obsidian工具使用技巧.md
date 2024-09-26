# Obsidian工具使用卡片

卡片代码：
```ccard
items: [
{
title: hello card
},
]



```

待办事项：

```dataview 
// dataview 不能缺，缺了识别不了 [list|table|task] field1, (field2 + field3) as myfield, ..., fieldN 
// 可以选择 list 或 table 或 task 三种视图，选择 table 时可以填写每列也就是 field 的名称，field 需出现在正常显示的笔记的 Front Matter 区域。 
from #tag or "folder" or [[link]] or outgoing[[link]] 
#// 查询的范围，可以使用标签，文件夹（可以用/进行嵌套），也可以使用双链,当前面加上 outgoing 表示从此链接发散。 
where field [>|>=|<|<=|=|&|'|'] [field2|literal value] (and field2 ...) (or field3...) 
// 根据 field 的值来进行过滤。 
sort field [ascending|descending|asc|desc] 
(ascending is implied if not provided) // 按照 field 排升降序。 
```

