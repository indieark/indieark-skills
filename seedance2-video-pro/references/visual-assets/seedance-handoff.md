# Seedance Handoff for Visual Assets

> Load when: 人物图、场景图或故事板母图已经生成或由用户提供，准备登记、确认并交给 Seedance 生成视频。
> Avoid: 还没有生成视觉资产提示词；先读对应的 `character-sheet.md`、`scene-sheet.md`、`storyboard-board.md`，再按需读 `grid-storyboard.md` 或 `four-column-storyboard.md`。
> Pairs with: `../visual-storyboard.md` 管确认门和生成历史；`../cli.md` 给完整命令；`../completion.md` 规范最终汇报。

本文件把外部图像工具生成的视觉资产交接给 `seedance2` CLI。CLI 不生成图片，只登记图片、提示词、确认记录和视频生成证据。

## Handoff Checklist

进入 Seedance 前必须能回答：

- 哪些图片是角色锚点，哪些是场景/背景锚点，哪张故事板母图是视频主运动参考图。
- 本次 Seedance payload 是否会同时包含故事板图、对应角色卡、场景/背景卡和必要道具/产品卡；不要只传故事板一张图来承担全部细节。
- 故事板或分镜里的每个 CUT 是否绑定了对应角色卡和场景卡；多张分镜拼版时，每张分镜也要有可回溯的 `character_refs` 和 `scene_ref`。
- 本次是单段生成、简稿故事板 + 角色卡，还是多个 4-15 秒生成轮次；拆分依据是否来自剧本复杂度、总时长和每轮输入负载。
- 每个生成轮次是否只包含本段相关故事板、角色卡、场景/背景卡、道具/产品卡和声音 brief，没有塞入其他段才出现的无关信息。
- 每张图片由谁提供或哪个外部工具生成，提示词保存在哪里。
- 故事板母图是否为 4K 或更高规格，图内文字、表格和说明是否清晰可读。
- 故事板母图是否从首版正式确认开始就是 4K 或等效 4K；低清草稿不得登记、确认或提交给 Seedance。
- `storyboard-prompt.txt` 是否保存完整绘图提示词，能解释故事板图片的结构、信息区和详细文本。
- 如果采用脚本拼版，是否保存了原子图片清单、composition manifest 和最终 4K 拼版图。
- `video-prompt.txt` 是否足够简短，只解释 Seedance 如何读取故事板母图、哪个区域决定运动、哪些区域只做约束。
- 最终输出规格是否锁定：画幅、清晰度/分辨率、时长、模型、是否等待完成和是否下载。
- 最终声音和文字轨道是否锁定：`generate_audio=true|false`、音乐/环境音/动作音效、说话人声、字幕、标题文字、logo、水印和随机字母策略。
- 最终生成输入是否锁定：实际提交哪些参考图、参考视频、参考音频和 prompt 文件；不提交当前段无关素材。
- 用户是否确认故事板图片和最终视频提示词。

## Register Project and Assets

创建项目：

```bash
seedance2 project create "<用户原始想法或项目标题>" --project-id <project-id>
```

登记人物图：

```bash
seedance2 asset add <project-id> --type character --name <角色名> --file <character.png> --purpose "<主角外貌锁定 / 三视图 master / 反派设定>"
```

登记场景图：

```bash
seedance2 asset add <project-id> --type scene --name <场景名> --file <scene.png> --purpose "<主场景空间锁定 / 产品广告桌面场景 / SC01 正面角度>"
```

保存剧本和风格规则：

```bash
seedance2 script set <project-id> --file <script.md>
seedance2 style set <project-id> --file <style.md>
```

## Write Storyboard Prompt

`storyboard-prompt.txt` 应保存给外部图像工具使用的完整提示词。内容至少包括：

