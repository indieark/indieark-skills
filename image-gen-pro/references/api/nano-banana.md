# Nano Banana API Reference

> Load when: 用户指定 `--model nano-banana` / `nano-banana-2`，或维护 NB adapter、NB env、NB 图生图字段。
> Avoid: 普通 prompt 方法论、MJ 参数、GPT-only Images API 参数。

## Runtime Model

- CLI alias: `nano-banana`, `nano-banana-2`, `nb`.
- Normalized model: `nano-banana-2`.
- Default route: `api-key`.
- Current adapter target: NB / ePhone-style OpenAI-compatible proxy shape.

## Capability Matrix

| Capability | Current support |
| --- | --- |
| text-to-image | implemented by `generate` |
| image-to-image / edit | implemented by `edit --image` |
| multiple input images | implemented as repeated multipart `image` fields |
| mask | not implemented |
| remote task id | supported when an async proxy returns `taskId` |
| URL output | accepted as fallback if proxy returns URLs |
| native Gemini fields | not sent by this adapter |

## Credential Sources

Priority:

```text
--api-key / --base-url
> IMAGE_GEN_PRO_NANO_BANANA_API_KEY / IMAGE_GEN_PRO_NANO_BANANA_API_BASE_URL
> IMAGE_GEN_PRO_API_KEY / IMAGE_GEN_PRO_API_BASE_URL
> config api_key / config base_url
> https://api.openai.com
```

Do not read `OPENAI_API_KEY`.

## Generate Payload

Endpoint:

```text
POST /v1/images/generations
Authorization: Bearer <redacted>
Content-Type: application/json
```

Body:

```json
{
  "model": "nano-banana-2",
  "prompt": "...",
  "aspect_ratio": "1:1",
  "quality": "1K",
  "response_format": "b64_json"
}
```

If a compatible NB API is mounted under an extra prefix, put that prefix in the shared or model-specific base URL, for example `/nbapi` or `/nbapi/v1`. The adapter posts to `/v1/images/*` under the configured prefix and does not retry hardcoded fallback prefixes after 404/405. A successful response may be synchronous `data[]` or async:

```json
{
  "taskId": "...",
  "status": "PENDING"
}
```

In that case the adapter polls `GET <configured-base-without-/v1>/task/<taskId>` until `SUCCESS` / `ERROR` / timeout. On success it unwraps the `data` object and records `remote_task` in local artifacts. Direct ePhone / OpenAI-compatible endpoints that return `data[]` synchronously still work without polling.

CLI mapping:

- `--size auto` omits `aspect_ratio`.
- `--size WIDTHxHEIGHT` or shortcut maps to reduced `aspect_ratio`.
- `--quality low|medium|high` maps to `0.5K|1K|2K`.
- `--quality 0.5K|1K|2K|4K` is accepted for NB.

## Size / Parameter Limits

`--size` uses the shared CLI size validator before NB-specific mapping.

| Parameter | Rule |
| --- | --- |
| Size shortcuts | `auto`, `square`, `portrait`, `landscape`, `2k`, `wide`, `4k`, `tall`. |
| Literal `WIDTHxHEIGHT` | each edge <= `3840`; each edge is a multiple of `16`; aspect ratio <= `3:1`; total pixels `655360..8294400`. |
| NB size mapping | nano-banana-2 sends reduced aspect_ratio; `auto` omits `aspect_ratio`. |
| `--quality` | `auto` omitted; `low/medium/high` -> `0.5K/1K/2K`; accepts `0.5K`, `1K`, `2K`, `4K`. |
| `-n` / `--n` | Must be `1`. |
| `--mask` | Rejected. |
| `--background` / `--moderation` / `--output-compression` | Rejected; these are currently GPT-only shared options. |
| `--output-format` | Local output extension only; request still uses `response_format=b64_json`. |

## CLI Parameter Mapping

| CLI option | Mapping |
| --- | --- |
| `--prompt` | `prompt` |
| `--image` | repeated multipart `image` fields on edit |
| `--size` | reduced `aspect_ratio`; omitted when `auto` |
| `--quality` | `0.5K`, `1K`, `2K`, `4K`; `auto` omits field |
| `--output-format` | local output extension; request uses `response_format=b64_json` |
| `--user` | forwarded as `user` when present |
| `--mask` | rejected |
| `--background` / `--moderation` / `--output-compression` | rejected |
| `-n` / `--n` | currently must be `1` |

## Edit Payload

Endpoint:

```text
POST /v1/images/edits
Authorization: Bearer <redacted>
Content-Type: multipart/form-data
```

Multipart fields:

- `model=nano-banana-2`
- `prompt=...`
- repeated `image` file fields
- optional `aspect_ratio`
- optional `quality`
- `response_format=b64_json`

The field name is `image`, not `image[]`. This follows the reference-derived NB compatible proxy shape.

The same async task response is supported for edits. Polling is local evidence only; `jobs delete` still deletes local artifacts and does not cancel the upstream NB task.

## Boundary

Official Google docs describe native Gemini image generation fields such as response modalities and image config. This adapter does not send those native fields. Keep raw Gemini support as a future separate adapter so the current NB proxy path stays compatible with OpenAI-style NB proxies.

Deferred native fields include response modalities, image config, thinking config, and raw Gemini file/media handling. Add a separate adapter before documenting those as supported runtime parameters.

Reference sources for the learned calling shape, not runtime dependencies:

- `C:\Vibe_Coding\IndieArk\20005-aigc\docs\architecture\model-parameters.md`
- `C:\Vibe_Coding\IndieArk\20005-aigc\mj_webui\service\src\nbCache.ts`
- `https://ai.google.dev/gemini-api/docs/image-generation`
- `https://ai.google.dev/gemini-api/docs/nanobanana`
