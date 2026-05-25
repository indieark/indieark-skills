# Visual Asset Generation Reference

> Load when: 复杂视频任务需要先规划或生成角色设定图、场景设定图、故事板母图，再交给 Seedance 生成视频。
> Avoid: 用户只要静态图成品、只问 Seedance API 参数、只做一次快速视频抽样，或已经有可用视觉资产且只需登记。
> Pairs with: `visual-storyboard.md` 管项目库和确认门；`director.md` 写视频 prompt；`completion.md` 汇报素材和证据。

本文件是视觉资产方法的运行时入口，只负责路由。不要把所有理论一次性加载；先判断需要哪类资产，再读取对应子文件。

进入本文件前，复杂任务应已通过 `visual-storyboard.md` 的生成前检索门，确认没有可直接复用的项目、角色图、场景图或故事板；否则先复用或让用户确认候选，不要直接生成新资产。

故事板母图的完整理念、首版 4K 规格、禁止低清预览确认门、文本规则、适用边界和视频读图规则以 `visual-assets/storyboard-board.md` 为准。本文件只保留路由摘要：故事板是按需组织的视频主参考信息图，九宫格、四栏、8 镜头和制作设定板只是版式实例；故事板适合清楚可规划且需要一致性的场景，粒子、爆炸、烟雾、混乱群体或强抽象动态优先 prompt-heavy 或混合路径。故事板主控镜头顺序和运动，不单独承担人物、背景和道具细节锁定；复杂任务提交视频时必须同时输入对应角色卡和场景/背景卡。

## Hard Boundary

- 图片生成不属于 `seedance2` CLI。CLI 只登记外部工具或用户提供的图片，并把它们用于后续视频生成。
- Skill 可以写图像生成提示词，并调用当前环境可用的图像生成工具或其他 image Skill。
- 不把图片 provider、模型名、鉴权或参数硬编码进 Seedance CLI。
- 用户只要静态图最终交付时，应交给图片生成 Skill；本 Skill 只在“图片服务于后续视频生成”时规划这些图。

## Loading Order

1. 先读本文件判断路径。
2. 需要查看子方法目录时，读 `visual-assets/README.md`，不要直接批量加载全部子文件。
3. 需要完整链路或不确定资产顺序时，读 `visual-assets/principles.md`。
4. 需要把一句想法拆成角色、场景、风格和视频段落时，读 `visual-assets/setting-director.md`。
5. 需要判断单段还是多段时，先读 `visual-assets/multi-segment-continuity.md` 的 Intelligent Orchestration Gate，再读 Automatic Split Route；先确认 15 秒只是单次生成上限，再按场景变化、角色负载、动作变化、镜头变化、道具状态和声音文字负载决定单段或多段。
6. 需要生成任何故事板图时，先读 `visual-assets/storyboard-board.md` 理解故事板母图理念和角色卡/场景卡锚定规则，再按需要读 `grid-storyboard.md` 或 `four-column-storyboard.md` 作为版式参考。
7. 需要先生成多张 CUT / 场景 / 调度原子图，再脚本拼成信息密集故事板海报时，读 `visual-assets/script-composed-storyboard.md`。
8. 任务拆成多个视频段并要求连续时，继续读 `visual-assets/multi-segment-continuity.md` 完整台账和 handoff 规则。
9. 只生成某一类图片时，只读对应文件。
10. 生成视频前，读 `visual-assets/seedance-handoff.md` 把图片资产转成 Seedance prompt 和项目登记动作。

## Asset Route

| Need | Read | Output | Register |
| ---- | ---- | ------ | -------- |
| 查看二级方法索引 | `visual-assets/README.md` | 子文件选择表 | N/A |
| 判断整体链路、避免直接抽卡 | `visual-assets/principles.md` | 资产顺序和确认点 | N/A |
| 从一句想法生成完整设定方案 | `visual-assets/setting-director.md` | 角色/场景/风格/段落规划 | `project` / `script` / `style` |
| 固定人物身份和连续性 | `visual-assets/character-sheet.md` | 角色卡提示词；正式角色卡只能用人设三视图或多视图模板 | `asset add --type character` |
| 固定空间、光线和道具 | `visual-assets/scene-sheet.md` | 先做场景卡路由判断，再按需选择基本场景卡、正交四视图或本次剧情多视角联合图，并写清场景 DNA | `asset add --type scene` |
| 生成视频主运动参考图 | `visual-assets/storyboard-board.md` | 自适应故事板母图提示词、配套角色/场景卡输入规则和读图规则 | `storyboard add` |
| 多张 CUT / 场景 / 调度图脚本拼版 | `visual-assets/script-composed-storyboard.md` | 剧本拆段、原子图片清单、composition manifest 和 4K 故事板海报 | `storyboard add` |
| 单段 4-15 秒镜头顺序 | `visual-assets/grid-storyboard.md` | 镜头网格版式提示词，可用九宫格或自定义格数 | `storyboard add` |
| 短剧/广告/系列项目总览 | `visual-assets/four-column-storyboard.md` | 项目级版式提示词，可用四栏、制作设定板或自定义栏目 | `storyboard add` |
| 智能编排与多段连续性 | `visual-assets/multi-segment-continuity.md` | 智能编排判断、连续性台账、镜头边界、`continuity_mode` 和按需尾帧/首尾帧/延长方案 | `storyboard add` / `history show` |
| 把图片资产交给 Seedance | `visual-assets/seedance-handoff.md` | `video-prompt.txt` 和登记步骤 | `storyboard approve` / `generate` |

