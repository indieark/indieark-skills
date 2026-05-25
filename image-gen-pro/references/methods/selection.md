# Method Selection

> Load when: 任务看起来需要多个方法，或不确定该读哪个 method 文件。
> Avoid: 已经明确只需要一个方法文件，或用户只问 CLI/API。
> Pairs with: `README.md` 做方法索引；`prompt-patterns.md` 输出通用骨架；具体 method 文件给细节。

## Selection Pipeline

1. 先判断是否真的需要方法论。
2. 选择一个主方法。
3. 只在必要时选择一个辅助方法。
4. 读具体 method 文件。
5. 回到 `../director.md` 生成最终 prompt。

## No-Method Cases

用 `none`，不要加载具体方法：

- 用户已经给出完整 prompt。
- 用户只要求 dry-run / API payload / CLI 参数。
- 任务是简单主体图，没有复杂构图、文字、参考图或商业约束。
- 用户明确要快速执行，不要扩展创意。

## Primary Method Matrix

| Need | Primary Method | Why |
| --- | --- | --- |
| 画面布局、焦点、留白、画幅 | `composition.md` | 先解决画面组织 |
| 同一角色、商品、品牌或系列图 | `consistency.md` | 先固定身份锚点 |
| 商品、商业视觉、商店封面 | `product.md` | 先解决卖点和可读性 |
| 风格、媒介、材质、调色 | `style.md` | 先约束视觉语言 |
| 输入图局部修改、换背景、保留结构 | `edit.md` | 先定义保留/修改边界 |
| 精确文字、标题、多语言、中文 | `typography.md` | 先控制文字风险 |
| 复杂规格、JSON/config-style 输入 | `structured-prompts.md` | 先保持字段不丢 |
| 信息图、field guide、教学图 | `infographics.md` | 先定义区域和阅读顺序 |
| 论文图、流程图、技术图 | `research-figures.md` | 先保持严谨表达 |
| App/dashboard/web/game UI mockup | `ui-mockups.md` | 先像产品规格 |
| 摄影、产品照、生活方式照片 | `photography.md` | 先定义拍摄上下文 |
| 海报、活动图、封面、宣传图 | `posters.md` | 先定义阅读层级 |

## Allowed Pairings

| Primary | Useful Secondary | Reason |
| --- | --- | --- |
| `product` | `composition`, `style`, `typography` | 商业图常需要版式、材质、文字区 |
| `posters` | `typography`, `composition` | 海报依赖标题层级和留白 |
| `edit` | `consistency`, `style` | 编辑常要保留身份或统一风格 |
| `infographics` | `typography`, `structured-prompts` | 信息图需要区域和文字约束 |
| `research-figures` | `structured-prompts`, `infographics` | 论文图需要字段和图示语法 |
| `ui-mockups` | `typography`, `structured-prompts` | UI 需要组件规格和文字控制 |
| `photography` | `product`, `style` | 摄影常关联产品和光线材质 |
| `consistency` | `style`, `edit` | 一致性常要绑定风格或编辑边界 |

## Stop Rules

- 不要同时加载 3 个以上方法文件，除非用户要求做完整方案。
- 如果两个方法冲突，以用户的实际交付物为准。
- 如果 prompt 变长，删掉抽象风格词，保留用途、主体、构图、限制和参考关系。
- 如果 API 能力不支持某项要求，回到 `../api.md` 和 provider-specific reference。
