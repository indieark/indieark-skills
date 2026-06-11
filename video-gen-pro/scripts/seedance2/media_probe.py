"""Local media metadata helpers used by run artifacts and asset serving."""

from __future__ import annotations

import hashlib
import json
import mimetypes
import os
import shutil
import struct
import subprocess
from pathlib import Path

from seedance2.constants import MEDIA_LIMITS_MB
from seedance2.http import is_http_url


def local_media_metadata(source: str, kind: str | None = None) -> dict:
    if is_http_url(source) or source.startswith(("data:", "asset://")):
        return {"source_type": "url"}
    path = Path(source).expanduser()
    if not path.exists() or not path.is_file():
        return {"source_type": "missing_local_file", "source_path": str(path)}

    data = path.read_bytes()
    mime, _ = mimetypes.guess_type(str(path))
    detected_kind = kind or _kind_from_mime(mime)
    meta = {
        "source_type": "local_file",
        "source_path": str(path),
        "sha256": hashlib.sha256(data).hexdigest(),
        "size_bytes": len(data),
        "mime": mime,
        "extension": path.suffix.lower(),
    }
    if detected_kind == "image":
        meta.update(_image_metadata(data))
    elif detected_kind in {"video", "audio"}:
        meta.update(_ffprobe_metadata(path, detected_kind))
    meta["warnings"] = _metadata_warnings(meta, detected_kind)
    return meta


def _kind_from_mime(mime: str | None) -> str | None:
    if not mime:
        return None
    return mime.split("/", 1)[0]


def _image_metadata(data: bytes) -> dict:
    dimensions = _image_dimensions(data)
    if not dimensions:
        return {"media_probe": {"kind": "image", "available": False}}
    width, height = dimensions
    return {
        "media_probe": {"kind": "image", "available": True},
        "width": width,
        "height": height,
        "pixels": width * height,
    }


def _image_dimensions(data: bytes) -> tuple[int, int] | None:
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    if data[:6] in (b"GIF87a", b"GIF89a") and len(data) >= 10:
        return struct.unpack("<HH", data[6:10])
    if data.startswith(b"\xff\xd8"):
        return _jpeg_dimensions(data)
    return None


def _jpeg_dimensions(data: bytes) -> tuple[int, int] | None:
    index = 2
    while index + 9 < len(data):
        if data[index] != 0xFF:
            index += 1
            continue
        marker = data[index + 1]
        index += 2
        if marker in {0xD8, 0xD9}:
            continue
        if index + 2 > len(data):
            return None
        size = int.from_bytes(data[index:index + 2], "big")
        if size < 2 or index + size > len(data):
            return None
        if marker in {
            0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
            0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
        }:
            height = int.from_bytes(data[index + 3:index + 5], "big")
            width = int.from_bytes(data[index + 5:index + 7], "big")
            return width, height
        index += size
    return None


def _ffprobe_metadata(path: Path, kind: str) -> dict:
    ffprobe = os.environ.get("SEEDANCE_FFPROBE_BIN", "ffprobe")
    ffprobe_path = shutil.which(ffprobe)
    if not ffprobe_path:
        return {
            "media_probe": {
                "kind": kind,
                "tool": "ffprobe",
                "available": False,
                "reason": "not_found",
            }
        }
    command = [
        ffprobe_path,
        "-v",
        "error",
        "-show_streams",
        "-show_format",
        "-of",
        "json",
        str(path),
    ]
    try:
        proc = subprocess.run(
            command,
            text=True,
            capture_output=True,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "media_probe": {
                "kind": kind,
                "tool": "ffprobe",
                "available": False,
                "reason": str(exc),
            }
        }
    if proc.returncode != 0:
        return {
            "media_probe": {
                "kind": kind,
                "tool": "ffprobe",
                "available": False,
                "reason": proc.stderr.strip()[:300],
            }
        }
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {
            "media_probe": {
                "kind": kind,
                "tool": "ffprobe",
                "available": False,
                "reason": "invalid_json",
            }
        }
    return _extract_ffprobe_fields(data, kind)


def _extract_ffprobe_fields(data: dict, kind: str) -> dict:
    streams = data.get("streams") or []
    selected = next(
        (
            stream
            for stream in streams
            if stream.get("codec_type") == ("video" if kind == "video" else "audio")
        ),
        {},
    )
    result = {
        "media_probe": {"kind": kind, "tool": "ffprobe", "available": True},
        "codec": selected.get("codec_name"),
        "duration_seconds": _float_or_none(
            selected.get("duration") or (data.get("format") or {}).get("duration")
        ),
    }
    if kind == "video":
        result["width"] = selected.get("width")
        result["height"] = selected.get("height")
        result["fps"] = _fps(selected.get("avg_frame_rate") or selected.get("r_frame_rate"))
        result["frame_count"] = _int_or_none(selected.get("nb_frames"))
    return result


def _fps(value: str | None) -> float | None:
    if not value or value == "0/0":
        return None
    if "/" not in value:
        return _float_or_none(value)
    numerator, denominator = value.split("/", 1)
    try:
        denom = float(denominator)
        return round(float(numerator) / denom, 3) if denom else None
    except ValueError:
        return None


def _float_or_none(value: object) -> float | None:
    try:
        return round(float(value), 3)
    except (TypeError, ValueError):
        return None


def _int_or_none(value: object) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _metadata_warnings(meta: dict, kind: str | None) -> list[str]:
    warnings: list[str] = []
    if kind in MEDIA_LIMITS_MB and meta.get("size_bytes"):
        limit_bytes = MEDIA_LIMITS_MB[kind] * 1024 * 1024
        if meta["size_bytes"] > limit_bytes:
            warnings.append(f"{kind} file exceeds {MEDIA_LIMITS_MB[kind]}MB")
    if kind == "video":
        if meta.get("extension") not in {".mp4", ".mov"}:
            warnings.append("video extension should be .mp4 or .mov")
        codec = (meta.get("codec") or "").lower()
        if codec and codec not in {"h264", "hevc", "h265"}:
            warnings.append("video codec should be H.264/AVC or H.265/HEVC")
        duration = meta.get("duration_seconds")
        if duration is not None and not (2 <= duration <= 15):
            warnings.append("single reference video duration should be 2-15 seconds")
        fps = meta.get("fps")
        if fps is not None and not (24 <= fps <= 60):
            warnings.append("video FPS should be 24-60")
    return warnings
