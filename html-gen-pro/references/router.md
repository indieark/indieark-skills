# Router

Load when: 需要判断用户请求属于 4 路线中的哪一条 / 是否要委托 extension / 是否要路由到他处。
Avoid: 不要在用户未选择路线或未通过美学方向门前直接动手写代码。
Pairs with: `route-introduction.md`, `extensions.md`, `install.md`, `boundary.md`, `flows.md`

> **本仓库自持方法论 + 路由**：本文件主导 L1 路线判定；流程状态机详见 [`flows.md`](flows.md)；与他者的边界仲裁详见 [`boundary.md`](boundary.md)。

## Task Types

- `html-design-request`: 用户要做真实网页 / 程序前端设计。
- `style-mockup-request`: 用户要把某个具体风格落成可运行 HTML mockup。
- `existing-frontend-optimize-request`: 用户要优化已有 IndieArk 项目前端。
- `methodology-only-question`: 只问方法论 / 字体 / 配色 / 设计原则——不附带具体生成需求。
- `audit-only-request`: 只审查现有 UI 的合规 / 可访问性 / lint。
- `repository-maintenance`: 补本 Skill 自身的文档 / 规则 / 校验。

## Mandatory Trigger Rule

只要用户消息满足以下任一，就必须触发 `html-gen-pro`，不要让其他网页 / 前端 Skill 先于本 Skill 直接执行：

- 含 "做 / 创建 / 设计 / mockup / 原型 / 重塑 / 优化 / 改" 等动作 + "网页 / 网站 / Landing / 营销页 / 产品介绍 / Dashboard / Admin / Web App / 控制台 / 前端 / UI" 等对象。
- 含 IndieArk 子项目名（`20009-feedback` / `20013-hot` / `1-showcase` / `20005-aigc` / `tide-spider` 等）+ "前端 / UI / 视觉 / 重塑 / 优化"。
- 含具体风格关键词（claymorphism / glassmorphism / liquid-glass / neubrutalism / brutalist / swiss / magazine / editorial / 杂志风 / 终端风 / Y2K / cyber 等）+ 生成意图。
- 用户明确说"不要 AI 味的网页 / 想要 stunning 的网页 / 不要做 PPT，要真网页"。

## Route Menu

每次 `html-design-request` / `style-mockup-request` / `existing-frontend-optimize-request` 都先按 [`route-introduction.md`](route-introduction.md) 展示 4 路线菜单（除非命中"领域特化优先"——目前 v0.2.0 暂无）：

| Route | Extension | 适合 | 默认建议 |
| ---- | ---- | ---- | ---- |
| `landing-page` | `nextlevelbuilder/ui-ux-pro-max-skill` | Landing Page、营销页、产品介绍、活动页、Pricing、Changelog、个人主页 | 对外门面 / 视觉冲击优先 |
| `app-frontend` | `nextlevelbuilder/ui-ux-pro-max-skill` | Dashboard、Admin、Web App、组件库 mockup、UI Showcase | 工具型 UI / 信息密度优先 |
| `existing-project-optimize` | **不绑** extension（跟随项目原生栈）| 已有 IndieArk 项目前端重塑 / 视觉优化 | 项目原生栈 / 零业务逻辑侵入 |
| `style-mockup` | `nextlevelbuilder/ui-ux-pro-max-skill`（默认 / 67 styles 广覆盖）/ `Leonxlnx/taste-skill`（brutalist · swiss · luxury(soft) 命中时优先 / 深度立场） | claymorphism / liquid-glass / brutalism / 杂志风 / Y2K 等具体风格演示 | 风格纯粹度优先 |

## Recommendation Rule

判定顺序：**`existing-project-optimize` → `style-mockup` → `app-frontend` → `landing-page` fallback**。

### 1. 子项目名优先（命中即直推）

用户消息含 IndieArk 子项目名（`20009-feedback` / `20013-hot` / `1-showcase` / `20005-aigc` / `tide-spider` / 其他 `^\d{4,5}-` 模式的子项目名）+ 前端相关动词（"改 / 重塑 / 优化 / 美化 / 视觉"）→ 直接推荐 `existing-project-optimize`，**不绑** extension。

例外：用户明确说"参考 20009-feedback 的风格做一个新的 Landing"（即用现有项目作风格参考但产出独立网页）→ 仍走 `landing-page`，把现有项目作为 inspiration 输入。

### 2. 具体风格关键词优先

用户消息含具体风格关键词（claymorphism / glassmorphism / liquid-glass / neubrutalism / brutalist / swiss / magazine / editorial / 杂志风 / 终端风 / Y2K / cyber / vaporwave 等）→ 推荐 `style-mockup`。

