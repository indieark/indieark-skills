# Multi-Segment Continuity Method

> Load when: 一个项目要分多个 Seedance 视频段生成，或用户要求短剧、广告、系列内容在多条视频之间保持角色、场景、道具、动作或剧情连续。
> Avoid: 只生成单段 4-15 秒视频；先读 `storyboard-board.md` 决定故事板母图信息密度和版式。
> Pairs with: `setting-director.md` 做段落规划；`storyboard-board.md` 定义每段故事板母图；`character-sheet.md` / `scene-sheet.md` 锁定锚点；`seedance-handoff.md` 登记、确认和生成。

多段生成不能只靠一句 prompt 或同一个 seed 保证连续。正确做法是把连续性当成项目约束：每段都继承同一套角色图、场景图、风格规则和段落台账，并让后一段明确承接前一段的剧情状态。

连续不等于每段都接上一段尾帧。剧本拆分时先判断镜头边界，尽量让一个完整镜头落在一次生成里；除非确实是长镜头继续，否则不要把同一个镜头拆成两次生成。镜头发生切换时，后一段可以只承接角色、场景、道具和剧情状态，不必强行使用上一段尾帧。

关键判断发生在剧本阶段，而不是生成失败后补救。先把故事写清楚、把每段分在自然镜头边界上，AI 再根据镜头语言选择 `continuity_mode`：新机位或新景别通常是 `cut_continuity`；同一长镜头因为时长限制被迫跨段时，才必须使用 `extend` 或尾帧硬衔接；已经换镜头的段落不要为了“连续”强行接尾帧。

## Intelligent Orchestration Gate

<!-- contract: intelligent-orchestration-gate complexity-change-density-gate max-duration-not-target per-round-information-budget -->

智能编排的第一原则：15 秒是单次生成上限，不是默认目标。每个生成轮次的长度由剧情复杂度、场景变化度、角色数量、动作阶段、道具状态变化、镜头变化和声音/对白负载共同决定。

先判断每个候选段落的信息负载：

| Dimension | Low Load | High Load |
| --------- | -------- | --------- |
| 场景变化度 | 同一空间、光线稳定、背景关系稳定 | 多空间切换、光线变化、空间关系需要重新解释 |
| 角色负载 | 1-2 个角色，身份和服装稳定 | 多角色、多角色组、换装、身份关系需要解释 |
| 动作变化度 | 一个连续动作链或一个展示点 | 多个动作阶段、追逐、打斗、产品功能切换 |
| 镜头变化度 | 同一长镜头、缓慢推进、缓慢拉远、轻微摇移 | 多机位、多景别、正反打、主观视角、复杂调度 |
| 道具状态 | 道具少，状态稳定 | 关键道具位置、破损、佩戴、交接或状态变化多 |
| 声音文字 | 无对白或短声音 brief | 强对白、旁白、字幕、标题文字或声音节奏复杂 |

单段生成适合低负载内容：同一场景、人物不多、镜头语言稳定、动作连续、长镜头变化不大时，可以使用 10-15 秒单段故事板和单段视频。

多段生成适合高负载内容：即使总时长只有 15 秒，只要一个分镜里包含多场景、多角色组、多动作阶段、复杂运镜、强道具状态变化或高密度声音文字，就拆成多个更短故事板和视频段。例如 15 秒内容可以拆成 3 个 5 秒段落，每段一个故事板、一个 `video-prompt.txt`、一组相关参考图，再逐段生成并拼接。

复杂项目必须先输出智能编排表：

```text
智能编排判断：
- 总时长：
- 推荐生成轮次：<单段 / SD01+SD02+...>
- 15 秒是否作为上限而非目标：
- 单段可行性：<可行 / 不可行>，原因：
- 信息负载评估：
  - 场景变化度：
  - 角色负载：
  - 动作变化度：
  - 镜头变化度：
  - 道具状态：
  - 声音文字：
- 每段规划：
  - SD01：<时长>，<故事目标>，<场景>，<角色>，<核心动作>，<storyboard_id>
  - SD02：...
- 拼接/连续性策略：<cut_continuity / tail_frame_handoff / first_last_bridge / extend>
```

## Automatic Split Route

