# video-gen-script

video-gen 技能族的**剧本编排卫星**。源仓位于 `skills/video-gen-pro`（仓库内 `skills/` 下 8 个 skill 平级共存），发布后与兄弟 skill 同级安装。

## 职责

- 自然语言 → 剧本候选 → 资产清单 → 镜头清单的流程协议与阶段提醒。
- 智能编排拆分门：判断 15 秒是否只是上限、单段是否可行、是否需要多个更短故事板和生成轮次。
- 多段连续性台账、尾帧交接、`extend` 链规划。
- 生成前确认门、结构化修改意见、结果复盘。

## 目录

| 文件 | 说明 |
|---|---|
| `SKILL.md` | 运行时入口：触发条件、技能族意图路由、前置条件路由 |
| `skill.json` | 卫星元数据（`role: satellite`，hub 指向 video-gen-pro） |
| `references/generation-workflow.md` | 流程协议 + 确认门 + 复盘 canonical |
| `references/multi-segment-continuity.md` | 拆分门 + 连续性台账 canonical |

## 维护约定

- description 由 `SKILL.md` frontmatter 唯一持有（SSOT），其他索引只链接不复制；长度硬上限 1024 字符、目标 ≤500，由 `scripts/validate_repository.py` 校验。
- 跨 skill 相对链接按「安装后同级」约定书写（`../video-gen-xxx/...`），改动后跑仓库校验脚本。
