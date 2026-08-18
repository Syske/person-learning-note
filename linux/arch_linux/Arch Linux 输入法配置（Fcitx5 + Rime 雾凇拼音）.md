# Arch Linux 输入法配置（Fcitx5 + Rime 雾凇拼音）

## 环境

- OS: Arch Linux
- DE: KDE Plasma (Wayland)
- 输入法框架: Fcitx5
- 输入法引擎: Rime (雾凇拼音 rime-ice)

---

## 1. 安装必要软件包

```bash
sudo pacman -S fcitx5 fcitx5-rime fcitx5-configtool
# 雾凇拼音（AUR）
yay -S rime-ice-git
```

## 2. 配置环境变量

Fcitx5 需要环境变量才能被图形程序加载。在 Wayland + KDE 下，通过 `environment.d` 配置（对所有 systemd 用户进程生效）：

**`~/.config/environment.d/im.conf`**

```
GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS=@im=fcitx
GLFW_IM_MODULE=fcitx
SDL_IM_MODULE=fcitx
```

> 终端中也需要这些变量，可在 `~/.bashrc` 中添加相同的 export，方便终端下使用。

## 3. 配置 Fcitx5

### 3.1 启用 Wayland IM 支持

编辑 `~/.config/fcitx5/config`，确保 **`waylandim` 未被禁用**（Wayland 必须）：

```ini
[Behavior/DisabledAddons]
0=kimpanel
# waylandim 不要出现在这里
```

> 如果禁用了 waylandim，Fcitx5 在 Wayland 下无法正常切换窗口输入状态。

### 3.2 禁用 spell 插件（可选）

`spell` 插件依赖 `enchant` 库，后者会初始化所有拼写后端。若未安装 `aspell` / `nuspell` / `voikko` 等库，enchant 会超时，导致 Fcitx5 启动卡顿约 2 分钟。

```ini
[Behavior/DisabledAddons]
0=kimpanel
1=spell
```

### 3.3 推荐焦点行为

```ini
[Behavior]
ActiveByDefault=True              # 新窗口默认激活中文
resetStateWhenFocusIn=No          # 切回窗口时记住上次状态
```

- `ActiveByDefault=True`：新打开的应用直接可用中文输入，无需按 Ctrl+Space
- `resetStateWhenFocusIn=No`：每个窗口独立记住中/英状态，切回时不变

### 3.4 设置默认输入法

编辑 **`~/.config/fcitx5/profile`**（需在 fcitx5 未运行时编辑，否则会被覆写）：

```ini
[Groups/0]
Name=Default
Default Layout=us
DefaultIM=rime                        # 默认输入法设为 Rime

[Groups/0/Items/0]
Name=keyboard-us
Layout=

[Groups/0/Items/1]
Name=pinyin
Layout=cn

[Groups/0/Items/2]
Name=rime                             # 添加 Rime 输入法
Layout=cn
```

## 4. 配置 Rime（雾凇拼音）

### 4.1 基础配置

**`~/.local/share/fcitx5/rime/default.custom.yaml`**

```yaml
patch:
  schema_list:
    - schema: rime_ice                  # 使用雾凇拼音
  ascii_composer:
    reset_ascii_mode: true
    switch_key:
      Shift_L: commit_code              # 按 Shift 临时上屏英文
      Shift_R: commit_code
  switcher:
    hotkeys:
      - Control+grave                   # Ctrl+` 切换方案
      - Control+Shift+grave
    save_options:
      - full_shape
      - ascii_punct
      - traditionalization
      - emoji
  menu:
    page_size: 7                        # 每页候选词数
  key_binder:
    bindings:
      - { when: has_menu, accept: comma, send: Page_Up }
      - { when: has_menu, accept: period, send: Page_Down }
```

### 4.2 部署 Rime

复制预编译的雾凇拼音词库（`rime-ice-git` 已预编译）：

```bash
cp /usr/share/rime-data/build/rime_ice.table.bin \
   /usr/share/rime-data/build/rime_ice.reverse.bin \
   /usr/share/rime-data/build/rime_ice.prism.bin \
   /usr/share/rime-data/build/rime_ice.schema.yaml \
   ~/.local/share/fcitx5/rime/build/

# 复制依赖的词典
for f in melt_eng.prism.bin melt_eng.reverse.bin melt_eng.table.bin melt_eng.schema.yaml \
         radical_pinyin.prism.bin radical_pinyin.reverse.bin \
         radical_pinyin.table.bin radical_pinyin.schema.yaml; do
  cp "/usr/share/rime-data/build/$f" ~/.local/share/fcitx5/rime/build/
done
```

也可用 `rime_deployer` 重新部署：

```bash
rime_deployer --build \
  ~/.local/share/fcitx5/rime/ \
  /usr/share/rime-data/ \
  ~/.local/share/fcitx5/rime/build/
```

> ⚠️ `rime_deployer` 的三个参数顺序：用户目录 → 共享目录 → build 目录，缺一不可。
> 雾凇拼音的源 schema（`rime_ice.schema.yaml`）在共享目录 `/usr/share/rime-data/`，
> 用户目录下只有 build 产物，若漏掉共享目录参数会报 `missing input schema: rime_ice`。
> **坑**：`rime_deployer` 即使报错，退出码仍为 0，必须看 stderr 中 `E` 开头的日志。

### 4.3 默认英文输入、Shift 手动切中文

默认英文 + 手动切换的关键：让 schema 的 `ascii_mode` 开关默认置为「英文」。

**`~/.local/share/fcitx5/rime/rime_ice.custom.yaml`**

```yaml
# 雾凇拼音覆写：默认英文输入，中文手动切换
patch:
  # switches 列表第 0 项是 ascii_mode（states: ["中", "Ａ"]）
  # reset: 1 表示该开关默认处于第 1 项（英文）
  switches/@0/reset: 1