自动拆分的目标不是把长内容机械切成多条，而是让每一次视频生成只承载当前段真正相关的信息。Seedance 单次时长只能按 4-15 秒规划，这是硬限制；更核心的创作原则是控制每轮输入负载，让角色、场景、道具、故事板和声音信息保持相关、清晰、平均，不把整部片的无关信息塞进同一次生成。

默认决策顺序：

```text
用户输入
-> 智能编排门：判断 15 秒是否只是上限、单段是否可行、是否需要多故事板
-> 判断难度和信息负载
-> 生成或整理剧本
-> 从剧本分析角色卡、场景/背景卡、道具/产品卡需求
-> 按总时长、复杂度和镜头边界拆分生成轮次
-> 每轮只绑定本段相关的故事板、角色卡、场景卡、道具卡和声音 brief
-> 用户确认段落表与故事板后逐段生成
```

先判断是否能单段表达：

- 内容简单、总时长 4-15 秒、单一场景、少量角色、动作链清楚：可以只用一张故事板母图；若角色一致性重要，使用简稿故事板 + 角色卡。
- 同一角色的连续动作但信息不复杂：一张轻量故事板负责动作和镜头，角色卡负责脸、服装和体态，场景卡按需加入。
- 总时长超过 15 秒，或包含多个主要场景、多个角色组、战斗/追逐/产品功能切换、明显情绪段落、多个关键道具状态变化：必须拆成多段。
- 宣传片、短剧、系列广告、多人多场景战斗等任务，不要用一张大故事板和长 prompt 硬塞；应先写剧本，再拆 SD01 / SD02 / SD03，每段有自己的故事板和素材包。

每个生成轮次尽量满足：

- 时长在 4-15 秒内，且最好只承担一个剧情目标、展示点、动作阶段或情绪转折。
- 一个主场景或一个清楚的场景切换，不混入本段不会出现的场景卡。
- 只包含本段实际出现的角色卡、场景/背景卡、道具/产品卡和参考音频。
- 故事板只表达本段镜头顺序、动作节奏和调度，不替代角色/场景/道具卡。
- `video-prompt.txt` 只写本段读图规则、承接状态、声音 brief 和禁止项，不复述全片设定。

拆分后的每段可以负载不同，但不能一段极重、一段极轻。如果某段需要同时解释新角色、新空间、新道具、新冲突和复杂运镜，优先继续拆段、先补设定卡，或把信息移到故事板/卡片里，而不是把全部文字堆进视频 prompt。

## Continuity Targets

至少锁定这些连续性目标：

| Target | What to Preserve |
| ------ | ---------------- |
| 角色身份 | 脸、发型、年龄感、体型、服装、配饰、动作习惯 |
| 场景空间 | 入口出口、门窗、桌面、道具位置、光源方向 |
| 道具状态 | 产品、信物、伤痕、雨水、破损、手持物的位置和变化 |
| 时间线 | 每段发生顺序、上一段结束状态、下一段起始状态 |
| 镜头语言 | 画幅、景别节奏、运镜速度、景深、色彩和颗粒 |
| 声音节奏 | 是否有对白、环境声、音乐情绪和转场节奏 |

## Continuity Ladder

按可控性从低到高选择：

1. 只用同一段文字提示词：连续性弱，只适合草稿。
2. 复用同一项目的角色图、场景图和风格规则：基础一致性。
3. 为每段写清 `start_state`、`end_state` 和 `carry_over`：剧情连续性。
4. 每段登记独立故事板 `sb-sd01`、`sb-sd02`，但共用同一项目资产：可回溯。
5. 镜头切换但剧情连续：承接 `end_state`、角色卡、场景卡、道具状态和风格规则，不强制使用上一段尾帧。
6. 需要画面硬衔接：用上一段尾帧作为下一段 `first-frame`，或用 `first-last` 预设下一段首尾。
7. 如果下一段只是同一长镜头继续向前，优先用 `extend`，而不是重新生成一段无关视频。

不要把 `--seed` 当成连续性保证。相同 seed 只能降低部分随机性，不能在不同 prompt、不同参考图或不同段落之间锁死人物和场景。

## Segment Boundary Rules

