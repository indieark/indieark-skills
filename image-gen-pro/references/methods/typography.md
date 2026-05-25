# Typography Method

> Load when: 海报、标题、UI、包装、中文或多语言文字需要进入画面。
> Avoid: 不需要模型生成文字，或文字应后期排版。
> Pairs with: `posters.md` 处理商业层级；`composition.md` 预留文字区域。

## Core Idea

精确文字是高风险项。能后期排版就后期排版；必须由模型生成时，把文字、位置和层级写清楚。

## Rules

- 需要精确出现的文字放在引号里。
- 明确语言、大小写、行数、位置和字重。
- 不要一次要求大量小字。
- 中文、多语言、数字和符号越复杂，越应减少其他画面复杂度。
- 如果文字必须可编辑，要求留白，不让模型生成文字。

## Mini Template

```text
Include exact text: "[text]".
Typography: [font mood], [weight], [case], [line count].
Placement: [area], with enough margin and contrast.
Do not add any other letters, logos, subtitles, or watermarks.
```

## Safer Alternative

```text
Leave a clean empty title area at [position] for later typography.
No generated text, no fake letters, no logo marks.
```

## Debug

- 出现乱码：改成后期排版方案。
- 字太小：减少文案，增加留白。
- 字压主体：回到 `composition.md` 先定义 safe area。
