# ubuntu常用操作

### 修改更新源

编辑`sources.list`文件

```sh
sudo vi /etc/apt/sources.list
```

将原有更新源注释掉，并加入国内更新源：

- 阿里云

```
deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
```

- 中科大

  ```
  deb https://mirrors.ustc.edu.cn/ubuntu/ bionic main restricted universe multiverse
  deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic main restricted universe multiverse
  
  deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
  deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
  
  deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
  deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
  
  deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
  deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
  ```

  

  ### vim常用命令补充

用命令示例:

将当前行第一个a替换为b

```
:s/a/b/
```

 

#将当前行的所有a替换为b

```
:s/a/b/g
```

 

将每行第一个a替换为b

```
:%s/a/b
```

 

将整个文件的所有a替换为b

```
:%s/a/b/g
```

 

将1至3行的第一个a替换为b

```
:1,3s/a/b/
```

 

将1至3行的所有a替换为b

```
:1,3s/a/b/g
```

 

上面是一些常用的替换,但是我们日常碰到的问题不止这么简单,这就要涉及到一些较为高级的替换操作,会涉及到转义,正则表达式相关的知识,下面是一些例子:

使用`#`作为分隔符，此时中间出现的`/`不会作为分隔符，如`:`将当前行的字符串"`a/`"替换为"`b/`"

```
:s#a/#b/#
```

 

找到包含字母a的行并删除

```
:g/a/d
```

 

删除所有空行

```
:g/^$/d
```

 

 多个空格替换为一个空格

```
:s/ \+/ /g
```

