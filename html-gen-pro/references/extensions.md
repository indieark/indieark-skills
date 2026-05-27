# Extensions

Load when: 需要说明外部 extension 来源 / 安装 / 委托边界 / 路线角色。
Avoid: 不要复制外部仓库代码到本 Skill；不要绕过 route gate；不要在 `existing-project-optimize` 路线下委托 extension。
Pairs with: `router.md`, `install.md`, `capability-matrix.md`, `usage.md`

## Extension Registry

| Route | Source | Local checkout | Runtime Skill entry | locked_commit | verified_date |
| ---- | ---- | ---- | ---- | ---- | ---- |
| `landing-page` / `app-frontend` / `style-mockup` | `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill` | `extensions/ui-ux-pro-max` | `extensions/ui-ux-pro-max/CLAUDE.md` | `b7e3af8` | `2026-05-26` |
| `style-mockup` | `https://github.com/Leonxlnx/taste-skill` | `extensions/taste-skill` | `extensions/taste-skill/README.md`（child Skill 入口见 `skills/<child>/SKILL.md`）| `3c7017d` | `2026-05-27` |
| `existing-project-optimize` | **不绑** extension | — | — | — | — |

- `locked_commit`：该 extension 上次验证通过后锁定的 Git commit SHA（短 7 位即可）。填写后，安装脚本应 `git checkout <locked_commit>` 而不是 pull 到 latest；`(unset)` 表示跟随 upstream default branch。
- `verified_date`：上次人工端到端验证该 extension 与 html-gen-pro router 兼容性的日期（`YYYY-MM-DD`）；`(unverified)` 表示尚未完成首次验证。
- `ui-ux-pro-max` Runtime Skill entry = `extensions/ui-ux-pro-max/CLAUDE.md`（首次端到端验证已确认；upstream 是 multi-skill collection 包，实际搜索能力靠 `extensions/ui-ux-pro-max/src/ui-ux-pro-max/scripts/search.py`）。
- `taste-skill` Runtime Skill entry = `extensions/taste-skill/README.md`（含 9 子 Skill 注册表）；S4 委托时按美学方向打开对应子 Skill：brutalist / swiss → `skills/brutalist-skill/SKILL.md`；luxury(soft) → `skills/soft-skill/SKILL.md`。其余子 Skill（`minimalist-skill` / `redesign-skill` / `brandkit` 等）不在本 extension 化范围内，redesign-skill + brandkit 保留为 [`boundary.md`](boundary.md) §6 接力关系。

## Route Roles

`ui-ux-pro-max` 同时服务 3 条路线（landing-page / app-frontend / style-mockup），靠 prompt 切换模式；`taste-skill` 只在 `style-mockup` 路线作为风格分流的第 2 选择。委托时显式声明所在路线：

### `landing-page`

Use `ui-ux-pro-max` 当用户要做对外门面独立网页（Landing / 营销页 / Pricing / 活动页 / Changelog / 个人主页）。核心价值：

- **161 industry rules**：覆盖 SaaS / 电商 / 内容 / 工具 / 教育 / 医疗 / 金融 / 房产 / 招聘 等行业的版式与文案套路。
- **67 styles + 161 palettes + 57 font pairings**：视觉系统素材库。
- **预交付 checklist + section-by-section playbook**：营销页 hero / features / pricing / testimonial / cta 等段落的标准产出指引。

### `app-frontend`

Use `ui-ux-pro-max` 当用户要做工具型 UI（Dashboard / Admin / Web App / 组件库 mockup）。核心价值：

- **99 UX guidelines**：信息密度、导航、空状态、错误反馈、可访问性的成体系规则。
- **设计系统生成器**：让你能产出可重复使用的 design token + 组件 spec。
- 与 `landing-page` 同一套素材库，但调用模式偏 UX guidelines + 设计系统而非 industry rules。

### `style-mockup`

本路线**双 extension 并列**：`ui-ux-pro-max` 提供 67 styles 广覆盖，`taste-skill` 提供少数风格的深度立场。S4 委托时按美学方向选取：

#### `ui-ux-pro-max`（默认 / 广覆盖）

Use `ui-ux-pro-max` 当用户要把某个具体风格落到可运行 HTML mockup，**且该风格在 67 styles 库内有现成规则**：

- **67 styles**：claymorphism / glassmorphism / liquid-glass / neubrutalism / magazine / editorial / 杂志风 / 终端风 / Y2K / cyber / vaporwave 等。
- **161 palettes + 57 font pairings**：与风格搭配的配色与字体对。
- 适合"探索性风格 mockup / 快速风格切换 / 同一份内容多风格对比"。

#### `taste-skill`（深度立场 / 风格空缺填补）

Use `taste-skill` 当美学方向落到下列**社区已用单 Skill 做出深度立场**的方向（taste-skill 在这些风格上比 ui-ux-pro-max 的素材库立场更鲜明、机械感与排版细节更激进）：

