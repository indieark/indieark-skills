# Capability Matrix

Load when: 用户问"这五条路线到底差在哪 / 我该选哪个 / X 能力哪条路线有"，或需要把推荐句的依据落到结构化对比上。
Avoid: 不要在路由决策本身用本表（路由决策走 `router.md`）；本表是辅证，不是 trigger 表。
Pairs with: `router.md`, `route-introduction.md`, `extensions.md`

> 真值来源：五个上游 SKILL.md（已下载到 `extensions/`）。本文件是面向用户的对比镜像；若五条路线能力升级，先看 upstream SKILL.md 再更新本表 + `extensions.md` 的 `verified_date`。

## 维度速查

| 能力 | image-first-ppt | web-html-ppt | design-html-ppt | svg-ppt | academic-image-ppt |
| ---- | ---- | ---- | ---- | ---- | ---- |
| 上游 | `NyxTides/ppt-image-first` | `op7418/guizang-ppt-skill` | `alchaincyf/huashu-design` | `hugohe3/ppt-master` | `fangyuanopus/literature-report-ppt-builder` |
| 输出格式 | PPTX（整页 image2 嵌入） | 单文件 HTML（横向翻页） | 单文件 HTML + 自带导出 MP4 / 原生 PPTX / PDF | PPTX（原生 SVG 元素 → PPTX shape） | PPTX（整页 image2 嵌入） |
| 默认画幅 | 16:9 | 16:9 横向 | 16:9 横向 | `ppt169`（可切 `ppt43` / `xhs` / `story`） | 16:9 |
| 中文支持 | 一等公民 | 一等公民（含 Windows 兜底 `Microsoft YaHei UI` / `Noto Sans SC`） | 一等公民 | 一等公民（Noto Sans SC） | 一等公民（默认中文论文汇报） |
| 可编辑 | ❌ 整页图片，PowerPoint 内不可逐元素改 | ❌ 静态 HTML，需改源码 | ❌ 静态 HTML，需改源码（PPTX 导出后是 image2 嵌入，不是原生 shapes） | ✅ 原生 PPT shape / 文本框 / 图标分层 | ❌ 同 image-first |
| 原生动画 | ❌ | ✅ Motion One 入场 + 翻页 | ✅ HTML/CSS/JS 动画（含 launch film 级 motion + 5 维评审审校 v0.4.0） | ✅ PPT 切换 + 元素动画（可对象级 customize-animations） | ❌ |
| 多人协作编辑 | ❌ | ❌（需共享源文件） | ❌（需共享源文件） | ✅（PPT 原生对象多人编辑） | ❌ |
| 图源约束 | 无（GPT-image 自由生成） | 弱（推荐 GPT-M 2.0 + 截图美化） | 弱（用户提供 + AI 生成） | 弱（`image_gen.py` 可选） | **强**：仅允许论文主文图 / SI / 用户截图 / 既有 PPT 页面；禁止重绘任何实验数据图 |
| 必带 speaker notes | ❌ | ❌ | ❌（v0.4.0 治理层启用后可强制） | ✅ `notes/total.md`（Step 6 自动产出） | ✅ `speaker_notes.md`（quality 模式强制） |
| 必带答辩 backup / Q&A | ❌ | ❌ | ❌ | ❌ | ✅ `backup_slides.md` + `question_prep.md`（quality 模式强制） |
| 风格预览 / 风格反演确认 | ✅ 首页/目录页/正文页 3 张图先确认 | 模板二选一（电子杂志 / 瑞士国际主义） | director's notes 工作流（launch film 场景，11500 字 + 13 镜 storyboard） | Strategist 八确认（色 / 字 / 图标 / 图片方案） | 走样例 deck 节奏 + adaptive navigation |
| 长 deck 容量 | 受 image 生成速度限制 | 单 HTML 文件，页数无硬上限 | 单 HTML 文件，页数无硬上限 | 顺序生成，单 agent 主程一次跑完 | 默认 ≥ 20 页 |
| 离线 / 单文件交付 | PPTX 单文件 | 单 HTML 文件（含本地 motion.min.js 兜底） | HTML / MP4 / PPTX / PDF 任选单文件 | PPTX + 备份 SVG 源 | PPTX 单文件 |
| 后续修改成本 | 重生成对应页 image2 | 改 HTML + CSS（参数化字号 / 间距） | 改 HTML + CSS，再跑对应导出脚本 | 直接 PowerPoint 编辑 | 重生成对应页 image2 |
| MP4 导出 | ❌ | ❌（需 L2 video-html-ppt 后操作或外挂工具） | ✅ 自带 `render-video.js` | ❌ | ❌ |
| 原生 PPTX 导出 | ❌（image2 嵌入，非原生 shapes） | ❌ | ✅ 自带 `html2pptx.js`（46KB 核心引擎） | ✅ 原生 SVG → PPTX shape | ❌（同 image-first） |
| PDF 导出 | ❌ | ❌ | ✅ 自带 `export_deck_pdf.mjs` / `export_deck_stage_pdf.mjs` | ❌ | ❌ |
| TTS provider | N/A | N/A（L2 时用户主机自备） | ⚠️ 锁豆包（火山引擎 openspeech）；没 key 时跳过 TTS 段可出无声 MP4 | N/A | N/A |
| L2 后操作支持 | ❌ | ✅ `video-html-ppt`（v0.3.0 引入；录屏 + 主机 TTS） | ❌（路线自带视频化能力，无需 L2） | ❌ | ❌ |
| LaTeX 公式渲染 | ❌（需手工截图嵌入） | ❌（需手工 MathJax / KaTeX） | ❌ | ✅ 上游 v2.8.0+ 自带：Strategist 锁定策略（mixed / render-all / text-only）+ 4-provider fallback（codecogs → quicklatex → mathpad → wikimedia，全部 no-API-key）+ 透明 PNG 嵌入 | ❌（如论文含公式，沿用原图截图，不重渲染） |