## Default Path

复杂任务默认路径：

```text
用户想法
-> visual-storyboard.md 执行 project list / asset search / asset show 检索门
-> setting-director.md 产出设定资产规划
-> multi-segment-continuity.md 先做 Intelligent Orchestration Gate：判断 15 秒是否只是上限、单段是否可行、是否需要多个更短故事板和生成轮次
-> character-sheet.md / scene-sheet.md 生成或补齐设定图
-> 如果是多段视频，multi-segment-continuity.md 写连续性台账
-> storyboard-board.md 确认每个分镜/CUT 绑定对应角色卡和场景卡
-> storyboard-board.md 决定故事板母图的信息密度和版式
-> 如果需要真实文字、CUT 表、场景布局和多张原子图，script-composed-storyboard.md 规划脚本拼版
-> 必要时参考 grid-storyboard.md 或 four-column-storyboard.md 生成具体故事板图
-> seedance-handoff.md 写视频提示词并登记
-> visual-storyboard.md 展示 4K 故事板图、storyboard-prompt 摘要和短 video-prompt，并完成 approve
-> generate --project --storyboard，并追加对应角色卡和场景/背景卡为 `--reference-image`
```

简单任务可以跳过视觉资产，直接回到 `director.md` 和 6 个快速生成命令。

## Per-Asset Confirmation Gates

复杂任务不要把人物图、场景图、故事板图和视频生成一次性静默跑完。除非用户明确授权“按默认方案全自动推进”，否则按下表逐项确认；即使合并确认，故事板图片和最终 `video-prompt.txt` 仍必须单独确认。

| Step | Confirm With User | Do After Approval |
| ---- | ----------------- | ----------------- |
| 1. 设定方案 | 项目目标、画幅、时长、风格、角色清单、场景清单、段落数量 | 写 `script.md` / `style.md`，必要时创建项目 |
| 2. 人物设定图提示词 | 角色名、脸部 DNA、发型、服装、体态、固定识别点、设定图类型；正式角色卡必须选择 three-view 或 multi-view | 调用外部图像工具生成；用 `asset add --type character` 登记 |
| 3. 场景设定图提示词 | 主要场景列表、场景卡路由判断、场景图类型、空间 DNA、角度说明、光线方向、关键道具位置、空间关系、禁止穿帮提醒；单镜头推进/拉远用基本场景卡，严格复用才用正交四视图，某次剧情多镜头角度才用多视角联合图 | 调用外部图像工具生成；用 `asset add --type scene` 登记 |
| 4. 故事板母图提示词 | 信息密度；必须放进图里的信息区；实际镜头数量；每个分镜/CUT 绑定的角色卡和场景卡；哪个区域决定视频运动；读图顺序 | 调用外部图像工具生成；保存 `storyboard-prompt.txt` |
| 5. 脚本拼版清单（按需） | 剧本拆段、CUT 数量、每个原子图引用的角色卡/场景卡、文字区、时间码、对白、声音、色板和读图顺序 | 用确定性脚本合成 4K 故事板；保存 composition manifest |
| 6. 视频提示词 | 故事板母图作为主运动参考图；角色卡锁人物；场景/背景卡锁空间和道具；各参考图编号用途、声音 brief、参数和禁止项 | `storyboard add`、展示给用户、`storyboard approve` 后再 `generate` |

第 4 步生成的故事板母图必须首版正式图即 4K 或更高规格；可包含详细文字、表格、镜头说明、对白、灯光、声音和情绪节奏。低清草稿不能登记、确认或提交 Seedance。第 5 步的 `video-prompt.txt` 反而应该短，只写读图规则、运动目标、区域主次和禁止项，不逐字复述故事板绘图提示词。

