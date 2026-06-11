---
name: video-gen-cinematography
description: 影视语言参考库（cinematography／film language）。要把视频 prompt 的槽位真正填好时使用：运镜 camera move、景别 shot scale、构图 composition、光影调色 lighting tone、视觉基调 visual tone、风格核心 style core（94 风格模板）、时间氛围 scene tokens、参考图按需投放 image input。横切导演法与故事板法的填料层，附带可在浏览器打开的示例画廊。不负责：选方法论（走 video-gen-pro 的方法选择门）、剧本拆分（走 video-gen-script）、真实生成执行（走 video-gen-pro）。
---

# Video Gen Cinematography 影视语言参考库

开始前先读 `../video-gen-pro/SKILL.md` 挂载技能族公共规则（Execution Modes、Red Lines）。本 skill 是 video-gen 技能族的**填料层卫星**：横切导演法与故事板法，按维度供给 prompt 槽位的词表、模板与示例媒体。

## 何时使用

- 用户问「运镜／景别／构图／光影／调色／视觉基调／风格怎么选怎么写」，或写 prompt 时需要具体维度的填料。
- 导演法、故事板法、资产法流程中任何「填槽位」步骤（它们会路由到这里）。
- 用户要决定「参考图要不要喂、怎么喂」（image input 投放决策）。

## Hard Rules

- 必须先读 `references/input.md`（维度索引与按需加载规则），再按维度读 `references/input/` 对应文件；不要一次性全量加载。
- `references/input/media/` 与 `references/input/gallery.html` 是示例媒体与人类画廊：md 内 `![](media/...)` 引用与 gallery.html 同步维护，**改路径必裂图，禁止移动或重命名 media 内文件**。
- 本 skill 只供给填料，不替用户选方法论：方法选择门在 `../video-gen-pro/references/methods.md`。

## 意图路由（技能族）

| 用户意图 | 去哪 |
|---|---|
| 真实生成／提交／查询／下载视频任务、CLI/API/Key | `../video-gen-pro/SKILL.md` |
| 剧本候选、拆段、连续性、确认门、复盘 | `../video-gen-script/SKILL.md` |
| 问功能介绍／怎么用 | `../video-gen-guide/SKILL.md` |
| 只要 prompt 参考包、自己去 Sora/Veo3/Kling 跑 | `../video-gen-advisor/SKILL.md` |
| 三段式导演法写视频 prompt | `../video-gen-director/SKILL.md` |
| 故事板母图、九宫格/四栏/脚本拼版、4K 确认门 | `../video-gen-storyboard/SKILL.md` |
| 角色/场景/道具设定图、资产登记复用 | `../video-gen-assets/SKILL.md` |
| 运镜/景别/构图/光影/风格/参考图投放 | 本 skill |

## 前置条件路由

- 填料服务的骨架在方法论侧：三段式骨架见 `../video-gen-director/references/director-method.md`，母图流程见 `../video-gen-storyboard/references/visual-storyboard.md`。
- 参考图来自资产库时，交接规则见 `../video-gen-assets/references/seedance-handoff.md`。
- 槽位填完回到调用方法论，最终生成回 `../video-gen-pro/SKILL.md`。

## References

| File | Load When |
|---|---|
| `references/input.md` | 任何填料请求先读：维度索引、按需加载规则、参考图投放决策入口 |
| `references/input/README.md` | 填料层总览与边界 |
| `references/input/camera-move.md` | 运镜 |
| `references/input/shot-scale.md` | 景别 |
| `references/input/composition.md` | 构图 |
| `references/input/lighting-tone.md` | 光影调色 |
| `references/input/visual-tone.md` | 视觉基调 |
| `references/input/style-core.md` | 风格核心（94 风格模板） |
| `references/input/scene-tokens.md` | 时间氛围 token |
| `references/input/image-input.md` | 参考图按需投放 |
| `references/input/gallery.html` | 人类画廊（浏览器打开看示例，不供模型加载） |
