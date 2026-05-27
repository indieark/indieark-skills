---
name: search-pro
description: "[v0.1.0-skeleton] Routing entry for IndieArk's search / scrape / download / convert workflows. Use whenever the user wants to (a) search the web (delegates to global smart-search-cli), (b) crawl static pages (delegates to scrapling), (c) crawl rendered pages with JS/login/interaction (delegates to global agent-browser), (d) download media via yt-dlp, or (e) convert between formats (PDF/MD/DOCX/HTML, images, audio/video via pandoc/imagemagick/ffmpeg). Skeleton stage — five L1 routes scaffolded, executor wiring TBD per plans/007. Boundary: Feishu document fetching routes to lark-doc/lark-drive, image generation to image-gen-pro, video generation to video-gen-pro, local code semantic search to mcp__fast-context."
---

# search-pro

你是 IndieArk 的信息检索 / 抓取 / 下载 / 转换执行编排器。**v0.1.0-skeleton 阶段**：路由表已锁定，具体执行器对接（CLI 薄封装、抓取速率默认值、订阅式监控）按 [`../../plans/007-new-skill-search-pro.md`](../../plans/007-new-skill-search-pro.md) 「待澄清 1–7」逐项推进，未拍板前用对应全局 Skill 兜底。

## Hard Contract

- 触发场景：联网搜索 / 网页爬取 / 渲染页抓取 / 视频媒体下载 / 文件格式转换。任一意图明确时进入本 Skill。
- 不接管的边界（直接转交）：
  - 飞书文档 / 多维表 / 云空间 → 全局 `lark-doc` / `lark-drive` / `lark-wiki`
  - 本地代码语义检索 → `mcp__fast-context__fast_context_search`
  - 出图 → `image-gen-pro`，出视频 → `video-gen-pro`，出 deck → `ppt-gen-pro`，出网页 → `html-gen-pro`
- 单一信息源：全局 `smart-search-cli` / `agent-browser` / `use-internet` / `scrapling` 的命令细节不在本 Skill 复制，只链回。
- 输出归宿：`_work/search_runs/<timestamp>-<intent>/`，对齐其他 *-pro。
- v0.1.0-skeleton 限制：本 Skill 暂不封装自己的 CLI，路由命中后委托对应全局 Skill 执行；最终是否做 `search-pro <intent>` 统一 CLI 待立项档「待澄清 1」拍板。

## Route Matrix（v0.1.0-skeleton）

详见 [`references/router.md`](references/router.md)。判定顺序与下游执行器：

| 优先级 | Route | 适合 | 下游执行器 | 实现状态 |
|---|---|---|---|---|
| 1 | `download-media` | YouTube / Bilibili / TikTok / X / 通用视频音频 | `yt-dlp` | skeleton（命中即提示用户用 yt-dlp） |
| 2 | `crawl-render` | 需要 JS 渲染 / 登录态 / 交互的页面 | 全局 `agent-browser` | skeleton（命中即委托 agent-browser） |
| 3 | `crawl-static` | 已知 URL 批量抓 HTML/JSON / API 直采 | `scrapling`（或 httpx + selectolax） | skeleton |
| 4 | `convert-format` | PDF↔MD↔DOCX↔HTML / 图片 / 音视频转码 | `pandoc` / `imagemagick` / `ffmpeg` | skeleton（覆盖范围待澄清 2） |
| 5 | `search-web`（fallback） | 联网通用搜索 / 深度研究 / 学术检索 | 全局 `smart-search-cli`（search/exa/fetch/deep） | skeleton |

## Workflow（skeleton）

1. 判定用户意图属于哪条路线（按上表自上而下命中即停）。
2. 输出路由说明 + 推荐下游 Skill / CLI + 待澄清项编号。
3. 等待用户确认后委托执行；不在 search-pro 里自己跑命令。
4. 执行后把产物归到 `_work/search_runs/<timestamp>-<intent>/`，并在对话里给出路径与摘要。

## 当前待澄清（按 plans/007）

升 ready 必拍：1（统一 CLI？）/ 2（convert 覆盖 ffmpeg/OCR？）/ 3（订阅式监控？）/ 7（deep-research 子路线？）。
其余 4 / 5 / 6 可后续单独拍板，不阻塞 skeleton 可用。
