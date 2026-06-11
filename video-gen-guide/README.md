# video-gen-guide

video-gen 技能族的**说明卫星**（guide mode）。只解释能力、边界、输入、确认门和下一步建议，不调 CLI、不生成。

## 目录

| 文件 | 说明 |
|---|---|
| `SKILL.md` | 运行时入口：触发条件、Hard Rules、技能族意图路由 |
| `skill.json` | 卫星元数据（`role: satellite`，hub 指向 video-gen-pro） |
| `references/guide-mode.md` | guide mode 的 8 项结构与按需说明协议 canonical |

## 维护约定

- description 由 `SKILL.md` frontmatter 唯一持有（SSOT）；长度硬上限 1024 字符、目标 ≤500，由 `scripts/validate_repository.py` 校验。
- 跨 skill 相对链接按「安装后同级」约定书写（`../video-gen-xxx/...`），改动后跑仓库校验脚本。
