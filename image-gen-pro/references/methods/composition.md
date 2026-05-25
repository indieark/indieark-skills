# Composition Method

> Load when: 画面需要明确构图、焦点、视角、留白、层次或多主体关系。
> Avoid: 用户只要简单主体图，或已经给出精确构图。
> Pairs with: `../director.md` 输出最终 prompt；`posters.md` 处理商业层级。

## Core Idea

先定义画布，再定义主体。好的图像 prompt 不应只堆形容词，而要交代“画面怎么组织”。

## Prompt Order

1. Output purpose and aspect.
2. Main subject and visual priority.
3. Camera/framing/viewpoint.
4. Foreground, midground, background.
5. Negative space and text-safe area.
6. Lighting and finish.

## Practical Controls

- 用 `centered`, `rule of thirds`, `symmetrical`, `isometric`, `top-down`, `close-up`, `wide establishing shot` 这类构图词控制视角。
- 有文案、logo、UI overlay 时，明确 safe area，例如 `leave clean negative space on the right third`。
- 多主体时写主次，不要让模型猜谁最重要。
- 背景复杂时拆成层次：foreground props、midground subject、background environment。

## Mini Template

```text
Create [asset type] in [aspect/size intent].
Composition: [primary subject] is [framing/viewpoint], with [foreground], [midground], and [background].
Focus hierarchy: [what is most important], then [secondary detail].
Leave [negative space/text-safe area] for [purpose].
Finish: [lighting, material, color, rendering].
```

## Common Failures

- 只写风格不写布局，结果主体位置随机。
- 同时要求近景和全景，空间逻辑冲突。
- 没有 text-safe area，后续排版会遮挡主体。
- 背景细节比主体更强，商业图失焦。
