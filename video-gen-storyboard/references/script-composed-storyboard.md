# Script-Composed Storyboard Board

> Load when: 需要像影视分镜信息图一样，先生成多张 CUT 图、场景图、俯视调度图或细节图，再用确定性脚本拼成一张 4K 故事板母图供用户确认和 Seedance 读取。
> Avoid: 只需要一张轻量故事板图，或外部图像工具已经能稳定生成清晰可读的完整故事板母图。
> Pairs with: `storyboard-board.md` 定义故事板母图理念；`grid-storyboard.md` / `four-column-storyboard.md` 提供版式参考；`../../video-gen-assets/references/seedance-handoff.md` 负责登记、确认和视频提示词。

脚本拼版故事板不是新概念，而是故事板母图的一种生产方式。高能力图像模型可以直接生成包含中文文字、表格和复杂版式的完整 4K 故事板母图；脚本拼版用于需要确定性可编辑文字、指定字体/品牌版式、超密集 CUT 表或程序化复盘的场景。它把“图像生成”与“版式排版”拆开：先生成角色、场景、CUT 关键画面和俯视调度等原子图片，再用脚本把文字、时间码、对白、镜头说明、声音和色彩信息排进同一张 4K 信息图。

这条路线适合用户给出的示例：左侧或中央是 CUT 列表和分镜画面，右侧是场景俯视图，底部是光影、色板、风格和声音说明。关键优势是文字、时间码、对白、镜头说明和版式可以确定性修改、复用和回溯。

## When To Use

Use when:

- 故事板信息密度高，并且需要后续精确编辑 CUT 编号、时间码、对白、镜头类型、声音、灯光和场景布局。
- 用户需要在可回溯的版式清单里确认剧本拆分、每段时长、每个镜头的内容，再生成视频。
- 角色/场景一致性重要，且需要多个局部图共同说明。
- 需要指定字体、品牌版式、可复制文本层、超密集 CUT 表或程序化修改记录。
- 一个项目拆成多个视频段，每段都需要独立故事板和统一样式。

Avoid when:

- 只有一个简单镜头，直接生成 4-6 格故事板即可。
- 用户明确要快速抽样，不需要确认信息图。
- 没有足够设定图或 CUT 图，脚本拼版只会把空信息排得更整齐。

## Route

```text
用户想法
-> 生成或确认剧本
-> 判断内容复杂度、总时长和每轮输入负载，决定单段或多个 4-15 秒生成轮次
-> 按目标总时长拆分为 SD01 / SD02 / ...
-> 先按剧情节拍和镜头边界拆段，避免同一镜头跨两次生成
-> 每段按 Seedance 单次 4-15 秒限制拆成 CUT / beat
-> 为每段绑定已确认的角色卡和场景卡；缺失时先生成或登记
-> 每个 CUT 参考对应角色卡、场景卡生成关键画面、俯视调度图或细节图
-> 用脚本把图片、真实文本、时间码、对白、声音、灯光和色板拼成 4K 故事板母图
-> 用户确认故事板母图和简短 video-prompt.txt
-> storyboard add / approve
-> generate --project --storyboard，并追加角色卡、场景/背景卡和必要道具/产品卡
```

这里的“脚本”是确定性排版工具，可以是 Python/Pillow、HTML/CSS 截图、Canvas、Figma 自动化或其他本地工具。它不属于 `videogen` CLI 的 API 调用层；CLI 只登记最终故事板图片、`storyboard-prompt.txt`、`video-prompt.txt` 和确认记录。

## Script And Duration Split

先把剧本拆成可执行视频段。Seedance 单次生成通常按 4-15 秒规划；长片段不要硬塞进一条任务。

拆分不是机械按秒切片。先看每段需要多少角色、场景、道具、动作和声音信息，再让每个生成轮次的输入负载尽量均衡：本段出现什么，就只提交什么；下一段才出现的角色、场景或道具不要提前塞进本段。若单段内信息过载，优先继续拆段或先补角色/场景/道具卡，而不是把长说明塞进视频 prompt。

```text
Script Plan:
- Project title:
- Total duration:
- Segment count:
- Global character lock:
- Global scene lock:
- Global style lock:
- Global sound strategy:

SD01:
- Duration:
- Story goal:
- Start state:
- End state:
- CUT 1: timecode, character_refs, scene_ref, image goal, action, camera, dialogue, sound
- CUT 2: ...

SD02:
- Duration:
- Start state must match SD01 end:
- End state:
- CUT list:
```

