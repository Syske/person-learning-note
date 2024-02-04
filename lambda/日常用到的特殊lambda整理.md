# 日常用到的特殊lambda整理

#### `map`处理

-  提取`map`嵌套`map`的内层`value`

```java
// 原数据结构：
Map<Long, Map<Long, TutorialsEvaluationDto>> tutorialsEvaluationDtoMap = Maps.newHashMap();
// 省略数据获取过程

// lambda数据处理，提取TutorialsEvaluationDto的userId
List<Long> userIds = tutorialsEvaluationDtoMap.values().stream().map(Map::values).flatMap(Collection::stream)
                       .map(TutorialsEvaluationDto::getUserId).collect(Collectors.toList());

```