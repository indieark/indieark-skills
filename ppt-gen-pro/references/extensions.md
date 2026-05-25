# Extensions

Load when: 需要说明三种外部 PPT 生成路线、安装来源或委托边界。
Avoid: 不要复制外部仓库代码到本 Skill；不要绕过 route gate。
Pairs with: `router.md`, `install.md`, `capability-matrix.md`

## Extension Registry

| Route                 | Source                                                            | Local checkout                              | Runtime Skill entry                                                            | locked_commit | verified_date  |
| --------------------- | ----------------------------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------ | ------------- | -------------- |
| `image-first-ppt`     | `https://github.com/NyxTides/ppt-image-first`                     | `extensions/ppt-image-first`                | `extensions/ppt-image-first/SKILL.md`                                          | `(unset)`     | `(unverified)` |
| `web-html-ppt`        | `https://github.com/op7418/guizang-ppt-skill`                     | `extensions/guizang-ppt-skill`              | `extensions/guizang-ppt-skill/SKILL.md`                                        | `(unset)`     | `(unverified)` |
| `svg-ppt`             | `https://github.com/hugohe3/ppt-master`                           | `extensions/ppt-master`                     | `extensions/ppt-master/skills/ppt-master/SKILL.md`                             | `(unset)`     | `(unverified)` |
| `academic-image-ppt`  | `https://github.com/fangyuanopus/literature-report-ppt-builder`   | `extensions/literature-report-ppt-builder`  | `extensions/literature-report-ppt-builder/academic-slide-minimalist/SKILL.md`  | `8fe01a4`     | `2026-05-25`   |
| `design-html-ppt`     | `https://github.com/alchaincyf/huashu-design`                     | `extensions/huashu-design`                  | `extensions/huashu-design/SKILL.md`                                            | `9100be3`     | `2026-05-25`   |
| `video-html-ppt` (L2) | `https://github.com/ConardLi/garden-skills`                       | `extensions/garden-skills`                  | `extensions/garden-skills/skills/web-video-presentation/SKILL.md`              | `ea0c0c8`     | `2026-05-25`   |

- `locked_commit`：该扩展上次验证通过后锁定的 Git commit SHA（短 7 位即可）。填写后，安装脚本应 `git checkout <locked_commit>` 而不是 pull 到 latest；`(unset)` 表示跟随 upstream default branch。
- `verified_date`：上次人工端到端验证该扩展与 ppt-gen-pro router 兼容性的日期（`YYYY-MM-DD`）；`(unverified)` 表示尚未完成首次验证。

## 版本锁定

`scripts/install_extensions.py` 是 lock/freshness 的真源：

- 表中 `locked_commit` 和 `verified_date` 是给人/Agent 看的镜像，**真值写在 `scripts/install_extensions.py` 的 `EXTENSIONS` 列表里**。
- 验证扩展兼容性后必须同时更新两处，避免脱节。

### 默认行为

不带标志运行 `python scripts/install_extensions.py` 时，所有 route 都跟随 upstream default branch（`git pull --ff-only`）。用户安装/更新时拿到的是上游最新提交，`locked_commit` 不参与。

### 工作流标志

| 场景 | 命令 | 行为 |
| ---- | ---- | ---- |
| 开发、想吃 upstream 最新 | `python scripts/install_extensions.py` | clone --depth 1 或 git pull --ff-only |
| CI / 发版要可复现 | `python scripts/install_extensions.py --locked` | 按 EXTENSIONS 中 `locked_commit` 做 fetch + checkout；未填的 route 仍跟 latest |
| 升级 lock 到当前 upstream | `python scripts/install_extensions.py --update-lock` | 先 git pull --ff-only，然后输出当前 commit SHA + 今天日期，由你手动写回 EXTENSIONS 和本表 |
| 检查 lock 新鲜度 | `python scripts/install_extensions.py --check-freshness` | 列出 `verified_date` 缺失或距今 > 90 天的 route（stderr WARN，不阻塞退出码） |

### 锁定规则

- 扩展 upstream 有 breaking change 前，`locked_commit` 保持不变；`--locked` 安装时使用该 commit 而不是 `git pull`。
- 需要跟进 upstream 时，先在测试环境跑 `--update-lock` 拿新 SHA → 端到端验证新 commit 兼容 → 把 SHA 和当日日期写回 EXTENSIONS + 本表。
- 若 `verified_date` 距今超过 90 天，进入 Skill 工作流前建议先重新验证；Agent 应在委托前调用 `--check-freshness` 并提示用户。
- `--update-lock` 不会自动改本 Markdown 表格，避免脚本破坏表格格式；脚本只输出建议值，由人手动落字。

## Update Contract

- `extensions/` stores live Git checkouts, not copied snapshots.
- Keep each extension's `.git` directory so it remains updateable.
- Re-running `python scripts/install_extensions.py` updates existing checkouts with `git pull --ff-only`.
- Do not ask the user to manually update each upstream extension unless automatic update fails and the error must be resolved by hand.
- Use `Local checkout` for updating and source inspection; use `Runtime Skill entry` for delegation after the user chooses a route.

## Route Roles

### Image-First PPT

