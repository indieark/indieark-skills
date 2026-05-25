# Generation Workflow Reference

> Load when: 用户要生成视频、了解生成流程、进入复杂项目化任务，或需要在每一步确认素材、方法、进度和下一步。
> Avoid: 只查询已有 task 状态、只问 API 参数、只做传统剪辑/转码，或用户明确要求快速一次性抽样且风险低。
> Pairs with: `interaction.md` 做问询门；`visual-storyboard.md` 管项目库和视觉故事板；`visual-assets.md` 管角色/场景/故事板图；`director.md` 写 prompt；`completion.md` 汇报结果。

本文件是“从自然语言创意到可复盘视频生成”的端到端用户流程协议。它不替代各子方法；它规定每一步如何提示用户、展示进度、请求确认、接收修改意见和进入下一步。

核心原则：每一步前都要说明“已完成多少、下一步是什么、需要哪些素材、即将使用什么方法、确认后会产生什么文件或调用什么工具”。复杂任务没有用户确认，不直接批量生成资产或提交视频 API。

## Anti-Bypass Director Contract

<!-- contract: director-process-required natural-language-to-shot-breakdown scene-card-before-storyboard no-direct-prompt-bypass -->

复杂生成任务不能从一句自然语言创意直接跳到最终视频 prompt、图片生成或 Seedance API。除非用户明确说“快速抽样 / 先绕过导演流程出一版 / 不做项目化资产”，否则必须先完成以下导演检查：

- 自然语言转剧本：先输出 2-3 个剧本候选；用户已有明确剧本时，也要整理为选定剧本和规模估算。
- 剧本转镜头：把选定剧本拆成镜头清单，每个镜头至少有 `shot_id`、时长、画面目的、景别、运镜、动作、声音和文字轨道。
- 镜头转资产：从镜头清单反推角色卡、场景卡、道具/产品卡需求，形成 `shot_id -> character_refs / scene_ref / prop_refs` 依赖表。
- 场景卡门：每个非抽象镜头必须有 `scene_ref`。若没有可复用场景卡，先生成或登记场景卡；不能只靠最终视频 prompt 里的场景描述替代场景资产。
- 故事板门：进入故事板图片生成前，必须已有镜头清单和场景引用；缺少 `scene_ref` 时回到资产规划，不继续生成故事板。

允许快速路径的条件只有一个：用户明确要求低成本快速抽样或绕过项目化流程。此时仍要给一个简短导演拆分，完成回复必须说明“本次是快速路径，未生成/登记完整角色卡、场景卡或故事板资产”。

## Progress Contract

每次进入或继续复杂生成任务时，先给用户一条进度提醒：

```text
流程进度：
- 当前阶段：<创意整理 / 剧本候选 / 资产规划 / 角色场景图 / 故事板 / 生成前确认 / API 生成 / 结果复盘>
- 已完成：<已确认的输入、资产、剧本、故事板或任务>
- 下一步：<即将做什么>
- 需要你确认：<确认项或可修改项>
- 继续后会使用：<方法 reference / 外部图像工具 / seedance2 CLI 子命令>
```

如果用户只要功能介绍或使用向导，不进入执行，只解释这条流程和触发边界。

## Stage 1: Idea To Script Candidates

先把自然语言创意整理成 2-3 个剧本候选，不直接写最终 prompt。

必须给出：

- 候选标题和一句话梗概。
- 预计总时长。
- 预计镜头数量。
- 需要的角色数量。
- 需要的主要场景数量。
- 需要的关键道具 / 产品 / 文字 / 声音元素。
- 推荐路线：快速 prompt-heavy、角色卡 + 场景卡、故事板母图、多段生成。
- 智能编排判断：15 秒是否只是上限，单段是否可行，是否需要拆成多个故事板和视频段。
- 导演拆分摘要：每个候选的关键镜头节拍、场景变化和需要生成的场景卡。

确认格式：

