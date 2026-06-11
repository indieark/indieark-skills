# Storyboard Method 故事板法

> Load when: 已选择故事板法（图像母图主控镜头顺序和运动），需要按需选择故事板版式、脚本拼版或多段连续性子方法。
> Avoid: 还没判断是否用故事板法；先回到 `../../video-gen-pro/references/methods.md` 选方法，或回到 `../../video-gen-assets/references/assets.md` 判断是否需要视觉资产。
> Pairs with: `../../video-gen-pro/references/methods.md` 是方法论入口；`../../video-gen-assets/references/assets.md` 管角色卡/场景卡资产；`visual-storyboard.md` 管项目库、确认门和生成历史；`../../video-gen-assets/references/seedance-handoff.md` 进入视频生成。

故事板法是两种方法论之一：以**图像母图为主、短读图 prompt 为辅**控制镜头顺序和运动。故事板是上层概念——一张按需压缩视频信息的 4K 主运动参考图；首版正式故事板就必须 4K / 等效 4K，不走低清预览确认。九宫格、四栏、8 镜头、制作设定板和脚本拼版只是不同信息密度和版式。故事板不单独承担人物、背景和道具细节锁定，视频提交时要和对应角色卡、场景/背景卡一起作为参考输入。复杂任务进入本目录前应先完成 `visual-storyboard.md` 的项目/资产检索门。

## 智能编排判断（Intelligent Orchestration Gate）

判断单段还是多段时，先做智能编排判断：先确认 15 秒只是单次生成上限，再按场景变化、角色负载、动作变化、镜头变化、道具状态和声音文字负载决定单段或多段。`15 秒是否只是上限`、`单段是否可行`、信息负载来自哪里、是否拆成多个更短故事板和生成轮次——这些都在 `../../video-gen-script/references/multi-segment-continuity.md` 的 Intelligent Orchestration Gate 与 Automatic Split Route 里展开。智能编排与多段连续性是故事板法的编排能力，不是独立方法。

## Method Index

| Need | File | Output |
| ---- | ---- | ------ |
| 生成视频主运动参考图 | `storyboard-board.md` | 自适应故事板母图、信息密度、配套角色/场景卡输入、区域主次和视频读图规则 |
| 多张 CUT / 场景 / 调度图需要拼成信息图 | `script-composed-storyboard.md` | 原子图片清单、脚本拼版清单、4K 故事板海报和短视频读图 prompt |
| 单段视频需要镜头顺序母图 | `grid-storyboard.md` | 镜头网格版式提示词和视频读图 prompt，可九宫格或自定义格数 |
| 短剧、广告、系列内容需要项目总览 | `four-column-storyboard.md` | 项目级版式提示词和视频读图 prompt，可四栏、制作设定板或自定义栏目 |
| 判断单段或多段并保持连续 | `../../video-gen-script/references/multi-segment-continuity.md` | 智能编排判断、连续性台账、镜头边界、`continuity_mode`、按需尾帧/首尾帧/长镜头延长和多段 prompt 模板 |

## Loading Patterns

已有角色图和场景图：

```text
visual-storyboard.md 已登记或确认可复用资产
storyboard-board.md
-> 为每个分镜/CUT 绑定对应角色卡和场景卡
-> 信息密集或需要中文文字/表格时，可直接生成完整 4K 故事板母图；需要确定性可编辑文字、指定字体/品牌版式、超密集 CUT 表或程序化复盘时进入 script-composed-storyboard.md
-> 必要时参考 grid-storyboard.md 或 four-column-storyboard.md
-> ../../video-gen-assets/references/seedance-handoff.md
```

多段视频或系列内容：

```text
visual-storyboard.md 检索门已完成
../../video-gen-assets/references/setting-director.md
-> ../../video-gen-script/references/multi-segment-continuity.md 先做 Intelligent Orchestration Gate，判断 15 秒是否只是上限、单段是否可行、是否需要多个更短故事板和生成轮次
-> storyboard-board.md
-> 每段需要 CUT 海报确认时进入 script-composed-storyboard.md
-> 必要时参考 grid-storyboard.md 或 four-column-storyboard.md
-> ../../video-gen-assets/references/seedance-handoff.md
```

## Boundary

- 图片生成由 Skill 编排当前环境可用的图像生成工具；`videogen` CLI 只登记生成结果。
- 本目录不写具体图片 provider、模型、Key 或鉴权参数。
- 故事板、分镜和 CUT 原子图必须参考已确认的角色卡和场景卡；多张分镜拼版时，每张分镜也要能回溯到对应 `character_refs` 和 `scene_ref`。
- 故事板图默认是视频主运动参考图；角色卡和场景/背景卡默认是人物、空间、背景和道具细节锚点。提交 Seedance 时必须在 `video-prompt.txt` 写清参考图编号和主次。
- 故事板图可以包含详细文字、表格和镜头说明，但首版正式图必须 4K 清晰可读；低清草稿不能登记、确认或提交 Seedance；交给 Seedance 的 `video-prompt.txt` 要短，只写读图规则和边界。
- 清楚可规划的镜头优先故事板法；混沌粒子、爆炸烟尘、抽象动态或难以画清的随机效果优先 prompt-heavy 或混合路径（导演法）。
