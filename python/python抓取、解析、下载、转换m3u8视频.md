# python抓取、解析、下载、转换m3u8视频

### 前言





### 知识扩展

在开始抓取`m3u8`视频之前，我们先了解下`m3u8`的相关知识，了解的更多，可以让我们少走弯路。

#### m3u8是什么？

在此之前，我仅仅知道`m3u8`是一种网络串流，在平时娱乐时候会找一些`m3u8`的资源，看看直播啥的，直到今天要分享`m3u8`的相关内容，才真正开始搜集`m3u8`的相关知识点。关于`m3u8`连百度百科都没有说明，搜到知乎一篇内容（【全网最全】m3u8到底是什么格式？一篇文章搞定m3u8下载），下面的原理图也是参照的这篇内容：

![](https://gitee.com/sysker/picBed/raw/master/images/20211023154111.png)

从上面的原理图中我们可以得到以下知识点：

- 首先`m3u8`并非是视频格式，而是视频文件的索引。
- `ts`文件才是我们真正播放的视频资源

`m3u8`通常分两种格式，一种是单码率（固定分辨率），一种是多码率（包含多种分别率）。下面就是一个单码率的`m3u8`文件的内容：

```
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:10
#EXT-X-MEDIA-SEQUENCE:1619459525
#EXT-X-PROGRAM-DATE-TIME:2021-10-23T05:39:42Z
#EXTINF:10.0,
1634967582-1-1619459525.hls.ts
#EXT-X-PROGRAM-DATE-TIME:2021-10-23T05:39:52Z
#EXTINF:10.0,
1634967592-1-1619459526.hls.ts
#EXT-X-PROGRAM-DATE-TIME:2021-10-23T05:40:02Z
#EXTINF:10.0,
1634967602-1-1619459527.hls.ts
```

这个就是一个多码率的`m3u8`文件，从多码率的文件格式可以看出来，多码率中包括了多个单码率是`m3u8`文链接：

```
#EXTM3U
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=500000,RESOLUTION=480x270
500kb/hls/index.m3u8
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=300000,RESOLUTION=360x202
300kb/hls/index.m3u8
```

##### m3u8文件指令

另外我在另外一篇博客发现`m3u8`其实是`m3u`文件的扩展（参考文档`2`），这可能就是为什么没有找到`m3u8`相关词条的原因吧，同时在`m3u`的词条中发现了`M#U`文件的指令描述（每个字段的含义）：

```makefile
#EXTM3U //必需，表示一个扩展的m3u文件

#EXT-X-VERSION:3 //hls的协议版本号，暗示媒体流的兼容性

#EXT-X-MEDIA-SEQUENCE:xx //首个分段的sequence number

#EXT-X-ALLOW-CACHE:NO //是否缓存

#EXT-X-TARGETDURATION:5 //每个视频分段最大的时长（单位秒）

#EXT-X-DISCONTINUITY //表示换编码

#EXTINF: //每个切片的时长
```

另外关于`m3u`的文件指令是有国际标准的，感兴趣的小伙伴可以去看下：

```
http://tools.ietf.org/html/draft-pantos-http-live-streaming-06
```

好了，关于`m3u8`的相关内容，我们就说这么多，感兴趣的小伙伴可以自己继续探索，下面我们看下如何用`python`抓取、解析和下载`m3u8`文件索引中的视频文。



### 抓取、解析、下载

首先我们先要拿到目标视频资源的索引文件，也就是`m3u8`文件。一般稍微懂点`web`开发的小伙伴，应该都知道浏览器抓包吧，`F12`打开浏览器控制台，然后选择`Network`，刷新下页面，在左侧资源区找到`index.m3u8`文件。

通常会有两个`m3u8`，第一个是获取视频码率列表的，也就是多码率`m3u8`，这个文件我们是没办法直接解析的，我们要找的是包含`ts`视频资源的`m3u8`文件。这里我随便在网上搜了一个葫芦娃的视频，然后通过控制台拿到`m3u8`文件地址：

![](https://gitee.com/sysker/picBed/raw/master/images/20211023161658.png)

```
https://vod1.bdzybf1.com/20200819/wMgIH6RN/1000kb/hls/index.m3u8
```

下面我们就用`python`解析下载这个视频文件。

#### 解析m3u8文件

解析`m3u8`文件最核心的地方是分析`m3u8`的文件结构，然后根据其文件内容写出对应的解析逻辑。这里我推荐直接用`requests`库模拟调用，然后分析响应结果，因为用文本工具之类的查看`m3u8`文件的话，换行符`\n`、制表符`\t`这些看起来不够直观，但是`requests`就不会有这个问题，因为我们解析的就是`requests`的响应结果。

这里的以我们上面`m3u8`文件为例响应结果如下：

![](https://gitee.com/sysker/picBed/raw/master/images/20211023164625.png)

可以清晰地看出，这个`m3u8`文件是通过换行符`\n`分割的，有部分`m3u8`文件中会出现制表符和换行符组合的情况，所以具体情况具体分析。

另外，我从响应内容中发现，这个视频资源是进行了`AES-128`加密的，所以后面在下载视频资源的时候要解密。

##### 解析ts视频地址

因为`python`代码都很简单，代码量也不多，所以就不展开讲了，看代码注释应该可以看懂。这个方法主要是为了获取`ts`视频文件的地址。

```python
import requests

def getTsFileUrlList(m3u8Url):
    # 组装请求头
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
            }
    # 请求 m3u8文件，并拿到文件内容
    ts_rs = requests.get(url = m3u8Url, headers=headers).text
    print(ts_rs)
    # 换行符分割文件内容
    list_content = ts_rs.split('\n');
    print('list_content:{}'.format(list_content))
    player_list = []
    # 循环分割结果
    for line in list_content:
      # 以下拼接方式可能会根据自己的需求进行改动
      if '#EXTINF' in line:
        continue;
      # 仅记录 ts文件地址  
      elif line.endswith('.ts'):
        player_list.append(line)
    print('数据列表组装完成-size: {}'.format(len(player_list)));
    return player_list;
```

运行上面这个方法的话，最终会获取到`m3u8`索引文件中所有的`ts`视频地址，但是由于我们刚才已经从`m3u8`文件中发现了，视频资源是加密的，所以在下载的时候我们需要解密。

#### 下载文件

下载并解密视频资源，这里我加了一个解密操作

```python
def fileDownloadWithdecrypt(fileSavePath, player_list):
    # 创建文件夹
    if not os.path.exists(fileSavePath):
        os.mkdir(fileSavePath);
    # 循环 ts 视频资源列表
    for index, url in enumerate(player_list):
        # 发送下载请求
        ts_video = requests.get(url = url, headers=headers)
        # 保存文件
        with open('{}/{}.ts'.format(fileSavePath, str(index + 1)), 'wb') as file:
            # 视频资源解密
            context = decrypt(ts_video.content);
            # 文件写入
            file.write(context)
            print('正在写入第{}个文件'.format(index + 1))
    print('下载完成');
```

下面是解密代码

```python
from Crypto.Cipher import AES   # 用于AES解码

def decrypt(context):
    # 加密的key
    key =  b'2cd1da2aedacaec8';
    # 解密
    cryptor = AES.new(key, AES.MODE_CBC, key);
    decrypt_content = cryptor.decrypt(context);
    return decrypt_content;
```

这里用的是`pycryptodome`库，安装方式如下：

```
 pip3 install pycryptodome
```

关于密文，在`m3u8`文件里面已经有了，直接下载就可以拿到，这里我就不通过代码拿了：

![](https://gitee.com/sysker/picBed/raw/master/images/20211023175827.png)

这里下载视频会比较费时间，为了提高下效率可以用多线程，但是由于时间的关系就不演示了。



#### 合并视频



##### 参考内容

[^1]: https://zhuanlan.zhihu.com/p/346683119
[^2]: https://www.cnblogs.com/shakin/p/3870439.html



