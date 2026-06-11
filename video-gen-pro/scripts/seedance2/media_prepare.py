"""Optional local image/audio preparation before Base64 payload encoding."""

from __future__ import annotations

import argparse
import math
import os
import shutil
import subprocess
from pathlib import Path

from seedance2.artifacts import resolve_run_dir
from seedance2.constants import (
    AUDIO_PREPARE_BITRATE,
    AUDIO_PREPARE_TARGET_MB,
    EXIT_USAGE,
    IMAGE_PREPARE_MAX_EDGE,
    IMAGE_PREPARE_TARGET_MB,
    MAX_MEDIA_ASPECT_RATIO,
    MAX_MEDIA_EDGE_PX,
    MAX_REQUEST_BODY_MB,
    MAX_REFERENCE_AUDIO_SECONDS,
    MAX_REFERENCE_AUDIO_TOTAL_SECONDS,
    MAX_REFERENCE_VIDEO_FPS,
    MAX_REFERENCE_VIDEO_PIXELS,
    MAX_REFERENCE_VIDEO_SECONDS,
    MEDIA_LIMITS_MB,
    MIN_MEDIA_ASPECT_RATIO,
    MIN_MEDIA_EDGE_PX,
    MIN_REFERENCE_AUDIO_SECONDS,
    MIN_REFERENCE_VIDEO_FPS,
    MIN_REFERENCE_VIDEO_PIXELS,
    SUPPORTED_AUDIO_EXTENSIONS,
    SUPPORTED_IMAGE_EXTENSIONS,
    SUPPORTED_VIDEO_CODECS,
    SUPPORTED_VIDEO_EXTENSIONS,
)
from seedance2.errors import SeedanceError
from seedance2.http import is_http_url
from seedance2.media_probe import local_media_metadata


def prepare_local_media(args: argparse.Namespace) -> list[dict]:
    if getattr(args, "prepare_local_media", "auto") == "off":
        args.media_preparation = []
        return []

    run_dir = resolve_run_dir(args)
    prepare_dir = run_dir / "prepared"
    records: list[dict] = []
    audio_used_seconds = 0.0
    for attr, kind, index, source in _local_media_sources(args):
        path = Path(source).expanduser()
        decision = _prepare_decision(path, kind, audio_used_seconds)
        if kind == "audio" and decision.get("effective_duration") is not None:
            audio_used_seconds += float(decision["effective_duration"])
        must_prepare = bool(decision["must_prepare"])
        should_prepare = bool(decision["should_prepare"])
        if not should_prepare:
            records.append(_record(kind, source, "kept", reason="within_target"))
            continue
        prepare_dir.mkdir(parents=True, exist_ok=True)
        if kind == "image":
            record = _prepare_image(path, prepare_dir, must_prepare, decision["reasons"])
        elif kind == "audio":
            record = _prepare_audio(
                path,
                prepare_dir,
                must_prepare,
                trim_seconds=decision.get("trim_seconds"),
                reasons=decision["reasons"],
            )
        else:
            record = _prepare_video(path, prepare_dir, must_prepare, decision)
        records.append(record)
        if record["status"] == "prepared":
            _replace_arg_source(args, attr, index, record["prepared_path"])

    args.media_preparation = records
    _validate_base64_budget(args)
    return records


def _local_media_sources(args: argparse.Namespace) -> list[tuple[str, str, int | None, str]]:
    sources: list[tuple[str, str, int | None, str]] = []
    for attr in ("first_frame", "last_frame"):
        source = getattr(args, attr, None)
        if source and _is_local_file(source):
            sources.append((attr, "image", None, source))
    for index, source in enumerate(getattr(args, "reference_image", None) or []):
        if _is_local_file(source):
            sources.append(("reference_image", "image", index, source))
    for index, source in enumerate(getattr(args, "reference_audio", None) or []):
        if _is_local_file(source):
            sources.append(("reference_audio", "audio", index, source))
    if getattr(args, "serve_local_assets", "none") == "cloudflare":
        for index, source in enumerate(getattr(args, "reference_video", None) or []):
            if _is_local_file(source):
                sources.append(("reference_video", "video", index, source))
    return sources


