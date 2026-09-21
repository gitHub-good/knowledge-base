# 🪟 Windows / PowerShell / Git Bash 速查

> 本机日常环境：Windows + Git Bash + 偶尔 PowerShell。最容易踩的坑是**三套环境的路径与命令差异**。

## 📊 〇、环境对照表（先记住这个）

| 任务 | CMD | PowerShell | Git Bash |
| --- | --- | --- | --- |
| 列目录 | `dir` | `Get-ChildItem`（别名 `ls`/`gci`） | `ls` |
| 找内容 | `findstr "err" a.log` | `Select-String "err" a.log` | `grep "err" a.log` |
| 管道符 | `\|` | `\|` | `\|` |
| 路径分隔 | `\` | `\` 或 `` ` `` | `/`，D 盘是 `/d/` |
| 环境变量 | `%PATH%` | `$env:PATH` | `$PATH` |
| 执行脚本 | `script.bat` | `.\script.ps1` | `./script.sh` |

Git Bash 路径换算：`D:\work\demo` ⇔ `/d/work/demo`。在 Git Bash 里粘贴 Windows 路径前，把 `\` 换成 `/`、盘符改小写加 `/`。

## 🐚 一、Git Bash（日常主力）

```bash
# Windows 程序也能直接调
explorer .                 # 资源管理器打开当前目录
code .                     # VS Code 打开当前目录
clip < output.txt          # 内容进剪贴板
powershell.exe -c "..."    # 临时借用 PS 命令
cmd //c "dir"              # 临时借用 CMD（注意双斜杠）
```

## ⚡ 二、PowerShell（CMD 的现代替代）

```powershell
# ── 查找与过滤（最常用）──
Get-ChildItem -Recurse -Filter "*.log" | Select-String "ERROR" | Select-Object -First 20
Get-ChildItem -Recurse -Include *.tmp | Remove-Item -WhatIf    # -WhatIf 干跑预览！

# ── 进程与端口 ──
Get-Process java | Sort-Object CPU -Descending | Select-Object -First 5
Get-NetTCPConnection -LocalPort 8080                           # 谁占了 8080
Stop-Process -Id 1234 -Force

# ── 系统信息 ──
Get-PSDrive -PSProvider FileSystem    # 各盘剩余空间
Get-ComputerInfo | Select-Object OsName, OsVersion
Get-EventLog -LogName System -Newest 20 -EntryType Error       # 系统错误日志

# ── 实用小件 ──
Set-Clipboard "内容"        /   Get-Clipboard
Invoke-WebRequest https://example.com -OutFile page.html       # 下载
(Get-Item app.exe).VersionInfo                                 # 看 exe 版本
```

## 🖥️ 三、CMD 仍好用的几条

```bat
:: 端口占用三步曲
netstat -ano | findstr :8080     :: 拿到 PID
tasklist /FI "PID eq 1234"       :: PID 对应进程名
taskkill /F /PID 1234            :: 强杀

:: 映射网络盘
net use Z: \\server\share /persistent:yes

:: 定时关机/取消
shutdown /s /t 3600
shutdown /a
```

## 📦 四、包管理（装软件不再点下一步）

```powershell
# winget（系统自带）
winget search vscode
winget install Git.Git
winget upgrade --all              # 全部软件一键升级

# scoop（命令行工具首选，装在用户目录免管理员）
scoop install ripgrep fzf jq 7zip
# 装完即可在 Git Bash 用 rg / fzf / jq
```

推荐命令行三件套（配 Git Bash 如虎添翼）：`rg`（grep 十倍速）、`fzf`（模糊搜索历史 `Ctrl+R`）、`jq`（命令行解析 JSON：`curl -s api | jq '.data.items[0]'`）。

## 🎯 五、高频场景

| 场景 | 做法 |
| --- | --- |
| 文件被占用删不掉 | `Get-Process | Where-Object {$_.Path -like "*目标目录*"} ` 找到进程后停掉 |
| 查看大文件占盘 | WinDirStat / `Get-ChildItem -Recurse \| Sort Length -Desc \| Select -First 10 Name,@{n='MB';e={[int](/personal-assistant/commands/$_.Length/1MB)}}` |
| 长路径删不掉 | Git Bash：`rm -rf 目录`；或 robocopy 空目录覆盖法 |
| 环境变量改完不生效 | 关掉终端重开（终端启动时快照环境） |
| 脚本乱码 | 文件转 UTF-8（无 BOM），或 PS 里 `chcp 65001` |
| 开机自启管理 | `Ctrl+Shift+Esc` → 启动应用 标签 |
