# Transparent Output

Load when the user asks for transparent PNG, 抠图/扣图, cutout asset, removed background, no background, alpha channel, sprite-ready output, icon/character/product with clean compositing edges, or a transparent deliverable.

## Non-Negotiable Protocol

Transparency is a deterministic workflow, not a prompt promise.

Required route:

```text
1. Generate a cutout-ready source image: the complete subject on one flat solid chroma background chosen to be easy to remove.
2. Run imagen transparent on that generated chroma image.
3. Verify the result is a PNG with real alpha.
4. Tell the user it was generated plus post-processed.
```

If the user is asking AI to create a new cutout/transparent asset, do not first generate a normal complex-background image. The first generated deliverable must already be designed for extraction: single solid background, no floor plane, no contact shadow, no reflection, no texture, and high contrast against the subject.

Failures:

- Checkerboard pattern inside the generated image is fake transparency.
- White, black, gray, blurred, gradient, textured, or "transparent-looking" pixels are not alpha.
- A PNG without an alpha channel is not a transparent deliverable.
- A model instruction like "make the background transparent" is not sufficient unless followed by `imagen transparent` or proven alpha verification.

## Required Command Shape

First generate the cutout-ready chroma-background source through CLI:

```powershell
imagen generate `
  --prompt "Create [subject] as a cutout-ready asset. Use a single flat solid chroma background color: #ff00ff that does not appear on the subject and is easy to remove. No gradient, no texture, no floor, no shadow, no reflection, no checkerboard. Keep the entire subject fully visible." `
  --route auto `
  --output-file .\outputs\<name>-chroma.png `
  --run-id <name>-chroma
```

Then post-process the generated image:

```powershell
imagen transparent `
  --input .\outputs\<name>-chroma.png `
  --output .\outputs\<name>-transparent.png `
  --background auto `
  --metadata-file .\outputs\<name>-transparent.metadata.json `
  --preview-file .\outputs\<name>-transparent.preview.png
```

The transparent command preserves canvas size, outputs PNG with alpha, and writes metadata declaring `transparency_source=generated_chroma_background_plus_postprocess`.

## Edge Cleanup Defaults

`imagen transparent` uses deterministic post-processing after alpha creation:

- Remove visible opaque pixels that are still close to the detected solid background color. This prevents colored halo pixels from expanding the alpha bbox.
- Run RGB-only 去污染 on remaining edge pixels: semi-transparent pixels use known-background unmixing, and local magenta/green/background-like spill is neutralized without changing alpha.
- Preserve canvas size. RGB cleanup must not change alpha, bbox, or anchor.
- 连通域小岛清理 is opt-in through `--min-island-area <pixels>` because small effects, hair strands, sparks, or icon details may be legitimate foreground.
- 不默认改 alpha feather. Alpha feather / trimap matting can soften jagged edges, but it can expand or shrink the bbox; only add that as an explicit future option with separate verification.

Useful transparent tuning parameters:

```powershell
imagen transparent `
  --input .\outputs\<name>-chroma.png `
  --output .\outputs\<name>-transparent.png `
  --background auto `
  --tolerance 36 `
  --soft-range 18 `
  --min-island-area 64 `
  --edge-decontaminate-strength 0.78
```

## Generation Prompt Rules

Use a chroma background that is unlikely to appear in the subject and easy for deterministic removal. Prefer magenta, green, cyan, blue, or yellow; avoid white/black unless the subject makes all chroma colors unsafe.

Required prompt constraints:

```text
Use one single flat solid chroma background color: #[hex].
The image is intended for background removal / cutout extraction.
The background must be uniform.
No gradient, no texture, no shadow, no floor, no reflection, no lighting spill, no checkerboard.
Keep the entire subject fully visible inside the image.
Do not crop hair, hands, feet, tail, weapon, clothing, effects, or accessories.
No text, no watermark, no extra objects.
```

When a user provides an existing complex-background image and only asks to remove its background, you may run `imagen transparent` only if the background is already flat enough. Otherwise, explain that reliable transparent output requires regenerating or editing a cutout-ready pure-color-background source first.

For batch/sprite work, use the same background color for every frame/panel and keep each subject inside its own frame boundary.

## Verification

Minimum verification before delivery:

- Output path ends with `.png`.
- The image has an alpha channel.
- Background/corners have alpha 0.
- Subject area has visible alpha and no accidental transparent holes.
- No obvious remaining chroma-colored halo at the edge.
- Metadata includes `transparent_output=true`.
- Metadata alpha bbox is not null for a visible subject.
- Metadata records background-like cleanup, optional island cleanup, and RGB-only edge decontamination counts.
- Checkerboard preview is only a preview file, never the final transparent image.

If Pillow is available, verify alpha directly:

```powershell
python -c "from PIL import Image; im=Image.open(r'.\outputs\<name>-transparent.png'); print(im.mode, im.getchannel('A').getbbox())"
```

Expected: mode includes alpha (`RGBA` or `LA`) and bbox is not `None`.

## User Disclosure

Use `reporting.md` for the full final reply. The disclosure sentence must say:

```text
已生成并后处理为透明 PNG：先生成可控纯色背景版本，再通过 imagen transparent 得到真实 alpha。
```

Do not claim the provider directly returned perfect transparency unless the artifact proves that exact route.

## Metadata To Record

The CLI writes a metadata file like:

```json
{
  "transparent_output": true,
  "transparency_source": "generated_chroma_background_plus_postprocess",
  "background": {
    "mode": "auto",
    "detected": "#ff00ff"
  },
  "alpha": {
    "bbox": [12, 8, 508, 500],
    "alpha_changed": true,
    "background_like_cleanup_tolerance": 129,
    "removed_background_like_pixels": 42,
    "min_island_area": 64,
    "removed_island_pixels": 3
  },
  "edge_cleanup_details": {
    "mode": "rgb-unmix-despill",
    "rgb_only": true,
    "alpha_preserved_after_rgb_cleanup": true,
    "edge_decontaminate_strength": 0.78,
    "rgb_unmixed_pixels": 18,
    "rgb_decontaminated_pixels": 31
  }
}
```

When reporting, include the final transparent PNG path and metadata path. Mention preview path only as a visual check, not as the deliverable.
