# Usage

Load when: 用户已经选定路线（或接受推荐），需要进入 S3 美学方向门 → S4 委托 / 起步骨架 → S5 五维 critique。
Avoid: 不要在用户未选择路线前直接读本文件；不要跳过美学方向门直接进入 S4。
Pairs with: `flows.md`, `extensions.md`, `install.md`, `workflow.md`, `critique.md`, `reporting.md`

## S0–S5 状态机下的资源映射

详细状态机定义见 [`flows.md`](flows.md)；本文件是"每个阶段读什么 / 调用什么 / 委托给谁"的速查表。

| 阶段 | 阶段名 | 读什么 | 调用 / 委托 | 输出 |
| ---- | ---- | ---- | ---- | ---- |
| S0 | 路由触发 | [`README.md`](README.md) | [`router.md`](router.md) Mandatory Trigger Rule 自查 | 进入本 Skill 的确认 |
| S1 | 标准介绍 | [`route-introduction.md`](route-introduction.md) | 输出 4 路线介绍 + 推荐句 + 选择问题 | 用户选择或接受推荐 |
| S2 | 用户选择 + 安装检查 | [`install.md`](install.md), [`extensions.md`](extensions.md) | `python scripts/install_extensions.py --check-only`（landing / app-frontend → 仅检 ui-ux-pro-max；style-mockup → 检 ui-ux-pro-max + taste-skill 双 extension）| extension 就绪态或缺失提示 |
| S3 | 美学方向门 | [`workflow.md`](workflow.md) §1, [`styles.md`](styles.md), [`inspiration.md`](inspiration.md) | 与用户对齐"气质 + 受众 + 一句话差异化" | 美学方向描述（不少于 3 句话）|
| S4 | 委托 / 起步骨架 / 项目重塑 | 见下方各路线分支 | 见下方各路线分支 | 可运行产物（HTML / React app / 项目内改动）|
| S5 | 五维 critique + 完工汇报 | [`critique.md`](critique.md), [`reporting.md`](reporting.md), 可选 [`verify.md`](verify.md) | 五维 critique 自查 + 完工汇报模板 | critique 报告 + 完工汇报 |

## S4 各路线的委托路径

### `landing-page` 路线

1. 打开 [`extensions/ui-ux-pro-max/SKILL.md`](../../../extensions/ui-ux-pro-max/SKILL.md)（Phase 3 安装后存在；首次端到端验证时确认实际入口路径并回填到 [`extensions.md`](extensions.md) Registry）。
2. 在 prompt 里显式声明 "Route = landing-page; mode = marketing landing page"，让 ui-ux-pro-max 加载 **161 industry rules + 预交付 checklist + section-by-section playbook**。
3. 把 S3 锁定的美学方向作为输入传给 extension：行业（SaaS / 电商 / 内容 / 工具 / 教育 等）+ 风格（67 styles 里选 1-2）+ 配色（161 palettes 里选 1）+ 字体对（57 font pairings 里选 1）。
4. 起步骨架基底：可拉 [`../../../templates/landing-page-skeleton/`](../../../templates/landing-page-skeleton/)（hero / features / cta 三段空骨架）作 fast-start。
5. 产物落点：`_work/html_runs/<slug-or-timestamp>/`。

### `app-frontend` 路线

1. 打开 `extensions/ui-ux-pro-max/SKILL.md`。
2. prompt 里声明 "Route = app-frontend; mode = dashboard / admin / web app"，让 ui-ux-pro-max 加载 **99 UX guidelines + 设计系统生成器**。
3. 把 S3 锁定的美学方向 + 信息密度模式（dense / spacious / 平衡）+ 主功能模块清单作为输入。
4. 起步骨架基底：可拉 [`../../../templates/dashboard-skeleton/`](../../../templates/dashboard-skeleton/)（sidebar + topbar + grid 主区）。
5. 默认技术栈 Vite + React + Tailwind；除非用户指定 Vue / Svelte。
6. 产物落点：`_work/html_runs/<slug-or-timestamp>/`。

### `existing-project-optimize` 路线（**不调用 extension**）

1. **先**过 [`../../../templates/existing-project-optimize-checklist.md`](../../../templates/existing-project-optimize-checklist.md) 接入前 checklist（含 git status / package.json / 路由表 / 设计系统现状 / 业务逻辑入口）。
2. `cat <project>/package.json` 确认原生栈；在 [`cases.md`](cases.md) 查该项目的接入注意事项与立场要点。
3. S3 美学方向门基础上加一条："新方向是否与项目现有设计系统兼容？不兼容时是否要切到 style-mockup 路线做独立 mockup？"
4. **改动范围只限视觉与组件层**：不动业务逻辑、API 调用、路由表、数据流。
5. 产物落点：**直接改对应项目目录**（如 `20009-feedback/`、`1-showcase/`）；本 Skill 不留副本。
6. 提交：用 conventional commits 在该项目仓库提交，**不在 IndieArk 根仓库或本 Skill 仓库提交**。

### `style-mockup` 路线

本路线**双 extension 并列**，按 S3 锁定的美学方向择一委托（**不允许同一次执行混用两个 extension**）：

