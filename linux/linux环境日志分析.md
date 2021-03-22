## 前言

了解`linux`常用命令，有助于提升我们的生产力，提升工作效率，更快速地定位问题，当然也是为了更好地解决问题。这两天，趁着在家办公的时间，我把`linux`系统中常用的命令整理了一下，主要涉及到查找、查看，都是日志分析是常用的，有几个命令平时工作中经常用到，也有很多从来都没有过，但都是特别有用的工具，掌握之后可以很好地协助我们解决`linux`环境下的很多问题，好了，闲话稍多，我们直接看正文。



## 日志分析

### 查看文件内容

#### cat

查看文件内容

##### 用法

```sh
cat fileName
```

##### 参数

```shell
  -A, --show-all           等效于 -vET
  -b, --number-nonblank    带行号输出，对空白行不编号
  -e                       等效于 -vE，行尾增加$符
  -E, --show-ends          效果同-e
  -n, --number             对所有输出行进行编号，感觉和-b类似
  -s, --squeeze-blank      当遇到有连续两行或两行以上的空白行，就代换为一行的空白行
  -t                       等效于 -vT
  -T, --show-tabs          对制表符TAB 以^I显示
  -u                       忽略
  -v, --show-nonprinting   使用^和M-符号，除了LFD和TAB
      --help     获取帮助信息
      --version  显示版本
```

#### tail

显示文件尾

##### 用法

```sh
tail [OPTION] fileName
```

##### 参数

```sh
 -c, --bytes=K            输出最后K个字节；或者，使用-c+K,从每个文件的第k个开始输出字节
  -f, --follow[={name|descriptor}]
                           随着文件的增长输出附加数据，强制刷新；
                           -f， --follow，和--follow=描述符是等效的     
  -F                       等效于 --follow=name --retry
  -n, --lines=K            输出最后K行，而不是最后10行；
                           或者使用-n+K输出以Kth开头的行
      --max-unchanged-stats=N
                           使用--follow=name，重新打开N次（默认5次）迭代后更改大小查看是							否已取消链接或重命名（这是旋转日志文件的常见情况）。
      --pid=PID            组合 -f, 在进程 ID, PID 死掉后终止
  -q, --quiet, --silent    从不输出给出文件名的头信息（文件名及路径）
      --retry              持续尝试打开文件，即使它是或不可访问的， 当它后面跟随文件名时是非						   常有效的, 例如，通过 --follow=name
  -s, --sleep-interval=N   组合 -f, 循环睡眠N秒(默认 1.0) 。
                           通过inotify 和 --pid=P, 确保进程P在N秒内至少运行一次
  -v, --verbose            总是输出文件头信息（文件名及路径）
      --help     获取帮助信息
      --version  查看版本信息
```

### 统计文件信息

#### wc

统计文件信息

##### 用法

```sh
wc [OPTION]
```

##### 参数

```shell
  -c, --bytes            统计字节数
  -m, --chars            统计字符数
  -l, --lines            统计行数
      --files0-from=F    从指定的以NUL结尾的文件F中文件读取文件名输入；
                           如果文件F是 - 则从示例输入中读取文件名
  -L, --max-line-length  打印最长行长度
  -w, --words            打印字数
      --help     获取帮助信息
      --version  显示版本信息
```

### 查找检索

#### grep

字符串查找

##### 用法

```
grep [OPTION]  PATTERN [fileName]
```

示例：`grep-i'hello world'menu.h main.c`

 PATTERN默认以正则表达式解析

**用grep -A,-B,-C 来查看after/before/around 行：**

```shell
grep -[A|B|C] [行数] [fileName]
```

例如：

```sh
 grep -A 10 -n 'KA06' int01bpoimp.java
```

就是在int01bpoimp.java中查找KA06并显示后面的10行，`-n`的意思是显示文件行号

##### 参数

```shell
-s, --no-messages		# 忽略错误信息

-v, --invert-match 		# 逆转结果，显示未匹配行

-V, --version， 			# 显示版本信息

  --help				# 获取帮助信息
  
-E、 --extended-regexp  # PATTERN是一个扩展正则表达式（ERE）

-F、 --fixed-strings	  # PATTERN是一组换行分隔的固定字符串

-G、 --basic-regexp  # PATTERN是一个基本正则表达式（BRE）

-P、 --perl-regexp  # PATTERN是一个perl正则表达式

-e、 --regexp=PATTERN  # 使用PATTERN进行匹配

-f、 --file=file  # 从file获取匹配内容

-i、 --ignore-case  # 忽略大小写区别

-w、 --word-regexp # 强制模式只匹配整个单词

-x、 --line-regexp # 强制模式只匹配整行

-z、 --null-data # 数据行以0字节结尾，而不是换行符

-n     # 显示文件行号
```

