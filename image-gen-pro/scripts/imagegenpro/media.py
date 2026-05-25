from __future__ import annotations

import shutil
import struct
from pathlib import Path
from typing import Any

from .artifacts import sha256_file
from .errors import UsageError


SUPPORTED_FORMATS = {
    "png": "image/png",
    "jpeg": "image/jpeg",
    "webp": "image/webp",
}
MAX_INPUT_EDGE = 4096
MAX_INPUT_BYTES = 20 * 1024 * 1024
LOSSY_QUALITY = 90


def prepare_media_item(raw: str, role: str, run_dir: Path, mode: str) -> tuple[dict[str, Any], list[str]]:
    if mode not in {"auto", "off"}:
        raise UsageError("--prepare-local-media must be one of: auto, off")
    source = Path(raw)
    if not source.exists() or not source.is_file():
        raise UsageError(f"{role} file does not exist or is not a file: {raw}")

    base = {
        "role": role,
        "source_path": str(source),
        "path": str(source),
        "source_size_bytes": source.stat().st_size,
        "source_sha256": sha256_file(source),
        "size_bytes": source.stat().st_size,
        "sha256": sha256_file(source),
        "preparation": {
            "mode": mode,
            "status": "skipped" if mode == "off" else "prepared",
            "action": "none",
            "tool": None,
            "reason": "local media preparation disabled",
        },
    }
    if mode == "off":
        return base, []

    source_spec = inspect_image(source)
    item = {
        **base,
        "source_format": source_spec["format"],
        "source_mime_type": source_spec["mime_type"],
        "source_width": source_spec.get("width"),
        "source_height": source_spec.get("height"),
        "source_has_alpha": source_spec.get("has_alpha"),
        "source_inspection": source_spec.get("inspection"),
    }
    prepared, prepared_spec, preparation = _prepare_file(source, run_dir, role, item["sha256"], source_spec)
    item.update(prepared_spec)
    warnings = _spec_warnings(item)
    item["path"] = str(prepared)
    item["prepared_path"] = str(prepared)
    item["prepared_size_bytes"] = prepared.stat().st_size
    item["prepared_sha256"] = sha256_file(prepared)
    item["size_bytes"] = item["prepared_size_bytes"]
    item["sha256"] = item["prepared_sha256"]
    item["preparation"] = preparation
    return item, warnings


def inspect_image(path: Path) -> dict[str, Any]:
    pillow = _inspect_with_pillow(path)
    if pillow:
        return pillow
    header = path.read_bytes()[:512]
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return _inspect_png(path)
    if header.startswith(b"\xff\xd8"):
        return _inspect_jpeg(path)
    if _is_webp(header):
        return _inspect_webp(header)
    raise UsageError(f"image file is not a supported PNG, JPEG, or WebP image: {path}")


def _inspect_with_pillow(path: Path) -> dict[str, Any] | None:
    try:
        from PIL import Image
    except Exception:
        return None
    try:
        with Image.open(path) as image:
            image.load()
            fmt = (image.format or "").lower()
            if fmt == "jpg":
                fmt = "jpeg"
            has_alpha = _pillow_has_alpha(image)
            return {
                "format": fmt,
                "mime_type": SUPPORTED_FORMATS.get(fmt, f"image/{fmt or 'unknown'}"),
                "width": image.width,
                "height": image.height,
                "mode": image.mode,
                "has_alpha": has_alpha,
                "inspection": "pillow",
                "exif_orientation": _pillow_exif_orientation(image),
            }
    except UsageError:
        raise
    except Exception as exc:
        raise UsageError(f"image file cannot be opened as an image: {path}") from exc


def _pillow_has_alpha(image) -> bool:
    if image.mode in {"RGBA", "LA"}:
        return True
    return "transparency" in image.info


def _pillow_exif_orientation(image) -> int | None:
    try:
        orientation = image.getexif().get(274)
    except Exception:
        return None
    return orientation if isinstance(orientation, int) else None


