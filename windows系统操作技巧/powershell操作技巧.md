
### 别名

#### 设置别名

```powershell
Set-Alias -Name 别名 -Value 原始命令
```

#### 获取别名

```powershell
# 获取所有别名
Get-alias 
# 获取指定名称的别名
Get-alias -Name pdb
# 支持正则表达式
Get-alias -Name pdb*
# `Get-Alias`还提供了一些其他选项，如`-Definition`参数，它允许您按原始命令或函数来过滤别名
Get-Alias -Definition git.exe
```

#### 删除别名

```powershell
Remove-Item Alias:<别名名称>
# 从PowerShell 6.0开始，引入了一个新的cmdlet `Remove-Alias`
Remove-Alias -Name git
```


### posh-git乱码

将`powershell`默认编码设置为`utf8`

```powershell
$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```