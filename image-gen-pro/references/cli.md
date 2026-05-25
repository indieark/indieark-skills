# CLI Reference

Load when changing or using the CLI.

## Normal-Use Rule

Do not run `imagen --help` for normal generation/editing. Do not use `imagen --help` to determine config/readiness. This file is the command surface SSOT. Use `--help` only when adding/changing CLI options, investigating an argparse failure, or resolving a conflict between this reference and the installed command.

For config preflight before real execution, use `imagen config list` plus `imagen doctor` / `imagen doctor --model <model>`; the runtime protocol lives in `routes.md`.

Use installed commands as `imagen ...`. Use `python scripts\imagen.py ...` only when working inside this repository.

## Commands

```powershell
python scripts\imagen.py setup --non-interactive --provider placeholder
python scripts\imagen.py setup --non-interactive --default-model nano-banana-2
python scripts\imagen.py setup --non-interactive --route-preset codex-cli-first
python scripts\imagen.py setup --non-interactive --route-preset api-key-first
python scripts\imagen.py setup --non-interactive --api-key "<provider-api-key>" --base-url "https://api.openai.com"
python scripts\imagen.py doctor
python scripts\imagen.py doctor --model gpt-image-2
python scripts\imagen.py doctor --model nano-banana-2
python scripts\imagen.py doctor --model mj
python scripts\imagen.py doctor --api-key "<one-command-key>" --base-url "http://127.0.0.1:8080/v1"
python scripts\imagen.py config path
python scripts\imagen.py config list
python scripts\imagen.py config get default_provider
python scripts\imagen.py config get default_model
python scripts\imagen.py config get api_key
python scripts\imagen.py config set default_provider placeholder
python scripts\imagen.py config set default_model mj
python scripts\imagen.py config set default_route auto
python scripts\imagen.py config set enabled_routes api-key,codex-cli
python scripts\imagen.py config set route_priority api-key,codex-cli
python scripts\imagen.py config set batch_dir _work/image_gen_batches
python scripts\imagen.py config set api_key "<provider-api-key>"
python scripts\imagen.py config set base_url "http://127.0.0.1:8080/v1"
python scripts\imagen.py runs list --limit 20
python scripts\imagen.py runs show <run-id>
python scripts\imagen.py jobs list --limit 20
python scripts\imagen.py jobs show <run-id>
python scripts\imagen.py jobs wait <run-id> --timeout-sec 0
python scripts\imagen.py jobs delete <run-id>
python scripts\imagen.py batches run --file .\batch.json
python scripts\imagen.py batches run --file .\batch.json --batch-id product-icons-001 --resume
python scripts\imagen.py batches run --file .\batch.json --dry-run-payload
python scripts\imagen.py batches run --file .\batch.json --concurrency 7
python scripts\imagen.py batches list --limit 20
python scripts\imagen.py batches show <batch-id>
python scripts\imagen.py transparent --input .\source.png --output .\transparent.png --background auto
python scripts\imagen.py transparent --input .\source.png --output .\transparent.png --background "#ff00ff" --metadata-file .\transparent.metadata.json
python scripts\imagen.py transparent --input .\source.png --output .\transparent.png --background auto --min-island-area 64 --edge-decontaminate-strength 0.78
python scripts\imagen.py plan --prompt "..." --provider placeholder
python scripts\imagen.py plan --prompt-file .\prompt.txt --provider placeholder
python scripts\imagen.py dry-run --prompt "..." --provider placeholder
python scripts\imagen.py generate --prompt "..." --dry-run-payload
python scripts\imagen.py edit --prompt "..." --image .\input.png --dry-run-payload
python scripts\imagen.py edit --prompt "..." --image .\input.png --mask .\mask.png --prepare-local-media auto --dry-run-payload
python scripts\imagen.py edit --prompt "..." --image .\input.png --prepare-local-media off --dry-run-payload
python scripts\imagen.py edit --prompt "图生图：基于源图生成一版新图，保持主体结构并调整风格" --image .\input.png --route auto --output-file .\outputs\image-to-image.png
python scripts\imagen.py generate --prompt "..." --route codex-cli --output-file .\outputs\image.png
python scripts\imagen.py generate --prompt "..." --route api-key --output-file .\outputs\image.png
python scripts\imagen.py generate --model nano-banana-2 --prompt "..." --route api-key --output-file .\outputs\nb.png
python scripts\imagen.py generate --model mj --prompt "... --ar 16:9" --route api-key --output-file .\outputs\mj.png
python scripts\imagen.py edit --prompt "..." --image .\input.png --route auto --output-file .\outputs\edit.png
python scripts\imagen.py edit --model nano-banana-2 --prompt "..." --image .\input.png --route api-key --output-file .\outputs\nb-edit.png
python scripts\imagen.py version
```

