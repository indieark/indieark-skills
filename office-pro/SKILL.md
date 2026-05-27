---
name: office-pro
description: "[v0.1.0-skeleton] Routing entry for IndieArk's office automation + data analysis workflows. Use whenever the user wants to (a) automate office tasks across communication/doc/calendar/task platforms — v0.1.0 focused on Feishu via global lark-* sub-skills; multi-platform (Notion/Outlook/Slack/钉钉) TBD, or (b) explore/clean/stat/visualize data (technical stack pandas/polars/duckdb + plotly/matplotlib TBD). Skeleton stage — two L1 routes (office-connect, data-analysis) scaffolded, executor wiring TBD per plans/008. Boundary: pure Feishu OpenAPI single-shot calls route directly to the corresponding lark-* sub-skill; decks go to ppt-gen-pro, long-form writing to write-pro, images to image-gen-pro."
---

# office-pro

你是 IndieArk 的办公接入 + 数据分析执行编排器。**v0.1.0-skeleton 阶段**：两条 L1 路线骨架已锁，具体平台范围（多平台 vs 仅飞书）与数据分析技术栈按 [`../../plans/008-new-skill-office-pro.md`](../../plans/008-new-skill-office-pro.md) 「待澄清 1 / 2 / 4」逐项推进。

## Hard Contract

- 触发场景：
  - 办公接入：发消息 / 拉文档 / 写表 / 安排日程 / 派任务 / 开会拿纪要 / 写日报周报
  - 数据分析：探索 / 清洗 / 统计 / 可视化 / 报告（CSV / Excel / Parquet / SQLite / 飞书 sheets）
- 不接管的边界（直接转交）：
  - 纯飞书 OpenAPI 单点调用（"发条消息到 xxx 群" / "拿一下这份文档的 token"）→ 直接走对应 `lark-*` 子 Skill
  - 把分析结果做成 deck → `ppt-gen-pro`
  - 写成长文 / 公众号 → `write-pro`
  - 出图 → `image-gen-pro`
  - 找资料 / 抓网页 → `search-pro`
- 单一信息源：全局 `lark-*` 40+ 子 Skill 的 API 调用细节不在本 Skill 复制；IndieArk 根目录 `.agent/feishu-*.md` 协议也不复制，只链回。
- 输出归宿：`_work/office_runs/<timestamp>-<intent>/`。
- v0.1.0-skeleton 限制：本 Skill 暂不封装自己的 CLI / Python entrypoint；数据分析路线先用 ad-hoc 脚本，技术栈按 plans/008 Q2 拍板后再固化到 `scripts/`。

## Route Matrix（v0.1.0-skeleton）

详见 [`references/router.md`](references/router.md)。

| 路线 | 子路 | 下游 | 实现状态 |
|---|---|---|---|
| `office-connect` | feishu（默认） / notion / outlook / slack / 钉钉（多平台待 Q1） | 对应 `lark-*` / 第三方 API | skeleton — 飞书可用，其他平台 TBD |
| `data-analysis` | explore / clean / stat / viz / report | pandas / polars / duckdb / plotly / matplotlib（Q2 待选） | skeleton — 技术栈未拍板，每次按用户偏好走 |

## Workflow（skeleton）

1. 判定意图属于 `office-connect` 还是 `data-analysis`（也可能两条串联：先拉数据 → 再分析 → 再回写飞书表）。
2. 输出路由说明 + 子路 + 下游 lark-* / 库选择，给出待澄清编号。
3. 等用户确认后委托执行；现阶段不在本 Skill 里跑命令。
4. 产物归 `_work/office_runs/<timestamp>-<intent>/`，含 `plan.md` + `data/` + `report.md`（如有报告）。

## 与全局 lark-* 的关系

- 全局 `lark-*` 40+ 子 Skill 是**单点 OpenAPI 能力**。
- office-pro 是**业务流程编排层**，把多个 lark-* 调用组装成端到端剧本（如：开会 → 抓纪要 → 抽待办 → 写回任务 → 通知群）。
- 与 `lark-workflow-meeting-summary` / `lark-workflow-standup-report` 关系：这两个本就是流程化 Skill，office-pro 可链回复用，不复制其逻辑；最终是吸收还是共存待 plans/008 implementing 阶段拍板。

## 当前待澄清（按 plans/008）

升 ready 必拍：1（多平台/仅飞书）/ 2（数据分析默认栈）/ 4（自动报告边界）。
其余 3 / 5 / 6 / 7 可后续单独拍板，不阻塞 skeleton 可用。
