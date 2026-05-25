# Official Cookbook Examples Gallery

> Load when: 需要参考官方 cookbook 风格的最小 API/图像任务案例，但仍要以当前官方文档为准。
> Avoid: 需要最新 API capability 判定；那应读 `../api/gpt-image-2.md` 并核对官方文档。
> Pairs with: `../api.md`、`../api/gpt-image-2.md`、`../methods/prompt-patterns.md`。

Source: adapted from `gpt_image_2_skill` cookbook/gallery snapshot; prompts are rewritten for local use.

## Minimal Generation Case

- Size: `1024x1024`
- Quality: `medium`

```text
Create a clear image of [subject].
Style: [simple style].
Composition: centered subject, clean background.
Constraints: no text, no watermark, no extra objects.
```

## Minimal Edit Case

- Size: `auto`
- Quality: `medium`

```text
Edit the input image.
Keep unchanged: [protected details].
Change only: [target change].
Make the edit blend naturally with the original lighting and perspective.
```
