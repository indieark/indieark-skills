# Boundary · 与其他 Skill 的边界

Load when: 用户请求疑似与 `ppt-gen-pro` / 全局 `web-design-guidelines` / 全局 `frontend-design` / 全局风格 Skill 重叠；或本 Skill 触发后发现路由错了想转交。
Avoid: 不要在不确定边界时强行接活；不确定就直接问用户"你要的是 A 还是 B"。
Pairs with: `../SKILL.md`, `styles.md`

## §1 · 与 `ppt-gen-pro`（同 IndieArk）

**最重要的边界**——因为 ppt-gen-pro 也有"网页 PPT / 设计 HTML PPT / 网页演讲"路线，与本 Skill 看上去最像。

| 判定 | ppt-gen-pro | html-gen-pro |
|---|---|---|
| 产物语义 | **幻灯片性质的网页 deck**：按页推进、横向翻页、单文件 HTML、演讲叙事容器 | **真正的产品级网页或应用前端**：多 section、可滚动、可交互、可导航的常规网页 / Dashboard |
| 主要用途 | 路演 / 汇报 / 演讲 / 课件 / Pitch Deck / 演讲网页版 | Landing Page / 营销页 / Dashboard / 已有项目前端优化 |
| 用户语言提示 | "PPT / slides / deck / 演示文稿 / Pitch / 路演稿 / 演讲网页 / 单文件 deck / 一屏一镜 / 网页 PPT" | "网页 / 落地页 / 主页 / 仪表板 / 营销页 / 重做前端 / 重塑 UI / 优化界面" |
| 翻页模型 | 离散页（左右键 / 滚轮触发整页切换） | 连续滚动（垂直长页 / SPA 多视图） |
| 与项目代码 | 不进入业务项目，独立产物 | 可以进入业务项目原代码做迭代 |

**冲突仲裁规则**：

- 用户说"做网页 PPT" → 路由到 `ppt-gen-pro/web-html-ppt`，本 Skill 不接。
- 用户说"做单文件 deck 一屏一页" → 路由到 `ppt-gen-pro/design-html-ppt` 或 `web-html-ppt`。
- 用户说"做一个网页 / 做一个 landing / 优化项目前端" → 本 Skill。
- 用户说"做一个网页演示我的项目"但**没说 PPT 也没说翻页**：默认本 Skill；同时主动确认"你想要可滚动的产品页，还是按页翻的 deck？"。
- 用户先说"网页 PPT"做完后又说"我想把它变成可滚动的产品页" → 这是新需求，**结束 ppt-gen-pro**、**进入 html-gen-pro 重新做**，不要在 ppt 容器上硬改。

## §2 · 与全局 `frontend-design`

全局 `frontend-design` 是**方法论上游**：

| 区分 | 全局 frontend-design | html-gen-pro |
|---|---|---|
| 形态 | 方法论 + 美学方向指引 | 执行入口 + 流程编排 + 五维 critique |
| 用户语言 | "什么是好的前端设计？字体怎么选？怎么避免 AI 味？" | "帮我做一个网页 / 帮我优化这个前端" |
| 是否动手写代码 | 倾向于讨论 + 指导 | 直接写交付 |

**关系**：

- 本 Skill 在 Step 1（美学方向）阶段**引用** `frontend-design` 的 Design Thinking 与 Frontend Aesthetics Guidelines，**不复制**其内容。
- 用户只问"前端设计原则"但没要做东西 → 路由到 `frontend-design`，本 Skill 不接。
- 用户已经在做（本 Skill 主导）但中途问"那字体一般怎么挑" → 直接答（小范围引用上游），不切换 Skill。

## §3 · 与全局 `web-design-guidelines`

全局 `web-design-guidelines` 是**评审上游**（fetch Vercel labs 的最新规则做 file:line 级 audit）：

| 区分 | 全局 web-design-guidelines | html-gen-pro |
|---|---|---|
| 形态 | 审查清单（accessibility / 合规 / 最佳实践） | 设计 + 实现 + 五维 critique |
| 用户语言 | "review my UI / audit / 检查可访问性 / 检查合规" | "做 / 优化 / 重塑" |
| 是否产出新代码 | 只产 review 报告 | 产代码 + 产 critique |

