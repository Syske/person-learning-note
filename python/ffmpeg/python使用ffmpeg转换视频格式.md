# ffmpeg转换视频格式

#python #ffmpeg

## 前言


## 视频格式转换

### 准备工作

这里我们用到的工具是`ffmpeg`，这个工具非常强大。

#### 安装配置`ffmpeg`



下载地址
```
https://www.gyan.dev/ffmpeg/builds/
```
选择任意版本均可，因为我们这里只用到`bin`目录下的`exe`，所以只需要下载基本版本即可：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20231003091119.png)

然后解压，并配置环境变量：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20231003091322.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20231003091441.png)

安装配置完成之后，可以通过`ffmpeg`命令测试下配置是否正常：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20231003091935.png)


#### 安装ffmpeg-python

```sh
pip install ffmpeg-python
```

### 编写代码

```python
import ffmpeg

input_file = 'sunraise1.avi'
output_file = 'sunraise1.mp4'

input_stream = ffmpeg.input(input_file)
output_stream = ffmpeg.output(input_stream, output_file)

ffmpeg.run(output_stream)
```

如果`ffmpeg`环境配置有问题，就会在运行时提示文件不存在：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20231003091806.png)

上面的这段代码，等同于下面行命令：
```sh
ffmpeg -i sunraise1.avi sunraise1.avi
```

需要注意的是，`ffmpeg`默认的编码是`h264`，所以转码之后的视频需要通过支持`h264`的播放器进行播放：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20231003092312.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20231003092447.png)

手动合并视频：

```sh
ffmpeg -loglevel quiet -f concat  -safe 0  -i 凶案深处-第01集.txt -vcodec copy -acodec copy 第01集.mp4
```
需要注意的是，这里的`txt`文件中的路径，如果是相对路径，则必须要是相对于`txt`文件的路径：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20231211225106.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20231211225211.png)

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20231211225302.png)
