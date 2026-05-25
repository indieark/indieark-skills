# Intelligent Routing Reference

> Load when: 需求复杂，需要选择交互策略、输入模式、场景、导演方法、API 操作或验证路径。
> Avoid: 用户已经明确只要某个 reference 的局部规则，例如只问 CLI 或只做一次反馈修正。
> Pairs with: `interaction.md` 先判断是否追问；`scenes.md` 和 `methods/README.md` 承接场景与方法路由。

本文件定义 Seedance 2.0 Skill 内部的智能路由。目标是根据用户需求选择最小足够方案，而不是默认加载所有参考、套所有方法。

## Routing Principles

1. 先读项目/会话规则：宿主仓库的 `AGENTS.md` 或等价文件、当前用户要求。
2. 只加载当前任务需要的 reference，遵守渐进披露。
3. 先分类需求，再选择输入模式、场景、导演方法、API 操作。
4. 优先最轻方案；只有用户需求复杂时才升级。
5. 不确定会影响生成成本或结果时追问；低风险默认可以直接收束。

## Routing Pipeline

```text
用户请求
-> 交互问询门
-> 需求完整度
-> 任务类型
-> 自然语言转剧本 / 镜头拆分门
-> 输入素材角色
-> 项目/资产检索门（复杂任务）
-> 智能编排与拆分门
-> 场景卡门
-> 场景类型
-> 导演方法
-> 视觉资产规划 / 故事板母图选择（按需）
-> 项目资产库 / 视觉故事板确认门
-> 声音设计（有声/参考音频/音效/对白时）
-> API 操作
-> 验证/迭代路径
-> 完成回复
```

## 1. Need Completeness

先读 `interaction.md` 通过交互问询门，决定 `ask / propose options / proceed`。

| Signal                 | Route                                                  |
| ---------------------- | ------------------------------------------------------ |
| 只说“做个视频”         | 先问意图、主体、画幅、时长、声音、素材                 |
| 指定场景但缺少参数     | 保留场景，只问影响结果的 1-3 个缺口                    |
| 素材用途不明           | 先问每个素材是首帧、尾帧、参考图、参考视频还是参考音频 |
| 成本较高且多方向都合理 | 给 2-3 个方向让用户选                                  |
| 信息足够               | 直接进入导演方案和 API payload                         |

Ask 时一次最多问 3 个会影响生成结果的问题。Propose options 时给 2-3 个方向让用户选。Proceed 时说明使用的关键默认值。

## 2. Director Process Gate

复杂生成任务默认进入 `director-process-required`。不要把用户的一句自然语言直接改写成最终 prompt，也不要跳过场景卡生成。

| Signal | Route |
| ------ | ----- |
| 只有自然语言创意 | 先进入 `generation-workflow.md` Stage 1，输出剧本候选和规模估算 |
| 用户已选剧本或给了完整剧情 | 仍要做 `natural-language-to-shot-breakdown`：拆镜头、估时长、列角色/场景/道具 |
| 任意镜头有明确地点、空间、布光或道具关系 | 先过 `scene-card-before-storyboard`，检索或生成场景卡 |
| 任意非抽象镜头缺 `scene_ref` | 回到资产规划，不生成故事板，不写最终视频 prompt |
| 场景卡只想默认出一张单图 | 先读 `scene-sheet.md` 的 `Scene Card Routing Contract`，按镜头角度数、复用强度和空间风险选择类型 |
| 用户明确说快速抽样或绕过项目化流程 | 可以走快速路径，但仍输出简短镜头拆分，并在完成回复说明未登记完整资产 |

## 3. Intelligent Orchestration / Split

智能编排先于具体故事板版式。15 秒是单次生成上限，不是默认目标。核心目标不是机械切段，而是判断单段能否承载当前信息量，让模型每轮只处理本段需要的故事板、角色卡、场景/背景卡、道具/产品卡和声音 brief。

```text
用户输入
-> 生成或整理剧本
-> 从剧本分析需要的角色卡、场景/背景卡、道具/产品卡
-> 形成 shot_id 到 character_refs / scene_ref / prop_refs 的依赖表
-> Intelligent Orchestration Gate：判断 15 秒是否只是上限、单段是否可行、信息负载来自哪里
-> 按场景变化、角色负载、动作变化、镜头变化、道具状态和声音文字负载拆分生成轮次
-> 每轮生成本段故事板，并只提交本段相关参考图
```

