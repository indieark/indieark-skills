# Inspiration · 灵感源

Load when: 用户想看参考站点 / 风格博物馆 / 别人怎么做的；或美学方向卡住、需要外部素材打开思路。
Avoid: 不要假装本 Skill 内置 fetch 能直接抓素材——这些是**参考源**，不是可调用的 API；不要把外部灵感站点的整页直接照搬到产物（Dribbble 视觉常常无法落地）。
Pairs with: `styles.md`, `workflow.md`, `flows.md`, `extensions.md`, `cases.md`

> 本 Skill 不绑定任何外部服务，也不内置 fetch 脚本。本文件是一张"外部灵感源 + IndieArk 内部既有视觉"的路标表，由 Agent 在会话内手工或借 `smart-search` / `WebFetch` 等工具按需访问。
>
> **与 extension 的分工**：本仓库现有 2 个 extension——`ui-ux-pro-max` 在 S4 提供**结构化素材库**（67 styles / 161 palettes / 57 font pairings / 161 industry rules），覆盖 landing-page / app-frontend / style-mockup 三条路线；`taste-skill` 在 `style-mockup` 路线作为 brutalist / swiss / luxury(soft) 三类气质的**深度立场子 Skill**（含 1-10 dials 调参与 image-first pipeline）。两者都是"工作时的字典"。本文件的**外部站点 / 字体源 / 配色源 / IndieArk 内部参考**是"工作前的灵感地图"。三者不重叠：素材库 / 深度立场由 extension 推荐具体值，灵感地图由 Agent 用来在 S3 找气质方向。

## 一、AI 网页生成器（既是灵感源也是参考产物）

| 来源 | 类型 | 用法 |
|---|---|---|
| [v0.app](https://v0.app/) | Vercel 的 AI 网页生成器 | 看它的 "Explore" / "Community" 找近期热门组件和落地页气质；**不要直接照抄它的默认输出**，那就是 AI slop |
| [Lovable](https://lovable.dev/) | 全栈 AI 生成器 | 看它社区作品里"产品页 + Dashboard"组合 |
| [bolt.new](https://bolt.new/) | StackBlitz AI 生成器 | 类似 v0；快速验证一个气质是否可行时拿来 mock |

**重要提醒**：v0 / Lovable / bolt 的"默认产物"普遍是 AI slop（白底 + 紫渐变 + Inter 字体 + 三列卡片）。引用它们的目的是看**社区里挑战默认**的作品。

## 二、组件库 / Design System（作为词汇库）

| 来源 | 价值 |
|---|---|
| [shadcn-ui](https://ui.shadcn.com/) | 组件粒度的设计基线；本 Skill 在 React 路线**手写**而非依赖其 npm 包，避免大量隐式依赖 |
| [21st.dev](https://21st.dev/) | 大量手工设计的 React/Tailwind 组件；近年最干净的灵感站 |
| [Tailwind UI](https://tailwindui.com/) | Tailwind 官方付费组件库；公开预览页足够看版式 |
| [Origin UI](https://originui.com/) | 免费 React + Tailwind 组件库；表单与小组件类的灵感密度高 |
| [Park UI](https://park-ui.com/) | 跨框架组件库；按 token 拆得很清，看怎么定义 design tokens |

## 三、纯灵感画廊

| 来源 | 何时去看 |
|---|---|
| [Awwwards](https://www.awwwards.com/) | 高端品牌站 / 设计工作室自营页 / experimental web |
| [SiteInspire](https://www.siteinspire.com/) | 按风格 tag 过滤；editorial、minimal、portfolio 这类风格最多 |
| [Land-book](https://land-book.com/) | 落地页与产品页专项 |
| [One Page Love](https://onepagelove.com/) | 单页设计专项 |
| [Httpster](https://httpster.net/) | 反主流 / brutalist / 独立创作风格 |
| [Brutalist Websites](https://brutalistwebsites.com/) | 看 brutalist 风格 |
| [Dribbble](https://dribbble.com/) | 看小组件、动效、风格碎片（**不直接照抄整页**——Dribbble 视觉常常没法落地） |
| [Behance](https://www.behance.net/) | 完整品牌项目；看气质连贯性 |
| [Cosmos](https://www.cosmos.so/) | moodboard 工具 / 灵感聚合 |
| [Refind](https://refind.com/) | 设计周报聚合 |

## 四、字体源（反 AI slop 第一步）

| 来源 | 价值 |
|---|---|
| [Google Fonts](https://fonts.google.com/) | 必查；按 "Display / Serif / Mono" 分类逐个看，避开 Inter / Roboto |
| [Bunny Fonts](https://fonts.bunny.net/) | Google Fonts 的隐私友好镜像；CDN 速度同档 |
| [Fontshare](https://www.fontshare.com/) | ITF 团队的免费商用字体集；近年质量奇高 |
| [Pangram Pangram](https://pangrampangram.com/) | 高质量付费 + 部分免费字体；display 字体重镇 |
| [Use & Modify](https://usemodify.com/) | 免费 + 可改字体目录 |
| [Velvetyne](https://velvetyne.fr/) | 法国实验字体厂 |
| [Open Foundry](https://open-foundry.com/) | 开源字体策展站 |

## 五、配色源

| 来源 | 用法 |
|---|---|
| [Realtime Colors](https://realtimecolors.com/) | 在真实排版预览中试配色；最贴近落地效果 |
| [Coolors](https://coolors.co/) | 经典配色生成器 |
| [Huemint](https://huemint.com/) | AI 配色生成；按品牌色 + 模板尝试 |
| [Color Hunt](https://colorhunt.co/) | 社区策展配色 |
| [Refactoring UI 配色章节](https://www.refactoringui.com/) | 不是源，是方法 |

## 六、动效与微交互

| 来源 | 用法 |
|---|---|
| [Motion (Framer Motion)](https://motion.dev/) | React 动效一等公民 |
| [GSAP](https://gsap.com/) | 复杂 timeline、滚动驱动动画首选 |
| [Codrops Articles](https://tympanus.net/codrops/) | 实验性 web 效果教程；动效爱好者圣地 |
| [Codepen 探索](https://codepen.io/) | 小动效原型 / 实验 / 抄实现 |

## 七、IndieArk 内部既有视觉参考

参考已有 IndieArk 项目里**已落地**的优秀视觉，避免在已建立的视觉语言之外再造一套：

| 内部参考 | 价值 |
|---|---|
| `gadget/Indieark_steam_design/` | Steam 风暗色 UI / Glassmorphism 落地样本 |
| `20013-hot/` | Steam 风视觉延展 |
| `1-showcase/` | 多主题系统（CSS Custom Properties）落地样本 |
| `20009-feedback/` | 工具型仪表板的实战 UI |
| `20005-aigc/` | AI 美术流程类型站点的实战 UI |

详见根目录 [`../../../../../PROJECTS.md`](../../../../../PROJECTS.md) "跨项目可复用能力" 表。