```text
剧本候选确认：
1. <候选 A>：<时长>，<镜头数>，<角色>，<场景>，<道具>，<路线>
2. <候选 B>：...
3. <候选 C>：...

请确认选哪版，或指出要合并/删改的点。确认后我会进入资产规划。
```

用户选定或修改后，保存/登记剧本，再进入资产规划。

## Stage 2: Asset Plan Confirmation

在生成任何图片资产前，先汇总将要生成或复用的资产：

```text
资产规划确认：
- 角色卡：<数量> 张，分别是 <CH01...>
- 场景卡：<数量> 张，分别是 <SC01...>
- 道具/产品卡：<数量> 张，分别是 <PROP01...>
- 故事板：<单段 / 多段>，预计 <数量> 张母图
- 智能编排判断：<总时长、推荐生成轮次、每段时长、每段故事目标、信息负载、单段/多段原因>
- 复用资产：<从 project/asset search 找到的候选；确认后用 asset reuse 登记到当前项目，或一次性引用素材路径/source>
- 新生成资产：<需要外部图像工具生成的清单>
- 本步方法：<character-sheet / scene-sheet / storyboard-board / script-composed-storyboard>
- 镜头资产依赖：<shot_id -> character_refs / scene_ref / prop_refs>
- 场景卡路由判断：<每个 SCxx 的镜头角度数、复用强度、空间风险、选择类型；不要默认简单单图>
```

若 `asset search` 命中既有角色卡或场景卡，必须先展示候选来源和用途，并让用户确认复用、新生成或另选。跨项目长期复用默认用 `asset reuse` 复制/登记到当前项目并保留 `reused_from`；只有快速抽样才允许直接引用旧项目素材路径。

如果需要批量生成角色卡和场景卡，必须先展示每张图的提示词摘要，至少包括角色 DNA、场景 DNA、画风、画面限定和禁止项。用户确认后再批量调用外部图像工具。

如果资产规划显示任意非抽象镜头缺少 `scene_ref`，先生成或登记场景卡，不进入故事板图片生成或视频 prompt 编写。生成场景卡前必须读取 `scene-sheet.md` 的 `Scene Card Routing Contract`：每个主要场景都要先判断镜头角度数、复用强度和空间风险，再选择基本场景卡、正交四视图或多视角联合图；不能默认只生成简单场景单图。

批量生成前的确认字段：

```text
批量图片生成确认：
- CH01 提示词摘要：
- CH02 提示词摘要：
- SC01 提示词摘要：
- SC02 提示词摘要：
- 批量方式：<逐张生成 / 并行生成>
- 故事板规格：首版正式故事板即 4K 或更高；不设置低清预览确认门，低清草稿不得登记或提交 Seedance。
- 生成后动作：登记到项目库，并进入故事板设计。
```

## Stage 3: Storyboard Edit Contract

生成故事板前，必须为每个镜头写结构化提示词，让用户能逐镜头修改，而不是一次性塞进图片工具。

每个镜头至少包含：

- shot_id / 分镜序号。
- 时长。
- 角色引用：`character_refs`。
- 场景引用：`scene_ref`。
- 景别：WS / FS / MS / CS / CU / ECU。
- 机位和运镜。
- 人物动作、站位和情绪。
- 画面重点和道具。
- 声音 brief：音乐、环境音、动作音效、对白/无对白。
- 文字轨道：字幕、标题文字、无随机字母/水印。
- 可编辑项：可让用户改景别、角色、场景、镜头顺序、动作、声音、文字。

镜头清单中任何一项缺 `scene_ref`、`character_refs` 或必要道具引用时，先退回 Stage 2 补齐资产计划；不要把缺失信息隐藏进最终 prompt。

用户修改方式可以是自然语言，也可以是程序化数据。默认回复必须使用标准文本块 + 结构化 JSON；不要启动 HTML 交互，也不要把修改意见只写成自由文本。

推荐修改数据结构：

