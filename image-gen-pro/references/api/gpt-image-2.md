# GPT Image 2 API Reference

> Load when: 需要实现或维护 `gpt-image-2` provider adapter、payload builder、local validation、response saving 或 CLI 参数映射。
> Avoid: 只做通用 prompt 规划、gallery 选择、placeholder dry-run 或非 provider-specific 文档维护。
> Pairs with: `../api.md` 定义运行时 API 边界；`../provider-adapter.md` 定义 adapter 契约；`../../../docs/research/gpt-image-2-extraction-spec.md` 定义来源仓库迁移规则。

更新时间：2026-05-19（Asia/Shanghai）

## Official Sources Checked

- `https://developers.openai.com/api/docs/guides/image-generation`
- `https://developers.openai.com/api/docs/models/gpt-image-2`
- `https://platform.openai.com/docs/api-reference/images`

本文件记录当前官方文档口径和本仓库的实现决策。后续如果官方文档变化，先更新本文件，再改 provider adapter。

## Local Implementation Target

第一版真实 CLI 使用 Image API，而不是 Responses API：

| Local command | Image API call | Endpoint |
| --- | --- | --- |
| `generate` | `client.images.generate(...)` | `POST /v1/images/generations` |
| `edit` | `client.images.edit(...)` | `POST /v1/images/edits` |

The adapter always uses the configured base URL plus the normal `/v1/images/*` path. Direct OpenAI-compatible roots and `/v1` base URLs are supported; if a proxy mounts GPT Image behind another prefix, put that prefix directly in the base URL. The adapter does not probe project-specific fallback paths.

理由：

- 单 prompt 文生图和单轮编辑优先用 Image API。
- Responses API 更适合多轮可编辑图像体验，后续单独立项。
- `plan` / `dry-run` 继续保持 provider-neutral，不调用本 provider adapter。

## Model Defaults

| Field | Value |
| --- | --- |
| model | `gpt-image-2` |
| output source | `data[].b64_json` |
| default output format | `png` |
| default size | `auto` |
| default quality | `auto` |
| supported qualities | `auto`, `low`, `medium`, `high` |
| supported formats | `png`, `jpeg`, `webp` |
| compression | 0-100, only for `jpeg` and `webp` |
| moderation | `auto`, `low` |
| transparent background | not supported for `gpt-image-2` |

## Capability Matrix

| Capability | Current support |
| --- | --- |
| text-to-image | implemented by `generate` |
| image-to-image / edit | implemented by `edit --image` |
| multiple input images | implemented as repeated edit images |
| mask | edit-only; same format and dimensions as first image, each submitted file less than 50MB, alpha required |
| remote task id | not available for sync Images API |
| URL output | not implemented for this model |
| transparent output | use `imagen transparent` post-processing, not provider background transparency |

## CLI Parameter Mapping

| CLI option | Mapping |
| --- | --- |
| `--size` | API `size`; accepts `auto`, a size tier with `--aspect`, or validated `WIDTHxHEIGHT`; gpt-image-2 sends normalized size |
| `--aspect` | Used with `--size 1080p|2k|4k` to derive a concrete GPT Image canvas |
| `--quality` | API `quality=auto|low|medium|high` |
| `--output-format` | API `output_format=png|jpeg|webp` |
| `--output-compression` | API `output_compression`, only for JPEG/WebP |
| `--background` | API `background`, except local reject for `transparent` |
| `--moderation` | API `moderation=auto|low` |
| `-n` / `--n` | API `n` |
| `--user` | API `user` |

## Parameter Limits

| Parameter | Rule |
| --- | --- |
| `--size` / `--aspect` | Shared CLI size validator runs before payload construction; see Size Rules below. |
| `--quality` | Must be `auto`, `low`, `medium`, or `high`. |
| `--output-format` | Must be `png`, `jpeg`, or `webp`. |
| `--output-compression` | Only valid with `jpeg` or `webp`; value must be `0..100`. |
| `--background transparent` | Rejected locally; use `imagen transparent` for transparent PNG delivery. |
| `--moderation` | Must be `auto` or `low`. |
| `-n` / `--n` | Must be at least `1`. |
| `--mask` | Edit-only; official mask rule is enforced locally: same format and dimensions as the first image, each submitted file less than 50MB, alpha channel required. |

## Generate Payload

Required:

- `model`
- `prompt`

Optional local parameters to map:

- `n`
- `size`
- `quality`
- `background`
- `moderation`
- `output_format`
- `output_compression`
- `user`
- `stream`
- `partial_images`

Local rules:

