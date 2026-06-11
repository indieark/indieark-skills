# References

这些文件是 Skill 运行时按需读取的参考，不是仓库维护文档。本目录只剩 hub（执行器+路由枢纽）自己的参考；方法论、剧本编排、资产与填料层的参考已拆到各卫星 skill（见文末「卫星 references」）。

加载顺序约定：**核心概念 → 入口决策 → 场景与方法 → Provider 边界 → 运行时与产物**。这五组是运行时导航分区；具体前后顺序以 `../SKILL.md` 的「决策管线」为准。遵守渐进披露：先读入口，再按任务链路加载必要文件；不要因为在同一分区就批量加载整组。

## 核心概念（Core Concepts）

先厘清剧本 / 资产 / 方法论三者边界，再进入具体路线。

| File          | Load When                                                      |
| ------------- | -------------------------------------------------------------- |
| `concepts.md` | 需要厘清一次任务里内容/料/组织方式分别是什么、谁可省略、资产有哪些维度和形态、故事板算资产还是方法论产物 |

## 入口决策（Entry & Routing）

判断是否追问、选哪条任务路线。

| File             | Load When                                                      |
| ---------------- | -------------------------------------------------------------- |
| `interaction.md` | 需要判断是否问询用户、给方向选项、或停止追问直接执行；advisor mode 越界确认也在这里 |
| `router.md`      | 复杂请求需要判断追问/执行、输入模式、场景、导演方法和 API 操作 |

## 场景与方法（Scenes & Craft）

把用户意图收束到具体场景 → 选择导演方法 → 声音方案。

| File                | Load When                                                      |
| ------------------- | -------------------------------------------------------------- |
| `scenes.md`         | 用户指定具体场景、用途或素材组合，需要避免强套通用模板         |
| `methods.md`        | 需要在导演法、故事板法之间选择导演方法（两法分开存储，仅选一个主结构；导演法用三段式骨架，时序递进写在【画面内容】里）；细则在 `../../video-gen-director/references/director-method.md` 与 `../../video-gen-storyboard/references/README.md` |
| `sound-design.md`   | 有声/无声、音效、音乐、说话人声、字幕/标题文字、画面文字或参考音频需要形成可执行方案 |

## Provider 边界（Provider Boundary）

火山方舟 API 调用契约 + CLI 命令模板。

| File     | Load When                                                      |
| -------- | -------------------------------------------------------------- |
| `api.md` | 需要修改或确认火山方舟 API 调用、payload、模型、端点、互斥规则 |
| `cli.md` | 需要写 `scripts/video_gen_pro.py` 的命令行调用模板           |

## 运行时与产物（Runtime & Artifacts）

完成回复、证据归档和反馈驱动的迭代修正。

| File           | Load When                          |
| -------------- | ---------------------------------- |
| `completion.md` | 生成完成、失败、超时或下载后，需要规范回复用户 |
| `iteration.md` | 用户反馈结果不满意，需要定向修正   |

## 卫星 references（跨 skill 路由）

以下参考已迁出本目录，由对应卫星 skill 持有；按需跨 skill 加载。

| 原职责 | 现归属 |
| ------ | ------ |
| 功能介绍 guide mode | `../../video-gen-guide/references/guide-mode.md` |
| 参考包 advisor mode | `../../video-gen-advisor/references/advisor-mode.md` |
| 流程协议（阶段提醒、剧本候选、确认门、复盘） | `../../video-gen-script/references/generation-workflow.md` |
| 智能编排拆分门、多段连续性台账 | `../../video-gen-script/references/multi-segment-continuity.md` |
| 导演法三段式细则 | `../../video-gen-director/references/director-method.md` |
| 故事板法版式与端到端流程、资产检索与确认门 | `../../video-gen-storyboard/references/`（入口 `README.md`、流程 `visual-storyboard.md`） |
| 资产设定图族（角色/场景/道具/素材/交接） | `../../video-gen-assets/references/`（入口 `assets.md`） |
| 填料层输入指南（运镜/景别/构图/光影/风格/参考图投放） | `../../video-gen-cinematography/references/input.md` |

## 维护约定

- 每次任务只加载真正需要的文件，遵守渐进披露。
- 保持本目录精简。超过 100 行的新增参考应有目录或拆分，并从 `SKILL.md` 与本表同时登记。
- 卫星持有的参考不要回拷到本目录；hub 只通过上表路由，避免双份漂移。
