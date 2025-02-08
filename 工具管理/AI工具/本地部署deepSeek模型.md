### 前言

春节期间，我一直持续关注`DeepSeek AI`模型的技术动态，在很多技术推送内容中发现了多个本地化部署的实践方案，本着研究学习的想法，我准备在本地做一次部署实践，同时以实操日志的形式，完整记录从零部署`DeepSeekAI`的全过程，期待为各位小伙伴提供一份经过验证的部署指南。

本次实践将涵盖环境配置、依赖项安装、参数调优等关键环节，过程中遇到的典型报错及解决方案也将一并整理说明。

我本地的环境是`win11 + WSL`，电脑配置：
- 运行内存`16GB`
- 集成显卡
同样的操作我在`arch-linux`也是操作成功的，下面就让我们开始整个过程：

### 模型选择和下载

这里需要科学上网，然后选择适合自己的模型：

```
https://huggingface.co/deepseek-ai/
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/f3d0a0ba-4e1f-42a0-9a9e-85708e59667b.jpg)

因为我的笔记本电脑配置不高（`16GB ROM`，集成显卡），所以我选择的是`DeepSeek-R1-Distill-Qwen-1.5B`：

```
https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
```
然后通过`git`进行克隆：

```sh
# 从Hugging Face下载模型
# 安装git大文件插件
git lfs install
# 克隆模型文件
git clone https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
```

虽然科学上网了，但是我始终没有克隆成功，最后发现仓库文件不多，所以就挨个手动下载到本地：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/9b5320a2-0091-4860-a331-fc33ac6562c8.jpg)
有条件的铁子可以自己下载，没有条件的铁子可以用我提供的，下载连接附后面。



### 工具准备

#### 安装python依赖

这里的依赖是为了后面量化和运行模型：

```sh
pip install transformers numpy torch sentencepiece
```

#### 下载编译llama工具

`llama`是量化和运行`AI`模型的工具，首先要配置编译环境：
```sh
# Ubuntu/Debian
sudo apt install cmake
# macOS
brew install cmake
```

然后，克隆`llama`源码进行编译：
```sh
# 克隆仓库
git clone https://github.com/ggerganov/llama.cpp
# 国内推荐gitee，但是不是最新版本：
# https://gitee.com/heismart/llama.cpp.git
cd llama.cpp

# 创建构建目录
mkdir build
cd build

# 配置 CMake（默认启用 CPU 优化）
cmake .. -DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS
```
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/50df032e-91ba-414e-940d-b2debc1584c9.jpg)

配置完成后开始编译

```sh
# 开始编译（根据CPU核心数调整-j后的数字）
cmake --build . --config Release -j 4
```
如下提示说明编译完成：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/8ee6be37-0fd3-40d6-94d0-829096d6536c.jpg)


### 模型的转换、量化和运行

这里需要注意模型文件夹的路径，我的模型文件和`llama.cpp`在同一级目录下，模型和工具压缩包直接解压就行，链接附后面：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/ea0775e0-ca37-4af0-80b5-e3fa256d8d60.jpg)

#### 模型转换

这里需要注意的是不同版本会有差异，最新版本转换脚本有多个，需要根据自己的需要选择。

转换为 `FP16 `格式：

```sh
cd llama.cpp

python3 convert_hf_to_gguf.py \
    ../DeepSeek-R1-Distill-Qwen-1.5B \
    --outfile deepseek-r1-1.5b.f16.gguf \
    --outtype f16
```
如下提示表示模型转换成功：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/af6ad276-8652-4b1c-b819-3bd3f5b8c8d9.jpg)

原模型下载下来是`3.3G`，转换完成后会在当前目录下（`llama.cpp`）生成一个`deepseek-r1-1.5b.f16.gguf`文件

#### 模型量化

```sh
# 还是上面的目录，没有新开窗口不需要切换
cd llama.cpp
# 执行量化命令
./build/bin/llama-quantize deepseek-r1-1.5b.f16.gguf deepseek-r1-1.5b.q4_0.gguf q4_0
```

简单解释下上面的量化命令：
- `llama-quantize`是我们`llama`的量化命令，在老版本下是`quantize`
- `deepseek-r1-1.5b.f16.gguf`是我们要量化的模型
- `deepseek-r1-1.5b.q4_0.gguf`表示我们量化后生成的文件
- `q4_0`表示量化参数，不同量化参数的运行内存是不一样的

|量化类型|适用场景|内存需求|
|---|---|---|
|q4_0|平衡速度与精度|~1.5GB|
|q5_1|更高精度输出|~2.0GB|
|q8_0|接近原始精度的评估|~3.0GB|

如下提示表示量化完成：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/f1b1922c-c67e-4195-9b6f-2a60a025c434.jpg)

在查找资料过程中，发现量化模型还有一中方案是`bitsandbytes`，后面有时间再进一步研究:

```sh
pip install bitsandbytes
```

#### 运行模型

这里还没来得研究具体的命令，简单先让模型跑起来，明天再继续研究：
```sh
./build/bin/llama-run deepseek-r1-1.5b.q4_0.gguf
```
运行效果如下：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/0270226e-2aa5-4619-826e-80e6436939c3.jpg)

当输入问题之后，控制台不断有内容输出的那个瞬间，内心的喜悦无法言表，此刻我又离`AI`更近了一步～



### 内容扩展

在跑通整个链路之后，我发现有个`llama-server`命令可以直接以服务端的方式运行模型，这样我们就可以在浏览器直接访问了，默认端口是`8080`，具体命令如下：

```sh
./build/bin/llama-server -m deepseek-r1-1.5b.q4_0.gguf 
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/b8db9007-519c-4032-b494-d3c1a6621b47.jpg)

浏览器效果如下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/7ca73ae0-d085-4cc7-b3fa-398a95e9899c.jpg)

好了，至此整个过程圆满结束。


#### 资源链接

有条件的小伙伴建议手动从官网下载，某盘的网速不敢想象，我上传感觉都好慢

```
# llama的地址，有效期365天
链接: https://pan.baidu.com/s/1eKV3_bSKZrxg-HLXvUupbg?pwd=qha3 提取码: qha3 复制这段内容后打开百度网盘手机App，操作更方便哦
```

模型地址：
```
# 有效期365天
链接: https://pan.baidu.com/s/1qqm53xQ3T1uLxtX9sHfhRg?pwd=4w8w 提取码: 4w8w 复制这段内容后打开百度网盘手机App，操作更方便哦
```

感兴趣的小伙伴可以折腾起来了，新的一年，让我们从部署自己的`AI`开始，开启自己的`AI`新旅程～