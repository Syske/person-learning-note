近期，接到一个新的需求，涉及到文件下载，因为我的服务全是发在内网的，项目又是完全的前后端分离的，前端服务通过nginx转发到外网，而且我的文件是传到内网文件服务器的，所以如何下载文件成为这个问题的难点。因为之前做过图片base64传输的需求，所以我首先想到的就是同时base64传输，然后前端将base64转成文件下载，查询了很多资料和博客，踩了很多坑，然后就有了这篇文章。

### 原理

先说思路，然后我们再贴代码，具体流程如下图：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200417102811.png)

用户发出文件访问请求时，nginx将请求转发至内网前端服务，然后前端服务访问后端接口，后端接口根据用户请求的文件名，请求文件服务器，并将文件转换成base64字符串返回给前端，前端将base64还原成文件，然后模拟下载。

### 代码实现

原理很简单，接下来我们看下如何实现：

#### 前端代码

按照流程，我们先看前端代码，核心代码还是js:

```js
 function clickBt() {
        console.log("网页加载完毕");
        $.ajax({
            type:"POST",
            url: "file/download",
            data: {fileName:"myfile.pdf"},
            success: function (data) {
             var downLoad =  $('#download');
                console.log("base64:" , data);
                console.log("msg:",data.msg)
                console.log("success:",data.success)
                if (data.success) {
                    var blob = b64toBlob(data.obj, "application/pdf");
                    console.log(blob);
                    var url = window.URL.createObjectURL(blob);
                    console.log('url:', url);
                    downLoad.attr("href", url);
                    dataURLtoFile(url, "test.pdf");
                } else {
                    alert("获取文件失败：", data.msg);
                }
            }
        });
    }
   /***
     * 下载文件
     * @param blobUrl：blob文件链接，例如：blob:http://localhost:8081/283340bd-f3c5-49d9-a3ac-b9e48ea08228
     * @param filename: 保存的文件名
     * */
    function dataURLtoFile(blobUrl, filename) {//将base64转换为文件
            var eleLink = document.createElement('a')
            eleLink.download = filename
            eleLink.style.display = 'none'
            eleLink.href = blobUrl
            // 触发点击
            document.body.appendChild(eleLink)
            eleLink.click()
            // 然后移除
            document.body.removeChild(eleLink);
    }

    /**
     * base64转Blob
     * @param b64Data：base64字符串，不含类型，如：JVBERi0xLjQKJeLjz9MKNCAwIG9iago8P……
     * @param contentType：类型，比如："application/pdf"
     * @param sliceSize
     * @returns {Blob}
     */
    function b64toBlob(b64Data, contentType, sliceSize) {
        contentType = contentType || '';
        sliceSize = sliceSize || 512;

        var byteCharacters = window.atob(b64Data);
        console.log("byteCharacters:",byteCharacters)
        var byteArrays = [];

        for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
            var slice = byteCharacters.slice(offset, offset + sliceSize);

            var byteNumbers = new Array(slice.length);
            for (var i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
            }

            var byteArray = new Uint8Array(byteNumbers);

            byteArrays.push(byteArray);
        }

        var blob = new Blob(byteArrays, { type: contentType });
        console.log("blob", blob)
        return blob;
    }
```

#### data类型

这里是文件类型：

| 序号 | 文件类型 | data类型                                                     |
| ---- | -------- | ------------------------------------------------------------ |
| 1    | txt      | data:text/plain;base64,                                      |
| 2    | doc      | data:application/msword;base64,                              |
| 3    | docx     | data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64, |
| 4    | xls      | data:application/vnd.ms-excel;base64,                        |
| 5    | xlsx     | data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64, |
| 6    | pdf      | data:application/pdf;base64,                                 |
| 7    | pptx     | data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64, |
| 8    | ppt      | data:application/vnd.ms-powerpoint;base64,                   |

如果是图片的额话：

| 序号 | 图片类型 | data类型                   |
| ---- | -------- | -------------------------- |
| 1    | png      | data:image/png;base64,     |
| 2    | jpg      | data:image/jpeg;base64,    |
| 3    | gif      | data:image/gif;base64,     |
| 4    | svg      | data:image/svg+xml;base64, |
| 5    | ico      | data:image/x-icon;base64,  |
| 6    | bmp      | data:image/bmp;base64,     |

#### 后端代码

##### controller

