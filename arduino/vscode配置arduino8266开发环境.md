### vscode配置arduino环境

 这里再补充下`vscode arduino`开发环境的设置。

#### 前期准备

- 确保本地安装了`arduino`环境
- 打开`vscode`，安装`arduino`扩展：
   
    ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221127194308.png)

#### 添加配置

- 配置`arduino`环境。打开`vscode`设置（快捷键`ctrl+,`），找到`arduino configuration`:
   
    ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221127194731.png)

    首先配置`arduino`的安装目录，这个目录就是`arduino`的安装根目录（可以看到`arduino_debug.exe`）：

    ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221127195004.png)

    配置`command Path`和波特率：

    ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221127195152.png)


    当然，这里你也可以直接打开`seting.config`进行配置：

    ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221127195548.png)

    ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221127195614.png)

    这里附上我的完整配置：

```json
    {
        "arduino.path": "D:\\workspace\\dev-tools\\arduion-tools\\arduino-nightly",
        "arduino.commandPath": "arduino_debug.exe",
        "arduino.logLevel": "info",
        "arduino.allowPDEFiletype": false,
        "arduino.enableUSBDetection": true,
        "arduino.disableTestingOpen": false,
        "arduino.skipHeaderProvider": false,
        "arduino.additionalUrls": [
            "https://raw.githubusercontent.com/VSChina/azureiotdevkit_tools/master/package_azureboard_index.json",
            "http://arduino.esp8266.com/stable/package_esp8266com_index.json"
        ],
        "arduino.defaultBaudRate": 115200,
        "[python]": {
            "editor.formatOnType": true
        }
    }
```

#### 项目初始化

- 打开一个已经创建好的`arduino`项目，初始化配置。

    ![修改配置](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221127200225.png)


- 之后创建新的`arduino`项目，首次编译时会自动创建相关环境文件

    ![环境配置](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221205000208.png)

### 遇到的问题

如果你注意留意上面截图的话，会发现控制台报错了：

   ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221129214414.png)


对于这个错误，我找了很多资料，但是并没有找到和我一样的问题，最终在一次偶然的调试过程中，我找到了问题——开发板`exceptions`设置问题：

![发现问题](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221129214829.png)


默认情况下`exceptions`的设置`Legay(new can return nullptr)`，从上面的截图可以看到控制台提示的是非法的设置，说明是因为控制板de`exceptions`设置不正确，这里选择`Enabled`，然后再次运行就可以看到具体的错误信息，如果代码没有编译错误，可以直接看到成功提示：

![编译错误](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221129215720.png)

![编译成功](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221129220011.png)


如果在上传代码过程中报错，需要检查串口监听是否关闭：

![串口被占用](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221130003959.png)