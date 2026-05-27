<div align="center">

# IndieArk Skills

**为 Claude Code · Codex CLI · Cursor 等 AI 协作终端打造的，面向独立开发者与小团队的「八件套」生产级 Agent Skills。**

<a id="skills-gallery"></a>

<table>
<tr>
<td width="50%" valign="top">
<a href="#image-gen-pro"><img src="./assets/skills/image-gen-pro.png" alt="image-gen-pro" width="100%"></a>
<br/><a href="#image-gen-pro"><strong>image-gen-pro</strong></a> <code>图</code>
<br/><sub>图像生成 / 编辑 / 透明 / 批量</sub>
</td>
<td width="50%" valign="top">
<a href="#ppt-gen-pro"><img src="./assets/skills/ppt-gen-pro.png" alt="ppt-gen-pro" width="100%"></a>
<br/><a href="#ppt-gen-pro"><strong>ppt-gen-pro</strong></a> <code>片</code>
<br/><sub>演示文稿 / Slide Deck</sub>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="#html-gen-pro"><img src="./assets/skills/html-gen-pro.png" alt="html-gen-pro" width="100%"></a>
<br/><a href="#html-gen-pro"><strong>html-gen-pro</strong></a> <code>网</code>
<br/><sub>HTML / 网页 / Landing</sub>
</td>
<td width="50%" valign="top">
<a href="#seedance2-video-pro"><img src="./assets/skills/seedance2-video-pro.png" alt="seedance2-video-pro" width="100%"></a>
<br/><a href="#seedance2-video-pro"><strong>seedance2-video-pro</strong></a> <code>视</code>
<br/><sub>Seedance 2.0 视频导演</sub>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="#search-pro"><img src="./assets/skills/search-pro.png" alt="search-pro" width="100%"></a>
<br/><a href="#search-pro"><strong>search-pro</strong></a> <code>搜</code> · <sub>🚧 Preview</sub>
<br/><sub>检索 / 抓取 / 下载 / 转换</sub>
</td>
<td width="50%" valign="top">
<a href="#office-pro"><img src="./assets/skills/office-pro.png" alt="office-pro" width="100%"></a>
<br/><a href="#office-pro"><strong>office-pro</strong></a> <code>办</code> · <sub>🚧 Preview</sub>
<br/><sub>办公接入 + 数据分析</sub>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="#struct-pro"><img src="./assets/skills/struct-pro.png" alt="struct-pro" width="100%"></a>
<br/><a href="#struct-pro"><strong>struct-pro</strong></a> <code>构</code> · <sub>🚧 Preview</sub>
<br/><sub>文件夹 / 代码 / 文档结构治理</sub>
</td>
<td width="50%" valign="top">
<a href="#write-pro"><img src="./assets/skills/write-pro.png" alt="write-pro" width="100%"></a>
<br/><a href="#write-pro"><strong>write-pro</strong></a> <code>写</code> · <sub>🚧 Preview</sub>
<br/><sub>各类内容写作编排</sub>
</td>
</tr>
</table>

