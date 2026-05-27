# Cases · IndieArk 内部前端项目案例

Load when: 路由判定指向 `existing-project-optimize` / 用户提到 IndieArk 子项目名 / 需要查"这个项目能改什么 / 不能改什么 / 立场要点是什么"。
Avoid: 不要把本表当成"项目当前实现状态"的真源——状态以各项目仓库的实际代码为准；本文件只描述**接入立场**与**改动范围**。
Pairs with: `route-introduction.md`, `router.md`, `extensions.md`, `capability-matrix.md`, [`../../../templates/existing-project-optimize-checklist.md`](../../../templates/existing-project-optimize-checklist.md)

> **正源边界**：项目列表 / 端口 / 状态以 [`../../../../../PROJECTS.md`](../../../../../PROJECTS.md) 为权威；本文件只补"前端层接入注意事项"，不复制端口表 / 状态字段。

## 适用路线一览

| 项目目录 | 推荐路线 | 是否绑定 extension |
| ---- | ---- | ---- |
| `1-showcase/` | `existing-project-optimize` | 否 |
| `20009-feedback/` | `existing-project-optimize` | 否 |
| `20013-hot/` | `existing-project-optimize` | 否 |
| `20005-aigc/` | `existing-project-optimize` | 否 |
| `20007-review/` | `existing-project-optimize` | 否 |
| `0-steamworks/`（GitHub `20029-steamworks`） | `existing-project-optimize` | 否 |
| `gadget/Indieark_steam_design/` | `existing-project-optimize` | 否 |
| 其他含前端的业务项目 | `existing-project-optimize`（默认） | 否 |

`existing-project-optimize` 路线统一**不绑** extension（详见 [`extensions.md`](extensions.md)）：项目已有自己的设计系统、组件库、栈选择，外部素材库反而是干扰。

## 项目级立场要点

### `1-showcase/` — IndieArk 官方展示站

**项目定位**：多主题静态官网，使用 CSS Custom Properties 做主题切换。

**可改**：

- 任一主题的视觉细节（typography、palette、间距、组件样式）。
- 新增主题（保持 CSS Custom Properties 切换契约）。
- 首页 / 关于 / 项目展示页的版式与信息层级。
- 静态资源（图标、插画、字体）替换。

**不可改（需用户书面确认）**：

- 主题切换机制（CSS Custom Properties 体系本身）。
- 路由 / 多页结构 / SEO meta 配置。
- 部署脚本 / 构建管线。

**接入注意**：

- 这是 IndieArk **门面**项目；做风格改动前先在 S3 明确"这次是单主题深耕"还是"新增主题"。
- 改动前先 `cat 1-showcase/README.md` 看当前主题清单，避免覆盖现有主题的 token。
- 多主题站点天然适合做 `style-mockup` 路线 cross-pollination，但**不要**把 mockup 直接 paste 进 1-showcase——先按主题契约改造。

### `20009-feedback/` — Steam 游戏评论跟踪/回复

**项目定位**：工具型 Dashboard（评论列表 + 筛选 + 回复工作流）。

**可改**：

- 列表 / 卡片 / 筛选器的视觉与信息密度。
- 状态徽章、reaction 组件的视觉。
- 空状态 / loading / error 状态的呈现。
- 响应式断点（移动端浏览体验）。

**不可改（需用户书面确认）**：

- 数据获取逻辑（Steam API 调用、轮询、缓存）。
- 飞书推送 / 回复入队逻辑。
- 状态管理结构（评论状态机本身）。

**接入注意**：

- 这是工具型 UI，遵守 [`capability-matrix.md`](capability-matrix.md) 中 `app-frontend` 的工程标准（响应式、a11y、键盘导航），但路线**还是** `existing-project-optimize`（不调用 ui-ux-pro-max 的 99 UX guidelines 套版，而是改本项目原生组件）。
- reaction 组件是该项目特色资产，**可以**作为其他路线（如 `landing-page`）的 inspiration 参考，但不要从 feedback 仓库 import 进新项目——抽提到 `00000-model/01 复用资产/` 才是正确路径。

### `20013-hot/` — 飞书群聊 24h 热搜资讯 bot

**项目定位**：含 SteamUI 风格（Glassmorphism 暗色）的资讯展示页。

**可改**：

- Glassmorphism 视觉参数（blur、透明度、边框、阴影）。
- 资讯卡片排版、缩略图比例、文字层级。
- 暗色主题的色阶细化。

**不可改（需用户书面确认）**：

- 飞书卡片推送 schema（Schema V2 契约）。
- 资讯抓取与去重逻辑。

**接入注意**：

- Glassmorphism 是该项目的标签，做风格改动时**先与用户对齐**："还是 Glassmorphism 深耕？还是要换风格？"——后者属于重大风格改向，要慎重。
- 如果是 Glassmorphism 深耕，在 S3 链入全局 `glassmorphism` Skill 做风格规则参考（不是 ui-ux-pro-max）。
- SteamUI 暗色是该项目的视觉基准，改动时保持与 Steam 平台一致的"灰阶 + 蓝色 accent"基调。

