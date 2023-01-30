# 配置安装vue-electron开发环境

#### 安装vue

首先要安装淘宝的`cnpm`命令管理工具，这个工具可以代替默认的`npm`管理工具

```sh
npm install -g cnpm --registry=https://registry.npm.taobao.org
```

通过如下命令安装`vue`环境：

```sh
cnpm install --global vue-cli  
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211128162704.png)

#### 验证

安装完成后，输入`vue`验证是否安装成功：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211128162809.png)

#### 创建项目

可以通过如下命令创建`vue`项目，其中`demo`表示项目名称

```
vue init webpack demo
```

之后根据提示信息操作即可

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211128162958.png)

#### 运行项目

通过如下命令就可以启动我们刚刚创建的`vue`项目了：

```
cd demo
npm run dev
```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211128163249.png)

然后根据提示的地址访问服务即可：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20211128163359.png)

