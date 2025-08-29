tags: #git

#### 1、设置全局用户信息

```sh
git config --global user.name "syske" # 设置全局用户名
git config --global user.email "syske@qq.com" # 设置全局邮箱
```

### 2、查看全局名称及邮箱

```sh
git config user.name
git config user.email
```

### 3、初始化本地仓库

```sh
git init
```

### 4.查看状态

```sh
git status
```

### 5.查看当前分支

```sh
git config  可以查看命令
git branch
git branch -av
```

### 6、生成ssh

```sh
ssh-keygen -t rsa -C "syske@qq.com"
```

用户名和密码为空 ，连续敲回车

```sh
cd ~/.ssh
```

查看公钥

```sh
cat id_rsa.pub 
ssh-rsa AAAAB3Hz1uhQHpf1S5ZRO5H9KBCjeQHU14o2snJXcvNzaC1yc2EAAAADAQABAAABAQC7hbUdwRT62NxFWnMhHcYFe4fNYq7tcAEF5q3U0MMWnk85tOq4ERrRqZQ4ZEKI+UWsLH/ddLMaZKk4xxNSYSyzO1sHbd1It1UXBfbEvHoBw44waVk6BsbEkclgUqyBg85ZW0t4oSnTIrYWtaPBhLc0Hz1uhQHpf1S5ZRO5H9KBCjeQHU14o2snJXcvGn9OdqwSCgTBPYs+sqCvieU5Mhw3kzvjYXXIcev+TJGdw2bYljMrvfavTo6SfqKTp+O6OfLJOZUnpsdfdsfYUNOROTZ+y5Xs9CntWDL64LoGJ99ocfZh3So6rziTaWInIUGJ 123123@163.com
```


登录远程库系统 将上述公钥匙 放到共钥匙设置里面

### 7、添加远程仓库

```sh
git remote add origin git@github.com:Syske/note.git  #别名最好不一样写
```

### 8、查看远程库：

```sh
git remote -v
origin  git@github.com:Syske/note.git (fetch)
origin  git@github.com:Syske/note.git (push)
```

### 9、定义Git全局的 .gitignore 文件
```
 git config --global core.excludesfile ~/.gitignore
```

```
#               表示此为注释,将被Git忽略
*.a             表示忽略所有 .a 结尾的文件
!lib.a          表示但lib.a除外
/TODO           表示仅仅忽略项目根目录下的 TODO 文件，不包括 subdir/TODO
build/          表示忽略 build/目录下的所有文件，过滤整个build文件夹；
doc/*.txt       表示会忽略doc/notes.txt但不包括 doc/server/arch.txt
 
bin/:           表示忽略当前路径下的bin文件夹，该文件夹下的所有内容都会被忽略，不忽略 bin 文件
/bin:           表示忽略根目录下的bin文件
/*.c:           表示忽略cat.c，不忽略 build/cat.c
debug/*.obj:    表示忽略debug/io.obj，不忽略 debug/common/io.obj和tools/debug/io.obj
**/foo:         表示忽略/foo,a/foo,a/b/foo等
a/**/b:         表示忽略a/b, a/x/b,a/x/y/b等
!/bin/run.sh    表示不忽略bin目录下的run.sh文件
*.log:          表示忽略所有 .log 文件
config.php:     表示忽略当前路径的 config.php 文件
 
/mtk/           表示过滤整个文件夹
*.zip           表示过滤所有.zip文件
/mtk/do.c       表示过滤某个具体文件
 
被过滤掉的文件就不会出现在git仓库中（gitlab或github）了，当然本地库中还有，只是push的时候不会上传。
 
需要注意的是，gitignore还可以指定要将哪些文件添加到版本管理中，如下：
!*.zip
!/mtk/one.txt
 
唯一的区别就是规则开头多了一个感叹号，Git会将满足这类规则的文件添加到版本管理中。为什么要有两种规则呢？
想象一个场景：假如我们只需要管理/mtk/目录中的one.txt文件，这个目录中的其他文件都不需要管理，那么.gitignore规则应写为：：
/mtk/*
!/mtk/one.txt
 
假设我们只有过滤规则，而没有添加规则，那么我们就需要把/mtk/目录下除了one.txt以外的所有文件都写出来！
注意上面的/mtk/*不能写为/mtk/，否则父目录被前面的规则排除掉了，one.txt文件虽然加了!过滤规则，也不会生效！
 
----------------------------------------------------------------------------------
还有一些规则如下：
fd1/*
说明：忽略目录 fd1 下的全部内容；注意，不管是根目录下的 /fd1/ 目录，还是某个子目录 /child/fd1/ 目录，都会被忽略；
 
/fd1/*
说明：忽略根目录下的 /fd1/ 目录的全部内容；
 
/*
!.gitignore
!/fw/ 
/fw/*
!/fw/bin/
!/fw/sf/
说明：忽略全部内容，但是不忽略 .gitignore 文件、根目录下的 /fw/bin/ 和 /fw/sf/ 目录；注意要先对bin/的父目录使用!规则，使其不被排除。
```

- 温馨提示：

> 如果你不慎在创建.gitignore文件之前就push了项目，那么即使你在.gitignore文件中写入新的过滤规则，这些规则也不会起作用，Git仍然会对所有文件进行版本管理。简单来说出现这种问题的原因就是Git已经开始管理这些文件了，所以你无法再通过过滤规则过滤它们。所以大家一定要养成在项目开始就创建.gitignore文件的习惯，否则一单push，处理起来会非常麻烦。
