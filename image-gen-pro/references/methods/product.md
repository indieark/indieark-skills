# Product Visual Method

> Load when: 商品图、商店封面、营销主视觉、包装或商业素材需要可用成品感。
> Avoid: 非商业草图、自由概念图、只测试 API 参数。
> Pairs with: `composition.md` 控制版式；`posters.md` 控制营销层级；`style.md` 控制材质。

## Core Idea

商业图优先服务点击、识别和转化。prompt 要写清楚产品、卖点、使用场景和留白，而不是只写“高级”。

## Required Fields

- Product or game identity.
- Target platform or placement.
- Primary promise or mood.
- Subject hierarchy.
- Brand-safe area or text-safe area.
- Output finish: photography, 3D render, illustration, key art.

## Store Art Notes

- 主体要在缩略图下仍可识别。
- 避免把标题文字交给模型生成；除非明确测试文字能力。
- 留出标题、logo、折扣贴纸或平台 UI 的空间。
- 动作游戏偏强轮廓和对比，策略/模拟偏可读场景和系统感。

## Mini Template

```text
Create [commercial asset] for [platform/use].
Main selling point: [promise].
Visual hierarchy: [hero subject] first, [supporting details] second.
Composition: [crop/viewpoint], with clean safe area for [text/logo].
Finish: [photography/render/illustration], [lighting], [material], [palette].
Avoid: clutter, unreadable small details, fake text, extra logos.
```

## Common Failures

- 画面很美但卖点不清。
- 背景噪声太多，缩略图不可读。
- 模型生成乱码标题，后期难修。
- 过度堆风格，产品本体不稳定。