def _is_local_file(source: str) -> bool:
    return not (
        is_http_url(source)
        or source.startswith(("data:", "asset://"))
        or not Path(source).expanduser().is_file()
    )


def _prepare_decision(path: Path, kind: str, audio_used_seconds: float) -> dict:
    meta = local_media_metadata(str(path), kind)
    target_mb = IMAGE_PREPARE_TARGET_MB if kind == "image" else AUDIO_PREPARE_TARGET_MB
    limit_mb = MEDIA_LIMITS_MB[kind]
    size_mb = path.stat().st_size / 1024 / 1024
    reasons: list[str] = []
    must_prepare = False
    should_prepare = size_mb > target_mb
    if size_mb > limit_mb:
        reasons.append(f"size_over_{limit_mb}mb")
        must_prepare = should_prepare = True
    extension = path.suffix.lower()
    if kind == "image":
        if extension not in SUPPORTED_IMAGE_EXTENSIONS:
            reasons.append("unsupported_image_extension")
            must_prepare = should_prepare = True
        if _dimensions_need_prepare(meta):
            reasons.append("image_dimensions_or_ratio_out_of_range")
            must_prepare = should_prepare = True
    elif kind == "audio":
        if extension not in SUPPORTED_AUDIO_EXTENSIONS:
            reasons.append("unsupported_audio_extension")
            must_prepare = should_prepare = True
        duration = meta.get("duration_seconds")
        if duration is not None:
            if duration < MIN_REFERENCE_AUDIO_SECONDS:
                return _cannot_prepare(
                    reasons,
                    f"audio duration is shorter than {MIN_REFERENCE_AUDIO_SECONDS}s and cannot be safely extended",
                )
            remaining = MAX_REFERENCE_AUDIO_TOTAL_SECONDS - audio_used_seconds
            if remaining < MIN_REFERENCE_AUDIO_SECONDS:
                return _cannot_prepare(
                    reasons,
                    "total reference audio duration exceeds 15s and later audio cannot be safely kept",
                )
            target_duration = min(float(duration), MAX_REFERENCE_AUDIO_SECONDS, remaining)
            if target_duration < float(duration):
                reasons.append("trim_audio_to_official_duration")
                must_prepare = should_prepare = True
                return {
                    "must_prepare": must_prepare,
                    "should_prepare": should_prepare,
                    "reasons": reasons,
                    "trim_seconds": round(target_duration, 3),
                    "effective_duration": round(target_duration, 3),
                }
            return {
                "must_prepare": must_prepare,
                "should_prepare": should_prepare,
                "reasons": reasons,
                "trim_seconds": None,
                "effective_duration": float(duration),
            }
    elif kind == "video":
        if extension not in SUPPORTED_VIDEO_EXTENSIONS:
            reasons.append("unsupported_video_extension")
            must_prepare = should_prepare = True
        reasons.extend(_video_prepare_reasons(meta))
        if reasons:
            must_prepare = should_prepare = True
    return {
        "must_prepare": must_prepare,
        "should_prepare": should_prepare,
        "reasons": reasons,
        "trim_seconds": None,
    }


def _cannot_prepare(reasons: list[str], message: str) -> dict:
    return {
        "must_prepare": False,
        "should_prepare": False,
        "reasons": reasons + [message],
        "cannot_prepare": message,
    }


def _dimensions_need_prepare(meta: dict) -> bool:
    width = meta.get("width")
    height = meta.get("height")
    if width is None or height is None:
        return False
    ratio = width / height if height else 0
    return (
        width < MIN_MEDIA_EDGE_PX
        or height < MIN_MEDIA_EDGE_PX
        or width > MAX_MEDIA_EDGE_PX
        or height > MAX_MEDIA_EDGE_PX
        or ratio < MIN_MEDIA_ASPECT_RATIO
        or ratio > MAX_MEDIA_ASPECT_RATIO
    )


