## win10企业版激活

以管理员身份运行`cmd`，并执行以下命令

### 卸载密钥

```
slmgr.vbs /upk
```

### 安装新密钥

```sh
slmgr /ipk NPPR9-FWDCX-D2C8J-H872K-2YT43
# 另一个密钥
slmgr /ipk PBHCJ-Q2NYD-2PX34-T2TD6-233PK
```

### 设置计算机名称

```
slmgr /skms zh.us.to
```

### 激活

```
slmgr /ato
```

