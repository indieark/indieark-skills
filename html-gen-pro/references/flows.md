# Flows (S0–S5 状态机)

Load when: 需要把"路由 → 介绍选择 → 安装检查 → 美学方向门 → 委托 / 起步骨架 → 五维 critique"串成可执行状态机，或排查用户在哪个状态卡住。
Avoid: 不要在本文件复制路由触发词、路线介绍文案、五维 critique 清单或风格黑名单（真源分别在 `router.md` / `route-introduction.md` / `critique.md` / `styles.md`）；本文件只描述状态机与跨阶段交接。
Pairs with: `router.md`, `route-introduction.md`, `extensions.md`, `install.md`, `usage.md`, `workflow.md`, `critique.md`, `reporting.md`, `verify.md`

> **方法论视角与 router 视角分工**：[`workflow.md`](workflow.md) 是**方法论视角**的流程详细说明（美学方向门怎么问 / 五段流程在思考层面长什么样）；本文件是 **router 视角**的状态机（每个状态读什么、调用什么、跨阶段交接什么）。两者互链不重复。

## 六阶段状态机

```
┌───────────┐  强触发  ┌──────────┐  用户选定  ┌──────────┐  extension 在场？      ┌──────────┐
│  S0 路由  │ ───────▶ │ S1 介绍  │ ─────────▶ │ S2 选择+ │ ─────────────────────▶ │ S3 美学  │
│ router.md │          │ route-in │          │  安装检查 │  (ui-ux-pro-max         │  方向门   │
└───────────┘          └──────────┘          │install.md│   + taste-skill)        │workflow§1│
                                              └──────────┘                        └──────────┘
                                                                                       │
                                                                                       ▼ 气质+受众+差异化锁定
                                                                                  ┌──────────┐
                                                                                  │ S4 委托/ │
                                                                                  │ 起步骨架/│
                                                                                  │ 项目重塑  │
                                                                                  │  usage.md │
                                                                                  └──────────┘
                                                                                       │
                                                                                       ▼ 产物就绪 + sanity check
                                                                                  ┌──────────┐
                                                                                  │ S5 五维  │
                                                                                  │ critique │
                                                                                  │ +汇报+verify │
                                                                                  └──────────┘
```

## S0 · 路由触发（[`router.md`](router.md)）

**输入**：用户的自然语言请求。

**判定顺序**（与 [`router.md`](router.md) Recommendation Rule 完全一致）：

1. 子项目名优先：含 `20009-feedback` / `20013-hot` / `1-showcase` / `20005-aigc` / `tide-spider` 等 → `existing-project-optimize`。
2. 具体风格关键词优先：claymorphism / glassmorphism / liquid-glass / neubrutalism / brutalist / swiss / magazine / editorial / 杂志风 / 终端风 / Y2K / cyber → `style-mockup`。
3. 工具型 UI 关键词：Dashboard / Admin / Web App / 后台 / 控制台 / 仪表板 / 工具页 → `app-frontend`。
4. fallback：`landing-page`。
5. 模糊请求：反问用户分类，**不盲推**。

**否定词扫描**：扫描 [`router.md`](router.md) 的"否定词清单"；命中 PPT / audit / 纯方法论 / 后端 关键词时路由出本 Skill。

**输出**：`{route, recommendation_sentence}` 或"路由出本 Skill"。

## S1 · 标准介绍（[`route-introduction.md`](route-introduction.md)）

**输入**：S0 的 `{route, recommendation_sentence}`。

**呈现规则**：

- 展示 4 路线菜单 + 推荐句 + 取舍提示（使用 [`route-introduction.md`](route-introduction.md) 的标准话术）。
- 强调本仓库强制 S3 美学方向门 + S5 五维 critique；让用户明白这不是"立刻开始写代码"的入口。

**用户响应面**：

| 用户回复 | 解释 |
|---|---|
| `1` / `2` / `3` / `4` | 菜单选定路线 |
| `按推荐来` / `好的` | 路线 = `recommendation_sentence` 指向的路线 |
| 重新表达需求 | 退回 S0 重新判定 |
| 明确说"不要走 html-gen-pro" | 路由出本 Skill，按用户指定路径走 |

**输出**：`{route_confirmed}` → 进入 S2。

## S2 · 用户选择 + 安装检查（[`install.md`](install.md), [`extensions.md`](extensions.md)）

**输入**：S1 的 `{route_confirmed}`。

