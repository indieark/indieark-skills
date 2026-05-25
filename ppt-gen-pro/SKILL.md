---
name: ppt-gen-pro
description: Mandatory presentation and slide deck generation router skill. Use whenever the user wants to create, plan, structure, rewrite, storyboard, or prepare PPT/PPTX/slides/decks/presentations. It routes among five L1 generation forms (image-first, web/HTML, design HTML, SVG/editable, academic-image) and one L2 post-process layer (video-html-ppt for web-html-ppt recording). It must introduce the L1 routes, recommend one, ask the user to choose, and then delegate to the selected installed extension.
---

# ppt-gen-pro

## 触发条件

当用户需要创建、规划、改写、结构化或准备演示文稿、PPT、PPTX、slides、slide deck、presentation、路演稿、汇报稿、课程课件、Pitch Deck、网页 PPT 或 PDF deck 时，必须触发本 Skill。

## 定位

本 Skill 是顶层 PPT 路由器和扩展调度层（v0.3.0 起二层结构）：

- **L1 路线层**：识别 PPT 生成意图，给用户介绍 4 种通用路线 + 1 种领域特化自动路由，并推荐最合适的一种。
- **L2 后操作层**：在 L1 产物之上做视频化 / 录屏 / 旁白等二次加工；当前唯一 L2 = `video-html-ppt`，**仅适用 L1=web-html-ppt**。
- 内部扩展层：通过本仓库登记的外部 Skill 源安装、检查和委托执行。
- 协调层：保留用户选择、route 选择理由、L2 决策、安装状态、输出边界和验证结果。

## 四种通用 L1 路线

每次用户要生成 PPT 时，都要按 [`references/route-introduction.md`](references/route-introduction.md) 的标准介绍先说明取舍，并让用户选择：

1. 图片 PPT：`NyxTides/ppt-image-first`。标准 PPT 默认路线，适合高完成度视觉稿、风格预览、答辩/汇报封面、图像级页面和大多数常规交付。
2. 网页 PPT：`op7418/guizang-ppt-skill`。适合单文件 HTML 横向翻页 PPT、主文字内容、演讲内容、叙事表达、动效展示、线下分享、观点演讲、杂志风/瑞士风网页 deck、多平台封面和配图。
3. 设计 HTML PPT：`alchaincyf/huashu-design`。适合高保真原型、设计稿 mockup、launch film 级品牌动画、设计评审 deck，以及需要 MP4 / 原生 PPTX / PDF 多格式导出而不希望外挂工具的场景。注意：自带豆包 TTS（火山引擎 openspeech），没豆包 API key 时跳过 TTS 段仍可出无声 MP4 / PDF / PPTX。
4. SVG PPT：`hugohe3/ppt-master`。可编辑优先路线，适合用户明确要求可编辑原生 PPT 元素、后续多人编辑、PowerPoint 对象级修改、原生动画，或明确要走 SVG/PPTX 工程化导出。

默认推荐策略（判定顺序 `svg → design → web → image-first`）：如果用户没有明确偏好，标准 PPT 优先推荐图片 PPT；如果用户强调主文字、演讲内容、叙事、动效、网页演示、单 HTML、杂志风或瑞士风，推荐网页 PPT；如果用户强调高保真原型 / 设计稿 / launch film / 多格式导出（MP4 / PPTX / PDF）/ 豆包 TTS，推荐设计 HTML PPT；只有用户明确强调可编辑、原生 PPT 元素、后续多人编辑或 PowerPoint 对象级修改时，才推荐 SVG PPT。

## 领域特化路线（自动路由，不进通用菜单）

通用三种内置路线之外，再登记**领域特化路线**：当请求落入某个明确领域且通用 3 选 1 会产生错误推荐时，跳过通用菜单直接推。当前唯一已登记：

- `academic-image-ppt`：`fangyuanopus/literature-report-ppt-builder`（内部 skill 名 `academic-slide-minimalist`）。用于论文 / 文献汇报 / 组会 / journal club / 答辩 / SI / supplementary / 课题汇报 / paper / 课程文献。输出形态与图片 PPT 相同（PPTX），但工作流强制 close reading → figure manifest → page brief → image2，且**禁止重绘任何实验数据图**，并必带 speaker notes + backup + Q&A prep。

触发判定见 [`references/router.md`](references/router.md) §0；详细话术见 [`references/route-introduction.md`](references/route-introduction.md) 的 "Domain-Specialized Routes" 小节。

## L2 后操作层（v0.3.0）

在 L1 路线产物之上，本 Skill 支持 L2 后操作做视频化 / 录屏 / 旁白配音等二次加工。当前唯一登记的 L2 = `video-html-ppt`（上游 `ConardLi/garden-skills/skills/web-video-presentation`，scaffold + 模板，render-video / TTS 由 Agent 主机环境组装）。

**L2 触发模型**：

- 路由器在 L1 判定完后扫一遍 L2 触发词（录屏 / 旁白 / 视频版 / 按视频节奏 / 一屏一镜 等，全集见 `references/post-processes.md`）。
- 命中即在介绍阶段附加 L2 选项预览；**未命中时不主动提**，避免决策疲劳。
- L1 完成后再询问"是否进入 L2"；用户确认才切到 L2 入口。

**L2 适用范围**：

- ✅ `web-html-ppt`：HTML deck 有真实 DOM 容器可被 Headless 录屏。
- ❌ `image-first-ppt` / `academic-image-ppt`：产物是 image2 嵌入式 PPTX，没 HTML 容器。
- ❌ `svg-ppt`：原生 PPT 对象走 PowerPoint 原生导出。
- ❌ `design-html-ppt`：路线自带 `render-video.js` + 豆包 TTS，无需 L2。

详见 [`references/post-processes.md`](references/post-processes.md)（L2 真源）和 [`references/flows.md`](references/flows.md)（S0 路由 → S1 介绍选择 → S2 引导流程状态机）。

## 使用流程

1. 读取 [`references/README.md`](references/README.md)。
2. 如果本地未安装或可能需要更新三种扩展，先读取 [`references/install.md`](references/install.md)，运行扩展安装/更新/检查流程。
3. 对 PPT 生成请求，必须先读取 [`references/route-introduction.md`](references/route-introduction.md)，输出标准路线介绍、推荐路线和选择问题。
4. 用户选择后，读取 [`references/usage.md`](references/usage.md)、[`references/router.md`](references/router.md) 和 [`references/extensions.md`](references/extensions.md)，按明确的外部 Skill 入口把需求委托给对应扩展。
5. 执行完成后按 [`references/reporting.md`](references/reporting.md) 汇报路线、输出、验证和后续可改点。

## Red Lines

- 不提交 secrets、私有素材、客户资料或生成产物。
- 不覆盖用户已有 deck；未来修改现有文件时默认输出新文件。
- 不把外部扩展的内部实现复制进本 Skill；本 Skill 只维护路由、安装、更新、检查、选择和委托协议。
- 不在用户未选择 L1 路线前直接进入某个扩展生成。
- 不允许 L2 单独达成（不存在"绕过 L1 直接 L2"路径）；L2 必须在 L1 选定后才进入。