Use `NyxTides/ppt-image-first` as the default standard PPT route for conversation-first, image-first decks where the page is treated as a high-fidelity visual image and then packaged into PPTX.

### Web / HTML PPT

Use `op7418/guizang-ppt-skill` for main text, speech content, storytelling, animation, single-file HTML slide decks, magazine style, Swiss style, talks, covers, and presentation images.

### Design HTML PPT

Use `alchaincyf/huashu-design` 当用户要的是**高保真原型 / 设计稿 mockup / launch film 级品牌动画 / 设计评审 deck**，或需要 **HTML deck + 原生多格式导出（MP4 / PPTX / PDF）**。它与 `web-html-ppt` 同为 HTML deck 路线，但带自己的工具链（12 脚本）。

输出形态：单文件 HTML + 可选 MP4 / PPTX / PDF 导出。区别于 `web-html-ppt`：

- **多格式导出**：自带 `render-video.js`（HTML → MP4）/ `html2pptx.js`（HTML → 原生 PPTX）/ `export_deck_pdf.mjs`（HTML → PDF），不依赖外挂工具。
- **设计治理层（v0.3.0 暂未启用，留 v0.4.0）**：20 设计哲学 + 5 维评审。
- **TTS provider caveat**：自带 `tts-doubao.mjs`，锁定豆包（火山引擎 openspeech）TTS。用户没豆包 API key 时跳过 TTS，仍可出无声 MP4 / PDF / PPTX。

适合：高保真原型、设计稿 mockup、launch film 级品牌动画、设计评审 deck、需要 MP4 / 原生 PPTX / PDF 多格式导出的场景。

不适合：纯主文字演讲（走 `web-html-ppt` 更轻量）、论文证据汇报（走 `academic-image-ppt` 有图源铁律）、需要 PowerPoint 对象级编辑（走 `svg-ppt`）。

### SVG PPT

Use `hugohe3/ppt-master` when the user explicitly needs natively editable PPTX, real PowerPoint shapes, native animations, PowerPoint object-level editing, future co-editing, or SVG/PPTX engineering export.

### Video HTML PPT（L2 后操作路线）

Use `ConardLi/garden-skills/skills/web-video-presentation` 当用户已经选了 `web-html-ppt` 作 L1 路线，并且明确要进入「按视频节奏播放 / 录屏 / 旁白配音 / 一屏一镜 / 自动播放」等后操作时。

形态约束：

- **仅适用 web-html-ppt**：image-first / svg / academic 路线的产物不适合 HTML 视频化录屏；design-html-ppt 自带 `render-video.js`，无需 L2。
- **轻 scaffold**：上游是 scaffold.sh + 模板 + 方法论文档，本身**不带** render-video 或 TTS 实现；实际 MP4 输出 / TTS 由 Agent 主机环境组装（与 design-html-ppt 的豆包 TTS 锁定形成对比）。
- **触发模型**：路由器先按 L1 路线推 web-html-ppt，再检测 L2 触发词命中后预览 L2 选项；不触发词命中不打扰。

适合：演讲型 HTML deck 完成后需要录屏成 MP4 / 一屏一镜节奏 / 主机自备 TTS 旁白配音。

不适合：image-first / svg / academic 已是图片或对象级 PPTX，没有 HTML 容器去录屏；design-html-ppt 已自带视频化工具链。

### Academic Image PPT（领域特化路线）

Use `fangyuanopus/literature-report-ppt-builder`（内部 skill 名 `academic-slide-minimalist`）when the user is preparing a literature report, paper group meeting, journal club, thesis defense rehearsal, or any deck where the central content is a published paper plus its supplementary information.

输出形态和 `image-first-ppt` 同源（都是 image-first PPTX），区别在内容约束和工作流：

- **图源铁律**：只允许使用论文主文图、SI / Supporting Information 图、用户上传的截图或既有 PPT 页面；**禁止**生成或重绘任何实验数据图（分子结构 / 晶体 / 光谱 / 显微 / XRD / NMR / 性能曲线 / 反应机理等）。
- **工作流**：close reading → paper logic tree → terminology table → main/SI evidence crosswalk → figure source manifest → adaptive navigation → deck order map → page briefs → image2 page generation → PPTX assembly → render audit / Q&A prep。
- **必带交付物**：`figure_source_manifest.md`、`speaker_notes.md`、`backup_slides.md`、`question_prep.md`。
- **不适合**：商业路演、产品发布、纯视觉概念页、伪造或重绘实验数据。

什么时候**不**走这条路线（即使用户说"做 PPT"）：纯商业 / 产品 / 路演 / 自媒体场景，即使有学术参考资料但不以论文证据链为主线时，仍然走 `image-first-ppt`。

## Delegation Contract

- `ppt-gen-pro` owns trigger, recommendation, user choice, installation check, and final reporting.
- The selected extension owns its own detailed workflow and generation mechanics.
- After route choice, open exactly the selected route's `Runtime Skill entry`; do not infer a different path from the repository name.
- Do not mix two routes in one execution unless the user explicitly asks for a hybrid workflow.
- If an extension is missing or stale, install or update it before delegation.
