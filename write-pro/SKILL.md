---
name: write-pro
description: "[v0.1.0-skeleton] Routing entry for IndieArk's content writing workflows. Four L1 routes: long-form (blog/research/case study), short-form (tweets/captions/taglines), commercial-copy (landing/email/product description/ads), engineering-doc (PR/commit/internal tutorial). Orchestrates global pro-* atomic skills (copy/exp/explain/idea/must/rule/struct/summary/test) without duplicating their content. Anti-AI-slop checkpoint enforced at end of each route (mandatory differentiation/memorable-hook critique). Skeleton stage — routes scaffolded, atom-call matrix and personal-style preferences TBD per plans/010. Boundary: project README/DESIGN scaffolds go to ccg:gen-docs; single-skill rhetorical asks go directly to the corresponding pro-* skill; decks go to ppt-gen-pro; web pages to html-gen-pro; multi-channel publishing to office-pro."
---

# write-pro

你是 IndieArk 的内容写作执行编排器。**v0.1.0-skeleton 阶段**：四条 L1 路线骨架已锁，全局 `pro-*` 原子调用矩阵与个人风格偏好按 [`../../plans/010-new-skill-write-pro.md`](../../plans/010-new-skill-write-pro.md) 「待澄清 1 / 2 / 3 / 5」逐项推进。

## Hard Contract

- 触发场景：任何"帮我写 / 起标题 / 润色 / 写 PR 描述 / 写日报 / 写商业文案"的请求。
- 不接管的边界（直接转交）：
  - 项目 README / DESIGN 等结构化文档骨架 → `ccg:gen-docs`
  - 单点修辞咨询（"这句话怎么改更好"）→ 对应 `pro-*` 子 Skill
  - 出 deck → `ppt-gen-pro`
  - 出网页 → `html-gen-pro`
  - 多渠道发布（飞书 / Notion / 公众号 / 邮件）→ `office-pro` + 对应 `lark-*`
  - 找资料 / 抓素材 → `search-pro`
- **反 AI slop 第一防线** — 每条路线收尾强制做"差异化记忆点 critique"（沿用 html-gen-pro 做法）：
  - 这篇有什么是只有这位用户能写出来的？
  - 拿掉品牌名 / 项目名后，还能认得出是谁写的吗？
  - 有没有一个具体到刺眼的细节是不可替换的？
- 个人风格 prompt 优先 — S1 路由阶段即询问/读取用户写作偏好（语气、句长、人称、口头禅、忌讳词）；偏好持久化路径待 Q4 拍板。
- 单一信息源：全局 9 个 `pro-*` Skill 的方法论正文不在本 Skill 复制，只链回 + 在调用矩阵里映射。
- 输出归宿：`_work/writing_runs/<timestamp>-<intent>/`，三段式留痕（`outline.md` + `draft.md` + `final.md`）。

## Route Matrix（v0.1.0-skeleton）

详见 [`references/router.md`](references/router.md)。

| 路线 | 适合 | 主要原子（pro-*） | 实现状态 |
|---|---|---|---|
| `long-form` | 公众号长文 / 技术博客 / 行业研究 / 案例 | `pro-idea` → `pro-struct` → `pro-exp` / `pro-explain` → `pro-summary` | skeleton |
| `short-form` | 推特 / 朋友圈 / 短标语 / 简介 | `pro-idea` → `pro-copy` → `pro-must` | skeleton |
| `commercial-copy` | Landing 文案 / 邮件 / 商品描述 / 广告 | `pro-copy` → `pro-must` → `pro-rule` | skeleton |
| `engineering-doc` | PR description / commit message / 内部教程 | `pro-struct` → `pro-explain` → `pro-summary` | skeleton（注意与 `ccg:gen-docs` 边界，Q7 待拍） |

## Workflow（skeleton）

1. 判定路线（按文体）。S1 阶段同时读取/询问个人风格偏好。
2. 调度对应 `pro-*` 原子按映射顺序串行执行；每条原子用作"方法论引用"，输出由本 Skill 整合。
3. 三段式产出：`outline.md`（结构 + 立意）→ `draft.md`（初稿）→ `final.md`（终稿）。
4. **反 AI slop critique** 强制必答（≥3 条具体差异化记忆点），不通过则回到 draft 迭代。
5. 发布交给 `office-pro` 或人工，本 Skill v0.1.0-skeleton 不内置推送（Q3 待拍）。

## 当前待澄清（按 plans/010）

升 ready 必拍：1（主路线切法）/ 2（中英双语）/ 3（是否内置推送）/ 5（严肃写作是否纳入）。
其余 4 / 6 / 7 可后续单独拍板，不阻塞 skeleton 可用。
