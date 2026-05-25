# Router

Load when: 需要判断用户请求属于规划、建档、改写、图片 PPT、网页 PPT 还是 SVG PPT。
Avoid: 不要在用户未选择路线前直接进入某个扩展生成。
Pairs with: `workflow.md`, `route-introduction.md`, `extensions.md`, `install.md`, `post-processes.md`, `flows.md`

> **二层架构（v0.3.0）**：路由从此分两层 — L1 路线（生成形态）由本文件主导；L2 后操作（视频化 / 录屏 / 旁白）真源在 `post-processes.md`；两层串联的状态机在 `flows.md`。

## Task Types

- `deck-planning`: 梳理主题、受众、大纲、页数和素材。
- `deck-rewrite`: 改写已有大纲、讲稿或页面文案。
- `deck-storyboard`: 规划每页内容、版式和视觉素材。
- `repository-maintenance`: 补文档、规则、索引或 validator。
- `generation-request`: 用户要求生成真实 PPT / slides / deck。

## Mandatory Trigger Rule

只要用户要生成、创建、改写成、整理成、做成或导出演示文稿 / PPT / PPTX / slides / deck / Pitch Deck / 网页 PPT，就必须触发 `ppt-gen-pro`。不要让其他 PPT Skill 先于本 Skill 直接执行。

## Route Menu

每次 `generation-request` 都先按 `route-introduction.md` 展示四种通用路线（学术领域特化路线走自动路由，不进入默认菜单）：

| Route | 扩展 | 适合 | 默认建议 |
| ---- | ---- | ---- | ---- |
| `image-first-ppt` | `NyxTides/ppt-image-first` | 标准 PPT、高完成度视觉稿、整页图片、风格预览、图像级返修 | 默认推荐 |
| `web-html-ppt` | `op7418/guizang-ppt-skill` | 主文字、演讲内容、叙事、动效、单文件 HTML、杂志风、瑞士风、演讲展示 | 文字/演讲/动效优先 |
| `design-html-ppt` | `alchaincyf/huashu-design` | 高保真原型、设计稿 mockup、设计哲学、设计动画、launch film、多格式导出（MP4/PPTX/PDF）、豆包 TTS | 设计稿/动画/多格式导出优先 |
| `svg-ppt` | `hugohe3/ppt-master` | 可编辑原生 PPT 元素、PowerPoint 对象级修改、原生动画、后续多人编辑、SVG/PPTX 工程化导出、**数学公式 / LaTeX 排版**（上游 v2.8.0+ 内置 4-provider fallback，无需 API key） | 可编辑优先 / 公式优先 |

### 领域特化路线（自动路由，不进入通用 3 选 1 菜单）

| Route | 扩展 | 触发场景 | 路由方式 |
| ---- | ---- | ---- | ---- |
| `academic-image-ppt` | `fangyuanopus/literature-report-ppt-builder` | 论文汇报、文献汇报、组会、journal club、答辩预演、课题汇报、课程文献阅读 | 检测触发词命中即推荐，跳过通用菜单 |

## Recommendation Rule

判定顺序：**先看领域特化触发词，再走通用路线推荐**。

### 0. 领域特化优先（命中即直推，跳过通用菜单）

- 用户提到「论文 / 文献汇报 / 组会 / journal club / 答辩 / SI / supplementary / 课题汇报 / paper / 课程文献 / 文献阅读 / 主文图 / 文献讲解」中任何一个 → 直接推荐 `academic-image-ppt`，**不展示** 通用 3 选 1 菜单。
- 说明：学术汇报场景的用户意图明确，且证据真实性 / 图源约束 / 答辩准备和通用 PPT 完全不同；走通用路线会失去 figure manifest、speaker notes、backup slides、Q&A prep 这些必带交付物。
- 例外：用户明确说"虽然是论文话题但只要好看的视觉稿、不要管图源真实性" → 仍按通用规则走 `image-first-ppt`。
- 触发词冲突：用户消息同时含「论文 / 文献」和「公式 / LaTeX」时仍走 academic（academic 链路内部已有图源真实性约束和 speaker notes，比公式渲染优先级更高；svg-ppt 的 LaTeX 能力只在「非学术 + 公式」场景胜出）。

### 通用路线推荐（领域特化未命中时）

判定顺序：`svg` → `design` → `web` → `image-first` 默认（design 与 web 同属 HTML deck 家族，design 触发词更专一，优先判定）。

