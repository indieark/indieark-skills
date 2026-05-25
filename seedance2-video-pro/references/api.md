# Seedance 2.0 API Reference Notes

> Load when: 需要确认 Seedance 2.0 模型、endpoint、payload content role、互斥规则或 API 限制。
> Avoid: 只需要写导演 prompt 或问询用户，不涉及 payload / 参数 / API 行为。
> Pairs with: `cli.md` 写命令；`router.md` 决定 API operation；`director.md` 确保 prompt 和素材角色一致。

This file is the Skill-local API reference. It summarizes the current working assumptions and points agents back to official documentation before changing the API layer.

## Official Sources

| Topic | URL |
|-------|-----|
| Seedance 2.0 API reference | https://www.volcengine.com/docs/82379/1393047?lang=zh |
| Create video generation task | https://www.volcengine.com/docs/82379/1520757?lang=zh |
| Query video generation task | https://www.volcengine.com/docs/82379/1521309?lang=zh |
| List video generation tasks | https://www.volcengine.com/docs/82379/1521675?lang=zh |
| Cancel or delete task | https://www.volcengine.com/docs/82379/1521720?lang=zh |
| Base URL and authentication | https://www.volcengine.com/docs/82379/1541594?lang=zh |
| Badcase reporting | https://www.volcengine.com/docs/82379/2389900?lang=zh |

## Models

Only Seedance 2.0 models are in scope:

- `doubao-seedance-2-0-260128`
- `doubao-seedance-2-0-fast-260128`

Do not silently fall back to 1.0 or 1.5 models.

## Endpoints

```text
POST   https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks
GET    https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{task_id}
GET    https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks
DELETE https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{task_id}
```

Authentication:

```text
Authorization: Bearer $ARK_API_KEY
```

## Content Roles

Use explicit roles so prompt references are unambiguous:

```json
{"type":"image_url","image_url":{"url":"..."},"role":"first_frame"}
{"type":"image_url","image_url":{"url":"..."},"role":"last_frame"}
{"type":"image_url","image_url":{"url":"..."},"role":"reference_image"}
{"type":"video_url","video_url":{"url":"..."},"role":"reference_video"}
{"type":"audio_url","audio_url":{"url":"..."},"role":"reference_audio"}
```

For reference-driven prompts, label assets by the per-role order in `content`.
Official-style prompt labels such as `图片1`, `图片2`, `视频1`, and `音频1`
map to the first/second `reference_image`, first `reference_video`, and first
`reference_audio`. The CLI records this mapping in `media-manifest.json` as
`reference_index` and warns in `prompt_reference_warnings` when a prompt omits a
reference label.

## Mode Selection

| Mode | Required Inputs | Notes |
|------|-----------------|-------|
| Text-to-video | prompt only | Can use web search if official API supports it |
| First frame | one image as `first_frame`; prompt optional | Good for animating a starting image |
| First + last frame | `first_frame` + `last_frame`; prompt optional | Good for controlled transition |
| Omnireference | `reference_image` / `reference_video` / `reference_audio`; prompt optional | Best for character, motion, rhythm, and style references |
| Video editing intent | reference video and optional reference image; prompt optional | Same content-generation payload shape as omnireference; use prompt to describe intent |
| Video extension | one or more reference videos; prompt optional | Use prompt to continue the narrative |

## Guardrails

- First-frame / last-frame mode cannot be mixed with omnireference mode.
- Reference audio cannot be the only non-text input.
- When a prompt is supplied, it must describe how each reference should be used.
- `edit` is not a stronger mask/inpaint/subject-replacement API unless official fields are added and tested; treat it as an edit-intent wrapper over reference content.
- Local `reference_video` paths are rejected by default; use `--serve-local-assets cloudflare`, an HTTPS URL, or a signed object URL.
- HTTP(S) media URLs should be probed before task submission and recorded in run artifacts.
- Local media is validated before payload creation. Images fail early for known
  extension, size, dimension, or aspect-ratio violations when Pillow cannot
  auto-fix them first. Video/audio use
  `ffprobe` metadata when available to validate duration, total duration, video
  FPS, codec, dimensions, aspect ratio, and pixel count; known violations are
  auto-prepared with ffmpeg when available, and unavailable metadata is recorded
  as manifest warnings instead of guessed.
- Keep generated video goals short enough for a 4-15 second clip.
- `doubao-seedance-2-0-260128` supports `480p`, `720p`, and `1080p`; `doubao-seedance-2-0-fast-260128` does not support `1080p`.
- Built-in default `ratio` for Seedance 2.0 is `adaptive`; callers can still pass `16:9`, `4:3`, `1:1`, `3:4`, `9:16`, or `21:9`.
- `duration` for Seedance 2.0 is `4-15` integer seconds or `-1` for model-selected duration.
- `seed` is limited to `-1..4294967295`.
- `callback_url` must be HTTP(S), `execution_expires_after` must be `3600-259200` seconds, and `safety_identifier` must be at most 64 chars.
- `service_tier=flex` is rejected because this skill only covers Seedance 2.0 and Seedance 2.0 does not support offline/flex inference.
- Do not expose 1.0/1.5-only fields (`draft`, `draft_task`, `frames`, `camera_fixed`) on the Seedance 2.0 CLI path.
- Reference inputs are limited to 9 images, 3 videos, and 3 audios.
- List-task `page_num` and `page_size` are both limited to `1-500`.
- The list-task `filter.status` values are `queued`, `running`, `cancelled`, `succeeded`, and `failed`; `expired` is a returned task status but not an official list filter value.
- Re-check official docs before changing file size, duration, resolution, or parameter limits.
