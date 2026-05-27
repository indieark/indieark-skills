---
name: html-gen-pro
description: Mandatory full-function web page and program frontend design skill (methodology + cases + templates + flows + extension routing). Use whenever the user wants to create or optimize a real web page, landing page, marketing page, dashboard, web app UI, or the frontend of an existing IndieArk project. Routes among landing-page, app-frontend, existing-project-optimize, and style-mockup; recommends one; asks the user to choose; gates on aesthetic direction; runs a five-axis critique; and delegates to the ui-ux-pro-max or taste-skill extension when external asset libraries or style child Skills are needed. Distinct from PPT/slide decks (route to ppt-gen-pro), pure methodology asks (frontend-design), and pure review/audit asks (web-design-guidelines). The bar is "stunning + runnable," not just "functional."
---

# html-gen-pro

## 触发条件

当用户的请求落入以下任一场景时，必须触发本 Skill：

- 创建独立网页：Landing Page、营销页、产品介绍页、个人主页、活动页、Pricing 页、Changelog 页。
- 设计应用前端：Dashboard 原型、Admin 控制台、Web App 主界面、组件库 mockup、UI Showcase。
- **对已有 IndieArk 项目的前端做迭代优化 / 视觉重塑**：`20009-feedback`、`20013-hot`、`1-showcase`、`20005-aigc` 等子项目的前端目录。
- 风格 mockup / 设计稿：把 claymorphism / glassmorphism / liquid-glass / neubrutalism / brutalist / swiss / magazine / editorial 等具体风格落到可运行 HTML 上。
- 用户明确说"我想要一个 stunning 的网页 / 不要 AI 味的网页 / 这个前端太普通了帮我重塑 / 不要做 PPT，要真网页"。

## 不触发（路由到他处）

- "做 PPT / slides / deck / 网页 PPT / 演示文稿 / Pitch Deck" → [`ppt-gen-pro`](../../../ppt-gen-pro/skills/ppt-gen-pro/SKILL.md)
- 只要"审查我已有 UI 的可访问性 / 合规打分 / 改 lint 警告" → 全局 `web-design-guidelines`
- 只问"前端设计原则 / 字体怎么挑 / 配色方法论"——不附带具体生成需求 → 全局 `frontend-design`
- 后端 API、CLI、数据管线、业务逻辑：路由到对应业务 Skill 或直接走 Claude Code 默认能力

详见 [`references/boundary.md`](references/boundary.md)。

## 定位（v0.2.0 router-alpha）

本 Skill 是**全功能 Skill**：**方法论中心 + 案例库 + 模板库 + 流程引导 + 功能路由**五位一体。它**不是**纯胶水路由器（不退化为只委托 extension），也不是只讲方法论的"沉默 Skill"——本仓库自持以下资产：

- **方法论中心**（不外包）：美学方向门、五段方法论流程、五维 critique、反 AI slop 立场、风格 Skill 路标、边界仲裁规则。
- **案例库**（不外包）：IndieArk 内部前端项目案例索引（`references/cases.md`）。
- **模板库**（不外包）：起步骨架 boilerplate（[`../../templates/`](../../templates/)）。
- **流程引导**：S0–S5 状态机（[`references/flows.md`](references/flows.md)）。
- **功能路由**：4 条 L1 路线 + 2 个 extension（`ui-ux-pro-max` 主力 / `taste-skill` 在 `style-mockup` 路线作为 brutalist · swiss · luxury(soft) 风格的深度立场分流）。

> 与 `ppt-gen-pro`（纯胶水路由器）的关键差异、四层模型详见 [`../../docs/architecture/model-vs-methodology.md`](../../docs/architecture/model-vs-methodology.md)。

## 四种 L1 路线

每次用户提出网页 / 前端优化需求时，都要按 [`references/route-introduction.md`](references/route-introduction.md) 的标准介绍先说明取舍，并让用户选择或接受推荐：