### 进程相关

#### ps

##### 用法

```sh
ps [-aefls] [-u UID] [-p PID]
```

##### 参数

```sh
 -a, --all       # 显示所有用户进程
 -e, --everyone  # 显示所有用户进程，感觉和-a一样
 -f, --full      # 显示进程uids, ppids
 -h, --help      # 获取帮助信息
 -l, --long      # 显示 uids, ppids, pgids, winpids
 -p, --process   # 显示指定PID的进程信息
 -s, --summary   # 显示进程汇总信息
 -u, --user      # 显示uid的进程信息，需指定uid
 -V, --version   # 显示版本信息
 -W, --windows   # 显示窗口和cygwin进程
```

#### kill

向由PID或JOBSPEC标识的进程发送由SIGSPEC或SIGNUM命名的信号。如果SIGSPEC和SIGNUM都不存在，则假定为SIGTERM。

Kill是shell内置的，原因有两个：它允许使用job id而不是进程id，并且允许在达到可以创建的进程限制时终止进程。

##### 用法

```sh
kill [-s sigspec | -n signum | -sigspec] pid | jobspec ... or kill -l [sigspec]
```

##### 参数

```sh
 -s sig    # sig是进程信号名称
 -n sig    # sig值进程信号号码
 -l        # 列出标识名；如果参数跟在“-l”后面，它们是假定为应列出其名称的信号号码
 -L        # 同-l
 -u		   # 杀死指定用户进程，后跟进程uid
```

##### 信号号码

```shell
# kill -l
1) SIGHUP     2) SIGINT     3) SIGQUIT     4) SIGILL     5) SIGTRAP
6) SIGABRT     7) SIGBUS     8) SIGFPE     9) SIGKILL    10) SIGUSR1
11) SIGSEGV    12) SIGUSR2    13) SIGPIPE    14) SIGALRM    15) SIGTERM
16) SIGSTKFLT    17) SIGCHLD    18) SIGCONT    19) SIGSTOP    20) SIGTSTP
21) SIGTTIN    22) SIGTTOU    23) SIGURG    24) SIGXCPU    25) SIGXFSZ
26) SIGVTALRM    27) SIGPROF    28) SIGWINCH    29) SIGIO    30) SIGPWR
31) SIGSYS    34) SIGRTMIN    35) SIGRTMIN+1    36) SIGRTMIN+2    37) SIGRTMIN+3
38) SIGRTMIN+4    39) SIGRTMIN+5    40) SIGRTMIN+6    41) SIGRTMIN+7    42) SIGRTMIN+8
43) SIGRTMIN+9    44) SIGRTMIN+10    45) SIGRTMIN+11    46) SIGRTMIN+12    47) SIGRTMIN+13
48) SIGRTMIN+14    49) SIGRTMIN+15    50) SIGRTMAX-14    51) SIGRTMAX-13    52) SIGRTMAX-12
53) SIGRTMAX-11    54) SIGRTMAX-10    55) SIGRTMAX-9    56) SIGRTMAX-8    57) SIGRTMAX-7
58) SIGRTMAX-6    59) SIGRTMAX-5    60) SIGRTMAX-4    61) SIGRTMAX-3    62) SIGRTMAX-2
63) SIGRTMAX-1    64) SIGRTMAX
```

不加任何参数直接执行 `kill`命令，默认执行的是`kill -15`

##### 常用信号

| 信号编号 | 信号名 | 含义                                                         |
| -------- | ------ | ------------------------------------------------------------ |
| 0        | EXIT   | 程序退出时收到该信息。                                       |
| 1        | HUP    | 挂掉电话线或终端连接的挂起信号，这个信号也会造成某些进程在没有终止的情况下重新初始化。 |
| 2        | INT    | 表示结束进程，但并不是强制性的，常用的 "Ctrl+C" 组合键发出就是一个 kill -2 的信号。 |
| 3        | QUIT   | 退出。                                                       |
| 9        | KILL   | 杀死进程，即强制结束进程。                                   |
| 11       | SEGV   | 段错误。                                                     |
| 15       | TERM   | 正常结束进程，是 kill 命令的默认信号。                       |

### 其他利器

#### awk

linux下强大的文本分析工具，支持正则

##### 用法

```shell
awk[POSIX或GNU样式选项]-f progfile[--]文件...
awk[POSIX或GNU样式选项][--]'program'文件...
```

##### 参数

