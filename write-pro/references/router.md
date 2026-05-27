# write-pro · L1 路由（v0.1.0-skeleton）

> 父级：[../SKILL.md](../SKILL.md)
> 立项档：[../../../plans/010-new-skill-write-pro.md](../../../plans/010-new-skill-write-pro.md)

## 判定顺序（按文体；plans/010 Q1 待拍板是否改按受众/平台）

| 优先级 | Route | 命中条件 |
|---|---|---|
| 1 | `engineering-doc` | PR description / commit message / 内部教程 / API 文档（非项目骨架）/ 模块说明（非完整 README） |
| 2 | `commercial-copy` | Landing 文案 / 邮件营销 / 商品描述 / 广告语 / 转化文案 |
| 3 | `short-form` | 推特 / 朋友圈 / 标语 / 短简介 / 评论 |
| 4 | `long-form`（fallback） | 公众号长文 / 技术博客 / 行业研究 / 案例分析 / 长文体杂文 |

边界优先：用户说"帮我写 README" / "帮我写项目说明" → 转 `ccg:gen-docs`（Q7 待最终拍板）。

## 全局 `pro-*` 原子调用矩阵（v0.1.0-skeleton）

| 路线 | 顺序 | 原子 | 作用 |
|---|---|---|---|
| `long-form` | 1 | `pro-idea` | 选题立意 / 角度筛选 |
|  | 2 | `pro-struct` | 长文结构 / 大纲 / 章节切分 |
|  | 3 | `pro-exp` 或 `pro-explain` | 经验体（叙事重）vs 讲解体（清晰重），按读者类型择一 |
|  | 4 | `pro-summary` | 收尾 / 金句 / 行动召唤 |
| `short-form` | 1 | `pro-idea` | 钩子 / 槽点 / 反差点 |
|  | 2 | `pro-copy` | 短文文案打磨（字数 / 节奏 / 拆句） |
|  | 3 | `pro-must` | 必须保留的关键信息（链接 / 标签 / 提及） |
| `commercial-copy` | 1 | `pro-copy` | 主文案打磨 |
|  | 2 | `pro-must` | 必须保留的卖点 / CTA / 信任锚 |
|  | 3 | `pro-rule` | 平台规则 / 合规 / 字数限制 / 投放规范 |
| `engineering-doc` | 1 | `pro-struct` | 文档结构（动机 / 现状 / 方案 / 影响面 / 验证） |
|  | 2 | `pro-explain` | 讲解（让不在场的同事看得懂） |
|  | 3 | `pro-summary` | TL;DR / 摘要 / commit subject |

实际调用时按用户语境裁剪：不是每条都必须串完，最少必经原子 ≥1 个。

## 三段式产出

```
_work/writing_runs/2026-05-27-1700-tech-blog-rag-design/
├─ outline.md   ← 立意 + 结构 + 受众假设 + 个人风格 prompt 快照
├─ draft.md     ← 初稿（含 anti-slop critique 第一轮回应）
└─ final.md     ← 终稿（critique 全部通过）
```

## Anti-AI-slop critique（强制）

每条路线 draft → final 之前必须回答（≥3 条具体）：

1. 这篇有什么是**只有这位用户**能写出来的？
2. 拿掉品牌名 / 项目名后，还能**认得出**是谁写的吗？
3. 有没有一个**具体到刺眼**的细节是不可替换的？
4. 有没有泛泛的"赋能 / 闭环 / 抓手"类大词没洗净？

不通过则回 draft 迭代，**不允许直接交付**。

## 个人风格偏好（v0.1.0-skeleton 占位）

S1 路由阶段读取 / 询问：

- 语气（理性 / 自嘲 / 冷感 / 热血）
- 句长偏好（短促 / 长句嵌套）
- 人称（第一 / 第二 / 第三）
- 口头禅 / 高频用词
- 忌讳词（再也不想看到的词）

持久化路径 plans/010 Q4 待拍板（候选：项目级 `.write-pro.yaml` / 全局 `~/.write-pro/style.yaml` / 与 struct-pro 共用偏好层）。

## 与其他 *-pro / 全局 Skill 的衔接

- 写完转 deck → `ppt-gen-pro`
- 写完转网页 → `html-gen-pro`
- 写完发布到飞书/Notion/邮件 → `office-pro`
- 写之前要找资料 → `search-pro`
- 项目 README/DESIGN 骨架 → `ccg:gen-docs`
- 单点修辞改写 → 直接对应 `pro-*`

## 未来扩展（plans/010 待澄清）

- Q1：主路线切法 — 如果改按受众/平台，重写本路由判定表
- Q2：中英双语 — 拍板后或新增独立路线、或在每条路线内 v0.1.0-skeleton 双输出
- Q3：内置推送渠道 — 拍板后或纳入本 Skill、或一律走 office-pro
- Q5：严肃写作（学术/政策/法律/招投标）— 拍板后新增路线 `serious-form`
- Q6：个性化语料库（用户过往作品 → embedding 引用风格）— 拍板后新增 references 与 ingestion 流程
