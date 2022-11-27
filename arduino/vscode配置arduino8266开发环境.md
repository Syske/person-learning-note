
### vscode配置arduino环境

 这里再补充下`vscode arduino`开发环境的设置。

 1. 确保本地安装了`arduino`环境
 2. 打开`vscode`，安装`arduino`扩展：
   
    ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221127194308.png)

 3. 配置`arduino`环境。打开`vscode`设置（快捷键`ctrl+,`），找到`arduino configuration`:
   
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

4. 打开一个已经创建好的`arduino`项目，初始化配置。

    ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20221127200225.png)