| Signal | Route |
| ------ | ----- |
| 单一动作、单场景、总时长 4-15 秒、信息量低 | 一张故事板母图即可；同场景长镜头可以使用 10-15 秒单段；角色一致性重要时追加角色卡 |
| 同一角色连续动作但不复杂 | 简稿故事板 + 角色卡；按需追加场景/背景卡 |
| 多角色、多场景、宣传片、战斗变化、多个产品点、声音文字密集或总时长超过 15 秒 | 先写剧本，再拆成多个 4-15 秒生成轮次；高信息负载的 15 秒内容也可拆成多个 4-6 秒段 |
| 某段需要同时解释新角色、新空间、新道具和复杂运镜 | 继续拆分或先补卡片，不把全部信息堆进 `video-prompt.txt` |
| 镜头切换但剧情连续 | 用 `cut_continuity` 承接剧情状态和资产锚点，不强制尾帧 |
| 同一长镜头超过时长限制 | 标记 `extend` 或 `tail_frame_handoff`，按长镜头延续处理 |

## 4. Task Type

| User Need      | Primary Reference           | Output                                                |
| -------------- | --------------------------- | ----------------------------------------------------- |
| 新生成视频     | `scenes.md` + `director.md` | director prompt + selected-mode payload               |
| 复杂新生成视频 | `visual-storyboard.md`      | project assets + storyboard approval + traceable generation |
| 智能编排或多段连续视频 | `visual-storyboard.md` + `visual-assets.md` | orchestration table + continuity ledger + per-segment storyboards + handoff prompts |
| 清楚可规划的镜头或角色/场景一致性强 | `visual-storyboard.md` + `visual-assets.md` | lookup gate + 4K storyboard-first board + concise read-the-board video prompt |
| 像示例图一样需要 CUT 表、场景图、调度图和大量可读文字 | `visual-storyboard.md` + `visual-assets/script-composed-storyboard.md` | script split + atomic images + composed 4K storyboard poster + concise video prompt |
| 粒子/爆炸/烟雾/抽象动态为主 | `director.md` + optional visual anchors | prompt-heavy or hybrid prompt; no storyboard means detailed per-shot video prompt |
| 按图动起来     | `api.md` + `scenes.md`      | first-frame payload                                   |
| 从首帧到尾帧   | `api.md` + `director.md`    | first/last-frame payload                              |
| 多参考素材综合 | `api.md` + `scenes.md`      | omnireference payload                                 |
| 有声音效/说话人声/字幕/标题文字/参考音频 | `sound-design.md` + `director.md` | audio/text brief + prompt sound section + generate_audio/reference_audio decision |
| 修改/延长视频  | `scenes.md` + `api.md`      | edit/extension-style prompt + reference video payload |
| 结果不满意     | `iteration.md`              | targeted revision                                     |
| 只问怎么用 API | `api.md`                    | explanation or command, no director expansion         |

## 5. Input Mode

| Inputs                            | API Mode                                         |
| --------------------------------- | ------------------------------------------------ |
| prompt only                       | text-to-video                                    |
| one starting image                | first frame                                      |
| starting image + ending image     | first + last frame                               |
| reference images/videos/audio     | omnireference                                    |
| reference video with edit request | video edit / reference-driven generation         |
| existing output and user feedback | iteration; reuse prior task context if available |

Guardrails:

- 不混用首帧/尾帧和全能参考。
- `reference_audio` 不能单独作为唯一非文本输入。
- prompt 必须说明每个参考素材用途；如果使用 `reference_audio`，必须写清它是参考节奏、音色、情绪还是对白。
- `generate_audio=true` 时必须有声音设计；用户要无声或没有声音方案时用 `generate_audio=false`。

## 5. Scene Route

先读 `scenes.md`，选择一个主场景：

- Product / Commercial
- Short Drama / Narrative
- Character Action
- Atmosphere / Mood Film
- Social Short / Viral Hook
- Video Edit / Extension
- Reference-Driven Generation

如果用户指定场景，优先尊重指定场景；不要改成更通用的广告、短剧或电影模板。

## 6. Method Route

先读 `methods/README.md`，再按需加载具体方法。

| Need                                   | Method                                             |
| -------------------------------------- | -------------------------------------------------- |
| 单镜头、限制多、素材/声音/参数都要控住 | `methods/clapperboard.md`                          |
| 多节拍、短剧、广告、产品展示、起承转合 | `methods/storyboard.md`                            |
| 轻量 prompt 或简单动作                 | 不加载方法文件，直接用 `director.md`               |
| 反馈修正                               | `iteration.md`，不要重新选复杂方法，除非原结构错误 |

不要把多个方法完整叠加。可以吸收判断思路，但输出只采用一个主结构。

## 7. Sound Route

有声、无声和参考音频先读 `sound-design.md`，再写入最终 prompt：

