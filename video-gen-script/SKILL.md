---
name: video-gen-script
description: 视频剧本编排（script planning／smart split／multi-segment continuity／confirmation gate）。把想法写成剧本候选与镜头清单、判断长内容如何拆段（智能编排拆分门）、维护多段连续性台账／尾帧交接／extend 链、生成前确认与结果复盘时使用。不负责：故事板母图与版式（走 video-gen-storyboard）、三段式 prompt 写法（走 video-gen-director）、真实生成执行（走 video-gen-pro）。
---

# Video Gen Script 剧本编排

开始前先读 `../video-gen-pro/SKILL.md` 挂载技能族公共规则（Execution Modes、强制执行协议、Red Lines、决策管线）。本 skill 是 video-gen 技能族的**剧本编排卫星**：管「内容怎么从一句话变成可执行的剧本与镜头清单、长内容怎么拆段、多段之间怎么保持连续、生成前怎么确认、生成后怎么复盘」。

## 何时使用

- 用户要把自然语言想法写成剧本候选、资产清单、镜头清单（资产从剧本拆，镜头只引用资产）。
- 用户问「这条 60 秒怎么拆段 / 15 秒是不是上限 / 要不要分多轮生成」——走智能编排拆分门。
- 多段视频或系列内容需要连续性台账、尾帧交接、`extend` 链规划。
- 真实生成前的确认门（素材清单、标准文本回复、结构化修改意见）与生成后的结果复盘。
- 生成类任务全程的阶段提醒义务（当前阶段、已完成、下一步、需要素材、是否确认继续）。

## 意图路由（技能族）

| 用户意图 | 去哪 |
|---|---|
| 真实生成／提交／查询／下载视频任务、CLI/API/Key | `../video-gen-pro/SKILL.md` |
| 剧本候选、拆段、连续性、确认门、复盘 | 本 skill |
| 问功能介绍／怎么用 | `../video-gen-guide/SKILL.md` |
| 只要 prompt 参考包、自己去 Sora/Veo3/Kling 跑 | `../video-gen-advisor/SKILL.md` |
| 三段式导演法写视频 prompt | `../video-gen-director/SKILL.md` |
| 故事板母图、九宫格/四栏/脚本拼版、4K 确认门 | `../video-gen-storyboard/SKILL.md` |
| 角色/场景/道具设定图、资产登记复用 | `../video-gen-assets/SKILL.md` |
| 运镜/景别/构图/光影/风格/参考图投放 | `../video-gen-cinematography/SKILL.md` |

## 前置条件路由

- 拆分门判定需要故事板母图时，先读 `../video-gen-storyboard/references/README.md` 再规划版式；母图版式不在本 skill。
- 镜头清单转最终 prompt 时，按所选方法去 `../video-gen-director/references/director-method.md` 或 `../video-gen-storyboard/references/storyboard-board.md`。
- 剧本拆出的资产清单要落成设定图/登记复用时，去 `../video-gen-assets/references/assets.md`。
- 确认门通过、进入真实生成时，交回 `../video-gen-pro/SKILL.md` 的强制执行协议走 CLI；本 skill 不直接调 API。

## References

| File | Load When |
|---|---|
| `references/generation-workflow.md` | 需要阶段提醒、剧本候选流程协议、素材清单、标准文本回复、生成前确认门、结构化修改意见或结果复盘 |
| `references/multi-segment-continuity.md` | 需要智能编排拆分门（Intelligent Orchestration Gate）、多段连续性台账、尾帧交接或 `extend` 链规划 |

## 不在本 skill 范围

- 故事板母图、版式、读图规则 → `../video-gen-storyboard/SKILL.md`。
- 三段式 prompt 骨架与写法 → `../video-gen-director/SKILL.md`。
- 槽位填法（运镜/景别/构图/风格）→ `../video-gen-cinematography/SKILL.md`。
- 调用火山方舟 API、任务管理、证据归档 → `../video-gen-pro/SKILL.md`。
