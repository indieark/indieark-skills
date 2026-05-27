# Critique · 五维评审

Load when: workflow.md §5 评审阶段；或用户提交已有 UI 让本 Skill 评分；或草稿前想先看评分维度心里有数。
Avoid: 不要把"五维都 5 分"当成目标——某些气质本来就需要在某维度故意"低分"（如 brutalist 故意降低工程质量的整洁度）。
Pairs with: `workflow.md`

> 五个维度的设计目标是让"产物为什么 stunning"可结构化讨论；分数本身不是 KPI，**是讨论的脚手架**。

## 维度 1 · 视觉冲击（Visual Impact）

> 用户第一眼是否被抓住？

- **Typography**：display 字体是否 distinctive、非 AI 通用？body 字体与 display 是否成对协调？字号层级是否大胆（hero 至少 60px+ 还是缩在 32px 的"安全区"）？
- **Color**：是否有明确的 dominant + accent？是否避免了"白底紫渐变"、"深蓝品牌万能色"、"灰白苹果味通用色"？是否敢用大块色？
- **Spatial Composition**：版式有没有出乎意料的部分（asymmetry / overlap / diagonal flow / grid-breaking）？还是规规矩矩的"hero + 3 列卡片 + footer"？
- **Backgrounds & Texture**：是否有 noise / gradient mesh / 几何图案 / 分层透明 / drop shadow / grain overlay 等氛围层？还是平白的纯色？

**评分参考**：

| 分 | 描述 |
|---|---|
| 1 | AI 通用味满分；放在 Vercel templates 里完全没人认出来 |
| 3 | 有清晰的气质选择；但执行不够大胆，落回安全区 |
| 5 | 第一眼就有记忆点；字体 + 颜色 + 版式三者协调放大同一种气质 |

## 维度 2 · 信息层级（Information Hierarchy）

> 用户在 3 秒内能不能 scan 到核心？

- 视觉权重是否服务于阅读路径（最大的元素 = 最重要的信息）？
- 段落 vs. headline vs. CTA 的对比度是否够大？
- 是否有"页面里所有东西看起来一样重"的灾难？
- 移动端折叠后核心信息还在不在 above-the-fold？

**反模式**：把 CTA 做得和正文一样大、用同色相、没有 hover 区分——典型 AI 折中症。

## 维度 3 · 交互细节（Interaction Details）

> 用户每次操作有没有"被理解"的反馈？

- Hover / Focus / Active / Disabled 四态是否都设计了？还是只默认态？
- 关键动作是否有 micro-interaction（按钮缩放、链接下划线动画、表单聚焦光晕、卡片悬浮抬起）？
- 页面加载是否有一次精心编排的入场动画（staggered reveal）？还是噼里啪啦全部一起出现？
- 滚动是否有意图：parallax / scroll-triggered fade / sticky transform？

**警惕过度动效**：每个元素都在弹跳 = 没有重点。一次精心编排的入场 + 关键 CTA 的 hover 反馈，胜过五处零散的 micro-interaction。

## 维度 4 · 工程质量（Engineering Quality）

> 把光鲜的视觉脱掉后，代码还能不能称得上 production-grade？

- **语义 HTML**：用了 `<header>` / `<nav>` / `<main>` / `<section>` / `<article>` / `<footer>` 而不是一堆 `<div>`？
- **响应式**：手机、平板、桌面、超宽屏都试过？字号是否用 `clamp()` 等流式单位而非死值？
- **可访问性（A11y）**：颜色对比度通过 WCAG AA？交互元素有可见 focus ring？图像有 alt？图标有 aria-label？
- **性能**：CSS 没有重复定义？字体 preload？图像懒加载？JS 没有不必要的整页重绘？
- **跨浏览器**：在 Safari 上摸过？iOS Safari 100vh 坑、Firefox `backdrop-filter` 缺陷有没有兜底？

> 与全局 `web-design-guidelines` 的合规清单有重叠；本维度只做"现场快查"，深度审查仍可接力到全局 Skill。

## 维度 5 · 差异化记忆点（The Memorable One Thing）

> 一句话说清楚"这页面凭什么和别的不一样"？

这是**反 AI slop 的最关键防线**。把页面盖住 80%，留 20%——你能不能凭那 20% 认出这是哪个页面？

- 有没有"那一个东西"：一段大字号宣言、一种独特版式、一个签名动效、一种从未见过的配色、一个奇异的字体组合？
- 还是只能描述成"白色简洁现代风、紫色渐变、漂亮卡片"？后者是 AI 通用语义，0 分。

**必答题**：在 critique 报告里**强制用一句话**写出当前的差异化记忆点。说不出来 = 这维度 1 分，必须重做美学方向。

## Critique 输出模版

```text
[维度 1 视觉冲击]    4/5   字体大胆但 accent 颜色偏弱；hero 字号建议 80px+
[维度 2 信息层级]    3/5   CTA 与正文对比度不足；折叠后核心 USP 看不到
[维度 3 交互细节]    2/5   仅有默认态；hover 缺失；入场动画零散无编排
[维度 4 工程质量]    4/5   响应式 OK；可访问性 focus ring 缺失
[维度 5 差异化点]    3/5   "用 Times New Roman 做编辑风排版" — 有方向但还不够极致

差异化记忆点（一句话）：用古典衬线 + 杂志风左右双栏 + 黑色文本块下移做层叠效果，做出"打开高级杂志而非软件产品页"的感觉。

下一轮优先动：维度 3（编排入场 + 加 CTA hover）+ 维度 5（左右双栏的"层叠"目前还不够明显）
```
