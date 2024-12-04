# 资源加载器

### 前言
几个月前，有同事给我们分享了`apollo`的配置加载过程，因为当时刚刚研究过`spring boot`的启动过程，所以对于`spring boot`的资源加载后置处理器有点印象，所以我当时觉得`apollo`应该就是通过这个组件来实现的，后来闲下来我就打算研究下这块的实现逻辑，于是就有了今天的内容。

### 资源加载器
```properties
org.springframework.boot.env.PropertySourceLoader=io.github.syske.springbootbeanlisttest.sourceloader.SyskePropertySourceLoader
```

资源加载器
```java
/**
 * @program: springboot-bean-list-test
 * @description: 资源加载器
 * @author: syske
 * @date: 2022-06-23 17:53
 */
public class SyskePropertySourceLoader implements PropertySourceLoader {
    @Override
    public String[] getFileExtensions() {
        return new String[] {"properties"};
    }

    @Override
    public List<PropertySource<?>> load(String name, Resource resource) throws IOException {
        System.out.println("加载配置文件……");
        List<PropertySource<?>> propertySourceList = Lists.newArrayList();
        Properties properties = new Properties();
        properties.load(resource.getInputStream());
        properties.setProperty("server.port", "8088");
        PropertySource propertySource = new PropertiesPropertySource("test", properties);
        propertySourceList.add(propertySource);

        return propertySourceList;
    }
}
```