- Reject missing or empty prompt before adapter call.
- Reject `--image` and `--mask` on `generate`.
- Reject `background=transparent` for `gpt-image-2`.
- Include `output_compression` only when `output_format` is `jpeg` or `webp`.
- Do not expose `response_format`; GPT Image output is base64 image data.
- Stream and partial image support is deferred unless explicitly implemented with artifact handling.

## Edit Payload

Required:

- `model`
- `prompt`
- at least one `image`

Optional:

- `mask`
- `n`
- `size`
- `quality`
- `background`
- `output_format`
- `output_compression`
- `user`

Local rules:

- Route any call with one or more `--image` inputs to edit.
- Preserve repeatable `--image`; pass multiple input images as a list.
- `mask` is edit-only.
- When multiple images and a mask are provided, treat the mask as applying to the first image.
- Validate local image paths exist before adapter call.
- Validate mask path exists before adapter call.
- Official mask rule is enforced locally: the submitted mask must match the first image format and dimensions, each submitted file must be less than 50MB, and the mask must include an alpha channel.
- Masking with GPT Image is prompt-based guidance; the model may not follow the exact mask shape with complete precision.
- Omit `input_fidelity` for `gpt-image-2`; official docs say this model always processes image inputs at high fidelity.

## Size Rules

Use the shared CLI size validator as the capability source for `gpt-image-2` output sizes.

Supported forms:

| Form | Rule |
| --- | --- |
| `--size auto` | Sends API `size=auto`. |
| `--size 1080p --aspect WIDTH:HEIGHT` | Derives a canvas from a 1920x1080 target pixel budget and the requested aspect. |
| `--size 2k --aspect WIDTH:HEIGHT` | Derives a canvas from a 2560x1440 target pixel budget and the requested aspect. |
| `--size 4k --aspect WIDTH:HEIGHT` | Derives a canvas from a 3840x2160 target pixel budget and the requested aspect. |
| `--size WIDTHxHEIGHT` | Sends the validated literal canvas. |

All concrete canvas values must pass these constraints:

- each edge <= `3840`
- each edge is a multiple of `16`
- long edge / short edge <= `3`
- total pixels >= `655360`
- total pixels <= `8294400`

Tier-derived canvases are recorded in the request payload and run artifacts.

## Response Handling

Expected final response:

```json
{
  "created": 1713833628,
  "data": [
    {
      "b64_json": "<base64 image data>"
    }
  ]
}
```

Current Image API behavior:

- `/v1/images/generations` and `/v1/images/edits` return the image response directly.
- The response does not include a persistent remote task id for later `status` or `wait`.
- Streaming / partial image events are a separate execution mode and do not create a video-style task id.
- If true progress events are needed later, implement an explicit streaming Image API route or a Responses API route; do not fake progress in the synchronous `api-key` route.

Local output writer must:

- decode `data[].b64_json`
- write one output file per item
- use stable suffixes for `n > 1`
- write `result.json` without raw base64
- write `media-manifest.json` with output path, bytes, sha256, format and index
- preserve provider request id or response id when available

Do not implement URL downloading for `gpt-image-2` until official docs expose URL output for this model. The source repository had URL handling as a generic fallback, but current official Image API docs show base64 output for GPT Image.

## Error Mapping

Adapter errors should map into stable local categories:

| Local category | Examples |
| --- | --- |
| `missing_api_key` | no usable API key source |
| `invalid_request` | unsupported size, transparent background, missing image |
| `provider_auth` | rejected key or organization verification issue |
| `provider_policy` | moderation/content policy rejection |
| `provider_rate_limit` | rate limit or quota exhaustion |
| `provider_timeout` | image generation exceeded local timeout |
| `provider_unavailable` | transient upstream service failure |
| `unknown_provider_error` | anything else after redaction |

Errors must not include full API keys, raw Authorization headers, raw base64 image data, or private local file contents.

## Source Repository Differences

Keep these differences explicit while migrating from `gpt_image_2_skill`:

- Keep generate/edit routing and repeatable image behavior.
- Keep output naming and artifact ideas.
- Keep `gpt-image-2` default.
- Adapt `response_format` / URL fallback: for this model, write base64-only until official docs say otherwise.
- Adapt dotenv fallback into Settings + process env precedence.
- Keep `input_fidelity` as a compatibility warning only; do not send it.
- Reject transparent background locally for this model.

## Not In First Adapter

- Responses API multi-turn editing.
- File ID based image inputs.
- streaming final/partial images.
- remote progress polling for synchronous Image API calls.
- fake task ids for providers that do not return one.
- automatic mask alpha-channel repair.
- pricing calculator.
- remote URL image inputs for Image API.
