### 1、内存设置的坑
在1.8之前的jdk中，设置内存的参数基本都是：
```
-XX:PermSize=128m
-XX:MaxPermSize=256m
```
但是升级到1.8以后，这些参数就不再起作用，当然你设置了也不会报错，只有把上面的参数换成这样才有效：
```
-XX:MetaspaceSize=128m
-XX:MaxMetaspaceSize=256m
```
- 新参数叫元空间（MetaspaceSize）
- 当然本质上的问题是因为jdk1.8取消了永久代，因为在以前的jdk中经常会出现永久代内存泄漏的问题
```
#主要是1.6及以前的版本
java.lang.OutOfMemoryError: PerMGen spance
```
在jdk1.8中（应该说从jdk1.7开始），将字符串有永久代转移到堆中，从1.8开始取消了永久代，所以我们再也看不到上面的错误，转而替代的是：
```
java.lang.OutOfMemoryError: java Heap space
```