**分支**：

- `landing-page` / `app-frontend` 路线 → 检查 `extensions/ui-ux-pro-max/SKILL.md` 是否存在。
  - 存在 → 进入 S3。
  - 缺失 → 提示用户跑 `python scripts/install_extensions.py`；可手动 `git clone https://github.com/nextlevelbuilder/ui-ux-pro-max-skill extensions/ui-ux-pro-max`。
- `style-mockup` 路线 → 检查 `extensions/ui-ux-pro-max/SKILL.md` **和** `extensions/taste-skill/README.md` 是否都存在（双 extension 并列，S3 美学方向锁定后由 S4 择一委托）。
  - 都存在 → 进入 S3。
  - 任一缺失 → 提示用户跑 `python scripts/install_extensions.py --route style-mockup`；可手动 `git clone https://github.com/Leonxlnx/taste-skill extensions/taste-skill`。
- `existing-project-optimize` 路线 → 不需 extension；先过 [`../../../templates/existing-project-optimize-checklist.md`](../../../templates/existing-project-optimize-checklist.md) 接入前 checklist，确认 `git status` 干净、`package.json` 已读、业务逻辑入口已知、用户授权改动范围明确。

**输出**：`{route_confirmed, extension_ready_or_na, project_checklist_passed_if_applicable}` → 进入 S3。

## S3 · 美学方向门（强制 gate）（[`workflow.md`](workflow.md) §1, [`styles.md`](styles.md), [`inspiration.md`](inspiration.md)）

**输入**：S2 结果。

**职责**：未与用户对齐"气质 + 受众 + 一句话差异化"前，**禁止写大段代码**。

**问询模板**：

```text
我们进入美学方向门，先对齐 3 件事：

1. 气质（vibe）：你想要什么气质？参考词：{brutalist / swiss / magazine / editorial / claymorphism / glassmorphism / liquid-glass / neubrutalism / 终端风 / Y2K / cyber / vaporwave / 杂志风 / 极简 / ...}
2. 受众（audience）：是给谁看？{开发者 / 设计师 / 投资人 / 普通用户 / SaaS 决策者 / 学术读者 / ...}
3. 一句话差异化（unique angle）：这个网页凭什么和别的不一样？要能说出具体元素（如"用 ASCII art 做 hero"、"全黑底 + 单一霓虹色"、"杂志竖排"），不能是"现代 / 简约 / 用户友好"这类 AI slop 词汇。

我可以帮你提选项，但这 3 件事必须锁定才进入下一步。
```

**styles.md 反 AI slop 黑名单同步显示**：S3 时把当前要避免的 AI slop 黑名单（Inter / Roboto / 紫色渐变白底 / 通用 hero+grid 套版等）作为约束传给用户，让用户明白本 Skill 拒绝的"通用美感"是什么。

**回到 S2 的条件**：用户改主意要换路线 → 回到 S1 重新选择。

**输出**：`{vibe, audience, unique_angle}` → 进入 S4。

## S4 · 委托 / 起步骨架 / 项目重塑（[`usage.md`](usage.md)）

**输入**：S3 锁定的 `{vibe, audience, unique_angle}` + S2 的 `{route_confirmed}`。

**分支**（详细 prompt 模板见 [`usage.md`](usage.md) S4 各路线的委托路径）：

- `landing-page` → 打开 `extensions/ui-ux-pro-max/SKILL.md`，prompt 模式 = "marketing landing page"，附 161 industry rules 调用 + 起步骨架 [`../../../templates/landing-page-skeleton/`](../../../templates/landing-page-skeleton/)。
- `app-frontend` → 打开 `extensions/ui-ux-pro-max/SKILL.md`，prompt 模式 = "dashboard / admin / web app"，附 99 UX guidelines + 起步骨架 [`../../../templates/dashboard-skeleton/`](../../../templates/dashboard-skeleton/)。
- `existing-project-optimize` → 跟随项目原生栈 + 接入前 checklist + [`cases.md`](cases.md) 项目立场要点；**不调用 extension**；产物直接改对应项目目录。
- `style-mockup` → 按美学方向择一委托（不允许同一次执行混用两个 extension）：
  - 美学方向命中 **brutalist · swiss · luxury(soft)** → 委托 `extensions/taste-skill/`，由 Agent 选取对应子 Skill 入口（`brutalist-skill/SKILL.md` / `soft-skill/SKILL.md`），prompt 模式 = "style = <风格名> + dials (DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY)" + 起步骨架 [`../../../templates/style-mockup-skeleton/`](../../../templates/style-mockup-skeleton/)。
  - 其余风格 → 委托 `extensions/ui-ux-pro-max/SKILL.md`，prompt 模式 = "style = <风格名>"，附 67 styles 库调用 + 起步骨架 [`../../../templates/style-mockup-skeleton/`](../../../templates/style-mockup-skeleton/) + 链入全局风格 Skill（claymorphism / glassmorphism / 等）。

