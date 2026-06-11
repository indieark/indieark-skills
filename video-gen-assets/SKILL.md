---
name: video-gen-assets
description: 视频资产设定图生成法（character sheet／scene sheet／prop sheet／三视图／asset reuse）。需要角色卡、场景卡、道具卡、平面素材图、声线登记，跨剧本检索复用已有资产，或把图片资产交接给 Seedance 当参考图时使用；图像本体由外部 image-gen-pro 生成。不负责：故事板母图与版式（走 video-gen-storyboard）、参考图怎么喂给模型（走 video-gen-cinematography 的 image-input）、真实视频生成（走 video-gen-pro）。
---

# Video Gen Assets 资产生成法

开始前先读 `../video-gen-pro/SKILL.md` 挂载技能族公共规则（Execution Modes、Red Lines）。本 skill 是 video-gen 技能族的**资产卫星**：角色／场景／道具设定图的生成、登记、跨剧本复用与 Seedance 交接的 canonical。

## 何时使用

- 用户要「角色设定图／三视图／角色卡／场景卡／道具卡／素材图」，或要为视频项目沉淀可复用资产。
- 生成前发现画面一致性靠语言撑不住、需要先出设定图锚定主体时。
- 已有资产库需要检索复用（`asset search|list|show`）或登记新资产时。

## Hard Rules

- 必须先读 `references/assets.md`（入口与 Default Path），按资产类型再读对应 sheet 文件。
- 设定图图像由外部 `image-gen-pro` skill 生成，本技能族不接管图像 CLI；本 skill 只负责提示词结构、登记与交接。
- 资产命名与引用详略一致性遵守 `../video-gen-pro/references/concepts.md`。

## 意图路由（技能族）

| 用户意图 | 去哪 |
|---|---|
| 真实生成／提交／查询／下载视频任务、CLI/API/Key | `../video-gen-pro/SKILL.md` |
| 剧本候选、拆段、连续性、确认门、复盘 | `../video-gen-script/SKILL.md` |
| 问功能介绍／怎么用 | `../video-gen-guide/SKILL.md` |
| 只要 prompt 参考包、自己去 Sora/Veo3/Kling 跑 | `../video-gen-advisor/SKILL.md` |
| 三段式导演法写视频 prompt | `../video-gen-director/SKILL.md` |
| 故事板母图、九宫格/四栏/脚本拼版、4K 确认门 | `../video-gen-storyboard/SKILL.md` |
| 角色/场景/道具设定图、资产登记复用 | 本 skill |
| 运镜/景别/构图/光影/风格/参考图投放 | `../video-gen-cinematography/SKILL.md` |

## 前置条件路由

- 写设定图提示词涉及风格、光影、构图槽位时，MUST 按需读 `../video-gen-cinematography/references/input/` 对应文件；把资产图喂给 Seedance 前 MUST 读 `../video-gen-cinematography/references/input/image-input.md`。
- 资产将用于故事板母图时，交接给 `../video-gen-storyboard/SKILL.md`；多段任务的资产连续性见 `../video-gen-script/references/multi-segment-continuity.md`。
- 资产备齐后回 `../video-gen-pro/SKILL.md` 走确认门与真实生成。

## References

| File | Load When |
|---|---|
| `references/assets.md` | 任何资产请求先读：入口、Default Path、类型分流 |
| `references/README.md` | 资产族文件加载索引 |
| `references/principles.md` | 资产生成通用原则 |
| `references/character-sheet.md` | 角色卡／三视图 |
| `references/scene-sheet.md` | 场景卡 |
| `references/prop-sheet.md` | 道具卡 |
| `references/graphic-sheet.md` | 平面素材图 |
| `references/setting-director.md` | 设定导演：资产体系统筹 |
| `references/seedance-handoff.md` | 资产图交接 Seedance 当参考图 |
