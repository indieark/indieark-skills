# Assets 资产族入口

> Load when: 复杂视频任务需要先规划或生成可登记、可跨剧本复用的人物设定图、场景设定图，再交给 Seedance；或需要进入资产链路理念、设定导演流和交接。
> Avoid: 用户只要静态图成品、只问 Seedance API 参数、只做一次快速视频抽样，或已经有可用视觉资产且只需登记。只需要故事板母图和版式时，去方法论 `../../video-gen-storyboard/references/README.md`。
> Pairs with: `README.md` 是资产二级索引；`../../video-gen-storyboard/references/visual-storyboard.md` 管项目库和确认门；`../../video-gen-director/references/director-method.md` 写视频 prompt；`../../video-gen-pro/references/completion.md` 汇报素材和证据。

本文件是**资产**（人物、场景、道具、素材四类图像资产，以及人物附属的声线音频资产，都是可登记可复用的料）的运行时入口，只负责路由。不要把所有理论一次性加载；先判断需要哪类资产，再读取对应子文件。资产维度与形态的概念边界以 `../../video-gen-pro/references/concepts.md` 为准。

进入本文件前，复杂任务应已通过 `../../video-gen-storyboard/references/visual-storyboard.md` 的生成前检索门，确认没有可直接复用的项目、角色图、场景图或故事板；否则先复用或让用户确认候选，不要直接生成新资产。

故事板母图、九宫格/四栏/脚本拼版等版式、智能编排和多段连续性属于**方法论产物**（故事板法），不在本文件，完整规则见 `../../video-gen-storyboard/references/README.md`。资产与故事板法的关系：故事板法主控镜头顺序和运动，但不单独承担人物、背景和道具细节锁定；复杂任务提交视频时必须同时输入对应角色卡和场景/背景卡。

## Hard Boundary

- 图片生成不属于 `videogen` CLI。CLI 只登记外部工具或用户提供的图片，并把它们用于后续视频生成。
- Skill 可以写图像生成提示词，并调用当前环境可用的图像生成工具或其他 image Skill。
- 不把图片 provider、模型名、鉴权或参数硬编码进 Seedance CLI。
- 用户只要静态图最终交付时，应交给图片生成 Skill；本 Skill 只在“图片服务于后续视频生成”时规划这些图。

## Loading Order

1. 先读本文件判断路径。
2. 需要查看资产二级索引时，读 `README.md`，不要直接批量加载全部子文件。
3. 需要完整链路或不确定资产顺序时，读 `principles.md`。
4. 需要把一句想法拆成角色、场景、风格和视频段落时，读 `setting-director.md`。
5. 需要固定人物身份时，读 `character-sheet.md`（角色音色另见其声线小节）；需要固定空间、光线和场景陈设时，读 `scene-sheet.md`；需要固定反复出镜的关键道具或产品时，读 `prop-sheet.md`；需要可复用的 logo/纹理/角标/转场等通用素材时，读 `graphic-sheet.md`。
6. 需要故事板母图、版式或智能编排判断时，转到方法论 `../../video-gen-storyboard/references/README.md`。
7. 生成视频前，读 `seedance-handoff.md` 把图片资产转成 Seedance prompt 和项目登记动作。

## Asset Route

| Need | Read | Output | Register |
| ---- | ---- | ------ | -------- |
| 查看资产二级索引 | `README.md` | 子文件选择表 | N/A |
| 判断整体链路、避免直接抽卡 | `principles.md` | 资产顺序、reference 纯净度和确认点 | N/A |
| 从一句想法生成完整设定方案 | `setting-director.md` | 角色/场景/风格/段落规划 | `project` / `script` / `style` |
| 固定人物身份和连续性 | `character-sheet.md` | 角色卡提示词；正式角色卡只能用人设三视图或多视图模板 | `asset add --type character` |
| 固定角色音色 | `character-sheet.md`（声线小节） | 声线音频样本，omni `reference_audio` 锁音色 | `asset add --type voice --role <角色名>` |
| 固定空间、光线和场景陈设 | `scene-sheet.md` | 先做场景卡路由判断，再按需选择基本场景卡、正交四视图或本次剧情多视角联合图，并写清场景 DNA | `asset add --type scene` |
| 固定反复出镜的关键道具/产品 | `prop-sheet.md` | 道具卡提示词；纯净底单图 / 主图+拆解 / 多视图道具卡，纯图像零文字 | `asset add --type prop` |
| 登记可复用的 logo/纹理/角标/转场等素材 | `graphic-sheet.md` | 素材方法；轴=复用范围，参考图输入或后期叠加 | `asset add --type graphic` |
| 故事板母图、版式、多段连续性 | `../../video-gen-storyboard/references/README.md` | 故事板法母图、版式、智能编排判断和读图规则 | `storyboard add` |
| 把图片资产交给 Seedance | `seedance-handoff.md` | `video-prompt.txt` 和登记步骤 | `storyboard approve` / `generate` |

## Default Path

下面是**故事板分支**（用户需要严格画面一致性，决定出 4K 故事板母图）的默认路径：

