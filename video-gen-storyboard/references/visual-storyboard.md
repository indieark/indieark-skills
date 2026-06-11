# Visual Storyboard Workflow Reference

> Load when: 用户要做短剧、广告、系列内容、角色一致性任务，或已经有角色图/场景图/故事板图，需要避免直接抽卡。
> Avoid: 用户明确只要一次快速草稿、只查任务状态、只问 API 参数，或只做传统视频剪辑。
> Pairs with: `../../video-gen-pro/references/router.md` 判断是否进入项目库；`../../video-gen-assets/references/assets.md` 规划人物/场景资产；`../../video-gen-pro/references/cli.md` 执行 project/storyboard/generate 命令；`../../video-gen-pro/references/completion.md` 汇报项目、故事板和生成记录。

本文件定义复杂视频任务的默认创作路径：先建立项目资产、做生成前资产检索、保留生成前确认，最后生成视频。**项目库 / 资产检索 / 确认门是复杂任务的默认质量门**（防止闷头抽卡、保证可回溯），任何复杂任务都走，**和是否用故事板无关**。**故事板是偏好驱动的可选产物**：用户需要严格画面一致性（系列、多段反复复用同一角色/场景，或直接要故事板）时才生成 4K 故事板母图；复杂但无一致性诉求时，走导演法 prompt-heavy 用语言控制直接生成，同样经过确认门，不强制先出故事板。它不替代 `../../video-gen-director/references/director-method.md`；后者是导演法的文字为主、资产为辅控场（三段式骨架：基础设定 + 氛围与画质 + 画面内容，时序递进写在画面内容里，用资产但不另生成图像母图），这里管理可保存、可确认、可回溯的视觉故事板资产。

端到端阶段提醒、剧本候选、资产批量确认、结构化修改意见、生成前所有输入确认和结果复盘以 `../../video-gen-script/references/generation-workflow.md` 为准。本文件只定义项目库和视觉故事板资产怎么登记、确认和回溯。

视觉故事板适合清楚、可规划、需要一致性的镜头；是否用它由一致性诉求决定，而非任务复杂度。一旦决定用故事板，故事板图片从首版正式生成开始就必须按 4K 或更高规格生成；当前流程不设置低清预览确认门，低清草稿不得登记为故事板资产或提交给 Seedance。故事板可以承载详细文本、表格、镜头说明、对白、灯光、声音和情绪节奏；最终提交给 Seedance 的 `video-prompt.txt` 应保持简短，让模型集中读取故事板图的镜头顺序和调度。故事板不单独负责人物、背景和道具细节锁定；复杂任务提交视频时必须把相关角色卡、场景/背景卡和必要道具/产品卡一起作为参考图输入。若主要效果是爆炸、粒子、烟雾、混乱战场或强抽象动态，优先使用 prompt-heavy 或混合路径，不强行套故事板。

## 生成前检索门

进入复杂任务后，先调研和检索本地项目库，不要默认新建一套资产。

推荐顺序：

1. 用 `project list` 找是否已有相关项目。
2. 用 `asset search --query`、`asset search --tag` 或 `asset search --role` 查已有角色图、场景图和参考图。
3. 对候选资产用 `asset show <project-id> <asset-id>` 看来源、存储路径、hash、用途、标签和描述。
4. 已有项目继续看 `storyboard show` 与 `history list/show`，判断是复用、迭代，还是补登记。

命中角色或场景资产时，不要直接跳过。先给用户展示候选资产的 `project_id`、`asset_id`、名称、用途、来源和预览路径，让用户确认“复用 / 新生成 / 另选候选”。只有缺失、质量不合适或用户明确要新版本时，才调用外部图像工具生成新人物/场景/故事板图并登记。

## Cross-Project Asset Reuse

角色卡和场景卡都是可跨项目复用的创作资产。默认复用闭环是：

1. `asset search` 跨项目找到候选。
2. `asset show` 查看来源项目、资产用途、素材路径、hash、标签和别名。
3. 向用户确认复用哪个候选，以及是否沿用原名称、角色、标签和用途。
4. 长期复用到当前项目时，执行 `asset reuse <target_project_id> <source_project_id> <source_asset_id>`；本地文件会复制到当前项目资产目录，外部素材会登记同一 source，并在新 `asset.json` 写入 `reused_from`。
5. 只做一次快速试生成时，可以临时引用 `asset show` 返回的 `material.stored_path` 或 `material.source` 作为 `--reference-image`，但最终回复必须说明这是未登记到当前项目的一次性引用。

复用后的角色/场景资产与新生成资产同等使用：故事板、CUT、`video-prompt.txt` 和 `generation-record.json` 都必须继续写清 `character_refs`、`scene_ref`、素材编号和来源项目，避免日后无法追溯。

