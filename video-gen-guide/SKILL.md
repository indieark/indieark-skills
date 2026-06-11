---
name: video-gen-guide
description: video-gen 技能族使用向导（usage guide／feature introduction／how to use）。用户问「这个视频 skill 能做什么／怎么用／有哪些模式／生成前要准备什么／边界在哪／为什么不触发」时使用；只解释能力、输入、确认门与下一步建议，不调 CLI、不构造 payload、不要求 API key。不负责：真实生成（走 video-gen-pro）、只要 prompt 参考包（走 video-gen-advisor）。
---

# Video Gen Guide 使用向导

开始前先读 `../video-gen-pro/SKILL.md` 挂载技能族公共规则（Execution Modes、Red Lines）。本 skill 是 video-gen 技能族的**说明卫星**（guide mode）：只解释、不出活。

## 何时使用

- 用户问「这个 Skill 能做什么 / 怎么用 / 功能介绍 / 使用向导 / 有哪些模式 / 生成前需要准备什么」。
- 用户对输入模式、角色卡、场景卡、道具卡、故事板、声音、生成前确认、结果复盘、CLI/API/Key、触发边界等具体功能有疑惑，但暂时不生成视频。
- 用户问边界场景「能不能做 / 该怎么选工具 / 为什么不触发」（如静态图、其他 provider、传统剪辑）。

## Hard Rules

- 必须先读 `references/guide-mode.md`，默认按它的 8 项结构详细说明；可按用户问题选择完整介绍或按需功能说明。
- 不调用 CLI、不构造 payload、不创建项目/资产/故事板、不要求 API key、不声明已生成结果。

## 意图路由（技能族）

| 用户意图 | 去哪 |
|---|---|
| 真实生成／提交／查询／下载视频任务、CLI/API/Key | `../video-gen-pro/SKILL.md` |
| 剧本候选、拆段、连续性、确认门、复盘 | `../video-gen-script/SKILL.md` |
| 问功能介绍／怎么用 | 本 skill |
| 只要 prompt 参考包、自己去 Sora/Veo3/Kling 跑 | `../video-gen-advisor/SKILL.md` |
| 三段式导演法写视频 prompt | `../video-gen-director/SKILL.md` |
| 故事板母图、九宫格/四栏/脚本拼版、4K 确认门 | `../video-gen-storyboard/SKILL.md` |
| 角色/场景/道具设定图、资产登记复用 | `../video-gen-assets/SKILL.md` |
| 运镜/景别/构图/光影/风格/参考图投放 | `../video-gen-cinematography/SKILL.md` |

## References

| File | Load When |
|---|---|
| `references/guide-mode.md` | 任何功能介绍、使用向导、支持模式、准备事项或边界说明请求（必读） |

## 不在本 skill 范围

- 用户从「问怎么用」转为「真的生成」时，交回 `../video-gen-pro/SKILL.md` 的强制执行协议。
- 介绍完后用户要参考包，去 `../video-gen-advisor/SKILL.md`。
