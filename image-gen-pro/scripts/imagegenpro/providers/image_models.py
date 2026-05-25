from __future__ import annotations

from math import gcd
from pathlib import Path
from typing import Any

from ..constants import (
    GPT_IMAGE_2_MODEL,
    IMAGE_MODEL_ALIASES,
    MJ_MODEL,
    NANO_BANANA_MODEL,
    PROVIDER_PAYLOAD_SCHEMA,
)
from ..errors import UsageError
from ..media import prepare_media_item


SIZE_SHORTCUTS = {
    "auto": "auto",
    "square": "1024x1024",
    "portrait": "1024x1536",
    "landscape": "1536x1024",
    "2k": "2048x2048",
    "wide": "2048x1152",
    "4k": "3840x2160",
    "tall": "2160x3840",
}
GPT_QUALITIES = {"auto", "low", "medium", "high"}
NB_QUALITY_MAP = {
    "auto": None,
    "low": "0.5K",
    "medium": "1K",
    "high": "2K",
    "0.5k": "0.5K",
    "1k": "1K",
    "2k": "2K",
    "4k": "4K",
}
OUTPUT_FORMATS = {"png", "jpeg", "webp"}
MODERATION = {"auto", "low"}
MASK_MAX_BYTES = 50 * 1024 * 1024


def normalize_image_model(value: str | None) -> str:
    key = (value or GPT_IMAGE_2_MODEL).strip().lower()
    if key not in IMAGE_MODEL_ALIASES:
        allowed = ", ".join(IMAGE_MODEL_ALIASES)
        raise UsageError(f"--model must be one of: {allowed}")
    return IMAGE_MODEL_ALIASES[key]


