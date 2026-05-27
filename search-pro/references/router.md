# search-pro · L1 路由（v0.1.0-skeleton）

> 父级：[../SKILL.md](../SKILL.md)
> 立项档：[../../../plans/007-new-skill-search-pro.md](../../../plans/007-new-skill-search-pro.md)

## 判定顺序

自上而下，命中即停。判定时优先看用户意图 + URL/资源类型，**不**根据 Skill 内部能力强弱去抢。

| 优先级 | Route | 命中条件（关键词 + 资源类型） |
|---|---|---|
| 1 | `download-media` | "下载"/"保存"+视频/音频/直播 URL；YouTube / Bilibili / TikTok / X / Twitch / 通用 m3u8 |
| 2 | `crawl-render` | 目标页 JS 渲染 / 登录态 / 需要点击翻页 / SPA / 数据藏在 XHR 后 |
| 3 | `crawl-static` | 已知静态 URL 列表 / API 端点 / sitemap 批采 / HTML/JSON 直接拿 |
| 4 | `convert-format` | "转成 / 换成 / 导出为" + PDF/MD/DOCX/HTML/PNG/JPG/MP4/MP3/WAV |
| 5 | `search-web`（fallback） | 上述都不命中 / 问题需要外部知识 / 多源比对 / 深度研究 |

## 路线 → 下游执行器（v0.1.0-skeleton）

### `search-web`
- 下游：全局 `smart-search-cli`
- 命令形态：`search` / `exa` / `fetch` / `deep`
- 选择策略：默认 `search`；多源比对用 `exa`；带网页正文抓取用 `fetch`；多 hop 深度研究用 `deep`
- 待澄清：多语言/区域默认偏好（plans/007 Q5）；deep-research 子路线是否本 Skill 内置（plans/007 Q7）

### `crawl-static`
- 下游：`scrapling`（首选）或 `httpx + selectolax`
- 选择策略：scrapling 适合"反爬较弱 + 需要 stealth"；httpx 适合纯 API 拉取
- 待澄清：抓取速率默认值 / robots.txt 是否硬遵守（plans/007 Q6）

### `crawl-render`
- 下游：全局 `agent-browser`
- 选择策略：v0.1.0-skeleton 一律 spawn agent-browser；是否做薄封装待澄清（plans/007 Q4）

### `download-media`
- 下游：`yt-dlp` 命令行
- 默认参数：最高质量 video+audio merge / 字幕一并下 / 写入 `_work/search_runs/<id>/media/`
- 不接管：飞书云空间视频（→ `lark-drive`）

### `convert-format`
- 下游：`pandoc`（文档） / `imagemagick`（图片） / `ffmpeg`（音视频，待澄清 Q2 是否纳入）
- 选择策略：
  - PDF/MD/DOCX/HTML 互转 → `pandoc`
  - 图片格式 / 尺寸 / 透明 → `imagemagick`（注意：去底/抠图本身走 `image-gen-pro` 的 transparent 路线，不在这里做）
  - 音视频转码 / 截帧 / 拼接 → `ffmpeg`（待 Q2 拍板是否纳入）
  - OCR（PDF/图 → 文本）→ 待 Q2 拍板

## 输出归宿

所有路线统一写到 `_work/search_runs/<timestamp>-<intent>/`：

```
_work/search_runs/2026-05-27-1430-deep-research-llm-bench/
├─ plan.md           ← 本次意图、路由、参数
├─ result.md         ← 摘要与下一步
└─ artifacts/        ← 原始抓取 / 下载 / 转换产物
```

## 未来扩展（plans/007 待澄清）

- Q1：统一 CLI `search-pro <intent>` — 拍板后可在 `scripts/search-pro` 落地，本路由表作为 CLI 的子命令映射。
- Q7：`deep-research` 子路线 — 拍板后单独建 route-deep-research.md。
- Q3：RSS / sitemap diff / 定时监控 — 拍板后新增 `route-watch.md`。
