# Reporting Common Rules

Load through `../reporting.md` when writing or reviewing user-facing replies.

## Tone And Layout

- Use a compact result card. Avoid long paragraphs before the result.
- Put the most useful outcome first: completed/failed state, output, preview, resolution, ratio.
- Prefer Chinese field labels in normal replies.
- Use one blank line between the artifact block and prompt/method block.
- Do not paste raw JSON unless the user asks for debugging detail.
- Do not end with vague help text. If a next step is useful, make it a concrete action.

## Required Labels

Use these labels consistently:

```text
已完成 / 未完成
输出
预览
实际分辨率
尺寸比例
Run / Batch
Route
Original Prompt
Final Prompt
Method
验证
下一步
```

For setup, config, doctor, runs, and jobs inspection, use `状态` and `路径` instead of fake output fields.

## Preview Rendering

- If `preview.path` exists and is local, show the path and then render it with Markdown image syntax.
- Resolve relative paths to absolute paths before rendering local previews.
- Use this shape:

```markdown
预览：C:\absolute\path\preview.png
![预览](C:\absolute\path\preview.png)
```

- For paths containing spaces, wrap the Markdown image URL in angle brackets:

```markdown
![预览](<C:\path with spaces\preview.png>)
```

- For multiple images, prefer `preview.kind=contact_sheet`; if missing, list each output path and say `未生成拼图预览`.

## Prompt Reporting

- `Original Prompt` is the user's current request or a short summary of it.
- `Final Prompt` is the prompt submitted to `imagen`; prefer the `prompt.txt` path when it exists.
- If only a prompt draft was requested, label it `Final Prompt Draft`.
- For reference-image imitation, never omit the user's original request.

## Verification Reporting

Only report checks actually performed:

- Real generate/edit: `job=succeeded`, output exists, `result.json` exists.
- Image metadata: exact `resolution` and `aspect_ratio` from output records.
- Multi-output preview: `preview.kind=contact_sheet` and preview path exists.
- Dry-run/payload: artifact path and `provider_api_call=false`.
- Edit/image-to-image: media manifest and prepared media when available.
- Transparent output: real PNG alpha, alpha bbox, metadata path, preview path if created.
- Batch: status, counts, `state.json`, `summary.json`, and representative item run artifacts.
- Codex/API route: cleanup or redaction status only if checked.