**关系**：

- 本 Skill 走完 5 段式流程，**最终验收阶段**可推荐用户接力到 `web-design-guidelines` 做合规 audit。
- 用户只要 audit、不要设计 → 路由到 `web-design-guidelines`，本 Skill 不接。
- 本 Skill 的"工程质量"维度（critique.md §4）做**现场快查**，深度审查仍接力上游。

## §4 · 与全局风格 Skill（claymorphism / glassmorphism / liquid-glass / neubrutalism）

全局风格 Skill 是**风格素材库**：

- 本 Skill 在美学方向阶段，**链回**到对应风格 Skill 让用户看具体样例和实现要点（详见 [`styles.md`](styles.md)）。
- 不复制风格 Skill 的代码片段或样式表到本仓库。
- 用户明确点名某种风格时，链入对应风格 Skill 的 SKILL.md 一起读。

## §5 · 与 IndieArk 子项目本身

| 子项目 | 本 Skill 边界 |
|---|---|
| `1-showcase/`（官方展示站） | ✅ 可以做前端优化 / 重塑视觉；典型本 Skill 场景 |
| `20009-feedback/` / `20013-hot/` / `20005-aigc/` / `20007-review/` 等含前端的业务项目 | ✅ 可以做前端层优化；**禁止**修改 API 调用、路由表、业务状态管理 |
| `20001-bundle/` / `20003-news/` / `20011-steamlocs/` 等纯后端项目 | ❌ 不触发本 Skill |
| `gadget/` 与 `archive/` | ⚠️ 默认不主动改；用户明确点名时再处理 |
| `00000-model/` / `00000-tutorials/` / `ai-director/` | ❌ 不触发本 Skill（是文档资产库，不是前端项目） |

> 改业务项目时遵守 IndieArk 工作区铁律：业务代码变更优先在对应子目录仓库中提交，**不在根仓库提交业务代码**（参见 [`../../../../../AGENT.md`](../../../../../AGENT.md)）。

## §6 · 与外部社区 Skill（互补接力注册表）

除全局风格 Skill 与 ppt-gen-pro 之外，下列**外部社区 Skill** 被本仓库登记为"互补接力对象"——它们提供本仓库**不打算自建**的能力，本仓库在对应阶段以"链回 + 一句话定位"的形式委托。完整调研档案见 [`../../../docs/research/external-skills.md`](../../../docs/research/external-skills.md)。

