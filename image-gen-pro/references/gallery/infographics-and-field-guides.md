# Infographics & Field Guides Gallery

> Load when: 需要信息图、教学图、field guide、分区说明、流程图或标注图参考。
> Avoid: 普通海报、纯摄影或无需信息结构的插画。
> Pairs with: `../methods/infographics.md`、`../methods/structured-prompts.md`、`../methods/typography.md`。

Source: adapted from `gpt_image_2_skill` gallery category `Infographics & Field Guides`; prompts are rewritten for local use.

## Patterns

### Field Guide Plate

- Use when: 展示一组对象、物种、部件或分类。
- Size: `1536x1024`
- Quality: `high`
- Prompt skeleton:

```text
Create a field guide plate about [topic].
Layout: organized grid with [number] items, consistent scale.
Each item: clear silhouette, key visual detail, short label placeholder.
Style: clean educational illustration, light background.
Text: short labels only or leave label areas blank.
Avoid: fake scientific names, crowded microtext, inconsistent item scale.
```

### Explainer Infographic

- Use when: 用区域解释概念、流程或系统。
- Size: `1536x1024`
- Quality: `medium` or `high`
- Prompt skeleton:

```text
Create an explainer infographic for [concept].
Layout: [number] numbered sections arranged left-to-right or top-to-bottom.
Section content: [short description of each region].
Visual grammar: icons, arrows, callouts, clean dividers.
Text: minimal readable labels, no invented statistics.
Avoid: dense paragraphs, random numbers, decorative arrows.
```

### Anatomy / Parts Diagram

- Use when: 标注物体结构、产品部件、生物结构或机器部件。
- Size: `1536x1024`
- Quality: `high`
- Prompt skeleton:

```text
Create a labeled parts diagram of [subject].
Composition: main subject centered with callout lines to key parts.
Labels: short generic labels or blank label boxes.
Style: precise technical illustration, clear linework.
Avoid: incorrect hidden internals, overlapping callouts, tiny text.
```

### Process Steps

- Use when: 展示步骤、工作流、制作过程、生命周期。
- Size: `1536x1024`
- Quality: `medium`
- Prompt skeleton:

```text
Create a step-by-step visual process for [process].
Layout: [number] stages in a clear sequence.
Each stage: one simple visual action, consistent icon style.
Arrows: show direction only, not decoration.
Avoid: too many steps, fake data, ambiguous order.
```
