# Route Introduction

Load when: 每次用户要做真实网页 / 程序前端设计 / 风格 mockup / 已有项目前端优化时，在委托任何 extension 或写代码前加载。
Avoid: 不要把本文件当成最终生成流程；它只负责"4 路线标准介绍 + 推荐理由 + 选择门"。
Pairs with: `router.md`, `extensions.md`, `capability-matrix.md`, `install.md`, `usage.md`, `flows.md`

## Why This Exists

`html-gen-pro` 的首要职责不是直接开始写 HTML，而是先让用户明白 4 种路线的取舍。介绍必须稳定、诚实、可复用：

- **`landing-page`** 是"对外门面"路线，优先保障视觉冲击力与单文件交付。
- **`app-frontend`** 是"工具型 UI"路线，优先保障信息密度、响应式与可用性。
- **`existing-project-optimize`** 是"项目内迭代"路线，优先保障原生栈兼容与业务逻辑零侵入。
- **`style-mockup`** 是"风格落地"路线，优先保障某一特定视觉气质（claymorphism / liquid-glass / brutalism 等）的纯粹度。

## 4 路线详细说明

### `landing-page` — 营销页 / 产品介绍 / 活动页

**适合**：Landing Page、营销页、产品介绍页、个人主页、活动页、Pricing 页、Changelog 页等"对外门面"独立网页。

**Extension**：`nextlevelbuilder/ui-ux-pro-max-skill`（提供 161 industry rules + 67 styles + 161 palettes + 57 font pairings + 99 UX guidelines + 预交付 checklist + section-by-section playbook）。

**模板**：[`../../../templates/landing-page-skeleton/`](../../../templates/landing-page-skeleton/)（hero / features / cta 三段空骨架）。

**默认技术栈**：单文件 HTML + CSS + JS（必要时引 CDN 字体 / Tailwind Play CDN）。

**边界**：不适合内部工具页（→ `app-frontend`）、不适合已有项目改造（→ `existing-project-optimize`）、不适合纯风格演示（→ `style-mockup`）。

### `app-frontend` — Dashboard / Admin / Web App

**适合**：Dashboard 原型、Admin 控制台、Web App 主界面、组件库 mockup、UI Showcase 等"工具型"独立网页。

**Extension**：`nextlevelbuilder/ui-ux-pro-max-skill`（同上；这条路线着重 UX guidelines + 设计系统 + 信息密度模式）。

**模板**：[`../../../templates/dashboard-skeleton/`](../../../templates/dashboard-skeleton/)（sidebar + topbar + grid 主区）。

**默认技术栈**：Vite + React + Tailwind（除非用户指定 Vue / Svelte）。

**边界**：不适合纯对外营销页（→ `landing-page`）、不适合已有项目改造（→ `existing-project-optimize`）。

### `existing-project-optimize` — 已有 IndieArk 项目前端重塑

**适合**：对 `20009-feedback`、`20013-hot`、`1-showcase`、`20005-aigc` 等 IndieArk 子项目的前端目录做迭代优化 / 视觉重塑。

**Extension**：**不绑 extension**。理由：本路线的核心是"跟随项目原生栈"，外部素材库（industry rules / palettes / font pairings）反而是负担，会引入与项目设计系统冲突的元素。本仓库方法论（美学方向门 + 五维 critique + 反 AI slop）足以承担。

**模板**：[`../../../templates/existing-project-optimize-checklist.md`](../../../templates/existing-project-optimize-checklist.md)（不出模板代码，出接入前 checklist）。

**默认技术栈**：跟随该项目原生栈（先 `cat package.json` 或同等确认）。

**边界**：
- 不擅自改业务逻辑 / API 调用 / 路由表；只动视觉与组件层。
- 任何破坏性改动先与用户确认。
- 优化后用 conventional commits 在该项目仓库提交，而不是 IndieArk 根仓库或本 Skill 仓库。

**案例索引**：见 [`cases.md`](cases.md) 的 IndieArk 内部前端项目分组。

### `style-mockup` — 风格落地

**适合**：把具体风格（claymorphism / glassmorphism / liquid-glass / neubrutalism / brutalist / swiss / magazine / editorial / 杂志风 / 终端风 / cyber / Y2K 等）落到可运行 HTML mockup，作为风格演示 / 设计探索 / 风格对比 / 风格预览。

**Extension**：双 extension 并列——`nextlevelbuilder/ui-ux-pro-max-skill`（默认 / 67 styles 库 + 161 palettes + 57 font pairings 广覆盖）/ `Leonxlnx/taste-skill`（在美学方向命中 **brutalist · swiss · luxury(soft)** 时优先委托 / 含 1-10 dials 调参的深度立场子 Skill）。不允许同一次执行混用两个 extension，按美学方向择一委托（取舍规则见 [`extensions.md`](extensions.md) "style-mockup" 段）。

**模板**：[`../../../templates/style-mockup-skeleton/`](../../../templates/style-mockup-skeleton/)（单页 + 风格变量空槽 + 全局风格 Skill 链回）。

**默认技术栈**：单文件 HTML + CSS + JS。

**边界**：不适合需要功能完整性的页面（→ `landing-page` / `app-frontend`）；mockup 默认无真实业务数据。