拆分原则：

- 每段只承担一个清楚的剧情目标或动作目标。
- 每段结尾必须有可见 `end_state`，供下一段承接。
- 每段只绑定本段相关角色卡、场景/背景卡、道具/产品卡和声音 brief。
- 每段边界优先落在镜头切换处；不要为了凑时长把同一个镜头拆成两个生成任务。
- 如果同一长镜头因为模型时长上限必须跨段，在段落表里标记为同镜头延续，并进入 `../../video-gen-script/references/multi-segment-continuity.md` 选择 `extend` 或尾帧硬衔接。
- 如果下一段已经换机位、换景别、换空间或换动作阶段，标记剧情连续即可，不要强制首帧接上一段尾帧。
- 每个 CUT 只写一个镜头任务，不把多个动作挤进一个格子。
- 每个 CUT 必须写清引用的角色卡和场景卡；换角色、换场景或换服装时，先新增或更新卡片。
- 时长写到段级即可；CUT 时间码用于节奏参考，不承诺模型逐帧精确执行。

## Atomic Images

原子图片先服务信息准确，不要求每张都像成片海报。

| Image Type | Purpose |
| ---------- | ------- |
| Character sheet | 锁定角色身份、服装、配饰、脸部识别点 |
| Scene sheet | 锁定空间结构、光源方向、关键道具和色彩 |
| Scene layout | 俯视图、站位、人物移动、镜头运动轨迹 |
| CUT frame | 参考对应角色卡和场景卡，生成每个镜头的关键画面、景别、动作和情绪 |
| Detail frame | 道具、手部、表情、产品或关键线索 |
| Mood / lighting strip | 光影、色彩、质感和氛围统一 |

原子图片专注角色、场景、动作、景别和情绪。CUT 编号、时间码、对白和镜头说明由脚本绘制到最终故事板上。

## Per-CUT Card Binding

脚本拼版路线里，角色卡和场景卡是每张原子图的一致性锚点，不只是最终故事板里的展示素材。

每个 CUT 图像提示词都应包含：

```text
参考角色卡：<character_card_id/name/path>，保持脸部、发型、服装、配饰、体态和道具一致。
参考场景卡：<scene_card_id/name/path>，保持空间结构、光线方向、关键道具、材质和环境氛围一致。
CUT 目标：<本 CUT 的动作、景别、构图、情绪和结束状态>。
禁止：不要改变角色身份、不要换服装、不要改场景结构、不要新增未登记角色或道具。
```

如果一个 CUT 同时出现多个角色，逐个列出角色卡；如果从 A 场景切到 B 场景，CUT 清单里必须把 `scene_ref` 改成 B 场景卡。最终拼版图可以把这些卡放在角色/场景区域，也可以只在清单里显示引用，但 `storyboard-prompt.txt` 和 composition manifest 必须能回溯到每个 CUT 用了哪张卡。

## Composition Manifest

脚本拼版前，先生成一个排版清单。它是 `storyboard-prompt.txt` 的一部分，也可以单独保存为 `composition-manifest.json` 或 `storyboard-layout.md`。

```text
Storyboard Composition Manifest:
- Output: 3840x2160 or higher
- Layout: custom production board / two-page spread / vertical cut list / project board
- Title bar:
- Columns / zones:
- Image slots:
  - cut_01: path, crop mode, label, timecode
    character_refs: [character_card_hero, character_card_support]
    scene_ref: scene_card_living_room
  - cut_02: path, crop mode, label, timecode
    character_refs: [...]
    scene_ref: ...
  - scene_layout_01: path, label
- Text blocks:
  - cut_01_note: subject, action, camera, dialogue, sound
  - lighting_mood:
  - color_palette:
- Reading order:
- Motion-driving zone:
- Constraint-only zones:
- Fonts and colors:
```

脚本输出的最终图片才是 `storyboard-image.*`。不要把一堆散图直接当故事板提交给 Seedance。

## Layout Rules