### `20005-aigc/` — AI 美术流程介绍

**项目定位**：流程说明类站点（步骤、对比、案例展示）。

**可改**：

- 步骤可视化（timeline、step indicator、对比卡片）。
- 案例展示的图片画廊版式。
- 文字密度、信息层级。

**不可改（需用户书面确认）**：

- 案例数据来源（如果是从外部 CMS / 飞书拉的，不要硬编码进前端）。

**接入注意**：

- 这是 AI 美术流程站点，**最忌讳** AI slop 装饰（紫色渐变、星光特效、generic gradient mesh）——它**讲的就是 AI 美术**，自己却长成 AI slop 一脸打脸。
- 适合走对比鲜明的风格（editorial / swiss / brutalist）来表达"AI 美术能做出非 AI slop 的东西"。

### `20007-review/` — Steam 评论分析网页复刻

**项目定位**：评论数据可视化（统计、词云、趋势图）。

**可改**：

- 图表色彩、布局、可读性。
- Tooltip、图例、空状态视觉。
- 响应式（移动端图表退化策略）。

**不可改（需用户书面确认）**：

- 图表底层库（如已使用某图表库，替换库属于业务改动）。
- 数据聚合逻辑。

**接入注意**：

- 数据可视化对**对比度**和**色觉无障碍**要求高，工程质量维度必须查色盲安全色板。
- 不要为了"好看"用低对比度的同色系——数据可视化里这等于错误信息。

### `0-steamworks/`（GitHub `20029-steamworks`） — Steamworks 主面板

**项目定位**：浏览器扩展架构 + Steamworks 数据面板（愿望单、事件、飞书同步）。

**可改**：

- 扩展弹窗 / 选项页 / overlay 的视觉。
- 数据卡片、状态指示器、操作按钮。

**不可改（需用户书面确认）**：

- 扩展 manifest 配置（权限、host_permissions、background script）。
- Steamworks API 调用、飞书同步逻辑。
- 内容脚本注入策略。

**接入注意**：

- 浏览器扩展的 UI 受 host page 影响（CSS isolation、shadow DOM 选择），不能直接套通用 Landing 视觉。
- 扩展 UI 改动后**必须**人工冒烟（在 Chrome / Edge 实际 reload extension 试一遍），CSS 选择器冲突很常见。

### `gadget/Indieark_steam_design/` — Steam 展柜工具

**项目定位**：浏览器新标签页扩展，steam.design 工作台简化实现。

**可改**：

- 新标签页布局、展柜组件视觉。

**不可改（需用户书面确认）**：

- 扩展架构、Steam 数据接入。

**接入注意**：

- 同 `0-steamworks/` 的扩展 UI 注意事项。
- 新标签页是高频界面，工程质量维度尤其关注**首屏加载速度**和**字体闪烁**。

## 跨项目复用资产

详见 [`../../../../../PROJECTS.md`](../../../../../PROJECTS.md) 的"跨项目可复用能力"表。本 Skill 角度的复用模式：

- **不要 import 跨项目组件**：每个项目内自包含；要跨项目复用，先把组件抽到 `00000-model/01 复用资产/`。
- **可以参考视觉决策**：`1-showcase` 的多主题 token 体系是其他项目做主题化时的参考样板。
- **可以参考反 AI slop 的具体落地**：`20013-hot` 的 Glassmorphism + Steam 灰阶基调，是反"通用紫白底"的具体范例。

## 接入流程

`existing-project-optimize` 路线 S2 阶段必跑 [`../../../templates/existing-project-optimize-checklist.md`](../../../templates/existing-project-optimize-checklist.md) 接入前 checklist。本表与 checklist 的分工：

- **本表（cases.md）**：项目特有的"可改 / 不可改 / 立场要点"，更新频率低。
- **checklist**：每次接入前的通用验证（git status / package.json / 业务逻辑入口 / 用户授权），每次接入都过一遍。

## 新项目加入流程

新的 IndieArk 子项目要纳入本表时：

1. 先在 [`../../../../../PROJECTS.md`](../../../../../PROJECTS.md) 完成项目登记。
2. 评估项目是否含前端代码（无前端的纯后端 / CLI 项目不进本表）。
3. 在本文件加一节"项目级立场要点"，至少包含：项目定位 / 可改 / 不可改 / 接入注意。
4. 同步更新 [`router.md`](router.md) 的"子项目名清单"和 [`route-introduction.md`](route-introduction.md) 的"适合"列。
5. 如该项目有特殊的设计语言（如 20013-hot 的 Glassmorphism），考虑是否需要在 [`styles.md`](styles.md) 链入对应全局风格 Skill。
