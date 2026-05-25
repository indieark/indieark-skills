# Prompt Patterns

> Load when: 已选好方法，需要把方法论压成可执行 prompt 骨架。
> Avoid: 只做方法选择，或具体 method 文件已经给出足够模板。
> Pairs with: `selection.md` 选择方法；`../director.md` 合成最终 prompt。

## Gallery-First Pattern

先从 `../gallery.md` 找相近类别，再改写，不从空白 prompt 开始：

```text
Use the gallery pattern for [category], adapted to [current subject/use].
Keep the core structure: [layout/style/field pattern].
Replace source-specific details with: [user subject/constraints].
```

## Canvas-First Pattern

```text
Create [asset type] for [use].
Canvas: [aspect/size/crop], [safe area if needed].
Composition: [subject placement], [foreground/midground/background].
Subject: [main subject and visible attributes].
Style: [medium, light, palette, finish].
Constraints: [must keep, avoid, output requirements].
```

## Edit-Invariant Pattern

```text
Edit the input image.
Keep unchanged: [identity/layout/pose/product/background].
Change only: [specific target].
Blend with original: [lighting/material/perspective].
Do not change: [protected details].
```

## Fixed-Region Pattern

```text
Create [infographic/UI/research figure] with [number] regions.
Region 1: [content and purpose].
Region 2: [content and purpose].
Region 3: [content and purpose].
Visual grammar: [lines/cards/arrows/panels].
Text: [exact short labels or no generated text].
```

## Exact-Text Pattern

```text
Include exact text: "[text]".
Place it in [location], [size/hierarchy].
No other generated text, no fake letters, no watermark.
```

## No-Text Pattern

```text
Leave a clean empty area at [location] for later typography.
No generated text, no fake letters, no logo marks.
```

## Reference-Role Pattern

```text
Use reference image 1 for [identity/product/layout/style].
Use reference image 2 for [secondary role].
Generate a new image, not a collage.
Preserve [specific anchors].
Change [specific target].
```

## Targeted-Negation Pattern

Use 1-4 targeted negatives only:

```text
Avoid: [specific artifact], [specific unwanted change], [specific extra element].
```

Good targets:

- `no extra text`
- `no watermark`
- `do not change the product label`
- `do not add extra fingers or limbs`
- `avoid cluttered background`

Avoid long generic negative lists.