## 何时进入项目库

默认进入项目库的场景：

- 短剧、广告、产品宣传、系列内容。
- 角色一致性、场景一致性或风格一致性要求高。
- 用户提供了角色图、场景图、剧本、品牌规范或故事板。
- 用户一句话想法明显会演化成多轮调优任务。

允许快速路径的场景：

- 用户明确说直接生成、快速草稿、先抽一版。
- 只有一个简单动作，且成本和回溯风险低。
- 用户明确绕过项目库。

快速路径也必须保留现有 run artifact；回复里说明这是快速抽样路径，稳定性低于项目库 + 视觉故事板路径。

## 默认流程

通用前段（任何复杂任务都走，与是否用故事板无关）：

```text
用户想法
-> project list / asset search 检索已有项目和素材
-> 复用候选项目/资产，或 videogen project create
-> 判断内容复杂度、总时长和每轮输入负载，并判断是否需要严格画面一致性
-> 生成或整理剧本，并从剧本分析需要的角色卡、场景/背景卡、道具/产品卡
-> 复用候选角色/场景资产（asset reuse），或 asset add character / scene
-> script set / style set
```

分叉：需要严格一致性（系列、多段反复复用同一角色/场景，或用户直接要故事板）走**故事板分支**；否则走**导演法 prompt-heavy 分支**。

故事板分支：

```text
-> storyboard plan
-> 按 assets.md 选择必要子方法，调用外部图像工具生成人物/场景/故事板图
-> 信息密集或需要中文文字/表格时，可直接生成完整 4K 故事板母图；需要确定性可编辑文字、指定字体/品牌版式、超密集 CUT 表或程序化复盘时，再按 script-composed-storyboard.md 脚本拼成 4K 故事板
-> storyboard add
-> 向用户展示 4K 故事板图 + storyboard-prompt.txt 摘要 + 简短 video-prompt.txt
-> storyboard approve
-> generate --project --storyboard，并追加对应角色卡、场景/背景卡为 `--reference-image`
-> history list/show 回溯
```

导演法 prompt-heavy 分支（复杂但无严格一致性诉求）：

```text
-> 按 ../../video-gen-director/references/director-method.md 把镜头清单转为详细分镜化 video-prompt.txt，用语言控制画面、镜头、声音和文字
-> 需要时仍可调用角色卡、场景/背景卡、道具/产品卡作为参考图灵活辅助，但不生成 4K 故事板母图
-> 向用户展示最终 video-prompt.txt + 参考素材清单 + 声音 brief
-> 经确认门后 generate，并按需追加 `--reference-image`
-> history list/show 回溯
```

## 多段连续性

如果一个项目要分多个视频生成，不要把每段当成彼此独立的新任务。先读 `../../video-gen-script/references/multi-segment-continuity.md`，把连续性写成项目资产和段落交接约束。

拆分的核心逻辑是内容复杂度、总时长和每轮输入负载。时长上限 4-15 秒是模型限制；更重要的是让每次生成只接收本段相关信息，避免把全片所有角色、场景、动作和道具塞进同一个 payload。内容简单且一张故事板能表达时，单段即可；同一角色的连续动作可以用简稿故事板 + 角色卡；宣传片、多人多场景战斗、短剧或多个产品卖点，应先拆剧本，再按段生成故事板和视频。

推荐流程：

1. 用同一 `project_id` 保存角色图、场景图、剧本、风格规则和所有故事板。
2. 先从用户输入生成或整理剧本，再从剧本分析需要哪些角色卡、场景/背景卡、道具/产品卡。
3. 在剧本拆分时优先按剧情节拍和镜头边界切段，尽量不要把同一个镜头拆成两次生成；如果必须跨段，先判定它是否是同一长镜头延续。
4. 在 `script.md` 或单独台账里写清每段 `start_state`、`end_state`、`carry_over` 和 `continuity_mode`。
5. 每段使用独立故事板 ID，例如 `sb-sd01`、`sb-sd02`、`sb-sd03`。
6. 每段只提交本段相关的故事板、角色卡、场景/背景卡、道具/产品卡和声音 brief；不要把其他段才出现的素材一起提交。
7. 后一段的 `video-prompt.txt` 必须显式承接前一段 `end_state`，不要只写“继续上一段”。
8. 镜头切换时只承接剧情状态和资产锚点，不强制尾帧；需要画面硬衔接时，用上一段尾帧作为下一段 `first-frame`，或用 `first-last` 预设首尾；同一长镜头继续向前时必须按长镜头处理，优先用 `extend`，或用尾帧硬衔接。
9. 每段生成后用 `history show` 回看 prompt、故事板和素材，再决定下一段是否继续、修正或重生成。

这条路径能显著提高多段连续性，但不能承诺模型在独立生成之间绝对一致。完成回复要说明已采取的连续性约束和仍需逐段验收的风险。

