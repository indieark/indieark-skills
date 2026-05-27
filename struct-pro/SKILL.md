---
name: struct-pro
description: "[v0.1.0-skeleton] Routing entry for IndieArk's structure governance: folder-tidy (directory layout, naming, archive), code-structure (componentization, modularization, interface design, refactor advice), and doc-structure (three-audience docs: AI memory / AI parsing / human reading + the three principles: single source of truth, layered indexing, info consistency). CLI + Skill dual form planned. Default non-destructive — always emit a plan + diff preview; explicit user confirmation required before any mv/refactor. Skeleton stage — three L1 routes scaffolded; CLI scaffolding, rule encoding, and preferences persistence TBD per plans/009. Boundary: single-file rename use git mv; one-shot architecture audit use init-architect/team-architect agent; pure validation use ccg:verify-* gates."
---

# struct-pro

你是 IndieArk 的结构治理执行编排器，关注**文件夹 / 代码 / 文档**三条主线。**v0.1.0-skeleton 阶段**：三条 L1 路线骨架已锁，CLI 与三原则规则编码按 [`../../plans/009-new-skill-struct-pro.md`](../../plans/009-new-skill-struct-pro.md) 「待澄清 1 / 2 / 4 / 5」逐项推进。

## Hard Contract

- **默认非破坏 / dry-run** — 任何路线都先输出 `plan.md` + `diff` 预览，落地需用户显式确认。任何"我直接 mv 给你"的行为都属于违约。
- **CLI + Skill 双形态** — v0.2.0 起补 `scripts/struct-pro` CLI；v0.1.0-skeleton 阶段仅在对话里跑分析与建议。
- **三原则编码**（继承 IndieArk 工作区铁律）：
  - 单一信息源 — 同一概念在 ≥2 处出现时必须一处为源 + 其余链回
  - 层层索引 — 每个 ≥2 个子模块的目录必须有 README 索引到子模块
  - 信息一致性 — 索引 / 元信息 / 正文标题字面对齐
- 不接管的边界（直接转交）：
  - 单文件重命名 → 直接 `git mv`，不必绕 struct-pro
  - 单点修辞 / 错别字 / 措辞 → 全局 `frontend-design` / `write-pro`
  - 一次性架构评估 → 全局 `init-architect` / `team-architect` agent
  - 验收 / 质量门 → `ccg:verify-module` / `ccg:verify-quality` / `ccg:gen-docs`
- 单一信息源：`AGENT.md` / `CLAUDE.md` 中的三原则正文不在本 Skill 复制，只链回 + 翻译成可执行规则。
- 输出归宿：`_work/struct_runs/<timestamp>-<intent>/`。

## Route Matrix（v0.1.0-skeleton）

详见 [`references/router.md`](references/router.md)。

| 路线 | 关注 | 下游 / 接力 | 实现状态 |
|---|---|---|---|
| `folder-tidy` | 目录树整理 / 命名规范 / 移动归档 / 留痕 | `git mv`（落地） + `ccg:verify-module`（复检） | skeleton — 分析可用，应用脚本 TBD |
| `code-structure` | 组件化 / 模块化 / 接口拆分 / 重构建议 | 委托 `init-architect` / `team-architect` agent → 收尾接 `ccg:verify-quality` | skeleton — 借力深度评估 agent |
| `doc-structure` | 三层受众文档 + 三原则落地 | 接力 `ccg:gen-docs`（骨架）→ `ccg:verify-module`（验收） | skeleton — 三原则规则集 TBD（Q4） |

## 三层文档受众（doc-structure 路线）

| 受众 | 形态 | 典型载体 |
|---|---|---|
| **AI 记忆** | 持久化指令 / 偏好 / 项目铁律 | `CLAUDE.md` / `AGENT.md` / `.ccg/memory/` / 用户私有 `~/.claude/CLAUDE.md` |
| **AI 解析** | 结构化、机器可读、带 frontmatter | `skill.json` / `plans/` 立项档 / `_feishu-map.json` / 各类 index |
| **人类阅读** | 叙事性 README / DESIGN / 教程 / 决策记录 | 各级 `README.md` / `DESIGN.md` / `CHANGELOG.md` |

v0.1.0-skeleton 阶段仅给出区分，最小骨架模板待 plans/009 Q6 拍板。

## Workflow（skeleton）

1. 判定路线（folder / code / doc，可串联）。
2. 扫描目标范围，输出 `plan.md`（现状描述 + 问题清单 + 建议变更 + 影响面）。
3. 对于 `folder-tidy`：附 `dry-run-diff.patch`（mv 模拟）。对于 `code-structure`：可委托架构师 agent 出深度报告。对于 `doc-structure`：附三原则违规清单。
4. 等用户显式确认后才接力下游执行；本 Skill v0.1.0-skeleton 不自己 mv / 改文件。
5. 落地后接 `ccg:verify-*` 复检；结果回写 `_work/struct_runs/<id>/result.md`。

## 当前待澄清（按 plans/009）

升 ready 必拍：1（偏好持久化路径）/ 2（--apply 是否允许）/ 4（三原则规则集编码方式）/ 5（语言专属规则集）。
其余 3 / 6 / 7 / 8 可后续单独拍板，不阻塞 skeleton 可用。
