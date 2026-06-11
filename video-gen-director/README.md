# video-gen-director

video-gen 技能族的**方法论卫星**：导演法三段式视频 prompt 写法（基础设定＋氛围与画质＋画面内容）的 canonical。语言控制为主、不预画母图；槽位填料引用 video-gen-cinematography。

## 目录

| 文件 | 说明 |
|---|---|
| `SKILL.md` | 运行时入口：触发条件、三段式 Hard Rules、技能族意图路由 |
| `skill.json` | 卫星元数据（`role: satellite`，hub 指向 video-gen-pro） |
| `references/director-method.md` | 导演法方法论 canonical：三段式骨架、控场技巧、时序递进、正反例 |

## 维护约定

- description 由 `SKILL.md` frontmatter 唯一持有（SSOT）；长度硬上限 1024 字符、目标 ≤500，由 `scripts/validate_repository.py` 校验。
- 「最终 prompt 三段之外零追加」是已归档的修复结论（见源仓 CHANGELOG），改动 director-method.md 时不得回退。
- 跨 skill 相对链接按「安装后同级」约定书写（`../video-gen-xxx/...`），改动后跑仓库校验脚本。