- 图片类型：故事板母图；可说明使用九宫格、四栏、8 镜头、制作设定板或自定义版式。
- 图片规格：4K 或更高，长边不少于 3840 px，或外部工具的等效 4K 档。
- 预览策略：不设置低清预览确认门；第一张进入登记和用户确认流程的故事板图必须为 4K 或等效 4K。
- 使用的角色图、场景图、产品图或风格图。
- 角色/产品/场景锁定规则。
- 每个分镜或 CUT 对应的角色卡、场景卡和必要产品卡；CUT 图生成时必须参考这些卡，不允许脱离卡片自行改变人物、服装、空间、光线或关键道具。
- 信息区、镜头区、读图顺序、哪个区域决定视频运动。
- 需要进入图内的详细文本、表格、对白、灯光、声音、情绪和摄影说明。
- 如果是脚本拼版：原子图片提示词摘要、CUT 时间码、文本区内容、排版清单、字体/色彩和最终输出规格。
- 禁止项：乱码文字、水印、无关角色、角色漂移、场景跳变。

不要只保存一句“生成故事板”。后续 debug 需要知道故事板图是怎么来的。

## Write Video Prompt

`video-prompt.txt` 不等同于故事板绘图提示词。它的任务是告诉 Seedance 如何读图。故事板母图默认是视频主运动参考图；角色卡和场景/背景卡是人物、空间、背景层次和道具细节参考；九宫格、四栏、8 镜头或制作设定板只是版式。如果本次故事板已经按场景调整格数、栏目或镜头密度，按实际结构写，不要硬补镜头 1-9。

故事板图越完整，`video-prompt.txt` 越要短。不要把 `storyboard-prompt.txt` 或图内镜头表逐字复制给 Seedance；让模型把注意力放回 4K 故事板图片。只有当爆炸、粒子、烟雾、复杂群体运动等动态无法在图里表达清楚时，才在视频 prompt 里补一两句关键动态。

<!-- contract: storyboard-concise-prompt no-storyboard-detailed-per-shot-prompt speech-track text-track -->

这条“短 prompt”只适用于已有故事板母图的路径。没有故事板时，回到 `../director.md` 的详细视频生成提示词结构，按每个分镜写清视觉内容、镜头参数、音频轨道、说话人声、字幕/标题文字和转场；不要用故事板路径的极简读图 prompt 代替详细分镜 prompt。

<!-- contract: final-input-lock storyboard-does-not-replace-final-prompt output-spec-lock no-unneeded-generation-inputs -->

短 prompt 不能省略最终输入控制。故事板控制镜头内容、动作和调度；`video-prompt.txt` 仍必须写清输出规格、声音策略、说话人声、字幕/标题文字和参考素材主次。声音不能只靠 `--generate-audio true`。如果本次生成有声，`video-prompt.txt` 必须保留声音 brief，写清音乐、环境音、动作音效、说话人声/无说话人声、字幕/标题文字策略或参考音频用途；如果没有声音方案或用户要无声，命令必须用 `--generate-audio false`，并在 prompt 写明不要音乐、对白、旁白、环境音、字幕、标题文字、logo、水印或随机字母。

通用故事板母图写法：

```text
参考图1是 @故事板母图，用于决定 <时长> 秒 <画幅> 视频的镜头顺序、动作节奏和调度。
参考图2..N 是本段对应角色卡、场景/背景卡和必要道具/产品卡，用于锁定人物、空间、背景层次和关键道具细节。
输出规格：<画幅>，<清晰度/分辨率>，<时长> 秒，<有声/无声/参考音频驱动>。

读图规则：
- <分镜故事区 / 镜头网格 / 指定区域> 决定视频镜头顺序、动作连续性和情绪节奏。
- 角色卡参考图优先锁定人物/产品外观，不让故事板里的简化人物覆盖角色卡。
- 场景/背景卡参考图优先锁定空间结构、背景层次、光线和道具，不让故事板里的简化背景覆盖场景卡。
- <调度信息区> 用于理解人物移动和镜头运动。
- <灯光/色彩/声音/摄影区> 用于统一风格，不新增剧情。
- 声音与文字：<无声 / 音乐风格 / 环境音 / 动作音效 / 说话人声或无说话人声 / 字幕或标题文字策略 / 不要 logo、水印或随机字母>。

运动目标：
按故事板母图中已写明的镜头顺序，把关键画面连接成连续动作和连续情绪。

保持角色卡中的人物、服装和配饰一致；保持场景/背景卡中的空间、光线和道具一致；按故事板母图执行镜头和运动。
不要把说明区当成新剧情，不要新增故事板之外的角色、场景或结果。
```

分镜母图写法：

