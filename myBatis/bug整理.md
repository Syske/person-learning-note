### 1、Mybatis中文模糊查询，数据库中有数据，但无结果匹配

#### 1.1 问题描述：
    Mybatis采用中文关键字进行模糊查询，sql语句配置无误，数据库有该数据，且无任何报错信息，但无查询结果

#### 1.2 解决方法：

> 修改数据库连接地址：
    
```
url=jdbc:mysql://localhost:3306/test?characterEncoding=UTF-8
```
-  其中，characterEncoding=UTF-8必须写在第一位


    