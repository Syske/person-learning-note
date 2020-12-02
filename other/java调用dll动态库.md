# java通过JNA调用动态库

### 前言

老规矩，先说下为什么会有这篇文章。近期对接了一个项目，应接口提供方要求，必须通过动态库调用，一个是为了安全可控，调用方不用知道内部实现，加密、解密、具体的逻辑不需要考虑，只需要调用即可；另一个是封装了统一的GUI界面。总之就是非用动态库不可，然后我查了很多资料，请教了几个大佬，最后在运气的加持下，终于调通了，但整个过程特别坎坷，所以我觉有必要记录下。需要说明的是我们这里采用的是JNA的方式

### 什么是动态库

说实话，一般我们不会有调用动态库的需求，因为这不是web开发的范畴，出发你涉及到嵌入式的开发，或者客户端开发。动态库也叫动态链接库，英文简写DLL，简单来讲，就是Windows下开发的程序模块，类似于java下的jar(不知道可不可以这样 理解)。它是实现Windows应用程序共享资源、节省内存空间、提高使用效率的一个重要技术手段。windows下它是以dll结尾的文件，比如:`msctf.dll`

百度百科给的解释是这样的：

> 动态链接库英文为***DLL\***，是**Dynamic Link Library**的缩写。DLL是一个包含可由多个程序，同时使用的代码和数据的库。在[Windows](https://baike.baidu.com/item/Windows/165458)中，这种文件被称为应用程序拓展。例如，在 [Windows](https://baike.baidu.com/item/Windows) 操作系统中，[Comdlg32.dll](https://baike.baidu.com/item/Comdlg32.dll) 执行与对话框有关的常见函数。因此，每个程序都可以使用该 DLL 中包含的功能来实现“打开”对话框。这有助于避免代码重用和促进内存的有效使用。 通过使用 DLL，程序可以实现模块化，由相对独立的组件组成。例如，一个计账程序可以按模块来销售。可以在运行时将各个模块加载到主程序中（如果安装了相应模块）。因为模块是彼此独立的，所以程序的加载速度更快，而且模块只在相应的功能被请求时才加载。

咱也不是特别知道，咱也不敢问，你现在只有保证知道动态库这样的东西就行了。

### 开整

Talk is cheap. Show me the code。先上代码，然后再解释

```java
public class DllTest {
    static {
        String filePath = "D:\\dll\\"; // 这里是你的动态库所在文件夹的绝对路径
        // 这里引用动态库和他的依赖
        System.load(filePath + "mfc100.dll");   
        System.load(filePath + "mydll.dll");        
    }

    public static void main(String[] args) {
        String strUrl = "http://127.0.0.1/test";
        String InData = "{\"data\":{\"operatorId\":\"test001\",\"operatorName\":\"超级管理员\",\"orgId\":\"123\"},\"orgId\":\"1232\"}";
        byte[] OutData = new byte[1024];

        String msg = CLibrary.INSTANCE.test(strUrl.getBytes(), InData.getBytes(), OutData);
        System.out.println(msg);
        try {
            System.out.println(new String(OutData, "GBK"));
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }

    }
    // 这里是最关键的地方
    public interface CLibrary extends Library {
        // FS_CheckCode是动态库名称，前面的d://test//是路径
        CLibrary INSTANCE = (CLibrary) Native.loadLibrary("mydll", CLibrary.class);

        // 我们要调用的动态库里面的方法。
        String test(byte[] strUrl, byte[] InData, byte[] OutData);
    }
}
```

动态库里面的方法是这么定义的：

```c
char* __stdcall test(char* strUrl,char* InData,char* OutData)
```

### 解释

小朋友，你是否有很多的问号❓😂没事，接下来我们就详细说明下。首先要关注的是java定义动态库接口方法，对应代码：

```java
public interface CLibrary extends Library {
        // FS_CheckCode是动态库名称，前面的d://test//是路径
        CLibrary INSTANCE = (CLibrary) Native.loadLibrary("mydll", CLibrary.class);

        // 我们要调用的动态库里面的方法。
        String test(byte[] strUrl, byte[] InData, byte[] OutData);
    }
```

其中，loadLibrary方法是创建动态库对象实例，第一入参是你要调用的动态库的名字，test方法对应动态库中的方法，这里需要注意的是jNA和动态库直接数据类型的对应关系，具体的对应看后面的附表。

这里还有一个需要注意的问题是是，动态库加载的问题：

```java
// 这里引用动态库和他的依赖
        System.load(filePath + "mfc100.dll");   
        System.load(filePath + "mydll.dll"); 
```

如果你没有把动态库放到classpath下，而且没有上面加载的代码，会报如下错误：

```sh
Exception in thread "main" java.lang.UnsatisfiedLinkError: Unable to load library 'NationECCode':
找不到指定的模块。
```

### 遇到的问题

#### JDK版本

如果完成了相应改造工作，你就可以直接运行了。如果你的JDK是64位，但你的动态库是32位（X86），它肯定会报如下错误：

```shell
java.lang.UnsatisfiedLinkError: D:\workspace\learning\github\httputil-demo\dll\mydll.dll: Can't load IA 32-bit .dll on a AMD 64-bit platform
	at java.lang.ClassLoader$NativeLibrary.load(Native Method)
	at java.lang.ClassLoader.loadLibrary0(ClassLoader.java:1941)
	at java.lang.ClassLoader.loadLibrary(ClassLoader.java:1824)
	at java.lang.Runtime.load0(Runtime.java:809)
	at java.lang.System.load(System.java:1086)
```

或者这样：

```java
Exception in thread "main" java.lang.UnsatisfiedLinkError: %1 不是有效的 Win32 应用程序。

	at com.sun.jna.Native.open(Native Method)
	at com.sun.jna.NativeLibrary.loadLibrary(NativeLibrary.java:278)
	at com.sun.jna.NativeLibrary.getInstance(NativeLibrary.java:455)
	at com.sun.jna.Library$Handler.<init>(Library.java:179)
	at com.sun.jna.Native.loadLibrary(Native.java:646)
	at com.sun.jna.Native.loadLibrary(Native.java:630)
```

当然如果你的动态库是64位，JDK是32位(X86)，同样也会报错（应该会，没试过）

解决方法很简单：

- 更换JDK版本
- 联系动态库封装的人，重新封装对应的版本

#### 找不到模块

这个问题上面已经说过了，就是因为没有加载动态库文件，而且也没有把它和它的依赖文件放到classpath下，就会报这个错。

#### 数据类型错误

这个问题本质上就是没有搞清楚JNA和动态库数据对应关系，我之前也没搞清楚，反复试了好多次才成功。然后在今天写这篇文章的时候，发现了`char*`作为出参和入参对应的类型是不一样的，才恍然大悟。希望小伙伴在自己搞的时候一定看清楚。

#### 出参未分配空间

和java不一样，动态库方法是把入参传给方法的，而且需要给出参分配空间，如果不分配内存空间，会报错：

```java
 java.lang.Error: Invalid memory access
```

这个问题也很好解决，就是给出参分配足够的空间：

```java
byte[] OutData = new byte[1024];
```

到这里，所有问题都解决了，动态库也完美运行起来了。

### 总结

收获就一句话：对于自己没有做过的事，要积极尝试，积极思考，积极请教，然后问题解决后要积极分享。好了，祝大家周末愉快！



JNA和动态库类型之间的映射关系：

| Native Type | Size                | Java Type  | Common Windows Types    |
| ----------- | ------------------- | ---------- | ----------------------- |
| char        | 8-bit integer       | byte       | BYTE, TCHAR             |
| short       | 16-bit integer      | short      | WORD                    |
| wchar_t     | 16/32-bit character | char       | TCHAR                   |
| int         | 32-bit integer      | int        | DWORD                   |
| int         | boolean value       | boolean    | BOOL                    |
| long        | 32/64-bit integer   | NativeLong | LONG                    |
| long long   | 64-bit integer      | long       | __int64                 |
| float       | 32-bit FP           | float      |                         |
| double      | 64-bit FP           | double     |                         |
| char*       | C string            | String     | LPCSTR                  |
| void*       | pointer             | Pointer    | LPVOID, HANDLE, LP*XXX* |

补充表：

<table>
<thead>
<tr>
<th style="text-align:center">Native Type</th>
<th style="text-align:center">Java Type</th>
<th style="text-align:center">Native Representation</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center">char</td>
<td style="text-align:center">byte</td>
<td style="text-align:center">8-bit integer</td>
</tr>
<tr>
<td style="text-align:center">wchar_t</td>
<td style="text-align:center">char</td>
<td style="text-align:center">16/32-bit character</td>
</tr>
<tr>
<td style="text-align:center">short</td>
<td style="text-align:center">short</td>
<td style="text-align:center">16-bit integer</td>
</tr>
<tr>
<td style="text-align:center">int</td>
<td style="text-align:center">int</td>
<td style="text-align:center">32-bit integer</td>
</tr>
<tr>
<td style="text-align:center">int</td>
<td style="text-align:center">boolean</td>
<td style="text-align:center">32-bit integer (customizable)</td>
</tr>
<tr>
<td style="text-align:center">long, __int64</td>
<td style="text-align:center">long</td>
<td style="text-align:center">64-bit integer</td>
</tr>
<tr>
<td style="text-align:center">long long</td>
<td style="text-align:center">long</td>
<td style="text-align:center">64-bit integer</td>
</tr>
<tr>
<td style="text-align:center">float</td>
<td style="text-align:center">float</td>
<td style="text-align:center">32-bit FP</td>
</tr>
<tr>
<td style="text-align:center">double</td>
<td style="text-align:center">double</td>
<td style="text-align:center">64-bit FP</td>
</tr>
<tr>
<td style="text-align:center">pointer</td>
<td style="text-align:center">Buffer/Pointer</td>
</tr>
<tr>
<td style="text-align:center">pointer array</td>
<td style="text-align:center">[] (array of primitive type)</td>
</tr>
<tr>
<td style="text-align:center">char*</td>
<td style="text-align:center">String</td>
</tr>
<tr>
<td style="text-align:center">wchar_t*</td>
<td style="text-align:center">WString</td>
</tr>
<tr>
<td style="text-align:center">char**</td>
<td style="text-align:center">String[]</td>
</tr>
<tr>
<td style="text-align:center">wchar_t**</td>
<td style="text-align:center">WString[]</td>
</tr>
<tr>
<td style="text-align:center">void*</td>
<td style="text-align:center">Pointer</td>
</tr>
<tr>
<td style="text-align:center">void **</td>
<td style="text-align:center">PointerByReference</td>
</tr>
<tr>
<td style="text-align:center">int&amp;</td>
<td style="text-align:center">IntByReference</td>
</tr>
<tr>
<td style="text-align:center">int*</td>
<td style="text-align:center">IntByReference</td>
</tr>
<tr>
<td style="text-align:center">struct</td>
<td style="text-align:center">Structure</td>
</tr>
<tr>
<td style="text-align:center">(*fp)()</td>
<td style="text-align:center">Callback</td>
</tr>
<tr>
<td style="text-align:center">varies</td>
<td style="text-align:center">NativeMapped</td>
</tr>
<tr>
<td style="text-align:center">long</td>
<td style="text-align:center">NativeLong</td>
</tr>
<tr>
<td style="text-align:center">pointer</td>
<td style="text-align:center">PointerType</td>
</tr>
</tbody>
</table>

然后又找到一些补充资料：

| C语言          | Java                                                         |
| -------------- | ------------------------------------------------------------ |
| char*          | String （作为入口参数）/ byte[] (作为出口参数)               |
| unsigned char* | String （作为入口参数）（不确定，没具体使用过）/ Pointer （作为出口参数） |
| int*           | IntByReference                                               |