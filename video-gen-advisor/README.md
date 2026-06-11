# video-gen-advisor

video-gen 技能族的**参考包卫星**（advisor mode）。输出 master prompt、平台变体、镜头清单、资产 brief、声音 brief 和评判 checklist；不调火山方舟 API、不出视频。

## 目录

| 文件 | 说明 |
|---|---|
| `SKILL.md` | 运行时入口：触发词、Hard Rules、技能族意图路由 |
| `skill.json` | 卫星元数据（`role: satellite`，hub 指向 video-gen-pro） |
| `references/advisor-mode.md` | advisor mode 的触发词清单、Hard Rules、参考包必给项 canonical |

## 维护约定

- description 由 `SKILL.md` frontmatter 唯一持有（SSOT）；长度硬上限 1024 字符、目标 ≤500，由 `scripts/validate_repository.py` 校验。
- 跨 skill 相对链接按「安装后同级」约定书写（`../video-gen-xxx/...`），改动后跑仓库校验脚本。
