"""Run artifact capture for create commands."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from seedance2.constants import DEFAULT_RUN_ROOT
from seedance2.http import is_http_url
from seedance2.media_probe import local_media_metadata


def create_run_artifacts(
    args: argparse.Namespace,
    *,
    mode: str,
    payload: dict,
) -> dict:
    run_dir = resolve_run_dir(args)
    run_dir.mkdir(parents=True, exist_ok=True)

    prompt_path = None
    prompt_sha256 = None
    if getattr(args, "prompt", None):
        prompt_path = run_dir / "prompt.txt"
        prompt_path.write_text(args.prompt + "\n", encoding="utf-8")
        prompt_sha256 = hashlib.sha256(args.prompt.encode("utf-8")).hexdigest()

    redacted_payload = redact_payload(payload)
    payload_path = run_dir / "request-payload-redacted.json"
    _write_json(payload_path, redacted_payload)

    manifest = build_media_manifest(args, payload, mode=mode)
    manifest["prompt"] = {
        "path": str(prompt_path) if prompt_path else None,
        "sha256": prompt_sha256,
    }
    manifest["reference_index"] = build_reference_index(args)
    manifest["prompt_reference_warnings"] = prompt_reference_warnings(
        getattr(args, "prompt", None), manifest["reference_index"]
    )
    manifest["preparation"] = getattr(args, "media_preparation", [])
    manifest["validation"] = getattr(args, "media_validation", [])
    manifest["project_context"] = getattr(args, "project_context", None)
    manifest_path = run_dir / "media-manifest.json"
    _write_json(manifest_path, manifest)
    generation_log_path = run_dir / "generation-log.json"

    return {
        "run_dir": str(run_dir),
        "payload_path": str(payload_path),
        "manifest_path": str(manifest_path),
        "generation_log_path": str(generation_log_path),
        "payload_redacted": redacted_payload,
        "manifest": manifest,
    }


def update_media_manifest(artifacts: dict, url_checks: list[dict]) -> None:
    manifest = dict(artifacts["manifest"])
    manifest["url_checks"] = url_checks
    artifacts["manifest"] = manifest
    _write_json(Path(artifacts["manifest_path"]), manifest)


def write_submit_summary(artifacts: dict, submission: dict) -> None:
    summary = {
        "ok": submission.get("ok"),
        "task_id": submission.get("task_id"),
        "status": submission.get("status"),
        "mode": submission.get("mode"),
        "model": submission.get("model"),
    }
    _write_json(Path(artifacts["run_dir"]) / "submit-summary.json", summary)


def write_task_result(artifacts: dict, result: dict) -> None:
    _write_json(Path(artifacts["run_dir"]) / "task-result.json", result)


def write_generation_log(
    artifacts: dict,
    *,
    stage: str,
    submission: dict | None = None,
    result: dict | None = None,
) -> None:
    manifest = artifacts.get("manifest", {})
    payload = artifacts.get("payload_redacted", {})
    log = {
        "schema_version": 1,
        "stage": stage,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "run_dir": artifacts["run_dir"],
        "artifacts": {
            "prompt_path": manifest.get("prompt", {}).get("path"),
            "payload_path": artifacts.get("payload_path"),
            "manifest_path": artifacts.get("manifest_path"),
            "generation_log_path": artifacts.get("generation_log_path"),
            "submit_summary_path": str(Path(artifacts["run_dir"]) / "submit-summary.json"),
            "task_result_path": str(Path(artifacts["run_dir"]) / "task-result.json"),
        },
        "request": _request_summary(payload),
        "prompt": manifest.get("prompt", {}),
        "project_context": manifest.get("project_context"),
        "references": manifest.get("reference_index", []),
        "prompt_reference_warnings": manifest.get("prompt_reference_warnings", []),
        "media": {
            "items": manifest.get("items", []),
            "preparation": manifest.get("preparation", []),
            "validation": manifest.get("validation", []),
            "url_checks": manifest.get("url_checks", []),
            "asset_server": manifest.get("asset_server"),
        },
        "submission": submission,
        "result": result,
    }
    _write_json(Path(artifacts["generation_log_path"]), log)


def redact_payload(payload: dict) -> dict:
    redacted = copy.deepcopy(payload)
    for item in redacted.get("content", []):
        if not isinstance(item, dict):
            continue
        for key in ("image_url", "video_url", "audio_url"):
            value = item.get(key)
            if isinstance(value, dict) and isinstance(value.get("url"), str):
                value["url"] = redact_media_url(value["url"])
    return redacted


def redact_media_url(url: str) -> str:
    if url.startswith("data:"):
        mime = url[5:].split(";", 1)[0] or "application/octet-stream"
        return f"data:{mime};base64,<redacted>"
    if is_http_url(url):
        parts = urlsplit(url)
        path = parts.path
        return urlunsplit((parts.scheme, parts.netloc, path, "", ""))
    return "<redacted>"


def _request_summary(payload: dict) -> dict:
    keys = [
        "model",
        "resolution",
        "ratio",
        "duration",
        "generate_audio",
        "watermark",
        "seed",
        "return_last_frame",
        "service_tier",
        "execution_expires_after",
        "callback_url",
    ]
    summary = {key: payload.get(key) for key in keys if key in payload}
    if "safety_identifier" in payload:
        summary["safety_identifier"] = "<present>"
    content = payload.get("content", [])
    summary["content_counts"] = {
        "text": sum(1 for item in content if item.get("type") == "text"),
        "image_url": sum(1 for item in content if item.get("type") == "image_url"),
        "video_url": sum(1 for item in content if item.get("type") == "video_url"),
        "audio_url": sum(1 for item in content if item.get("type") == "audio_url"),
    }
    if payload.get("tools"):
        summary["tools"] = payload["tools"]
    return summary


def build_media_manifest(
    args: argparse.Namespace, payload: dict, *, mode: str
) -> dict:
    sources = _source_entries(args, mode)
    payload_urls = _payload_media_urls(payload)
    items = []
    for index, source in enumerate(sources):
        item = dict(source)
        item["index"] = index
        if index < len(payload_urls):
            item["payload_url"] = redact_media_url(payload_urls[index])
        item.update(local_media_metadata(source["source"], source.get("kind")))
        items.append(item)
    return {
        "mode": mode,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "items": items,
    }


def build_reference_index(args: argparse.Namespace) -> list[dict]:
    entries: list[dict] = []
    counters = {
        "reference_image": 0,
        "reference_video": 0,
        "reference_audio": 0,
        "first_frame": 0,
        "last_frame": 0,
    }
    for source in _source_entries(args, mode=""):
        role = source["role"]
        counters[role] += 1
        entries.append({
            "label": _reference_label(role, counters[role]),
            "role": role,
            "kind": source["kind"],
            "source": source["source"],
        })
    return entries


def prompt_reference_warnings(prompt: str | None, reference_index: list[dict]) -> list[str]:
    if not prompt or not reference_index:
        return []
    warnings: list[str] = []
    for item in reference_index:
        label = item["label"]
        aliases = _label_aliases(label, item["role"])
        if not any(alias in prompt for alias in aliases):
            warnings.append(
                f"prompt does not mention {label}; describe how this {item['role']} should be used"
            )
    return warnings


def _reference_label(role: str, index: int) -> str:
    if role == "reference_image":
        return f"参考图{index}"
    if role == "reference_video":
        return f"参考视频{index}"
    if role == "reference_audio":
        return f"参考音频{index}"
    if role == "first_frame":
        return "首帧图片"
    if role == "last_frame":
        return "尾帧图片"
    return f"{role}{index}"


def _label_aliases(label: str, role: str) -> list[str]:
    aliases = [label]
    if role == "reference_image":
        aliases.append(label.replace("参考图", "图片"))
    if role == "reference_video":
        aliases.append(label.replace("参考视频", "视频"))
    if role == "reference_audio":
        aliases.append(label.replace("参考音频", "音频"))
    return aliases


def _source_entries(args: argparse.Namespace, mode: str) -> list[dict]:
    entries: list[dict] = []
    if getattr(args, "first_frame", None):
        entries.append({"role": "first_frame", "kind": "image", "source": args.first_frame})
    if getattr(args, "last_frame", None):
        entries.append({"role": "last_frame", "kind": "image", "source": args.last_frame})
    for source in getattr(args, "reference_image", None) or []:
        entries.append({"role": "reference_image", "kind": "image", "source": source})
    for source in getattr(args, "reference_video", None) or []:
        entries.append({"role": "reference_video", "kind": "video", "source": source})
    for source in getattr(args, "reference_audio", None) or []:
        entries.append({"role": "reference_audio", "kind": "audio", "source": source})
    return entries


def _payload_media_urls(payload: dict) -> list[str]:
    urls: list[str] = []
    for item in payload.get("content", []):
        if not isinstance(item, dict):
            continue
        for key in ("image_url", "video_url", "audio_url"):
            value = item.get(key)
            if isinstance(value, dict) and isinstance(value.get("url"), str):
                urls.append(value["url"])
    return urls


def resolve_run_dir(args: argparse.Namespace) -> Path:
    ensure_run_id(args)
    base = Path(getattr(args, "run_dir", None) or DEFAULT_RUN_ROOT).expanduser()
    return base / args.run_id


def ensure_run_id(args: argparse.Namespace) -> str:
    if not getattr(args, "run_id", None):
        args.run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    return args.run_id


def _write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
