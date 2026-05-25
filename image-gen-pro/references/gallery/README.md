# Gallery Categories

> Load when: 需要维护或迁移 gallery category 文件。
> Avoid: 普通生成任务；普通任务应先读 `../gallery.md`，再读一个具体 category。
> Pairs with: `../gallery.md` 作为总索引；`../methods/README.md` 作为 prompt craft 路由。

本目录承载从 `gpt_image_2_skill` 抽取来的 prompt atlas 分类。上游预览图片不迁移。

## SSOT 归属

- **Category 清单 / 文件名 / Use First For / Source Count**：唯一定义在 `../gallery.md` 的 `Category Catalog` 表。新增、改名、调整 source count 都只改那一处。
- **本 README**：只保留 file rules，不复述 category 列表。

## File Rules

- 每个 category 一个 Markdown 文件，文件名与 `../gallery.md` 表中 `File` 列严格一致。
- 每个条目保留 prompt、recommended size、quality、source metadata。
- 不提交私有素材。
- 预览图片资产默认不迁，除非后续明确纳入样例资产管理。
- 外部来源条目必须保留 source attribution。
- 新增 category 流程：先在 `../gallery.md` 的 `Category Catalog` 表登记一行，再在本目录创建对应文件。
