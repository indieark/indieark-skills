# MJ API Reference

> Load when: 用户指定 `--model mj`，或维护 MJ submit/poll adapter、MJ env、MJ prompt 参数边界。
> Avoid: NB/GPT Images API payload、普通 gallery 方法论、透明后处理。

## Runtime Model

- CLI model: `mj`.
- Default route: `api-key`.
- Current adapter target: generic MJ proxy contract learned from existing MJ usage: `/mj/submit/imagine` plus `/mj/task/<id>/fetch`.
- This is not the `/v1/images/*` Images API shape.

## Capability Matrix

| Capability | Current support |
| --- | --- |
| text-to-image | implemented by `generate --model mj` |
| image-conditioned imagine | implemented by `edit --model mj --image`, submitted through `base64Array` |
| mask / local redraw | not implemented |
| remote task id | recorded as `remote_task` when returned by submit |
| progress | adapter polls until success/failure/timeout |
| URL output | implemented; URLs are downloaded to local output files |
| advanced MJ actions | not implemented in CLI flags |

## Credential Sources

Priority:

```text
--api-key / --base-url
> IMAGE_GEN_PRO_MJ_API_KEY / IMAGE_GEN_PRO_MJ_API_BASE_URL
> IMAGE_GEN_PRO_API_KEY / IMAGE_GEN_PRO_API_BASE_URL
> config api_key / config base_url
> https://api.openai.com
```

The adapter sends the resolved key through:

```text
mj-api-secret: <redacted>
```

Do not read `OPENAI_API_KEY`.

## Imagine Submit

Endpoint:

```text
POST /mj/submit/imagine
Content-Type: application/json
mj-api-secret: <redacted>
```

Body:

```json
{
  "prompt": "...",
  "base64Array": [],
  "notifyHook": "",
  "state": "",
  "botType": "MID_JOURNEY"
}
```

For `imagen edit --model mj --image ...`, local image inputs are converted to data URLs and placed in `base64Array`.

## CLI Parameter Mapping

MJ is prompt-parameter driven. The CLI only maps a small shared surface:

| CLI option | Mapping |
| --- | --- |
| `--prompt` | MJ `prompt`; native params such as `--v`, `--q`, `--sref`, `--cref`, `--style`, `--stylize`, `--chaos`, and `--seed` stay inside this text |
| `--image` | converted to data URLs in `base64Array` |
| `--size auto` | no aspect ratio injection |
| `--size WIDTHxHEIGHT` / shortcut | appends `--ar W:H` unless prompt already contains `--ar` or `--aspect` |
| `--quality` | must stay `auto`; native quality belongs in prompt as V8 `--sd` / `--hd` or older `--q ...` |
| `--output-format` | local output extension only |
| `--timeout-sec` | submit + poll deadline |
| `--mask` | rejected |
| `--background` / `--moderation` / `--output-compression` | rejected |
| `-n` / `--n` | currently must be `1` |

## Size / Parameter Limits

`--size` uses the shared CLI size validator before MJ-specific prompt mapping.

| Parameter | Rule |
| --- | --- |
| Size shortcuts | `auto`, `square`, `portrait`, `landscape`, `2k`, `wide`, `4k`, `tall`. |
| Literal `WIDTHxHEIGHT` | each edge <= `3840`; each edge is a multiple of `16`; aspect ratio <= `3:1`; total pixels `655360..8294400`. |
| MJ size mapping | mj appends --ar W:H unless prompt already contains `--ar` or `--aspect`; `auto` injects nothing. |
| Prompt `--ar` / `--aspect` | Existing prompt ratio wins; CLI does not override it. |
| `--quality` | Must stay `auto`; native quality belongs in prompt as V8 `--sd` / `--hd` or older `--q ...`. |
| `-n` / `--n` | Must be `1`. |
| `--mask` | Rejected. |
| `--background` / `--moderation` / `--output-compression` | Rejected; these are currently GPT-only shared options. |
| `--output-format` | Local output extension only. |

## Polling

After submit, read the task id from `result`, `taskId`, or `id`, then poll:

```text
GET /mj/task/<task-id>/fetch
mj-api-secret: <redacted>
```

Terminal conditions:

- `status=SUCCESS` or `progress=100%`: parse output.
- `status=FAILURE`: fail the run with a redacted error.
- timeout: fail the run and preserve local artifact state.

Output extraction accepts:

- `data[].b64_json`
- `imageUrl`
- `imageUrls[].url`

URL outputs are downloaded into local output files.

## Boundary

MJ usage is prompt-parameter driven. Version, aspect ratio, quality, style reference, character reference, variation, upscale, modal, blend, describe, swap, video, and partial redraw are not interchangeable with Images API fields.

If a compatible MJ API is mounted under an extra prefix, put that prefix in the shared or model-specific base URL. For example, base URL `http://host:port/mjapi` submits to `/mjapi/mj/submit/imagine` and polls `/mjapi/mj/task/<taskId>/fetch`. The adapter does not retry hardcoded fallback prefixes after 404/405.

Some MJ UIs default new prompts to `--v 8.1`, and V8 quality control may use `--sd` or `--hd`, not `--q`. This CLI does not inject those UI defaults automatically. Put them in `--prompt`, for example:

```powershell
imagen generate --model mj --prompt "product hero render --v 8.1 --hd --ar 16:9" --route api-key
```

This first adapter only implements the drawing entry: `submit/imagine` plus task polling. Advanced MJ actions require their own CLI flags and reference updates before implementation.

Do not add MJ prompt parameters as generic CLI flags until their provider semantics, validation, and artifact representation are designed. For now, pass native MJ parameters inside `--prompt`.

Reference sources for the learned calling shape, not runtime dependencies:

- `C:\Vibe_Coding\IndieArk\20005-aigc\mj_webui\src\api\mjapi.ts`
- `C:\Vibe_Coding\IndieArk\20005-aigc\mj_webui\service\src\index.ts`
- `C:\Vibe_Coding\IndieArk\20005-aigc\docs\architecture\model-parameters.md`
- `https://docs.midjourney.com/hc/en-us/articles/32023408776205-Prompt-Basics`
- `https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List`