| Signal | Route |
| ------ | ----- |
| 用户明确要无声 | `generate_audio=false`，prompt 写明无音乐/对白/环境音 |
| 用户要有声但没说声音 | 按场景补一个简短声音策略；成本较高时问 1 个声音问题 |
| 用户要音效/音乐/对白 | 写 audio brief：音乐、环境音、动作音效、对白、禁止项 |
| 用户要说话人声、旁白、口播或明确不要人声 | 写清 `说话人声`；没有则写不要对白/旁白/口播 |
| 用户要字幕、标题、画面文字或品牌字样 | 写清文字轨道；没有则写不要字幕、标题文字、logo 或水印 |
| 用户提供参考音频 | 进入 omnireference；prompt 写清 `参考音频1` 的用途，且必须配合图/视频参考 |
| 用户要求精确 Foley/混音/配音 | 说明 Seedance prompt 只能表达声音意图，精确后期应走外部音频工作流 |
| 结果声音不好 | 进入 `iteration.md`，只改 1-3 个声音点 |

## 8. API Operation Route

先判断是否需要项目化创作路径。复杂任务在创建新角色、场景或故事板前，先调研当前项目库是否已有可复用资产：

```bash
seedance2 project list
seedance2 asset search --query "<角色/场景/品牌/风格关键词>"
seedance2 asset search --type character --tag "<标签>"
seedance2 asset list <project-id> --query "<关键词>"
seedance2 asset show <project-id> <asset-id>
seedance2 asset reuse <target-project-id> <source-project-id> <asset-id>
```

检索结果的处理规则：

- 找到匹配角色/场景图：先展示候选并请用户确认；长期复用到当前项目时用 `asset reuse` 登记，快速一次性引用时才直接使用 `asset show` 返回的素材路径或 source。
- 找到旧项目或旧故事板：先看 `project show`、`storyboard show`、`history list/show`，判断是否能复用或迭代。
- 没找到匹配资产：再创建项目、登记用户素材，或按 `visual-assets.md` 调用外部图像工具生成后登记。
- 用户明确要求快速抽样并绕过项目库时，可以跳过检索，但完成回复要说明这是快速路径。

| Need | Route |
| ---- | ----- |
| 短剧、广告、系列内容、角色/场景一致性 | 先用 `project list` / `asset search` 检索是否已有项目和角色/场景资产；不足时读 `visual-assets.md` 规划需要的人物/场景/故事板图，再用 `project` / `asset` / `script` / `style` / `storyboard` 登记，确认后用 `generate --project --storyboard` |
| 分多个视频生成且要求连续 | 进入同一 `project_id`，读 `visual-assets/multi-segment-continuity.md` 写连续性台账；先用剧本把剧情节拍和镜头边界拆清楚，不把同一镜头拆成两次生成；每段用独立 `storyboard_id` 和 `video-prompt.txt`；AI 按 `continuity_mode` 判断是剧情连续但切镜头、尾帧硬衔接、`first-last` 桥接，还是同一长镜头 `extend` / 尾帧延续 |
| 用户需要先生成剧本、按规定时长拆段、每段多张分镜图片，再拼成类似影视分镜信息图 | 先用 `script set` 保存剧本；按 `visual-assets/multi-segment-continuity.md` 拆 SD 段；读 `visual-assets/script-composed-storyboard.md` 规划 CUT 原子图和 composition manifest；外部图像工具生成原子图，脚本拼成 4K 故事板后 `storyboard add` / `approve` / `generate` |
| 用户已有故事板图和视频提示词 | 登记 `storyboard add`，再 `storyboard approve`，最后 `generate` |
| 用户明确快速抽样或绕过 | 走现有 6 个创建子命令，但保留 run artifact |

故事板路线只在它能让信息更清楚时使用。若选择故事板路线，故事板母图必须 4K 或更高，可以包含详细文本和表格；`video-prompt.txt` 只写读图规则、运动区域、约束区域、参考图编号用途、短声音 brief、说话人声/字幕策略和禁止项。故事板负责镜头顺序和运动，不单独负责人物、背景和道具细节；复杂任务生成时必须把对应角色卡、场景/背景卡作为额外 `--reference-image` 一起提交，并在 prompt 里说明主次。场景卡不能默认简单单图：单角度低复用才用基本场景卡，多镜头角度用多视角联合图，长期复用用正交四视图。若故事板需要大量准确文字、CUT 表或场景调度说明，优先脚本拼版而不是让图像模型一次生成整张带小字的信息图。若选择 prompt-heavy 路线或没有故事板，不要为了形式强行生成九宫格或四栏；改用 `director.md` 的详细分镜化视频 prompt，逐镜头写清视觉内容、镜头参数、音频轨道、说话人声、字幕/标题文字和转场。

