## 日志分析

了解linux常用命令，有助于提升我们的生产力，提升工作效率，更快速地定位问题，当然也是为了更好地解决问题。这两天，趁着在家办公的时间，我把linux系统中常用的命令整理了一下，主要涉及到查找、查看，有几个命令平时共组经常用到，也有很多从来都没有过。

#### 查看文件内容

##### cat

查看文件内容

**用法**

```sh
cat fileName
```

**参数：**

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

##### tail

显示文件尾

**用法**

```sh
tail [OPTION] fileName
```

**参数**

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

#### 统计文件信息

##### wc

统计文件信息

**用法**

```sh
wc [OPTION]
```

**参数**

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

#### 查找检索

##### grep

字符串查找

**用法**

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

**参数**

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

#### 进程相关

##### ps

**用法：**

```sh
ps [-aefls] [-u UID] [-p PID]
```

**参数**

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

##### kill

向由PID或JOBSPEC标识的进程发送由SIGSPEC或SIGNUM命名的信号。如果SIGSPEC和SIGNUM都不存在，则假定为SIGTERM。

Kill是shell内置的，原因有两个：它允许使用job id而不是进程id，并且允许在达到可以创建的进程限制时终止进程。

**用法：**

```sh
kill [-s sigspec | -n signum | -sigspec] pid | jobspec ... or kill -l [sigspec]
```

**参数**

```sh
 -s sig    # sig是进程信号名称
 -n sig    # sig值进程信号号码
 -l        # 列出标识名；如果参数跟在“-l”后面，它们是假定为应列出其名称的信号号码
 -L        # 同-l
 -u		   # 杀死指定用户进程，后跟进程uid
```

信号号码

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

常用信号

| 信号编号 | 信号名 | 含义                                                         |
| -------- | ------ | ------------------------------------------------------------ |
| 0        | EXIT   | 程序退出时收到该信息。                                       |
| 1        | HUP    | 挂掉电话线或终端连接的挂起信号，这个信号也会造成某些进程在没有终止的情况下重新初始化。 |
| 2        | INT    | 表示结束进程，但并不是强制性的，常用的 "Ctrl+C" 组合键发出就是一个 kill -2 的信号。 |
| 3        | QUIT   | 退出。                                                       |
| 9        | KILL   | 杀死进程，即强制结束进程。                                   |
| 11       | SEGV   | 段错误。                                                     |
| 15       | TERM   | 正常结束进程，是 kill 命令的默认信号。                       |

#### 其他利器

##### awk

linux下强大的文本分析工具，支持正则

**用法：**

```shell
awk[POSIX或GNU样式选项]-f progfile[--]文件...
awk[POSIX或GNU样式选项][--]'program'文件...
```

**参数**

```
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

##### curl

访问URL

**用法**

```
curl url
```

##### more

分页显示文件内容，Enter下一行，空格下一页，F下一屏，B上一屏，Q退出

**用法**

```shell
more fileName
```

##### less

分页显示文件内容

```
less fileName
```

**参数：**

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