例外：用户同时明确"风格 + 营销页内容"（如"做一个 brutalism 风格的 SaaS Landing"）→ 给 `style-mockup` 和 `landing-page` 二选一的取舍说明：
- `style-mockup` 重风格演示，业务数据占位。
- `landing-page` 重业务交付，风格是手段不是目的。

### 3. 工具型 UI 关键词

用户消息含 "Dashboard / Admin / Web App / 后台 / 控制台 / 仪表板 / 工具页 / 管理后台 / SaaS 后台" → 推荐 `app-frontend`。

### 4. Fallback：`landing-page`

未命中 1-3 时（或明确含 "Landing / 营销页 / 产品介绍 / 活动页 / Pricing"）→ 推荐 `landing-page`。

### 5. 模糊请求（"做个网页 / 帮我设计个前端"无更多上下文）

不要盲推。**反问**：

```text
你想做哪一类？
- 对外门面（Landing / 营销页 / Pricing）→ landing-page
- 工具型 UI（Dashboard / Admin / Web App）→ app-frontend
- 改造已有 IndieArk 项目前端 → existing-project-optimize
- 演示某个具体视觉风格 → style-mockup
```

## Choice Gate

生成前必须问用户选择：

```text
我建议走 `{recommended_route}` 路线，因为 {reason_sentence}。
也可以选：
1. landing-page：对外门面 / Landing / Pricing / 活动页
2. app-frontend：Dashboard / Admin / Web App
3. existing-project-optimize：改造已有 IndieArk 项目前端（不绑 extension，跟随项目原生栈）
4. style-mockup：演示具体视觉风格（claymorphism / liquid-glass / brutalism / 杂志风 等）

你想用哪一种？如果你不确定，我会按推荐路线继续。
```

用户明确选择或接受推荐后，才进入 S3 美学方向门（详见 [`flows.md`](flows.md)）。

## 与其他 Skill 的边界仲裁

完整边界规则真源在 [`boundary.md`](boundary.md)；本节是触发词级仲裁。

| 用户表达 | 仲裁结果 |
| ---- | ---- |
| "做 PPT / slides / deck / 网页 PPT / 演示文稿 / Pitch Deck" | 路由到 `ppt-gen-pro`，**不进入** html-gen-pro 4 路线菜单 |
| "网页 + 演讲 / 网页 + 一屏一镜 / 单文件 deck" | 提示用户："这听起来更像 `ppt-gen-pro` 的 `web-html-ppt` 路线（单文件 HTML deck）；如果你要的是真网页（含多页 / 业务逻辑 / 表单），才走 html-gen-pro。" |
| "审查我已有 UI 的可访问性 / 合规打分 / 改 lint 警告"（无生成需求）| 路由到全局 `web-design-guidelines` |
| "前端设计原则 / 字体怎么挑 / 配色方法论"（无生成需求）| 路由到全局 `frontend-design` |
| "想要 claymorphism 风格的网页"（含生成需求）| 走本 Skill `style-mockup`；同时在 S3 美学方向门时链入全局 claymorphism Skill |
| 后端 API / CLI / 数据管线 / 业务逻辑（无视觉需求）| 路由到对应业务 Skill 或 Claude Code 默认 |
| "把 20009-feedback 的反馈 API 改一下" | 路由出本 Skill；**只动视觉的优化才走** `existing-project-optimize` |

## 否定词清单（避免误触发）

以下关键词命中时，**优先路由出本 Skill**（除非用户在同一消息里也明确含上面的强触发词）：

- "PPT / slides / deck / Pitch Deck / 演示文稿 / 路演稿 / 汇报稿 / 课程课件"（→ `ppt-gen-pro`）
- "审查 / audit / 合规 / 评分 / lint"（无"改 / 重塑 / 优化"动词时 → `web-design-guidelines`）
- "怎么挑字体 / 配色方法论 / 设计原则"（无"做 / 实现"时 → `frontend-design`）
- "API / 接口 / 数据库 / 后端 / CLI / 脚本"（无视觉相关词时 → 业务 Skill 或默认）

## 路由触发词改动治理

- 改动本文件的关键词列表（强触发词、否定词、子项目名匹配模式、风格关键词）必须同步更新 [`../../../scripts/test_router.py`](../../../scripts/test_router.py)（Phase 3 起）的 `REGRESSION_CASES`。
- 测试必须全 PASS（7/7 case：4 路线正例 + 3 否定例）。
- 新增 IndieArk 子项目时在本文件第 1 条规则的子项目名清单中追加；在 [`cases.md`](cases.md) 加案例条目。
