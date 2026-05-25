"""SeedanceError exception and stdout/stderr output helpers."""

from __future__ import annotations

import json
import sys
from typing import Any

from seedance2.constants import EXIT_RUNTIME


class SeedanceError(Exception):
    def __init__(
        self, message: str, code: int = EXIT_RUNTIME, payload: dict | None = None
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.payload = payload or {}


def emit(payload: Any, fmt: str = "json") -> None:
    if fmt == "markdown":
        sys.stdout.write(_render_markdown(payload))
        sys.stdout.write("\n")
        return
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.stdout.write("\n")


def _render_markdown(payload: Any) -> str:
    if isinstance(payload, str):
        return payload
    if isinstance(payload, dict):
        lines: list[str] = []
        for key, value in payload.items():
            if isinstance(value, (dict, list)):
                lines.append(f"**{key}**:")
                lines.append("```json")
                lines.append(json.dumps(value, ensure_ascii=False, indent=2))
                lines.append("```")
            else:
                lines.append(f"**{key}**: {value}")
        return "\n".join(lines)
    return json.dumps(payload, ensure_ascii=False, indent=2)


def write_error(error: SeedanceError, fmt: str = "json") -> None:
    body: dict[str, Any] = {
        "ok": False,
        "error": error.message,
        "code": error.code,
    }
    if error.payload:
        body["details"] = error.payload
    if fmt == "markdown":
        sys.stderr.write(f"Error ({error.code}): {error.message}\n")
        if error.payload:
            sys.stderr.write(
                json.dumps(error.payload, ensure_ascii=False, indent=2) + "\n"
            )
    else:
        sys.stderr.write(json.dumps(body, ensure_ascii=False, indent=2) + "\n")