## 用户确认门

复杂任务保留以下确认点。第 1、4、5 点是通用门，任何复杂任务都走；第 2、3 点仅在走故事板分支时适用，导演法 prompt-heavy 分支跳过（其 video-prompt.txt 本身更详细，在第 4 点统一确认）：

1. 设定确认：角色、场景、风格、时长、画幅。
2. 故事板确认（仅故事板分支）：哪张 4K 故事板图片、对应什么镜头顺序、图内文字/表格是否可读。
3. 配套参考图确认（仅故事板分支）：本段会和故事板一起提交哪些角色卡、场景/背景卡、道具/产品卡。
4. 视频提示词确认：最终提交给 Seedance 的 prompt（故事板分支为短读图 prompt，导演法分支为详细分镜化 prompt）、参考图编号用途、素材主次和声音 brief；无声任务确认 `generate_audio=false`。
5. 生成确认：是否真实调用 API、是否等待、是否下载。

多段项目还要确认段落表：每段时长、起始状态、结束状态、镜头边界、`continuity_mode`、承接素材，以及哪些段落只做剧情连续、哪些段落使用尾帧承接、`first-last` 或 `extend`。

自动拆分项目还要确认：为什么选择单段或多段、每段承担的剧情目标、本段参考图清单是否只包含相关角色/场景/道具、是否存在输入过载段落需要继续拆分。

如果用户已经明确授权某一步，可以合并确认，但不要在未确认视频提示词时直接提交复杂任务；走故事板分支时还必须先确认 4K 故事板图。

最终生成前确认当前默认使用标准文本格式 + 结构化 JSON 字段。Agent 收到结构化修改意见 JSON 后按 `../../video-gen-script/references/generation-workflow.md` 的字段只修改对应剧本、资产、镜头或生成参数，不重写整条链路。

## CLI 使用边界

- 项目库默认在 `_work/video_projects/`，该目录被 Git 忽略。
- `project` 记录原始意图、标题、平台、画幅、时长。
- `asset` 记录角色图和场景图；本地文件会复制到项目目录，`asset.json` 保存名称、用途、描述、角色、标签、别名、来源、存储路径和 hash。
- `asset search` 支持跨项目按类型、关键词、标签、角色和来源类型检索；`asset list` 是项目内筛选；`asset show` 查看单个资产详情。
- `asset reuse` 把既有角色/场景资产登记到当前项目，保存 `reused_from`，用于跨项目长期复用和回溯。
- `script` 和 `style` 分别保存剧本和风格规则。
- `storyboard plan` 只生成本地规划脚手架，不调用图片模型。
- `storyboard add` 登记已生成或用户提供的故事板图片、故事板提示词和视频提示词。
- `storyboard approve` 是生成前的确认门。
- `generate --project --storyboard` 默认把故事板图片作为第一张 `omni` 参考图，并把 `video-prompt.txt` 作为提交 prompt；复杂任务还必须通过额外 `--reference-image` 追加对应角色卡和场景/背景卡。
- `history list/show` 查询项目生成记录。

图片生成不属于 CLI 边界。人物设定图、场景设定图和故事板母图由 Skill 根据 `../../video-gen-assets/references/assets.md` 选择必要子文件写提示词，并交给当前环境可用的图像生成工具或其他 image Skill；生成后的图片再用 `asset add` / `storyboard add` 登记。九宫格、四栏、8 镜头或制作设定板只是故事板母图的可选版式，不作为固定模板。

如果故事板像影视分镜信息图一样包含大量 CUT、时间码、对白、场景布局、灯光、声音和色板，可以直接用高能力图像模型生成完整 4K 故事板母图；提示词要写清文字内容、栏目结构、字号层级、读图顺序和画面对应关系。需要确定性可编辑文字、指定字体/品牌版式、超密集 CUT 表或程序化复盘时，采用脚本拼版路线：外部图像工具生成原子图片，确定性脚本绘制文字和版式，最终输出一张 4K 故事板母图再登记，并保留 `storyboard-prompt.txt` 和 composition manifest 供回溯。

## 汇报要求

最终回复除 `../../video-gen-pro/references/completion.md` 的常规字段外，还要包含：

- 项目：`project_id`、项目标题。
- 故事板：`storyboard_id`、是否已 approved。
- 输入：故事板图片、`storyboard-prompt.txt`、`video-prompt.txt`。
- 配套参考图：角色卡、场景/背景卡、道具/产品卡及其编号用途。
- 多段项目：段落编号、上一段结束状态、本段起始状态、镜头边界和承接方式。
- 历史：`generation-record.json` 或 `history show` 可查的 run id。

不要把私有素材、故事板图片或输出视频建议提交到 Git。
