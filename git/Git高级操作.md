# Git高级操作



### merge后回滚操作



#### 查看日志

查看所有分支的所有操作记录（包括已经被删除的 `commit `记录和 `reset `的操作）

```sh
 git reflog
```

找到`merge`操作

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211020113317.png)



#### 回滚操作

通过`reset`命令回退到`merge`之前的操作：

```sh
git reset --hard b85bbfb424
```

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211020113637.png)



#### 推送到远程

如果`merge`之后已经`push`远程仓库，则还需要强制推送到远程：

```sh
git push -f
```

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211020113828.png)

至此，`merge`操作就回滚成功了。