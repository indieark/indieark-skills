---
name: video-gen-director
description: 导演法三段式视频 prompt 方法论（director method／video prompt writing）。用语言控制为主、不预画母图：需要按三段式骨架（基础设定＋氛围与画质＋画面内容）写视频 prompt、做单镜头或少镜头控场、把时序递进写进画面内容时使用。不负责：图像母图主控与版式（走 video-gen-storyboard）、运镜景别构图等槽位填法库（走 video-gen-cinematography）、真实生成执行（走 video-gen-pro）。
---

# Video Gen Director 导演法

开始前先读 `../video-gen-pro/SKILL.md` 挂载技能族公共规则（Execution Modes、Red Lines）。本 skill 是 video-gen 技能族的**方法论卫星**：导演法三段式 prompt 写法的 canonical。

## 何时使用

- 用户要「用三段式／导演法写视频 prompt」，或任务以语言控制为主、单镜头/少镜头、不需要预画母图。
- 方法选择门（`../video-gen-pro/references/methods.md`）判定走导演法时。
- 故事板法流程中把镜头清单转写为详细分镜 prompt 时（visual-storyboard 流程会路由到这里）。

## Hard Rules

- 必须读 `references/director-method.md` 并按其三段式骨架产出：基础设定（主体／场景／风格核心）＋ 氛围与画质 ＋ 画面内容（时序递进）。
- 最终 prompt 严格三段，三段之外**零追加**；多段 Prompt Pattern 仅限故事板法使用。

## 意图路由（技能族）

| 用户意图 | 去哪 |
|---|---|
| 真实生成／提交／查询／下载视频任务、CLI/API/Key | `../video-gen-pro/SKILL.md` |
| 剧本候选、拆段、连续性、确认门、复盘 | `../video-gen-script/SKILL.md` |
| 问功能介绍／怎么用 | `../video-gen-guide/SKILL.md` |
| 只要 prompt 参考包、自己去 Sora/Veo3/Kling 跑 | `../video-gen-advisor/SKILL.md` |
| 三段式导演法写视频 prompt | 本 skill |
| 故事板母图、九宫格/四栏/脚本拼版、4K 确认门 | `../video-gen-storyboard/SKILL.md` |
| 角色/场景/道具设定图、资产登记复用 | `../video-gen-assets/SKILL.md` |
| 运镜/景别/构图/光影/风格/参考图投放 | `../video-gen-cinematography/SKILL.md` |

## 前置条件路由

- 填运镜、景别、构图、光影、视觉基调、风格核心、时间氛围等槽位时，MUST 按需读 `../video-gen-cinematography/references/input/` 下对应文件（入口 `../video-gen-cinematography/references/input.md`）。
- 资产引用详略与命名一致性按 `../video-gen-pro/references/concepts.md`；声音描写按 `../video-gen-pro/references/sound-design.md`。
- prompt 写好后回 `../video-gen-pro/SKILL.md` 走确认门与真实生成；多段连续性问题转 `../video-gen-script/SKILL.md`。

## References

| File | Load When |
|---|---|
| `references/director-method.md` | 任何导演法写 prompt 请求（必读）：三段式骨架、控场技巧、时序递进写法、正反例 |
