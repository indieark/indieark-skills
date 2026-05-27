# Styles · 链回全局风格 Skill

Load when: workflow.md §1 美学方向阶段，用户对风格无方向；或用户点名某种具体风格想看落地样例。
Avoid: 不要把全局风格 Skill 的内容复制过来——只能链接 + 一句话定位；不要在路由层判定风格关键词时跳过 [`router.md`](router.md) 真源。
Pairs with: `workflow.md`, `flows.md`, `inspiration.md`, `route-introduction.md`, `extensions.md`

> 本文件**不是风格教程**，而是一张"全局风格 Skill 路标表 + 反 AI slop 黑名单"。具体风格规则、样例、CSS 实现要点全部在对应风格 Skill 内部。
>
> **链回 extension 素材库**：本仓库现有 2 个 extension——`ui-ux-pro-max`（67 styles + 161 palettes + 57 font pairings，是 `landing-page` / `app-frontend` / `style-mockup` 三条路线在 S4 阶段的素材源）与 `taste-skill`（在 `style-mockup` 路线作为 brutalist / swiss / luxury(soft) 三类气质的深度立场分流，含 1-10 dials 调参与 image-first pipeline）。详见 [`extensions.md`](extensions.md) 的 "style-mockup" 段。本文件的"反 AI slop 黑名单"是**本仓库自持的方法论立场**，不外包给任一 extension：不论 extension 推什么风格，本仓库都拒绝下面黑名单里的元素。

## 全局风格 Skill 路标

| 风格 | 一句话定位 | 何时推荐 | 全局 Skill 入口 |
|---|---|---|---|
| **claymorphism** | 圆润、像粘土玩具、柔光、立体感 | 玩具 / 儿童产品 / 轻量 SaaS / 给"科技感"降温的场景 | `~/.claude/skills/ccg/domains/frontend-design/claymorphism/SKILL.md` |
| **glassmorphism** | 半透明磨砂玻璃 + 多层模糊 + 鲜亮背景 | 信息密度高但要保持视觉呼吸的 Dashboard / 多浮层界面 / 苹果生态产品风 | `~/.claude/skills/ccg/domains/frontend-design/glassmorphism/SKILL.md` |
| **liquid-glass** | iOS 26 风液态玻璃 + 折射光 + 动态拟态 | 高端消费品 / Apple 生态衍生 / 新一代沉浸式 Hero | `~/.claude/skills/ccg/domains/frontend-design/liquid-glass/SKILL.md` |
| **neubrutalism** | 厚黑边 + 高饱和块 + 错位阴影 + 反精致 | 独立产品 / Web3 / 反主流主张 / "我不像主流 SaaS"宣言 | `~/.claude/skills/ccg/domains/frontend-design/neubrutalism/SKILL.md` |

读取规则：用户的气质提到对应关键词时，**先把对应风格 Skill 的 SKILL.md 读进来再动手**（CLAUDE.md 的 ccg 自动路由规则会处理；不行就手动 `Read` 一次）。

## 不在上表里但常用的"无 Skill 风格"

以下风格 IndieArk 目前**没有专门的全局 Skill**，按 `frontend-design` 的 Design Thinking 自由发挥即可，注意找参考站点（见 [`inspiration.md`](inspiration.md)）。"外部 Skill 路标"列登记**社区已做出的填补型 Skill**（调研档案见 [`../../../docs/research/external-skills.md`](../../../docs/research/external-skills.md) Tier 3.5）：

