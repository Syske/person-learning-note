### 扫描命令
```sh
mvn sonar:sonar   -Dsonar.host.url=http://sonar.coolcollege.cn:9001   -Dsonar.login=7cd050b58095a951b35e72e6af8e472db1c06791
```

### 常见扫描规则

#### 1. Use static access with "".

父类的静态成员不应该使用子类访问

##### 例

```
Use static access with "com.alibaba.fastjson.JSON" for "parseObject".
```

问题代码

```java
logger.info("-----提报提交结果：{}", JSONObject.toJSONString(submitInstance));
```

修改方案

```java
logger.info("-----提报提交结果：{}", JSON.toJSONString(submitInstance));
```

#### 2. Provide the parametrized type for this generic.

为此泛型提供参数化类型