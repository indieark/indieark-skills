---
name: video-gen-advisor
description: 视频参考包模式（advisor mode／prompt-only／no generation）。用户说「只要 prompt／只给提示词／给我参考包／给我素材包／我自己去 Sora、Veo3、Kling、Runway、Pixverse、Hailuo、Pika、即梦、Vidu 跑」时使用：输出 master prompt＋平台变体＋镜头清单＋资产 brief＋声音 brief＋评判 checklist，不调火山方舟 API、不出视频、不创建真实记录。不负责：真实生成执行（走 video-gen-pro）、功能介绍（走 video-gen-guide）。
---

# Video Gen Advisor 参考包模式

开始前先读 `../video-gen-pro/SKILL.md` 挂载技能族公共规则（Execution Modes、Red Lines）。本 skill 是 video-gen 技能族的**参考包卫星**（advisor mode）：交付完整参考包，让用户去任意平台自己跑。

## 何时使用

- 用户说「参考模式 / advisor mode / 不要生成 / 我自己去 Sora|Veo3|Kling|Runway|Pixverse|Hailuo|MiniMax|Pika|即梦|Vidu 跑 / 只要 prompt / 只给提示词 / 给我素材包 / 给我参考包 / 给我资产」。
- 用户明确指定其他视频 provider 但仍要本技能族的导演化方案。

## Hard Rules

- 必须读 `references/advisor-mode.md`，输出参考包必给项：master prompt、平台变体、镜头清单、资产 brief、声音 brief、评判 checklist。
- 只允许调用只读 CLI（`config list` / `doctor` / `project list` / `asset search|list|show` / `history list|show`）和 6 个模式子命令的 `--dry-run-payload` 形式。
- 禁止调火山方舟 API、禁止 `wait` / `status`、不要求 API key、不声明已生成视频、不创建项目/资产/故事板真实记录。
- 用户从 advisor mode 切回真实生成时，按 `../video-gen-pro/references/interaction.md` 的 Advisor Mode 越界确认处理，再交回 `../video-gen-pro/SKILL.md`。

## 意图路由（技能族）

| 用户意图 | 去哪 |
|---|---|
| 真实生成／提交／查询／下载视频任务、CLI/API/Key | `../video-gen-pro/SKILL.md` |
| 剧本候选、拆段、连续性、确认门、复盘 | `../video-gen-script/SKILL.md` |
| 问功能介绍／怎么用 | `../video-gen-guide/SKILL.md` |
| 只要 prompt 参考包、自己去其他平台跑 | 本 skill |
| 三段式导演法写视频 prompt | `../video-gen-director/SKILL.md` |
| 故事板母图、九宫格/四栏/脚本拼版、4K 确认门 | `../video-gen-storyboard/SKILL.md` |
| 角色/场景/道具设定图、资产登记复用 | `../video-gen-assets/SKILL.md` |
| 运镜/景别/构图/光影/风格/参考图投放 | `../video-gen-cinematography/SKILL.md` |

## 前置条件路由

- 镜头方案按需读 `../video-gen-director/references/director-method.md`、`../video-gen-pro/references/scenes.md`、`../video-gen-pro/references/methods.md`。
- 复杂任务的资产 brief 与拆段建议按需读 `../video-gen-assets/references/assets.md`、`../video-gen-storyboard/references/visual-storyboard.md`、`../video-gen-pro/references/sound-design.md`、`../video-gen-script/references/multi-segment-continuity.md`。

## References

| File | Load When |
|---|---|
| `references/advisor-mode.md` | 任何参考包请求（必读）：触发词清单、Hard Rules、参考包必给项、平台变体规则 |
