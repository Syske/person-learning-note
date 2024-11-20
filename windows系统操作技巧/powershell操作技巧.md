
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

### 别名永久生效

在PowerShell中设置别名永久生效通常涉及到修改用户的配置文件。对于PowerShell来说，用户级别的配置文件通常是`$PROFILE`文件。这个文件位于每个用户的文档目录下的`WindowsPowerShell`文件夹内，文件名为`Microsoft.PowerShell_profile.ps1`。如果该文件不存在，你可以创建它。

要为所有会话设置一个永久的别名，你需要编辑或创建这个配置文件，并在其中添加`Set-Alias`命令。下面是如何操作的步骤：

1. 打开PowerShell并检查你的个人配置文件是否存在：
   ```powershell
   Test-Path $PROFILE
   ```

2. 如果返回`False`，说明你的个人配置文件不存在，你需要创建它：
   ```powershell
   New-Item -Path $PROFILE -Type File -Force
   ```

3. 使用你喜欢的文本编辑器打开这个配置文件。例如，使用记事本：
   ```powershell
   notepad $PROFILE
   ```

4. 在打开的文件中，添加你想要设置的别名。例如，如果你想为`Get-ChildItem`（等同于`dir`）设置一个别名`gci`，你可以这样写：
   ```powershell
   Set-Alias -Name gci -Value Get-ChildItem
   ```

5. 保存文件并关闭编辑器。

6. 为了使更改生效，你需要重新启动PowerShell或者在当前会话中运行`. $PROFILE`来加载新的配置。

如果你希望设置系统级别的别名，那么你需要将上述命令添加到所有用户共用的配置文件中，这个文件通常位于`C:\Windows\System32\WindowsPowerShell\v1.0\profile.ps1`。但是，修改这个文件可能需要管理员权限，并且会影响所有使用该计算机的用户。

记得在修改任何配置文件之前，最好先备份原始文件，以防出现问题。