# Edit Endpoint Showcase Gallery

> Load when: 需要图像编辑、局部替换、换背景、保留主体、mask/inpaint 或参考图改写案例。
> Avoid: 纯文生图、没有输入图或不需要保留原图结构。
> Pairs with: `../methods/edit.md`、`../methods/consistency.md`、`../iteration.md`。

Source: adapted from `gpt_image_2_skill` gallery category `Edit Endpoint Showcase`; prompts are rewritten for local use.

## Patterns

### Background Replacement

- Use when: 保留主体，只换背景或环境。
- Size: `auto`
- Quality: `high`
- Prompt skeleton:

```text
Edit the input image.
Keep unchanged: the main subject, silhouette, pose, product details and edge quality.
Change only: replace the background with [new environment].
Blend: match lighting direction, shadows and perspective to the original subject.
Avoid: changing the subject, adding extra objects over the subject, fake text.
```

### Local Object Change

- Use when: 只改一个区域、物件、颜色、材质或细节。
- Size: `auto`
- Quality: `high`
- Prompt skeleton:

```text
Edit the input image.
Keep unchanged: overall composition, camera angle, lighting, background and all unmasked areas.
Change only: [target object/region] into [new state].
Make the edit physically consistent with the original scene.
Avoid: repainting unrelated areas or changing identity/product labels.
```

### Style Transfer With Structure Locked

- Use when: 保留构图和主体，把视觉风格改成另一种媒介。
- Size: `auto`
- Quality: `medium` or `high`
- Prompt skeleton:

```text
Edit the input image into [target style].
Preserve: layout, subject identity, pose, major shapes and readable details.
Transform: color treatment, line quality, material finish and background texture.
Avoid: changing the subject count, replacing important objects, adding text.
```