生成类任务不要再走旧的 `create` 总命令；先按输入模式选择 6 个创建子命令之一。图片生成不是 CLI operation；需要视觉资产时由 Skill 调用外部图像生成工具，CLI 只登记生成后的图片。命令细节以 `cli.md` 为准。

| Need             | CLI Command                                                |
| ---------------- | ---------------------------------------------------------- |
| 创建创作项目     | `project create`                                           |
| 检索已有项目     | `project list` / `project show`                            |
| 检索角色/场景资产 | `asset search` / `asset list` / `asset show`               |
| 复用既有角色/场景资产 | `asset reuse <target-project-id> <source-project-id> <asset-id>` |
| 登记角色/场景资产 | `asset add --tag ... --role ... --alias ...`               |
| 保存剧本/风格    | `script set` / `style set`                                 |
| 规划/登记/确认故事板 | `storyboard plan` / `storyboard add` / `storyboard approve` |
| 已确认故事板生成 | `generate --project <id> --storyboard <id> --reference-image <character-card> --reference-image <scene-background-card>` |
| 文生视频         | `text-to-video`                                            |
| 首帧图生视频     | `first-frame`                                              |
| 首尾帧           | `first-last`                                               |
| 全能参考         | `omni`                                                     |
| 视频编辑意图     | `edit`                                                     |
| 视频延长         | `extend`                                                   |
| 查询任务         | `status`                                                   |
| 等待结果         | `wait` or creation command with `--wait`                   |
| 等待并下载       | `wait --download` or creation command with `--wait --download` |
| 列表             | `list`                                                     |
| 取消/删除        | `delete`                                                   |
| 查询项目生成记录 | `history list` / `history show`                            |

## 9. Verification Route

执行类任务按生成阶段验收，不只看命令退出码。

| Stage      | Verify                                                                 |
| ---------- | ---------------------------------------------------------------------- |
| 提交前     | 路由已选定；自然语言已转剧本和镜头清单；每个非抽象镜头有 `scene_ref`；prompt 写清参考素材用途；故事板路线已同时准备故事板图、角色卡和场景/背景卡；有声任务写清声音设计或参考音频用途；复杂任务已确认 project/storyboard；模式互斥通过；必要时已跑 `--dry-run-payload` |
| 提交后     | 运行目录存在 `request-payload-redacted.json`、`media-manifest.json`、`generation-log.json`；真实提交存在 `submit-summary.json` |
| 等待完成   | `task-result.json` 存在；任务状态成功；结果里有 `content.video_url`     |
| 下载交付   | 用户要求下载时本地 MP4 存在，路径返回给用户                            |
| 历史回溯   | 项目化运行存在 `generation-record.json`，可用 `history show` 查询        |
| 结果不匹配 | 进入 `iteration.md`，只做 1-3 处定向修改                               |

完成、失败、超时或只提交未等待时，读取 `completion.md`，把实际提交的 prompt、使用的素材清单、结果、证据目录和下一步一起汇报给用户。

代码或文档变更按影响面验证：

| Change Type          | Verify                                                                    |
| -------------------- | ------------------------------------------------------------------------- |
| 文档/路由/index 改动 | `python skills/seedance2-video-pro/scripts/validate_skill.py`（自检 references 链接 + payload JSON） |
| CLI 行为改动         | `python -m py_compile skills/seedance2-video-pro/scripts/seedance2_video.py` + `python skills/seedance2-video-pro/scripts/seedance2_video.py --help` 冒烟 |
| API 参数改动         | 重新查火山官方文档，再补测试或对照 `references/api.md`                    |
| 真实生成改动         | 用有效 `ARK_API_KEY` 跑创建子命令 / `status` / `wait`（仅手动）           |

## Routing Output Contract

执行前给 Agent 自己一个短决策：

```text
Route:
- Need: ...
- Interaction: ask / options / proceed
- Completeness: ask / proceed
- Input mode: ...
- Scene: ...
- Method: none / clapperboard / storyboard
- Project flow: none / project+visual-storyboard / quick-sample
- Sound: silent / generated audio brief / reference_audio role / post-audio recommended
- Split: intelligent orchestration gate / single storyboard / storyboard + cards / multi-segment rounds by complexity-change-density-load
- Asset lookup: project list / asset search / asset list / asset show / skipped because ...
- CLI command: ...
- Verification: dry-run artifacts / submitted task / completed task / downloaded mp4
- Completion: prompt + materials + result + artifacts + acceptance
- References loaded: ...
```

对用户不必展示完整 route，除非用户要求解释。对用户展示时保持简短。
