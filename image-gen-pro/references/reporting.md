# Reporting Reference

Load after any `imagen` execution, batch run, dry-run, transparent post-process, run/job/config inspection, or failed execution. This file is the runtime entry and SSOT index for user-facing result replies.

## Goal

Every visible reply should be easy to scan, pleasant to read, and backed by artifacts. The user should not need to open raw JSON to answer the basic questions:

- Did it finish?
- Where is the output?
- Can I preview it?
- What model/route/method was used?
- What was the actual resolution and aspect ratio?
- What evidence was checked?
- What is the next concrete correction path if needed?

## Layered Index

| Need | Load |
| --- | --- |
| Shared tone, field labels, preview rendering, no-secret rules | `reporting/common.md` |
| Exact templates for generate/edit, batch, transparent, dry-run, inspection, failure | `reporting/templates.md` |
| How the Skill should render the final chat reply | `reporting/common.md` and `reporting/templates.md` |

Do not duplicate the long templates in `SKILL.md`. `SKILL.md` should only point here.

## Hard Rules

- Report only facts supported by `imagen` stdout JSON, run artifacts, batch artifacts, transparent metadata, or the current user request.
- Do not say an image was generated unless a real `imagen generate/edit` output file exists.
- Do not say a dry-run generated an image; say it wrote artifacts only.
- Do not expose API keys, Authorization headers, raw provider responses, long base64 payloads, or raw Codex session text.
- Every completion or failure report must include prompt information when a prompt exists.
- Prompt fields are standardized as `Original Prompt` and `Final Prompt`; method fields are standardized as `Method`.
- Real generated-image reports must include output path(s), preview, actual resolution, and aspect ratio from `outputs` / `preview`.
- If a preview image exists locally, include both the path and a Markdown image preview using an absolute path.
- If multiple images were produced and `preview.kind=contact_sheet`, report the contact-sheet preview; otherwise list per-image paths or say the multi-image preview was unavailable.
- For reference-image imitation, include both the user's original prompt/request and the final prompt submitted through `imagen`.
- Keep `Method` short: one line naming the route/method and why it was used.
- Prefer one compact result card over raw JSON dumps; raw JSON is for debugging only.

## Output Families

| Family | User-Facing Shape |
| --- | --- |
| Real generate/edit | Completion card with output, preview, actual resolution, aspect ratio, run, route, prompt, method, verification |
| 图生图 / image-to-image | Edit completion card with source image role, prepared media when available, output, preview, resolution, ratio, and verification |
| Multi-output run | Same as real generate/edit, but output and resolution lines may be comma-separated or grouped by index; preview should be the contact sheet when available |
| Batch | Batch summary card with counts, batch state path, batch preview, representative outputs, run artifact pointer |
| Transparent output | Completion card with final transparent PNG, preview, source image, alpha verification, metadata path |
| Dry-run / payload dry-run | Artifact-only card; output line must say no image was generated |
| Runs/jobs/config/doctor | Inspection card with key state, paths, active model/route, and no raw secrets |
| Failure | Failure card with failed layer, saved artifact path, prompt, method, and exactly one next corrective action |

## Skill Rendering Protocol

Skill must render the user-facing reply from these reporting templates after it reads `imagen` stdout JSON and the saved artifacts. Do not ask the user to inspect raw JSON, and do not invent a second reporting format in the chat.

Rendering order:

1. Read the relevant stdout JSON and artifact files.
2. Load `reporting/common.md` for tone, preview rendering, and required labels.
3. Load `reporting/templates.md` for the matching output family.
4. Fill only fields backed by artifacts or the current user request.
5. Include local previews with Markdown image syntax when a preview path exists.