```json
{
  "workflow_stage": "storyboard_edit",
  "reorder": ["shot_02", "shot_01", "shot_03"],
  "edits": [
    {
      "shot_id": "shot_02",
      "field": "shot_size",
      "value": "CU",
      "note": "改成角色手部特写"
    },
    {
      "shot_id": "shot_03",
      "field": "character_refs",
      "value": ["CH01", "CH02"],
      "note": "增加第二个说话人"
    }
  ],
  "approval": "revise"
}
```

Agent 收到结构化修改意见后，只修改对应镜头，不重写整套剧本和资产。

## Stage 4: Standard Reply And JSON Contract

标准回复流程恢复为 HTML 之前的格式：对话文本负责让用户看懂当前状态和下一步，结构化 JSON 负责让 Agent 精确接收确认或修改意见。不得把生成前确认、结果复盘或修改意见包装成 HTML 页面。

## Final Input Lock Contract

<!-- contract: final-input-lock audio-text-lock no-unneeded-generation-inputs storyboard-does-not-replace-final-prompt output-spec-lock -->

提交 Seedance 前必须锁定最终输入。故事板只控制镜头内容、动作节奏和调度，不替代声音、字幕/画面文字、生成参数、参考素材用途或最终 `video-prompt.txt`。

最终输入锁定必须包含：

- 输出规格：画幅、清晰度/分辨率、预计时长、模型和是否等待下载。
- 声音策略：有声 / 无声 / 参考音频驱动；`generate_audio=true|false`；音乐、环境音、动作音效和参考音频用途。
- 说话人声：对白、旁白、口播、喘息/笑声，或明确不要说话人声。
- 字幕和画面文字：对白字幕、旁白字幕、标题文字、品牌字样、UI 文字，或明确不要字幕、标题文字、logo、水印和随机字母。
- 生成输入：本次实际提交的参考图、参考视频、参考音频和 prompt 文件；只提交当前段需要的输入，不把无关角色卡、场景卡、其他段故事板或无用途音频塞进 payload。
- 最终提示词：有故事板时使用短读图 `video-prompt.txt`，但必须写清声音、说话人声、字幕/标题文字、输出规格和参考图主次；没有故事板时使用详细分镜 prompt。

有声不等于有字幕；无声不等于可以省略文字策略。无声视频使用 `--generate-audio false`，并在 prompt 写明不要音乐、对白、旁白或环境音。没有字幕或标题文字时，写明不要字幕、标题文字、logo、水印和随机字母。

每个确认门默认包含两部分：

- 人读文本块：阶段、已完成、待确认、下一步、将使用的方法或 CLI。
- 机器可读 JSON：`workflow_stage`、`approval`、`target_stage`、`requested_changes`、`dimensions` 和必要的项目 / 故事板 / run id。

生成前确认的标准回复格式：

```text
生成前确认：
- 当前阶段：final_input_review
- 已完成：
- 待确认：
- 模型 / 分辨率 / 画幅 / 时长：
- 声音 / 说话人声 / 字幕与画面文字：
- 参考素材：
- 故事板与提示词：
- 输出和证据目录：
- 下一步会执行：

确认后我会调用 CLI；如需修改，请指出要改的字段。
```

对应确认 JSON：

```json
{
  "workflow_stage": "final_input_review",
  "review_gate": "before_video_generation",
  "approval": "approved",
  "target_stage": null,
  "requested_changes": [],
  "selected_project_id": "proj_redhood",
  "selected_storyboard_id": "sb_01",
  "selected_run_id": "run_01",
  "dimensions": {
    "ratio": "9:16",
    "resolution": "720p",
    "duration_seconds": 12,
    "generate_audio": true,
    "sound_strategy": "有声：低频紧张音乐 + 雨声环境音，不要对白",
    "speech_track": "不要说话人声",
    "text_track": "不要字幕、标题文字、logo、水印或随机字母"
  }
}
```

结果复盘的标准回复格式：

```text
结果复盘：
- 当前阶段：result_review
- 视频结果：
- 任务信息：
- 最终输入：
- 使用素材：
- 证据目录：
- 验收结论：
- 下一步选项：
```

对应复盘 JSON：

