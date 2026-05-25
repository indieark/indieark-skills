# Completion Response Reference

> Load when: 生成任务提交、等待、下载或失败后，需要向用户汇报结果。
> Avoid: 只在执行前做路由、写 prompt 或解释 API，还没有运行或验收结果。
> Pairs with: `router.md` 的验证路径；`cli.md` 的 artifact 说明；`iteration.md` 的反馈修正。

本文件定义生成完成后的用户回复格式。目标是让用户能立刻看到结果、输入、素材、证据和下一步，而不是只收到一个 URL。

完成回复恢复为 HTML 之前的标准文本格式。若任务使用 `generation-workflow.md` 的结构化流程复盘，完成回复要说明用户下一步可选择认可、下载、退回某阶段或只改 1-3 个点，并在需要时附上结构化 JSON 修改语义。不要生成或引导用户打开 HTML 交互页。

## 成功回复

成功生成或已等待完成时，按这个顺序回复：

```text
已生成

- 视频：<本地 MP4 路径优先；没有下载才给 content.video_url>
- 任务：<task_id>
- 参数：<CLI 子命令 / 模型 / 画幅 / 时长 / 有声或无声>
- 项目：<如果有 project_id/storyboard_id，说明项目、故事板、是否已确认>
- 提示词：<实际提交的 prompt；太长时给摘要 + prompt.txt 路径>
- 声音：<有声/无声；音乐、环境音、动作音效、对白或参考音频用途摘要>
- 素材：<使用的图片/视频/音频清单，含角色、编号、处理状态>
- 证据：<run_dir；列出关键 artifact>
- 验收：<是否符合用户目标；若有偏差，下一轮改哪 1-3 处>
- 复盘：<文本验收和下一步；需要修改时给出 workflow_stage / target_stage / requested_changes 的结构化 JSON 摘要>
```

## 输入内容

结果汇报必须包含实际输入，而不是只说“已使用素材”。

### 项目和故事板

如果运行使用 `--project` 或 `--storyboard`，回复必须包含：

- `project_id` 和项目标题。
- `storyboard_id`、故事板状态和是否 approved。
- 故事板图片来源或本地路径摘要。
- `storyboard-prompt.txt` 和 `video-prompt.txt` 路径。
- 如果是脚本拼版故事板，说明原子图片数量、composition manifest / 拼版清单路径，以及最终 4K 故事板图片。
- `generation-record.json` 路径，或可执行的 `seedance2 history show <project_id> <run_id>`。

### 提示词

- 优先展示实际提交的 prompt。
- 如果 prompt 很长，先给 3-6 行摘要，再给 `prompt.txt` 的本地路径。
- 如果 prompt 来自 `--prompt-file`，说明使用了哪个文件，并确认 CLI 已把提交内容保存到 `prompt.txt`。
- 如果 `generate_audio=true`，提示词摘要必须包含声音设计；如果没有，验收里标记为下一轮需要修正。
- 如果 `media-manifest.json` 有 `prompt_reference_warnings`，必须在验收里指出哪些参考素材没有在 prompt 中写清用途。

### 声音设计

有声任务必须汇报：

- `generate_audio` 是 `true` 还是 `false`。
- 音乐、环境音、动作音效、对白/无对白的实际提交摘要。
- 如果使用 `参考音频1`，说明它用于节奏、音色、情绪还是对白。
- 如果用户要求精确音效但本次只通过 Seedance prompt 表达，说明仍需听感验收，必要时下一轮只改 1-3 个声音点。

### 素材清单

素材清单至少包含：

| Field | Meaning |
| ----- | ------- |
| 编号 | `参考图1` / `参考视频1` / `参考音频1` / `首帧` / `尾帧` |
| 用途 | 用户或 prompt 中定义的素材角色 |
| 来源 | 本地路径、HTTPS URL、signed URL 或 `asset://` 的安全摘要 |
| 处理 | 原样使用、Base64、自动修复、转码、截断、Cloudflare tunnel |
| 证据 | `media-manifest.json` 中可复查的记录 |

不要泄露私有 signed URL 的完整 query string。必须展示时只保留域名、文件名或安全摘要，并把完整值留在本地 artifact。

## 证据清单

回复里必须给出 run directory，并按实际存在情况列出：

- `prompt.txt`
- `request-payload-redacted.json`
- `media-manifest.json`
- `generation-log.json`
- `project-generation.json` 或项目目录下的 `generation-record.json`（如果使用项目库）
- `submit-summary.json`
- `task-result.json`
- 下载后的本地 MP4 路径

不要把完整 JSON artifact 贴给用户；只摘关键字段。用户需要复盘时，让用户打开本地文件。

## 未完成或失败回复

失败、超时、未等待完成或下载失败时，按这个顺序回复：

```text
未完成

- 阶段：<提交前 / 提交后 / 等待中 / 上游失败 / 下载失败>
- 原因：<CLI 错误摘要；不贴敏感信息>
- 输入：<实际 prompt 摘要 + 素材清单>
- 已保存：<run_dir 和已存在 artifact>
- 下一步：<补 key / 换素材 / 重试 wait / 下载 / 定向改 prompt>
```

如果任务已经提交但没有等完，不要说“生成失败”。应返回 `task_id`、当前状态和下一条可执行命令，例如 `seedance2 wait <task_id> --download outputs`。

## 隐私和安全

- 不输出 API Key、Authorization header、完整 signed URL、完整私有素材下载地址。
- 不把 `.env`、原始商业素材或输出 MP4 路径建议提交到 Git。
- 可以输出本地路径，因为用户和 Agent 在同一台机器上；但商业素材路径只作为复盘证据，不做公开外链。
- 如果使用 Cloudflare tunnel，只汇报它用于本次临时本地视频暴露，并确认命令结束后已关闭。

## 简短模板

信息很多时仍保持简短，默认 7 行以内；用户要求详细复盘时再展开。

```text
已生成。
视频：C:\...\outputs\<task_id>.mp4
任务：<task_id>；参数：omni / 720p / 9:16 / 8s / 有声
提示词：已按“参考图1=角色外观，参考视频1=动作节奏...”提交；完整见 <run_dir>\prompt.txt
声音：轻快电子节拍 + 产品点击音；无对白；参考音频1只用于鼓点节奏
素材：参考图1=<file> 原样/修复；参考视频1=<file> tunnel/转码；参考音频1=<file> 截断
证据：<run_dir>（payload、manifest、generation-log、task-result 均已保存）
验收：基本符合目标；下一轮建议只调节动作速度和结尾停顿。
```