```sh
    -f progfile		--file=progfile
	-F fs			--field-separator=fs
	-v var=val		--assign=var=val
	-m[fr] val
	-O			--optimize
	-W compat		--compat
	-W copyleft		--copyleft
	-W copyright		--copyright
	-W dump-variables[=file]	--dump-variables[=file]
	-W exec=file		--exec=file
	-W gen-po		--gen-po
	-W help			--help
	-W lint[=fatal]		--lint[=fatal]
	-W lint-old		--lint-old
	-W non-decimal-data	--non-decimal-data
	-W profile[=file]	--profile[=file]
	-W posix		--posix
	-W re-interval		--re-interval
	-W source=program-text	--source=program-text
	-W traditional		--traditional
	-W usage		--usage
	-W use-lc-numeric	--use-lc-numeric
	-W version		--version
```

#### curl

访问URL，可以发送`get`、`post`、`put`、`delete`等请求，完全可以取代 Postman

##### 用法

```sh
curl url
```

##### 常用参数（以下内容参考：阮一峰《curl 的用法指南》）

###### -A

`-A`参数指定客户端的用户代理标头，即`User-Agent`。curl 的默认用户代理字符串是`curl/[version]`。

 ```bash
 $ curl -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36' https://google.com
 ```

上面命令将`User-Agent`改成 Chrome 浏览器。

 ```bash
 $ curl -A '' https://google.com
 ```

上面命令会移除`User-Agent`标头。

也可以通过`-H`参数直接指定标头，更改`User-Agent`。

 ```bash
 $ curl -H 'User-Agent: php/1.0' https://google.com
 ```

###### -b

`-b`参数用来向服务器发送 Cookie。

 ```bash
 $ curl -b 'foo=bar' https://google.com
 ```

上面命令会生成一个标头`Cookie: foo=bar`，向服务器发送一个名为`foo`、值为`bar`的 Cookie。

 ```bash
 $ curl -b 'foo1=bar;foo2=bar2' https://google.com
 ```

上面命令发送两个 Cookie。

 ```bash
 $ curl -b cookies.txt https://www.google.com
 ```

上面命令读取本地文件`cookies.txt`，里面是服务器设置的 Cookie（参见`-c`参数），将其发送到服务器。

###### -c

`-c`参数将服务器设置的 Cookie 写入一个文件。

 ```bash
 $ curl -c cookies.txt https://www.google.com
 ```

上面命令将服务器的 HTTP 回应所设置 Cookie 写入文本文件`cookies.txt`。

###### -d

`-d`参数用于发送 POST 请求的数据体。

 ```bash
 $ curl -d'login=emma＆password=123'-X POST https://google.com/login
 # 或者
 $ curl -d 'login=emma' -d 'password=123' -X POST  https://google.com/login
 ```

使用`-d`参数以后，HTTP 请求会自动加上标头`Content-Type : application/x-www-form-urlencoded`。并且会自动将请求转为 POST 方法，因此可以省略`-X POST`。

`-d`参数可以读取本地文本文件的数据，向服务器发送。

 ```bash
 $ curl -d '@data.txt' https://google.com/login
 ```

上面命令读取`data.txt`文件的内容，作为数据体向服务器发送。

###### --data-urlencode

`--data-urlencode`参数等同于`-d`，发送 POST 请求的数据体，区别在于会自动将发送的数据进行 URL 编码。

 ```bash
 $ curl --data-urlencode 'comment=hello world' https://google.com/login
 ```

上面代码中，发送的数据`hello world`之间有一个空格，需要进行 URL 编码。

###### -e

`-e`参数用来设置 HTTP 的标头`Referer`，表示请求的来源。

 ```bash
 curl -e 'https://google.com?q=example' https://www.example.com
 ```

上面命令将`Referer`标头设为`https://google.com?q=example`。

`-H`参数可以通过直接添加标头`Referer`，达到同样效果。

 ```bash
 curl -H 'Referer: https://google.com?q=example' https://www.example.com
 ```

###### -F

`-F`参数用来向服务器上传二进制文件。

 ```bash
 $ curl -F 'file=@photo.png' https://google.com/profile
 ```

上面命令会给 HTTP 请求加上标头`Content-Type: multipart/form-data`，然后将文件`photo.png`作为`file`字段上传。

`-F`参数可以指定 MIME 类型。

 ```bash
 $ curl -F 'file=@photo.png;type=image/png' https://google.com/profile
 ```

上面命令指定 MIME 类型为`image/png`，否则 curl 会把 MIME 类型设为`application/octet-stream`。

`-F`参数也可以指定文件名。

 ```bash
 $ curl -F 'file=@photo.png;filename=me.png' https://google.com/profile
 ```