def build_generate_payload(args, prompt: str, run_dir: Path | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    model = normalize_image_model(args.model)
    if getattr(args, "image", None):
        raise UsageError("--image is edit-only")
    if getattr(args, "mask", None):
        raise UsageError("--mask is edit-only")
    request, warnings = _base_request(args, prompt, model)
    if model == GPT_IMAGE_2_MODEL and args.moderation:
        if args.moderation not in MODERATION:
            raise UsageError("--moderation must be one of: auto, low")
        request["moderation"] = args.moderation
    endpoint = "/mj/submit/imagine" if model == MJ_MODEL else "/v1/images/generations"
    method = "mj.imagine" if model == MJ_MODEL else "images.generate"
    return _payload(model, "generate", method, endpoint, request, [], warnings), _media_manifest([], args.prepare_local_media)


def build_edit_payload(args, prompt: str, run_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    model = normalize_image_model(args.model)
    request, warnings = _base_request(args, prompt, model)
    media: list[dict[str, Any]] = []
    for path in args.image:
        item, item_warnings = _media_item(path, "image", run_dir, args.prepare_local_media)
        media.append(item)
        warnings.extend(item_warnings)
    request["image"] = [_file_placeholder(item) for item in media]
    if args.mask:
        if model != GPT_IMAGE_2_MODEL:
            raise UsageError("--mask is currently only supported for gpt-image-2")
        mask, mask_warnings = _media_item(args.mask, "mask", run_dir, args.prepare_local_media)
        _validate_gpt_mask(media[0], mask)
        media.append(mask)
        warnings.extend(mask_warnings)
        request["mask"] = _file_placeholder(mask)
    endpoint = "/mj/submit/imagine" if model == MJ_MODEL else "/v1/images/edits"
    method = "mj.imagine" if model == MJ_MODEL else "images.edit"
    return _payload(model, "edit", method, endpoint, request, media, warnings), _media_manifest(media, args.prepare_local_media)


def _base_request(args, prompt: str, model: str) -> tuple[dict[str, Any], list[str]]:
    if model == GPT_IMAGE_2_MODEL:
        return _gpt_request(args, prompt)
    if model == NANO_BANANA_MODEL:
        return _nb_request(args, prompt, model)
    if model == MJ_MODEL:
        return _mj_request(args, prompt, model)
    raise UsageError(f"unsupported model: {model}")


def _gpt_request(args, prompt: str) -> tuple[dict[str, Any], list[str]]:
    if args.n < 1:
        raise UsageError("--n must be at least 1")
    if args.quality not in GPT_QUALITIES:
        raise UsageError("--quality must be one of: auto, low, medium, high")
    output_format = args.output_format.lower()
    if output_format not in OUTPUT_FORMATS:
        raise UsageError("--output-format must be one of: png, jpeg, webp")
    if args.output_compression is not None:
        if output_format == "png":
            raise UsageError("--output-compression is only valid for jpeg or webp")
        if not 0 <= args.output_compression <= 100:
            raise UsageError("--output-compression must be between 0 and 100")
    if args.background == "transparent":
        raise UsageError("background=transparent is not supported for gpt-image-2")

    request: dict[str, Any] = {
        "model": GPT_IMAGE_2_MODEL,
        "prompt": prompt,
        "n": args.n,
        "size": _normalize_size(args.size),
        "quality": args.quality,
        "output_format": output_format,
    }
    warnings: list[str] = []
    if args.background:
        request["background"] = args.background
    if args.output_compression is not None:
        request["output_compression"] = args.output_compression
    if args.user:
        request["user"] = args.user
    if _large_experimental_size(request["size"]):
        warnings.append("size is above 2560x1440 total pixels and should be treated as experimental")
    return request, warnings


def _nb_request(args, prompt: str, model: str) -> tuple[dict[str, Any], list[str]]:
    if args.n != 1:
        raise UsageError("nano-banana route currently supports only --n 1")
    if args.background:
        raise UsageError("--background is currently only supported for gpt-image-2")
    if args.moderation:
        raise UsageError("--moderation is currently only supported for gpt-image-2")
    if args.output_compression is not None:
        raise UsageError("--output-compression is currently only supported for gpt-image-2")
    output_format = args.output_format.lower()
    if output_format not in OUTPUT_FORMATS:
        raise UsageError("--output-format must be one of: png, jpeg, webp")
    request: dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "response_format": "b64_json",
    }
    aspect_ratio = _aspect_ratio_from_size(args.size)
    if aspect_ratio:
        request["aspect_ratio"] = aspect_ratio
    quality = _nb_quality(args.quality)
    if quality:
        request["quality"] = quality
    if args.user:
        request["user"] = args.user
    return request, []


def _mj_request(args, prompt: str, model: str) -> tuple[dict[str, Any], list[str]]:
    if args.n != 1:
        raise UsageError("mj route currently supports only --n 1")
    if args.background:
        raise UsageError("--background is currently only supported for gpt-image-2")
    if args.moderation:
        raise UsageError("--moderation is currently only supported for gpt-image-2")
    if args.output_compression is not None:
        raise UsageError("--output-compression is currently only supported for gpt-image-2")
    if args.quality != "auto":
        raise UsageError("mj route quality is prompt-level; keep --quality auto and put native MJ parameters such as --sd, --hd, or --q in the prompt")
    output_format = args.output_format.lower()
    if output_format not in OUTPUT_FORMATS:
        raise UsageError("--output-format must be one of: png, jpeg, webp")
    final_prompt = prompt
    aspect_ratio = _aspect_ratio_from_size(args.size)
    if aspect_ratio and "--ar " not in final_prompt and "--aspect " not in final_prompt:
        final_prompt = f"{final_prompt} --ar {aspect_ratio}".strip()
    return {
        "model": model,
        "prompt": final_prompt,
        "base64Array": [],
        "notifyHook": "",
        "state": "",
        "botType": "MID_JOURNEY",
    }, []


def _payload(provider: str, command: str, method: str, endpoint: str, request: dict[str, Any], media: list[dict[str, Any]], warnings: list[str]) -> dict[str, Any]:
    return {
        "schema": PROVIDER_PAYLOAD_SCHEMA,
        "provider": provider,
        "command": command,
        "method": method,
        "endpoint": endpoint,
        "provider_api_call": False,
        "request": request,
        "files": media,
        "warnings": warnings,
    }


def _normalize_size(value: str) -> str:
    size = SIZE_SHORTCUTS.get(value, value)
    if size == "auto":
        return size
    try:
        width_s, height_s = size.lower().split("x", 1)
        width = int(width_s)
        height = int(height_s)
    except ValueError as exc:
        allowed = ", ".join(SIZE_SHORTCUTS)
        raise UsageError(f"--size must be a shortcut ({allowed}) or WIDTHxHEIGHT") from exc
    if width <= 0 or height <= 0:
        raise UsageError("--size dimensions must be positive")
    if width > 3840 or height > 3840:
        raise UsageError("--size dimensions must be <= 3840")
    if width % 16 != 0 or height % 16 != 0:
        raise UsageError("--size dimensions must be multiples of 16")
    long_edge = max(width, height)
    short_edge = min(width, height)
    if long_edge / short_edge > 3:
        raise UsageError("--size aspect ratio must be <= 3:1")
    pixels = width * height
    if pixels < 655360 or pixels > 8294400:
        raise UsageError("--size total pixels must be between 655360 and 8294400")
    return f"{width}x{height}"


def _aspect_ratio_from_size(value: str) -> str | None:
    size = SIZE_SHORTCUTS.get(value, value).strip().lower()
    if size == "auto":
        return None
    if ":" in size and "x" not in size:
        left, right = size.split(":", 1)
        try:
            width = int(left)
            height = int(right)
        except ValueError as exc:
            raise UsageError("--size aspect ratio must be WIDTH:HEIGHT") from exc
        if width <= 0 or height <= 0:
            raise UsageError("--size aspect ratio dimensions must be positive")
    else:
        normalized = _normalize_size(size)
        width_s, height_s = normalized.split("x", 1)
        width = int(width_s)
        height = int(height_s)
    divisor = gcd(width, height)
    return f"{width // divisor}:{height // divisor}"


def _nb_quality(value: str) -> str | None:
    key = value.strip().lower()
    if key not in NB_QUALITY_MAP:
        allowed = ", ".join(["auto", "low", "medium", "high", "0.5K", "1K", "2K", "4K"])
        raise UsageError(f"--quality for nano-banana must be one of: {allowed}")
    return NB_QUALITY_MAP[key]


def _large_experimental_size(size: str) -> bool:
    if size == "auto":
        return False
    width_s, height_s = size.split("x", 1)
    return int(width_s) * int(height_s) > 2560 * 1440


def _validate_gpt_mask(first_image: dict[str, Any], mask: dict[str, Any]) -> None:
    image_format = first_image.get("format")
    mask_format = mask.get("format")
    image_width = first_image.get("width")
    image_height = first_image.get("height")
    mask_width = mask.get("width")
    mask_height = mask.get("height")
    if None in {image_format, mask_format, image_width, image_height, mask_width, mask_height}:
        raise UsageError("--mask validation requires --prepare-local-media auto so format, dimensions, and alpha can be checked")
    if mask_format != image_format:
        raise UsageError("--mask format must match the first --image for gpt-image-2 edits")
    if first_image.get("size_bytes", 0) >= MASK_MAX_BYTES or mask.get("size_bytes", 0) >= MASK_MAX_BYTES:
        raise UsageError("--image and --mask must each be less than 50MB for gpt-image-2 edits")
    if (mask_width, mask_height) != (image_width, image_height):
        raise UsageError("--mask dimensions must match the first --image for gpt-image-2 edits")
    if mask.get("has_alpha") is not True:
        raise UsageError("--mask must have an alpha channel for gpt-image-2 edits")


def _media_item(raw: str, role: str, run_dir: Path, prepare_mode: str) -> tuple[dict[str, Any], list[str]]:
    return prepare_media_item(raw, role, run_dir, prepare_mode)


def _media_manifest(media: list[dict[str, Any]], prepare_mode: str) -> dict[str, Any]:
    return {
        "schema": "image-gen-pro.media-manifest.v1",
        "prepare_local_media": prepare_mode,
        "inputs": media,
        "outputs": [],
    }


def _file_placeholder(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "role": item["role"],
        "path": item["path"],
        "sha256": item["sha256"],
        "size_bytes": item["size_bytes"],
    }
