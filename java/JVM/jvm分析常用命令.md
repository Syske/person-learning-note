# JVM 分析常用命令

JVM 分析是 Java 应用性能调优和故障排查的重要环节，以下是一些常用的 JVM 分析命令和工具：

## 基础监控命令

1. **jps** - Java 进程状态工具
   ```
   jps -lvm
   ```
   列出所有 Java 进程及其主类和 JVM 参数

2. **jstat** - JVM 统计监控工具
   ```
   jstat -gcutil <pid> 1000 10
   ```
   每1秒(1000ms)采集一次GC情况，共10次

3. **jinfo** - JVM 配置信息工具
   ```
   jinfo <pid>
   ```
   查看指定进程的 JVM 参数和系统属性

## 内存分析命令

4. **jmap** - 内存映射工具
   ```
   jmap -heap <pid>
   ```
   查看堆内存配置和使用情况
   
   ```
   jmap -histo:live <pid>
   ```
   查看堆中对象统计信息（按类）
   
   ```
   jmap -dump:format=b,file=heap.hprof <pid>
   ```
   生成堆转储文件(Heap Dump)

5. **jhat** - 堆分析工具
   ```
   jhat heap.hprof
   ```
   分析堆转储文件(启动Web服务，默认端口7000)

## 线程分析命令

6. **jstack** - 线程堆栈工具
   ```
   jstack <pid>
   ```
   获取Java进程的线程堆栈信息
   
   ```
   jstack -l <pid>
   ```
   获取线程堆栈信息(包含锁信息)

## 高级分析工具

7. **VisualVM**
   - 图形化工具，集成了多种监控和分析功能
   - 远程连接需要配置JMX

8. **JConsole**
   - JMX 客户端，提供基本的监控功能

9. **Arthas** (阿里开源)
   - 强大的在线诊断工具
   - 支持热修复、方法调用监控等高级功能

10. **MAT (Memory Analyzer Tool)**
    - 专业的堆内存分析工具
    - 可以分析内存泄漏问题

## 常用组合命令

- 查找Java进程并查看GC情况:
  ```
  jps | grep <关键字> | awk '{print $1}' | xargs jstat -gcutil
  ```

- 查找高CPU线程并分析:
  ```
  top -Hp <pid>
  jstack <pid> | grep -A 20 <nid>
  ```

这些命令和工具可以帮助开发者和运维人员有效地监控和分析JVM运行状态，诊断内存泄漏、线程阻塞、CPU过高等常见问题。