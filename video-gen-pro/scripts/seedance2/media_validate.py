"""Official local media spec validation before task submission."""

from __future__ import annotations

import argparse
from pathlib import Path

from seedance2.constants import (
    EXIT_USAGE,
    MAX_MEDIA_ASPECT_RATIO,
    MAX_MEDIA_EDGE_PX,
    MAX_REFERENCE_AUDIO_SECONDS,
    MAX_REFERENCE_AUDIO_TOTAL_SECONDS,
    MAX_REFERENCE_VIDEO_FPS,
    MAX_REFERENCE_VIDEO_PIXELS,
    MAX_REFERENCE_VIDEO_SECONDS,
    MAX_REFERENCE_VIDEO_TOTAL_SECONDS,
    MEDIA_LIMITS_MB,
    MIN_MEDIA_ASPECT_RATIO,
    MIN_MEDIA_EDGE_PX,
    MIN_REFERENCE_AUDIO_SECONDS,
    MIN_REFERENCE_VIDEO_FPS,
    MIN_REFERENCE_VIDEO_PIXELS,
    MIN_REFERENCE_VIDEO_SECONDS,
    SUPPORTED_AUDIO_EXTENSIONS,
    SUPPORTED_IMAGE_EXTENSIONS,
    SUPPORTED_VIDEO_CODECS,
    SUPPORTED_VIDEO_EXTENSIONS,
)
from seedance2.errors import SeedanceError
from seedance2.http import is_http_url
from seedance2.media_probe import local_media_metadata


def validate_local_media(args: argparse.Namespace) -> list[dict]:
    records: list[dict] = []
    errors: list[str] = []
    video_durations: list[float] = []
    audio_durations: list[float] = []

    for entry in _local_sources(args):
        meta = local_media_metadata(entry["source"], entry["kind"])
        record = {
            "role": entry["role"],
            "kind": entry["kind"],
            "source": entry["source"],
            "status": "checked",
            "warnings": [],
            "errors": [],
        }
        _validate_common(meta, record)
        if entry["kind"] == "image":
            _validate_image(meta, record)
        elif entry["kind"] == "video":
            _validate_video(meta, record, video_durations)
        elif entry["kind"] == "audio":
            _validate_audio(meta, record, audio_durations)
        records.append(record)
        errors.extend(record["errors"])

    _validate_total_duration(
        "reference video",
        video_durations,
        MAX_REFERENCE_VIDEO_TOTAL_SECONDS,
        errors,
        records,
    )
    _validate_total_duration(
        "reference audio",
        audio_durations,
        MAX_REFERENCE_AUDIO_TOTAL_SECONDS,
        errors,
        records,
    )

    args.media_validation = records
    if errors:
        raise SeedanceError(
            "local media does not meet Seedance 2.0 input requirements",
            code=EXIT_USAGE,
            payload={"errors": errors, "validation": records},
        )
    return records


def _validate_common(meta: dict, record: dict) -> None:
    kind = record["kind"]
    extension = (meta.get("extension") or "").lower()
    allowed = {
        "image": SUPPORTED_IMAGE_EXTENSIONS,
        "video": SUPPORTED_VIDEO_EXTENSIONS,
        "audio": SUPPORTED_AUDIO_EXTENSIONS,
    }[kind]
    if extension and extension not in allowed:
        record["errors"].append(
            f"{kind} extension must be one of {', '.join(allowed)}: {record['source']}"
        )
    size_bytes = meta.get("size_bytes")
    if size_bytes:
        limit_bytes = MEDIA_LIMITS_MB[kind] * 1024 * 1024
        if size_bytes > limit_bytes:
            record["errors"].append(
                f"{kind} file exceeds {MEDIA_LIMITS_MB[kind]}MB: {record['source']}"
            )


def _validate_image(meta: dict, record: dict) -> None:
    width = meta.get("width")
    height = meta.get("height")
    if width is None or height is None:
        record["warnings"].append(
            "image dimensions unavailable; width/height/aspect ratio were not validated"
        )
        return
    if not _edge_in_range(width) or not _edge_in_range(height):
        record["errors"].append(
            f"image width and height must be {MIN_MEDIA_EDGE_PX}-{MAX_MEDIA_EDGE_PX}px: "
            f"{width}x{height}"
        )
    _validate_aspect_ratio("image", width, height, record)


