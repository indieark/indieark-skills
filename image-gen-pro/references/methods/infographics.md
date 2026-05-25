# Infographics Method

> Load when: 信息图、field guide、教学图、流程图、分区说明或带标签视觉需要生成。
> Avoid: 普通插画、海报或没有信息结构的图。
> Pairs with: `structured-prompts.md` 管理区域；`typography.md` 控制文字风险。

## Core Idea

信息图先是版式，再是图像。必须定义区域、标签、图例和阅读顺序。

## Region Schema

- Header: title or topic.
- Main visual: subject or diagram.
- Callouts: labeled details.
- Side panel: facts, legend, steps.
- Footer: optional source or note.

## Mini Template

```text
Create an infographic about [topic].
Layout: [number] clearly separated regions.
Region 1: [purpose and content].
Region 2: [purpose and content].
Labels: short, high contrast, readable.
Style: [flat/vector/editorial/scientific], clean spacing.
Avoid: dense tiny text, fake data, cluttered arrows.
```

## Data Safety

- 不编造真实统计数字。
- 用户没给数据时，使用占位标签或视觉结构，不写具体数值。
- 复杂文字建议后期排版。

## Debug

- 太乱：减少区域数量。
- 标签不可读：减少文字，增加留白。
- 箭头乱飞：用 numbered callouts 代替自由箭头。