[![License](https://img.shields.io/badge/license-Proprietary-blue?style=flat-square)](./LICENSE)
[![Skills count](https://img.shields.io/badge/skills-8-orange?style=flat-square)](#skills-gallery)
[![Active](https://img.shields.io/badge/active-4-brightgreen?style=flat-square)](#skills-gallery)
[![Preview](https://img.shields.io/badge/preview-4-yellow?style=flat-square)](#skills-gallery)
[![Spec](https://img.shields.io/badge/spec-SKILL.md-black?style=flat-square)](https://agentskills.io)

</div>

---

## 目录

| 安装 | 使用 | 维护 |
|---|---|---|
| [PowerShell 一键安装](#powershell-一键安装)<br>[手动复制](#手动复制)<br>[Git Submodule](#git-submodule) | [八件套总览](#八件套总览)<br>[兼容性](#兼容性)<br>[什么是 Skill](#什么是-skill) | [更新](#更新)<br>[发布维护者指南](#发布维护者指南)<br>[License](#license) |

---

## 八件套总览

IndieArk Skills 把独立开发与小团队最高频的八种 AI 协作任务，按一字定位拆成八件套，每件都是一个独立 Skill。任何一件单装可用、组合更香：

| | Skill | 定位 | 状态 |
|---|---|---|---|
| 图 | [`image-gen-pro`](#image-gen-pro) | 图像生成 / 编辑 / 透明 / 批量 | `active` |
| 片 | [`ppt-gen-pro`](#ppt-gen-pro) | 演示文稿 / Slide Deck | `active` |
| 网 | [`html-gen-pro`](#html-gen-pro) | HTML / 网页 / Landing | `active` |
| 视 | [`seedance2-video-pro`](#seedance2-video-pro) | Seedance 2.0 视频导演 + API | `active` |
| 搜 | [`search-pro`](#search-pro) | 检索 / 抓取 / 下载 / 转换 | `preview` |
| 办 | [`office-pro`](#office-pro) | 办公接入 + 数据分析 | `preview` |
| 构 | [`struct-pro`](#struct-pro) | 文件夹 / 代码 / 文档结构治理 | `preview` |
| 写 | [`write-pro`](#write-pro) | 内容写作统一编排 | `preview` |

> `preview` 表示 v0.1.0-skeleton：SKILL.md / skill.json / references/ 路由完备，可被 agent 加载，但 CLI / 下游执行链尚未就位；正式落地节奏见各仓库内 `plans/`。

---

### `image-gen-pro`

<a id="image-gen-pro"></a>

![image-gen-pro](./assets/skills/image-gen-pro.png)

**分类：** 图像生成 / Prompt 工程  
**适用：** 海报、UI 截图、产品图、信息图、技术图解、漫画、头像、品牌板，以及图生图与图像编辑工作流。  
**CLI：** `imagen`

`image-gen-pro` 是面向 GPT Image 2 与 OpenAI 兼容图像 API 的统一执行 skill。它在不同的 agent 环境里都能识别正确的运行路径：本地完整生图、宿主图像工具委托、或纯 prompt advisor 模式。

亮点：

- 三种运行路由：**API key** / **Codex CLI 委托** / **placeholder dry-run**
- 18 个视觉类别 + 80+ 结构化 prompt 模板（`references/`）
- 同时覆盖 **图生图**、**图像编辑**、**透明 PNG**、**批量 manifest** 全链路
- `imagen doctor` / `imagen dry-run` / `imagen plan` 提供生图前的完整 sanity check
- `_work/image_gen_runs/` 默认本地留痕，方便回看、复用、版本对比

链接：[skill 目录](./image-gen-pro) · [SKILL.md](./image-gen-pro/SKILL.md) · [README](./image-gen-pro/README.md)

---

### `ppt-gen-pro`

<a id="ppt-gen-pro"></a>

![ppt-gen-pro](./assets/skills/ppt-gen-pro.png)

**分类：** 演示文稿 / Slide Deck  
**适用：** 技术分享、产品方案、商业汇报、训练材料的多平台 deck 产出。

`ppt-gen-pro` 把"做 PPT"这件事拆成路由判定 + 模板 + 内容编排三段，让 agent 在 deck 语境下知道何时调风格、何时调结构、何时回模板。

亮点：

- 按受众 / 平台 / 风格做 L1 路由判定
- 与 [`image-gen-pro`](#image-gen-pro) 联动获取首屏与配图
- 多模板风格切换，避免每次都从零拼版

链接：[skill 目录](./ppt-gen-pro) · [SKILL.md](./ppt-gen-pro/SKILL.md)

---

### `html-gen-pro`

<a id="html-gen-pro"></a>

![html-gen-pro](./assets/skills/html-gen-pro.png)

**分类：** 网页 / 静态站点 / 原型  
**适用：** Landing page、产品官网、HTML slide deck、设计原型、文档站。

`html-gen-pro` 把网页生成从"AI 拼一张能跑的页面"提升到"设计系统先行 + 可演进的产物"——先声明设计 token、再出 v0、再补完整布局与交互。

亮点：

- 设计系统先行（tokens → v0 → full build → 验证）
- 多种页面类型模板（landing / dashboard / docs / slides）
- HTML / CSS / JS / React inline + Babel 实施范式齐备
- 与 [`image-gen-pro`](#image-gen-pro) 联动产出首屏视觉与配图
- 高级模式参考：设备框、幻灯片引擎、动画时间线、仪表盘

链接：[skill 目录](./html-gen-pro) · [SKILL.md](./html-gen-pro/SKILL.md) · [README](./html-gen-pro/README.md)

---

### `seedance2-video-pro`

<a id="seedance2-video-pro"></a>

![seedance2-video-pro](./assets/skills/seedance2-video-pro.png)

**分类：** 视频生成 / 镜头导演  
**适用：** 短视频、产品演示、动画镜头、多机位镜头序列。  
**CLI：** `seedance2`

`seedance2-video-pro` 把 Seedance 2.0 的能力封装成"导演 + API 执行"两层：agent 既能写镜头脚本，也能直接拉起生成。

亮点：

- `seedance2` CLI 包装，统一参数与产物
- 镜头脚本生成 + 多机位序列编排
- 与 [`image-gen-pro`](#image-gen-pro) 联动取首帧 / 关键帧

链接：[skill 目录](./seedance2-video-pro) · [SKILL.md](./seedance2-video-pro/SKILL.md) · [README](./seedance2-video-pro/README.md)

---

### `search-pro` · 🚧 Preview

<a id="search-pro"></a>

![search-pro](./assets/skills/search-pro.png)

**分类：** 信息检索 / 抓取 / 下载 / 转换  
**状态：** `v0.1.0-skeleton` — 路由层已就位，下游 CLI 集成与统一 facade 仍在 plans/007 决议。

`search-pro` 是"获取与转换信息"的统一路由层，下游接 `smart-search-cli` / `scrapling` / `agent-browser` / `yt-dlp` / `pandoc` & `ffmpeg` & `imagemagick`，让 agent 在抓 / 爬 / 下 / 转之间不再手忙脚乱。

亮点：

- **5 条 L1 路线**：search-web / crawl-static / crawl-render / download-media / convert-format
- 按目标可用性、是否需要 JS、是否需要登录智能选下游
- 离线 / 在线 / 订阅监控边界清晰
- 升 `ready` 阻塞项见私库 `plans/007`

链接：[skill 目录](./search-pro) · [SKILL.md](./search-pro/SKILL.md) · [路由表](./search-pro/references/router.md)

---

### `office-pro` · 🚧 Preview

<a id="office-pro"></a>

![office-pro](./assets/skills/office-pro.png)

**分类：** 办公接入 / 数据分析  
**状态：** `v0.1.0-skeleton` — 飞书主路线确定，多平台与分析栈仍在 plans/008 决议。

`office-pro` 是办公自动化 + 数据分析的统一入口。接入层先以飞书为主（编排全局 40+ `lark-*` 子 skill，不复制底层 OpenAPI），分析层覆盖探索 / 清洗 / 统计 / 可视化 / 报告。

亮点：

- **双主路线**：`office-connect`（飞书优先）+ `data-analysis`（探索 → 清洗 → 统计 → 可视化 → 报告）
- 飞书 OpenAPI 编排（多维表 / 电子表格 / 云文档 / 消息 / 审批）
- 凭据不入仓库，本地 env 处理
- 升 `ready` 阻塞项见私库 `plans/008`

链接：[skill 目录](./office-pro) · [SKILL.md](./office-pro/SKILL.md) · [路由表](./office-pro/references/router.md)

---

### `struct-pro` · 🚧 Preview

<a id="struct-pro"></a>

![struct-pro](./assets/skills/struct-pro.png)

**分类：** 结构治理 / 重构  
**状态：** `v0.1.0-skeleton` — 三条主路线骨架就位，CLI 形态与跨仓边界仍在 plans/009 决议。

`struct-pro` 是文件夹 / 代码 / 文档"三线结构治理"的 CLI + Skill 组合。遵循三原则：**单一信息源** · **层层索引** · **信息一致性**。

亮点：

- **三条主路线**：`folder-tidy` / `code-structure` / `doc-structure`
- 默认**非破坏性 dry-run**；任何破坏性动作显式 opt-in
- v0.1.0 锁定**跨仓库 mv 禁用**
- 文档结构覆盖**三受众矩阵**：AI 记忆 / AI 阅读 / 人类阅读
- 代码结构关注组件化 / 模块化 / 接口对接口
- 升 `ready` 阻塞项见私库 `plans/009`

链接：[skill 目录](./struct-pro) · [SKILL.md](./struct-pro/SKILL.md) · [路由表](./struct-pro/references/router.md)

---

### `write-pro` · 🚧 Preview

<a id="write-pro"></a>

![write-pro](./assets/skills/write-pro.png)

**分类：** 内容写作 / 编排  
**状态：** `v0.1.0-skeleton` — 4 条路线 + 反 AI slop critique 已锁，个性化语料与发布渠道仍在 plans/010 决议。

`write-pro` 是各类内容写作的统一编排入口，调度全局 9 个 `pro-*` 方法论原子（`copy` / `exp` / `explain` / `idea` / `must` / `rule` / `struct` / `summary` / `test`）。它不是另一个写作 skill，而是**反 AI slop 的第一防线** + **个人风格 prompt 优先**的编排层。

亮点：

- **4 条 L1 路线**：long-form / short-form / commercial-copy / engineering-doc
- **反 AI slop 强制 critique**：draft → final 之前必须列出 ≥3 条不可替换的差异化记忆点，否则回 draft 迭代
- 三段式产出：`outline` → `draft` → `final`
- 完整 `pro-*` 调用矩阵（不复制原子方法论正文，按路线映射）
- 升 `ready` 阻塞项见私库 `plans/010`

链接：[skill 目录](./write-pro) · [SKILL.md](./write-pro/SKILL.md) · [路由表](./write-pro/references/router.md)

---

## 安装

> 当前面向 Windows / PowerShell 工作站。其他平台可走 [手动复制](#手动复制) 或 [Git Submodule](#git-submodule)。

### PowerShell 一键安装

```powershell
git clone https://github.com/indieark/indieark-skills.git
cd indieark-skills
.\install.ps1
```

默认安装目标：

```powershell
$env:USERPROFILE\.codex\skills
```

需要同时安装 CLI wrapper（`imagen` / `seedance2` 等）：

```powershell
.\install.ps1 -InstallCli
```

CLI wrapper 默认写入：

```powershell
$env:LOCALAPPDATA\Microsoft\WindowsApps
```

### 手动复制

把对应 skill 文件夹复制到你的 agent skills 目录即可：

```powershell
# Codex CLI
Copy-Item -Recurse .\image-gen-pro $env:USERPROFILE\.codex\skills\
# Claude Code
Copy-Item -Recurse .\image-gen-pro .claude\skills\
# Cursor
Copy-Item -Recurse .\image-gen-pro .agents\skills\
```

下次 agent 扫描时自动识别。

### Git Submodule

```powershell
git submodule add https://github.com/indieark/indieark-skills.git vendor/indieark-skills
New-Item -ItemType SymbolicLink -Path ".codex\skills\image-gen-pro" -Target "vendor/indieark-skills/image-gen-pro"
```

---

## 更新

```powershell
cd indieark-skills
.\update.ps1
```

`update.ps1` 会执行 `git pull --ff-only` 并重新安装 skill。需要同步 CLI wrapper：

```powershell
.\update.ps1 -InstallCli
```

---

## 兼容性

| Agent / Runtime | Skill 安装位置 | 状态 |
|---|---|---|
| **Codex CLI** | `$env:USERPROFILE\.codex\skills\<name>\` | ✅ 主要测试目标 |
| **Claude Code** | `.claude/skills/<name>/` 或全局 `~/.claude/skills/` | ✅ 兼容（手动复制） |
| **Cursor** | `.agents/skills/<name>/` | ✅ 兼容（手动复制） |
| **Claude.ai (web)** | Settings → Capabilities → Skills | ✅ 兼容（上传 `.zip`） |

> `SKILL.md` 是跨 agent 的可移植格式；只要你的 agent 支持 Agent Skills 规范，把文件夹放到它扫描的目录即可。

---

## 什么是 Skill

一个 **Skill** 是 agent 按需加载的自包含文件夹，核心是 `SKILL.md`（YAML frontmatter + 指令），可选附 references / scripts / assets：

```text
<skill-name>/
├── SKILL.md      ← 必需：何时使用 + 怎么使用
├── README.md     ← 给人看的文档
├── skill.json    ← 元信息（version / cli / 路由 / 阻塞项）
├── references/   ← 可选：agent 按需加载的扩展文档
├── scripts/      ← 可选：确定性可执行脚本
└── assets/       ← 可选：模板、字体、图片
```

agent 是否激活某个 skill，由 frontmatter 的 `description` 决定——所以 description 就是你和 agent 之间的契约。完整规范见 [agentskills.io](https://agentskills.io) 与 [`anthropics/skills`](https://github.com/anthropics/skills) 参考仓库。

---

## 发布维护者指南

私库工作区中，本仓库应放在 `C:\Vibe_Coding\IndieArk\indieark-skills`，与开发源 `C:\Vibe_Coding\IndieArk\skills` 平级。

从私库 runtime 目录刷新本仓库（**注意：会覆盖各 skill 目录**）：

```powershell
.\publish.ps1 -SourceRoot ..\skills
```

刷新后验证：

```powershell
.\install.ps1 -WhatIf
git status --short
git diff --stat
```

`manifest.json` 的 `status` 字段：

- `active` — 正式发布，CLI 与下游执行链完备
- `preview` — v0.1.0-skeleton，SKILL.md / skill.json / references/ 可被 agent 加载，CLI 与下游执行链尚未就位

新增 skill 流程见各私库的 `plans/<编号>-new-skill-<name>.md`。

---

## License

[Proprietary](./LICENSE) © IndieArk
