# git 优化美化

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

