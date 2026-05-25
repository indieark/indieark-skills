# Consistency Method

> Load when: 角色、产品、品牌、系列图或多面板需要保持一致。
> Avoid: 单张图且不要求复用身份、造型或系统。
> Pairs with: `edit.md` 保留输入图特征；`style.md` 控制统一视觉语言。

## Core Idea

一致性来自可复述的“身份锚点”，不是泛泛地说 keep consistent。每个锚点都要可观察。

## Anchor Types

- Character: age range, body shape, hair, clothing, accessories, expression, signature colors.
- Product: shape, material, logo placement, labels, proportions, defects or unique marks.
- Brand: palette, typography feel, icon style, surface treatment, photo/render finish.
- Series: same camera angle, same lighting logic, same background language, same crop.

## Prompt Rules

- 先列不变项，再列变化项。
- 多图参考时声明每张图的角色，例如 identity、pose、style、product detail。
- 不要要求“完全一样”，改成保留具体可见特征。
- 连续输出时使用同一组 anchors，不每次改写同义词。

## Mini Template

```text
Use the reference as the identity anchor.
Preserve: [stable features].
Change only: [target change].
Keep consistent: [palette, material, camera, lighting].
Do not alter: [protected details].
```

## Checklist

- 是否列出了 3-7 个稳定特征？
- 是否说清楚每张参考图的用途？
- 是否避免了新增不必要饰品、文字或 logo？
- 是否明确了哪些地方可以变化？
