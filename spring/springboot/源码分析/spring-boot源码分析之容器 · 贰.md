# spring-boot源码分析之容器 · 贰

### 前言





### 容器

开始分享容器相关知识点之前，我们先补充一个知识点——`spring boot`默认容器。从创建容器的源码我们可以看出，在不指定容器类别的情况下，`spring boot`默认为我们创建的容器是`AnnotationConfigServletWebServerApplicationContext`

![](https://gitee.com/sysker/picBed/raw/master/20210902081459.png)

![](https://gitee.com/sysker/picBed/raw/master/20210902081545.png)

然后，在`debug`的时候，我也理清楚了`scan`调用的基本流程了（才发现昨天是找错类了，一直以为创建的是`default`的容器）：



### 总结

