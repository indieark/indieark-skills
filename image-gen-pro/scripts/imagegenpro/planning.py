from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from .constants import ALLOWED_PROVIDERS, NEUTRAL_REQUEST_SCHEMA
from .errors import UsageError


def validate_provider(provider: str) -> str:
    if provider not in ALLOWED_PROVIDERS:
        allowed = ", ".join(ALLOWED_PROVIDERS)
        raise UsageError(f"provider must be one of: {allowed}")
    return provider


def resolve_prompt(prompt: str | None = None, prompt_file: str | None = None) -> str:
    if prompt and prompt_file:
        raise UsageError("use either --prompt or --prompt-file, not both")
    if prompt_file:
        path = Path(prompt_file)
        if not path.exists() or not path.is_file():
            raise UsageError(f"prompt file does not exist or is not a file: {prompt_file}")
        prompt = path.read_text(encoding="utf-8").strip()
    if prompt is None or not prompt.strip():
        raise UsageError("prompt must not be empty")
    return prompt.strip()


def build_neutral_request(prompt: str, provider: str, reference: list[str] | None = None) -> dict[str, Any]:
    references = reference or []
    provider = validate_provider(provider)
    return {
        "schema": NEUTRAL_REQUEST_SCHEMA,
        "provider": provider,
        "prompt": prompt,
        "references": [normalize_reference(item) for item in references],
        "execution": {
            "mode": "dry-run-only",
            "provider_api_call": False,
        },
        "next_steps": [
            "Select a concrete provider before adding API-specific fields.",
            "Implement provider-specific request mapping outside the core neutral schema.",
            "Keep submitted provider payloads and responses redacted in artifacts.",
        ],
    }


def summarize_request(request: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": request["schema"],
        "provider": request["provider"],
        "prompt_chars": len(request["prompt"]),
        "reference_count": len(request["references"]),
        "provider_api_call": False,
        "next_steps": request["next_steps"],
    }


def normalize_reference(raw: str) -> dict[str, Any]:
    if not raw or not raw.strip():
        raise UsageError("reference must not be empty")
    raw = raw.strip()
    if _is_url(raw):
        return {
            "source_type": "url",
            "value": _redact_url(raw),
            "exists": None,
            "sha256": None,
            "size_bytes": None,
        }

    path = Path(raw)
    if not path.exists() or not path.is_file():
        raise UsageError(f"reference file does not exist or is not a file: {raw}")
    return {
        "source_type": "local_file",
        "path": str(path),
        "exists": True,
        "sha256": _sha256_file(path),
        "size_bytes": path.stat().st_size,
    }


def _is_url(value: str) -> bool:
    parts = urlsplit(value)
    return parts.scheme in {"http", "https"} and bool(parts.netloc)


def _redact_url(value: str) -> str:
    parts = urlsplit(value)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
