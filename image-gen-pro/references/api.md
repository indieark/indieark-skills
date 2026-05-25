# API Boundary Reference

> Load when: 需要确认真实调用、payload、provider 能力边界、dry-run 规则或 artifact 字段。
> Avoid: 只做创意 brainstorm，不涉及 CLI/API。
> Pairs with: `cli.md` 给命令模板；`provider-adapter.md` 给 adapter 分层。

本文件是运行时 API 边界入口。模型细节从 `api/README.md` 进入；当前已支持 provider payload dry-run、Codex CLI route 和 API key HTTP route。

## Current State

- 已实现：`plan` / `dry-run` 中立请求和 artifact。
- 已实现：`generate` / `edit --dry-run-payload` 的 redacted provider payload 和 media manifest。
- 已实现：`auto|codex-cli|api-key` route selection、Codex CLI route、API key HTTP route、response saving。
- 已实现：`edit --prepare-local-media auto|off` 的本地图片校验、prepared-media 副本和 manifest 记录。
- 已实现：本地 `job.json` 和 `jobs list|show|wait|delete` 状态层。
- 已实现：`gpt-image-2` 默认模型、NB 模型入口、NB async task polling、MJ submit/poll 绘图入口，以及显式 base URL 前缀支持。
- 未实现：GPT 远端轮询/状态、NB 远端取消、MJ 高级动作、可选 SDK adapter、更细 provider-specific 错误映射。

## API Rules

- provider-specific 参数只写在 provider-specific reference 和 provider adapter，不写进 core neutral workflow。
- API key 只从安全来源读取，不写入 artifact，不进入日志。
- `--dry-run-payload` 必须不访问网络。
- `auto` route 按 CLI config 的 `route_priority` 尝试；默认 preset 可设为 Codex CLI 优先或 API key 优先。
- GPT/NB 的 Images-compatible `api-key` route 通常是同步生成：返回图片响应后写出文件，不提供远端 task id 或可轮询进度。例外是兼容异步代理返回 `taskId/PENDING` 时，adapter 会在配置的 base URL 前缀下轮询 `/task/<task-id>`；CLI 不自动探测项目专属前缀。
- MJ route 是单独 submit/poll 契约，可记录 `remote_task`；不要把它套进 `/v1/images/*` 字段模型。
- 不要为同步 Images-compatible route 伪造远端进度；`jobs` 只表示本地 run/job 状态，除非 provider adapter 显式记录了 remote task。
- core CLI 不强制安装 provider SDK；SDK adapter 只能作为可选增强。
- artifact 保存 redacted request、response 摘要、输出文件路径和错误类型。
- 输入素材 manifest 记录路径、大小、hash、MIME 或 URL 摘要；本地 edit 图片可复制到 run 目录用于本次 route，但 `_work/` 不进入 Git。

## Future Operations

| Operation | Purpose | Artifact |
| --- | --- | --- |
| `generate --dry-run-payload` | 构造文生图 provider payload 不提交 | prompt, redacted payload, media manifest, summary |
| `edit --dry-run-payload` | 构造图像编辑 provider payload 不提交 | prompt, media manifest, redacted payload, summary |
| `generate --route codex-cli` | 通过本机 `codex` CLI 尝试真实生成 | prompt, session file summary, result summary, outputs |
| `edit --route codex-cli` | 通过本机 `codex` CLI 和 reference image 尝试真实编辑 | prompt, media manifest, session file summary, result summary, outputs |
| `generate --route api-key` | 文本生成图片真实提交 | prompt, redacted payload, result summary, outputs |
| `edit --route api-key` | 输入图像编辑真实提交 | prompt, media manifest, redacted payload, result summary, outputs |
| `show-run` | 查看历史 run | manifest, generation log |

## Adapter Checklist

- model defaults and override rules
- credential resolution
- route selection
- request builder
- local input validation
- redaction
- response parser
- image output writer
- stable error mapping
- mock tests and manual smoke test notes