def _inspect_png(path: Path) -> dict[str, Any]:
    data = path.read_bytes()[:33]
    if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise UsageError(f"image file is not a valid PNG: {path}")
    width, height = struct.unpack(">II", data[16:24])
    color_type = data[25]
    return {
        "format": "png",
        "mime_type": "image/png",
        "width": width,
        "height": height,
        "has_alpha": color_type in {4, 6},
        "inspection": "header",
    }


def _inspect_jpeg(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    if len(data) < 4 or data[:2] != b"\xff\xd8":
        raise UsageError(f"image file is not a valid JPEG: {path}")
    index = 2
    sof_markers = {
        0xC0,
        0xC1,
        0xC2,
        0xC3,
        0xC5,
        0xC6,
        0xC7,
        0xC9,
        0xCA,
        0xCB,
        0xCD,
        0xCE,
        0xCF,
    }
    while index + 9 < len(data):
        if data[index] != 0xFF:
            index += 1
            continue
        while index < len(data) and data[index] == 0xFF:
            index += 1
        if index >= len(data):
            break
        marker = data[index]
        index += 1
        if marker in {0xD8, 0xD9, 0x01} or 0xD0 <= marker <= 0xD7:
            continue
        if index + 2 > len(data):
            break
        segment_length = struct.unpack(">H", data[index : index + 2])[0]
        if segment_length < 2 or index + segment_length > len(data):
            break
        if marker in sof_markers:
            height, width = struct.unpack(">HH", data[index + 3 : index + 7])
            return {
                "format": "jpeg",
                "mime_type": "image/jpeg",
                "width": width,
                "height": height,
                "has_alpha": False,
                "inspection": "header",
            }
        index += segment_length
    raise UsageError(f"image file is not a valid JPEG: {path}")


def _is_webp(header: bytes) -> bool:
    return len(header) >= 12 and header[:4] == b"RIFF" and header[8:12] == b"WEBP"


def _inspect_webp(header: bytes) -> dict[str, Any]:
    item: dict[str, Any] = {
        "format": "webp",
        "mime_type": "image/webp",
        "inspection": "header",
        "has_alpha": None,
    }
    if len(header) >= 30 and header[12:16] == b"VP8X":
        flags = header[20]
        width = 1 + int.from_bytes(header[24:27], "little")
        height = 1 + int.from_bytes(header[27:30], "little")
        item.update({"width": width, "height": height, "has_alpha": bool(flags & 0x10)})
    return item


def _copy_prepared(source: Path, run_dir: Path, role: str, digest: str, fmt: str) -> Path:
    prepared_dir = run_dir / "prepared-media"
    prepared_dir.mkdir(parents=True, exist_ok=True)
    suffix = source.suffix.lower()
    if not suffix:
        suffix = ".jpg" if fmt == "jpeg" else f".{fmt}"
    destination = prepared_dir / f"{role}-{digest[:12]}{suffix}"
    if not destination.exists() or sha256_file(destination) != digest:
        shutil.copy2(source, destination)
    return destination


def _prepare_file(source: Path, run_dir: Path, role: str, digest: str, source_spec: dict[str, Any]) -> tuple[Path, dict[str, Any], dict[str, Any]]:
    actions = _needed_actions(source, source_spec)
    if actions == ["copy"]:
        prepared = _copy_prepared(source, run_dir, role, digest, source_spec["format"])
        return prepared, _active_spec(source_spec, "copy"), _preparation("copy", "header", prepared)
    prepared = _prepare_with_pillow(source, run_dir, role, digest, source_spec, actions)
    return prepared


def _needed_actions(source: Path, source_spec: dict[str, Any]) -> list[str]:
    actions: list[str] = []
    if source_spec.get("format") not in SUPPORTED_FORMATS:
        actions.append("convert")
    if source_spec.get("exif_orientation") not in {None, 1}:
        actions.append("exif_transpose")
    width = source_spec.get("width")
    height = source_spec.get("height")
    if isinstance(width, int) and isinstance(height, int) and max(width, height) > MAX_INPUT_EDGE:
        actions.append("resize")
    if source.stat().st_size > MAX_INPUT_BYTES:
        actions.append("compress")
    return actions or ["copy"]


def _prepare_with_pillow(source: Path, run_dir: Path, role: str, digest: str, source_spec: dict[str, Any], actions: list[str]) -> tuple[Path, dict[str, Any], dict[str, Any]]:
    try:
        from PIL import Image, ImageOps
    except Exception as exc:
        raise UsageError("Pillow is required to resize, compress, or convert this local image. Install it with: python -m pip install Pillow") from exc

    try:
        with Image.open(source) as image:
            image.load()
            image = ImageOps.exif_transpose(image)
            image = _resize_if_needed(image)
            target_format = _target_format(role, source_spec, actions)
            image = _convert_mode_for_save(image, target_format)
            prepared = _prepared_output_path(run_dir, role, digest, target_format)
            prepared.parent.mkdir(parents=True, exist_ok=True)
            _save_image(image, prepared, target_format)
    except UsageError:
        raise
    except Exception as exc:
        raise UsageError(f"image file cannot be normalized for route submission: {source}") from exc

    prepared_spec = inspect_image(prepared)
    preparation = _preparation(",".join(actions), "pillow", prepared)
    preparation.update({
        "max_input_edge": MAX_INPUT_EDGE,
        "max_input_bytes": MAX_INPUT_BYTES,
    })
    return prepared, _active_spec(prepared_spec, ",".join(actions)), preparation


def _resize_if_needed(image):
    width, height = image.size
    long_edge = max(width, height)
    if long_edge <= MAX_INPUT_EDGE:
        return image
    scale = MAX_INPUT_EDGE / long_edge
    new_size = (max(1, round(width * scale)), max(1, round(height * scale)))
    try:
        from PIL import Image
        resample = Image.Resampling.LANCZOS
    except Exception:
        resample = 1
    return image.resize(new_size, resample=resample)


def _target_format(role: str, source_spec: dict[str, Any], actions: list[str]) -> str:
    source_format = source_spec.get("format")
    has_alpha = bool(source_spec.get("has_alpha"))
    if role == "mask":
        return "png"
    if "compress" in actions or "resize" in actions:
        return "webp" if has_alpha else "jpeg"
    if source_format in SUPPORTED_FORMATS:
        return str(source_format)
    return "webp" if has_alpha else "jpeg"


def _convert_mode_for_save(image, target_format: str):
    if target_format == "jpeg":
        if image.mode not in {"RGB", "L"}:
            return image.convert("RGB")
        return image
    if target_format in {"png", "webp"} and image.mode == "CMYK":
        return image.convert("RGB")
    return image


def _save_image(image, path: Path, target_format: str) -> None:
    if target_format == "jpeg":
        image.save(path, format="JPEG", quality=LOSSY_QUALITY, optimize=True, progressive=True)
    elif target_format == "webp":
        image.save(path, format="WEBP", quality=LOSSY_QUALITY, method=6)
    elif target_format == "png":
        image.save(path, format="PNG", optimize=True)
    else:
        raise UsageError(f"unsupported prepared image format: {target_format}")


def _prepared_output_path(run_dir: Path, role: str, digest: str, fmt: str) -> Path:
    extension = ".jpg" if fmt == "jpeg" else f".{fmt}"
    return run_dir / "prepared-media" / f"{role}-{digest[:12]}{extension}"


def _active_spec(spec: dict[str, Any], action: str) -> dict[str, Any]:
    return {
        "format": spec.get("format"),
        "mime_type": spec.get("mime_type"),
        "width": spec.get("width"),
        "height": spec.get("height"),
        "mode": spec.get("mode"),
        "has_alpha": spec.get("has_alpha"),
        "inspection": spec.get("inspection"),
        "preparation_action": action,
    }


def _preparation(action: str, tool: str, prepared: Path) -> dict[str, Any]:
    return {
        "mode": "auto",
        "status": "prepared",
        "action": action,
        "actions": action.split(","),
        "tool": tool,
        "reason": "route submissions use normalized run-local media",
        "copied": action == "copy",
        "path": str(prepared),
    }


def _spec_warnings(item: dict[str, Any]) -> list[str]:
    warnings = []
    if item.get("width") is not None and item.get("height") is not None:
        if item["width"] <= 0 or item["height"] <= 0:
            raise UsageError("image dimensions must be positive")
    return warnings