Installed form:

```powershell
imagen doctor
imagen doctor --model gpt-image-2
imagen config list
imagen config get default_model
imagen config get api_key
imagen config set default_model nano-banana-2
imagen setup --non-interactive --route-preset api-key-first
imagen setup --non-interactive --api-key "<provider-api-key>" --base-url "https://api.openai.com"
imagen config set route_priority api-key,codex-cli
imagen generate --prompt "..." --route api-key --api-key "<temporary-key>" --base-url "http://127.0.0.1:8080/v1" --output-file .\outputs\image.png
imagen doctor --model mj
imagen generate --model mj --prompt "... --ar 1:1" --route api-key --output-file .\outputs\mj.png
imagen generate --model mj --prompt "... --v 8.1 --hd --ar 1:1" --route api-key --output-file .\outputs\mj.png
imagen edit --prompt "..." --image .\input.png --route auto --output-file .\outputs\edit.png
imagen batches run --file .\batch.json --dry-run-payload
imagen batches run --file .\batch.json --concurrency 7
imagen batches run --file .\batch.json --batch-id product-icons-001 --resume
imagen batches show product-icons-001
```

## Input Contract

- `--provider` only accepts `placeholder` in the current phase.
- `generate` / `edit` use config `default_model` when `--model` is omitted; the initial default is `gpt-image-2`.
- `--model` accepts `gpt-image-2`, `nano-banana`, `nano-banana-2`, `nb`, and `mj`; `nano-banana` / `nb` normalize to `nano-banana-2`.
- Use either `--prompt` or `--prompt-file`; the prompt must not be empty.
- `--prompt-file` is read as UTF-8 text.
- `--reference` may be repeated.
- Local references must exist and be files; the CLI records path, size, and SHA-256.
- HTTP(S) references are not fetched; query strings and fragments are stripped before writing artifacts.
- `generate` / `edit --dry-run-payload` builds payload artifacts without network or credentials.
- `setup --route-preset` accepts `codex-cli-first`, `api-key-first`, `codex-cli-only`, or `api-key-only`.
- `setup --default-model` and `config set default_model` persist the user's preferred default model.
- `config list` plus `doctor` / `doctor --model <model>` are the authoritative readiness checks before real execution; `--help` is not a config check.
- `setup --default-model` does not reset existing route preferences unless `--route-preset` is also passed.
- `setup --api-key` and `setup --base-url` persist API route credentials into the local CLI config. `config set api_key` and `config set base_url` do the same.
- `default_model`, `default_route`, `enabled_routes`, and `route_priority` define the user's normal generation preference.
- API key resolution: `--api-key` > model-specific env > `IMAGE_GEN_PRO_API_KEY` > config `api_key`.
- Base URL resolution: `--base-url` > model-specific env > `IMAGE_GEN_PRO_API_BASE_URL` > config `base_url` > `https://api.openai.com`.
- Configured `base_url` is canonicalized to provider root/prefix: trailing `/` and terminal `/v1` are removed when saving; runtime appends the model endpoint.
- Model-specific env names are `IMAGE_GEN_PRO_GPT_IMAGE_2_API_KEY`, `IMAGE_GEN_PRO_NANO_BANANA_API_KEY`, `IMAGE_GEN_PRO_MJ_API_KEY`, with matching `_API_BASE_URL` names.
- `OPENAI_API_KEY` is not an image-gen-pro credential source.
- `--api-key` / `--base-url` are one-command temporary overrides and do not write config by themselves.
- `imagen config list`, `imagen config get api_key`, and `imagen doctor` mask API keys. Run artifacts record only `api_key_source` / `base_url_source`, never the key value.
- `runs list|show` reads saved artifacts from configured `run_dir` and returns JSON for Skill reporting.
- `jobs list|show|wait|delete` manages local `job.json` state only; it does not imply remote provider progress or cancellation.
- `batches run|list|show` is the stable batch generation system. It reads a JSON manifest, writes persistent batch state, and executes each item through the existing `generate` / `edit` route handling.
- Batch manifests must contain at least 3 items. Batch concurrency is bounded to 1-7 workers and defaults to 5. CLI `--concurrency` overrides top-level manifest `concurrency` for the current run.
- Batch manifests must not contain `api_key` or `base_url`; credentials still come from env/config or single-command non-batch tests.
- `batches run --resume` skips already succeeded items, but only when the manifest `request_sha256` matches the original batch request.
- Batch artifacts are stored under configured `batch_dir`, default `_work/image_gen_batches`; per-item run artifacts still use configured `run_dir`.
- `transparent` post-processes a local chroma-background image into PNG with alpha; it requires Pillow, never overwrites the input, preserves canvas size, and writes metadata describing the generation-plus-post-processing transparency route.
- `transparent` default edge cleanup removes opaque background-like halo pixels, runs RGB-only 去污染 for semi-transparent/chroma-contaminated edge RGB, and does not default to alpha feather.
- Option `--min-island-area` enables opt-in 连通域小岛清理 for tiny detached foreground fragments.
- Option `--edge-decontaminate-strength` controls edge RGB neutralization strength; the default is `0.78`.
- `generate` / `edit --route codex-cli` uses the local `codex` command for `gpt-image-2`, extracts the image from new session rollout files, then deletes those rollout files and records only a redacted session summary plus cleanup result.
- `generate` / `edit --route api-key` submits through the standard-library HTTP adapter.
- `gpt-image-2` and `nano-banana-2` use `/v1/images/generations` and `/v1/images/edits`; NB edit uses repeated `image` multipart fields.
- Base URL prefixes are explicit: set the shared or model-specific base URL to the provider root or mounted prefix; the CLI does not probe project-specific fallback paths.
- `nano-banana-2` also supports async proxy responses: if submit returns `taskId` + `PENDING`, the CLI polls `/task/<task-id>` under the configured base URL prefix and records `remote_task`.
- `mj` uses `/mj/submit/imagine` plus `/mj/task/<task-id>/fetch`, sends `mj-api-secret`, and records `remote_task` when a task id is returned.
- MJ native parameters are prompt text. Include `--v 8.1 --sd` or `--v 8.1 --hd` in `--prompt` when that is the desired MJ behavior; CLI `--quality` stays `auto` for MJ.
- `generate` / `edit --route auto` follows configured `route_priority`; an explicitly disabled route is rejected.
- `generate` rejects edit-only inputs such as `--image` and `--mask`.
- 图生图 / image-to-image / 以图改图 maps to `edit`, not `generate`: `edit` requires at least one local `--image`; `--mask` is optional and edit-only.
- GPT `--mask` follows the official Images Edit rule: same format and dimensions as the first `--image`, each submitted file less than 50MB, alpha channel required; mask guidance is prompt-based.
- `edit` defaults to `--prepare-local-media auto`: local PNG/JPEG/WebP inputs are inspected and copied into the run directory before route submission.
- `--prepare-local-media off` keeps the older path/hash-only behavior for debugging or intentionally unsupported local files.
- `gpt-image-2` provider payloads reject `background=transparent`.
- `output_compression` is only valid with `--output-format jpeg|webp`.