def _video_prepare_reasons(meta: dict) -> list[str]:
    reasons: list[str] = []
    codec = (meta.get("codec") or "").lower()
    if codec and codec not in SUPPORTED_VIDEO_CODECS:
        reasons.append("transcode_video_codec")
    duration = meta.get("duration_seconds")
    if duration is not None:
        if duration < 2:
            reasons.append("video_too_short_unfixable")
        elif duration > MAX_REFERENCE_VIDEO_SECONDS:
            reasons.append("trim_video_to_official_duration")
    fps = meta.get("fps")
    if fps is not None and not (MIN_REFERENCE_VIDEO_FPS <= fps <= MAX_REFERENCE_VIDEO_FPS):
        reasons.append("normalize_video_fps")
    width = meta.get("width")
    height = meta.get("height")
    if width is not None and height is not None:
        ratio = width / height if height else 0
        pixels = int(width) * int(height)
        if (
            width < MIN_MEDIA_EDGE_PX
            or height < MIN_MEDIA_EDGE_PX
            or width > MAX_MEDIA_EDGE_PX
            or height > MAX_MEDIA_EDGE_PX
            or ratio < MIN_MEDIA_ASPECT_RATIO
            or ratio > MAX_MEDIA_ASPECT_RATIO
            or pixels < MIN_REFERENCE_VIDEO_PIXELS
            or pixels > MAX_REFERENCE_VIDEO_PIXELS
        ):
            reasons.append("normalize_video_dimensions")
    return reasons


def _prepare_image(path: Path, prepare_dir: Path, must_prepare: bool, reasons: list[str]) -> dict:
    try:
        from PIL import Image
    except ImportError:
        if must_prepare:
            raise SeedanceError(
                "Pillow is required to auto-fix this image format/size/dimensions for "
                "Seedance 2.0; run `python -m pip install pillow`, pass a compliant "
                "image, or provide an HTTPS/signed URL",
                code=EXIT_USAGE,
                payload={
                    "path": str(path),
                    "reasons": reasons,
                    "install": "python -m pip install pillow",
                    "alternatives": [
                        "pass a compliant jpeg/png/webp/bmp/tiff/gif/heic/heif image",
                        "provide an HTTPS/signed image URL",
                    ],
                },
            )
        return _record("image", str(path), "skipped", reason="pillow_not_installed")

    output = prepare_dir / f"{path.stem}-prepared.jpg"
    try:
        with Image.open(path) as image:
            image = image.copy()
            image = _normalize_image_geometry(image)
            if image.mode in {"RGBA", "LA", "P"}:
                background = Image.new("RGB", image.size, (255, 255, 255))
                if image.mode == "P":
                    image = image.convert("RGBA")
                background.paste(image, mask=image.getchannel("A") if "A" in image.getbands() else None)
                image = background
            else:
                image = image.convert("RGB")
            image.save(output, "JPEG", quality=85, optimize=True, progressive=True)
    except Exception as exc:
        if must_prepare:
            raise SeedanceError(
                f"failed to prepare image: {exc}",
                code=EXIT_USAGE,
                payload={"path": str(path)},
            )
        return _record("image", str(path), "skipped", reason=str(exc))

    record = _prepared_record("image", path, output)
    record["reasons"] = reasons
    return record


