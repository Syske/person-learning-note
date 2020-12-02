- 在生产环境下启动Weblogic时，发现原来好好的nohup信息输出到指定文件中的功能，突然出问题了。现象是控制台输出的信息一部分输出到了我指定的文件，另一部分却输出到了nohup.out，而我是不想让它产生nohup.out文件，不知道是什么原因。

  ```sh
  nohup redirecting stderr to stdout
  ```

  

- 我的启动命令是这样的：
```sh
nohup bin/startManagedServer.sh myserver htp://192.168.0.1 -Xms2048m -Xmx2048m > logs/myserver.out &
```
- 现在指行这个命令，会给我产生两个文件，一个中logs/myserver.out，另一个是nohup.out文件。
怎样才能让它不产生nohup.out文件呢。
网上搜了半天，据说好象可以把后面的 “&” 改成 “2>&1 &”，于是把启动命令改成如下：
```sh
nohup bin/startManagedServer.sh myserver htp://192.168.0.1 -Xms2048m -Xmx2048m > logs/myserver.out 2>&1 &
```
- 再次执行，问题解决,解释如下：

> **2>&1**
表示把标准错误(stderr)重定向，标准输出(stdout)是1。
尖括号后面可以跟文件名，或者是&1, &2，分别表示重定向到标准输出和标准错误。

- 2> &1
- 1> &2
- 2> stderr.log
- 1> stdout.log