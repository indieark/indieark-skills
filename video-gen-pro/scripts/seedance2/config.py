"""Config file management (XDG / AppData style) and secret masking."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from seedance2.constants import APP_NAME, CONFIG_FILENAME, EXIT_CONFIG, SECRET_CONFIG_KEYS
from seedance2.errors import SeedanceError


def config_dir() -> Path:
    override = os.environ.get("VIDEO_GEN_PRO_CONFIG_DIR")
    if override:
        return Path(override).expanduser()
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / APP_NAME
        return Path.home() / "AppData" / "Roaming" / APP_NAME
    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg) / APP_NAME
    return Path.home() / ".config" / APP_NAME


def config_file_path() -> Path:
    return config_dir() / CONFIG_FILENAME


def load_config_file() -> dict:
    path = config_file_path()
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SeedanceError(
            f"config file is not valid JSON: {path} ({exc})",
            code=EXIT_CONFIG,
        )
    except OSError as exc:
        raise SeedanceError(
            f"failed to read config file: {path} ({exc})",
            code=EXIT_CONFIG,
        )


def save_config_file(data: dict) -> Path:
    path = config_file_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2)
    path.write_text(text + "\n", encoding="utf-8")
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return path


def mask_secret(value: str | None) -> str | None:
    if not value:
        return value
    if len(value) <= 6:
        return "***"
    return f"{value[:4]}...{value[-2:]}"


def redact_config(data: dict) -> dict:
    redacted = dict(data)
    for key in SECRET_CONFIG_KEYS:
        if key in redacted and redacted[key]:
            redacted[key] = mask_secret(redacted[key])
    return redacted
