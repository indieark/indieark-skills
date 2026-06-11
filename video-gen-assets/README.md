# video-gen-assets

video-gen 技能族的**资产卫星**：角色／场景／道具／平面素材设定图的提示词结构、资产登记、跨剧本检索复用与 Seedance 交接的 canonical。图像本体由外部 `image-gen-pro` skill 生成，本技能族不接管图像 CLI。

## 目录

| 文件 | 说明 |
|---|---|
| `SKILL.md` | 运行时入口：触发条件、Hard Rules、技能族意图路由 |
| `skill.json` | 卫星元数据（`role: satellite`，hub 指向 video-gen-pro） |
| `references/assets.md` | 资产法入口：Default Path、类型分流 |
| `references/README.md` | 资产族文件加载索引 |
| `references/principles.md` | 通用原则 |
| `references/character-sheet.md` / `scene-sheet.md` / `prop-sheet.md` / `graphic-sheet.md` | 各类型 sheet 细则 |
| `references/setting-director.md` | 设定导演（资产体系统筹） |
| `references/seedance-handoff.md` | 资产图交接 Seedance 规则 |

## 维护约定

- description 由 `SKILL.md` frontmatter 唯一持有（SSOT）；长度硬上限 1024 字符、目标 ≤500，由 `scripts/validate_repository.py` 校验。
- 资产命名与引用详略一致性的 canonical 在 hub 的 `../video-gen-pro/references/concepts.md`，本 skill 不复制只引用。
- 跨 skill 相对链接按「安装后同级」约定书写（`../video-gen-xxx/...`），改动后跑仓库校验脚本。
