# office-pro · L1 路由（v0.1.0-skeleton）

> 父级：[../SKILL.md](../SKILL.md)
> 立项档：[../../../plans/008-new-skill-office-pro.md](../../../plans/008-new-skill-office-pro.md)

## 判定顺序

| 优先级 | Route | 命中条件 |
|---|---|---|
| 1 | `data-analysis` | 用户给数据文件 / 提到统计 / 可视化 / 分析报告 / "看看这份数据" |
| 2 | `office-connect` | 用户提到飞书 / 群消息 / 文档 / 多维表 / 日历 / 任务 / 会议纪要 / 日报周报 |
| — | 两者串联 | "把这份数据分析完发到 xxx 群" / "拉飞书表分析" — 先 data-analysis 再 office-connect |

## `office-connect` 子路（v0.1.0-skeleton 仅 feishu）

| 子路 | 下游 | 状态 |
|---|---|---|
| `feishu/im` | `lark-im` | active — 发消息 / 群通知 / 富文本 |
| `feishu/doc` | `lark-doc` / `lark-markdown` | active — 文档读写 |
| `feishu/drive` | `lark-drive` | active — 云空间文件 |
| `feishu/sheets` | `lark-sheets` | active — 电子表格 |
| `feishu/base` | `lark-base` | active — 多维表 |
| `feishu/calendar` | `lark-calendar` | active — 日程 |
| `feishu/task` | `lark-task` | active — 任务 |
| `feishu/vc` | `lark-vc` / `lark-vc-agent` | active — 视频会议 |
| `feishu/approval` | `lark-approval` | active — 审批 |
| `feishu/workflow/meeting-summary` | `lark-workflow-meeting-summary` | active — 端到端会议纪要剧本 |
| `feishu/workflow/standup` | `lark-workflow-standup-report` | active — 端到端日报周报剧本 |
| `notion` / `outlook` / `slack` / `dingtalk` | — | **TBD（plans/008 Q1 待拍板）** |

## `data-analysis` 子路（v0.1.0-skeleton）

| 子路 | 关注 | 候选实现（plans/008 Q2 待拍板） |
|---|---|---|
| `explore` | 数据形态 / 字段类型 / 缺失值 / 样本 | pandas.info/describe + duckdb 直接查 CSV/Parquet |
| `clean` | 类型转换 / 缺失填充 / 去重 / 标准化 | pandas / polars |
| `stat` | 聚合 / 分组 / 相关 / 假设检验 | pandas / polars / scipy |
| `viz` | 柱/线/散点/热力 / 交互看板 | plotly（默认交互 HTML）/ matplotlib（静态 PNG）— Q3 待拍板 |
| `report` | Markdown / HTML 报告 | 本路或转交 write-pro / ppt-gen-pro — Q4 待拍板 |

## 产物归宿

`_work/office_runs/<timestamp>-<intent>/`：

```
_work/office_runs/2026-05-27-1500-weekly-active-users-analysis/
├─ plan.md          ← 意图、路线、子路、下游
├─ data/            ← 原始 / 中间 / 清洗后数据
├─ figures/         ← 可视化 PNG/HTML
└─ report.md        ← 摘要（若 Q4 决定本 Skill 出报告）
```

## 与全局 lark-* / .agent/feishu-*.md 的关系

- 单点 API 调用直接走对应 `lark-*`，不必绕 office-pro。
- 端到端剧本（涉及 ≥3 个 lark-* / ≥2 个步骤）走 office-pro，office-pro 负责状态、留痕、回滚提示。
- 飞书 CLI 授权流程权威来源：[`.agent/feishu-auth.md`](../../../../../.agent/feishu-auth.md)；office-pro 不复制其内容。

## 未来扩展（plans/008 待澄清）

- Q1：多平台 — 拍板后逐个落 `references/route-notion.md` / `route-outlook.md` / `route-slack.md` / `route-dingtalk.md`。
- Q2：数据分析默认栈 — 拍板后在 `scripts/office-pro-analyze` 固化；现在每次按用户偏好临场选。
- Q4：自动报告边界 — 拍板"出到哪一层"，明确 office-pro / write-pro / ppt-gen-pro 三者衔接顺序。
- Q5：OCR / 表格抽取 — 拍板归属（office-pro vs search-pro convert-format）。
- Q7：飞书任务自动同步 PROJECTS.md — 拍板后落 `references/workflows/sync-projects.md`。
