"""Webhook receiver helpers for optional callback_url integrations."""

from __future__ import annotations

import argparse
import json
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from seedance2.constants import EXIT_RUNTIME, EXIT_USAGE
from seedance2.errors import SeedanceError


def cmd_callback_server(args: argparse.Namespace) -> dict:
    out_dir = Path(args.out_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    server = _CallbackServer((args.host, args.port), _CallbackHandler)
    server.out_dir = out_dir
    server.path_prefix = args.path
    server.max_events = args.max_events
    server.events = []

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        while args.max_events == 0 or len(server.events) < args.max_events:
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    return {
        "ok": True,
        "url": f"http://{args.host}:{args.port}{args.path}",
        "out_dir": str(out_dir),
        "received": len(server.events),
        "events": server.events,
    }


def cmd_callback_smoke(args: argparse.Namespace) -> dict:
    payload = {
        "id": args.task_id,
        "status": args.status,
        "video_url": "https://example.com/generated.mp4",
        "created_at": int(time.time()),
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        args.url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "User-Agent": "videogen-callback-smoke",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as response:
            text = response.read().decode("utf-8", errors="replace")
            return {
                "ok": 200 <= response.status < 300,
                "url": args.url,
                "http_status": response.status,
                "response": json.loads(text) if text else {},
                "sent": payload,
            }
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        raise SeedanceError(
            f"callback smoke failed: HTTP {exc.code}",
            code=EXIT_RUNTIME,
            payload={"http_status": exc.code, "raw": text[:500]},
        )
    except urllib.error.URLError as exc:
        raise SeedanceError(
            f"callback smoke failed: {exc.reason}",
            code=EXIT_RUNTIME,
            payload={"reason": str(exc.reason)},
        )


class _CallbackServer(ThreadingHTTPServer):
    out_dir: Path
    path_prefix: str
    max_events: int
    events: list[dict]


class _CallbackHandler(BaseHTTPRequestHandler):
    server: _CallbackServer

    def do_POST(self) -> None:
        if urlparse(self.path).path != self.server.path_prefix:
            self.send_error(404, "not found")
            return
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length > 10 * 1024 * 1024:
            self.send_error(413, "payload too large")
            return
        raw = self.rfile.read(length)
        event = _callback_event(self, raw)
        path = _write_callback_event(self.server.out_dir, event)
        summary = {
            "received_at": event["received_at"],
            "task_id": event.get("task_id"),
            "status": event.get("status"),
            "path": str(path),
        }
        self.server.events.append(summary)
        response = json.dumps({"ok": True, **summary}, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format, *args) -> None:
        return


def _callback_event(handler: _CallbackHandler, raw: bytes) -> dict:
    parsed = None
    try:
        parsed = json.loads(raw.decode("utf-8")) if raw else None
    except json.JSONDecodeError:
        parsed = None
    task_id = _extract_task_id(parsed)
    status = parsed.get("status") if isinstance(parsed, dict) else None
    return {
        "received_at": datetime.now().isoformat(timespec="seconds"),
        "method": "POST",
        "path": handler.path,
        "headers": {key: value for key, value in handler.headers.items()},
        "task_id": task_id,
        "status": status,
        "body": parsed,
        "raw_body": raw.decode("utf-8", errors="replace") if parsed is None else None,
    }


def _write_callback_event(out_dir: Path, event: dict) -> Path:
    stem = _safe_name(event.get("task_id") or "callback")
    status = _safe_name(event.get("status") or "unknown")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = out_dir / f"{timestamp}-{stem}-{status}.json"
    path.write_text(json.dumps(event, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def _extract_task_id(body: object) -> str | None:
    if not isinstance(body, dict):
        return None
    for key in ("id", "task_id"):
        value = body.get(key)
        if isinstance(value, str):
            return value
    nested = body.get("task")
    if isinstance(nested, dict):
        value = nested.get("id") or nested.get("task_id")
        if isinstance(value, str):
            return value
    return None


def _safe_name(value: object) -> str:
    text = str(value or "").strip()
    safe = "".join(ch if ch.isalnum() or ch in "._-" else "-" for ch in text)
    safe = safe.strip("-")
    if not safe:
        raise SeedanceError("empty callback filename component", code=EXIT_USAGE)
    return safe[:80]
