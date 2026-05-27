# html-gen-pro Skill

这是可安装的 Skill 包（canonical installable Skill package）。当你只拿到这个包目录（脱离 IndieArk 主仓库）时，看这个 README 起步。

## 这是什么

一个**全功能网页与程序前端设计 Skill**：方法论中心 + 案例库 + 模板库 + 流程引导 + 功能路由五位一体。

定位：交付物的最低标准是「视觉惊艳 + 真的能跑 + 不重复 AI 味」。不是「能渲染就行」。

## 谁该用 / 何时触发

用户请求落入以下任一场景时，自动触发本 Skill：

- 做独立网页：Landing / 营销 / Pricing / 个人主页 / 活动页
- 设计应用前端：Dashboard / Admin / Web App / 组件库 mockup
- 对已有项目前端做迭代优化 / 视觉重塑
- 风格 mockup：把 claymorphism / glassmorphism / brutalist / swiss / cyberpunk 等具体风格落到可运行 HTML

不触发：做 PPT/slides 路由到 `ppt-gen-pro`；只问设计原则路由到 `frontend-design`；只做 UI 审查路由到 `web-design-guidelines`。

## 包内结构

- `SKILL.md` — 给 Agent 读的强制执行协议。**这是真源**，本 README 只是人类入口。
- `references/` — 路由 / 方法论 / 风格 / 案例 / critique / 报告 / 验证 / 安装等懒加载子文档。
- `agents/openai.yaml` — OpenAI Agent 平台兼容元数据（跨 Anthropic / OpenAI / 其他 Agent 平台移植用）。
- `examples/` — 真实跑通的产物长期收录（每条 L1 路线至少 1 条）。
- `skill.json` — 机器可读元数据（版本号、capability 列表）。

## 4 条 L1 路线（一句话）

1. `landing-page` — 营销页 / 产品介绍 / Pricing。委托 `ui-ux-pro-max`。
2. `app-frontend` — Dashboard / Admin / Web App。委托 `ui-ux-pro-max`。
3. `existing-project-optimize` — 改已有项目前端。**不绑 extension**（跟随原生栈）。
4. `style-mockup` — 风格落地 mockup。命中 brutalist / swiss / luxury(soft) 时委托 `taste-skill`，其余委托 `ui-ux-pro-max`。

## 强制 5 段流程（S0–S5）

S0 路由触发 → S1 标准介绍 4 路线 + 推荐 → S2 用户选择 + extension 安装检查 → **S3 美学方向门（强制 gate，未对齐前不允许写代码）** → S4 委托 / 起步骨架 / 项目内重塑 → S5 五维 critique + 完工汇报。

第 5 维「差异化记忆点」是强制必答，禁止模糊词（"现代 / 简约 / 用户友好" 都算 AI slop）。

## 反 AI slop 立场

- 禁用字体：Inter / Roboto / Arial / system-ui
- 禁用配色：白底 + 紫渐变 + 灰卡片
- 禁用版式：hero + 三列卡片 + CTA + footer 套版
- 禁用 hover：`translateY(-4px)` + 软阴影
- 禁用文案：「Build, Ship, Scale」「The future of X」

完整黑名单见 `references/styles.md` 与 `references/critique.md`。

## 怎么开始

让 Agent 按用户请求触发即可。Agent 会先读 SKILL.md → 跟着 S0-S5 走。

需要看真实产物长什么样：翻 `examples/` 任一条；需要看路由细节：读 `references/router.md`；需要看怎么委托 extension：读 `references/usage.md`。
