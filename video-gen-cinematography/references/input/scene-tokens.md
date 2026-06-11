# Scene Tokens 时间光影 / 地点氛围速查

> Load when: 写场景图提示词或氛围描述时，需要把中文的时间、光线、氛围选择转换成英文风格锚点，帮助外部图像工具稳定画面。
> Avoid: 只需要场景卡的结构/路由判断（去 `../../../video-gen-assets/references/scene-sheet.md`）、或整片风格基调（去 `style-core.md` 画风 / `visual-tone.md` 视觉基调）。
> Pairs with: `../../../video-gen-assets/references/scene-sheet.md` 的场景概念图字段引用本表；`style-core.md` / `visual-tone.md` 管整片风格、本表管单镜时间/氛围。

生成场景概念图时可把中文选择转换为英文风格锚点：

```text
时间光影：
- 白天：daytime, bright sunlight
- 夜晚：nighttime, moonlight, stars
- 黎明：dawn, early morning light
- 黄昏：dusk, golden hour
- 阴天：overcast sky, soft diffused light
- 暴风雨：stormy weather, dark clouds

地点氛围：
- 平静：peaceful, serene
- 紧张：tense, suspenseful
- 浪漫：romantic, intimate
- 神秘：mysterious, foggy
- 欢快：cheerful, vibrant
- 忧郁：melancholic, somber
- 史诗：epic, majestic
- 恐怖：horror, creepy
```

这些 token 填进场景图提示词的 `时间光影`、`地点氛围` 字段，或导演法【画面内容】里需要锚定单镜时间/氛围处。整片层面的风格核心走 `style-core.md`、视觉基调走 `visual-tone.md`、段落级色彩与影调走 `lighting-tone.md`，不要和本表混——本表只管单个场景的时间与氛围锚点。