```text
参考 @分镜母图 生成一段 <时长> 秒 <画幅> 视频。
请按分镜母图中的实际读图顺序理解镜头，把关键画面连接成连续动作。
镜头 1：...
镜头 2：...
...
镜头 N：...
保持人物、服装、场景、光线、道具和风格一致；不要新增分镜之外的剧情。
```

四栏故事板写法：

```text
参考 @故事板图片 生成一段 <时长> 秒 <画幅> 视频。
前三栏用于稳定主视觉、人物/产品细节和场景关系；第四栏或指定分镜区决定镜头顺序。
按第四栏的实际镜头顺序连续生成：...
保持故事板中的人物/产品、服装/外观、场景、光线、主色调和整体风格一致。
不要新增故事板之外的角色、地点、卖点或结局。
```

脚本拼版故事板写法：

```text
参考 @脚本拼版故事板 生成 <时长> 秒 <画幅> 视频。
CUT 区按编号和时间码决定镜头顺序、动作连续性和情绪推进。
每个 CUT 已按清单绑定对应角色卡和场景卡；角色设定区只锁定人物外观；场景布局区只锁定空间、站位和镜头运动；灯光、声音、色彩和风格区只统一氛围。
按 CUT 1 到 CUT N 连接成连续视频，保持人物、服装、场景、道具、光线和色彩一致。
不要把说明区当成新剧情，不要新增故事板之外的角色、场景、对白或结果。
```

多参考备用路径写法：

```text
参考图1用于故事板镜头顺序和调度；参考图2用于主角外貌和服装；参考图3用于场景/背景空间、光线和关键道具。
以参考图1作为主运动参考图，参考图2和参考图3只用于一致性约束，不新增剧情。
```

如果有多张图，prompt 必须说明主次，避免模型自行混合。

多段视频写法：

```text
这是 <项目名> 的第 <SD02/N> 段，承接上一段的剧情状态。
本段是按剧本复杂度、总时长和输入负载拆出的独立生成轮次；只读取本段相关参考图，不读取其他段的角色/场景/道具。
上一段结束状态：<可见画面、人物位置、道具状态、光线和情绪落点>。
本段承接方式：<cut_continuity / tail_frame_handoff / first_last_bridge / extend>。
本段起始状态：从上一段结束状态延续，不重置人物、道具、场景或光线；如果是 cut_continuity，可以切到新机位、新景别或新构图。
本段镜头顺序：镜头 1 ... 镜头 N ...
本段结束状态：<交给下一段的可见状态>。
参考图用途：角色图锁定身份；场景图锁定空间；故事板图锁定本段镜头顺序；上一段尾帧只在 tail_frame_handoff / first_last_bridge 时用于起始画面。
```

不要默认每段都用上一段尾帧。镜头切换时，通常只承接剧情状态、角色卡、场景卡和道具状态；如果下一段要画面硬衔接，才把上一段尾帧作为下一段 `first-frame`。如果只是同一长镜头继续向前，优先走 `extend`，不要重新抽一段独立视频。

## Register Storyboard

登记故事板图片、故事板绘图提示词和视频提示词：

```bash
seedance2 storyboard add <project-id> --storyboard-id <storyboard-id> --image <storyboard.png> --prompt <storyboard-prompt.txt> --video-prompt <video-prompt.txt>
```

向用户展示：

- 故事板图片路径或可视预览。
- `storyboard-prompt.txt` 摘要。
- `video-prompt.txt` 全文或摘要。
- 将调用的模型、画幅、清晰度/分辨率、时长、有声/无声、说话人声、字幕/标题文字和实际提交输入。

用户确认后：

```bash
seedance2 storyboard approve <project-id> <storyboard-id>
```

如果用户要求绕过确认，回复中说明这是快速抽样路径，并使用 `--allow-unapproved-storyboard`。

## Generate

默认项目化生成：

```bash
seedance2 generate --project <project-id> --storyboard <storyboard-id> --duration <seconds> --ratio <ratio> --generate-audio <true|false> --reference-image <character-card.png> --reference-image <scene-background-card.png> --wait
```

需要下载：

