#python
## 使用pyenv

pyenv是一个流行的工具，用于在Unix-like系统（如Linux和macOS）上管理多个Python版本。

安装pyenv:
```sh
curl https://pyenv.run | bash
```

或者使用git克隆仓库：
```sh
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

配置环境变量（可选，但推荐）:

将以下行添加到你的~/.bashrc或~/.zshrc文件中：
```sh
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

然后，运行source ~/.bashrc或source ~/.zshrc来应用更改。

安装Python版本:
```sh
pyenv install 3.8.5  # 安装特定版本的Python
```

设置全局Python版本:
```sh
pyenv global 3.8.5  # 设置全局Python版本为3.8.5
```
在特定项目中使用特定版本:
```sh
cd your_project_directory
pyenv local 3.7.9  # 为当前目录设置特定版本的Python
```