## Exit Codes

- `0`: success
- `2`: usage error
- `3`: configuration error
- `5`: runtime error

## Artifact Files

`plan` and `dry-run` write:

- `prompt.txt`
- `request.json`
- `manifest.json`
- `summary.json`
- `generation-log.json`
- `job.json`

`generate` and `edit --dry-run-payload` write:

- `prompt.txt`
- `request-payload-redacted.json`
- `media-manifest.json`
- `summary.json`
- `generation-log.json`
- `edit --prepare-local-media auto` also writes prepared input copies under `prepared-media/`.

Real `generate` and `edit` also write:

- `result.json`
- output image files in `outputs/` or the requested `--output-file`
- output records in `summary.json`, `result.json`, `media-manifest.json`, and `generation-log.json` include actual `width`, `height`, `resolution`, and `aspect_ratio` when the saved image can be inspected.
- single-output runs set `preview.path` to the output image; multi-output runs write `preview/contact-sheet.png` when Pillow is available and record it as `preview.kind=contact_sheet`.

`batches run` writes:

- `_work/image_gen_batches/<batch-id>/request.json`
- `_work/image_gen_batches/<batch-id>/state.json`
- `_work/image_gen_batches/<batch-id>/summary.json`
- per-item normal run artifacts under configured `run_dir`
- final state and summary include the effective `concurrency`
- final state and summary include a batch-level `preview` when succeeded items produced image outputs; multiple images are combined into a contact-sheet preview when Pillow is available.

`transparent` writes:

- transparent PNG at `--output`
- metadata JSON at `--metadata-file` or `<output-stem>.metadata.json`
- optional checkerboard preview PNG at `--preview-file`

## 快捷速查（中文）

只有在新增/修改 CLI 参数、调试 parser 报错、或本参考与实际命令冲突时，才用 `--help` 复核；正常生成不要先跑 `--help`。

