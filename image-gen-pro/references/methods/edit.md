# Edit Method

> Load when: 用户提供输入图并要求局部修改、替换、扩展、保留身份或 mask 编辑。
> Avoid: 纯文生图，没有输入图或保留要求。
> Pairs with: `../iteration.md` 做结果修正；`consistency.md` 保留身份和产品细节。

## Core Idea

编辑 prompt 的重点不是“生成什么”，而是“保留什么、只改什么、不要动什么”。

## Edit Invariants

- Keep: 必须保留的主体、结构、身份、布局、比例、材质。
- Change: 目标修改，尽量具体。
- Protected area: 不该动的区域或元素。
- Finish: 修改后的光线、边缘、材质要和原图一致。
- Mask: 如果有 mask，说明 mask 用于标记局部编辑范围；仍需写清保留项和修改项。

## Mini Template

```text
Edit the input image.
Keep unchanged: [identity/layout/pose/product details/background if needed].
Change only: [specific target].
Blend the edit with [lighting/material/perspective] from the original.
Do not change: [protected details].
```

## Mask Notes

- mask 应只描述编辑区域；GPT Image 会把 mask 作为 prompt-based guidance，不保证完全贴合 mask 边界。
- 多图输入时，mask 默认对应第一张图。
- GPT mask 必须与第一张输入图同格式、同尺寸，提交文件均小于 50MB，mask 带 alpha。
- 如果用户目标是保留主体，只替换背景，明确 `keep the subject silhouette and edges natural`。

## Common Failures

- 没写保留项，模型重画整张图。
- 修改目标太宽，导致身份、姿势、背景一起变。
- 没写融合规则，编辑区域像贴图。
- 对文字/logo 做编辑但没有要求精确保留或重排。
