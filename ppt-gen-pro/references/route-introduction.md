# Route Introduction

Load when: 每次用户要生成真实 PPT / slides / deck 时，在委托任何扩展前加载。
Avoid: 不要把本文件当成最终生成流程；它只负责标准介绍、推荐理由和选择门。
Pairs with: `usage.md`, `router.md`, `extensions.md`, `reporting.md`, `capability-matrix.md`

## Why This Exists

`ppt-gen-pro` 的首要职责不是直接生成，而是让用户先明白四种路线的取舍。介绍必须稳定、诚实、可复用：

- 图片 PPT 是标准默认路线，优先保障成品视觉质量和常规交付稳定性。
- 网页 PPT 是演讲、主文字、叙事和动效路线，优先保障现场表达与单文件 HTML 体验。
- 设计 HTML PPT 是高保真原型 / 设计稿 / 多格式导出（MP4 + 原生 PPTX + PDF）路线，与网页 PPT 同为 HTML deck 家族，但定位偏设计治理和导出深度，不是默认标准 PPT 路线。
- SVG PPT 是可编辑优先路线，只在用户明确需要 PowerPoint 对象级编辑、原生动画或 SVG/PPTX 工程化导出时推荐；当前不作为默认标准 PPT 路线。

## Upstream Observations

### 图片 PPT：`NyxTides/ppt-image-first`

真实价值在于 conversation-first + image-first 工作流：先做轻量需求确认和内容基底，再生成首页 / 目录页 / 正文页真实风格预览，确认后写规划文件并生成整页视觉图，最后封装成 PPTX。

适合：标准 PPT、汇报、答辩、路演、产品介绍、视觉完成度优先、风格预览、图像级返修。

边界：页面通常以整页图片为核心，不保证每个文字框、图形和图标都是 PowerPoint 原生可编辑对象。

### 网页 PPT：`op7418/guizang-ppt-skill`

真实价值在于单文件 HTML 横向翻页 deck，提供电子杂志风和瑞士国际主义两套成熟视觉系统，并内置 WebGL / Motion One 动效、布局清单和视觉检查规则。

适合：主文字内容、演讲稿、观点分享、叙事表达、动效展示、网页演示、单文件 HTML、杂志风、瑞士风、发布会或内部分享。

边界：不适合大量表格、传统 PPTX 多人协作编辑，或必须在 PowerPoint 里逐项改元素的场景；不带原生 MP4 / PPTX 导出。

### 设计 HTML PPT：`alchaincyf/huashu-design`

真实价值在于把 HTML deck 与「**设计治理 + 多格式导出**」打包成一个完整工具链：12 个独立脚本覆盖 HTML → MP4（`render-video.js`）、HTML → 原生 PPTX（`html2pptx.js` 46KB）、HTML → PDF（`export_deck_pdf.mjs`）、旁白 pipeline、配乐混音、TTS（豆包）。

适合：高保真原型、设计稿 mockup、launch film 级品牌动画、设计评审 deck，以及需要 MP4 / 原生 PPTX / PDF 多格式导出而不希望外挂工具的场景。

边界：
- TTS 链路锁定豆包（火山引擎 openspeech）API key；没 key 时跳过 TTS 段，仍可出无声 MP4 / PDF / PPTX。
- 设计治理层（20 设计哲学 + 5 维评审）v0.3.0 未启用，留 v0.4.0；本路线当前只用其 HTML deck + 导出工具链。
- 不适合纯主文字演讲（走网页 PPT 更轻）或论文证据汇报（走 academic-image-ppt 有图源铁律）。

### SVG PPT：`hugohe3/ppt-master`

真实价值在于从文档生成原生可编辑 PPTX：以真实 PowerPoint shapes、原生动画和 SVG-to-PPTX 导出为核心，而不是把页面拍平成图片。**自 v2.8.0 起内置 LaTeX 公式渲染**：Strategist 锁定公式策略（mixed / render-all / text-only），4-provider fallback（codecogs → quicklatex → mathpad → wikimedia），全部 no-API-key、零配置；公式以透明 PNG 嵌入，与原生 shape 共存。

适合：用户明确要求可编辑原生元素、PowerPoint 对象级修改、原生动画、后续多人编辑、SVG/PPTX 工程化导出；**或含数学公式 / LaTeX 排版需求**（教学课件 / 数学讲义 / 物理化学反应式等，非学术汇报场景）。

边界：可编辑链路比整页图片链路更复杂，交付前更依赖 PowerPoint 打开复查。除非用户把”可编辑”或”公式渲染”放在”标准视觉交付省心”之前，否则不要推荐 SVG。学术场景（论文 / 文献汇报 / 答辩）即使含公式仍走 `academic-image-ppt`，因为图源真实性约束和 speaker notes 比 LaTeX 渲染优先级更高。

