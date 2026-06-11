---
name: video-gen-storyboard
description: 故事板法（storyboard method／visual consistency）。需要严格画面一致性、以图控视频时使用：故事板母图主控镜头顺序与运动、九宫格／四栏／脚本拼版三种版式、项目资产库与生成历史、4K 故事板确认门。不负责：纯文字三段式 prompt（走 video-gen-director）、多段拆分与连续性台账（走 video-gen-script）、角色场景设定图生成（走 video-gen-assets）、真实生成执行（走 video-gen-pro）。
---

# Video Gen Storyboard 故事板法

开始前先读 `../video-gen-pro/SKILL.md` 挂载技能族公共规则（Execution Modes、Red Lines）。本 skill 是 video-gen 技能族的**方法论卫星**：故事板法（母图主控、以图控视频）的 canonical。

## 何时使用

- 用户要「故事板／分镜母图／九宫格／四栏／脚本拼版」，或任务需要严格画面一致性、多镜头同角色同场景。
- 方法选择门（`../video-gen-pro/references/methods.md`）判定走故事板法时。
- 用户有现成剧本/脚本，要把它拼进母图版式（脚本拼版故事板）时。

## Hard Rules

- 必须先读 `references/README.md` 选版式，再读对应版式文件；端到端流程按 `references/visual-storyboard.md`。
- **4K 故事板确认门是红线**：母图未经用户确认不得投入视频生成（Red Lines 全文在 `../video-gen-pro/SKILL.md`）。
- 故事板母图由外部 `image-gen-pro` skill 生成，本技能族不接管图像 CLI。

## 意图路由（技能族）

| 用户意图 | 去哪 |
|---|---|
| 真实生成／提交／查询／下载视频任务、CLI/API/Key | `../video-gen-pro/SKILL.md` |
| 剧本候选、拆段、连续性、确认门、复盘 | `../video-gen-script/SKILL.md` |
| 问功能介绍／怎么用 | `../video-gen-guide/SKILL.md` |
| 只要 prompt 参考包、自己去 Sora/Veo3/Kling 跑 | `../video-gen-advisor/SKILL.md` |
| 三段式导演法写视频 prompt | `../video-gen-director/SKILL.md` |
| 故事板母图、九宫格/四栏/脚本拼版、4K 确认门 | 本 skill |
| 角色/场景/道具设定图、资产登记复用 | `../video-gen-assets/SKILL.md` |
| 运镜/景别/构图/光影/风格/参考图投放 | `../video-gen-cinematography/SKILL.md` |

## 前置条件路由

- 多段拆分、连续性台账、尾帧交接前，MUST 先读 `../video-gen-script/references/multi-segment-continuity.md`。
- 角色/场景/道具设定图缺失时，先走 `../video-gen-assets/SKILL.md` 生成并登记；交接规则见 `../video-gen-assets/references/seedance-handoff.md`。
- 把镜头清单转写为详细分镜 prompt 时，按 `../video-gen-director/references/director-method.md` 三段式；槽位填料读 `../video-gen-cinematography/references/input.md`。
- 母图确认后回 `../video-gen-pro/SKILL.md` 走真实生成。

## References

| File | Load When |
|---|---|
| `references/README.md` | 任何故事板请求先读：版式选择门与流程总览 |
| `references/visual-storyboard.md` | 端到端执行流程：检索门、母图生成、4K 确认门、切片投产 |
| `references/storyboard-board.md` | 项目资产库与故事板登记、生成历史 |
| `references/grid-storyboard.md` | 九宫格版式细则 |
| `references/four-column-storyboard.md` | 四栏版式细则 |
| `references/script-composed-storyboard.md` | 脚本拼版版式细则（现成剧本拼进母图） |
