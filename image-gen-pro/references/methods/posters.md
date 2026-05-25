# Posters Method

> Load when: 商业海报、活动视觉、封面、宣传图、key art 或带标题层级的画面。
> Avoid: 不需要营销层级的普通插画。
> Pairs with: `composition.md` 控制布局；`typography.md` 控制文字；`product.md` 控制卖点。

## Core Idea

海报是层级系统：谁先被看见、文案放哪里、情绪是什么、行动是什么。prompt 要控制阅读顺序。

## Hierarchy

1. Hero visual.
2. Title or logo area.
3. Supporting visual details.
4. Subtitle / date / CTA area.
5. Background mood.

## Mini Template

```text
Create a poster/key art for [event/product/game].
Hero: [main subject] dominates the composition.
Hierarchy: [title area], [secondary info area], [supporting details].
Mood: [emotion].
Composition: [crop/viewpoint], strong silhouette, clear negative space.
Typography: [exact text or no generated text].
Avoid: clutter, fake extra text, unreadable small details.
```

## Text Strategy

- 精确标题少于一行时可以尝试模型生成。
- 多行中文、日期、地点、价格等建议留白后期排版。
- 标题区和主体不要竞争同一空间。

## Debug

- 不像海报：补 title area、hero hierarchy、negative space。
- 太像壁纸：加入商业信息区。
- 太乱：减少配角和背景道具。
