# Visual Assets Method Index

> Load when: 已进入 `../visual-assets.md`，需要按需选择视觉资产子方法，而不是加载整套理论。
> Avoid: 还没有判断是否需要视觉资产；先回到 `../visual-assets.md` 做路由。
> Pairs with: `../visual-assets.md` 是运行时入口；`../visual-storyboard.md` 管项目库、确认门和生成历史。

本目录只保存视频生成前的视觉资产方法。运行时先读 `../visual-assets.md`，再按下表只读一个或少数必要文件。复杂任务在进入本目录前应先完成 `../visual-storyboard.md` 的项目/资产检索门。故事板是上层概念：一张按需压缩视频信息的 4K 主运动参考图；首版正式故事板就必须 4K / 等效 4K，不走低清预览确认。九宫格、四栏、8 镜头和电影制作设定板只是不同信息密度和版式。故事板不单独承担人物、背景和道具细节锁定，视频提交时要和对应角色卡、场景/背景卡一起作为参考输入。

## Method Index

| Need | File | Output |
| ---- | ---- | ------ |
| 理解为什么要先做视觉资产 | `principles.md` | 三层链路、确认门和常见错误 |
| 从一句想法拆出角色、场景、风格和段落 | `setting-director.md` | 可登记的项目设定和资产清单 |
| 生成或修正人物设定图 | `character-sheet.md` | 角色卡提示词；正式角色卡只能用人设三视图或多视图模板 |
| 生成或修正场景设定图 | `scene-sheet.md` | 基本场景卡、严格复用正交四视图、本次剧情多视角联合图、场景 DNA 和禁止穿帮提醒 |
| 生成视频主运动参考图 | `storyboard-board.md` | 自适应故事板母图、信息密度、配套角色/场景卡输入、区域主次和视频读图规则 |
| 多张 CUT / 场景 / 调度图需要拼成信息图 | `script-composed-storyboard.md` | 原子图片清单、脚本拼版清单、4K 故事板海报和短视频读图 prompt |
| 单段视频需要镜头顺序母图 | `grid-storyboard.md` | 镜头网格版式提示词和视频读图 prompt，可九宫格或自定义格数 |
| 短剧、广告、系列内容需要项目总览 | `four-column-storyboard.md` | 项目级版式提示词和视频读图 prompt，可四栏、制作设定板或自定义栏目 |
| 判断单段或多段并保持连续 | `multi-segment-continuity.md` | 智能编排判断、连续性台账、镜头边界、`continuity_mode`、按需尾帧/首尾帧/长镜头延长和多段 prompt 模板 |
| 视觉资产已生成，准备进 Seedance | `seedance-handoff.md` | CLI 登记、确认、`video-prompt.txt` 和生成步骤 |

## Loading Patterns

一句话复杂任务：

```text
../visual-storyboard.md 检索门已完成
principles.md
-> setting-director.md
-> character-sheet.md / scene-sheet.md
-> storyboard-board.md
-> 信息密集或文字要求高时进入 script-composed-storyboard.md
-> 必要时参考 grid-storyboard.md 或 four-column-storyboard.md
-> seedance-handoff.md
```

已有角色图和场景图：

```text
../visual-storyboard.md 已登记或确认可复用资产
storyboard-board.md
-> 为每个分镜/CUT 绑定对应角色卡和场景卡
-> 信息密集或需要真实文字排版时进入 script-composed-storyboard.md
-> 必要时参考 grid-storyboard.md 或 four-column-storyboard.md
-> seedance-handoff.md
```

多段视频或系列内容：

```text
../visual-storyboard.md 检索门已完成
setting-director.md
-> multi-segment-continuity.md 先做 Intelligent Orchestration Gate，判断 15 秒是否只是上限、单段是否可行、是否需要多个更短故事板和生成轮次
-> storyboard-board.md
-> 每段需要 CUT 海报确认时进入 script-composed-storyboard.md
-> 必要时参考 grid-storyboard.md 或 four-column-storyboard.md
-> seedance-handoff.md
```