**分支 A（默认 / 广覆盖）—— 委托 `ui-ux-pro-max`**

适用美学方向：claymorphism / glassmorphism / liquid-glass / neubrutalism / magazine / 杂志风 / 终端风 / Y2K / cyber / vaporwave 等 67 styles 库覆盖的风格。

1. 打开 `extensions/ui-ux-pro-max/SKILL.md`。
2. prompt 里声明 "Route = style-mockup; style = <风格名>"，让 ui-ux-pro-max 加载 **67 styles 库**对应风格规则 + 161 palettes + 57 font pairings。
3. 同时 S3 时**链入全局风格 Skill**：claymorphism / glassmorphism / liquid-glass / neubrutalism 等（详见 [`styles.md`](styles.md)）。

**分支 B（深度立场 / 风格空缺填补）—— 委托 `taste-skill`**

适用美学方向：**brutalist · swiss · luxury(soft)**（具体触发条件见 [`extensions.md`](extensions.md) "style-mockup" 段；社区空缺风格 brutalist / swiss + luxury 的第二选项走此分支）。

1. 打开 `extensions/taste-skill/README.md` 总入口，由 Agent 在 S4 按美学方向选取对应子 Skill 入口：
   - brutalist · swiss → `extensions/taste-skill/brutalist-skill/SKILL.md`（install name `industrial-brutalist-ui`）
   - luxury(soft) → `extensions/taste-skill/soft-skill/SKILL.md`（install name `high-end-visual-design`）
2. prompt 里声明 "Route = style-mockup; style = <风格名>; dials = {DESIGN_VARIANCE: 1-10, MOTION_INTENSITY: 1-10, VISUAL_DENSITY: 1-10}"——dials 由 Agent 与用户在 S3 美学方向阶段协商默认值，taste-skill 子 Skill 内部按 dials 落地。
3. 不需要再链入全局风格 Skill（taste-skill 子 Skill 已自持立场）。

**两分支共同点**：

4. 起步骨架基底：可拉 [`../../../templates/style-mockup-skeleton/`](../../../templates/style-mockup-skeleton/)（单页 + 风格变量空槽）。
5. mockup 默认 desktop 单尺寸；除非用户要求响应式演示。
6. 产物落点：`_work/html_runs/<slug-or-timestamp>/`。

## 委托时的 prompt 模板

### 对 `ui-ux-pro-max` 委托时（landing-page / app-frontend / style-mockup 默认分支）

```text
我现在在 html-gen-pro 的 {route} 路线下委托你，请按以下输入生成：

【美学方向】（S3 锁定结果）
- 气质：{vibe_description}
- 受众：{audience}
- 一句话差异化：{unique_angle}

【硬性约束】
- 行业：{industry}（若 landing-page 路线）
- 风格：{style_name}（若 style-mockup 路线）
- 信息密度：{density_mode}（若 app-frontend 路线）

【起步骨架】
- 基底已用 templates/{skeleton_name}/，可在此基础上扩展。

【反 AI slop 立场】
- 禁用：Inter / Roboto / 紫色渐变白底 / 通用 hero+grid 套版（详见 html-gen-pro 的 styles.md 黑名单）。
- 差异化记忆点必须有一句话能说清。

【产物落点】
- _work/html_runs/{slug}/
```

### 对 `taste-skill` 子 Skill 委托时（style-mockup 路线 brutalist · swiss · luxury(soft) 分支）

```text
我现在在 html-gen-pro 的 style-mockup 路线下委托你（taste-skill / {sub_skill_name}），请按以下输入生成：

【美学方向】（S3 锁定结果）
- 气质：{vibe_description}（命中 brutalist / swiss / luxury-soft 之一）
- 受众：{audience}
- 一句话差异化：{unique_angle}

【dials 调参】（1-10）
- DESIGN_VARIANCE: {1-10}    # 风格立场强度（越大越偏激）
- MOTION_INTENSITY: {1-10}   # 动效强度（soft-skill 默认 spring motion）
- VISUAL_DENSITY: {1-10}     # 视觉密度

【起步骨架】
- 基底已用 templates/style-mockup-skeleton/，可在此基础上扩展。

【反 AI slop 立场】
- 沿用 taste-skill 子 Skill 内部立场（不需重复 ui-ux-pro-max 的 67 styles 库规则）。
- 差异化记忆点必须有一句话能说清。

【产物落点】
- _work/html_runs/{slug}/
```

委托完成后 Agent 必须**回到 html-gen-pro**做 S5 五维 critique，不要直接以 extension 输出收尾。

## 委托后的兜底检查

extension 产出后，Agent 在 S5 之前先做"完整性 sanity check"（不计入五维 critique，仅是基本可运行性验证）：

- HTML 文件能用浏览器打开（无 404 / 无致命 JS 错误）。
- 主要资源（字体 / 图像 / 样式）路径正确或有合理 fallback。
- 响应式断点至少 mobile-first 工作（landing-page / app-frontend 路线必查）。
- a11y 基本项：每个 `<img>` 有 alt、按钮有可识别文本、对比度可接受。

完整性失败时不要进 S5，回到 S4 修复后再走 critique。