| 外部 Skill | 何时接力 | 本仓库链入位置 | 不重复理由 |
|---|---|---|---|
| [`anthropics/skills · webapp-testing`](https://skills.sh/anthropics/skills/webapp-testing) | 验收阶段（S5）做功能验证 / UI 行为调试 / 截图 / 浏览器日志 | [`verify.md`](verify.md) "Playwright MCP 接力指引" | Playwright 工具链已成熟（73.5K installs），本仓库不重复造轮子 |
| [`vercel-labs · web-design-guidelines`](https://skills.sh/vercel-labs/agent-skills/web-design-guidelines) | 完工后做合规审查（spacing / typography / interaction / accessibility 四维硬规则） | 本文件 §3 + [`../SKILL.md`](../SKILL.md) "与其他 Skill 的接力" | 合规审查方法论由 Vercel 官方维护，本仓库不重复 |
| [`vercel-labs · vercel-composition-patterns`](https://skills.sh/vercel-labs/agent-skills/vercel-composition-patterns) | `app-frontend` 路线 S4 写 React 组件结构时 | （建议）后续在 [`router.md`](router.md) `app-frontend` 行 + [`workflow.md`](workflow.md) S4 段补一句路标 | React 组合模式是上游通用知识，不属于本仓库方法论资产 |
| [`luukalleman/premium-design-skill`](https://github.com/luukalleman/premium-design-skill)（Kinetic Luxe） | 美学方向阶段（S3）确定为 **editorial & magazine** 或 **luxury & refined** 风格时 | [`styles.md`](styles.md) "无 Skill 风格" 表 editorial / luxury 两行 | 13 个原创 editorial-luxe 组件 + serif display + 异步排版，已成型，本仓库不自建该风格素材库 |
| [`Leonxlnx/taste-skill · brutalist-skill`](https://github.com/Leonxlnx/taste-skill) | **已 extension 化** — 美学方向阶段（S3）确定为 **brutalist & raw** 或 **swiss & grid** 风格时，S4 自动委托 | [`styles.md`](styles.md) "无 Skill 风格" 表 brutalist / swiss 两行；自动委托见 [`extensions.md`](extensions.md) "style-mockup" 段 | hard mechanical + Swiss type + 锐对比已成型；本仓库不自建该风格素材库 |
| [`Leonxlnx/taste-skill · soft-skill`](https://github.com/Leonxlnx/taste-skill) | **已 extension 化** — 美学方向阶段（S3）确定为 **luxury & refined** 且气质偏 calm / softer contrast / spring motion 时，S4 自动委托 | [`styles.md`](styles.md) "无 Skill 风格" 表 luxury 行（与 premium-design-skill 并列第二选项）；自动委托见 [`extensions.md`](extensions.md) "style-mockup" 段 | premium-design-skill 偏 editorial-luxe（接力模式），soft-skill 偏 calm-premium（extension 模式），气质分流 |
| [`Leonxlnx/taste-skill · redesign-skill`](https://github.com/Leonxlnx/taste-skill) | `existing-project-optimize` 路线 S3–S4 阶段做"先审 UI 再修"流程参考（**接力模式**——未 extension 化，由 Agent 引导用户启用） | [`router.md`](router.md) `existing-project-optimize` 行（建议追加路标） | 同路线的"audit-first then fix"框架可作为本仓库方法论的外部对照；不进入 EXTENSIONS 列表以保持 existing-project-optimize 路线 unbound |
| [`Leonxlnx/taste-skill · brandkit`](https://github.com/Leonxlnx/taste-skill) | IndieArk 子项目走 0→1 品牌建立流程（logo / 调色板 / 字体 / 应用板）时（**接力模式**） | 本仓库**不覆盖品牌套装方向**，全权 delegate | 内置 brandkit + 2 个 imagegen Skill，本仓库不自建 |

**接力协议**：

- **不复制**外部 Skill 的方法论 / 组件代码到本仓库，只链回。
- **不在路由层硬接管**外部 Skill 的能力域——例如美学方向选定 editorial 后，由 Agent 主动建议用户启用 premium-design-skill 而非"假装本仓库内置 editorial 素材库"。
- **快照管理**：所有外部 Skill 的当前状态、`verified_date`、`source` 字段在 [`../../../docs/research/external-skills.md`](../../../docs/research/external-skills.md) 维护；本表只保留"接力关系"，不保留版本信息。
- **混合定位说明**（2026-05-27 三次刷新起）：本表 §6 同时含**接力**与**已 extension 化**两类外部 Skill——`taste-skill/brutalist-skill` 与 `taste-skill/soft-skill` 已升级为本仓库第 2 个 extension（与 `ui-ux-pro-max` 并列），S4 自动委托不再依赖用户启用；`taste-skill/redesign-skill` + `taste-skill/brandkit` + `premium-design-skill` + `vercel-composition-patterns` + `web-design-guidelines` + `webapp-testing` 6 项保留**接力模式**。判定方法：看"何时接力"列首是否标 **已 extension 化**。

> 与 [`extensions.md`](extensions.md) 的区别：`extensions.md` 注册的是"**会本地 clone + 版本锁 + 在 S4 由本 Skill 自动调用**"的 extension（当前 `ui-ux-pro-max` 与 `taste-skill` 两个，后者只在 `style-mockup` 路线启用）；本表 §6 注册的是"**由 Agent 在对话内引导用户切换 Skill**"的接力对象。两套机制**共存**：同一个上游仓库（如 taste-skill）可有部分子 Skill 走 extension、部分子 Skill 走接力，由本表"何时接力"列首标识区分。
