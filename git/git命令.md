tags: [#git]

- 1.设置全局用户名称

```
git config --global user.name "12345"
```

- 2.设置全局邮箱

```
git config --global user.email "12345@qq.cn"
- - #查看全局名称及邮箱
git config user.name
git config user.email
```


- 3.初始化本地库

```
git init
```

- 4.查看状态

```
git status
```

- 5.查看当前分支

```
git config  可以查看命令
git branch
git branch -av
```



- 生成ssh



```
1.ssh-keygen -t rsa -C "12323@qq.cn"
#用户名和密码为空 ，连续敲回车

2.cd ~/.ssh

3、查看公钥
cat id_rsa.pub 

ssh-rsa AAAAB3NzaC1yc2EAA5H9KBCjeQHU14o2snJXcvGn9OdqwSCgTBPYs+sqCvieU5Mhw3kzvjYXXIcev+TJGdw2bYljMrvfavTo6SfqKTp+O6OfLJOZUnpVXdOqpPHIQJpUygZfMscgDzKCoby66YUNOROTZ+y5Xs9CntWDL64LoGJ99ocfZh3So6rziTaWInIUGJAADAQABAAABAQC7hbUdwRT62NxFWnMhHcYFe4fNYq7tcAEF5q3U0MMWnk85tOq4ERrRqZQ4ZEKI+UWsLH/ddLMaZKk4xxNSYSyzO1sHbd1It1UXBfbEvHoBw44waVk6BsbEkclgUqyBg85ZW0t4oSnTIrYWtaPBhLc0Hz1uhQHpf1S5ZRO 12323@qq.cn
```

> 登录远程库系统 将上述公钥匙 放到共钥匙设置里面

- 添加  .gitignore文件，在工程上新增文件，选择java 删掉需要上传的文件。保存即可。

- 4.添加远程  

```
git remote add origin git@127.0.0.1:nsuranceServiceGroup/lss.git  别名最好不一样写

查看远程库：git remote -v
会出现两个链接
origin   git@127.0.0.1:nsuranceServiceGroup/lss.git (fetch)
origin   git@127.0.0.1:nsuranceServiceGroup/lss.git (push)

#一个是拉取 的一个是推送的
```
- 5.添加到暂存库

```
git add .
```
- 6.提交到暂存库

```
git commit -m "initial commit"
```

- 7.将gitlab的文件拉下来  第一次选yes

```
git pull origin master --allow-unrelated-histories
：q #退出
```
- 8.这个是将本地仓库代码上传到gitlab

```
git push -u origin master
```

---
- 切换分支

```
git checkout master
```

- 看命令

```
git marge -h #该命令可以忽略历史枪指向拉文件到本地库
```
- 从master住分支克隆一个develop分支
- 如果有开发任务
- 从develop分支克隆一个特性分支feature-001（禅道号）
- 将feature-001拉到本地进行本地开发
- 开发完成后将feature-001上传及  - 请求合并至develop分支  合并后删除feature-001分支
- 如果确定要发布  
- 从develop分支克隆一个发布分支release1.0.0
- 发布无误后 将release1.0.0请求合并至master分支  合并后删除release1.0.0

- 本地清理远程库已经删除的分支命令

```
git remote prune origin(远程库名称)
```

