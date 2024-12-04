# git常用统计操作

#### 统计时间段代码提交数量

```shell
 git log --format='%aN' | sort -u | while read name; do echo -en "$name\t"; git log --since ==2022-03-18 --until==2022-3-30  --author="$name" --pretty=tformat: --numstat | awk '{ add += $1; subs += $2; loc += $1 + $2 } END { printf "added lines: \t%s, removed lines: \t%s, total lines: \t%s\n", add, subs, loc }' -; done
```

