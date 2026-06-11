"""setup, doctor, and config subcommand handlers."""

from __future__ import annotations

import argparse
import importlib.util
import os
import shutil
import sys
import urllib.parse
from typing import Any

from seedance2.api import task_url
from seedance2.config import (
    config_dir,
    config_file_path,
    load_config_file,
    mask_secret,
    redact_config,
    save_config_file,
)
from seedance2.constants import (
    ALLOWED_MODELS,
    ALLOWED_RATIOS,
    ALLOWED_RESOLUTIONS,
    CONFIG_KEYS,
    AUTO_DURATION,
    CLI_NAME,
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
    DEFAULT_RATIO,
    EXIT_USAGE,
    GITHUB_API_BASE,
    GITHUB_REPO,
    MAX_DURATION,
    MIN_DURATION,
    SECRET_CONFIG_KEYS,
)
from seedance2.errors import SeedanceError
from seedance2.http import request_json
from seedance2.settings import Settings


def parse_bool(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"expected boolean, got {value!r}")


# ---------------------------------------------------------------------------
# setup
# ---------------------------------------------------------------------------


def cmd_setup(args: argparse.Namespace) -> dict:
    cfg = load_config_file() if not args.reset else {}
    if args.non_interactive:
        updates = _setup_non_interactive(args)
    else:
        updates = _setup_interactive(cfg)
    cfg.update(updates)
    cfg = {k: v for k, v in cfg.items() if v is not None}
    path = save_config_file(cfg)
    return {
        "ok": True,
        "config_path": str(path),
        "config": redact_config(cfg),
        "wrote_keys": sorted(updates.keys()),
        "reset": bool(args.reset),
    }


def _setup_non_interactive(args: argparse.Namespace) -> dict:
    pairs = [
        ("api_key", args.api_key),
        ("base_url", args.base_url),
        ("model", args.model),
        ("default_resolution", args.default_resolution),
        ("default_ratio", args.default_ratio),
        ("default_duration", args.default_duration),
        ("default_generate_audio", args.default_generate_audio),
        ("default_watermark", args.default_watermark),
    ]
    updates: dict = {}
    for key, value in pairs:
        if value is None:
            continue
        updates[key] = _coerce_config_value(key, value)
    if not updates and not args.reset:
        raise SeedanceError(
            "non-interactive setup requires at least one of "
            "--api-key/--base-url/--model/--default-*",
            code=EXIT_USAGE,
        )
    return updates


def _prompt(question: str, default: Any = None, *, secret: bool = False) -> str | None:
    if secret:
        suffix = " [keep current]" if default else ""
    else:
        suffix = f" [{default}]" if default not in (None, "") else ""
    sys.stderr.write(f"{question}{suffix}: ")
    sys.stderr.flush()
    try:
        line = input()
    except EOFError:
        return None if secret else default
    line = line.strip()
    if not line:
        return None if secret else default
    return line


