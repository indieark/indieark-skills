# Structured Prompts Method

> Load when: 需求复杂、字段多、要稳定复用，或用户给了规格表/JSON/config。
> Avoid: 简短创意图或单张简单 prompt。
> Pairs with: `product.md` 做商业素材；`infographics.md` 做固定区域信息图。

## Core Idea

复杂图像任务用结构化规格比自然段更稳定。结构化不是为了让模型输出 JSON，而是为了让输入约束不丢。

## Useful Sections

- intent
- canvas
- subject
- layout
- style
- lighting
- text
- references
- constraints
- avoid

## Mini Template

```text
Intent: [what this image is for]
Canvas: [aspect/size/crop]
Subject: [main subject]
Layout: [regions and hierarchy]
Style: [medium, palette, finish]
Lighting: [source and mood]
Text: [exact text or no generated text]
References: [role of each input image]
Constraints: [must keep, must avoid]
```

## When To Use

- 需要多次迭代同一资产。
- 用户要求“按这个配置生成”。
- 图里有固定区域、图例、标签或 UI。
- 多人协作时需要可审阅规格。

## Avoid

- 把互相冲突的要求都塞进结构里。
- 字段太多但没有优先级。
- 在 provider adapter 中硬编码方法论字段。