拆段发生在剧本规划阶段，不应等到生成失败后再补救。

优先级：

1. 先按剧情节拍拆：每段只承担一个清楚动作、冲突、展示点或情绪转折。
2. 再按镜头边界拆：一个镜头尽量放进同一次生成，不把同一镜头拆成两段。
3. 先判断段落开头是不是同一个镜头继续；如果不是，就不要要求画面接尾帧。
4. 单个镜头超过模型可控时长时，才考虑拆成长镜头延续，并标记 `continuity_mode: extend` 或 `tail_frame_handoff`。
5. 如果镜头已经切到新机位、新景别、新空间或新动作阶段，标记 `continuity_mode: cut_continuity`，只承接剧情状态和资产锚点。
6. 如果下一段必须从上一段最后一帧无缝开始，标记 `continuity_mode: tail_frame_handoff`。
7. 如果下一段不仅要承接起点，还必须到达指定终点画面，标记 `continuity_mode: first_last_bridge`。

`continuity_mode` 由 Skill/AI 在剧本拆分时根据剧情和镜头语言判断。不要默认所有段落都走尾帧承接；尾帧是硬衔接工具，不是多段连续性的唯一手段。

## Segment Ledger

复杂项目必须先写连续性台账。格式可以简短，但每段都要有明确交接状态：

```text
Continuity Bible:
- Character lock:
- Scene lock:
- Style lock:
- Persistent props:
- Forbidden drift:

SD01:
- Story goal:
- Shot boundary:
- Continuity mode to next: cut_continuity / tail_frame_handoff / first_last_bridge / extend
- Start state:
- End state:
- Carry over to SD02:
- Reference assets:
- Storyboard:

SD02:
- Story goal:
- Shot boundary:
- Continuity mode from previous:
- Start state should continue SD01 story state:
- End state:
- Carry over to SD03:
- Reference assets:
- Storyboard:
```

`end_state` 不要写抽象情绪，要写可见状态，例如“女主右手握着红色钥匙站在门内，门缝漏出冷绿光，雨水打湿披风下摆”。

## Prompt Pattern

每段 `video-prompt.txt` 都要写明本段在全片中的位置：

```text
这是 <项目名> 的第 <SD02/N> 段，承接上一段的剧情状态。

全片连续性：
参考 @角色设定图 锁定人物身份、脸、发型、服装和配饰。
参考 @场景设定图 锁定空间结构、光源方向、关键道具和主色调。
遵守 style bible：<画幅/色彩/光线/镜头语言/声音节奏>。

上一段结束状态：
<SD01 end_state，写成可见画面和道具状态>

本段承接方式：
<cut_continuity / tail_frame_handoff / first_last_bridge / extend>。
如果是 cut_continuity，本段可以从新机位、新景别或新构图开始，但角色、场景、道具状态和剧情因果必须延续。
如果是 tail_frame_handoff，本段首帧必须接上一段尾帧。
如果是 extend，本段继续同一长镜头，不切机位。

本段起始状态：
从上一段结束状态延续，不要重置人物服装、道具状态、场景逻辑或已经发生的剧情；是否画面无缝接帧由本段承接方式决定。

本段镜头顺序：
镜头 1：<根据 continuity_mode 承接上一段尾帧或尾部状态，可为新机位/新景别>。
镜头 2：<推进动作>。
...
镜头 N：<本段结束状态，交给下一段>。

本段结束状态：
<SD02 end_state，供 SD03 继续使用>

禁止：
不要换脸、换服装、换场景结构、改变道具位置、跳过上一段结果、提前出现下一段才发生的事件。
```

## Image and Video Handoff

推荐做法：

- 每段都保留独立 `storyboard-prompt.txt` 和 `video-prompt.txt`。
- 故事板 ID 用段落编号，例如 `sb-sd01`、`sb-sd02`、`sb-sd03`。
- `cut_continuity`：镜头切换但剧情连续，继续用同一项目角色卡、场景卡、故事板和 `end_state`，不强制尾帧。
- `tail_frame_handoff`：需要画面无缝硬衔接时，生成上一段时保存尾帧，并把尾帧作为下一段 `first-frame`。
- `first_last_bridge`：下一段必须从上一段尾帧到达指定终点画面时，使用 `first-last`。
- `extend`：同一长镜头继续向前时，优先用 `extend --reference-video <SD01 video url>`。本地 MP4 需要先提供可访问 URL，或按 `cli.md` 使用 `--serve-local-assets cloudflare`。