- 默认：推荐 `image-first-ppt`。标准 PPT、普通汇报、答辩、产品介绍、商业展示和未明确偏好的请求，都先走图片 PPT。
- 用户强调"主文字、演讲内容、讲稿、叙事、动效、网页 PPT、HTML、单文件、杂志风、瑞士风、线下分享、演讲"：推荐 `web-html-ppt`。
- 用户强调"高保真原型、设计稿、mockup、设计哲学、5 维评审、设计动画、launch film、品牌动画、MP4 导出、原生 PPTX 导出、PDF 导出、豆包 TTS"：推荐 `design-html-ppt`，并提醒"TTS 链路锁定豆包 API key，没 key 时跳过 TTS 段可出无声 MP4/PDF/PPTX"。
- 用户强调"可编辑、原生 PPT 元素、PowerPoint 里逐项改、原生动画、后续多人编辑、对象级修改"：推荐 `svg-ppt`，并提醒它是可编辑优先，不是标准 PPT 默认路线。
- 用户提到"数学公式、LaTeX、公式渲染、公式排版"（且非学术场景，否则按 §0 走 academic）：推荐 `svg-ppt`，并说明上游 ppt-master v2.8.0+ 内置 LaTeX 公式渲染：Strategist 锁定公式策略（mixed / render-all / text-only），4-provider fallback（codecogs → quicklatex → mathpad → wikimedia），全部 no-API-key 对终端用户零配置。
- 用户只说"标准 PPT、做一份 PPT、帮我生成 PPT"：推荐 `image-first-ppt`，不要默认推 SVG 或 design。
- 用户同时要求"好看"和"可编辑"时，先说明图片 PPT 与 SVG PPT 的取舍；如果用户没有明确把可编辑放在第一位，仍推荐 `image-first-ppt`。
- 用户同时要"演讲"和"高保真设计"时，先说明 `web-html-ppt`（演讲优先 / 轻量）与 `design-html-ppt`（多格式导出 / 设计治理）的取舍。

## Choice Gate

生成前必须问用户选择：

```text
我建议用图片 PPT 路线，因为标准 PPT 默认更适合稳定的整页视觉稿和常规交付。
也可以选：
1. 图片 PPT：标准默认 / 整页视觉稿 / 高完成度画面 / 图像级返修
2. 网页 PPT：主文字 / 演讲内容 / 动效 / 单文件 HTML / 杂志风或瑞士风
3. 设计 HTML PPT：高保真原型 / 设计稿 mockup / launch film / 多格式导出（MP4 + 原生 PPTX + PDF）/ 豆包 TTS
4. SVG PPT：可编辑原生元素 / PowerPoint 对象级修改 / 后续多人编辑

你想用哪一种？如果你不确定，我会按推荐路线继续。
```

用户明确选择或接受推荐后，才委托对应扩展。

## §3 · L2 后操作路由（v0.3.0 新增）

L2 后操作只在 L1 路线选定后才进入决策；真源是 `post-processes.md`，本节是路由器侧的触发词索引。

### L2 触发词

| 触发词类别 | 关键词样例 | 命中后行为 |
|---|---|---|
| 视频节奏 | 按视频节奏 / 一屏一镜 / 自动播放 / video pace | 推 `video-html-ppt`（要求 L1=`web-html-ppt`） |
| 录屏 | 录屏 / 屏幕录制 / screen capture / screencast | 推 `video-html-ppt` |
| 旁白 / 配音 | 旁白 / 配音 / 解说 / narration / voiceover | 视 L1 而定：`design-html-ppt` 自带豆包 TTS / `web-html-ppt` → L2 主机自备 |
| 视频成品 | 视频版 / 视频化 / 出片 / 转 MP4 | 视 L1 而定：`design-html-ppt` 自带 `render-video.js` / `web-html-ppt` → L2 video-html-ppt |

### L2 仲裁规则

| 用户表达 | 仲裁结果 |
|---|---|
| 「设计动画 + 视频 / 设计稿出片」 | 走 L1 `design-html-ppt`（自带视频化），**不进** L2 |
| 「演讲网页 PPT + 后续要录成 MP4」 | L1 `web-html-ppt` + L2 `video-html-ppt`（介绍阶段并列展示） |
| 「MP4 / PPTX / PDF 多格式导出」 | 走 L1 `design-html-ppt`（自带 3 格式工具链），不进 L2 |
| 「PPT 视频版」无上下文 | 询问 deck 形态偏好：演讲 → L1 web + L2 video / 设计稿 → L1 design |
| L1 = `image-first-ppt` / `svg-ppt` / `academic-image-ppt` 时触发 L2 | 拒绝进入 L2，提示用户切 L1（理由见 `post-processes.md`「适用范围」） |

### L2 触发模型

- **预扫描**：S0 路由判定完 L1 后，同时扫一遍 L2 触发词，命中即在 S1 介绍阶段附加 L2 选项预览。
- **不打扰**：未命中 L2 触发词时，路由器不主动提 L2，避免决策疲劳。
- **L1 锁定**：L2 不可独立达成；用户必须先确认 L1 路线，才可在 S2 末尾被询问是否进入 L2。