def _normalize_image_geometry(image):
    width, height = image.size
    scale = 1.0
    if max(width, height) > IMAGE_PREPARE_MAX_EDGE:
        scale = min(scale, IMAGE_PREPARE_MAX_EDGE / max(width, height))
    if max(width, height) > MAX_MEDIA_EDGE_PX:
        scale = min(scale, MAX_MEDIA_EDGE_PX / max(width, height))
    if min(width, height) < MIN_MEDIA_EDGE_PX:
        scale = max(scale, MIN_MEDIA_EDGE_PX / min(width, height))
    if scale != 1.0:
        width = max(1, int(round(width * scale)))
        height = max(1, int(round(height * scale)))
        image = image.resize((width, height))
    target_width, target_height = _bounded_dimensions(width, height)
    if (target_width, target_height) == (width, height):
        return image
    canvas = Image.new("RGBA", (target_width, target_height), (255, 255, 255, 255))
    canvas.paste(image, ((target_width - width) // 2, (target_height - height) // 2))
    return canvas


def _bounded_dimensions(width: int, height: int) -> tuple[int, int]:
    width = max(MIN_MEDIA_EDGE_PX, min(MAX_MEDIA_EDGE_PX, width))
    height = max(MIN_MEDIA_EDGE_PX, min(MAX_MEDIA_EDGE_PX, height))
    ratio = width / height
    if ratio > MAX_MEDIA_ASPECT_RATIO:
        height = max(height, math.ceil(width / MAX_MEDIA_ASPECT_RATIO))
    elif ratio < MIN_MEDIA_ASPECT_RATIO:
        width = max(width, math.ceil(height * MIN_MEDIA_ASPECT_RATIO))
    return int(width), int(height)


def _prepare_audio(
    path: Path,
    prepare_dir: Path,
    must_prepare: bool,
    *,
    trim_seconds: float | None,
    reasons: list[str],
) -> dict:
    ffmpeg = os.environ.get("SEEDANCE_FFMPEG_BIN", "ffmpeg")
    ffmpeg_path = shutil.which(ffmpeg)
    if not ffmpeg_path:
        if must_prepare:
            raise SeedanceError(
                "ffmpeg is required to auto-fix this audio format/size/duration for "
                "Seedance 2.0; run `winget install Gyan.FFmpeg`, pass compliant "
                "wav/mp3 audio, or provide an HTTPS/signed URL",
                code=EXIT_USAGE,
                payload={
                    "path": str(path),
                    "reasons": reasons,
                    "install": "winget install Gyan.FFmpeg",
                    "alternatives": [
                        "pass compliant wav/mp3 audio within 2-15s and 15MB",
                        "provide an HTTPS/signed audio URL",
                    ],
                },
            )
        return _record("audio", str(path), "skipped", reason="ffmpeg_not_installed")

    output = prepare_dir / f"{path.stem}-prepared.mp3"
    command = [
        ffmpeg_path,
        "-y",
        "-i",
        str(path),
        "-vn",
    ]
    if trim_seconds is not None:
        command.extend(["-t", str(trim_seconds)])
    command.extend(["-acodec", "libmp3lame", "-b:a", AUDIO_PREPARE_BITRATE, str(output)])
    proc = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )
    if proc.returncode != 0 or not output.exists():
        if must_prepare:
            raise SeedanceError(
                "failed to prepare audio with ffmpeg",
                code=EXIT_USAGE,
                payload={"path": str(path), "ffmpeg": proc.stderr[-500:]},
            )
        return _record("audio", str(path), "skipped", reason="ffmpeg_failed")
    record = _prepared_record("audio", path, output)
    record["reasons"] = reasons
    if trim_seconds is not None:
        record["trim_seconds"] = trim_seconds
    return record


def _prepare_video(path: Path, prepare_dir: Path, must_prepare: bool, decision: dict) -> dict:
    if "video_too_short_unfixable" in decision["reasons"]:
        raise SeedanceError(
            "reference video is shorter than 2s and cannot be safely auto-fixed",
            code=EXIT_USAGE,
            payload={"path": str(path), "reasons": decision["reasons"]},
        )
    ffmpeg = os.environ.get("SEEDANCE_FFMPEG_BIN", "ffmpeg")
    ffmpeg_path = shutil.which(ffmpeg)
    if not ffmpeg_path:
        if must_prepare:
            raise SeedanceError(
                "ffmpeg is required to auto-fix this video duration/codec/FPS/dimensions "
                "for Seedance 2.0 before Cloudflare tunnel serving; run `winget install "
                "Gyan.FFmpeg`, pass a compliant mp4/mov video, or provide an "
                "HTTPS/signed URL",
                code=EXIT_USAGE,
                payload={
                    "path": str(path),
                    "reasons": decision["reasons"],
                    "install": "winget install Gyan.FFmpeg",
                    "alternatives": [
                        "pass compliant mp4/mov video within 2-15s, 24-60 FPS, and official pixel bounds",
                        "provide an HTTPS/signed video URL",
                        "use asset:// media",
                    ],
                },
            )
        return _record("video", str(path), "skipped", reason="ffmpeg_not_installed")
    meta = local_media_metadata(str(path), "video")
    output = prepare_dir / f"{path.stem}-prepared.mp4"
    command = [ffmpeg_path, "-y", "-i", str(path)]
    duration = meta.get("duration_seconds")
    if duration is not None and duration > MAX_REFERENCE_VIDEO_SECONDS:
        command.extend(["-t", str(MAX_REFERENCE_VIDEO_SECONDS)])
    width = meta.get("width")
    height = meta.get("height")
    target_dimensions = _video_target_dimensions(width, height)
    if target_dimensions:
        target_width, target_height = target_dimensions
        command.extend([
            "-vf",
            (
                f"scale={target_width}:{target_height}:force_original_aspect_ratio=decrease,"
                f"pad={target_width}:{target_height}:(ow-iw)/2:(oh-ih)/2"
            ),
        ])
    fps = meta.get("fps")
    if fps is not None and fps > MAX_REFERENCE_VIDEO_FPS:
        command.extend(["-r", str(MAX_REFERENCE_VIDEO_FPS)])
    elif fps is not None and fps < MIN_REFERENCE_VIDEO_FPS:
        command.extend(["-r", str(MIN_REFERENCE_VIDEO_FPS)])
    command.extend([
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        AUDIO_PREPARE_BITRATE,
        str(output),
    ])
    proc = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=False,
        timeout=300,
    )
    if proc.returncode != 0 or not output.exists():
        raise SeedanceError(
            "failed to auto-fix video with ffmpeg",
            code=EXIT_USAGE,
            payload={"path": str(path), "ffmpeg": proc.stderr[-500:]},
        )
    record = _prepared_record("video", path, output)
    record["reasons"] = decision["reasons"]
    return record


