# struct-pro · L1 路由（v0.1.0-skeleton）

> 父级：[../SKILL.md](../SKILL.md)
> 立项档：[../../../plans/009-new-skill-struct-pro.md](../../../plans/009-new-skill-struct-pro.md)

## 判定顺序

| 优先级 | Route | 命中条件 |
|---|---|---|
| 1 | `doc-structure` | 用户提到 README / DESIGN / 索引 / 单一信息源 / 文档体系 / "文档好乱" |
| 2 | `code-structure` | 用户提到组件化 / 模块拆分 / 接口 / 重构 / "这块代码结构怎么改" |
| 3 | `folder-tidy` | 用户提到目录乱 / 文件归档 / 命名漂移 / "整理一下这个目录" |
| — | 多路串联 | 大型整改一般 doc → code → folder 或反向，串联时每条都走 dry-run |

## `folder-tidy` 路线

- 输入：目标根目录 / 范围（可多个）
- 扫描项：命名风格一致性 / 目录深度 / 同名概念散落 / 孤儿文件 / 留痕缺失
- 输出：`plan.md`（变更列表） + `dry-run-diff.patch`（git mv 模拟）
- 落地：用户确认后调 `git mv`；跨独立子仓库的移动 v0.1.0 禁用（Q7 待拍）
- 复检：可选接 `ccg:verify-module`

## `code-structure` 路线

- 输入：目标模块 / 文件 / 目录
- 扫描项：
  - 组件化：UI/逻辑/数据分层是否混淆
  - 模块化：模块边界是否清晰、是否泄露内部状态
  - 接口对接口：跨模块调用是否走显式 interface / contract
  - 可维护：圈复杂度 / 重复代码 / 命名
  - 可复用：是否绑定具体业务、是否容易抽出
  - 可扩展：扩展点是否显式
- 委托：深度评估可 spawn 全局 `init-architect` 或 `team-architect` agent
- 语言专属规则集：v0.1.0 暂用通用启发式；按语言落地待 Q5 拍板
- 落地：仅出建议 `plan.md`，重构本身由用户或下游 agent 执行
- 复检：接 `ccg:verify-quality`

## `doc-structure` 路线

- 输入：项目 / 模块 / 工作区根
- 扫描项（三原则编码 TBD，Q4 待拍板）：
  - 单一信息源违规 — 同一概念在 ≥2 处实质重复（非链回）
  - 层层索引缺失 — ≥2 个子模块的目录缺 README 索引
  - 信息一致性违规 — frontmatter `name` / 索引行 / 正文标题字面不一致
- 三层受众检查：
  - AI 记忆层（`CLAUDE.md` / `AGENT.md` / `.ccg/memory`）是否齐备
  - AI 解析层（`skill.json` / frontmatter / 结构化 index）是否齐备
  - 人类阅读层（`README.md` / `DESIGN.md`）是否齐备
- 输出：`plan.md`（三原则违规清单 + 三层受众缺漏 + 建议补全清单）
- 接力：补骨架走 `ccg:gen-docs`；补完走 `ccg:verify-module`

## 用户偏好持久化（v0.1.0-skeleton 占位）

- 候选路径（plans/009 Q1 待拍）：
  - 项目级 `.struct-pro.yaml`（项目根，与 `.ccg/` 同级）
  - 全局 `~/.struct-pro/preferences.yaml`
  - 两层叠加（项目覆盖全局）
- 偏好项（候选）：命名风格（kebab/snake/camel）、目录深度上限、文档骨架模板偏好、是否倾向 monorepo、跨仓库 mv 允许度。

## 产物归宿

`_work/struct_runs/<timestamp>-<intent>/`：

```
_work/struct_runs/2026-05-27-1600-doc-three-principles-audit/
├─ plan.md            ← 现状 / 问题 / 建议 / 影响面
├─ dry-run-diff.patch ← 仅 folder-tidy 有
└─ violations.json    ← 仅 doc-structure 有，机器可读违规清单
```

## 未来扩展（plans/009 待澄清）

- Q1：偏好持久化路径 — 拍板后落 `references/preferences.md` + 加载逻辑
- Q2：`--apply` 是否允许 — 拍板后定 CLI 入参契约
- Q4：三原则规则集编码 — 拍板后落 `references/principles.md`（JSON Schema / regex 表 / NL rules 之一）
- Q5：语言专属规则集 — 拍板后落 `references/code/python.md` / `typescript.md` / `rust.md` / `go.md`
- Q6：三层受众最小骨架模板 — 拍板后落 `references/templates/{ai-memory,ai-parse,human-read}.md`