```bash
seedance2 generate --project <project-id> --storyboard <storyboard-id> --duration <seconds> --ratio <ratio> --generate-audio <true|false> --reference-image <character-card.png> --reference-image <scene-background-card.png> --wait --download <output-dir>
```

`generate` 会把故事板图作为 `参考图1`，再按命令行顺序追加 `--reference-image`。复杂任务中，后续参考图应优先放角色卡、场景/背景卡、道具/产品卡；`video-prompt.txt` 必须写清 `参考图1`、`参考图2`、`参考图3` 等用途。只有简单快速抽样或用户明确接受低一致性风险时，才允许只传故事板图。

多段生成时，每段用独立故事板 ID 和独立 run。剧情连续但镜头切换时，下一段可以继续用 `generate --project --storyboard`，不必使用上一段尾帧：

```bash
seedance2 generate --project <project-id> --storyboard sb-sd02 --duration <seconds> --reference-image <character-card.png> --reference-image <scene-background-card.png> --wait
```

只有需要画面硬衔接时，生成当前段才需要保留尾帧，并把结果尾帧用于下一段 `first-frame` 或 `first-last`：

```bash
seedance2 generate --project <project-id> --storyboard sb-sd01 --duration <seconds> --return-last-frame --wait
seedance2 first-frame --first-frame sd01-last-frame.png --prompt-file sd02-video-prompt.txt --duration <seconds> --wait
```

如果下一段只是延长上一段同一镜头：

```bash
seedance2 extend --reference-video <sd01-video-url> --prompt-file sd02-extension-prompt.txt --duration <seconds> --wait
```

提交前不确定时先 dry run：

```bash
seedance2 generate --project <project-id> --storyboard <storyboard-id> --duration <seconds> --reference-image <character-card.png> --reference-image <scene-background-card.png> --dry-run-payload
```

## Verify Artifacts

执行后检查：

- `prompt.txt` 是否等于或来自 `video-prompt.txt`。
- `request-payload-redacted.json` 是否包含预期故事板图、角色卡、场景/背景卡和参数。
- `media-manifest.json` 是否记录故事板图片、角色卡、场景/背景卡、来源摘要、处理状态和 reference index。
- `generation-log.json` 是否记录 `project_context`。
- `generation-record.json` 是否写回项目历史。
- `storyboard-prompt.txt` 或 composition manifest 是否能追溯每个 CUT 使用的角色卡和场景卡。
- 真实提交时检查 `submit-summary.json`；等待完成时检查 `task-result.json` 和本地 MP4 或 `content.video_url`。

## Completion Report

最终回复按 `../completion.md`，并额外包含：

- 用户原始输入或项目目标。
- 使用的角色图、场景图、故事板图。
- 实际提交的 `video-prompt.txt` 摘要或全文。
- `storyboard-prompt.txt` 路径。
- 如果是脚本拼版，说明原子图片数量、composition manifest 或拼版清单路径。
- `project_id`、`storyboard_id`、`run_id`。
- 是否已确认故事板，是否真实提交，是否等待和下载。
- 多段项目还要说明段落编号、上一段结束状态、本段起始状态、承接素材和下一段风险。

## Debug Signals

| Symptom | Likely Cause | Fix |
| ------- | ------------ | --- |
| 视频没有按故事板顺序 | `video-prompt.txt` 没按实际结构说明 | 重写镜头顺序，再生成 |
| 第二段像重新开始 | 没写上一段 `end_state` 或承接方式选错 | 补连续性台账和 `continuity_mode`；只有硬衔接才用上一段尾帧做 `first-frame` |
| 角色不像设定图 | 故事板图里角色已漂移 | 回到 `character-sheet.md` 修 master 图 |
| 场景光线跳变 | 场景图或故事板缺光源锚点 | 回到 `scene-sheet.md` 固定主光和空间 DNA |
| 背景或道具细节丢失 | 只提交了故事板，没有提交场景/背景卡或道具卡 | 重新生成时把场景/背景卡、道具/产品卡作为 `--reference-image` 一起输入 |
| 产品变形 | 故事板没有产品细节锁定 | 回到 `storyboard-board.md` 加产品细节区，必要时参考 `four-column-storyboard.md` |
| 结果无法回溯 | 没保存 prompt 或未登记资产 | 补登记，不要直接把散图交给 Seedance |