def _setup_interactive(cfg: dict) -> dict:
    sys.stderr.write(
        f"{CLI_NAME} setup: leave a field blank to keep the current value.\n"
        f"config file: {config_file_path()}\n\n"
    )
    updates: dict = {}

    api_key = _prompt(
        "Volcengine Ark API key (ARK_API_KEY)", cfg.get("api_key"), secret=True
    )
    if api_key and api_key != cfg.get("api_key"):
        updates["api_key"] = api_key

    base_url = _prompt("Base URL", cfg.get("base_url") or DEFAULT_BASE_URL)
    if base_url and base_url != cfg.get("base_url"):
        updates["base_url"] = base_url

    model = _prompt(
        f"Default model ({'/'.join(ALLOWED_MODELS)})",
        cfg.get("model") or DEFAULT_MODEL,
    )
    if model and model not in ALLOWED_MODELS:
        raise SeedanceError(
            f"model must be one of {', '.join(ALLOWED_MODELS)}", code=EXIT_USAGE
        )
    if model and model != cfg.get("model"):
        updates["model"] = model

    resolution = _prompt(
        f"Default resolution ({'/'.join(ALLOWED_RESOLUTIONS)})",
        cfg.get("default_resolution") or "720p",
    )
    if resolution and resolution not in ALLOWED_RESOLUTIONS:
        raise SeedanceError(
            f"default_resolution must be one of {', '.join(ALLOWED_RESOLUTIONS)}",
            code=EXIT_USAGE,
        )
    if resolution and resolution != cfg.get("default_resolution"):
        updates["default_resolution"] = resolution

    ratio = _prompt(
        f"Default ratio ({'/'.join(ALLOWED_RATIOS)})",
        cfg.get("default_ratio") or DEFAULT_RATIO,
    )
    if ratio and ratio not in ALLOWED_RATIOS:
        raise SeedanceError(
            f"default_ratio must be one of {', '.join(ALLOWED_RATIOS)}",
            code=EXIT_USAGE,
        )
    if ratio and ratio != cfg.get("default_ratio"):
        updates["default_ratio"] = ratio

    duration_raw = _prompt(
        "Default duration in seconds", str(cfg.get("default_duration") or 5)
    )
    if duration_raw and str(duration_raw) != str(cfg.get("default_duration") or 5):
        updates["default_duration"] = _coerce_config_value(
            "default_duration", duration_raw
        )

    audio_raw = _prompt(
        "Default generate audio (true/false)",
        str(cfg.get("default_generate_audio", True)).lower(),
    )
    if audio_raw is not None and audio_raw != str(
        cfg.get("default_generate_audio", True)
    ).lower():
        try:
            updates["default_generate_audio"] = parse_bool(audio_raw)
        except argparse.ArgumentTypeError as exc:
            raise SeedanceError(str(exc), code=EXIT_USAGE)

    watermark_raw = _prompt(
        "Default watermark (true/false)",
        str(cfg.get("default_watermark", False)).lower(),
    )
    if watermark_raw is not None and watermark_raw != str(
        cfg.get("default_watermark", False)
    ).lower():
        try:
            updates["default_watermark"] = parse_bool(watermark_raw)
        except argparse.ArgumentTypeError as exc:
            raise SeedanceError(str(exc), code=EXIT_USAGE)

    return updates


# ---------------------------------------------------------------------------
# doctor
# ---------------------------------------------------------------------------


def cmd_doctor(args: argparse.Namespace) -> dict:
    settings = Settings(args)
    diagnostics: dict = {
        "ok": True,
        "config_path": str(config_file_path()),
        "config_exists": config_file_path().exists(),
        "config_sources": settings.config_sources,
        "effective": {
            "api_key": mask_secret(settings.api_key),
            "base_url": settings.base_url,
            "model": settings.model,
            "default_resolution": settings.default_resolution,
            "default_ratio": settings.default_ratio,
            "default_duration": settings.default_duration,
            "default_generate_audio": settings.default_generate_audio,
            "default_watermark": settings.default_watermark,
        },
        "checks": [],
    }
    api_key_ok = bool(settings.api_key)
    diagnostics["checks"].append({
        "name": "api_key",
        "ok": api_key_ok,
        "message": (
            "API key resolved" if api_key_ok
            else f"missing API key; run `{CLI_NAME} setup` or set ARK_API_KEY"
        ),
    })
    base_url_ok = settings.base_url.startswith(("http://", "https://"))
    diagnostics["checks"].append({
        "name": "base_url",
        "ok": base_url_ok,
        "message": (
            f"base_url={settings.base_url}" if base_url_ok
            else f"base_url is not http(s): {settings.base_url}"
        ),
    })
    model_ok = settings.model in ALLOWED_MODELS
    diagnostics["checks"].append({
        "name": "model",
        "ok": model_ok,
        "message": (
            f"model={settings.model}" if model_ok
            else f"model must be one of {', '.join(ALLOWED_MODELS)}"
        ),
    })
    diagnostics["checks"].extend(_check_optional_tools())
    if api_key_ok and base_url_ok and model_ok and not args.skip_connectivity:
        diagnostics["checks"].append(_probe_connectivity(settings))
    if not args.skip_update_check:
        diagnostics["checks"].append(_check_github_update())
    diagnostics["ok"] = all(c["ok"] for c in diagnostics["checks"])
    if not diagnostics["ok"]:
        diagnostics["hint"] = f"fix the failing checks above; rerun `{CLI_NAME} doctor`"
    return diagnostics