- 已安装环境优先用 `imagen ...`；仓库开发/测试可用 `python scripts\imagen.py ...`。
- 文生图：`imagen generate --prompt "..." --route auto --output-file .\outputs\name.png`
- 图生图/编辑：`imagen edit --prompt "..." --image .\input.png --route auto --output-file .\outputs\edit.png`
- 默认模型可用 `imagen config set default_model gpt-image-2|nano-banana-2|mj` 配置；未传 `--model` 时使用 config 的 `default_model`，初始值是 `gpt-image-2`。NB 用 `--model nano-banana|nano-banana-2|nb`；MJ 用 `--model mj`。
- 非 `gpt-image-2` 模型优先走 `api-key` route；`codex-cli` 当前只支持 `gpt-image-2`。
- NB 仍走 `/v1/images/*` 兼容代理；MJ 走 `/mj/submit/imagine` + `/mj/task/<id>/fetch`，不要套用 Images API payload。
- 如果 API 挂在额外前缀下，必须把前缀显式写进共享或模型专属 base URL；CLI 不自动猜测项目后端前缀。NB async `taskId/PENDING` 轮询和 MJ submit/poll 都相对于配置的 base URL 执行；MJ V8.1 的 `--sd` / `--hd` 放在 prompt 里。
- payload dry-run：`imagen generate|edit ... --dry-run-payload --run-id <id>`
- 首次设置：`imagen setup --non-interactive --default-model gpt-image-2|nano-banana-2|mj --route-preset api-key-first|codex-cli-first|api-key-only|codex-cli-only`
- route 配置：`imagen config set default_route auto`、`imagen config set enabled_routes api-key,codex-cli`、`imagen config set route_priority api-key,codex-cli`
- 永久保存 API route 凭据：`imagen setup --non-interactive --api-key <key> --base-url <url>` 或 `imagen config set api_key <key>` / `imagen config set base_url <url>`
- 单次临时 API route 凭据：`imagen generate ... --route api-key --api-key <key> --base-url <url>`
- 批量生成：`imagen batches run --file <batch.json> --dry-run-payload` 先检查 manifest；manifest 至少 3 个 item；真实执行默认 5 并发，允许 `--concurrency 1..7`；继续同一 manifest 用 `--resume`
- 检查：`imagen doctor --model gpt-image-2|nano-banana-2|mj`、`imagen runs show <run-id>`、`imagen jobs show <run-id>`
- 回复规范：执行后读 `references/reporting.md`，必要时再读 `references/reporting/common.md` 和 `references/reporting/templates.md`；这是 Skill 回复格式，不是 CLI 命令。
- 配置检查：`imagen config list` 查看默认模型、route、目录和脱敏凭据来源；`imagen doctor` / `imagen doctor --model <model>` 查看默认或目标模型/route 是否可用；`imagen config get default_model` 和 `imagen config get api_key` 用于定点检查，不显示 key 明文。

## api-key 凭证边界

- API key 解析顺序：单次 `--api-key` > 模型专属环境变量 > `IMAGE_GEN_PRO_API_KEY` > 本机 config `api_key`。
- Base URL 解析顺序：单次 `--base-url` > 模型专属环境变量 > `IMAGE_GEN_PRO_API_BASE_URL` > 本机 config `base_url` > `https://api.openai.com`。
- `--api-key` / `--base-url` 是单次临时覆盖，不会自动写入 config；用户选择永久保存时，用 `imagen setup --non-interactive --api-key ... --base-url ...` 或 `imagen config set ...`。
- 模型专属变量名和 provider 细节按需读 `references/routes.md` 与 `references/api/README.md`；不要读取或恢复通用 `OPENAI_API_KEY`。
- `api_key` / `base_url` 可以保存到本机 CLI config；`config list`、`config get api_key` 和 `doctor` 只显示脱敏 key。
- API key 不写入 Skill、文档、artifact、日志、provider response 或最终回复明文。

## 执行前路由快照

正式执行前填写此快照，确认路由、模式和确认状态：

```text
Task:
- Deliverable: prompt-only / plan / dry-run-artifact / payload-artifact / real-image / transparent-png / batch / inspect-config
- Input roles: prompt / source image / mask / style reference / composition reference / identity reference / batch manifest / prior run
- Task family: direct-generate / image-edit / reference-imitation / multi-reference-synthesis / transparent-output / batch-generate / iteration / route-config / runtime-inspect
- Execution mode: discuss / plan / dry-run / payload-dry-run / real-run / post-process / inspect
- References loaded: ...
- Method: none / reverse-prompting / composition / consistency / product / style / edit / typography / ...
- Model / route: ...
- Config preflight: config list / doctor status; configured / needs setup / temporary override / skipped
- Ambiguity resolved: ...
- Confirmation: model / route / method / size-ratio / final prompt / references shown and user confirmed
- CLI operation: imagen ...
- Verification: output path / job status / alpha / media manifest / run artifact
```
