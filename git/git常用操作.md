#### 1、设置全局用户信息

```sh
git config --global user.name "syske" # 设置全局用户名
git config --global user.email "caolei199311@163.com" # 设置全局邮箱
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
ssh-keygen -t rsa -C "caolei199311@163.com"
```

用户名和密码为空 ，连续敲回车

```sh
cd ~/.ssh
```

查看公钥

```sh
cat id_rsa.pub 
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC7hbUdwRT62NxFWnMhHcYFe4fNYq7tcAEF5q3U0MMWnk85tOq4ERrRqZQ4ZEKI+UWsLH/ddLMaZKk4xxNSYSyzO1sHbd1It1UXBfbEvHoBw44waVk6BsbEkclgUqyBg85ZW0t4oSnTIrYWtaPBhLc0Hz1uhQHpf1S5ZRO5H9KBCjeQHU14o2snJXcvGn9OdqwSCgTBPYs+sqCvieU5Mhw3kzvjYXXIcev+TJGdw2bYljMrvfavTo6SfqKTp+O6OfLJOZUnpVXdOqpPHIQJpUygZfMscgDzKCoby66YUNOROTZ+y5Xs9CntWDL64LoGJ99ocfZh3So6rziTaWInIUGJ caolei199311@163.com
```


登录远程库系统 将上述公钥匙 放到共钥匙设置里面

### 7、添加远程仓库

```sh
git remote add origin git@github.com:Syske/note.git  #别名最好不一样写
```

### 8、查看远程库：

```sh
git remote -v
origin  git@10.189.139.34:MedicalIInsuranceServiceGroup/ydjy/ydjylss.git (fetch)
origin  git@10.189.139.34:MedicalIInsuranceServiceGroup/ydjy/ydjylss.git (push)
```