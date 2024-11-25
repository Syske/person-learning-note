
### 镜像下载刻录



### 系统分区

```sh
fdisk /dev/sda
```

### 安装




#### 配置网络

```sh
# 直接进入无线网络管理工具
iwctl
# 连接指定的wifi
station wlan0 connect syske-wifi
# 然后输入wifi密码
```

#### 挂载目录

```
# root分区挂载
mount /dev/nvme0n1p6 /mnt

# EFI 分区挂载
mount --mkdir /dev/nvme0n1p1 /mnt/boot
# home分区挂载
mount --mkdir /dev/sda3 /mnt/home
```

