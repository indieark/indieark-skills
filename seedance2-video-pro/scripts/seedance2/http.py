"""HTTP request helper and media file / URL encoding."""

from __future__ import annotations

import base64
import json
import mimetypes
import urllib.error
import urllib.request
from pathlib import Path

from seedance2.constants import (
    EXIT_API,
    EXIT_RUNTIME,
    EXIT_USAGE,
    MEDIA_DEFAULTS,
    MEDIA_LIMITS_MB,
)
from seedance2.errors import SeedanceError


def is_http_url(text: str) -> bool:
    return text.startswith(("http://", "https://"))


def request_json(
    method: str,
    url: str,
    api_key: str,
    *,
    payload: dict | None = None,
    timeout: int = 60,
) -> dict:
    body = (
        json.dumps(payload, ensure_ascii=False).encode("utf-8")
        if payload is not None
        else None
    )
    req = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            text = response.read().decode("utf-8")
            return json.loads(text) if text else {}
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        try:
            data = json.loads(text)
            message = (
                data.get("error", {}).get("message") or data.get("message") or text
            )
        except json.JSONDecodeError:
            message = text
        raise SeedanceError(
            f"HTTP {exc.code}: {message}",
            code=EXIT_API,
            payload={"http_status": exc.code, "raw": text[:500]},
        )
    except urllib.error.URLError as exc:
        raise SeedanceError(
            f"network error: {exc.reason}",
            code=EXIT_RUNTIME,
            payload={"reason": str(exc.reason)},
        )


def media_to_url(path_text: str, kind: str) -> str:
    if path_text.startswith(("http://", "https://", "data:", "asset://")):
        return path_text
    if kind == "video":
        raise SeedanceError(
            "reference_video must be provided as a web url; "
            "serve the file through a temporary HTTPS tunnel or signed object URL",
            code=EXIT_USAGE,
        )
    path = Path(path_text).expanduser()
    if not path.exists() or not path.is_file():
        raise SeedanceError(f"{kind} file not found: {path_text}", code=EXIT_USAGE)
    size_mb = path.stat().st_size / 1024 / 1024
    limit = MEDIA_LIMITS_MB[kind]
    if size_mb > limit:
        raise SeedanceError(
            f"{kind} file is {size_mb:.1f} MB, max {limit} MB: {path}",
            code=EXIT_USAGE,
        )
    mime, _ = mimetypes.guess_type(str(path))
    if not mime:
        mime = MEDIA_DEFAULTS[kind]
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def probe_media_url(url: str, kind: str, timeout: int = 15) -> dict:
    if not is_http_url(url):
        return {"url": url, "kind": kind, "checked": False, "reason": "not_http_url"}
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return _probe_result(url, kind, response)
    except urllib.error.HTTPError as exc:
        if exc.code not in {403, 405}:
            raise SeedanceError(
                f"{kind} url is not accessible: HTTP {exc.code}",
                code=EXIT_USAGE,
                payload={"url": _redact_url(url), "http_status": exc.code},
            )
    except urllib.error.URLError as exc:
        raise SeedanceError(
            f"{kind} url is not accessible: {exc.reason}",
            code=EXIT_USAGE,
            payload={"url": _redact_url(url), "reason": str(exc.reason)},
        )

    req = urllib.request.Request(url, headers={"Range": "bytes=0-0"}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return _probe_result(url, kind, response)
    except urllib.error.HTTPError as exc:
        raise SeedanceError(
            f"{kind} url is not accessible: HTTP {exc.code}",
            code=EXIT_USAGE,
            payload={"url": _redact_url(url), "http_status": exc.code},
        )
    except urllib.error.URLError as exc:
        raise SeedanceError(
            f"{kind} url is not accessible: {exc.reason}",
            code=EXIT_USAGE,
            payload={"url": _redact_url(url), "reason": str(exc.reason)},
        )


def _probe_result(url: str, kind: str, response) -> dict:
    content_type = response.headers.get("Content-Type", "")
    content_length = response.headers.get("Content-Length")
    status = getattr(response, "status", response.getcode())
    if status < 200 or status >= 300:
        raise SeedanceError(
            f"{kind} url is not accessible: HTTP {status}",
            code=EXIT_USAGE,
            payload={"url": _redact_url(url), "http_status": status},
        )
    return {
        "url": _redact_url(url),
        "kind": kind,
        "checked": True,
        "http_status": status,
        "content_type": content_type,
        "content_length": int(content_length) if content_length and content_length.isdigit() else None,
    }


def _redact_url(url: str) -> str:
    return url.split("?", 1)[0]


def content_item(kind: str, source: str, role: str | None = None) -> dict:
    if kind == "text":
        return {"type": "text", "text": source}
    if kind == "image":
        item: dict = {
            "type": "image_url",
            "image_url": {"url": media_to_url(source, "image")},
        }
    elif kind == "video":
        item = {
            "type": "video_url",
            "video_url": {"url": media_to_url(source, "video")},
        }
    elif kind == "audio":
        item = {
            "type": "audio_url",
            "audio_url": {"url": media_to_url(source, "audio")},
        }
    else:
        raise SeedanceError(f"unsupported content kind: {kind}", code=EXIT_RUNTIME)
    if role:
        item["role"] = role
    return item
