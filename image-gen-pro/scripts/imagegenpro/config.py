from __future__ import annotations

import json
import os
import urllib.parse
from pathlib import Path
from typing import Any

from .constants import GPT_IMAGE_2_MODEL, IMAGE_MODEL_ALIASES, ROUTE_CHOICES, ROUTE_PRESETS, ROUTES
from .errors import ConfigError


CONFIG_ENV = "IMAGE_GEN_PRO_CONFIG_DIR"


def config_dir() -> Path:
    override = os.environ.get(CONFIG_ENV)
    if override:
        return Path(override)
    appdata = os.environ.get("APPDATA")
    if appdata:
        return Path(appdata) / "image-gen-pro"
    return Path.home() / ".config" / "image-gen-pro"


def config_path() -> Path:
    return config_dir() / "config.json"


def default_config() -> dict[str, Any]:
    return {
        "default_provider": "placeholder",
        "default_model": GPT_IMAGE_2_MODEL,
        "output_dir": "outputs",
        "run_dir": "_work/image_gen_runs",
        "batch_dir": "_work/image_gen_batches",
        "default_route": "auto",
        "enabled_routes": ["codex-cli", "api-key"],
        "route_priority": ["codex-cli", "api-key"],
    }


def load_config() -> dict[str, Any]:
    path = config_path()
    data = default_config()
    if not path.exists():
        return data
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigError(f"invalid config JSON: {path}: {exc}") from exc
    if not isinstance(loaded, dict):
        raise ConfigError(f"config must be a JSON object: {path}")
    data.update(loaded)
    return normalize_config(data)


def save_config(data: dict[str, Any]) -> Path:
    path = config_path()
    data = normalize_config(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return path


def apply_route_preset(data: dict[str, Any], preset: str) -> dict[str, Any]:
    if preset not in ROUTE_PRESETS:
        raise ConfigError(f"route preset must be one of: {', '.join(ROUTE_PRESETS)}")
    updated = dict(data)
    updated.update(ROUTE_PRESETS[preset])
    return normalize_config(updated)


def normalize_config(data: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(data)
    default_model = str(normalized.get("default_model", GPT_IMAGE_2_MODEL)).strip().lower()
    if default_model not in IMAGE_MODEL_ALIASES:
        raise ConfigError(f"default_model must be one of: {', '.join(IMAGE_MODEL_ALIASES)}")
    normalized["default_model"] = IMAGE_MODEL_ALIASES[default_model]
    default_route = normalized.get("default_route", "auto")
    if default_route not in ROUTE_CHOICES:
        raise ConfigError(f"default_route must be one of: {', '.join(ROUTE_CHOICES)}")
    normalized["default_route"] = default_route
    enabled = _normalize_route_list(normalized.get("enabled_routes", list(ROUTES)), "enabled_routes")
    if not enabled:
        raise ConfigError("enabled_routes must contain at least one route")
    priority = _normalize_route_list(normalized.get("route_priority", enabled), "route_priority")
    for route in enabled:
        if route not in priority:
            priority.append(route)
    priority = [route for route in priority if route in enabled]
    normalized["enabled_routes"] = enabled
    normalized["route_priority"] = priority
    if default_route != "auto" and default_route not in enabled:
        raise ConfigError("default_route must be enabled, or use auto")
    if "api_key" in normalized and not str(normalized["api_key"]).strip():
        normalized.pop("api_key", None)
    if "base_url" in normalized and normalized["base_url"]:
        normalized["base_url"] = normalize_base_url(str(normalized["base_url"]))
    return normalized


def normalize_base_url(raw: str, *, label: str = "base_url", error_cls: type[Exception] = ConfigError) -> str:
    base = str(raw).strip().rstrip("/")
    if not base:
        raise error_cls(f"{label} must not be empty")
    if not base.startswith(("http://", "https://")):
        raise error_cls(f"{label} must start with http:// or https://")
    parsed = urllib.parse.urlsplit(base)
    if not parsed.scheme or not parsed.netloc:
        raise error_cls(f"{label} must include a host")
    path = parsed.path.rstrip("/")
    if path == "/v1":
        path = ""
    elif path.endswith("/v1"):
        path = path[:-3].rstrip("/")
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, path, "", ""))


def mask_secret(value: str | None) -> str | None:
    if not value:
        return value
    if len(value) <= 6:
        return "***"
    return f"{value[:4]}...{value[-2:]}"


def redact_config(data: dict[str, Any]) -> dict[str, Any]:
    redacted = dict(data)
    if redacted.get("api_key"):
        redacted["api_key"] = mask_secret(str(redacted["api_key"]))
    return redacted


def parse_route_list(raw: Any) -> list[str]:
    return _normalize_route_list(raw, "route list")


def _normalize_route_list(raw: Any, label: str) -> list[str]:
    if isinstance(raw, str):
        text = raw.strip()
        if text.startswith("["):
            try:
                raw = json.loads(text)
            except json.JSONDecodeError as exc:
                raise ConfigError(f"{label} must be a JSON array or comma-separated list") from exc
        else:
            raw = [part.strip() for part in text.split(",") if part.strip()]
    if not isinstance(raw, list):
        raise ConfigError(f"{label} must be a list")
    result = []
    for item in raw:
        if item not in ROUTES:
            raise ConfigError(f"{label} entries must be one of: {', '.join(ROUTES)}")
        if item not in result:
            result.append(item)
    return result


def parse_value(raw: str) -> Any:
    lowered = raw.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    try:
        return int(raw)
    except ValueError:
        return raw