## Standard User Introduction

对 `generation-request` 使用下面结构，允许按用户语境轻微改写，但不要改变推荐顺序和取舍：

```text
我可以用四种方法做这份 PPT，先帮你选路线：

1. 图片 PPT（默认推荐）
   适合标准 PPT、汇报、答辩、路演、产品介绍和视觉完成度优先的交付。它会先做内容基底和真实风格预览，再把高质量整页视觉封装成 PPTX。缺点是页面通常不是逐元素可编辑。

2. 网页 PPT
   适合主文字、演讲内容、叙事表达、动效展示、网页演示和单文件 HTML。它更像一份可以直接演示的网页 deck，杂志风和瑞士风会更稳。缺点是不适合传统 PPTX 多人协作逐项改，也不带原生 MP4 / PPTX 导出。

3. 设计 HTML PPT
   适合高保真原型、设计稿 mockup、launch film 级品牌动画，以及需要 MP4 / 原生 PPTX / PDF 多格式导出的场景。它和网页 PPT 同为 HTML deck，但自带 `render-video.js` / `html2pptx.js` / `export_deck_pdf.mjs` 工具链。注意：自带豆包 TTS（火山引擎 openspeech），没豆包 API key 时跳过 TTS 段仍可出无声 MP4 / PDF / PPTX。

4. SVG PPT / 可编辑 PPT
   适合你明确要求 PowerPoint 里逐个文字框、图形、图标可编辑，需要原生动画，或者后续要多人继续改；**也适合含数学公式 / LaTeX 排版的教学课件 / 数学讲义**（自带 4-provider LaTeX 渲染，无需 API key）。它是可编辑优先路线，但链路更复杂，不作为标准 PPT 的默认推荐。

我的建议：{recommendation_sentence}

你可以回复 1 / 2 / 3 / 4，或直接说"按推荐来"。
```

用户选择后不要继续停在介绍层；读取 `usage.md`，检查对应扩展安装状态，然后打开对应外部 Skill 入口继续。

## Recommendation Sentences

按 `router.md` 判断后，把 `{recommendation_sentence}` 替换为其中一句：

- 默认 / 标准 PPT：`建议用图片 PPT，因为标准 PPT 更需要稳定的整页视觉质量和常规交付效果。`
- 主文字 / 演讲 / 动效 / 网页：`建议用网页 PPT，因为你的需求更像演讲型或叙事型 deck，单文件 HTML、动效和版式节奏会更合适。`
- 高保真 / 设计稿 / 多格式导出：`建议用设计 HTML PPT，因为你的需求要 HTML deck + 多格式导出（MP4 / 原生 PPTX / PDF）。提示：TTS 链路锁豆包 API，没 key 时跳过 TTS 仍可出无声 MP4。`
- 可编辑 / 原生对象：`建议用 SVG PPT，但这是为了可编辑性让路；如果你更看重成品观感，我仍建议改用图片 PPT。`
- 数学公式 / LaTeX（非学术场景）：`建议用 SVG PPT，因为上游 ppt-master v2.8.0+ 内置 LaTeX 4-provider 渲染（codecogs → quicklatex → mathpad → wikimedia，全部免 API key），公式以透明 PNG 嵌入与原生 shape 共存。如果你的场景是论文 / 文献汇报，我会改走学术专用路线 academic-image-ppt。`

## Selection Rules

- 如果用户只说"做一份 PPT""生成 PPT""标准 PPT"，默认推荐图片 PPT。
- 如果用户强调"演讲、讲稿、主文字、叙事、动效、网页 PPT、HTML、单文件、杂志风、瑞士风"，推荐网页 PPT。
- 如果用户强调"高保真原型、设计稿、mockup、设计哲学、5 维评审、设计动画、launch film、品牌动画、MP4 导出、原生 PPTX 导出、PDF 导出、豆包 TTS"，推荐设计 HTML PPT；同时给豆包 TTS caveat。
- 如果用户强调"可编辑、原生 PPT 元素、PowerPoint 里逐项改、多人协作修改、SVG"，才推荐 SVG PPT。
- 如果用户提到"数学公式 / LaTeX / 公式渲染 / 公式排版"（且非学术场景），推荐 SVG PPT 并解释 4-provider 免 key fallback；学术场景（论文 / 文献汇报）即使含公式仍走 academic。
- 如果用户同时要"好看"和"可编辑"，先说明取舍：图片 PPT 更稳，SVG 更可编辑；让用户决定哪个优先。
- 如果用户同时要"演讲"和"高保真设计"，先说明取舍：网页 PPT 轻量、聚焦演讲表达；设计 HTML PPT 重多格式导出和设计治理。
- 不要把 SVG / design 描述成更高级的默认路线；它们只是特定约束下的备选。

