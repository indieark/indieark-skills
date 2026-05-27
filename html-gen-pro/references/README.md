# References

运行时按需加载下列文件，**不要一次性复制所有内容到回复里**。表格按 S0–S5 状态机顺序排列（详见 [`flows.md`](flows.md)）；同阶段内按"先读 → 后读"排列。

## S0 · 路由触发

| 文件 | Load when | Avoid | Pairs with |
|---|---|---|---|
| [`router.md`](router.md) | 判断用户请求属于 4 路线中哪一条 / 是否要委托 extension / 是否要路由到他处 | 用户未选择路线 / 未通过美学方向门前不要写代码 | `route-introduction.md`, `extensions.md`, `boundary.md`, `flows.md` |
| [`boundary.md`](boundary.md) | 用户请求疑似与 ppt-gen-pro / web-design-guidelines / frontend-design / 风格 Skill 重叠 | 不要在不确定边界时强行接活；不确定就问用户 | `../SKILL.md`, `router.md`, `styles.md` |
| [`flows.md`](flows.md) | 把路由 → 介绍选择 → 安装检查 → 美学方向门 → 委托 → critique 串成可执行状态机 | 不要在本文件复制路由触发词 / 介绍文案 / critique 清单（真源在 router.md / route-introduction.md / critique.md） | `router.md`, `route-introduction.md`, `workflow.md`, `usage.md`, `critique.md`, `reporting.md`, `verify.md` |

## S1 · 标准介绍

| 文件 | Load when | Avoid | Pairs with |
|---|---|---|---|
| [`route-introduction.md`](route-introduction.md) | 每次用户要做真实网页 / 程序前端设计 / 风格 mockup / 已有项目优化时，在委托任何 extension 或写代码前 | 不要把本文件当成最终生成流程；它只负责"4 路线标准介绍 + 推荐理由 + 选择门" | `router.md`, `extensions.md`, `capability-matrix.md`, `install.md`, `usage.md`, `flows.md` |
| [`capability-matrix.md`](capability-matrix.md) | 用户在两条路线之间犹豫 / 需要从硬性约束反查路线 / 评估路线适用度 | 不要把本表当成"全部路线都同时适用"——同一次执行选一条 | `route-introduction.md`, `router.md`, `extensions.md`, `cases.md` |
| [`cases.md`](cases.md) | 路由判定指向 `existing-project-optimize` / 用户提到 IndieArk 子项目名 / 需查项目立场要点 | 不要把本表当成"项目当前实现状态"的真源（实际状态以项目仓库代码为准） | `route-introduction.md`, `router.md`, `extensions.md`, `capability-matrix.md`, `../../../templates/existing-project-optimize-checklist.md` |

## S2 · 用户选择 + 安装检查

| 文件 | Load when | Avoid | Pairs with |
|---|---|---|---|
| [`extensions.md`](extensions.md) | 路线确认为 `landing-page` / `app-frontend` / `style-mockup`（需要外部素材库）/ 想查某 extension 的来源、版本、产物角色 | 不要在本仓库复制 extension 内部的素材库内容；不要在路线判定中绕过 router.md | `router.md`, `install.md`, `usage.md`, `flows.md` |
| [`install.md`](install.md) | 首次使用 / 用户要求安装 / `ui-ux-pro-max` 或 `taste-skill` extension 缺失或需要更新 | 不要手动复制外部仓库内容；不要把 `extensions/` 提交到本仓库；不要在 `existing-project-optimize` 路线下试图安装 extension | `extensions.md`, `usage.md`, `flows.md` |

## S3 · 美学方向门（强制 gate）

| 文件 | Load when | Avoid | Pairs with |
|---|---|---|---|
| [`workflow.md`](workflow.md) | 进入生成请求，按"草稿 → 预览 → 五维评审 → 迭代"流程推进；本文件是**方法论视角**的细节 | 不要跳过"美学方向"直接写大段代码；不要在已有项目里把"试跑产物"和"业务代码"混到一起 | `critique.md`, `styles.md`, `boundary.md`, `flows.md` |
| [`styles.md`](styles.md) | 美学方向阶段，用户对风格无方向；或用户点名某种具体风格想看落地样例 | 不要把全局风格 Skill 的内容复制过来——只能链接 + 一句话定位 | `workflow.md`, `flows.md`, `inspiration.md`, `route-introduction.md`, `extensions.md` |
| [`inspiration.md`](inspiration.md) | 用户想看参考站点 / 风格博物馆 / 别人怎么做的；或美学方向卡住、需要外部素材打开思路 | 不要假装本 Skill 内置 fetch 能直接抓素材——这些是参考源，不是可调用的 API | `styles.md`, `workflow.md`, `flows.md`, `extensions.md`, `cases.md` |

## S4 · 委托 / 起步骨架 / 项目重塑

| 文件 | Load when | Avoid | Pairs with |
|---|---|---|---|
| [`usage.md`](usage.md) | 用户已选定路线（或接受推荐），需进入 S3 美学方向门 → S4 委托 / 起步骨架 → S5 五维 critique | 不要在用户未选择路线前直接读本文件；不要跳过美学方向门直接进入 S4 | `flows.md`, `extensions.md`, `install.md`, `workflow.md`, `critique.md`, `reporting.md` |

## S5 · 五维 critique + 完工汇报 + 可选视觉验证

| 文件 | Load when | Avoid | Pairs with |
|---|---|---|---|
| [`critique.md`](critique.md) | S5 五维评审；或用户要求做 UI critique | 不要把它当成做完才用——草稿前先看维度也行 | `workflow.md`, `reporting.md` |
| [`reporting.md`](reporting.md) | S5 五维 critique 完成、向用户做完工汇报时 | 不要在产物未通过完整性 sanity check 时写汇报；不要让汇报本身代替 critique | `critique.md`, `flows.md`, `usage.md`, `verify.md` |
| [`verify.md`](verify.md) | S5 五维 critique 即将完成 / 用户要求"看一眼实际渲染" / 工程质量维度需截图证据 | 不要把"渲染对就是设计好"——视觉验证只能证否；不要假装看了截图而没真启动 MCP | `flows.md`, `critique.md`, `reporting.md` |

## 加载策略

- **强制 S0**：[`router.md`](router.md) 是入门必读；任何任务先确定路由再决定下一步读哪个。
- **按需扩展**：表格中其余文件按状态机当前阶段加载，**不要批量预加载**。
- **方法论 vs router 视角**：[`workflow.md`](workflow.md)（方法论视角的"为什么"）与 [`flows.md`](flows.md)（router 视角的"这次要做什么"）共存不重复，需要时分别读。
- **本仓库自持 vs 外链**：[`router.md`](router.md) / [`capability-matrix.md`](capability-matrix.md) / [`cases.md`](cases.md) / [`workflow.md`](workflow.md) / [`critique.md`](critique.md) / [`styles.md`](styles.md) 黑名单部分是本仓库自持真源；[`extensions.md`](extensions.md) / [`install.md`](install.md) 是胶水规则；[`styles.md`](styles.md) 路标表 + [`inspiration.md`](inspiration.md) 是外部 / 全局 Skill 链回。
