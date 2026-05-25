"""Layered settings resolver: CLI args > env > config file > builtin defaults."""

from __future__ import annotations

import argparse
import os

from seedance2.config import load_config_file
from seedance2.constants import (
    ALLOWED_RATIOS,
    ALLOWED_RESOLUTIONS,
    AUTO_DURATION,
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
    DEFAULT_RATIO,
    EXIT_CONFIG,
    MAX_DURATION,
    MIN_DURATION,
)
from seedance2.errors import SeedanceError


class Settings:
    """Resolve effective settings and remember each value's origin."""

    def __init__(self, args: argparse.Namespace | None = None) -> None:
        cfg = load_config_file()
        self.config = cfg
        self.config_sources: dict[str, str] = {}
        self.api_key = self._resolve(
            args, "api_key", "ARK_API_KEY", cfg, alt_envs=("SEEDANCE_API_KEY",)
        )
        base_url = self._resolve(
            args, "base_url", "SEEDANCE_BASE_URL", cfg, default=DEFAULT_BASE_URL
        )
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.model = (
            self._resolve(args, "model", "SEEDANCE_MODEL", cfg, default=DEFAULT_MODEL)
            or DEFAULT_MODEL
        )
        self.default_resolution = _coerce_choice(
            cfg.get("default_resolution", "720p"),
            "default_resolution",
            ALLOWED_RESOLUTIONS,
        )
        self.default_ratio = _coerce_choice(
            cfg.get("default_ratio", DEFAULT_RATIO), "default_ratio", ALLOWED_RATIOS
        )
        self.default_duration = _coerce_duration(cfg.get("default_duration", 5))
        self.default_generate_audio = _coerce_bool(
            cfg.get("default_generate_audio", True), "default_generate_audio"
        )
        self.default_watermark = _coerce_bool(
            cfg.get("default_watermark", False), "default_watermark"
        )

    def _resolve(
        self,
        args: argparse.Namespace | None,
        attr: str,
        env_name: str,
        cfg: dict,
        *,
        default: str | None = None,
        alt_envs: tuple[str, ...] = (),
    ) -> str | None:
        if args is not None:
            cli_value = getattr(args, attr, None)
            if cli_value:
                self.config_sources[attr] = "cli"
                return cli_value
        env_value = os.environ.get(env_name)
        if env_value:
            self.config_sources[attr] = f"env:{env_name}"
            return env_value
        for alt in alt_envs:
            alt_value = os.environ.get(alt)
            if alt_value:
                self.config_sources[attr] = f"env:{alt}"
                return alt_value
        if cfg.get(attr):
            self.config_sources[attr] = "config_file"
            return cfg[attr]
        if default is not None:
            self.config_sources[attr] = "default"
            return default
        self.config_sources[attr] = "missing"
        return None

    def require_api_key(self) -> str:
        if not self.api_key:
            raise SeedanceError(
                "API key not configured; run `seedance2 setup`, "
                "set ARK_API_KEY, or pass --api-key",
                code=EXIT_CONFIG,
            )
        return self.api_key


def _coerce_bool(value: object, key: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "y", "on"}:
            return True
        if normalized in {"0", "false", "no", "n", "off"}:
            return False
    raise SeedanceError(
        f"config value `{key}` must be boolean true/false",
        code=EXIT_CONFIG,
    )


def _coerce_choice(value: object, key: str, choices: tuple[str, ...]) -> str:
    text = str(value)
    if text in choices:
        return text
    raise SeedanceError(
        f"config value `{key}` must be one of {', '.join(choices)}",
        code=EXIT_CONFIG,
    )


def _coerce_duration(value: object) -> int:
    try:
        duration = int(value)
    except (TypeError, ValueError):
        raise SeedanceError(
            "config value `default_duration` must be an integer",
            code=EXIT_CONFIG,
        )
    if duration == AUTO_DURATION or MIN_DURATION <= duration <= MAX_DURATION:
        return duration
    raise SeedanceError(
        f"config value `default_duration` must be {AUTO_DURATION} or "
        f"{MIN_DURATION}-{MAX_DURATION} seconds",
        code=EXIT_CONFIG,
    )
