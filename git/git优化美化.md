# git 优化美化

tags: [#git]

### 1、中文乱码

#### git status中文乱码

```shell
 git config --global core.quotepath false
```

#### 中文显示乱码

```
git config --global i18n.logoutencoding utf-8
# 设置提交编码
git config --global i18n.commitencoding utf-8
```

### 2、修改编辑器

git默认的编辑器为`nano`，不常用，需要修改为`vim`，方法如下：

打开`.git/config`文件，在`core`中添加 `editor=vim`即可。

或者运行命令` git config --global core.editor vim` 修改更加方便。