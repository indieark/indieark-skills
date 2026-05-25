# IndieArk Skills

IndieArk Codex Skills 运行时分发仓库。

本仓库只保存可安装的 runtime skill 目录，不保存私库开发仓库、外部扩展 checkout、工作目录、测试缓存或历史压缩包。

## 包含内容

| Skill | CLI | 说明 |
|---|---|---|
| `image-gen-pro` | `imagen` | 图片生成、图生图、编辑、透明图和批量任务 |
| `ppt-gen-pro` | 暂无 | PPT / slide deck 路由 skill |
| `seedance2-video-pro` | `seedance2` | Seedance 2.0 视频生成导演和 API 执行 |

## 安装

```powershell
git clone https://github.com/indieark/indieark-skills.git
cd indieark-skills
.\install.ps1
```

安装目标默认是：

```powershell
$env:USERPROFILE\.codex\skills
```

如果要同时安装 CLI wrapper：

```powershell
.\install.ps1 -InstallCli
```

CLI wrapper 默认写入：

```powershell
$env:LOCALAPPDATA\Microsoft\WindowsApps
```

## 更新

```powershell
cd indieark-skills
.\update.ps1
```

更新脚本会执行 `git pull --ff-only`，然后重新安装 skill。需要同步 CLI wrapper 时：

```powershell
.\update.ps1 -InstallCli
```

## 维护者发布

在私库工作区中，本仓库应放在 `C:\Vibe_Coding\IndieArk\indieark-skills`，与开发源 `C:\Vibe_Coding\IndieArk\skills` 平级。

从私库 runtime 目录刷新本仓库：

```powershell
.\publish.ps1 -SourceRoot ..\skills
```

刷新后运行：

```powershell
.\install.ps1 -WhatIf
git status --short
git diff --stat
```