```java
@Api(value = "file", description = "文件管理")
@Controller
@RequestMapping("/file")
public class FileManagerController {

    @Value("${my.fileServer.url}") // http://127.0.0.1/file-Server/
    private String remotUrl;

    @RequestMapping("/download")
    @ResponseBody
    public AjaxJson downLoad(String fileName) {
        if(StringUtils.isEmpty(fileName)) {
            return new AjaxJson(new Exception("文件名不能为空"));
        }
        String base64 = Base64Util.remotePdfToBase64(remotUrl + fileName);
        AjaxJson result = new AjaxJson("请求成功", true);
        result.setObj(base64);
        return result;
    }

}
```

base64工具类：

```java
public class Base64Util {
	private transient static Logger log = LoggerFactory.getLogger(Base64Util.class);

    /**
     * <p>将base64字符解码保存文件</p>
     * @param base64Code
     * @param targetPath
     * @throws Exception
     */
    public static void decoderBase64File(String base64Code,String targetPath) throws Exception {
        byte[] buffer = new BASE64Decoder().decodeBuffer(base64Code);
        FileOutputStream out = new FileOutputStream(targetPath);
        out.write(buffer);
        out.close();
    }

    /**
     *  将base64编码转换成PDF
     *  @param base64String
     *  1.使用BASE64Decoder对编码的字符串解码成字节数组
     *  2.使用底层输入流ByteArrayInputStream对象从字节数组中获取数据；
     *  3.建立从底层输入流中读取数据的BufferedInputStream缓冲输出流对象；
     *  4.使用BufferedOutputStream和FileOutputSteam输出数据到指定的文件中
     */
    public static void base64StringToPDF(String base64String, File file){
        BASE64Decoder decoder = new BASE64Decoder();
        BufferedInputStream bin = null;
        FileOutputStream fout = null;
        BufferedOutputStream bout = null;
        try {
            //将base64编码的字符串解码成字节数组
            byte[] bytes = decoder.decodeBuffer(base64String);
            //创建一个将bytes作为其缓冲区的ByteArrayInputStream对象
            ByteArrayInputStream bais = new ByteArrayInputStream(bytes);
            //创建从底层输入流中读取数据的缓冲输入流对象
            bin = new BufferedInputStream(bais);
            //创建到指定文件的输出流
            fout  = new FileOutputStream(file);
            //为文件输出流对接缓冲输出流对象
            bout = new BufferedOutputStream(fout);

            byte[] buffers = new byte[1024];
            int len = bin.read(buffers);
            while(len != -1){
                bout.write(buffers, 0, len);
                len = bin.read(buffers);
            }
            //刷新此输出流并强制写出所有缓冲的输出字节，必须这行代码，否则有可能有问题
            bout.flush();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                bout.close();
                fout.close();
                bin.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    /**
     * PDF转换为Base64编码
     * @param file
     * @return
     */
    public static String remotePdfToBase64(String file) {
        BASE64Encoder encoder = new BASE64Encoder();
        InputStream fin =null;
        BufferedInputStream bin =null;
        ByteArrayOutputStream baos = null;
        BufferedOutputStream bout =null;
        try {
            URL url = new URL(file);
            fin = url.openStream();
            bin = new BufferedInputStream(fin);
            baos = new ByteArrayOutputStream();
            bout = new BufferedOutputStream(baos);
            byte[] buffer = new byte[1024];
            int len = bin.read(buffer);
            while(len != -1){
                bout.write(buffer, 0, len);
                len = bin.read(buffer);
            }
            //刷新此输出流并强制写出所有缓冲的输出字节
            bout.flush();
            byte[] bytes = baos.toByteArray();
            return encoder.encodeBuffer(bytes).trim();

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                if (fin != null)
                    fin.close();
                if (bin != null)
                    bin.close();
                if (baos != null)
                    baos.close();
                if (bout != null)
                    bout.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return null;
    }


    public static void main(String[] args) {
        try {
            String base64Code =remotePdfToBase64("http://127.0.0.1/file-Server/myfile.pdf");
            log.info(base64Code);
            decoderBase64File(base64Code, "D://z2.pdf");
            base64StringToPDF(base64Code, new File("D://z3.pdf"));
            //toFile(base64Code, "D://z.pdf");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
	
}
```

### 总结

以上代码即可实现前后端分离项目得文件下载，如果需要兼容IE，需要考虑IE下兼容base64和blob文件格式，因为后来需要pdf文件预览，也就没有深入研究。随后我会发出pdf文件预览的相关解决方案，360兼容模式可用。