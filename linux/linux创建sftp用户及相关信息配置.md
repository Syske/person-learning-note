# linux创建sftp用户及相关信息配置

### **1、创建用户**

创建一个例名为 aaaa 的用户，指定它的默认目录为 /home/wwwroot/aaaa，并设置它的密码。

```bash
#创建用aaaa
~]＃ useradd -d /home/aaaa -m aaaa
#设置aaaa的密码，输入以下指令回车后输入密码即可
~]＃ passwd aaaa
```

后期想修改目录的话可以通过这个命令指定

```
usermod -d /home/wwwroot/test aaaa
```

如果不想让用户aaaa使用ssh登陆，安全性考虑用如下命令设置不允许登陆，但可以sftp访问

```bash
~]＃ usermod -s /sbin/nologin aaaa
```

恢复ssh登陆可用以下命令：

```bash
usermod -s /sbin/bash aaaa
```

### **2、权限设置与新建可写目录**

用户授权，设置目录权限，aaaa的用户组为root，据网上资料sftp用户访问目录需要设置所有者和所属组的权限均为root，并设置目录的权限为755，即注意两点：
(1)、ChrootDirectory（下面第3步会设置到这个目录） 的目录及其所有上级目录的所有者都只能为 root 
(2)、ChrootDirectory 的目录及其所有上级目录都不可以具有群组写入权限（最大权限 755）

```bash
#设置用户组为root
~]＃ chown -R root:aaaa /home/aaaa
#设置权限为755
~]＃ chmod 755 /home/aaaa
```

新建一个子目录，这个子目录，用户可以进行读写操作，权限可以设置到777由你定，一般新建时默认755可以了。

```bash
#新建子目录
~]＃ mkdir /home/aaaa/wwwroot
#为用户aaaa添加子目录的操作权
#设置所有者为aaaa，用户group为root，
~]＃ chown -R aaaa:root /home/aaaa/wwwroot
```

上面的第二句chown语句如果不设置的话，用户在wwwroot写入文件会提醒：Couldn't create directory: Permission denied

### **3、sftp设置**

修改配置文件 “sshd_config” 一般路径：/etc/ssh/sshd_config
执行命令：

```bash
~]＃ vi /etc/ssh/sshd_config
```

查找这一行：Subsystem   sftp   /usr/libexec/openssh/sftp-server，注释掉它。不然等一下重启会报错，接着往文件的末尾处添加以下代码，最好在末尾处添加

```bash
Subsystem sftp internal-sftp
UsePAM yes
Match user aaaa
ForceCommand internal-sftp
ChrootDirectory /home/aaaa
```

添加多个目录请重复这三句代码

```bash
Match user aaaa2
ForceCommand internal-sftp
ChrootDirectory /home/aaaa2
```

保存配置，下面两条指令自由选择一条执行重启sshd：

```bash
# reload:不间断服务重启
~]＃ /etc/init.d/sshd reload
# 或者用下面这条，先stop 再 start，间断服务重启
~]＃ /etc/init.d/sshd restart
```

### **4、测试sftp**

使用终端测试sftp，连接成功后，试着进入其它目录，可以看到提醒不存在的，因为限定了这个用户就只能访问自身的目录。

```
~]＃ sftp aaaa@192.168.1.286
Connecting to 116.62.190.22...
dukedb@116.62.190.22's password:
sftp> pwd
Remote working directory: /
sftp> cd /home
Couldn't canonicalise: No such file or directory
sftp> cd ../
sftp> pwd
Remote working directory: /
```