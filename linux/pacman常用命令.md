**安装软件包**
 安装或者升级单个软件包，或者一列软件包（包含依赖包），使用如下命令：

```undefined
pacman -S package_name1 package_name2
```

有时候在不同的软件仓库中，一个软件包有多个版本（比如extra和testing）。你可以选择一个来安装：

```undefined
pacman -S extra/package_name
pacman -S testing/package_name
```

**删除软件包**
 删除单个软件包，保留其全部已经安装的依赖关系

```undefined
pacman -R package_name
```

删除指定软件包，及其所有没有被其他已安装软件包使用的依赖关系：

```undefined
pacman -Rs package_name
```

缺省的，pacman会备份被删除程序的配置文件，将它们加上*.pacsave扩展名。如果你在删除软件包时要同时删除相应的配置文件（这种行为在基于Debian的系统中称为清除purging），你可是使用命令：

```undefined
pacman -Rn package_name
```

当然，它也可以加上-s参数来删除当前无用的依赖。这样的话，真正删除一个软件包、它的配置文件以及所有不再需要的依赖的命令如下：

```undefined
pacman -Rsn package_name
```

**升级系统**
 Pacman能够只用一个指令来升级系统中所有已安装的包。升级的时间取决于你的系统有多新。



```undefined
pacman -Su
```

当然，最好做法的是将升级系统和同步仓库数据合成为一条指令：



```undefined
pacman -Syu
```

**查询包数据库**
 Pacman可以在包数据库中查询软件包，查询位置包含了包的名字和描述：



```go
pacman -Ss package
```

要查询已安装的软件包：



```go
pacman -Qs package
```

一旦你得到了软件包的完整名字，你可以获取关于它的更为详尽的信息：



```go
pacman -Si package
pacman -Qi package
```

要获取已安装软件包所包含文件的列表：



```go
pacman -Ql package
```

你也可以通过查询数据库获知目前你的文件系统中某个文件是属于哪个软件包。



```undefined
pacman -Qo /path/to/a/file
```

要罗列所有不再作为依赖的软件包(孤立orphans)：



```undefined
pacman -Qdt
```

Pacman使用-Q参数来查询本地软件包数据库。参见：



```bash
pacman -Q –help
```

…而使用-S参数来查询远程同步的数据库。参见：



```bash
pacman -S –help
```

**其它用法**
 Pacman是个非常广泛的包管理工具，这里只是它的一些其它主要特性。
 • 下载包而不安装它：



```undefined
pacman -Sw package_name
```

• 安装一个’本地’包（不从源里）：



```go
pacman -U /path/to/package/package_name-version.pkg.tar.gz
```

• 安装一个’远程’包（不从源里）：



```cpp
pacman -U http://url/package_name-version.pkg.tar.gz
```

• 清理当前未被安装软件包的缓存(/var/cache/pacman/pkg):



```undefined
pacman -Sc
```

• 完全清理包缓存：



```undefined
pacman -Scc
```

Warning: 关于pacman -Scc，仅在你确定不需要做任何软件包降级工作时才这样做。pacman -Scc会从缓存中删除所有软件包。
 • 要删除孤立软件包（递归的，要小心)：



```jsx
pacman -Rs $(pacman -Qtdq)
```

• 重新安装你系统中所有的软件包（仓库中已有的）：



```jsx
pacman -S $(pacman -Qq | grep -v “$(pacman -Qmq)”)
```

• 获取本地软件包和它们大小的一个已排序清单列表：



```cpp
LANG=C pacman -Qi | sed -n ‘/^Name[^:]*: (.*)/{s//1 /;x};/^Installed[^:]*: (.*)/{s//1/;H;x;s/n//;p}’ | sort -nk2
```

要了解更详细的参数开关可以pacman –help或者man pacman。

**配置**
 Pacman的配置文件位于/etc/pacman.conf。关于配置文件的进一步信息可以用man pacman.conf查看。

**常用选项**
 常用选项都在[options]段。阅读man手册或者查看缺省的pacman.conf可以获得有关信息和用途。
 *跳过升级软件包*
 如果由于某种原因，你不希望升级某个软件包，可以加入内容如下：



```undefined
IgnorePkg = 软件包名
```

*跳过升级软件包组*
 和软件包一样，你也可以象这样跳过升级某个软件包组：



```undefined
IgnoreGroup = gnome
```

