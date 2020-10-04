
### IO流部分
#### IO流常用的有：字符流、字节流、缓冲流、序列化流、RandomAccessFile类等

#### 1、字节流

##### 常用于操作文件

- FileInputStream/FileOutputStream

- BufferedInputStream/BufferedOutputStream



#### 2、字符流

- InputStreamReader / OutputStreamWriter

- BufferedReader / BufferedWriter

- FileReader / FileWriter

- 其中**BufferedReader / BufferedWriter**也称为 **字符缓冲流** ，可以一次读一行，一次写一行；**FileReader / FileWriter**是从**InputStreamReader / OutPutStreamWriter**继承而来，**InputStreamReader / OutputStreamWriter、BufferedReader / BufferedWriter**是继承自**Reader /Writer**;



#### 3、缓冲流（字节流下的缓冲流）

- BufferedInputStream / BufferedOutputStream
- 缓冲流是属于字节流的

#### 4、RandomAccessFile类

- RandomAccessFile类从字面意思来看就是随机写入写出，也就是说这个类有可以写入和写出两种方法；



#### 5、对象的反序列化流、序列化流（ObjectOutputStream、ObjectInputStream）

- 序列化流、反序列化流涉及到序列化接口（serializable）,想要实现对象的序列化和反序列化，该对象必须继承序列化接口（即implements Serializable)

- 注意：所有的流在完成操作后都需要执行关闭流的操作（即close()方法），同时对于输入流要进行刷新（即flush()方法）操作；


#### 6、DataInputStream / DataOutputStream

- 数据输入流，数据输出流
