from __future__ import annotations

from math import gcd, sqrt
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


SIZE_TIERS = {
    "1080p": 1920 * 1080,
    "2k": 2560 * 1440,
    "4k": 3840 * 2160,
}
MIN_PIXELS = 655_360
MAX_PIXELS = 8_294_400
MAX_EDGE = 3840
SIZE_MULTIPLE = 16
MAX_ASPECT_RATIO = 3
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
        "size": _normalize_gpt_size(args.size, args.aspect),
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
    aspect_ratio = _aspect_ratio_from_args(args.size, args.aspect)
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
    aspect_ratio = _aspect_ratio_from_args(args.size, args.aspect)
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


def _normalize_gpt_size(value: str, aspect: str | None = None) -> str:
    size = value.strip().lower()
    if size == "auto":
        if aspect:
            raise UsageError("--aspect requires --size 1080p, 2k, 4k, or WIDTHxHEIGHT for gpt-image-2")
        return size
    if size in SIZE_TIERS:
        if not aspect:
            allowed = ", ".join(SIZE_TIERS)
            raise UsageError(f"--aspect is required when --size is one of: {allowed}")
        width, height = _dimensions_from_tier(size, aspect)
        return f"{width}x{height}"
    if aspect:
        raise UsageError("--aspect cannot be combined with explicit WIDTHxHEIGHT")
    width, height = _parse_literal_size(size)
    _validate_size_dimensions(width, height)
    return f"{width}x{height}"


def _parse_literal_size(size: str) -> tuple[int, int]:
    try:
        width_s, height_s = size.lower().split("x", 1)
        return int(width_s), int(height_s)
    except ValueError as exc:
        allowed = ", ".join(["auto", *SIZE_TIERS, "WIDTHxHEIGHT"])
        raise UsageError(f"--size must be one of: {allowed}") from exc


def _validate_size_dimensions(width: int, height: int) -> None:
    if width <= 0 or height <= 0:
        raise UsageError("--size dimensions must be positive")
    if width > MAX_EDGE or height > MAX_EDGE:
        raise UsageError(f"--size dimensions must be <= {MAX_EDGE}")
    if width % SIZE_MULTIPLE != 0 or height % SIZE_MULTIPLE != 0:
        raise UsageError(f"--size dimensions must be multiples of {SIZE_MULTIPLE}")
    long_edge = max(width, height)
    short_edge = min(width, height)
    if long_edge / short_edge > MAX_ASPECT_RATIO:
        raise UsageError(f"--size aspect ratio must be <= {MAX_ASPECT_RATIO}:1")
    pixels = width * height
    if pixels < MIN_PIXELS or pixels > MAX_PIXELS:
        raise UsageError(f"--size total pixels must be between {MIN_PIXELS} and {MAX_PIXELS}")


def _dimensions_from_tier(size: str, aspect: str) -> tuple[int, int]:
    width_ratio, height_ratio = _parse_aspect(aspect)
    target_pixels = SIZE_TIERS[size]
    raw_width = sqrt(target_pixels * width_ratio / height_ratio)
    raw_height = sqrt(target_pixels * height_ratio / width_ratio)
    max_raw_edge = max(raw_width, raw_height)
    if max_raw_edge > MAX_EDGE:
        scale = MAX_EDGE / max_raw_edge
        raw_width *= scale
        raw_height *= scale
    width = _round_to_multiple(raw_width)
    height = _round_to_multiple(raw_height)
    if width * height > MAX_PIXELS:
        scale = sqrt(MAX_PIXELS / (width * height))
        width = _floor_to_multiple(width * scale)
        height = _floor_to_multiple(height * scale)
    _validate_size_dimensions(width, height)
    return width, height


def _round_to_multiple(value: float) -> int:
    return max(SIZE_MULTIPLE, int(round(value / SIZE_MULTIPLE)) * SIZE_MULTIPLE)


def _floor_to_multiple(value: float) -> int:
    return max(SIZE_MULTIPLE, int(value // SIZE_MULTIPLE) * SIZE_MULTIPLE)


def _aspect_ratio_from_args(size_value: str, aspect: str | None) -> str | None:
    size = size_value.strip().lower()
    if aspect:
        if size in SIZE_TIERS:
            raise UsageError(f"--size {size} is only available for gpt-image-2")
        if size != "auto":
            raise UsageError("--aspect cannot be combined with explicit WIDTHxHEIGHT")
        width, height = _parse_aspect(aspect)
    elif size == "auto":
        return None
    elif size in SIZE_TIERS:
        raise UsageError(f"--size {size} is only available for gpt-image-2")
    else:
        width, height = _parse_literal_size(size)
        _validate_size_dimensions(width, height)
    divisor = gcd(width, height)
    return f"{width // divisor}:{height // divisor}"


def _parse_aspect(value: str) -> tuple[int, int]:
    try:
        width_s, height_s = value.strip().lower().split(":", 1)
        width = int(width_s)
        height = int(height_s)
    except ValueError as exc:
        raise UsageError("--aspect must be WIDTH:HEIGHT") from exc
    if width <= 0 or height <= 0:
        raise UsageError("--aspect dimensions must be positive")
    long_edge = max(width, height)
    short_edge = min(width, height)
    if long_edge / short_edge > MAX_ASPECT_RATIO:
        raise UsageError(f"--aspect ratio must be <= {MAX_ASPECT_RATIO}:1")
    return width, height


def _nb_quality(value: str) -> str | None:
    key = value.strip().lower()
    if key not in NB_QUALITY_MAP:
        allowed = ", ".join(["auto", "low", "medium", "high", "0.5K", "1K", "2K", "4K"])
        raise UsageError(f"--quality for nano-banana must be one of: {allowed}")
    return NB_QUALITY_MAP[key]


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