**完整性 sanity check**（产物就绪后、进 S5 之前）：

- HTML 文件能用浏览器打开（无 404 / 无致命 JS 错误）。
- 主要资源（字体 / 图像 / 样式）路径正确或有合理 fallback。
- 响应式断点至少 mobile-first 工作（landing-page / app-frontend 路线必查）。
- a11y 基本项：`<img alt>` / 按钮可识别 / 对比度可接受。

**输出**：可运行产物 + 完整性 sanity check 通过 → 进入 S5。

## S5 · 五维 critique + 完工汇报 + 可选视觉验证（[`critique.md`](critique.md), [`reporting.md`](reporting.md), 可选 [`verify.md`](verify.md)）

**输入**：S4 的可运行产物。

**五维 critique**（详细清单见 [`critique.md`](critique.md)）：

- 视觉冲击（typography + 配色 + 空间）
- 信息层级（视觉权重 + 阅读路径 + scan-ability）
- 交互细节（micro-interaction + 动效 + 状态反馈）
- 工程质量（语义 HTML + 响应式 + 可访问性 + 性能 + 跨浏览器）
- **差异化记忆点**（强制必答，反 AI slop 第一防线）

**可选视觉验证**：按 [`verify.md`](verify.md) 走 Playwright MCP；不能用 MCP 时走 fallback（`python -m http.server` + 让用户回贴截图）。**不要假装看了截图**。

**完工汇报**：按 [`reporting.md`](reporting.md) 模板（路线 / 美学方向 / 改动文件 / 五维 critique 结论 / 预览方式 / 残余风险 / 接力建议）。

**输出**：完工汇报 → 流程结束。

## 状态间约束

1. **S0 不直接跳 S4**：必须经过 S1 让用户确认，S3 让用户对齐美学方向。
2. **S3 是强制门**：未锁定 `{vibe, audience, unique_angle}` 前 S4 不能开始。
3. **S2 → S3 不能跳 install 检查**：landing / app-frontend / style-mockup 路线下 extension 缺失时必须先 install 才能进 S3 末段或 S4。
4. **S5 不能跳过 critique 直接 reporting**：第五维"差异化记忆点"强制必答。
5. **跨路线切换重启状态机**：用户在 S4 中途要切换路线，必须回到 S1 重新选定；本 Skill 不在 S4 内做横切。
6. **完工后无新指令时退出状态机**：S5 报告完成后等待用户下一轮指令；不主动开始新的设计。

## 与现有 reporting.md 的衔接

S5 完成后必须按 [`reporting.md`](reporting.md) 报告，至少包含：

- 选定的路线 + 触发原因
- S3 锁定的美学方向（气质 + 受众 + 一句话差异化）
- 是否调用 extension（landing / app-frontend 路线 → ui-ux-pro-max；style-mockup 路线 → 按美学方向择 ui-ux-pro-max 或 taste-skill）/ 是否过了接入前 checklist（existing-project-optimize 路线时）
- 五维 critique 结论（必含差异化记忆点的具体内容）
- 改动文件清单（对外 demo → `_work/html_runs/<slug>/`；项目重塑 → 项目目录）
- 是否走了 Playwright MCP 视觉验证

## 维护契约

- 新增路线时：S0 加判定分支 + S1 菜单加项 + S2 安装检查加分支 + S4 加委托模板 + 同步 [`router.md`](router.md) / [`route-introduction.md`](route-introduction.md) / [`extensions.md`](extensions.md) / [`capability-matrix.md`](capability-matrix.md) 真源。
- 新增 extension 时：S2 安装检查加 install 路径 + S4 加委托 prompt 模板 + 同步 [`extensions.md`](extensions.md) Registry。
- 状态机改动时：先改本文件，再同步 `scripts/test_router.py`（Phase 3 起）的状态断言；router dry-run 应覆盖每个状态间转移。
