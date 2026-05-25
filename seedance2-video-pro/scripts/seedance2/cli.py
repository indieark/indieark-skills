"""Main entry point: parse -> dispatch -> emit."""

from __future__ import annotations

import sys
from typing import List, Optional

from seedance2.constants import EXIT_CONFIG, EXIT_OK, EXIT_RUNTIME
from seedance2.errors import SeedanceError, emit, write_error
from seedance2.parser import build_parser


def main(argv: Optional[List[str]] = None) -> int:
    _configure_stdio()
    parser = build_parser()
    args = parser.parse_args(argv)
    fmt = getattr(args, "format", "json") or "json"
    try:
        result = args.func(args)
    except SeedanceError as exc:
        write_error(exc, fmt)
        return exc.code
    except KeyboardInterrupt:
        write_error(SeedanceError("interrupted by user", code=EXIT_RUNTIME), fmt)
        return EXIT_RUNTIME
    except Exception as exc:  # pragma: no cover - last-resort guard
        write_error(SeedanceError(f"unexpected error: {exc}", code=EXIT_RUNTIME), fmt)
        return EXIT_RUNTIME
    if result is None:
        return EXIT_OK
    if isinstance(result, dict) and "ok" in result and not result["ok"]:
        emit(result, fmt=fmt)
        return EXIT_CONFIG
    emit(result, fmt=fmt)
    return EXIT_OK


def _configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            reconfigure(encoding="utf-8", errors="replace")