## 选型决策辅助

按维度反查推荐路线：

| 用户硬性需求 | 推荐路线 | 理由 |
| ---- | ---- | ---- |
| 标准汇报 / 产品介绍 / 路演 / 商业 deck | `image-first-ppt` | 图片级稳定 + 风格预览先行，常规交付误差最低 |
| 单文件 HTML / 网页演示 / 演讲 / 杂志风或瑞士风 | `web-html-ppt` | 唯一支持 HTML 横向翻页 + 浏览器即开即用 |
| 后续要在 PowerPoint 里改文字 / 颜色 / 动画 | `svg-ppt` | 唯一输出原生 PPT 对象，其他三条都是 image-first |
| 论文 / 文献汇报 / 组会 / 答辩 / journal club | `academic-image-ppt` | 唯一对图源加铁律 + 自动产出 speaker notes / backup / Q&A prep |
| 文档量大 / 需要 PDF / DOCX / EPUB / 网页转 PPT | `svg-ppt` | 唯一提供 `source_to_md/` 多格式转换脚本链 |
| 需要 GPT-image 风格预览先看 3 张再决定 | `image-first-ppt` | 唯一硬性把"风格反演确认"放在写 spec 之前 |
| 演讲带动效 / 入场动画 / WebGL 背景 | `web-html-ppt` | Motion One + WebGL fluid/grid 内置 |
| 高保真原型 / 设计稿 mockup / launch film 级品牌动画 | `design-html-ppt` | 唯一自带 director's notes 工作流（launch film 11500 字 + 13 镜 storyboard） |
| 同一份 deck 要 MP4 + 原生 PPTX + PDF 同时产出 | `design-html-ppt` | 唯一自带 3 路导出工具链（`render-video.js` / `html2pptx.js` / `export_deck_pdf.mjs`） |
| 旁白 / 配音 + 视频（需要 TTS） | `design-html-ppt`（豆包）或 `web-html-ppt` + L2（主机自备） | design 锁豆包 API，web-html + L2 需用户主机环境组装 |
| 数学公式 / LaTeX 排版（教学课件 / 数学讲义） | `svg-ppt` | 唯一上游内置 LaTeX 公式渲染（v2.8.0+，4-provider fallback 无 API key） |
| 论文含公式但要走学术路线（图源真实 + speaker notes） | `academic-image-ppt` | 学术场景图源约束 + speaker notes 优先级高于公式渲染；论文图含公式直接沿用截图 |

## 不要混用

- 不要在同一次执行里横跨两条路线（用户明确要 hybrid 时除外）。
- 不要把 academic 的图源铁律套到 image-first（会失去 GPT-image 风格自由度）。
- 不要把 image-first / academic 的 image2 嵌入式 PPT 当作可编辑 PPT 给用户改，他们改不动。
- 不要把 svg-ppt 的"原生 PPT 元素"当作图像级保真承诺，shape 渲染在 PowerPoint 不同版本会有细微漂移。
- 不要把 design-html-ppt 的 `html2pptx.js` 导出当成 svg-ppt 那种原生 shape PPTX；它产出的 PPTX 仍是 image2 嵌入式，PowerPoint 内不可逐元素编辑。
- 不要假定 design-html-ppt 的 TTS / 视频化适用于其他路线 — TTS 链路锁豆包 API key，工具链仅在本路线内部。

## 维护契约

- 新增第 6 条路线时：先在本表末尾加列、再同步 `router.md` Route Menu 表和 `route-introduction.md`。
- 上游 SKILL.md 实质变化时（新增 / 移除核心能力）：本表 + `extensions.md` 的 `verified_date` 一起翻新。
- 新增路线自带跨格式导出工具链时（如 MP4 / 原生 PPTX / PDF / 音频），在本表底部「v0.3.0 引入的 5 个导出/L2 能力行」继续追加新行，而不是改顶部「输出格式」单行（保持每个能力维度可单独 yes/no 比较）。
- 本表不存路由触发词，触发词唯一信息源仍是 `router.md` 和 `scripts/test_router.py` 的关键词常量。
