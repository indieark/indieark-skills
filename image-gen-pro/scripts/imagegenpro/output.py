from __future__ import annotations

import base64
from math import ceil, gcd, sqrt
import re
from pathlib import Path
from typing import Any

from .artifacts import sha256_file
from .errors import UsageError
from .media import inspect_image


ALLOWED_OUTPUT_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
FORMAT_EXTENSIONS = {
    "png": ".png",
    "jpeg": ".jpg",
    "webp": ".webp",
}


def resolve_output_base(args, config: dict[str, Any], prompt: str, run_id: str) -> Path:
    output_file = getattr(args, "output_file", None)
    if output_file:
        path = Path(output_file)
        _validate_output_extension(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path
    output_dir = Path(args.output_dir or config.get("output_dir") or "outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    extension = FORMAT_EXTENSIONS[args.output_format.lower()]
    return output_dir / f"{run_id}-{_slug(prompt)}{extension}"


def write_base64_outputs(items: list[dict[str, Any]], output_base: Path, output_format: str) -> list[dict[str, Any]]:
    if not items:
        raise UsageError("provider response did not include image data")
    outputs: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        blob = item.get("b64_json")
        if not isinstance(blob, str) or not blob.strip():
            raise UsageError("provider response image item is missing b64_json")
        target = _indexed_output_path(output_base, index, len(items), output_format)
        image_bytes = base64.b64decode(blob)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(image_bytes)
        outputs.append(_output_item(target, index, output_format))
    return outputs


def output_manifest_items(paths: list[Path], output_format: str) -> list[dict[str, Any]]:
    return [_output_item(path, index, output_format) for index, path in enumerate(paths)]


def build_output_preview(outputs: list[dict[str, Any]], preview_dir: Path) -> dict[str, Any] | None:
    if not outputs:
        return None
    if len(outputs) == 1:
        return _single_output_preview(outputs[0])
    return _contact_sheet_preview(outputs, preview_dir)


def _output_item(path: Path, index: int, output_format: str) -> dict[str, Any]:
    item = {
        "index": index,
        "path": str(path),
        "format": output_format,
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }
    try:
        spec = inspect_image(path)
    except UsageError as exc:
        item.update(_dimension_fields(None, None))
        item["has_alpha"] = None
        item["inspection"] = "failed"
        item["inspection_error"] = str(exc)[:300]
        return item
    item.update(_dimension_fields(spec.get("width"), spec.get("height")))
    item["mime_type"] = spec.get("mime_type")
    item["has_alpha"] = spec.get("has_alpha")
    item["inspection"] = spec.get("inspection")
    return item


def _single_output_preview(output: dict[str, Any]) -> dict[str, Any]:
    preview = {
        "kind": "single",
        "path": output.get("path"),
        "source_count": 1,
    }
    preview.update(_dimension_fields(output.get("width"), output.get("height")))
    return preview


def _contact_sheet_preview(outputs: list[dict[str, Any]], preview_dir: Path) -> dict[str, Any]:
    try:
        from PIL import Image
    except Exception:
        return _unavailable_preview(outputs, "Pillow is required to create multi-image previews")

    images = []
    skipped: list[dict[str, str]] = []
    for output in outputs:
        raw_path = output.get("path")
        if not raw_path:
            continue
        path = Path(str(raw_path))
        try:
            with Image.open(path) as image:
                image.load()
                images.append((path, image.convert("RGBA").copy()))
        except Exception as exc:
            skipped.append({"path": str(path), "error": exc.__class__.__name__})

    if not images:
        preview = _unavailable_preview(outputs, "no output images could be opened for preview")
        if skipped:
            preview["skipped"] = skipped
        return preview

    cell = 256
    padding = 16
    columns = max(1, min(3, ceil(sqrt(len(images)))))
    rows = ceil(len(images) / columns)
    width = columns * cell + (columns + 1) * padding
    height = rows * cell + (rows + 1) * padding
    canvas = Image.new("RGBA", (width, height), (245, 245, 245, 255))

    for index, (_path, image) in enumerate(images):
        thumb = image.copy()
        thumb.thumbnail((cell, cell))
        column = index % columns
        row = index // columns
        left = padding + column * (cell + padding) + (cell - thumb.width) // 2
        top = padding + row * (cell + padding) + (cell - thumb.height) // 2
        tile = Image.new("RGBA", (thumb.width, thumb.height), (255, 255, 255, 255))
        tile.alpha_composite(thumb)
        canvas.alpha_composite(tile, (left, top))

    preview_dir.mkdir(parents=True, exist_ok=True)
    preview_path = preview_dir / "contact-sheet.png"
    try:
        canvas.convert("RGB").save(preview_path, format="PNG", optimize=True)
        spec = inspect_image(preview_path)
    except Exception as exc:
        return _unavailable_preview(outputs, f"failed to create preview contact sheet: {exc.__class__.__name__}")

    preview = {
        "kind": "contact_sheet",
        "path": str(preview_path),
        "source_count": len(outputs),
        "rendered_count": len(images),
        "columns": columns,
        "rows": rows,
    }
    preview.update(_dimension_fields(spec.get("width"), spec.get("height")))
    if skipped:
        preview["skipped"] = skipped
    return preview


def _unavailable_preview(outputs: list[dict[str, Any]], reason: str) -> dict[str, Any]:
    preview = {
        "kind": "unavailable",
        "path": None,
        "source_count": len(outputs),
        "reason": reason,
    }
    preview.update(_dimension_fields(None, None))
    return preview


def _dimension_fields(width: Any, height: Any) -> dict[str, Any]:
    if not isinstance(width, int) or not isinstance(height, int) or width <= 0 or height <= 0:
        return {
            "width": None,
            "height": None,
            "resolution": None,
            "aspect_ratio": None,
        }
    return {
        "width": width,
        "height": height,
        "resolution": f"{width}x{height}",
        "aspect_ratio": _aspect_ratio(width, height),
    }


def _aspect_ratio(width: int, height: int) -> str:
    divisor = gcd(width, height)
    return f"{width // divisor}:{height // divisor}"


def _indexed_output_path(output_base: Path, index: int, total: int, output_format: str) -> Path:
    extension = FORMAT_EXTENSIONS[output_format]
    if output_base.suffix.lower() not in ALLOWED_OUTPUT_EXTENSIONS:
        output_base = output_base.with_suffix(extension)
    if total == 1:
        return output_base
    return output_base.with_name(f"{output_base.stem}_{index}{output_base.suffix}")


def _validate_output_extension(path: Path) -> None:
    if path.suffix.lower() not in ALLOWED_OUTPUT_EXTENSIONS:
        raise UsageError("--output-file must end in .png, .jpg, .jpeg, or .webp")


def _slug(prompt: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", prompt.lower()).strip("-")
    return (slug[:48] or "image").strip("-")