```json
{
  "workflow_stage": "result_review",
  "review_gate": "after_video_generation",
  "approval": "revise",
  "target_stage": "video_prompt",
  "selected_project_id": "proj_redhood",
  "selected_storyboard_id": "sb_01",
  "selected_run_id": "run_01",
  "requested_changes": [
    {"field": "camera_motion", "value": "slower dolly in"},
    {"field": "dialogue", "value": "remove narration"}
  ]
}
```

Agent 收到确认 JSON 后只修改对应字段。用户只给自然语言修改意见时，Agent 先把它归一化为上述 JSON 语义，再继续执行。

## Stage 5: Final Input Review

提交 Seedance 前必须展示所有输入，不能只说“我将生成视频”。

生成前确认必须包含：

- CLI 子命令：`text-to-video` / `first-frame` / `first-last` / `omni` / `edit` / `extend` / `generate`。
- 模型：`doubao-seedance-2-0-260128` 或 fast。
- 画幅、清晰度/分辨率、预计时长、是否等待下载。
- 声音策略：`generate_audio=true|false`、音乐、环境音、动作音效、参考音频用途；无声时明确 `generate_audio=false`。
- 说话人声策略：对白、旁白、口播或明确不要说话人声。
- 字幕和画面文字策略：字幕、标题文字、品牌字样或明确不要字幕、标题文字、logo、水印和随机字母。
- 参考图 / 参考视频 / 参考音频编号、用途和是否实际提交；无关输入不提交。
- 角色卡、场景/背景卡、道具/产品卡。
- 故事板图片、`storyboard-prompt.txt` 和 `video-prompt.txt`。
- 故事板规格复核：确认首版正式故事板为 4K 或等效 4K，文字清晰可读，且不是低清图简单放大。
- 导演流程复核：自然语言已转成选定剧本、镜头清单、资产依赖表；每个非抽象镜头已有 `scene_ref` 或明确快速路径说明。
- 实际提交 prompt 摘要或全文：有故事板时，短读图 prompt 仍必须写清声音、说话人声、字幕/画面文字、输出规格和参考素材主次；没有故事板时展示详细分镜 prompt。
- 输出目录、run id、是否等待完成、是否下载。

确认格式：

```text
生成前确认：
- 模式：
- 模型 / 分辨率 / 画幅 / 时长：
- 声音 / 说话人声 / 字幕与画面文字：
- 参考素材和实际提交输入：
- 故事板与提示词：
- 输出和证据目录：
- 下一步会执行：

确认后我会调用 CLI；如需修改，请指出要改的字段。
```

## Stage 6: Result Review

生成结果也要结构化复盘。默认使用文本摘要 + 结构化 JSON 字段，不生成 HTML 页面。

结果复盘至少包含：

- 视频结果：本地 MP4 或安全的 `content.video_url` 摘要。
- 任务信息：task_id、模型、模式、状态、时间。
- 输入复盘：最终 prompt、尺寸、分辨率、画幅、时长、声音、参考素材。
- 资产复盘：角色卡、场景卡、道具卡、故事板版本。
- 证据文件：run directory、payload、manifest、generation log、task result、generation record。
- 验收：与用户原始目标是否一致。
- 下一步：认可、下载、重试、只修改 1-3 个点、回到某个阶段。

结果复盘必须输出结构化 JSON，例如：

```json
{
  "workflow_stage": "result_review",
  "review_gate": "after_video_generation",
  "approval": "revise",
  "target_stage": "video_prompt",
  "selected_project_id": "proj_redhood",
  "selected_storyboard_id": "sb_01",
  "selected_run_id": "run_01",
  "requested_changes": [
    {"field": "camera_motion", "value": "slower dolly in"},
    {"field": "dialogue", "value": "remove narration"},
    {"field": "ending", "value": "hold final product shot for 1 second"}
  ]
}
```

结果不满意时，按 `iteration.md` 只做 1-3 处定向修改；不要从自然语言创意阶段全部重来，除非用户明确要求重做。
