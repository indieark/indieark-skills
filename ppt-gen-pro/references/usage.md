# Usage Path

Load when: 用户已经触发 PPT 生成意图，需要从 `ppt-gen-pro` 路由到某个外部扩展。
Avoid: 不要绕过选择门；不要把 `extensions/` 当作 vendored 源码提交。
Pairs with: `route-introduction.md`, `router.md`, `install.md`, `extensions.md`, `reporting.md`

## One-Line Contract

`ppt-gen-pro` 只负责强触发、标准介绍、路线推荐、安装检查、用户选择和委托；真实生成必须进入用户确认后的外部扩展 Skill 入口。

## Runtime Sequence

每次用户要生成真实 PPT / slides / deck 时，按这个顺序执行：

1. 识别为 `generation-request`，先触发 `ppt-gen-pro`，不要让任一外部 PPT Skill 直接抢跑。
2. 读取 `route-introduction.md`，用标准介绍说明图片 PPT、网页 PPT、SVG PPT 三种路线。
3. 读取 `router.md`，根据用户目标推荐一条路线，并让用户回复 `1 / 2 / 3` 或“按推荐来”。
4. 读取 `install.md`，运行安装检查。若选定路线缺失或 stale，运行对应 route 的 install-or-update。
5. 用户选择或接受推荐后，读取 `extensions.md` 中对应 route 的 Skill 入口路径。
6. 打开对应外部 Skill 的 `SKILL.md`，遵守外部 Skill 自己的工作流、确认门、输出路径和验证规则。
7. 完成后按 `reporting.md` 汇报：选择路线、外部 Skill、安装状态、输出路径、预览/检查结果和验证。

## Route To Entry Map

| Route | Install checkout | Runtime Skill entry | When to open |
| ---- | ---- | ---- | ---- |
| `image-first-ppt` | `extensions/ppt-image-first` | `extensions/ppt-image-first/SKILL.md` | 用户选择图片 PPT，或接受标准 PPT 默认推荐后 |
| `web-html-ppt` | `extensions/guizang-ppt-skill` | `extensions/guizang-ppt-skill/SKILL.md` | 用户选择网页 PPT，或需求明显是演讲、主文字、动效、单文件 HTML 后 |
| `svg-ppt` | `extensions/ppt-master` | `extensions/ppt-master/skills/ppt-master/SKILL.md` | 用户选择 SVG / 可编辑 PPT，或明确要求原生可编辑 PPTX、PowerPoint shapes、原生动画后 |
| `academic-image-ppt` | `extensions/literature-report-ppt-builder` | `extensions/literature-report-ppt-builder/academic-slide-minimalist/SKILL.md` | 用户提到论文、文献汇报、组会、journal club、答辩、SI、课题汇报 → router.md §0 命中后直接进入 |

## Install Check Commands

生成前最小检查：

```powershell
python scripts\install_extensions.py --check-only --format json
```

只修复选定路线：

```powershell
python scripts\install_extensions.py --route image-first-ppt
python scripts\install_extensions.py --route web-html-ppt
python scripts\install_extensions.py --route svg-ppt
python scripts\install_extensions.py --route academic-image-ppt
```

首次安装或统一刷新三路：

```powershell
python scripts\install_extensions.py
```

检查输出里的 `skill_entry` 字段就是后续要读取的外部 Skill 入口。不要猜外部 Skill 路径，也不要根据仓库名推断入口；尤其 `ppt-master` 的入口在 `skills/ppt-master/SKILL.md`。

## Recommendation Discipline

- 用户请求命中论文 / 文献汇报 / 组会 / journal club / 答辩 / SI / supplementary / 课题汇报 / paper / 课程文献等触发词：先走 `academic-image-ppt`，跳过通用菜单（见 `router.md` §0）。
- 不确定时推荐 `image-first-ppt`，因为普通 PPT 首先需要稳定的视觉交付。
- 讲稿、演讲、主文字、动效、网页展示和单文件 HTML 推荐 `web-html-ppt`。
- 只有可编辑、原生 PPTX、PowerPoint shapes、原生动画或对象级修改是硬需求时，才推荐 `svg-ppt`。
- 用户同时要“好看”和“可编辑”时，先说明取舍，再让用户决定优先级；若用户不表态，按图片 PPT 继续。
- 用户已明确选择某路线后，不要再反复劝说；直接检查安装并进入对应 Skill。

## Do Not

- 不要在用户未选择或接受推荐前进入外部 Skill。
- 不要把三个上游仓库的代码复制进 `skills/ppt-gen-pro/`。
- 不要删除 `extensions/*/.git`；这会破坏自动更新。
- 不要用 `npx skills add` 的安装产物替代本仓库的完整 checkout，除非项目后续明确切到 skill-manager 安装方案。
