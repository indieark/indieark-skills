# video-gen-cinematography

video-gen 技能族的**填料层卫星**：影视语言参考库（运镜、景别、构图、光影调色、视觉基调、风格核心、时间氛围 token、参考图投放），横切导演法与故事板法。附带示例媒体库与人类画廊。

## 目录

| 文件 | 说明 |
|---|---|
| `SKILL.md` | 运行时入口：触发条件、Hard Rules、技能族意图路由 |
| `skill.json` | 卫星元数据（`role: satellite`，hub 指向 video-gen-pro） |
| `references/input.md` | 填料层入口：维度索引与按需加载规则 |
| `references/input/` | 八个维度文件 + `media/`（示例视频/图片）+ `gallery.html`（人类画廊） |

## 维护约定

- description 由 `SKILL.md` frontmatter 唯一持有（SSOT）；长度硬上限 1024 字符、目标 ≤500，由 `scripts/validate_repository.py` 校验。
- **media 双界面引用**：`media/` 文件被 input 各 md 的 `![]()` 与 `gallery.html` 的 JS 同时引用，改文件名/路径必须两处同步，否则裂图。维度 md 是中文正文（Seedance 是中文模型）。
- 跨 skill 相对链接按「安装后同级」约定书写（本目录 references/input/*.md 内为 `../../../video-gen-xxx/...`），改动后跑仓库校验脚本。
