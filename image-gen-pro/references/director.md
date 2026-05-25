# Image Director Prompt Reference

> Load when: 需要把用户意图整理成图像 prompt、生成方案或 dry-run request。
> Avoid: 用户已经提供最终 prompt 且只要求 CLI/API 调用。
> Pairs with: `scenes.md` 提供场景字段；`api.md` 提供能力边界。

目标是保留用户意图，同时补足影响生成结果的结构字段。不要把所有方法论一次性塞进 prompt。

如果用户要实际图片，prompt 只是 `imagen generate/edit` 的输入，不是最终交付物。写完 prompt 后必须回到 `router.md` 选择 CLI 操作。

## Prompt Fields

按需使用以下字段：

- Purpose: 输出用途和受众。
- Subject: 主体、数量、身份、材质或产品。
- Composition: 构图、焦点、视角、留白。
- Scene: 环境、时间、背景复杂度。
- Style: 视觉风格、媒介、渲染质感。
- Lighting: 光线、色温、对比度。
- Constraints: 必须保留、必须避免、格式/尺寸/透明。
- References: 每张参考图的角色。

## Minimal Pattern

```text
Create [purpose] featuring [subject].
Composition: [focus, framing, viewpoint].
Style: [visual style, medium, lighting].
Constraints: [format, aspect, keep/avoid].
References: [only when provided].
```

## Edit Pattern

```text
Edit the input image.
Keep: [structure, subject identity, layout, items].
Change: [target modification].
Style and finish: [style, lighting, output look].
Do not change: [protected details].
```

## Reference Pattern

```text
Use reference image 1 for [role].
Use reference image 2 for [role].
Generate [new output], not a collage.
Preserve [identity/style/product details] where specified.
```

## Reference Image Routing

- If the reference image is the actual image to retouch, replace, remove from, extend, restore, or preserve structurally, use the edit pattern and `router.md` edit route.
- If the user wants to imitate or follow reference images for a new image, read `reverse-prompting.md` before writing the final prompt.
- First extract visible facts and transferable visual language, then write a clean final prompt. Do not include `image_1`, `source_map`, role labels, or analysis metadata in the final generation prompt.

## Transparent Output Routing

- If the user asks for transparent PNG, no background, cutout, sprite, icon alpha, or removed background, read `transparent-output.md`.
- The prompt must ask for a cutout-ready asset on a single flat solid chroma background, not a normal complex background, checkerboard, or "transparent-looking" background.
- Actual delivery requires `imagen transparent` after generation.

## Defaults

- 不添加用户没要求的文字、logo 或水印。
- 不承诺完全保留身份、布局或局部区域，除非 provider 能力和输入支持。
- prompt 过长时优先保留用途、主体、构图、限制和参考关系。

## Method Routing

- 构图复杂：读 `methods/composition.md`。
- 跨图一致：读 `methods/consistency.md`。
- 商业素材：读 `methods/product.md` 或 `methods/posters.md`。
- 局部编辑：读 `methods/edit.md`。
- 精确文字：读 `methods/typography.md`。
- 信息图/论文图/UI：分别读 `methods/infographics.md`、`methods/research-figures.md`、`methods/ui-mockups.md`。

## Dense Scene Rule

用可见细节代替抽象形容词。不要只写“高级、震撼、专业”，要写主体、视角、材质、光线、层级和限制。

## Targeted Negation

只否定会破坏结果的东西，例如 `no extra text`、`no watermark`、`do not change the product label`。不要堆长串负面词，避免稀释主目标。