- 输出必须 4K 或更高；横向信息图默认 3840x2160，超宽拼版可用更高宽度，但文字必须清晰。
- CUT 图保持统一比例，常用 16:9；需要特写或俯视图时允许不同 slot。
- 所有中文文字、CUT 编号、时间码、对白和镜头说明由脚本绘制，便于确定性编辑、复用和回溯。
- 每个 CUT 块至少包含：CUT 编号、时间范围、主体、动作、镜头、简短对白/字幕、声音或情绪。
- 场景布局图只说明空间和调度，不替代 CUT 画面。
- 底部或侧边可放灯光、色板、声音、风格规则；这些是约束区，不新增剧情。
- 版面可以像制作设定板、双页分镜、CUT 列表或项目总览；不要强制四栏或九宫格。

## Video Prompt Rule

脚本拼版故事板的信息已经很完整，`video-prompt.txt` 要更短：

```text
参考图1是 @脚本拼版故事板，用于决定 <SDxx> 的 <duration> 秒 <ratio> 视频镜头顺序、动作节奏和调度。
参考图2..N 是本段角色卡、场景/背景卡和必要道具/产品卡，用于锁定人物、空间、背景层次和关键道具细节。

读图规则：
- CUT 区按编号和时间码决定镜头顺序、动作连续性和情绪推进。
- 角色卡参考图优先锁定人物外观，不让故事板里的简化人物覆盖角色卡。
- 场景/背景卡参考图优先锁定空间结构、站位、人物移动、镜头运动和关键道具，不让故事板里的简化背景覆盖场景卡。
- 灯光、声音、色彩和风格区只统一氛围，不新增剧情。

按 CUT 1 到 CUT N 连接成连续视频，保持角色卡中的人物服装一致，保持场景/背景卡中的空间、光线、道具和色彩一致。
不要把说明区当成新故事，不要新增故事板之外的角色、场景、对白或结局。
```

如果本段包含爆炸、烟雾、粒子或魔法效果，只补一两句关键动态；不要把完整排版清单复制到视频 prompt。

## Confirmation Gate

生成视频前向用户确认：

```text
脚本拼版故事板确认：
- 剧本是否已按总时长拆成段落：
- 本段时长：
- 本段边界是否是镜头切换，还是同一长镜头跨段：
- CUT 数量和时间码：
- 角色/场景设定图是否复用：
- 每个 CUT 是否绑定了对应角色卡和场景卡：
- 原子图片是否都已确认：
- 最终故事板图片是否 4K 清晰可读：
- Seedance 提交时会同时输入哪些角色卡、场景/背景卡和道具/产品卡：
- CUT 顺序是否正确：
- 对白、声音、镜头说明是否准确：
- video-prompt.txt 是否只保留读图规则：
- 是否真实调用 Seedance：
```

如果用户改剧本、时长或 CUT 顺序，只回到脚本拆分和拼版清单，不要重新生成所有角色/场景图。只有 CUT 画面本身错了，才回到对应 CUT 图。

## Registration

确认后进入 `../../video-gen-assets/references/seedance-handoff.md`：

```bash
videogen storyboard add <project-id> --storyboard-id <storyboard-id> --image <composed-storyboard.png> --prompt <storyboard-prompt.txt> --video-prompt <video-prompt.txt>
videogen storyboard approve <project-id> <storyboard-id>
videogen generate --project <project-id> --storyboard <storyboard-id> --duration <seconds> --reference-image <character-card.png> --reference-image <scene-background-card.png> --wait
```

`storyboard-prompt.txt` 应包含：剧本拆分、原子图片提示词摘要、composition manifest、最终拼版规则和视频读图策略。这样后续能判断问题来自剧本、原子图、拼版，还是 Seedance 读图。

## Common Failures

| Symptom | Fix |
| ------- | --- |
| 用户要求可编辑文字层或固定字体 | 使用脚本拼版，把文字和版式交给确定性排版步骤 |
| 故事板像散图拼贴 | 在 composition manifest 里明确读图顺序、区域主次和统一色板 |
| 视频只读到单张 CUT | `video-prompt.txt` 明确 CUT 区决定镜头顺序，其他区只做约束 |
| 第二段不连续 | 回到 `../../video-gen-script/references/multi-segment-continuity.md`，写上一段 `end_state` 并选择正确 `continuity_mode`；只有硬衔接才用尾帧 |
| 用户改时长导致全乱 | 先重拆 SD/CUT，再只重排受影响的 CUT 和时间码 |