1. **`landing-page`**：营销页 / 产品介绍页 / 活动页 / Pricing / Changelog 等"对外门面"独立网页。Extension = `ui-ux-pro-max`；模板 = [`../../templates/landing-page-skeleton/`](../../templates/landing-page-skeleton/)。
2. **`app-frontend`**：Dashboard / Admin / Web App 主界面 / 组件库 mockup / UI Showcase 等"工具型"独立网页。Extension = `ui-ux-pro-max`；模板 = [`../../templates/dashboard-skeleton/`](../../templates/dashboard-skeleton/)。
3. **`existing-project-optimize`**：对已有 IndieArk 子项目前端做迭代优化 / 视觉重塑。**不绑 extension**（跟随项目原生栈，外部素材库反而是负担）；只走本仓库方法论 + [`../../templates/existing-project-optimize-checklist.md`](../../templates/existing-project-optimize-checklist.md) 接入前 checklist。
4. **`style-mockup`**：把具体风格（claymorphism / glassmorphism / liquid-glass / neubrutalism / brutalist / swiss / magazine / editorial / luxury(soft) 等）落到可运行 HTML mockup。Extension = `ui-ux-pro-max`（67 styles 库，默认）**或** `taste-skill`（brutalist / swiss / luxury(soft) 命中时优先，深度立场子 Skill）；模板 = [`../../templates/style-mockup-skeleton/`](../../templates/style-mockup-skeleton/)。取舍规则见 [`references/extensions.md`](references/extensions.md) "style-mockup" 段。

默认推荐顺序：先 `existing-project-optimize`（命中子项目名时优先），再 `style-mockup`（命中具体风格关键词时优先），再 `app-frontend`（"Dashboard / Admin / Web App" 关键词），最后 `landing-page`（fallback）。完整判定规则与冲突仲裁见 [`references/router.md`](references/router.md)。

## 设计哲学（Bar = "Stunning + Runnable"）

本 Skill 继承 `ConardLi/garden-skills/web-design-engineer` 的核心立场：

> "The bar is 'stunning,' not 'functional.'"

但延展到 IndieArk 场景：交付物的最低标准是 **"视觉惊艳 + 真的能跑 + 不重复 AI 味"**。具体要求：

1. **承担美学方向决断**：每一个交付都要先明确"这是哪种气质"（参考全局 `frontend-design` 的 Design Thinking + 本 Skill `references/styles.md` 的风格链回）；不允许同质化。
2. **真的能运行**：单文件 HTML 也好、Vite + React 也好，产物开箱即用、不依赖凭空假设的接口。
3. **反 AI slop**：禁用 Inter / Roboto / 紫色渐变白底 / 通用 hero+grid 套版（详见 [`references/critique.md`](references/critique.md) 的"差异化记忆点"维度与 [`references/styles.md`](references/styles.md) 的具体清单）。
4. **优化已有项目时不破坏运行**：跟随原生技术栈、保留业务逻辑入口、明确告知改了哪些文件。

## 使用流程（S0–S5 状态机）

按以下状态机走，**每一段都有可观察成果**。详细流程见 [`references/flows.md`](references/flows.md)（router 视角状态机）与 [`references/workflow.md`](references/workflow.md)（方法论视角细节）：

1. **S0 · 路由触发**：识别意图，进入本 Skill；读取 [`references/README.md`](references/README.md)。
2. **S1 · 标准介绍**：按 [`references/route-introduction.md`](references/route-introduction.md) 介绍 4 条路线 + 推荐一条 + 提出选择问题。
3. **S2 · 用户选择**：等用户拍板或接受推荐；命中 extension 路线时按 [`references/install.md`](references/install.md) 检查 `ui-ux-pro-max`（所有 extension 路线必备）和 `taste-skill`（`style-mockup` 路线且气质命中 brutalist / swiss / luxury(soft) 时才必备）是否安装。
4. **S3 · 美学方向门**（强制）：按 [`references/workflow.md`](references/workflow.md) §1 与 [`references/styles.md`](references/styles.md) 与用户对齐"气质 + 受众 + 一句话差异化"；**未对齐前禁止写大段代码**。
5. **S4 · 委托 / 起步骨架 / 项目内重塑**：
   - extension 路线 → 委托对应 extension（默认 `ui-ux-pro-max`；`style-mockup` 路线且气质命中 brutalist / swiss / luxury(soft) 时改委托 `taste-skill` 对应子 Skill。入口与取舍见 [`references/usage.md`](references/usage.md) + [`references/extensions.md`](references/extensions.md) "style-mockup" 段）+ 可选拉 [`../../templates/`](../../templates/) 起步骨架做底。
   - `existing-project-optimize` 路线 → 跟随项目原生栈，先过 [`../../templates/existing-project-optimize-checklist.md`](../../templates/existing-project-optimize-checklist.md)，直接改对应项目目录。
