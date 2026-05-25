# Flows (L3 引导流程状态机)

Load when: 需要把"路由 → 介绍选择 → 引导流程"三段串成可执行状态机，或排查用户在哪个状态卡住。
Avoid: 不要在本文件复制路由触发词或路线介绍文案（真源在 `router.md` / `route-introduction.md` / `post-processes.md`）；本文件只描述状态机和跨阶段交接。
Pairs with: `router.md`, `route-introduction.md`, `extensions.md`, `post-processes.md`, `capability-matrix.md`

## 三阶段状态机

```
┌─────────────────┐    L1 触发词 + 通用菜单    ┌──────────────────────┐    用户选定 L1     ┌─────────────────────┐
│   S0 · 路由     │ ─────────────────────────▶ │   S1 · 介绍选择        │ ─────────────────▶ │   S2 · 引导流程       │
│  (router.md)    │                            │  (route-introduction)  │                    │   (extension SKILL)   │
└─────────────────┘                            └──────────────────────┘                    └─────────────────────┘
        │                                                 │                                            │
        │ L2 触发词命中                                   │ L2 触发词命中                              │ L1 完成后
        ▼                                                 ▼                                            ▼
                                              [附加 L2 选项预览]                            [询问是否进入 L2]
                                              (post-processes.md)                          (post-processes.md)
```

## S0 · 路由（router.md）

**输入**：用户的 generation-request 自然语言。

**判定顺序**（与 `router.md` Recommendation Rule 完全一致）：

1. §0 领域特化优先（命中即直推，跳过通用菜单）：
   - `academic-image-ppt` ← 论文 / 文献汇报 / 组会 / journal club / 答辩 / SI / supplementary / 课题汇报 / paper / 课程文献 / 文献阅读 / 主文图 / 文献讲解
   - 例外：用户显式 opt-out（"虽然是论文但只要好看"）→ 回退通用菜单
2. 通用 4 选 1，判定顺序 `svg → design → web → image-first 默认`：
   - `svg-ppt`：可编辑 / 原生 PPT 对象 / 多人编辑 / 原生动画 / SVG/PPTX 工程化
   - `design-html-ppt`：高保真原型 / mockup / 设计稿 / launch film / motion design / MP4 导出 / 原生 PPTX 导出 / PDF 导出 / 豆包 TTS
   - `web-html-ppt`：主文字 / 演讲 / 讲稿 / 叙事 / 动效 / 单文件 HTML / 杂志风 / 瑞士风
   - `image-first-ppt`：默认 / 标准 PPT / 普通汇报

**L2 预扫描**：S0 完成后 router 同时扫一遍 L2 触发词（见 `post-processes.md`「触发模型」），结果作为 hint 带入 S1。

**输出**：`{l1_route, l2_preview, recommendation_sentence}`。

## S1 · 介绍选择（route-introduction.md）

**输入**：S0 的 `{l1_route, l2_preview, recommendation_sentence}`。

**呈现规则**：

- 学术领域命中（S0 §0）：直接给学术专用话术，**不展示** 通用 4 选 1 菜单。
- 通用 4 路线推荐：展示 4 选 1 菜单 + 推荐句 + 取舍提示。
- L2 预览（仅当 `l2_preview` 非空）：在 L1 选项旁附加一段说明，提示用户 L1 完成后可进入 L2。

**用户响应面**：

| 用户回复 | 解释 |
|---|---|
| `1` / `2` / `3` / `4` | 通用菜单选定 L1 |
| `按推荐来` / `好的`（接受推荐） | L1 = `recommendation_sentence` 指向的路线 |
| 重新表达需求 | 退回 S0 重新判定 |
| 明确拒绝学术专线 | 学术 §0 命中时切回通用菜单 |

**输出**：`{l1_route_confirmed, l2_preview}` → 进入 S2。

## S2 · 引导流程（committee to selected extension）

**输入**：S1 确认的 L1 路线 + L2 预览状态。

**职责切换**：S2 进入后，ppt-gen-pro 的职责从「推荐 / 路由」切换为「**执行委托**」。具体生成机制由扩展自己的 SKILL.md 负责。

**入口选择**：

| L1 路线 | Runtime Skill entry |
|---|---|
| `image-first-ppt` | `extensions/ppt-image-first/SKILL.md` |
| `web-html-ppt` | `extensions/guizang-ppt-skill/SKILL.md` |
| `design-html-ppt` | `extensions/huashu-design/SKILL.md` |
| `svg-ppt` | `extensions/ppt-master/skills/ppt-master/SKILL.md` |
| `academic-image-ppt` | `extensions/literature-report-ppt-builder/academic-slide-minimalist/SKILL.md` |

**L2 转交时机**：

- L1 完成且 `l2_preview` 非空 → 询问"是否进入 L2 后操作（如视频化 / 录屏）"。
- 用户接受 → 切到 `extensions/garden-skills/skills/web-video-presentation/SKILL.md`（仅 web-html-ppt 路线可达）。
- 用户拒绝 → ppt-gen-pro 走 reporting.md 收尾。

**输出**：交付物（PPTX / HTML / MP4 / PDF）+ 路由审计摘要（按 `reporting.md` 标准）。

## 状态间约束

1. **S0 不直接跳 S2**：必须经过 S1 让用户确认或显式 opt-in 推荐。学术 §0 也要在 S1 给用户撤回机会。
2. **S1 不绕过 S0**：用户不能直接说"用 design-html-ppt"跳过 S0 判定 — 路由触发词必须落到 router.md 真源；但用户显式点名路线时 S0 视为"触发命中即推荐"。
3. **L2 不可独立达成**：S0/S1 都不会单独给出 L2，必须挂在 L1 路线之下。
4. **跨路线切换重启状态机**：用户在 S2 中途要切换路线，必须回到 S1 重新选定；ppt-gen-pro 不在 S2 内做横切。

## 与现有 reporting.md 的衔接

S2 完成后必须按 `reporting.md` 报告路由结果，至少包含：

- 选定的 L1 路线 + 触发原因
- 是否进入了 L2（若是，L2 名称 + 触发原因）
- 上游扩展的 `locked_commit` / `verified_date`
- 交付物清单

## 维护契约

- 新增 L1 路线时：S0 加触发词 + S1 菜单加项 + S2 入口表加行。
- 新增 L2 后操作时：S0 L2 预扫描表加触发词 + S2 转交时机加分支 + 同步 `post-processes.md`。
- 状态机改动时：先改本文件，再同步 `scripts/test_router.py` 的状态断言；router dry-run 应覆盖每个状态间转移。
