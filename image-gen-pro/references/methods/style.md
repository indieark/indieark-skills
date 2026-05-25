# Style Method

> Load when: 需要控制媒介、材质、调色、光线、渲染方式或统一视觉系统。
> Avoid: 用户只要简单真实照片或已经有强参考图。
> Pairs with: `composition.md` 先定布局；`consistency.md` 保持跨图统一。

## Core Idea

风格要有边界。不要堆十几个风格词，要拆成媒介、材质、光线、调色和细节密度。

## Style Slots

- Medium: photo, watercolor, ink, pixel art, 3D render, vector, clay, oil painting.
- Material: glass, brushed metal, paper grain, ceramic, fabric, skin, plastic.
- Lighting: softbox, rim light, dusk, overcast, neon, studio, volumetric.
- Palette: muted, high contrast, pastel, monochrome plus accent, warm/cool balance.
- Detail density: minimal, clean, dense, ornamental, technical.

## Prompt Rules

- 选择一个主风格，最多两个辅助限定。
- 先写画面结构，再写风格。
- 参考艺术方向时描述可见属性，不依赖受版权保护的在世艺术家风格。
- 材质、光线、调色分开写，避免模型只抓住其中一个词。

## Mini Template

```text
Style: [primary medium] with [material treatment].
Lighting: [source, direction, contrast].
Palette: [dominant colors] with [accent color].
Detail level: [minimal/clean/dense], [texture rule].
Keep style bounded: avoid mixing unrelated media or overdecorated details.
```

## Debug

- 太花：降低 detail density，减少风格锚点。
- 太平：补 lighting direction 和 contrast。
- 不像同一套：固定 palette、line weight、render finish。
- 材质错：把材质写到主体名旁边，而不是只放在结尾。
