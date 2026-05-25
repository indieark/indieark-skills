# Media Handling

Load when using or changing local image inputs for `imagen edit`, including 图生图 / image-to-image requests.

## Image-To-Image Route

- 图生图、以图改图、基于这张图生成/改一版：当源图是待改对象、结构依据或像素输入时，执行路线是 `edit`。
- Required command shape: `imagen edit --prompt ... --image <source> --route auto|codex-cli|api-key --output-file ...`.
- `--mask` is optional and only for local/partial edits.
- For `gpt-image-2`, mask follows the official Images Edit rule: same format and dimensions as the first `--image`, each submitted file less than 50MB, alpha channel required.
- Masking with GPT Image is prompt-based guidance; the model may not follow the exact mask shape with complete precision.
- If the user only wants to imitate style, composition, color, lighting, or material language without preserving the source image as the editable object, use `reverse-prompting.md` and then `imagen generate ...`.
- After execution, report the media manifest / prepared-media evidence through `reporting.md`.

## Current Contract

- `edit --image` and `edit --mask` accept local files only.
- Default behavior is `--prepare-local-media auto`.
- `auto` validates PNG, JPEG, and WebP inputs before route submission.
- When Pillow is available, `auto` also normalizes Pillow-readable non-target formats into PNG/JPEG/WebP.
- When local images exceed the built-in size guard, `auto` creates a compressed/resized run-local copy.
- `auto` records source and prepared width, height, MIME type, format, hash, size, and alpha availability when detectable.
- `auto` writes accepted or normalized local media into `_work/image_gen_runs/<run-id>/prepared-media/` and routes against that copy.
- `off` skips image inspection and copying, but still records path, size, and SHA-256.
- Original user files are never overwritten.
- URL references are still only redacted in neutral `plan` / `dry-run`; they are not fetched.

## Manifest Fields

`media-manifest.json` stores:

- `prepare_local_media`: `auto` or `off`
- `inputs[]`: original path, active path, source/prepared sizes, hashes, role, detected format/MIME/dimensions, preparation actions, preparation status
- `outputs[]`: output image metadata after a real route succeeds

When `auto` is used, `inputs[].path` points to the prepared copy used by provider routes, while `inputs[].source_path` points to the user-provided local file.

## Built-In Guards

- Long edge above `4096` pixels is resized to fit within that edge.
- Files above `20 MiB` are re-saved with compression when Pillow is available.
- RGB images that need resize/compression are saved as JPEG.
- Images with alpha that need resize/compression are saved as WebP.
- Masks that need rewriting are saved as PNG to preserve alpha where possible.
- GPT masks with a different format from the first image, 50MB or larger submitted files, missing alpha, or mismatched dimensions are rejected before provider submission.
- EXIF orientation is normalized when Pillow performs a rewrite.

## Validation Boundary

The built-in validator uses header checks for PNG, JPEG, and WebP, so simple supported inputs work without Pillow. Pillow is recommended for automatic resize, compression, EXIF orientation normalization, and non-target format conversion. If an input needs those operations and Pillow is unavailable, the CLI fails with an install hint rather than submitting a likely-bad provider request.

Mask validation is stricter than ordinary image validation because the provider requires it. `--mask` with `--prepare-local-media off` is rejected if dimensions or alpha cannot be checked.

Do not add provider-specific remote limits here unless they are verified in the provider API reference. This file only owns local media preparation and static input evidence.