如果有多个角色或多个场景，逐个资产确认；不要用“角色设定已确认”替代每个角色的可见锚点确认。用户只改某一项时，只回到对应资产，不重做整条链路。

## Selection Rules

- 任何需要故事板图的任务：先把它理解为“视频主运动参考图”，再决定信息密度和版式；人物、背景和道具细节仍由角色卡、场景/背景卡和必要道具/产品卡补齐。
- 单段视频、单个爆点、需要镜头顺序：可用九宫格或更少/更多镜头的故事板版式。
- 短剧项目、广告项目、系列内容、需要用户确认项目视觉总览：可用四栏、制作设定板或自定义故事板版式。
- 像影视分镜信息图、CUT 表或制作设定海报一样需要大量准确文字时：优先脚本拼版，把 CUT 图交给图像工具，把文字和版式交给脚本。
- 画面清楚、动作可拆、镜头顺序重要：优先故事板法。
- 粒子、爆炸、烟尘、魔法能量、混乱战场、纯氛围随机效果：优先 prompt-heavy 或混合路线，不强制故事板。
- 一个项目拆成多个视频生成：先写连续性台账，并在剧本阶段按剧情节拍和镜头边界拆段，尽量不要把同一个镜头拆成两次生成；镜头切换时只承接剧情状态和资产锚点，需要画面硬衔接时才用上一段尾帧；同一长镜头跨段时必须按长镜头延续处理，优先用 `extend` 或尾帧硬衔接。
- 自动拆分不是机械按秒切片：先从用户输入生成剧本，再输出智能编排判断，说明 15 秒是否只是上限、单段是否可行、信息负载来自哪里、是否拆成多个更短故事板和生成轮次；每轮只提交本段相关故事板、角色卡、场景/背景卡、道具/产品卡和声音 brief。
- 场景天然不是九个镜头或四个栏目时，按场景重写提示词：可以减少、合并、扩展镜头，或把栏目换成角色、空间、调度、灯光、声音、色彩等更需要的信息区。
- 角色漂移风险高：先做人设图，不要直接做故事板。
- 场景空间复杂或跨段复用：先做场景设定图。
- 背景、道具或空间细节重要：把场景/背景卡作为视频生成的 `reference_image` 一起提交，不要只依赖故事板里的小背景。
- 多个主要场景：先列 `SCxx_场景名`，再逐个生成场景卡；不要把多个空间混进一条提示词。每个 `SCxx` 都必须先做 `scene-sheet.md` 的场景卡路由判断：镜头角度数、复用强度、空间风险和选择类型。单个场景里只做静止、推进或拉远时，基本场景卡够用；同一主场景需要长期复用时才用正交四视图；某一次剧情场景需要多个镜头角度时才用多视角联合图并裁切或登记子视角资产。不要默认只生成简单场景单图。
- 用户已有好图：不要重生成，先登记并描述用途。

## Done Criteria

进入 Seedance 前，至少能回答：

- 哪张图锁定角色？
- 哪张图锁定场景？
- 角色卡是否使用 `人设三视图提示词` 或 `多视图人设提示词`，而不是单图泛人设？
- 场景卡是否按主要场景逐个生成，并写清场景卡路由判断、场景图类型、场景 DNA、角度、光线、道具和禁止穿帮？
- 哪张故事板母图给 Seedance 当主运动参考图？
- 哪些角色卡和场景/背景卡会随故事板一起作为 `reference_image` 输入？
- 每个分镜或 CUT 分别绑定哪些角色卡和场景卡？
- 故事板母图是否首版正式图即 4K 或更高，图内文字和表格是否清晰可读？
- 故事板母图中哪个区域决定视频运动，哪些区域只做角色/场景/风格约束？
- `storyboard-prompt.txt` 是否保存完整绘图提示词？
- 如果采用脚本拼版，原子图片清单和 composition manifest 是否保存，并且最终 4K 故事板上的文字是否由脚本准确绘制？
- `video-prompt.txt` 是否简短说明如何读取这张母图和各区域主次，而不是复述整张图？
- 如果是多段视频，下一段是否写清上一段 `end_state`、本段 `start_state`、`continuity_mode` 和承接素材？
- 如果是自动拆分项目，是否已经输出智能编排判断：15 秒是否只是上限、单段是否可行、每段时长、拆段原因、每个生成轮次的剧情目标和参考图清单，以及是否避免无关信息输入过载？
- 用户是否确认故事板图片和视频提示词？