def _check_optional_tools() -> list[dict]:
    """Report local helper tools without making doctor fail when they are absent."""
    return [
        _python_module_tool_check(
            name="tool:pillow",
            module="PIL",
            install="python -m pip install pillow",
            required_when=(
                "local image format, size, dimensions, or aspect ratio must be "
                "auto-fixed before Base64 upload"
            ),
            missing_action=(
                "install Pillow, provide a compliant image, or use an HTTPS/signed URL"
            ),
        ),
        _binary_tool_check(
            name="tool:ffmpeg",
            env_var="SEEDANCE_FFMPEG_BIN",
            default_bin="ffmpeg",
            install="winget install Gyan.FFmpeg",
            required_when=(
                "local audio/video must be transcoded, trimmed, resized, or FPS-normalized"
            ),
            missing_action=(
                "install ffmpeg, provide compliant media, or use an HTTPS/signed URL"
            ),
        ),
        _binary_tool_check(
            name="tool:ffprobe",
            env_var="SEEDANCE_FFPROBE_BIN",
            default_bin="ffprobe",
            install="winget install Gyan.FFmpeg",
            required_when=(
                "local audio/video duration, codec, FPS, dimensions, or total duration "
                "should be validated before submission"
            ),
            missing_action=(
                "install ffprobe for deeper local validation; without it unavailable "
                "fields are recorded as manifest warnings"
            ),
        ),
        _binary_tool_check(
            name="tool:cloudflared",
            env_var="SEEDANCE_CLOUDFLARED_BIN",
            default_bin="cloudflared",
            install="winget install Cloudflare.cloudflared",
            required_when=(
                "local reference_video needs a temporary HTTPS URL via "
                "--serve-local-assets cloudflare"
            ),
            missing_action=(
                "install cloudflared, use an HTTPS/signed video URL, or use asset:// media"
            ),
        ),
    ]


def _python_module_tool_check(
    *,
    name: str,
    module: str,
    install: str,
    required_when: str,
    missing_action: str,
) -> dict:
    available = importlib.util.find_spec(module) is not None
    return {
        "name": name,
        "ok": True,
        "available": available,
        "message": (
            f"{module} available" if available
            else f"{module} not installed; {missing_action}"
        ),
        "required_when": required_when,
        "install": install,
        "missing_action": missing_action,
    }


def _binary_tool_check(
    *,
    name: str,
    env_var: str,
    default_bin: str,
    install: str,
    required_when: str,
    missing_action: str,
) -> dict:
    configured = os.environ.get(env_var, default_bin)
    path = shutil.which(configured)
    return {
        "name": name,
        "ok": True,
        "available": bool(path),
        "path": path,
        "env": env_var,
        "configured": configured,
        "message": (
            f"{configured} available" if path
            else f"{configured} not found; {missing_action}"
        ),
        "required_when": required_when,
        "install": install,
        "missing_action": missing_action,
    }


def _probe_connectivity(settings: Settings) -> dict:
    url = (
        task_url(settings)
        + "?"
        + urllib.parse.urlencode({"page_num": "1", "page_size": "1"})
    )
    try:
        request_json("GET", url, settings.api_key, timeout=20)
        return {"name": "connectivity", "ok": True, "message": "GET tasks?page_size=1 succeeded"}
    except SeedanceError as exc:
        return {
            "name": "connectivity",
            "ok": False,
            "message": exc.message,
            "details": exc.payload,
        }


def _check_github_update() -> dict:
    """Query GitHub Releases API for the latest version and compare with SCRIPT_VERSION."""
    import json
    import os
    import urllib.error
    import urllib.request

    from seedance2 import SCRIPT_VERSION

    repo = os.environ.get("VIDEO_GEN_PRO_GITHUB_REPO", GITHUB_REPO)
    api_base = os.environ.get("VIDEO_GEN_PRO_GITHUB_API", GITHUB_API_BASE).rstrip("/")
    url = f"{api_base}/repos/{repo}/releases/latest"

    try:
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": f"{CLI_NAME}/{SCRIPT_VERSION}",
            },
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode("utf-8"))
        latest = data.get("tag_name", "").lstrip("v")
        if latest and latest != SCRIPT_VERSION:
            return {
                "name": "update",
                "ok": False,
                "message": (
                    f"update available: {SCRIPT_VERSION} → {latest}; "
                    f"run the install script or: git pull && python scripts/video_gen_pro.py"
                ),
                "current_version": SCRIPT_VERSION,
                "latest_version": latest,
                "release_url": data.get("html_url", ""),
            }
        return {
            "name": "update",
            "ok": True,
            "message": f"up to date (v{SCRIPT_VERSION})",
        }
    except Exception as exc:
        return {
            "name": "update",
            "ok": True,
            "message": f"update check skipped ({exc})",
        }