项目化故事板路径示例：

```bash
seedance2 storyboard add <project-id> --storyboard-id sb-sd01 --image sd01-storyboard.png --prompt sd01-storyboard-prompt.txt --video-prompt sd01-video-prompt.txt
seedance2 storyboard approve <project-id> sb-sd01
seedance2 generate --project <project-id> --storyboard sb-sd01 --duration <seconds> --reference-image <character-card.png> --reference-image <scene-background-card.png> --wait

seedance2 storyboard add <project-id> --storyboard-id sb-sd02 --image sd02-storyboard.png --prompt sd02-storyboard-prompt.txt --video-prompt sd02-video-prompt.txt
seedance2 storyboard approve <project-id> sb-sd02
seedance2 generate --project <project-id> --storyboard sb-sd02 --duration <seconds> --reference-image <character-card.png> --reference-image <scene-background-card.png> --wait
```

剧情连续但镜头切换路径示例：

```bash
seedance2 storyboard add <project-id> --storyboard-id sb-sd02 --image sd02-storyboard.png --prompt sd02-storyboard-prompt.txt --video-prompt sd02-cut-continuity-prompt.txt
seedance2 storyboard approve <project-id> sb-sd02
seedance2 generate --project <project-id> --storyboard sb-sd02 --duration <seconds> --reference-image <character-card.png> --reference-image <scene-background-card.png> --wait
```

尾帧硬衔接路径示例：

```bash
seedance2 first-frame --first-frame sd01-last-frame.png --prompt-file sd02-video-prompt.txt --duration <seconds> --wait
```

同镜头延长路径示例：

```bash
seedance2 extend --reference-video <sd01-video-url> --prompt-file sd02-extension-prompt.txt --duration <seconds> --wait
```

## Confirmation Gate

多段生成前，先向用户展示：

- 段落数量和每段时长。
- 每段 `start_state` / `end_state`。
- 每段边界是否切镜头、换机位、换景别，还是同一长镜头继续。
- 每段 `continuity_mode`：剧情连续但切镜头 / 尾帧硬衔接 / 首尾帧桥接 / 长镜头延长。
- 角色图、场景图、风格规则是否共用。
- 哪些段落使用故事板图 + 角色卡 + 场景/背景卡承接，哪些段落还需要上一段尾帧、`first-last` 或 `extend`。
- 明确说明：多段生成可以显著提高连续性，但仍需要逐段验收和必要时重生成。

## Verification Checklist

- SD02 的起始状态是否承接 SD01 的结束状态；只有 `tail_frame_handoff` 或 `extend` 才要求画面首帧无缝接上。
- 人脸、发型、服装、配饰是否没有漂移。
- 场景光源、道具位置、天气和时间是否没有跳变。
- 道具状态是否按剧情变化，而不是随机重置。
- 每段 payload 是否同时包含段落故事板、角色卡和场景/背景卡。
- 每段 `generation-record.json` 是否能回溯到对应 `storyboard_id` 和 `video-prompt.txt`。
- 失败时是否只修正当前段或交接状态，而不是重写整个项目。

## Common Failures

| Symptom | Fix |
| ------- | --- |
| 第二段像重新开始 | 在 SD02 prompt 写入 SD01 end_state，并选择正确 `continuity_mode`；只有硬衔接才用尾帧 first frame |
| 角色漂移 | 回到 `character-sheet.md` 修 master 图，所有段落复用同一角色图 |
| 场景跳变 | 回到 `scene-sheet.md` 固定空间 DNA 和光源方向 |
| 道具状态丢失 | 在 segment ledger 里把道具位置和状态写入 `carry_over` |
| 同一镜头被拆成两段后不连贯 | 剧本重拆，尽量把同一镜头放入一次生成；过长时改 `extend` |
| 只靠 seed 仍不稳定 | 改用参考图、状态台账、尾帧承接、first-last 或 extend |
