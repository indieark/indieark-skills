# Methods

> Load when: 任务需要专业图像方法，而不是简单 prompt 或 API 调用。
> Avoid: 用户只要快速生成、CLI 参数、或仓库维护。
> Pairs with: `scenes.md` 选择场景；`director.md` 输出 prompt。

本目录承载从 `gpt_image_2_skill` craft 和 gallery 中抽出的 prompt 方法论。普通任务只读本索引；复杂视觉任务必须选一个主方法；方法选择不清时读 `selection.md`；需要输出 prompt 骨架时读 `prompt-patterns.md`；需要专业控制时，再按任务读取 1-2 个具体方法文件。

## Layered Loading

```text
SKILL.md
=> references/README.md
=> methods/README.md
=> selection.md
=> prompt-patterns.md or one concrete method file
=> ../director.md
```

不要默认把所有方法文件加载进上下文。

| Method | Use When | File |
| --- | --- | --- |
| selection | 方法选择不清、需要组合策略 | `selection.md` |
| prompt-patterns | 需要通用 prompt 骨架 | `prompt-patterns.md` |
| composition | 构图、焦点、留白、视觉层次复杂 | `composition.md` |
| consistency | 角色、商品、风格需要跨图一致 | `consistency.md` |
| product | 商品图、商店封面、商业视觉 | `product.md` |
| style | 风格约束、媒介、材质、统一视觉系统 | `style.md` |
| edit | 局部修改、保留结构、输入图编辑 | `edit.md` |
| typography | 海报、中文、多语言、精确文字 | `typography.md` |
| structured-prompts | JSON/config-style prompt 或复杂规格 | `structured-prompts.md` |
| infographics | 固定区域信息图、科普图、field guide | `infographics.md` |
| research-figures | 论文图、技术图、数据图、diagram grammar | `research-figures.md` |
| ui-mockups | App、dashboard、web UI、设计系统 mockup | `ui-mockups.md` |
| photography | 摄影、真实拍摄上下文、镜头/光线 | `photography.md` |
| posters | 商业海报、层级、文案、活动视觉 | `posters.md` |

## Selection Rules

- 只选一个主方法。
- 复杂任务最多再选一个辅助方法。
- 简单任务用 `none`，直接走 `../director.md`。
- 商业图、海报、角色一致性、参考图模仿、UI/信息图、精确文字、透明资产等高要求任务不能跳过方法选择。
- 方法论不写进 provider adapter。
- 后续迁移 gallery 或 prompt 模板时，先登记到本索引或对应 category 文件。
- 如果只是选方法，不读具体方法文件；如果只是套骨架，优先读 `prompt-patterns.md`。

## Craft Migration Map

| Source Craft Topic | Target |
| --- | --- |
| Use gallery before writing from scratch | `../gallery.md` |
| Exact text goes in quotes | `typography.md` |
| Canvas/aspect/layout before subject | `composition.md` |
| JSON/config-style prompts | `structured-prompts.md` |
| Fixed-region schemas | `infographics.md` |
| Research/data figure grammar | `research-figures.md` |
| UI prompts as product specs | `ui-mockups.md` |
| Multi-panel consistency | `consistency.md` |
| Camera and capture context | `photography.md` |
| Scene density beats adjectives | `../director.md` |
| Style anchors should be bounded | `style.md` |
| Promotional hierarchy | `posters.md` |
| Material/lighting/palette separation | `style.md` |
| Edit endpoint invariants | `edit.md` |
| Targeted negation | `../director.md` |
| Category mini-schemas | `../gallery.md` and category files |
| Dense Chinese/multilingual layouts | `typography.md` |
| Attribution/gallery metadata | `../gallery.md` |
| Safety/copyright notes | `../safety.md` |
