# Linux命令手册

##### 开机启动命令行模式

```
systemctl set-default multi-user.target
```

默认进入`GUI`模式

```
systemctl set-default graphical.target
```


### 常用命令

#### 解压

指定文件夹解压，这里需要注意的是`-C`是大写，否则会报错
```sh
tar -xvf ffmpeg-git-amd64-static.tar.xz -C ~/workspace/dev-tools
```