def _video_target_dimensions(width: object, height: object) -> tuple[int, int] | None:
    if width is None or height is None:
        return None
    target_width, target_height = _bounded_dimensions(int(width), int(height))
    pixels = target_width * target_height
    if pixels > MAX_REFERENCE_VIDEO_PIXELS:
        scale = math.sqrt(MAX_REFERENCE_VIDEO_PIXELS / pixels)
        target_width = int(target_width * scale)
        target_height = int(target_height * scale)
    if target_width * target_height < MIN_REFERENCE_VIDEO_PIXELS:
        scale = math.sqrt(MIN_REFERENCE_VIDEO_PIXELS / (target_width * target_height))
        target_width = int(math.ceil(target_width * scale))
        target_height = int(math.ceil(target_height * scale))
    target_width = max(2, target_width - target_width % 2)
    target_height = max(2, target_height - target_height % 2)
    return target_width, target_height


def _replace_arg_source(
    args: argparse.Namespace, attr: str, index: int | None, new_source: str
) -> None:
    if index is None:
        setattr(args, attr, new_source)
        return
    values = list(getattr(args, attr) or [])
    values[index] = new_source
    setattr(args, attr, values)


def _validate_base64_budget(args: argparse.Namespace) -> None:
    total_bytes = 0
    for _attr, _kind, _index, source in _local_media_sources(args):
        if _kind == "video":
            continue
        total_bytes += Path(source).expanduser().stat().st_size
    encoded_mb = total_bytes * 4 / 3 / 1024 / 1024
    if encoded_mb > MAX_REQUEST_BODY_MB:
        raise SeedanceError(
            "local image/audio Base64 payload would exceed the 64MB request body limit; "
            "use smaller prepared files, split inputs, or provide HTTPS/signed URLs",
            code=EXIT_USAGE,
            payload={
                "estimated_base64_mb": round(encoded_mb, 2),
                "limit_mb": MAX_REQUEST_BODY_MB,
            },
        )


def _prepared_record(kind: str, source: Path, output: Path) -> dict:
    return {
        "kind": kind,
        "status": "prepared",
        "source_path": str(source),
        "prepared_path": str(output),
        "source_size_bytes": source.stat().st_size,
        "prepared_size_bytes": output.stat().st_size,
    }


def _record(kind: str, source: str, status: str, *, reason: str) -> dict:
    return {
        "kind": kind,
        "status": status,
        "source_path": source,
        "reason": reason,
    }
