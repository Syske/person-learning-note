# sofa服务启动报错



错误截图：

![](https://gitee.com/sysker/picBed/raw/master/2022/20220509095157.png)

导致该问题的原因是缺少`rpc-sofa-boot`的`starter`，所以只需要增加如下依赖即可：

```xml
<dependency>
    <groupId>com.alipay.sofa</groupId>
    <artifactId>rpc-sofa-boot-starter</artifactId>
</dependency>
```

