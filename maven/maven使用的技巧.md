# maven使用技巧

### 前言
`maven`对每一个做`java`开发的小伙伴肯定都不陌生


### 常见报错

`http`安全问题

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20240809111126.png)

解决方法：
在对应镜像中，增加`blocked`，并将对应内容设置为`false

```xml
<mirrors>
  <mirror>
    <id>maven-default-http-blocker</id>
    <name>Block the use of insecure "http" in favor of "https"</name>
    <url>http://0.0.0.0/</url>
    <mirrorOf>central</mirrorOf>
    <!-- Allow HTTP connections -->
    <blocked>false</blocked>
  </mirror>
</mirrors>
```