# Research Figures Method

> Load when: 论文图、技术流程图、实验示意、数据图或科学教育图需要严谨表达。
> Avoid: 纯艺术化科学幻想图，或真实数据未给出却要求精确图表。
> Pairs with: `infographics.md` 做区域；`structured-prompts.md` 管理术语。

## Core Idea

论文图要清晰、可审稿、可复述。不要追求装饰性，优先结构、标签和术语一致。

## Figure Types

- Pipeline diagram.
- System architecture.
- Experimental setup.
- Comparison panels.
- Mechanism illustration.
- Data visualization mockup.

## Mini Template

```text
Create a research-style figure for [topic].
Figure type: [pipeline/system/setup/comparison/mechanism].
Panels: [A/B/C layout if needed].
Visual grammar: clean lines, consistent arrows, labeled modules.
Labels: short technical labels, no decorative text.
Style: publication-ready, white background, restrained colors.
Avoid: fake numerical results, unreadable microtext, ornamental effects.
```

## Rules

- 如果没有真实数据，不生成具体数值图表。
- 多 panel 要明确 A/B/C 的内容。
- 箭头方向必须表达因果或流程，不做装饰。
- 标签少而准，复杂说明留给 caption。

## Debug

- 太像营销图：降低饱和度和阴影。
- 模块混乱：减少节点，改成分层 pipeline。
- 标签错乱：使用编号和后期文字方案。