```text
用户想法
-> ../../video-gen-storyboard/references/visual-storyboard.md 执行 project list / asset search / asset show 检索门
-> setting-director.md 产出设定资产规划
-> ../../video-gen-script/references/multi-segment-continuity.md 先做 Intelligent Orchestration Gate：判断 15 秒是否只是上限、单段是否可行、是否需要多个更短故事板和生成轮次
-> character-sheet.md / scene-sheet.md 生成或补齐设定图
-> ../../video-gen-storyboard/references/storyboard-board.md 确认每个分镜/CUT 绑定对应角色卡和场景卡，决定信息密度和版式
-> seedance-handoff.md 写视频提示词并登记
-> ../../video-gen-storyboard/references/visual-storyboard.md 展示 4K 故事板图、storyboard-prompt 摘要和短 video-prompt，并完成 approve
-> generate --project --storyboard，并追加对应角色卡和场景/背景卡为 `--reference-image`
```

复杂但**无严格一致性诉求**的任务走**导演法 prompt-heavy 分支**：仍经过检索门和确认门，按需用 `character-sheet.md` / `scene-sheet.md` 生成角色卡/场景卡作为灵活参考，但**不生成故事板母图、不走 storyboard-board / approve**，直接按 `../../video-gen-director/references/director-method.md` 写详细分镜化 `video-prompt.txt` 后生成。

简单任务可以跳过视觉资产，直接回到 `../../video-gen-director/references/director-method.md` 和 6 个快速生成命令。

## Per-Asset Confirmation Gates

复杂任务不要把人物图、场景图、故事板图和视频生成一次性静默跑完。除非用户明确授权“按默认方案全自动推进”，否则按下表逐项确认；即使合并确认，最终 `video-prompt.txt` 仍必须单独确认，走故事板分支时故事板图片也必须单独确认。

| Step | Confirm With User | Do After Approval |
| ---- | ----------------- | ----------------- |
| 1. 设定方案 | 项目目标、画幅、时长、风格、角色清单、场景清单、段落数量 | 写 `script.md` / `style.md`，必要时创建项目 |
| 2. 人物设定图提示词 | 角色名、脸部 DNA、发型、服装、体态、固定识别点、设定图类型；正式角色卡必须选择 three-view 或 multi-view | 调用外部图像工具生成；用 `asset add --type character` 登记 |
| 3. 场景设定图提示词 | 主要场景列表、场景卡路由判断、场景图类型、空间 DNA、角度说明、光线方向、关键道具位置、空间关系、禁止穿帮提醒；单镜头推进/拉远用基本场景卡，严格复用才用正交四视图，某次剧情多镜头角度才用多视角联合图 | 调用外部图像工具生成；用 `asset add --type scene` 登记 |
| 4. 故事板母图提示词 | 见 `../../video-gen-storyboard/references/storyboard-board.md`：信息密度、必须放进图里的信息区、实际镜头数量、每个分镜/CUT 绑定的角色卡和场景卡、哪个区域决定视频运动、读图顺序 | 调用外部图像工具生成；保存 `storyboard-prompt.txt` |
| 5. 视频提示词 | 故事板母图作为主运动参考图；角色卡锁人物；场景/背景卡锁空间和道具；各参考图编号用途、声音 brief、参数和禁止项 | `storyboard add`、展示给用户、`storyboard approve` 后再 `generate` |

如果有多个角色或多个场景，逐个资产确认；不要用“角色设定已确认”替代每个角色的可见锚点确认。用户只改某一项时，只回到对应资产，不重做整条链路。

## Asset Selection Rules

- 角色漂移风险高：先做人设图，不要直接做故事板。
- 场景空间复杂或跨段复用：先做场景设定图。
- 背景、道具或空间细节重要：把场景/背景卡作为视频生成的 `reference_image` 一起提交，不要只依赖故事板里的小背景。
- 多个主要场景：先列 `SCxx_场景名`，再逐个生成场景卡；不要把多个空间混进一条提示词。每个 `SCxx` 都必须先做 `scene-sheet.md` 的场景卡路由判断：镜头角度数、复用强度、空间风险和选择类型。单个场景里只做静止、推进或拉远时，基本场景卡够用；同一主场景需要长期复用时才用正交四视图；某一次剧情场景需要多个镜头角度时才用多视角联合图并裁切或登记子视角资产。不要默认只生成简单场景单图。
- 用户已有好图：不要重生成，先登记并描述用途。
- 角色卡、场景卡直接作为视频模型参考输入，必须纯图像零文字（reference 纯净度），详见 `principles.md`。

## Done Criteria

进入 Seedance 前，资产层至少能回答：

- 哪张图锁定角色？哪张图锁定场景？
- 角色卡是否使用 `人设三视图提示词` 或 `多视图人设提示词`，而不是单图泛人设？
- 场景卡是否按主要场景逐个生成，并写清场景卡路由判断、场景图类型、场景 DNA、角度、光线、道具和禁止穿帮？
- 哪些角色卡和场景/背景卡会随故事板一起作为 `reference_image` 输入？
- 每个分镜或 CUT 分别绑定哪些角色卡和场景卡？

故事板母图规格、读图顺序、脚本拼版和多段连续性的 Done Criteria 见 `../../video-gen-storyboard/references/README.md`。
