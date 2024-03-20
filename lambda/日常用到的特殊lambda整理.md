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

- 将list中对象按某个属性分组，并将其中其他属性拼接成string字符串
```java
List<CoursePackCourseBaseVo> coursePackCourseBaseVos = bizCoursePackMapper.selectCoursePackCourseList(packIdList); 
Map<String, TwoResultTuple<String, String>> packCourseMap = coursePackCourseBaseVos.stream()  
            .collect(Collectors.toMap(  
                    CoursePackCourseBaseVo::getPackId, // Map的Key是packId  
                    course -> new TwoResultTuple<>(course.getCourseTitle(), String.valueOf(course.getCourseId())), // Map的Value是Pair对象  
                    (existing, replacement) -> new TwoResultTuple<>(  
                            existing.first + "," + replacement.first,  
                            existing.second + "," + replacement.second)  
            ));
```

- 将list按某个字段groupBy，然后将某个字段聚合成list
```java
Map<Integer, List<String>> typeDocIdMap = docRetrieveResults.stream().collect(  
        Collectors.groupingBy(a -> a.getSnapshot().getType() , Collectors.mapping(b -> b.getSnapshot().getId(), Collectors.toList())));
```

### 排序

```java
// 按更新时间倒叙  
results.sort(Comparator.comparing(DocRetrieveResult::getSnapshot, (a, b) -> -a.getUpdateTime().compareTo(b.getUpdateTime())));
```