# video-gen-storyboard

video-gen 技能族的**方法论卫星**：故事板法（母图主控、以图控视频）的 canonical。覆盖九宫格／四栏／脚本拼版三种版式、项目资产库与生成历史、4K 故事板确认门。

## 目录

| 文件 | 说明 |
|---|---|
| `SKILL.md` | 运行时入口：触发条件、Hard Rules、技能族意图路由 |
| `skill.json` | 卫星元数据（`role: satellite`，hub 指向 video-gen-pro） |
| `references/README.md` | 版式选择门与流程总览（加载索引） |
| `references/visual-storyboard.md` | 端到端执行流程（检索门 → 母图 → 4K 确认门 → 切片投产） |
| `references/storyboard-board.md` | 项目资产库与故事板登记 |
| `references/grid-storyboard.md` | 九宫格版式 |
| `references/four-column-storyboard.md` | 四栏版式 |
| `references/script-composed-storyboard.md` | 脚本拼版版式 |

## 维护约定

- description 由 `SKILL.md` frontmatter 唯一持有（SSOT）；长度硬上限 1024 字符、目标 ≤500，由 `scripts/validate_repository.py` 校验。
- 4K 故事板确认门是 Red Line，版式文件改动不得绕过；Red Lines 全文只在 hub SKILL.md 维护。
- 跨 skill 相对链接按「安装后同级」约定书写（`../video-gen-xxx/...`），改动后跑仓库校验脚本。
