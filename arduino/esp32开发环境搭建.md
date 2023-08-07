
### 确认python环境

目前绝大多数`linux`环境都自带了`python3`环境，如果没有需要安装

### clone源码

```sh
mkdir -p ~/esp
cd ~/esp
git clone --recursive https://github.com/espressif/esp-idf.git
```


### 设置工具

```sh
cd ~/esp/esp-idf
./install.sh esp32
```