| 风格 | 何时推荐 | 外部 Skill 路标 |
|---|---|---|
| brutalist & raw | 反主流叙事、设计哲学宣言、独立媒体；与 neubrutalism 区别：brutalist 偏"裸露 / 黑白 / 字体怪诞"，neu 偏"高饱和 + 错位阴影" | ✅ **extension** [`Leonxlnx/taste-skill · brutalist-skill`](https://github.com/Leonxlnx/taste-skill)（已 vendored 至 `extensions/taste-skill/`，S4 自动委托；install name `industrial-brutalist-ui`） |
| editorial & magazine | 长文阅读站 / 设计博客 / 文化品牌；强排版、衬线 + 等宽字穿插、左右双栏 | ⛓ **接力** [`luukalleman/premium-design-skill`](https://github.com/luukalleman/premium-design-skill)（13 组件 editorial-luxe；由 Agent 引导用户启用） |
| swiss & grid | 严肃媒体 / 高端 B2B / 设计工作室自我营销 | ✅ **extension** [`Leonxlnx/taste-skill · brutalist-skill`](https://github.com/Leonxlnx/taste-skill)（含 Swiss type 立场，与 brutalist 同子 Skill 双覆盖；S4 自动委托） |
| retro-futuristic / Y2K / vaporwave | 怀旧次文化、独立游戏、合成器音乐 | — 社区空缺 |
| organic & natural | 食品 / 美容 / 健康 / 户外品牌；曲线、自然色、植物纹理 | — 社区空缺 |
| luxury & refined | 奢侈品 / 高端服务；大量留白 + 衬线 + 一种 accent gold | ⛓ **接力** [`luukalleman/premium-design-skill`](https://github.com/luukalleman/premium-design-skill)（editorial-luxe，由 Agent 引导用户启用）<br>✅ **extension** [`Leonxlnx/taste-skill · soft-skill`](https://github.com/Leonxlnx/taste-skill)（install name `high-end-visual-design`，气质偏 calm + softer contrast + spring motion；已 vendored，S4 自动委托） |
| industrial / blueprint | 工程 / 硬件 / 制造业；网格底纹、技术线条、CAD 味 | — 社区空缺 |
| cyberpunk | 游戏 / Web3 / 科幻；霓虹色 + 字符故障 + 阴暗背景 | — 社区空缺 |

**两类路标语义**：

- **✅ extension**：已 vendored 到 `extensions/` 目录（locked_commit 锁定），S4 阶段由本仓库自动委托对应子 Skill，**不依赖用户手动启用**。当前 3 行（brutalist / swiss / luxury(soft 第二选项)）走此路径，全部委托 `taste-skill`。委托规则见 [`extensions.md`](extensions.md) "style-mockup" 段。
- **⛓ 接力**：未 vendored，由 Agent 在 S3 美学方向阶段引导用户手动启用外部 Skill。当前 2 行（editorial / luxury 主选项）走此路径，全部委托 `premium-design-skill`。接力协议见 [`boundary.md`](boundary.md) §6。

> 其余 4 个空缺风格（Y2K / organic / industrial / cyberpunk）按 [`inspiration.md`](inspiration.md) 的外部站点路标 + frontend-design 的 Design Thinking 自由发挥（**不必抢做 Skill** —— 这些风格的精髓在于"反模板"，做成 Skill 反而失去灵气，详见 [`../../../docs/research/external-skills.md`](../../../docs/research/external-skills.md) "对照启示"第 5 条）。

## 反 AI slop 黑名单

**在美学方向阶段就要主动避开**——这些组合是 AI 默认产物的指纹：

| 元素 | 为什么是 AI slop | 替代 |
|---|---|---|
| 字体 = Inter / Roboto / Arial / system-ui | 所有 AI 生成的"漂亮网站"都长这样 | 选 distinctive display + 配体（Fraunces / Cormorant / DM Serif / Space Grotesk / Recoleta / Migra / Inktrap / Mona Sans / Geist / IBM Plex / JetBrains Mono...）；变化要大胆 |
| 配色 = 白底 + 紫色渐变 + 灰色卡片 | Bolt/v0/Lovable 默认产物指纹 | 大块 dominant + 强 accent；或暗色主导 + 明亮 accent；或 editorial 双色 |
| 版式 = hero + 3 列特性卡 + CTA + footer | SaaS 万能模板 | 至少在一个 section 用 asymmetric / overlap / grid-breaking |
| 微动效 = 卡片 hover translateY(-4px) + shadow 加深 | 没人会记得 | 给一个签名级动效（更剧烈、更怪、更协调） |
| 文案 = "Build, Ship, Scale" / "The future of X" | 模板化口水话 | 与产品具体差异化点对齐的一句话 |

## 与 frontend-design 的协作

读取全局 `frontend-design` 的 SKILL.md 一起看；其中 "Frontend Aesthetics Guidelines" 部分是更详细的反 AI slop + 选型方法。本文件只补充：**IndieArk 工作区视角下的具体推荐 + 风格 Skill 路标**，不重复方法论。