只缺某一类图：

```text
character-sheet.md 或 scene-sheet.md
-> seedance-handoff.md
```

## Boundary

- 图片生成由 Skill 编排当前环境可用的图像生成工具；`seedance2` CLI 只登记生成结果。
- 本目录不写具体图片 provider、模型、Key 或鉴权参数。
- 每张生成图都必须保存提示词、来源摘要和用途，后续通过 CLI 登记到项目库。
- 正式角色卡必须走 `character-sheet.md` 的人设三视图或多视图模板；第一种人设描述只是文本基础，不单独作为复杂项目角色卡。
- 场景卡必须走 `scene-sheet.md` 的主要场景列表、场景卡路由判断和单场景提示词格式；多个主要场景逐个生成，不混成一条提示词。每个 `SCxx` 先判断镜头角度数、复用强度和空间风险：单镜头静止、推进或拉远时基本场景卡够用；正交四视图只用于严格复用；多视角联合图只用于某一次剧情场景里的多个镜头角度。不要默认只生成简单场景单图。
- 故事板、分镜和 CUT 原子图必须参考已确认的角色卡和场景卡；多张分镜拼版时，每张分镜也要能回溯到对应 `character_refs` 和 `scene_ref`。
- 故事板图默认是视频主运动参考图；角色卡和场景/背景卡默认是人物、空间、背景和道具细节锚点。提交 Seedance 时必须在 `video-prompt.txt` 写清参考图编号和主次。
- 自动拆分必须先生成或整理剧本，再输出智能编排判断，说明 15 秒是否只是上限、单段是否可行、信息负载来自哪里、是否需要多个更短故事板和生成轮次；每个生成轮次只提交本段相关故事板、角色卡、场景/背景卡、道具/产品卡和声音 brief。
- 故事板图可以包含详细文字、表格和镜头说明，但首版正式图必须 4K 清晰可读；低清草稿不能登记、确认或提交 Seedance；交给 Seedance 的 `video-prompt.txt` 要短，只写读图规则和边界。
- 信息密集、中文说明多或用户需要类似影视制作信息图时，优先考虑脚本拼版：图像工具生成 CUT / 场景 / 调度原子图，真实文字由脚本排版到最终 4K 故事板。
- 清楚可规划的镜头优先故事板法；混沌粒子、爆炸烟尘、抽象动态或难以画清的随机效果优先 prompt-heavy 或混合路径。
- 用户只要静态图片最终交付时，转交图片生成 Skill；本目录只服务后续视频生成。

## Source Notes

本目录吸收本机 `ai-director/docs/创作指南` 的三层链路：

- `设定导演流`：母系统，负责角色、场景、风格、连续性和段落逻辑。
- `故事板一图流`：故事板母图是视频主运动参考图，按项目复杂度决定信息区、镜头数量、栏目和读图顺序；角色和场景/背景细节仍由对应卡片补齐并随视频生成一起输入。
- `脚本拼版故事板`：当故事板需要大量可读文本和 CUT 信息时，先生成原子图片，再用确定性脚本排版成 4K 信息图，避免图像模型生成乱码小字。
- `分镜一图流`：单段 4-15 秒视频可用九宫格或其他镜头网格作为故事板版式。
- `四栏故事板`：短剧、广告、系列内容可用四栏作为故事板版式，也可升级为制作设定板。
- `智能编排与多段连续性`：当一个项目需要判断单段或多段时，先确认 15 秒是上限而非默认目标；低负载长镜头可以单段，高信息负载内容即使总时长 15 秒也可拆成多个 4-6 秒故事板和生成轮次。多段生成使用同一项目资产、连续性台账和剧本阶段的镜头边界决策减少漂移；尾帧只用于画面硬衔接，镜头切换不强制接尾帧，同一长镜头跨段时优先用 `extend` 或尾帧硬衔接。

不要把这些理论复制回 `../visual-assets.md`；入口只保留路由。
