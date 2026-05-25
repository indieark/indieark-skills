"""Task payload builder and lifecycle functions (submit, wait, download)."""

from __future__ import annotations

import argparse
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Iterable

from seedance2.constants import (
    ALLOWED_MODELS,
    AUTO_DURATION,
    EXIT_API,
    EXIT_CONFIG,
    EXIT_RUNTIME,
    EXIT_USAGE,
    FAST_MODEL,
    MAX_DURATION,
    MAX_REFERENCE_AUDIOS,
    MAX_REFERENCE_IMAGES,
    MAX_REFERENCE_VIDEOS,
    MAX_EXECUTION_EXPIRES_AFTER,
    MAX_SEED,
    MAX_SAFETY_IDENTIFIER_LENGTH,
    MIN_EXECUTION_EXPIRES_AFTER,
    MIN_DURATION,
    MIN_SEED,
)
from seedance2.errors import SeedanceError
from seedance2.http import content_item, probe_media_url, request_json
from seedance2.settings import Settings


def build_create_payload(
    settings: Settings,
    args: argparse.Namespace,
    *,
    mode: str,
    first_frame: str | None = None,
    last_frame: str | None = None,
    reference_images: Iterable[str] = (),
    reference_videos: Iterable[str] = (),
    reference_audios: Iterable[str] = (),
    web_search: bool = False,
) -> dict:
    model = args.model or settings.model
    resolution = args.resolution or settings.default_resolution
    ratio = args.ratio or settings.default_ratio
    duration = args.duration if args.duration is not None else settings.default_duration
    generate_audio = (
        args.generate_audio
        if args.generate_audio is not None
        else settings.default_generate_audio
    )
    watermark = (
        args.watermark
        if args.watermark is not None
        else settings.default_watermark
    )

    if model not in ALLOWED_MODELS:
        raise SeedanceError(
            f"only Seedance 2.0 models are allowed: {', '.join(ALLOWED_MODELS)}",
            code=EXIT_USAGE,
        )
    if model == FAST_MODEL and resolution == "1080p":
        raise SeedanceError(
            "doubao-seedance-2-0-fast-260128 does not support 1080p; "
            "use 480p/720p or switch to doubao-seedance-2-0-260128",
            code=EXIT_USAGE,
        )
    if duration != AUTO_DURATION and not (MIN_DURATION <= duration <= MAX_DURATION):
        raise SeedanceError(
            f"duration must be {AUTO_DURATION} or {MIN_DURATION}-{MAX_DURATION} seconds",
            code=EXIT_USAGE,
        )
    if args.seed is not None and not (MIN_SEED <= args.seed <= MAX_SEED):
        raise SeedanceError(
            f"seed must be between {MIN_SEED} and {MAX_SEED}",
            code=EXIT_USAGE,
        )
    if args.callback_url and not args.callback_url.startswith(("http://", "https://")):
        raise SeedanceError(
            "callback_url must be an HTTP(S) URL",
            code=EXIT_USAGE,
        )
    if args.execution_expires_after is not None and not (
        MIN_EXECUTION_EXPIRES_AFTER
        <= args.execution_expires_after
        <= MAX_EXECUTION_EXPIRES_AFTER
    ):
        raise SeedanceError(
            "execution_expires_after must be between "
            f"{MIN_EXECUTION_EXPIRES_AFTER} and {MAX_EXECUTION_EXPIRES_AFTER} seconds",
            code=EXIT_USAGE,
        )
    if args.service_tier == "flex":
        raise SeedanceError(
            "Seedance 2.0 does not support flex/offline service_tier; use default",
            code=EXIT_USAGE,
        )
    if (
        args.safety_identifier
        and len(args.safety_identifier) > MAX_SAFETY_IDENTIFIER_LENGTH
    ):
        raise SeedanceError(
            f"safety_identifier must be at most {MAX_SAFETY_IDENTIFIER_LENGTH} chars",
            code=EXIT_USAGE,
        )
    reference_images = list(reference_images or [])
    reference_videos = list(reference_videos or [])
    reference_audios = list(reference_audios or [])
    if len(reference_images) > MAX_REFERENCE_IMAGES:
        raise SeedanceError(
            f"reference images are limited to {MAX_REFERENCE_IMAGES}",
            code=EXIT_USAGE,
        )
    if len(reference_videos) > MAX_REFERENCE_VIDEOS:
        raise SeedanceError(
            f"reference videos are limited to {MAX_REFERENCE_VIDEOS}",
            code=EXIT_USAGE,
        )
    if len(reference_audios) > MAX_REFERENCE_AUDIOS:
        raise SeedanceError(
            f"reference audios are limited to {MAX_REFERENCE_AUDIOS}",
            code=EXIT_USAGE,
        )
    has_reference = bool(reference_images or reference_videos or reference_audios)
    has_frame = bool(first_frame or last_frame)

    if mode in ("first-frame", "first-last") and has_reference:
        raise SeedanceError(
            "first/last-frame mode cannot be mixed with "
            "reference_image/reference_video/reference_audio",
            code=EXIT_CONFIG,
        )
    if mode == "omni" and reference_audios and not (reference_images or reference_videos):
        raise SeedanceError(
            "reference audio cannot be used alone; "
            "add at least one reference image or video",
            code=EXIT_CONFIG,
        )
    if web_search and (has_frame or has_reference):
        raise SeedanceError(
            "--web-search is only valid for pure text-to-video",
            code=EXIT_CONFIG,
        )
    if not (args.prompt or first_frame or reference_images or reference_videos):
        raise SeedanceError(
            "provide --prompt, --first-frame, --reference-image, or --reference-video",
            code=EXIT_USAGE,
        )

    content: list[dict] = []
    if args.prompt:
        content.append(content_item("text", args.prompt))
    if first_frame:
        content.append(content_item("image", first_frame, "first_frame"))
    if last_frame:
        content.append(content_item("image", last_frame, "last_frame"))
    for source in reference_images:
        content.append(content_item("image", source, "reference_image"))
    for source in reference_videos:
        content.append(content_item("video", source, "reference_video"))
    for source in reference_audios:
        content.append(content_item("audio", source, "reference_audio"))

    payload: dict = {
        "model": model,
        "content": content,
        "resolution": resolution,
        "ratio": ratio,
        "duration": duration,
        "generate_audio": generate_audio,
        "watermark": watermark,
    }
    if args.seed is not None:
        payload["seed"] = args.seed
    if args.return_last_frame:
        payload["return_last_frame"] = True
    if args.callback_url:
        payload["callback_url"] = args.callback_url
    if args.execution_expires_after is not None:
        payload["execution_expires_after"] = args.execution_expires_after
    if args.service_tier:
        payload["service_tier"] = args.service_tier
    if args.safety_identifier:
        payload["safety_identifier"] = args.safety_identifier
    if web_search:
        payload["tools"] = [{"type": "web_search"}]
    return payload


