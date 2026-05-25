# Post-Processes (L2)

Load when: 用户在 L1 路线（生成形态）之外，明确要"视频化 / 录屏 / 旁白配音 / 按视频节奏播放"等后操作。
Avoid: 不要把 L2 当成 L1 备选；L1 没选定不进入 L2 决策。
Pairs with: `router.md`, `route-introduction.md`, `extensions.md`, `flows.md`, `capability-matrix.md`

> **二层架构定位**：ppt-gen-pro 的路由从 v0.3.0 起分两层：
> - **L1 · 路线层（generation route）** = deck 的生成形态（image-first / web-html / design-html / svg / academic）
> - **L2 · 后操作层（post-process）** = 在 L1 产物之上的二次加工（视频化 / 录屏 / 多格式导出）
>
> 本文件是 L2 的真源文档；L1 真源是 `router.md` + `route-introduction.md`。

## L2 Registry

| L2 名称 | 上游 | 适用 L1 路线 | 形态 | 触发模型 |
|---|---|---|---|---|
| `video-html-ppt` | `ConardLi/garden-skills/skills/web-video-presentation`（locked `ea0c0c8` / verified 2026-05-25） | **仅 `web-html-ppt`** | scaffold + 模板 + 方法论；render-video / TTS 由 Agent 主机环境组装 | 触发词命中时纳入"介绍选择"预览 |
| design 自带导出工具链 | `huashu-design`（v0.3.0 已 L1） | **仅 `design-html-ppt`**（路线内置） | `render-video.js` / `html2pptx.js` / `export_deck_pdf.mjs` / `tts-doubao.mjs` | L1 介绍阶段说明，不走 L2 菜单 |

design 自带工具链不算独立 L2，因为它绑死在 `design-html-ppt` 路线内部、不能被其他 L1 复用。它在表中只是为了说明"L2 不必为 design 重复登记"。

## 适用范围（Q-C1 + Q-P1-a 决策）

L2 仅限以下 L1 路线：

- ✅ `web-html-ppt`：HTML deck 有真实 DOM 容器，可被 Headless Chromium 录屏成 MP4，可注入主机 TTS 旁白。
- ❌ `image-first-ppt` / `academic-image-ppt`：产物是 image2 嵌入式 PPTX，没有 HTML 容器；视频化要重新做整套生成。
- ❌ `svg-ppt`：产物是原生 PPT 对象，视频化路径是 PowerPoint 原生导出，不走 HTML 工具链。
- ❌ `design-html-ppt`：路线自带 `render-video.js`，不走 L2 链路。

新增 L2 时必须显式登记适用 L1 范围，避免"广泛适用"假设。

## 触发模型（Q-B + Q-P1-a 决策）

**触发词命中预览**：路由器在 L1 推荐句之后，扫描用户消息是否命中以下 L2 触发词；命中即在介绍阶段附加 L2 选项预览。**没触发词的请求不打扰**。

### `video-html-ppt` 触发词

| 类别 | 触发词样例 |
|---|---|
| 视频节奏 | 按视频节奏 / 一屏一镜 / 自动播放 / video pace |
| 录屏 | 录屏 / 屏幕录制 / screen capture / screencast |
| 旁白 | 旁白 / 配音 / 解说 / narration / voiceover |
| 视频成品 | 视频版 / 视频化 / 出片 / 转 MP4 |

### 与 L1 触发词的仲裁规则

| 用户表达 | 仲裁 |
|---|---|
| 「设计动画 + 视频 / 设计稿出片」 | 走 L1 `design-html-ppt`（自带视频化），**不进** L2 |
| 「演讲网页 PPT + 后续要录成 MP4」 | L1 `web-html-ppt` + L2 `video-html-ppt`（介绍阶段并列展示） |
| 「MP4 / PPTX / PDF 多格式导出」 | 走 L1 `design-html-ppt`（自带 3 格式工具链），不进 L2 |
| 「PPT 视频版」无上下文 | 询问 deck 形态偏好：演讲 → L1 web + L2 video / 设计稿 → L1 design |
| 「TTS / 旁白配音」 | design 走豆包（路线内置）/ web-html 走 L2 video-html-ppt（主机自备） |

## 委托契约

- L2 委托必须在 L1 选定之后；不允许"先 L2 后 L1"反向流程。
- L2 入口：`extensions/garden-skills/skills/web-video-presentation/SKILL.md`。
- L2 上游若 unverified 或 stale（`verified_date` 缺失或 > 90 天），先按 `extensions.md` 的「锁定规则」走 `--check-freshness` 后再委托。
- L2 不接管 L1 的生成职责；它仅在 L1 产物之上加工。

## 与 capability-matrix 的对齐

`capability-matrix.md` 的「L2 后操作支持」行是路线 × L2 维度的索引：

- `web-html-ppt`：✅ `video-html-ppt`（v0.3.0 引入；录屏 + 主机 TTS）
- 其他 L1：❌（具体原因见上方「适用范围」）

「MP4 导出」/「TTS provider」等多格式 / 配音相关能力的真源也仍在 capability-matrix；本文件只负责 **L2 概念定义 + 触发模型 + 仲裁规则**。

## 维护契约

- 新增 L2 后操作时：先在本表 + capability-matrix 加行，再在 `router.md` §3 加触发词，最后在 `flows.md` 加状态机分支。
- L2 触发词新增 / 变更时：同步 `scripts/test_router.py` 的 `L2_TRIGGERS_*` 常量与回归用例。
- L2 上游变更（locked_commit / verified_date）时：同步 `scripts/install_extensions.py` 的 EXTENSIONS 列表与 `extensions.md` Registry 表，两处必须一致。