6. **S5 · 五维 critique + 完工汇报**：按 [`references/critique.md`](references/critique.md) 五个维度自查（**差异化记忆点强制必答**），按 [`references/reporting.md`](references/reporting.md) 模板汇报；可选用 [`references/verify.md`](references/verify.md) 走 Playwright MCP 视觉验证。

## 产物归宿

- **试跑 / 一次性 Demo / mockup**：默认落在 `_work/html_runs/<slug-or-timestamp>/`，对齐 `image-gen-pro` 的 `_work/image_gen_runs/` 与 `video-gen-pro` 的 `_work/seedance_upload/`。本地留痕，不进 Git。
- **优化已有 IndieArk 项目前端**：**直接改对应项目目录**（如 `20009-feedback/`、`1-showcase/`），不在本 Skill 落副本，避免双向漂移。
  - 修改前先确认该项目仓库当前状态（git status），把改动控制在用户授权的范围内。
  - 优化后用 conventional commits 在该项目仓库提交，而不是 IndieArk 根仓库。

## 技术栈策略

**不绑定**。按场景跟随：

| 场景 | 默认技术栈 | 理由 |
|---|---|---|
| `landing-page` / `style-mockup` | 单文件 HTML + CSS + JS（必要时引 CDN 字体 / Tailwind Play CDN）| 一文件好交付，无构建链路 |
| `app-frontend` | Vite + React + Tailwind（除非用户指定 Vue / Svelte）| 上下游生态完善 |
| `existing-project-optimize` | **跟随该项目原生栈**（先 `cat package.json` 或同等确认）| 不引入新依赖避免长期维护负担 |

读取 [`references/workflow.md`](references/workflow.md) §2 获取选型决策细则；[`references/capability-matrix.md`](references/capability-matrix.md) 提供 4 路线 × 8 维度对比。

## Red Lines

- 不在用户未确认"美学方向"前直接动手写大段代码（避免方向跑偏要重写）。
- 不复制任一 extension 的素材方法论到本仓库——`ui-ux-pro-max` 的 industry rules / 67 styles / 161 palettes / 57 font pairings / 99 UX guidelines / 预交付 checklist / section-by-section playbook 与 `taste-skill` 的 brutalist · swiss · soft 子 Skill 实现代码 / 1-10 dials / image-first pipeline 都只链回。
- 不复制全局 `frontend-design` / `web-design-guidelines` / 风格 Skill 的内容到本仓库——只链回。
- 不假装自己能看截图 / 跑浏览器：除非确实启动了 Playwright MCP 或自动化工具，否则明说"建议你本地预览验证"。
- 不在生产业务模块的目录里写"一次性 Demo"；试跑产物只去 `_work/html_runs/`。
- 修改已有项目前端时，不擅自改业务逻辑、API 调用、路由表；只动视觉与组件层；任何破坏性改动先与用户确认。
- 不提交 secrets、未授权字体、未授权图像、客户资料、生成产物的中间文件。
- **不替代 `ppt-gen-pro`**：用户要"网页 PPT / 单文件 deck / 演讲叙事容器"时主动转交，不要在本 Skill 里"顺便"做 deck。
- **不在用户未选择路线前直接动手**（v0.2.0 起 S0→S1→S2 强制 gate）。

## 与其他 Skill 的接力

- 完工后想做合规审查 → 推荐用户在同会话里调用 `web-design-guidelines`，把产物路径传过去。
- 想找具体风格灵感 → 在 [`references/styles.md`](references/styles.md) 中按需链入全局风格 Skill；外部素材主库链回 ui-ux-pro-max（67 styles 广覆盖）或 taste-skill（brutalist / swiss / luxury(soft) 深度立场）。
- 想要"演讲式叙事网页 deck" → 明确告知用户应改用 `ppt-gen-pro` 的 `web-html-ppt` 路线。
- 完工后想做视觉验证 → [`references/verify.md`](references/verify.md) 提供 Playwright MCP 接力指引（`claude mcp add @playwright/mcp` + 3 个 prompt 模板）。

## 元数据

详见 [`skill.json`](skill.json)。