## Post-Process Layer (L2，v0.3.0 引入)

L1 路线（生成形态）之外，ppt-gen-pro 从 v0.3.0 起支持 **L2 后操作层** — 在 L1 产物之上做视频化 / 录屏 / 旁白配音等二次加工。**真源在 `post-processes.md`，本节是介绍阶段的呈现规则**。

### 当前 L2 注册项

| L2 名称 | 上游 | 适用 L1 | 形态 |
|---|---|---|---|
| `video-html-ppt` | `ConardLi/garden-skills/skills/web-video-presentation`（locked `ea0c0c8` / verified 2026-05-25） | **仅 `web-html-ppt`** | scaffold + 模板 + 方法论；render-video / TTS 由 Agent 主机环境组装 |

### 介绍阶段的呈现规则

- **不打扰原则**：用户消息未命中 L2 触发词时，介绍阶段**不主动提** L2，避免决策疲劳。
- **预览触发**：路由器（S0）扫到 L2 触发词后，在标准 4 选 1 菜单之下附加一段：

```text
另外你提到「录屏 / 旁白 / 视频版」等需求，如果你选第 2 项（网页 PPT），我可以在生成完之后再带你走 L2「视频化后操作」：
- L2 `video-html-ppt`（轻 scaffold + 模板，主机自备 TTS / Headless 录屏）
注意：image-first / svg / academic 路线没有 HTML 容器，不能走这条 L2；设计 HTML PPT 自带 `render-video.js`，也不走 L2。
```

- **拒绝进入 L2 的兜底**：若用户在 L1=image-first/svg/academic 时执意要 L2，应先解释"产物没有 HTML 容器无法录屏"，再询问是否切 L1 到 web-html-ppt。

### 与 L1 路线的关系

| 用户表达 | 路由结果 |
|---|---|
| 「演讲 PPT + 后续要录成 MP4」 | L1 `web-html-ppt` + L2 `video-html-ppt` 预览 |
| 「设计稿 + 出片」 | L1 `design-html-ppt`（自带视频化），**不进** L2 |
| 「MP4 + PPTX + PDF 三格式导出」 | L1 `design-html-ppt`（自带 3 格式工具链），**不进** L2 |
| 「图片 PPT 但要录成视频」 | 解释 image-first 不适合录屏，引导切 L1 |

L2 详细委托契约、上游版本管理、触发词全集，全部以 `post-processes.md` 为准。

## Domain-Specialized Routes（领域特化路线，自动路由）

通用 3 选一菜单保持原样不变，但当用户请求里命中下列任一领域触发词时，**直接推荐对应特化路线、跳过通用菜单**，避免用户在通用 3 路线里挑出不合适的方案。

### `academic-image-ppt` — 学术文献汇报

- 扩展：`fangyuanopus/literature-report-ppt-builder`（内部 skill 名 `academic-slide-minimalist`）。
- 触发词：论文、文献汇报、组会、journal club、答辩、SI、supplementary、课题汇报、paper、课程文献、文献阅读、主文图、文献讲解。
- 推荐话术（直接给出，不展示通用菜单）：

```text
你这个是论文/文献汇报场景，我直接走学术专用路线 `academic-image-ppt`，不走通用 3 选一：

- 用 `fangyuanopus/literature-report-ppt-builder` 的 close reading → figure manifest → page brief 流程
- 图源只取论文主文图、SI 图或你给的截图，不重绘实验数据图
- 会同时产出 figure_source_manifest / speaker_notes / backup_slides / question_prep，方便答辩

如果你其实只想要论文话题的"好看视觉稿"、不在乎图源真实性，告诉我，我切回通用图片 PPT 路线。
```

- 跳过门：只有用户明确说"虽然是论文但只要视觉好看、不管图源真实性"时，才回退到通用 `image-first-ppt`。
- 委托入口：`extensions/literature-report-ppt-builder/academic-slide-minimalist/SKILL.md`。

### 未来扩展点

如新增教育课件、路演、自媒体封面等领域特化扩展，按相同模式登记：
- 在 `extensions.md` Registry 加行
- 在 `router.md` Recommendation Rule §0 加触发词
- 在本文件加 `## Domain-Specialized Routes` 子小节
- 不改通用 3 选一菜单（菜单专门给"不属于任何领域"的标准 PPT 用）
