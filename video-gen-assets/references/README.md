# Assets Index 资产二级索引

> Load when: 已进入 `assets.md`，需要按需选择资产子方法（人物/场景/道具/素材维度的设定图、声线、链路理念或交接），而不是加载整套理论。
> Avoid: 还没有判断是否需要视觉资产；先回到 `assets.md` 做路由。需要故事板母图或版式时，去方法论 `../../video-gen-storyboard/references/README.md`。
> Pairs with: `assets.md` 是资产族运行时入口；`../../video-gen-storyboard/references/visual-storyboard.md` 管项目库、确认门和生成历史；`../../video-gen-pro/references/concepts.md` 定义资产维度与形态。

本目录只保存可登记、可跨剧本复用的**资产**子方法：人物、场景、道具、素材四类图像资产的设定图，人物附属的声线音频资产，以及链路理念和 Seedance 交接。运行时先读 `assets.md`，再按下表只读一个或少数必要文件。复杂任务在进入本目录前应先完成 `../../video-gen-storyboard/references/visual-storyboard.md` 的项目/资产检索门。故事板母图、九宫格/四栏/脚本拼版等版式和多段编排属于**方法论产物**，不在本目录，见 `../../video-gen-storyboard/references/README.md`。

## Method Index

| Need | File | Output |
| ---- | ---- | ------ |
| 理解为什么要先做视觉资产 | `principles.md` | 三层链路、reference 纯净度、确认门和常见错误 |
| 从一句想法拆出角色、场景、风格和段落 | `setting-director.md` | 可登记的项目设定和资产清单 |
| 生成或修正人物设定图 | `character-sheet.md` | 角色卡提示词；正式角色卡只能用人设三视图或多视图模板；含声线（voice）附属音频资产登记 |
| 生成或修正场景设定图 | `scene-sheet.md` | 基本场景卡、严格复用正交四视图、本次剧情多视角联合图、场景 DNA 和禁止穿帮提醒 |
| 生成或修正道具/产品设定图 | `prop-sheet.md` | 道具卡提示词；纯净底单图 / 主图+拆解 / 多视图道具卡，纯图像零文字 |
| 生成或登记可复用视觉素材 | `graphic-sheet.md` | 素材方法；轴=复用范围，一次性/项目套件/跨项目 master，参考图输入或后期叠加 |
| 视觉资产已生成，准备进 Seedance | `seedance-handoff.md` | CLI 登记、确认、`video-prompt.txt` 和生成步骤 |

## Loading Patterns

一句话复杂任务：

```text
../../video-gen-storyboard/references/visual-storyboard.md 检索门已完成
principles.md
-> setting-director.md
-> character-sheet.md / scene-sheet.md / prop-sheet.md / graphic-sheet.md
-> ../../video-gen-storyboard/references/README.md 规划故事板母图与版式
-> seedance-handoff.md
```

只缺某一类资产：

```text
character-sheet.md / scene-sheet.md / prop-sheet.md / graphic-sheet.md
-> seedance-handoff.md
```

## Boundary

- 图片生成由 Skill 编排当前环境可用的图像生成工具；`videogen` CLI 只登记生成结果。
- 本目录不写具体图片 provider、模型、Key 或鉴权参数。
- 每张生成图都必须保存提示词、来源摘要和用途，后续通过 CLI 登记到项目库。
- 正式角色卡必须走 `character-sheet.md` 的人设三视图或多视图模板；第一种人设描述只是文本基础，不单独作为复杂项目角色卡。
- 场景卡必须走 `scene-sheet.md` 的主要场景列表、场景卡路由判断和单场景提示词格式；多个主要场景逐个生成，不混成一条提示词。每个 `SCxx` 先判断镜头角度数、复用强度和空间风险：单镜头静止、推进或拉远时基本场景卡够用；正交四视图只用于严格复用；多视角联合图只用于某一次剧情场景里的多个镜头角度。不要默认只生成简单场景单图。
- 角色卡和场景卡直接作为视频模型参考输入，必须纯图像、零语义文字（reference 纯净度）；故事板母图可带字，见 `principles.md`。
- 用户只要静态图片最终交付时，转交图片生成 Skill；本目录只服务后续视频生成。

## Source Notes

本目录吸收本机 `ai-director/docs/创作指南` 的三层链路中的资产层：

- `设定导演流`：母系统，负责角色、场景、风格、连续性和段落逻辑。
- 角色和场景/背景细节由对应卡片锁定，并随视频生成一起作为参考输入。

故事板一图流、脚本拼版、分镜一图流和智能编排属于方法论，见 `../../video-gen-storyboard/references/README.md`，不在本目录重复。
