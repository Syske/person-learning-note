- 安装指定文件到本地仓库命令：
> mvn install:install-file

> -DgroupId=<groupId>       : 设置项目代码的包名(一般用组织名)

> -DartifactId=<artifactId> : 设置项目名或模块名 

> -Dversion=1.0.0           : 版本号

> -Dpackaging=jar           : 什么类型的文件(jar包)

> -Dfile=<myfile.jar>       : 指定jar文件路径与文件名(同目录只需文件名)

- 安装命令实例：
```sh
mvn install:install-file -DgroupId=com.baidu -DartifactId=ueditor -Dversion=1.0.0 -Dpackaging=jar -Dfile=ueditor-1.1.2.jar
```