def _validate_video(meta: dict, record: dict, durations: list[float]) -> None:
    codec = (meta.get("codec") or "").lower()
    if codec and codec not in SUPPORTED_VIDEO_CODECS:
        record["errors"].append("video codec must be H.264/AVC or H.265/HEVC")
    duration = meta.get("duration_seconds")
    if duration is None:
        record["warnings"].append(
            "video duration unavailable; duration and total duration were not validated"
        )
    else:
        durations.append(float(duration))
        if not (MIN_REFERENCE_VIDEO_SECONDS <= duration <= MAX_REFERENCE_VIDEO_SECONDS):
            record["errors"].append(
                f"single reference video duration must be "
                f"{MIN_REFERENCE_VIDEO_SECONDS}-{MAX_REFERENCE_VIDEO_SECONDS}s: {duration}s"
            )
    width = meta.get("width")
    height = meta.get("height")
    if width is None or height is None:
        record["warnings"].append(
            "video dimensions unavailable; pixel count and aspect ratio were not validated"
        )
    else:
        if not _edge_in_range(width) or not _edge_in_range(height):
            record["errors"].append(
                f"video width and height must be {MIN_MEDIA_EDGE_PX}-{MAX_MEDIA_EDGE_PX}px: "
                f"{width}x{height}"
            )
        pixels = int(width) * int(height)
        if not (MIN_REFERENCE_VIDEO_PIXELS <= pixels <= MAX_REFERENCE_VIDEO_PIXELS):
            record["errors"].append(
                f"video pixel count must be {MIN_REFERENCE_VIDEO_PIXELS}-{MAX_REFERENCE_VIDEO_PIXELS}: "
                f"{pixels}"
            )
        _validate_aspect_ratio("video", int(width), int(height), record)
    fps = meta.get("fps")
    if fps is None:
        record["warnings"].append("video FPS unavailable; FPS was not validated")
    elif not (MIN_REFERENCE_VIDEO_FPS <= fps <= MAX_REFERENCE_VIDEO_FPS):
        record["errors"].append(
            f"video FPS must be {MIN_REFERENCE_VIDEO_FPS}-{MAX_REFERENCE_VIDEO_FPS}: {fps}"
        )


def _validate_audio(meta: dict, record: dict, durations: list[float]) -> None:
    duration = meta.get("duration_seconds")
    if duration is None:
        record["warnings"].append(
            "audio duration unavailable; duration and total duration were not validated"
        )
        return
    durations.append(float(duration))
    if not (MIN_REFERENCE_AUDIO_SECONDS <= duration <= MAX_REFERENCE_AUDIO_SECONDS):
        record["errors"].append(
            f"single reference audio duration must be "
            f"{MIN_REFERENCE_AUDIO_SECONDS}-{MAX_REFERENCE_AUDIO_SECONDS}s: {duration}s"
        )


def _validate_aspect_ratio(kind: str, width: int, height: int, record: dict) -> None:
    if not height:
        record["errors"].append(f"{kind} height must be non-zero")
        return
    ratio = width / height
    if not (MIN_MEDIA_ASPECT_RATIO <= ratio <= MAX_MEDIA_ASPECT_RATIO):
        record["errors"].append(
            f"{kind} aspect ratio must be {MIN_MEDIA_ASPECT_RATIO}-{MAX_MEDIA_ASPECT_RATIO}: "
            f"{ratio:.3f}"
        )


def _validate_total_duration(
    label: str,
    durations: list[float],
    limit: int,
    errors: list[str],
    records: list[dict],
) -> None:
    total = round(sum(durations), 3)
    if total > limit:
        message = f"total {label} duration must be <= {limit}s: {total}s"
        errors.append(message)
        records.append({
            "role": f"{label.replace(' ', '_')}_total",
            "kind": label.split()[-1],
            "source": None,
            "status": "checked",
            "warnings": [],
            "errors": [message],
        })


def _edge_in_range(value: object) -> bool:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return False
    return MIN_MEDIA_EDGE_PX <= number <= MAX_MEDIA_EDGE_PX


def _local_sources(args: argparse.Namespace) -> list[dict]:
    entries: list[dict] = []
    for attr, role in (("first_frame", "first_frame"), ("last_frame", "last_frame")):
        source = getattr(args, attr, None)
        if source and _is_local_file(source):
            entries.append({"role": role, "kind": "image", "source": source})
    for source in getattr(args, "reference_image", None) or []:
        if _is_local_file(source):
            entries.append({"role": "reference_image", "kind": "image", "source": source})
    for source in getattr(args, "reference_video", None) or []:
        if _is_local_file(source):
            entries.append({"role": "reference_video", "kind": "video", "source": source})
    for source in getattr(args, "reference_audio", None) or []:
        if _is_local_file(source):
            entries.append({"role": "reference_audio", "kind": "audio", "source": source})
    return entries


def _is_local_file(source: str) -> bool:
    return not (
        is_http_url(source)
        or source.startswith(("data:", "asset://"))
        or not Path(source).expanduser().is_file()
    )
