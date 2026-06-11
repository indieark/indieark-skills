# Input Index 输入指南二级索引

> Load when: 已进入 `../input.md`，需要按需选择某个槽位的填法子文件（景别构图运镜、风格库、光影调色、时间氛围 token、图片指南），而不是加载整套填法理论。
> Avoid: 还没判断要填哪个槽位；先回到 `../input.md` 做路由。需要选方法论本身去 `../../../video-gen-pro/references/methods.md`，需要资产图的绘图提示词去 `../../../video-gen-assets/references/`。
> Pairs with: `../input.md` 是输入指南运行时入口；`../../../video-gen-director/references/director-method.md` 与 `../../../video-gen-storyboard/references/README.md` 各方法论定义有哪些槽位；`../../../video-gen-pro/references/concepts.md` 定义横切维度边界。

本目录只保存**输入指南**子文件：提示词各槽位「填什么、怎么填」的填法理论、可挑选模板和速查锚点。它横切所有方法论，被导演法和故事板法共同调用。运行时先读 `../input.md`，再按下表只读一个或少数必要文件。

## Method Index

| Need | File | Output |
| ---- | ---- | ------ |
| 景别（含焦点/景深）各选项的画面语言效果、选用判据、prompt 写法 | `shot-scale.md` | 景别 + 焦点填法理论 |
| 构图（含机位角度）各选项的画面语言效果、选用判据、prompt 写法 | `composition.md` | 构图 + 机位角度填法理论 |
| 运镜手法各选项的画面语言效果、选用判据、prompt 写法，含镜头词库速查 | `camera-move.md` | 运镜填法理论 + 五类镜头词库附录 |
| 整片风格核心（画风/题材流派）的可挑选模板、抽象词→可见元素的翻译 | `style-core.md` | 画风模板库（即梦官方 94 风格）+ Style Bible 翻译规则 |
| 整片视觉基调（器材/画幅/胶片质感）的可挑选模板 | `visual-tone.md` | 视觉基调模板池 |
| 随段落微调的色彩与影调（冷暖/对比/明暗/调色/颗粒）的可挑选模板 | `lighting-tone.md` | 光影与调色模板池 |
| 时间光影 / 地点氛围的中英文风格锚点速查 | `scene-tokens.md` | 时间/氛围 token 表 |
| 参考图按需投放、图内零文字、参考素材编号 | `image-input.md` | Reference Purity + Input Economy + 全能参考写法 |

## 人类速览：可视化画廊

`gallery.html` 是上述六个填法维度的**可视化画廊**（景别 / 构图 / 运镜手法 / 色彩与影调 / 风格核心 / 视觉基调），把 154 项镜头语汇连同蒸馏好的中文提示词、配套参考媒体（`media/` 下 mp4 + webp）铺成影院式卡片墙，供人类浏览选词、点击复制提示词。它面向人眼，不参与 AI 运行时路由。

- 打开方式：浏览器直接打开 `gallery.html` 即可（自包含单文件，媒体走同目录 `media/` 相对路径）。
- 参考媒体已压缩入库：gif→mp4（crf 28）、png→webp（q80），总体积 435M→30M，肉眼几乎无损。

## 横切性说明

这些文件不属于任何单一方法论。同一份填法知识被多方共用：

- `shot-scale.md`：导演法在【画面内容】的景别子字段填（含焦点/景深），故事板法画母图时每格也要定取景。
- `composition.md`：导演法在【画面内容】的构图子字段填（含机位角度），故事板法画母图时每格也要定构图。
- `camera-move.md`：导演法在【画面内容】的运镜手法子字段填，故事板法画母图时每格也要定运动目标。
- `style-core.md`：导演法在【氛围与画质】填整片不变的风格核心，设定流的视觉圣经引用，故事板法定整片风格。
- `visual-tone.md`：导演法在【氛围与画质】填整片不变的视觉基调（器材/画幅/胶片质感）。
- `lighting-tone.md`：导演法在【氛围与画质】填随段落微调的色彩与影调，故事板法每段调色。
- `scene-tokens.md`：场景图（`../../../video-gen-assets/references/scene-sheet.md`）的时间/氛围字段引用。
- `image-input.md`：任何方法论最后往视频模型喂参考图时都遵守。

## Boundary

- 本目录只写「怎么填槽位」的填法知识，不定义「有哪些槽位」（那是方法论的事，见 `../../../video-gen-director/references/director-method.md` 与 `../../../video-gen-storyboard/references/README.md`）。
- 不重复资产维度与形态的梯度定义（那是 `../../../video-gen-pro/references/concepts.md` 和 `../../../video-gen-assets/references/` 的事）；本目录只管**喂**模型时怎么写，不管资产**做**多重。
