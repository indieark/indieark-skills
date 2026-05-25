# Edit With Local Media

Use when the user provides a local source image and optionally a mask.

## Dry-Run Payload

```powershell
python scripts\imagen.py edit --prompt "Replace the background with a clean studio setup" --image .\input.png --mask .\mask.png --prepare-local-media auto --dry-run-payload --run-id edit-media-dry-run
```

Inspect the prepared media and request:

```powershell
python scripts\imagen.py runs show edit-media-dry-run
```

## Real Edit

```powershell
python scripts\imagen.py edit --prompt "Replace the background with a clean studio setup" --image .\input.png --mask .\mask.png --prepare-local-media auto --route auto --output-file .\outputs\edited.png --run-id edit-media
```

## When To Use `off`

```powershell
python scripts\imagen.py edit --prompt "..." --image .\input.bin --prepare-local-media off --dry-run-payload
```

Use `off` only when debugging path/hash behavior or intentionally bypassing local image inspection. The default `auto` is safer for real execution.

## Notes

- `auto` accepts local PNG, JPEG, and WebP files.
- With Pillow available, `auto` also resizes/compresses oversized images and converts Pillow-readable non-target formats into PNG/JPEG/WebP.
- `auto` writes accepted or normalized inputs into `_work/image_gen_runs/<run-id>/prepared-media/`.
- User originals are never overwritten.
- Mask files without alpha are rejected.
- GPT masks must match the first input image format and dimensions, each submitted file must be less than 50MB, and the mask must include alpha; mask guidance is prompt-based.
