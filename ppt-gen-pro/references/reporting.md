# Reporting

Load when: 需要给用户汇报 route 选择、扩展安装、生成结果或失败信息。
Avoid: 不要报告不存在的输出文件、页数、截图或验证结果。
Pairs with: `workflow.md`, `route-introduction.md`, `usage.md`

## Route Selection Reply

用户要生成 PPT 时，先回复：

- 使用 `route-introduction.md` 的标准介绍结构说明三种路线。
- 推荐路线和理由。
- 让用户选择或接受推荐。
- 如扩展未安装，说明将安装或检查的来源仓库。
- 不要把 SVG PPT 包装成默认高级路线；它只在可编辑优先时推荐。

## Completion Reply

委托扩展完成后，结果回复至少包含：

- Original Request
- Selected Route
- Extension Used
- Extension Checkout Path
- Extension Skill Entry
- Method
- Output Path
- Preview or inspection result
- Verification

## Failure Reply

失败时必须区分：

- 扩展未安装或安装失败。
- 用户尚未选择路线。
- 选定扩展执行失败。
- 输出文件不存在或验证失败。