上面命令中，原始文件名为`photo.png`，但是服务器接收到的文件名为`me.png`。

###### -G

`-G`参数用来构造 URL 的查询字符串。

 ```bash
 $ curl -G -d 'q=kitties' -d 'count=20' https://google.com/search
 ```

上面命令会发出一个 GET 请求，实际请求的 URL 为`https://google.com/search?q=kitties&count=20`。如果省略`--G`，会发出一个 POST 请求。

如果数据需要 URL 编码，可以结合`--data--urlencode`参数。

 ```bash
 $ curl -G --data-urlencode 'comment=hello world' https://www.example.com
 ```

###### -H

`-H`参数添加 HTTP 请求的标头。

 ```bash
 $ curl -H 'Accept-Language: en-US' https://google.com
 ```

上面命令添加 HTTP 标头`Accept-Language: en-US`。

 ```bash
 $ curl -H 'Accept-Language: en-US' -H 'Secret-Message: xyzzy' https://google.com
 ```

上面命令添加两个 HTTP 标头。

 ```bash
 $ curl -d '{"login": "emma", "pass": "123"}' -H 'Content-Type: application/json' https://google.com/login
 ```

上面命令添加 HTTP 请求的标头是`Content-Type: application/json`，然后用`-d`参数发送 JSON 数据。

###### -i

`-i`参数打印出服务器回应的 HTTP 标头。

 ```bash
 $ curl -i https://www.example.com
 ```

上面命令收到服务器回应后，先输出服务器回应的标头，然后空一行，再输出网页的源码。

###### -I

`-I`参数向服务器发出 HEAD 请求，然会将服务器返回的 HTTP 标头打印出来。

 ```bash
 $ curl -I https://www.example.com
 ```

上面命令输出服务器对 HEAD 请求的回应。

`--head`参数等同于`-I`。

 ```bash
 $ curl --head https://www.example.com
 ```

###### -k

`-k`参数指定跳过 SSL 检测。

 ```bash
 $ curl -k https://www.example.com
 ```

上面命令不会检查服务器的 SSL 证书是否正确。

###### -L

`-L`参数会让 HTTP 请求跟随服务器的重定向。curl 默认不跟随重定向。

 ```bash
 $ curl -L -d 'tweet=hi' https://api.twitter.com/tweet
 ```

###### --limit-rate

`--limit-rate`用来限制 HTTP 请求和回应的带宽，模拟慢网速的环境。

 ```bash
 $ curl --limit-rate 200k https://google.com
 ```

上面命令将带宽限制在每秒 200K 字节。

###### -o

`-o`参数将服务器的回应保存成文件，等同于`wget`命令。

 ```bash
 $ curl -o example.html https://www.example.com
 ```

上面命令将`www.example.com`保存成`example.html`。

###### -O

`-O`参数将服务器回应保存成文件，并将 URL 的最后部分当作文件名。

 ```bash
 $ curl -O https://www.example.com/foo/bar.html
 ```

上面命令将服务器回应保存成文件，文件名为`bar.html`。

###### -s

`-s`参数将不输出错误和进度信息。

 ```bash
 $ curl -s https://www.example.com
 ```

上面命令一旦发生错误，不会显示错误信息。不发生错误的话，会正常显示运行结果。

如果想让 curl 不产生任何输出，可以使用下面的命令。

 ```bash
 $ curl -s -o /dev/null https://google.com
 ```

###### -S

`-S`参数指定只输出错误信息，通常与`-s`一起使用。

 ```bash
 $ curl -s -o /dev/null https://google.com
 ```

上面命令没有任何输出，除非发生错误。

###### -u

`-u`参数用来设置服务器认证的用户名和密码。

 ```bash
 $ curl -u 'bob:12345' https://google.com/login
 ```

上面命令设置用户名为`bob`，密码为`12345`，然后将其转为 HTTP 标头`Authorization: Basic Ym9iOjEyMzQ1`。

curl 能够识别 URL 里面的用户名和密码。

 ```bash
 $ curl https://bob:12345@google.com/login
 ```

上面命令能够识别 URL 里面的用户名和密码，将其转为上个例子里面的 HTTP 标头。

 ```bash
 $ curl -u 'bob' https://google.com/login
 ```

上面命令只设置了用户名，执行后，curl 会提示用户输入密码。

###### -v

`-v`参数输出通信的整个过程，用于调试。

 ```bash
 $ curl -v https://www.example.com
 ```

`--trace`参数也可以用于调试，还会输出原始的二进制数据。

 ```bash
 $ curl --trace - https://www.example.com
 ```

###### -x