# ---------------------------------------------------------------------------
# config subcommands
# ---------------------------------------------------------------------------


def cmd_config_path(args: argparse.Namespace) -> dict:
    return {
        "ok": True,
        "config_dir": str(config_dir()),
        "config_path": str(config_file_path()),
        "exists": config_file_path().exists(),
        "config_dir_env": "VIDEO_GEN_PRO_CONFIG_DIR",
    }


def cmd_config_list(args: argparse.Namespace) -> dict:
    cfg = load_config_file()
    return {
        "ok": True,
        "config_path": str(config_file_path()),
        "exists": config_file_path().exists(),
        "config": redact_config(cfg),
    }


def cmd_config_get(args: argparse.Namespace) -> dict:
    cfg = load_config_file()
    if args.key not in CONFIG_KEYS:
        raise SeedanceError(
            f"unknown config key: {args.key}; allowed: {', '.join(CONFIG_KEYS)}",
            code=EXIT_USAGE,
        )
    value = cfg.get(args.key)
    if args.key in SECRET_CONFIG_KEYS:
        value = mask_secret(value)
    return {"ok": True, "key": args.key, "value": value}


def cmd_config_set(args: argparse.Namespace) -> dict:
    if args.key not in CONFIG_KEYS:
        raise SeedanceError(
            f"unknown config key: {args.key}; allowed: {', '.join(CONFIG_KEYS)}",
            code=EXIT_USAGE,
        )
    cfg = load_config_file()
    value = _coerce_config_value(args.key, args.value)
    cfg[args.key] = value
    path = save_config_file(cfg)
    return {
        "ok": True,
        "config_path": str(path),
        "key": args.key,
        "value": (
            mask_secret(value) if args.key in SECRET_CONFIG_KEYS else value
        ),
    }


def cmd_config_unset(args: argparse.Namespace) -> dict:
    if args.key not in CONFIG_KEYS:
        raise SeedanceError(
            f"unknown config key: {args.key}; allowed: {', '.join(CONFIG_KEYS)}",
            code=EXIT_USAGE,
        )
    cfg = load_config_file()
    removed = args.key in cfg
    if removed:
        cfg.pop(args.key)
        save_config_file(cfg)
    return {
        "ok": True,
        "config_path": str(config_file_path()),
        "removed": args.key,
        "existed": removed,
    }


def _coerce_config_value(key: str, value: object) -> object:
    if key == "model":
        if value not in ALLOWED_MODELS:
            raise SeedanceError(
                f"model must be one of {', '.join(ALLOWED_MODELS)}",
                code=EXIT_USAGE,
            )
        return value
    if key == "default_resolution":
        if value not in ALLOWED_RESOLUTIONS:
            raise SeedanceError(
                f"default_resolution must be one of {', '.join(ALLOWED_RESOLUTIONS)}",
                code=EXIT_USAGE,
            )
        return value
    if key == "default_ratio":
        if value not in ALLOWED_RATIOS:
            raise SeedanceError(
                f"default_ratio must be one of {', '.join(ALLOWED_RATIOS)}",
                code=EXIT_USAGE,
            )
        return value
    if key == "default_duration":
        try:
            duration = int(value)
        except (TypeError, ValueError):
            raise SeedanceError("default_duration must be an integer", code=EXIT_USAGE)
        if duration != AUTO_DURATION and not (MIN_DURATION <= duration <= MAX_DURATION):
            raise SeedanceError(
                f"default_duration must be {AUTO_DURATION} or "
                f"{MIN_DURATION}-{MAX_DURATION} seconds",
                code=EXIT_USAGE,
            )
        return duration
    if key in {"default_generate_audio", "default_watermark"}:
        try:
            return parse_bool(value)
        except argparse.ArgumentTypeError as exc:
            raise SeedanceError(str(exc), code=EXIT_USAGE)
    return value
