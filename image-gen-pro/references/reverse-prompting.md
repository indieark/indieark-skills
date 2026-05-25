# Reverse Prompting

Load when the user provides one or more reference images and wants the new image to imitate, follow, borrow from, reproduce the feel of, or be similar to those images. This includes style, poster language, composition, color, lighting, material, camera, mood, commercial visual identity, product treatment, character look, or multi-image fusion.

Do not load this file for ordinary Photoshop-style edits of the supplied image. If the user says to modify this image, remove/replace a region, change an object, fix details, extend, restore, retouch, or keep the same image structure, route to `edit` / image-to-image instead.

## Routing Rule

This is a required route for reference-image imitation. Do not skip straight to generation when the user's reference image is meant as a style, composition, color, lighting, material, subject, or finish reference for a new image.

Choose one of these paths before writing a prompt:

| User intent | Route | Why |
| --- | --- | --- |
| "参考/模仿/照着这张图生成新的" | `reference-reverse-prompt` | Extract transferable visual language, then generate a clean prompt |
| "像这张海报/艺术风格/构图/色彩" | `reference-reverse-prompt` | Imitation needs structured reverse prompting, not raw image averaging |
| "提取风格模板/反推通用提示词/保留风格替换主体" | `style-template` | Build a reusable style prompt with a replaceable subject placeholder |
| "多张参考图融合" | `reference-reverse-prompt` | Each image needs an explicit role and conflict resolution |
| "把这张图里的 X 改成 Y" | `edit` | The user wants image-to-image editing, not style extraction |
| "修图、PS、去掉、替换、局部修改、保留原图" | `edit` | Preserve source image structure and use edit invariants |

If the intent is ambiguous, ask whether the reference image is a style/composition reference for a new image or the actual image to edit.

Execution rule:

```text
reference image(s)
-> reverse visible facts and transferable visual language
-> write a clean final prompt
-> run imagen generate
-> inspect imagen artifact before reporting
```

Do not bypass `imagen` after the reverse-prompt step. The reverse prompt is not the final deliverable unless the user only asked for prompt/analysis.

Final reporting must follow `reporting.md`: include both the user's original prompt/request and the final prompt submitted through `imagen`.

## Style Template Mode

Use this mode when the user wants to extract a reusable style prompt from a reference image, especially when they want to replace the subject while keeping the same visual universe.

The goal is not to copy the original content. The goal is to keep transferable visual language: composition, camera, light, color science, material, spatial logic, density, motion, post-processing traces, and signature style cues.

If the user only asks for a prompt/template, output the prompt draft and do not run `imagen`. If the user asks to generate a new image from the template, keep the existing execution route: write the final prompt, run `imagen generate`, inspect artifacts, then report through `reporting.md`.

Use this exact placeholder once in reusable templates:

```text
[在此处替换为您想要生成的主体内容]
```

Internal analysis dimensions:

1. Overall style and medium.
2. Subject-to-space relationship.
3. Foreground, midground, and background structure.
4. Composition and visual center of gravity.
5. Camera distance, angle, and focal-length feel.
6. Light source direction, hardness, contrast, rim light, or volume.
7. Palette, temperature, saturation, accent colors, and color grading.
8. Materials, surface texture, brushwork, rendering, or print feel.
9. Mood, atmosphere, and narrative tension.
10. Era, cultural context, or design movement.
11. Perspective, spatial logic, scale exaggeration, or flatness.
12. Information density, negative space, and visual hierarchy.
13. Motion state, frozen instant, blur, or kinetic tension.
14. Post-processing traces such as grain, halation, chromatic aberration, halftone, scan lines, or compression.
15. Signature cues that make the style recognizable at a glance.

Do the 15-part analysis internally. The final prompt should not mechanically list every item; keep only the 6-9 traits that actually define the reference style.

Template prompt rules:

- Strip specific character names, IP, brands, exact visible text, exact locations, and story events.
- Keep transferable subject placement, camera relationship, pose grammar, scale, and spatial role. Do not erase the way the subject sits inside the composition.
- Write a natural Chinese image-generation prompt, not a keyword pile.
- Avoid labels such as "reference image", "image 1", "style from", "source map", or analysis metadata in the final prompt.
- For model-specific suffixes such as MJ `--ar`, `--v`, `--stylize`, keep them outside the generic template unless the user explicitly asks for a model-specific version.

Default template shape:

```text
[在此处替换为您想要生成的主体内容]，置于……，采用……构图与……镜头关系，画面以……光影组织空间，整体色彩呈现……，材质与纹理具有……，背景与前景形成……层次，氛围偏向……，带有……后期痕迹和……视觉签名，避免具体文字、品牌标识和与主体无关的额外元素。
```

Self-check before output:

- The placeholder appears exactly once and remains unchanged.
- No original-specific character, brand, text, location, or story detail remains.
- The template keeps composition, lighting, color, material, density, and signature cues.
- Replacing the placeholder still produces a fluent prompt.
- The prompt is concrete; avoid empty words such as "高级感", "电影感", or "质感好" unless paired with precise visual evidence.

## Single Image Workflow

1. Record visible facts first: subject, scene, text, objects, layout, color, and spatial relationships.
2. Extract visual language second: composition, camera, lighting, palette, material, medium, texture, mood, and density.
3. Mark uncertainty separately; do not turn guesses into facts.
4. Convert the analysis into a generation prompt.
5. Run the final prompt through `imagen generate` when the user asked for an actual image.
6. Keep the final prompt natural and executable; avoid raw keyword piles.

Recommended analysis shape:

```json
{
  "summary": "...",
  "visible_facts": {
    "main_subject": "...",
    "scene": "...",
    "visible_text": []
  },
  "visual_language": {
    "composition": "...",
    "camera": "...",
    "lighting": "...",
    "color_palette": [],
    "materials_and_textures": [],
    "style": "...",
    "mood": "..."
  },
  "generation_prompt": {
    "positive_prompt": "...",
    "negative_prompt": "...",
    "quality_keywords": []
  },
  "uncertainty": []
}
```

## Multi-Image Workflow

Do not average multiple references. Assign a role to each image before fusion:

- subject: identity, silhouette, pose, outfit, product details
- composition: framing, camera distance, layout, depth
- color: palette, contrast, temperature, accent colors
- lighting: source direction, hardness, rim light, atmosphere
- style: medium, rendering traits, poster language, commercial finish
- material: fabric, metal, glass, skin, surface detail
- scene: environment, props, era, spatial structure

Keep `source_map`, `image_roles`, and `conflicts_and_resolution` in the analysis record only. Do not paste those metadata labels into the final generation prompt.

Final prompt rule:

```text
The final positive prompt must be a clean image-generation prompt.
It must not contain image_1, image_2, source map, role labels, conflict notes, or "from this image" metadata.
```

## Quality Bar

- Visible facts are faithful and do not invent brands, text, IP, artists, or off-image story.
- Visual language explains why the reference looks the way it does, not only what it contains.
- Strong poster or art style is described through composition, typography treatment, color, texture, lighting, hierarchy, and medium.
- Multi-image conflicts have explicit priority decisions.
- The prompt is editable: later user changes can update only affected fields instead of rewriting the whole image.