- **brutalist / swiss** → 委托 `extensions/taste-skill/skills/brutalist-skill/SKILL.md`（hard mechanical + Swiss type + 锐对比 + 1-10 dials 可调 DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY）。
- **luxury(soft / calm-premium)** → 委托 `extensions/taste-skill/skills/soft-skill/SKILL.md`（softer contrast + spring motion + calm-premium 气质，与 ui-ux-pro-max 的 luxury 模板差异化）。
- 不适用：`minimalist-skill` 在本仓库 v0.2.0-post-fuse 范围外（未登记到 styles.md 路标），用户点名 minimalist 时仍走 ui-ux-pro-max 67 styles。

**取舍规则**：

- 默认 ui-ux-pro-max（覆盖广，与 landing-page / app-frontend 同一套素材）。
- 命中 brutalist / swiss / luxury(soft) 三类气质关键词时，**优先 taste-skill** 对应子 Skill（避免 67 styles 库在这 3 个空缺方向的"通用感"）。
- 不允许同一次执行混用两个 extension——选一个、跑完五段流程；混用会破坏五维 critique 的"差异化记忆点"维度。

### `existing-project-optimize` — **不绑** extension

理由：本路线的核心是"跟随项目原生栈"，外部素材库（industry rules / palettes / font pairings）反而是负担，会引入与项目设计系统冲突的元素。

只走本仓库方法论：
- [`workflow.md`](workflow.md) 美学方向门 + 五段流程
- [`critique.md`](critique.md) 五维 critique
- [`styles.md`](styles.md) 反 AI slop 立场
- [`boundary.md`](boundary.md) 边界（不擅自改业务逻辑 / API / 路由表）
- [`cases.md`](cases.md) IndieArk 内部前端项目接入注意事项
- [`../../../templates/existing-project-optimize-checklist.md`](../../../templates/existing-project-optimize-checklist.md) 接入前 checklist

## 版本锁定

`scripts/install_extensions.py`（Phase 3 起）是 lock/freshness 的真源：

- 表中 `locked_commit` 和 `verified_date` 是给人/Agent 看的镜像，**真值写在 `scripts/install_extensions.py` 的 `EXTENSIONS` 列表里**。
- 验证 extension 兼容性后必须同时更新两处，避免脱节。

### 默认行为

不带标志运行 `python scripts/install_extensions.py` 时，所有 route 都跟随 upstream default branch（`git pull --ff-only`）。用户安装/更新时拿到的是上游最新提交，`locked_commit` 不参与。

### 工作流标志

| 场景 | 命令 | 行为 |
| ---- | ---- | ---- |
| 开发、想吃 upstream 最新 | `python scripts/install_extensions.py` | clone --depth 1 或 git pull --ff-only |
| CI / 发版要可复现 | `python scripts/install_extensions.py --locked` | 按 EXTENSIONS 中 `locked_commit` 做 fetch + checkout；未填的 route 仍跟 latest |
| 升级 lock 到当前 upstream | `python scripts/install_extensions.py --update-lock` | 先 git pull --ff-only，然后输出当前 commit SHA + 今天日期，由你手动写回 EXTENSIONS 和本表 |
| 检查 lock 新鲜度 | `python scripts/install_extensions.py --check-freshness` | 列出 `verified_date` 缺失或距今 > 90 天的 route（stderr WARN，不阻塞退出码） |
| 检查环境 Python 版本 | `python scripts/install_extensions.py --check-only` | 同时调用 `python --version` 与目录存在性校验，但 warn-only 不安装 |

### 锁定规则

- extension upstream 有 breaking change 前，`locked_commit` 保持不变；`--locked` 安装时使用该 commit 而不是 `git pull`。
- 需要跟进 upstream 时，先在测试环境跑 `--update-lock` 拿新 SHA → 端到端验证新 commit 兼容 → 把 SHA 和当日日期写回 EXTENSIONS + 本表。
- 若 `verified_date` 距今超过 90 天，进入 Skill 工作流前建议先重新验证；Agent 应在委托前调用 `--check-freshness` 并提示用户。
- `--update-lock` 不会自动改本 Markdown 表格，避免脚本破坏表格格式；脚本只输出建议值，由人手动落字。

## Update Contract

- `extensions/` 存放 live Git checkout，不复制 snapshot 到本仓库。
- 保留每个 extension 的 `.git` 目录，让它保持可更新。
- 重复运行 `python scripts/install_extensions.py` 通过 `git pull --ff-only` 更新现有 checkout。
- 不要让用户手动逐个 pull 上游 extension，除非自动更新失败且错误需人工处理。
- 使用 `Local checkout` 路径做更新与源码巡检；使用 `Runtime Skill entry` 路径在用户选择路线后做委托。
- `extensions/` 在本仓库 `.gitignore` 内（Phase 3 起），**不提交**到本仓库。

## Delegation Contract

- `html-gen-pro` 掌管 trigger / recommendation / user choice / **美学方向门** / **五维 critique** / installation check / final reporting。
- 选中的 extension（ui-ux-pro-max）掌管自己内部的素材库调用与具体生成机制。
- 路线选择后，打开**正好**对应路线的 `Runtime Skill entry`；不要根据仓库名猜路径。
- 不要在一次执行里混用两条路线，除非用户明确要求混合工作流。
- 如 extension 缺失或 stale，先安装或更新再委托。
- `existing-project-optimize` 路线下**禁止**调用 extension（参见 Route Roles 说明）。
