# Model Capability Matrix

> Load when: 需要比较 `gpt-image-2`、NB 和 MJ 的当前 CLI 能力、参数映射或未实现边界。
> Avoid: 需要具体 provider payload 时，改读同目录下对应模型文件。

本文件是跨模型能力索引。它记录当前 `imagen` adapter 已实现的能力、尺寸限制和高层参数映射；完整 payload、响应和错误边界仍以每个模型文件为准。

## Current Adapter Matrix

| Capability | `gpt-image-2` | `nano-banana-2` | `mj` |
| --- | --- | --- | --- |
| Default model | Yes | No | No |
| CLI aliases | `gpt-image-2` | `nano-banana`, `nano-banana-2`, `nb` | `mj` |
| Preferred real route | `codex-cli` or `api-key` | `api-key` | `api-key` |
| Generate | `/v1/images/generations` under configured base URL | `/v1/images/generations` under configured base URL or prefix | `/mj/submit/imagine` under configured base URL or prefix |
| Edit / image input | `/v1/images/edits`, multipart `image[]` | `/v1/images/edits`, repeated multipart `image` | submit imagine with `base64Array` |
| Mask | Supported by local CLI contract | Not implemented | Not implemented |
| Remote task id | None for sync Images API | Optional `remote_task` when an async proxy returns `taskId/PENDING` | `remote_task` from submit result |
| Output extraction | `data[].b64_json` | `data[].b64_json` or URL fallback | `data[].b64_json`, `imageUrl`, `imageUrls[].url` |
| Prompt-native params | Not required | Not required for current proxy | Required for native MJ options |

## Size And Parameter Limits

Load this section before choosing a model or explaining why a parameter is rejected. Then load the per-model file for payload details.

Use the shared CLI size validator as the capability source for model size limits.

| Limit | `gpt-image-2` | `nano-banana-2` | `mj` |
| --- | --- | --- | --- |
| Real route | `codex-cli` or `api-key` | `api-key` | `api-key` |
| Size limits | `auto`, size tier `1080p|2k|4k` plus `--aspect`, or literal `WIDTHxHEIGHT`; concrete canvases use each edge <= `3840`, multiple of `16`, aspect ratio <= `3:1`, total pixels `655360..8294400` | Uses `--aspect` or literal `WIDTHxHEIGHT` for ratio mapping | Uses `--aspect` or literal `WIDTHxHEIGHT` for prompt ratio mapping |
| Size mapping | gpt-image-2 sends normalized size as API `size` | nano-banana-2 sends reduced aspect_ratio; `auto` omits it | mj appends --ar W:H unless prompt already contains `--ar` or `--aspect`; `auto` injects nothing |
| Quality | `auto`, `low`, `medium`, `high` | `auto` omitted; `low/medium/high` -> `0.5K/1K/2K`; accepts `0.5K/1K/2K/4K` | CLI `--quality` must be `auto`; native `--sd`, `--hd`, `--q` stay in prompt |
| Count | `-n/--n >= 1` | `-n/--n` must be `1` | `-n/--n` must be `1` |
| Mask | Edit-only; same format and dimensions as first image; each submitted file less than 50MB; alpha required; prompt-based guidance | Rejected | Rejected |
| Background | Allowed except `transparent`; transparent PNG uses `imagen transparent` | Rejected | Rejected |
| Moderation | `auto` / `low` | Rejected | Rejected |
| Output compression | JPEG/WebP only, `0..100` | Rejected | Rejected |
| Remote task | None for sync Images API | Optional async `taskId/PENDING` polling | Submit returns task id and adapter polls |

Routing rules:

- For model limit lookup, load `model-capabilities.md` first.
- For concrete payload fields, response handling, redaction, or provider-specific errors, load `gpt-image-2.md`, `nano-banana.md`, or `mj.md`.
- When a model-specific limit changes, update this table, the provider file, adapter validation, and validator phrases in one change.

## CLI Parameter Mapping

| CLI option | `gpt-image-2` | `nano-banana-2` | `mj` |
| --- | --- | --- | --- |
| `--prompt` | `prompt` | `prompt` | `prompt`; may include native MJ params |
| `--image` | edit image input | edit image input | converted to data URL in `base64Array` |
| `--mask` | edit-only mask; same format and dimensions as first image; alpha required | rejected | rejected |
| `--size auto` | API `size=auto` | omit `aspect_ratio` unless `--aspect` is set | no `--ar` injection unless `--aspect` is set |
| `--size 1080p\|2k\|4k --aspect WIDTH:HEIGHT` | normalized concrete `size` | `--aspect WIDTH:HEIGHT` controls ratio; `--quality` controls NB output quality | `--aspect WIDTH:HEIGHT` controls ratio; native MJ params stay in prompt |
| `--size WIDTHxHEIGHT` | normalized `size` | reduced `aspect_ratio` | appends `--ar W:H` unless prompt already has `--ar` / `--aspect` |
| `--aspect WIDTH:HEIGHT` | derives size only with `--size 1080p\|2k\|4k` | reduced `aspect_ratio` | appends `--ar W:H` unless prompt already has `--ar` / `--aspect` |
| `--quality` | `auto`, `low`, `medium`, `high` | `low/medium/high` -> `0.5K/1K/2K`; also accepts `0.5K/1K/2K/4K` | only `auto`; native V8 `--sd` / `--hd` or older `--q` belongs in prompt |
| `--output-format` | provider output format | local output extension; request stays `response_format=b64_json` | local output extension for downloaded/decoded result |
| `--output-compression` | JPEG/WebP only | rejected | rejected |
| `--background` | allowed except `transparent` | rejected | rejected |
| `--moderation` | `auto` / `low` | rejected | rejected |
| `-n` / `--n` | supported by Images API | currently `1` only | currently `1` only |

## Model-Specific Env

Config `default_model` controls the model used when `--model` is omitted. Initial value is `gpt-image-2`; users can set it with `imagen setup --non-interactive --default-model ...` or `imagen config set default_model ...`.

Shared fallback remains `IMAGE_GEN_PRO_API_KEY` / `IMAGE_GEN_PRO_API_BASE_URL`. Model-specific env wins first:

| Model | API key env | Base URL env |
| --- | --- | --- |
| `gpt-image-2` | `IMAGE_GEN_PRO_GPT_IMAGE_2_API_KEY` | `IMAGE_GEN_PRO_GPT_IMAGE_2_API_BASE_URL` |
| `nano-banana-2` | `IMAGE_GEN_PRO_NANO_BANANA_API_KEY` | `IMAGE_GEN_PRO_NANO_BANANA_API_BASE_URL` |
| `mj` | `IMAGE_GEN_PRO_MJ_API_KEY` | `IMAGE_GEN_PRO_MJ_API_BASE_URL` |

`OPENAI_API_KEY` is not a credential source for this Skill.

Base URL prefixes are explicit. The adapter does not probe project-specific fallback paths; configure the shared or model-specific base URL to the provider root or mounted prefix you want to use.

## Deferred Capabilities

- Raw Gemini / native NB fields such as response modalities, thinking config, and native image config.
- NB remote task cancellation; `remote_task` is recorded only for async proxy recovery evidence.
- MJ upscale, variation, blend, describe, swap, video, partial redraw, and modal actions.
- MJ native parameter parsing as separate CLI flags; keep them inside `--prompt` until explicitly designed. UI defaults such as `--v 8.1 --sd` / `--hd` are prompt text, not generic CLI defaults.
- Remote cancellation for provider tasks; local `jobs delete` only removes local artifacts.