```

配合 `default.custom.yaml` 已有的：

```yaml
ascii_composer:
  reset_ascii_mode: true        # 部署后自动回英文
  switch_key:
    Shift_L: commit_code        # 按 Shift 中英切换（手动切中文）
    Shift_R: commit_code
```

**⚠️ 关键：必须清空 fcitx5 的 AltTriggerKeys**，否则 fcitx5 会抢走 Shift 键，Rime 的 Shift 切换永远不生效：

**`~/.config/fcitx5/config`**

```ini
[Hotkey/AltTriggerKeys]
# 留空！不能配 Shift_L 或 Shift_R
```

### 4.4 部署并重启生效

改完 Rime 配置后：

```bash
# 1. 重新部署（生成 build 产物）
rime_deployer --build ~/.local/share/fcitx5/rime/ /usr/share/rime-data/

# 2. 验证 reset 已写入编译产物

grep -n "ascii_mode" -A 3 ~/.local/share/fcitx5/rime/build/rime_ice.schema.yaml
# 应看到: reset: 1

# 3. 完全重启 fcitx5（fcitx5-remote -r 不够！）
fcitx5-remote -e
fcitx5 -d &

# 4. 验证
fcitx5-remote -n        # 应输出 rime
fcitx5-remote           # 应输出 2（已激活）
```

> ⚠️ `fcitx5-remote -r` 只是重载配置，不触发 Rime 重新部署，
> 还可能把当前输入法重置为 pinyin。必须 `fcitx5-remote -e` 退出后重启 fcitx5 进程才能完全生效。
> 若切到了 pinyin，用 `fcitx5-remote -s rime` 切回。

## 5. 重启 Fcitx5

```bash
pkill fcitx5
fcitx5 -rd &
```

验证：

```bash
fcitx5-remote -n        # 应输出 rime
fcitx5-remote           # 应输出 2（已激活）
```

## 6. 常见问题

### 6.1 切换窗口输入法异常

- 确保 `waylandim` 插件未被禁用
- 确保环境变量正确配置（KDE 下用 `environment.d`）
- 部分应用需要重启才能读取环境变量

### 6.2 Fcitx5 启动卡顿

禁用 `spell` 插件（见 3.2），或安装缺失的拼写后端：

```bash
sudo pacman -S hunspell aspell nuspell voikko
```

### 6.3 环境变量不生效

- KDE Wayland 使用 `~/.config/environment.d/*.conf`（systemd 用户环境）
- 终端使用 `~/.bashrc` 中的 export
- 修改后需重新登录或重启应用

### 6.4 Rime 部署失败

检查 build 目录是否包含完整的编译文件：

```bash
ls ~/.local/share/fcitx5/rime/build/rime_ice.*
# 应有: .prism.bin .reverse.bin .table.bin .schema.yaml
```

### 6.5 Shift 无法切换中/英（或切不回来）

症状：配置了 `switch_key: Shift_L: commit_code` 但按 Shift 没反应 / 切不回来。

根因：`~/.config/fcitx5/config` 的 `[Hotkey/AltTriggerKeys]` 配了 `Shift_L` 或 `Shift_R`，
fcitx5 把 Shift 当作「临时切换输入法」快捷键抢走了，Rime 收不到按键。

解决：清空该组：

```ini
[Hotkey/AltTriggerKeys]
```

### 6.6 默认英文失效 / 配置改了没生效

排查顺序：

1. 确认 `rime_ice.custom.yaml` 的 patch 已写入编译产物：
   `grep -n "reset: 1" ~/.local/share/fcitx5/rime/build/rime_ice.schema.yaml`
2. 确认当前输入法确实是 rime 而不是 pinyin：`fcitx5-remote -n`
3. 重启 fcitx5 进程（`fcitx5-remote -e` 后重新启动），仅 `-r` 重载不够

## 7. 参考文件路径汇总

| 文件 | 用途 |
|------|------|
| `~/.config/environment.d/im.conf` | 环境变量（systemd 用户环境） |
| `~/.config/fcitx5/config` | Fcitx5 主配置（含 AltTriggerKeys，需清空） |
| `~/.config/fcitx5/profile` | 输入法列表及顺序 |
| `~/.config/fcitx5/conf/pinyin.conf` | Fcitx5 拼音配置 |
| `~/.local/share/fcitx5/rime/default.custom.yaml` | Rime 用户配置（ascii_composer / switch_key） |
| `~/.local/share/fcitx5/rime/rime_ice.custom.yaml` | 雾凇拼音覆写（默认英文，switches/@0/reset: 1） |
| `~/.local/share/fcitx5/rime/build/` | Rime 编译文件 |
| `/usr/share/rime-data/` | Rime 共享数据（源 schema 在此） |
| `/etc/xdg/autostart/org.fcitx.Fcitx5.desktop` | Fcitx5 自动启动 |