## Standard User Introduction

对 `generation-request` 使用下面结构，允许按用户语境轻微改写，但不要改变推荐顺序和取舍：

```text
我可以用四种方式做这个网页 / 前端，先帮你选路线：

1. landing-page（营销页 / 产品介绍）
   适合对外门面、Landing Page、Pricing、活动页。单文件 HTML + 视觉冲击优先。会从 ui-ux-pro-max 拉 67 styles + 161 palettes 配色 + 57 font pairing + 161 industry rules 做底，本仓库守住反 AI slop。

2. app-frontend（Dashboard / Admin / Web App）
   适合工具型 UI、控制台、组件库 mockup。Vite + React + Tailwind 默认栈。同样走 ui-ux-pro-max 的设计系统 + UX guidelines。

3. existing-project-optimize（已有项目前端重塑）
   适合优化 IndieArk 子项目（20009-feedback / 20013-hot / 1-showcase / 20005-aigc 等）。跟随项目原生栈，不绑 extension（外部素材库反而是负担）；只动视觉层、不动业务逻辑。

4. style-mockup（风格落地）
   适合 claymorphism / liquid-glass / brutalism / 杂志风 / 终端风等风格演示。单文件 HTML mockup。默认从 ui-ux-pro-max 的 67 styles 库取风格规则；若美学方向命中 brutalist · swiss · luxury(soft)，优先委托 taste-skill（深度立场子 Skill + 1-10 dials 调参）。

无论哪一条，本仓库会强制走 S3 美学方向门（先对齐"气质 + 受众 + 一句话差异化"），完工时按五维 critique（视觉冲击 / 信息层级 / 交互细节 / 工程质量 / 差异化记忆点）自查。

我的建议：{recommendation_sentence}

你可以回复 1 / 2 / 3 / 4，或直接说"按推荐来"。
```

用户选择后不要停在介绍层；读取 [`router.md`](router.md) 与 [`usage.md`](usage.md)，检查 extension 安装状态（landing / app-frontend / style-mockup 路线），按 [`flows.md`](flows.md) S3 进入美学方向门。

## Recommendation Sentences

按 [`router.md`](router.md) 判断后，把 `{recommendation_sentence}` 替换为其中一句：

- 命中子项目名 / "优化前端"："建议走 `existing-project-optimize`，因为你的需求涉及已有项目原生栈，外部素材库反而会引入冲突。"
- 命中具体风格关键词："建议走 `style-mockup`，因为你的需求重点是把某个具体风格落到可运行 HTML 上。默认从 ui-ux-pro-max 的 67 styles 库取规则；若你命中 brutalist · swiss · luxury(soft)，会切到 taste-skill 的深度立场子 Skill（含 1-10 dials 调参）。"
- 命中 "Dashboard / Admin / Web App / 控制台 / 工具页"："建议走 `app-frontend`，因为你的需求是工具型 UI，信息密度和 UX guidelines 比视觉冲击优先。"
- fallback / 命中 "Landing / 营销页 / 介绍页 / Pricing"："建议走 `landing-page`，单文件 HTML + 视觉冲击优先，适合做对外门面。"

## Selection Rules

- 用户消息含 `20009-feedback` / `20013-hot` / `1-showcase` / `20005-aigc` / `tide-spider` 等 IndieArk 子项目名 → 优先推荐 `existing-project-optimize`，跳过通用菜单。
- 用户消息含 "claymorphism / glassmorphism / liquid-glass / neubrutalism / brutalist / swiss / magazine / editorial / 杂志风 / 终端风 / Y2K / cyber" 等具体风格关键词 → 推荐 `style-mockup`。
- 用户消息含 "Dashboard / Admin / Web App / 后台 / 控制台 / 仪表板 / 工具页 / 管理后台" → 推荐 `app-frontend`。
- 用户消息含 "Landing / 营销页 / 产品介绍 / 活动页 / Pricing / 着陆页 / Changelog 页 / 个人主页" → 推荐 `landing-page`。
- 用户同时命中多条路线（如"Landing + brutalism 风格"）→ 给 `style-mockup` 与 `landing-page` 二选一的取舍说明，让用户决定哪个优先。
- 用户只说"做个网页 / 帮我设计个前端"无更多上下文 → 反问"是对外门面（Landing）还是工具型 UI（Dashboard）还是改造已有项目？"，不要盲推。

## 不进入 4 路线菜单的请求（路由到他处）

| 用户表达 | 路由到 |
| ---- | ---- |
| "做 PPT / slides / deck / 网页 PPT / 演示文稿 / Pitch Deck" | `ppt-gen-pro`（[`../../../../ppt-gen-pro/skills/ppt-gen-pro/SKILL.md`](../../../../ppt-gen-pro/skills/ppt-gen-pro/SKILL.md)）|
| "审查我已有 UI 的可访问性 / 合规打分 / 改 lint 警告" | 全局 `web-design-guidelines` |
| "前端设计原则 / 字体怎么挑 / 配色方法论"（无生成需求）| 全局 `frontend-design` |
| 后端 API / CLI / 数据管线 / 业务逻辑 | 对应业务 Skill 或 Claude Code 默认 |

完整边界仲裁规则见 [`boundary.md`](boundary.md)。
