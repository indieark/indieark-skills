# Workflow

Load when: 用户进入生成请求，要按"草稿 → 预览 → 五维评审 → 迭代"流程推进。
Avoid: 不要跳过"美学方向"直接写大段代码；不要在已有项目里把"试跑产物"和"业务代码"混到一起。
Pairs with: `critique.md`, `styles.md`, `boundary.md`, `flows.md`

> **方法论视角 vs router 视角**：本文件是**方法论视角**的流程详细说明（美学方向门怎么问 / 五段流程在思考层面长什么样 / 反模式具体是什么）；router 视角的状态机（S0–S5 每个状态读什么、调用什么、跨阶段交接什么）在 [`flows.md`](flows.md)。两者互链不重复——方法论解释"为什么这样做"，flows 解释"这次要做什么"。

## §1 · 美学方向（Aesthetic Direction Gate）

在写任何代码前，先与用户对齐三件事——**这是硬门槛，跳过会导致返工**：

1. **气质（Tone）**：从这些极端方向里挑一个或组合，并写一句话理由。
   - brutally minimal / maximalist chaos / retro-futuristic / organic & natural / luxury & refined / playful & toy-like / editorial & magazine / brutalist & raw / art deco & geometric / soft & pastel / industrial & utilitarian / swiss / claymorphism / glassmorphism / liquid glass / neubrutalism / cyberpunk / Y2K / vaporwave / blueprint
2. **受众与目的**：谁来用、用来解决什么；这决定了字号、密度、动效尺度。
3. **一句话差异化记忆点**：用户走完这页后会记住的"那一个东西"是什么（一个动效？一段文字？一种排版？一种配色？）。

用户对气质无方向时，调用 [`styles.md`](styles.md) 给 3-5 个备选并解释取舍，让用户挑。**不要替用户默默选**。

> 与全局 `frontend-design` 的 Design Thinking 一致，但本 Skill 把"差异化记忆点"明确为**必答项**，因为没有差异化的产物会落回 AI 通用味。

## §2 · 技术栈选型

按场景跟随，不强绑定：

| 场景 | 默认 | 决策细节 |
|---|---|---|
| 独立 Landing Page / 营销页 / 一次性 mockup | 单文件 HTML + CSS + JS | 字体走 Google Fonts / Bunny Fonts CDN；要 utility 时引 Tailwind Play CDN；动效优先 CSS-only |
| 独立 Dashboard / Web App 原型 | Vite + React + Tailwind | 除非用户指定 Vue / Svelte / Solid。优先 shadcn-ui 风格组件，但**手写而非依赖 npm 包**——避免引入大量依赖 |
| 优化已有 IndieArk 项目前端 | **跟随项目原生栈** | 先看项目 `package.json` / `vite.config.*` / `tsconfig.json` 确认；新引依赖必须用户明确同意 |
| 用户要求 "可运行 React Demo" 但没指定构建 | Vite + React + TS + Tailwind | 一条命令 `npm create vite@latest -- --template react-ts` 起步；勿引入完整 monorepo 模板 |

**反模式**：

- 给一次性 mockup 引入完整 Vite + Tailwind + shadcn 工程——交付物臃肿、用户预览门槛高。
- 在已有项目里用一个新框架重写它的 UI 层——除非用户明确说"重写"。
- 用 Inter / Roboto / Arial / system-ui 等 AI 默认字体（详见 `critique.md` 差异化维度）。

## §3 · 草稿（Draft）

写最小可运行版本，含：

- 完整的骨架（hero、主信息、关键 CTA、必要的二级模块）
- 明确的字体（display + body 各一个 distinctive 选择）
- 明确的配色（dominant + accent，禁止"白底紫渐变"组合）
- 至少一个"差异化记忆点"已经被实现的微动效或排版
- 移动端基础响应式

产物落点：

- 独立 Demo → `_work/html_runs/<slug-or-timestamp>/index.html`（含相对路径资源）
- 项目内 → 项目原有目录，新建分支或直接改文件（与用户先约定）

把路径和预览方式告知用户：

```text
草稿落在 _work/html_runs/<slug>/index.html
本地预览：双击打开 / 或 `python -m http.server 8080` 后访问 http://localhost:8080
```

## §4 · 预览（Preview）

- 不要假装自己看了产物。除非确实启用了浏览器/截图工具，否则告诉用户"请你在浏览器里打开看看"。
- 等用户反馈"看到了"或"丑/不对"后，再进 Step 4 评审。
- 如果用户给截图描述问题，把问题点对应到 `critique.md` 的某个维度，便于结构化讨论。

## §5 · 五维评审（Five-Axis Critique）

按 [`critique.md`](critique.md) 的 5 个维度逐项过；每个维度给：

- 现状评分（1-5）
- 具体问题（指明 selector / 行号 / 区块名）
- 修改建议（具体到属性 / 数值）

输出一份小的 critique 报告（在对话里，不必落文件，除非用户要存档）。

## §6 · 迭代（Iterate）

- 按 critique 报告优先级排序：差异化记忆点 > 视觉冲击 > 信息层级 > 交互细节 > 工程质量。
- 一次只动 1-2 个维度，避免大改丢失方向。
- 每轮迭代后再回到 Step 4 简版自查；满意后输出最终交付清单：
  - 改动文件列表
  - 关键设计决策（一两句话回顾气质 + 差异化点）
  - 残余风险（已知问题、未覆盖浏览器、未优化的性能项）
  - 预览方式重申

## §7 · 接力到其他 Skill

- 用户想做合规 / 可访问性审查 → 推荐切到全局 `web-design-guidelines`，把产物路径传过去。
- 用户中途说"我其实要的是 PPT / 演讲网页" → 立即停止本 Skill，转 `ppt-gen-pro`。
- 用户想要更多风格灵感 → 切到 `styles.md` 链回的全局风格 Skill。
