### 迁移wsl到D盘

```sh
# 停用wsl
wsl --shutdown
# 导出要迁移的wsl
wsl --export archlinux D:\dev-tool\archlinux.tar

# 取消注册
wsl --unregister archlinux

# 重新导入
wsl --import archlinux D:\dev-tool\wsl\archlinux  D:\dev-tool\archlinux.tar
```

迁移过程，可以通过下述命令来查看`wsl`信息：
```sh
wsl -l
```