def task_url(settings: Settings, task_id: str | None = None) -> str:
    url = f"{settings.base_url}/contents/generations/tasks"
    return f"{url}/{task_id}" if task_id else url


def extract_video_url(result: dict) -> str:
    content = result.get("content")
    if isinstance(content, dict):
        return content.get("video_url") or ""
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict):
                video_url = item.get("video_url")
                if isinstance(video_url, dict) and video_url.get("url"):
                    return video_url["url"]
                if isinstance(video_url, str):
                    return video_url
    output = result.get("output")
    if isinstance(output, dict):
        return output.get("video_url") or ""
    return ""


def submit_task(
    settings: Settings, args: argparse.Namespace, payload: dict, mode: str
) -> dict:
    api_key = settings.require_api_key()
    result = request_json("POST", task_url(settings), api_key, payload=payload)
    task_id = result.get("id") or result.get("task_id")
    if not task_id:
        raise SeedanceError(
            "task id missing in API response",
            code=EXIT_API,
            payload={"response": result},
        )
    return {
        "ok": True,
        "task_id": task_id,
        "status": result.get("status", "created"),
        "mode": mode,
        "model": payload["model"],
        "response": result,
    }


def validate_payload_media_urls(payload: dict) -> list[dict]:
    checks: list[dict] = []
    for item in payload.get("content", []):
        if not isinstance(item, dict):
            continue
        for field, kind in (
            ("image_url", "image"),
            ("video_url", "video"),
            ("audio_url", "audio"),
        ):
            value = item.get(field)
            if isinstance(value, dict) and isinstance(value.get("url"), str):
                checks.append(probe_media_url(value["url"], kind))
    return checks


def wait_for_task(
    settings: Settings, task_id: str, *, interval: int, timeout: int
) -> dict:
    api_key = settings.require_api_key()
    start = time.time()
    while True:
        result = request_json("GET", task_url(settings, task_id), api_key)
        status = result.get("status", "unknown")
        elapsed = int(time.time() - start)
        if status == "succeeded":
            return {
                "ok": True,
                "task_id": task_id,
                "status": status,
                "video_url": extract_video_url(result),
                "elapsed_seconds": elapsed,
                "response": result,
            }
        if status in {"failed", "expired", "cancelled"}:
            raise SeedanceError(
                f"task ended with status: {status}",
                code=EXIT_RUNTIME,
                payload={"task_id": task_id, "status": status, "response": result},
            )
        if elapsed >= timeout:
            raise SeedanceError(
                f"timeout after {timeout}s",
                code=EXIT_RUNTIME,
                payload={
                    "task_id": task_id,
                    "status": status,
                    "elapsed_seconds": elapsed,
                    "resume_command": f"seedance2 wait {task_id}",
                },
            )
        sys.stderr.write(f"[{elapsed}s] {status}\n")
        sys.stderr.flush()
        time.sleep(interval)


def download_video(url: str, output_dir: str, task_id: str) -> Path:
    path = Path(output_dir).expanduser()
    path.mkdir(parents=True, exist_ok=True)
    output = path / f"seedance2_{task_id}_{int(time.time())}.mp4"
    try:
        with urllib.request.urlopen(url, timeout=300) as response:
            output.write_bytes(response.read())
    except (urllib.error.URLError, OSError) as exc:
        raise SeedanceError(
            f"failed to download video: {exc}",
            code=EXIT_RUNTIME,
            payload={"url": url},
        )
    return output
