# Capability Matrix

Load when: 用户在两条路线之间犹豫 / 需要从硬性约束反查路线 / 评估路线适用度。
Avoid: 不要把本表当成"全部路线都同时适用"的暗示——同一次执行选一条路线。
Pairs with: `route-introduction.md`, `router.md`, `extensions.md`, `cases.md`

## 4 路线 × 8 维度对比

| 维度 | `landing-page` | `app-frontend` | `existing-project-optimize` | `style-mockup` |
| ---- | ---- | ---- | ---- | ---- |
| 输出形态 | 单文件 HTML（hero / features / cta）| Vite + React app（sidebar / topbar / grid）| 项目原生形态（按 package.json）| 单文件 HTML（单页面风格演示）|
| 单/多文件 | 单文件优先 | 多文件（标准前端工程结构）| 跟随项目（多数多文件）| 单文件 |
| 设计系统支持 | 中（页面级配色 + 字体）| **高**（design token + 组件 spec + UX guidelines）| **跟随项目**（不重建）| 低（风格变量空槽，重风格不重系统）|
| a11y 检查 | 完工时手工自查（语义 HTML + 对比度 + 焦点）| 完工时手工自查（含键盘导航 + 状态反馈）| **必查**（不破坏项目已有 a11y）| 弱（mockup 默认无完整 a11y 要求）|
| 响应式 | 必备（mobile-first）| 必备（≥3 断点：mobile / tablet / desktop）| 跟随项目断点策略 | 可选（mockup 可只做 desktop 演示）|
| 视觉验证可行性 | **高**（单文件，Playwright MCP 直接载入）| 中（需先 `npm run dev`，再 MCP 取截图）| 跟随项目运行链路 | **高**（单文件）|
| 与项目代码耦合度 | 零（独立 demo）| 零（独立 demo）| **高**（直接改项目目录）| 零（独立 mockup）|
| 推荐场景 | 对外门面 / 营销 / Pricing / Changelog | Dashboard / Admin / 工具型 UI | IndieArk 子项目前端重塑 | 风格演示 / 设计探索 |

## 按硬性约束反查路线

### "单文件交付" 是硬约束

→ `landing-page` 或 `style-mockup`。
- 偏业务交付：`landing-page`。
- 偏风格演示：`style-mockup`。

### "工具型 UI 信息密度高" 是硬约束

→ `app-frontend`。
- 99 UX guidelines + 设计系统生成器在这里价值最大。

### "已有项目原生栈不能换" 是硬约束

→ `existing-project-optimize`。
- 不绑 extension（外部素材库会引入冲突元素）。
- 只动视觉与组件层；不动业务逻辑。
- 走 [`../../../templates/existing-project-optimize-checklist.md`](../../../templates/existing-project-optimize-checklist.md) 接入前 checklist。

### "某个具体视觉风格的纯粹度" 是硬约束

→ `style-mockup`。
- 风格关键词命中：claymorphism / glassmorphism / liquid-glass / neubrutalism / brutalist / swiss / magazine / editorial / 杂志风 / 终端风 / Y2K / cyber / vaporwave 等。

### "完工要做视觉验证" 是硬约束

→ 优先 `landing-page` / `style-mockup`（单文件最容易载入 Playwright MCP）；其次 `app-frontend`（需 dev server）；最后 `existing-project-optimize`（跟随项目运行链路，可能不支持 MCP）。

### "零业务逻辑侵入" 是硬约束

→ `existing-project-optimize`。强制只动视觉与组件层；任何破坏性改动先与用户确认。

## 路线冲突时的取舍

| 用户表达 | 取舍 |
| ---- | ---- |
| "brutalism 风格的 SaaS Landing" | `style-mockup`（风格演示，业务数据占位）vs `landing-page`（业务交付，风格是手段）。问用户：风格纯粹度 vs 业务可用性，哪个优先？ |
| "Dashboard 但只是 mockup" | `app-frontend`（功能完整）vs `style-mockup`（风格演示）。问用户：要功能流转还是只要静态视觉？ |
| "把 20009-feedback 的风格改成 claymorphism" | `existing-project-optimize`（项目内重塑，必须接受项目现有架构）；同时调用 claymorphism 全局 Skill 做风格规则。**不要** 切到 `style-mockup`（不能用占位数据替换真实项目）。 |
| "Landing 但要重用 20009-feedback 的 reaction 组件" | `landing-page`（独立网页）+ 在 S3 把 20009-feedback 作为 inspiration / 引用；但**不直接**改 20009-feedback 仓库（那是 `existing-project-optimize` 的领域）。|

## 与 ppt-gen-pro 的能力差异提醒

如果用户表达里含"网页演示 / 网页 deck / 单文件 HTML 演讲 / 一屏一镜 / 杂志风网页 deck"——这些**通常属于 `ppt-gen-pro` 的 `web-html-ppt` 路线**，**不是** html-gen-pro 的任何路线。仲裁规则：

- 容器是"演讲叙事的 deck"（横向翻页 + slide nav） → `ppt-gen-pro/web-html-ppt`。
- 容器是"网站 / 应用 / 工具 / 营销页"（含表单 / 业务流 / 多页路由） → html-gen-pro 的某条路线。

完整边界见 [`boundary.md`](boundary.md)。