`-x`参数指定 HTTP 请求的代理。

 ```bash
 $ curl -x socks5://james:cats@myproxy.com:8080 https://www.example.com
 ```

上面命令指定 HTTP 请求通过`myproxy.com:8080`的 socks5 代理发出。

如果没有指定代理协议，默认为 HTTP。

 ```bash
 $ curl -x james:cats@myproxy.com:8080 https://www.example.com
 ```

上面命令中，请求的代理使用 HTTP 协议。

###### -X

`-X`参数指定 HTTP 请求的方法。



 ```bash
 $ curl -X POST https://www.example.com
 ```

上面命令对`https://www.example.com`发出 POST 请求。



#### more

分页显示文件内容，Enter下一行，空格下一页，F下一屏，B上一屏，Q退出

##### 用法

```shell
more fileName
```

#### less

分页显示文件内容

```
less fileName
```

##### 参数

```shell
                   SUMMARY OF LESS COMMANDS

      Commands marked with * may be preceded by a number, N.
      # 标有*的命令前面可以加一个数字N。
      Notes in parentheses indicate the behavior if N is given.
      # 括号中的注释表示给定N时的行为。

  h  H                 Display this help. # 显示帮助信息
  q  :q  Q  :Q  ZZ     Exit.   # 退出
 ---------------------------------------------------------------------------

                           MOVING
                           # 光标移动
  # 向前移动过一行或多行
  e  ^E  j  ^N  CR  *  Forward  one line   (or N lines).
  # 向后移动过一行或多行
  y  ^Y  k  ^K  ^P  *  Backward one line   (or N lines).
  # 向前一屏或多行
  f  ^F  ^V  SPACE  *  Forward  one window (or N lines).
  # 向后一屏或多行
  b  ^B  ESC-v      *  Backward one window (or N lines).
  # 向后一屏并设置窗口为N
  z                 *  Forward  one window (and set window to N).
  # 向前一屏并设置窗口为N
  w                 *  Backward one window (and set window to N).
  # 向前移动一个窗口，但不要在文件末尾停止
  ESC-SPACE         *  Forward  one window, but don't stop at end-of-file.
  # 向前移动一个半窗口（并将半窗口设置为N）
  d  ^D             *  Forward  one half-window (and set half-window to N).
  # 向后移动一个半窗口（并将半窗口设置为N）
  u  ^U             *  Backward one half-window (and set half-window to N).
  # 右箭头*左半屏幕宽度（或N个位置）。
  ESC-)  RightArrow *  Left  one half screen width (or N positions).
  # 左箭头*右半屏幕宽度（或N个位置）。
  ESC-(  LeftArrow  *  Right one half screen width (or N positions).
  # 一直向前；像“tail -f”。
  F                    Forward forever; like "tail -f".
  # 刷新屏幕
  r  ^R  ^L            Repaint screen.
  # 刷新屏幕，丢弃缓冲输入。
  R                    Repaint screen, discarding buffered input.
        ---------------------------------------------------
        Default "window" is the screen height.
        Default "half-window" is half of the screen height.
 ---------------------------------------------------------------------------

                          SEARCHING
  # 向前搜索
  /pattern          *  Search forward for (N-th) matching line.
  # 向后搜索
  ?pattern          *  Search backward for (N-th) matching line.
  # 重复上次搜索
  n                 *  Repeat previous search (for N-th occurrence).
  # 反向重复上次搜索
  N                 *  Repeat previous search in reverse direction.
```



## 结语

虽然现在好多公司都采用的是云容器、云服务器，但掌握`Linux`常用的工具也是特别重要的，有一句话我特别认同：工作上要避免重复造轮子，但在学习上你必须要重复造轮子。我个人的理解是，工作上考虑到效率和开发进度，不允许我们浪费时间，而且自己造的轮子可靠性也不好说，但是在学习上我们只有通过重复造轮子才能了解很多组件的底层工作原理，也才能知其然，知其所以然。

回到今天分享的内容上就是，我们只有了解清楚了`Linux`的常用命令，然后慢慢解开`Linux`的神秘面纱，才能更清楚的了解云服务器，因为云容器都是运行在`Linux`环境下的，所以我最佩服的神级程序员就是`linus Torvalds`，不仅开发出了`Linux`（`22`岁）这样伟大的操作系统内核，而且还开发出了`git`（大佬仅有`10`天就开发出来了）伟大这样的多人协同神器，普通人怕是一辈子都达不到这样的高度，甚至可能想都不敢想，但`linus`在他年纪轻轻的时候就做到了，果然有些人的优秀就是天生的。好了，今天的内容就到这里吧，大家周末快乐呀😋