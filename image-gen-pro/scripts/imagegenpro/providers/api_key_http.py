from __future__ import annotations

import json
import mimetypes
import os
import re
import secrets
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from ..config import normalize_base_url
from ..constants import GPT_IMAGE_2_MODEL, MJ_MODEL, NANO_BANANA_MODEL
from ..errors import RuntimeRouteError, UsageError


API_KEY_ENV = "IMAGE_GEN_PRO_API_KEY"
BASE_URL_ENV = "IMAGE_GEN_PRO_API_BASE_URL"
DEFAULT_BASE_URL = "https://api.openai.com"
MODEL_API_KEY_ENVS = {
    GPT_IMAGE_2_MODEL: "IMAGE_GEN_PRO_GPT_IMAGE_2_API_KEY",
    NANO_BANANA_MODEL: "IMAGE_GEN_PRO_NANO_BANANA_API_KEY",
    MJ_MODEL: "IMAGE_GEN_PRO_MJ_API_KEY",
}
MODEL_BASE_URL_ENVS = {
    GPT_IMAGE_2_MODEL: "IMAGE_GEN_PRO_GPT_IMAGE_2_API_BASE_URL",
    NANO_BANANA_MODEL: "IMAGE_GEN_PRO_NANO_BANANA_API_BASE_URL",
    MJ_MODEL: "IMAGE_GEN_PRO_MJ_API_BASE_URL",
}

def resolve_api_key(args, config: dict[str, Any], model: str = GPT_IMAGE_2_MODEL) -> tuple[str, str]:
    if getattr(args, "api_key", None):
        return args.api_key, "cli_arg"
    model_env = MODEL_API_KEY_ENVS.get(model)
    if model_env:
        model_value = os.environ.get(model_env)
        if model_value:
            return model_value, f"env:{model_env}"
    value = os.environ.get(API_KEY_ENV)
    if value:
        return value, f"env:{API_KEY_ENV}"
    if config.get("api_key"):
        return str(config["api_key"]), "config_file"
    model_hint = f", set {model_env}" if model_env else ""
    raise RuntimeRouteError(
        f"missing API key: pass --api-key{model_hint}, set {API_KEY_ENV}, or run `imagen setup --api-key ...`",
        3,
    )


def resolve_base_url(args, config: dict[str, Any], model: str = GPT_IMAGE_2_MODEL) -> tuple[str, str]:
    if getattr(args, "base_url", None):
        return _normalize_base_url(args.base_url), "cli_arg"
    model_env = MODEL_BASE_URL_ENVS.get(model)
    if model_env:
        model_value = os.environ.get(model_env)
        if model_value:
            return _normalize_base_url(model_value), f"env:{model_env}"
    value = os.environ.get(BASE_URL_ENV)
    if value:
        return _normalize_base_url(value), f"env:{BASE_URL_ENV}"
    if config.get("base_url"):
        return _normalize_base_url(str(config["base_url"])), "config_file"
    return DEFAULT_BASE_URL, "default"


def submit_generate(payload: dict[str, Any], api_key: str, timeout_sec: int, base_url: str) -> dict[str, Any]:
    if payload["provider"] == MJ_MODEL:
        return _submit_mj(payload, api_key, timeout_sec, base_url)
    body = _request_without_file_placeholders(payload["request"])
    submitted = _post_json("/v1/images/generations", body, api_key, timeout_sec, base_url)
    return _maybe_poll_nb_task(payload["provider"], submitted, api_key, timeout_sec, base_url)


def submit_edit(payload: dict[str, Any], api_key: str, timeout_sec: int, base_url: str) -> dict[str, Any]:
    if payload["provider"] == MJ_MODEL:
        return _submit_mj(payload, api_key, timeout_sec, base_url)
    fields = _string_fields(_request_without_file_placeholders(payload["request"], drop={"image", "mask"}))
    files = []
    for item in payload.get("files", []):
        role = item["role"]
        field_name = "mask" if role == "mask" else ("image" if payload["provider"] == NANO_BANANA_MODEL else "image[]")
        files.append((field_name, Path(item["path"])))
    submitted = _post_multipart("/v1/images/edits", fields, files, api_key, timeout_sec, base_url)
    return _maybe_poll_nb_task(payload["provider"], submitted, api_key, timeout_sec, base_url)


def redact_response(raw: dict[str, Any]) -> dict[str, Any]:
    return _redact_value(raw)


def extract_image_data(raw: dict[str, Any], api_key: str, timeout_sec: int, base_url: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    data = raw.get("data")
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                if isinstance(item.get("b64_json"), str):
                    items.append({"b64_json": item["b64_json"]})
                elif isinstance(item.get("url"), str):
                    items.append({"b64_json": _download_url_to_b64(item["url"], api_key, timeout_sec, base_url)})
    image_url = raw.get("imageUrl")
    if isinstance(image_url, str):
        items.append({"b64_json": _download_url_to_b64(image_url, api_key, timeout_sec, base_url)})
    image_urls = raw.get("imageUrls")
    if isinstance(image_urls, list):
        for item in image_urls:
            if isinstance(item, dict) and isinstance(item.get("url"), str):
                items.append({"b64_json": _download_url_to_b64(item["url"], api_key, timeout_sec, base_url)})
            elif isinstance(item, str):
                items.append({"b64_json": _download_url_to_b64(item, api_key, timeout_sec, base_url)})
    return items


def _post_json(path: str, body: dict[str, Any], api_key: str, timeout_sec: int, base_url: str, *, auth_header: str = "Authorization") -> dict[str, Any]:
    headers = {"Content-Type": "application/json"}
    if auth_header == "mj-api-secret":
        headers["mj-api-secret"] = api_key
    else:
        headers["Authorization"] = f"Bearer {api_key}"
    data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        _join_api_url(base_url, path),
        data=data,
        method="POST",
        headers=headers,
    )
    return _read_json(request, timeout_sec, api_key)


def _post_multipart(path: str, fields: dict[str, str], files: list[tuple[str, Path]], api_key: str, timeout_sec: int, base_url: str) -> dict[str, Any]:
    boundary = "----image-gen-pro-" + secrets.token_hex(12)
    body = _multipart_body(boundary, fields, files)
    request = urllib.request.Request(
        _join_api_url(base_url, path),
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
    )
    return _read_json(request, timeout_sec, api_key)


def _read_json(request: urllib.request.Request, timeout_sec: int, api_key: str) -> dict[str, Any]:
    try:
        with urllib.request.urlopen(request, timeout=timeout_sec) as response:
            text = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = _safe_error_detail(exc, api_key)
        raise RuntimeRouteError(f"api-key route failed: {detail}", _exit_for_status(exc.code)) from exc
    except urllib.error.URLError as exc:
        reason = _redact_secret_text(str(exc.reason), api_key)
        raise RuntimeRouteError(f"api-key route failed: {reason}") from exc
    except TimeoutError as exc:
        raise RuntimeRouteError("api-key route timed out") from exc
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeRouteError("api-key route returned invalid JSON") from exc
    if not isinstance(data, dict):
        raise RuntimeRouteError("api-key route returned a non-object JSON response")
    return data


def _submit_mj(payload: dict[str, Any], api_key: str, timeout_sec: int, base_url: str) -> dict[str, Any]:
    body = _request_without_file_placeholders(payload["request"], drop={"image"})
    base64_array = []
    for item in payload.get("files", []):
        if item.get("role") != "image":
            continue
        base64_array.append(_file_to_data_url(Path(item["path"])))
    body["base64Array"] = base64_array
    submitted = _post_json("/mj/submit/imagine", body, api_key, timeout_sec, base_url, auth_header="mj-api-secret")
    task_id = _extract_mj_task_id(submitted)
    if not task_id:
        return submitted
    final = _poll_mj_task(task_id, api_key, timeout_sec, base_url)
    final["submitted"] = redact_response(submitted)
    final["remote_task"] = task_id
    return final


def _poll_mj_task(task_id: str, api_key: str, timeout_sec: int, base_url: str) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_sec
    last: dict[str, Any] | None = None
    while time.monotonic() < deadline:
        request = urllib.request.Request(
            _join_api_url(base_url, f"/mj/task/{task_id}/fetch"),
            method="GET",
            headers={"mj-api-secret": api_key},
        )
        last = _read_json(request, min(30, max(1, int(deadline - time.monotonic()))), api_key)
        status = str(last.get("status") or "").upper()
        progress = str(last.get("progress") or "")
        if status == "SUCCESS" or progress == "100%":
            return last
        if status == "FAILURE":
            message = _redact_secret_text(str(last.get("failReason") or last.get("description") or "mj task failed"), api_key)
            raise RuntimeRouteError(f"mj route failed: {message}", 5)
        time.sleep(5)
    detail = f"; last status: {last.get('status')}" if last else ""
    raise RuntimeRouteError(f"mj route timed out while waiting for task {task_id}{detail}", 5)


def _maybe_poll_nb_task(provider: str, submitted: dict[str, Any], api_key: str, timeout_sec: int, base_url: str) -> dict[str, Any]:
    if provider != NANO_BANANA_MODEL:
        return submitted
    task_id = submitted.get("taskId")
    status = str(submitted.get("status") or "").upper()
    if not isinstance(task_id, str) or not task_id.strip() or status != "PENDING":
        return submitted
    final = _poll_nb_task(task_id.strip(), api_key, timeout_sec, base_url)
    final["submitted"] = redact_response(submitted)
    final["remote_task"] = task_id.strip()
    return final


def _poll_nb_task(task_id: str, api_key: str, timeout_sec: int, base_url: str) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_sec
    last: dict[str, Any] | None = None
    while time.monotonic() < deadline:
        request = urllib.request.Request(
            _join_nb_task_url(base_url, task_id),
            method="GET",
            headers={"Authorization": f"Bearer {api_key}"},
        )
        last = _read_json(request, min(30, max(1, int(deadline - time.monotonic()))), api_key)
        status = str(last.get("status") or "").upper()
        if status == "SUCCESS":
            data = last.get("data")
            if isinstance(data, dict):
                return data
            raise RuntimeRouteError("nano-banana async task returned SUCCESS without object data", 5)
        if status == "ERROR":
            message = _redact_secret_text(str(last.get("error") or "nano-banana task failed"), api_key)
            raise RuntimeRouteError(f"nano-banana route failed: {message}", _exit_for_status(_status_code(last.get("code"))))
        time.sleep(3)
    detail = f"; last status: {last.get('status')}" if last else ""
    raise RuntimeRouteError(f"nano-banana route timed out while waiting for task {task_id}{detail}", 5)


def _extract_mj_task_id(data: dict[str, Any]) -> str | None:
    for key in ("result", "taskId", "id"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _file_to_data_url(path: Path) -> str:
    if not path.exists() or not path.is_file():
        raise UsageError(f"image file does not exist or is not a file: {path}")
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    import base64

    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def _download_url_to_b64(raw_url: str, api_key: str, timeout_sec: int, base_url: str) -> str:
    import base64

    if raw_url.startswith("data:image/") and ";base64," in raw_url:
        return raw_url.split(";base64,", 1)[1]
    url = _absolute_url(raw_url, base_url)
    request = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=min(timeout_sec, 120)) as response:
            data = response.read()
    except urllib.error.HTTPError as exc:
        detail = _safe_error_detail(exc, api_key)
        raise RuntimeRouteError(f"provider image download failed: {detail}", _exit_for_status(exc.code)) from exc
    except urllib.error.URLError as exc:
        reason = _redact_secret_text(str(exc.reason), api_key)
        raise RuntimeRouteError(f"provider image download failed: {reason}") from exc
    if not data:
        raise RuntimeRouteError("provider image download returned empty content")
    return base64.b64encode(data).decode("ascii")


def _safe_error_detail(exc: urllib.error.HTTPError, api_key: str) -> str:
    try:
        text = exc.read().decode("utf-8", errors="replace")
    except Exception:
        text = ""
    if not text:
        return f"http {exc.code}"
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return f"http {exc.code}"
    message = data.get("error", {}).get("message") if isinstance(data.get("error"), dict) else None
    if isinstance(message, str):
        safe_message = _redact_secret_text(message, api_key)
        return f"http {exc.code}: {safe_message[:300]}"
    return f"http {exc.code}"


def _redact_secret_text(text: str, api_key: str | None = None) -> str:
    safe = text
    if api_key:
        safe = safe.replace(api_key, "<redacted-api-key>")
    safe = re.sub(
        r"(?i)(Authorization\s*[:=]\s*Bearer\s+)[^\s\"'<>]+",
        r"\1<redacted-api-key>",
        safe,
    )
    safe = re.sub(
        r"(?i)(Bearer\s+)sk-[A-Za-z0-9][A-Za-z0-9_\-]{8,}",
        r"\1<redacted-api-key>",
        safe,
    )
    safe = re.sub(
        r"sk-[A-Za-z0-9][A-Za-z0-9_\-]{8,}",
        "<redacted-api-key>",
        safe,
    )
    return safe


def _redact_value(value: Any) -> Any:
    if isinstance(value, dict):
        redacted: dict[str, Any] = {}
        for key, item in value.items():
            if key == "b64_json":
                redacted[key] = "<redacted>"
            elif isinstance(item, str) and item.startswith("data:image/") and ";base64," in item:
                redacted[key] = "<redacted-data-url>"
            else:
                redacted[key] = _redact_value(item)
        return redacted
    if isinstance(value, list):
        return [_redact_value(item) for item in value]
    if isinstance(value, str) and value.startswith("data:image/") and ";base64," in value:
        return "<redacted-data-url>"
    return value


def _exit_for_status(status: int) -> int:
    if status in {400, 404, 422}:
        return 2
    if status in {401, 403}:
        return 3
    return 5


def _status_code(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 502


def _request_without_file_placeholders(request: dict[str, Any], drop: set[str] | None = None) -> dict[str, Any]:
    drop = drop or set()
    body = {}
    for key, value in request.items():
        if key in drop:
            continue
        body[key] = value
    return body


def _string_fields(data: dict[str, Any]) -> dict[str, str]:
    fields: dict[str, str] = {}
    for key, value in data.items():
        if value is None:
            continue
        fields[key] = str(value)
    return fields


def _multipart_body(boundary: str, fields: dict[str, str], files: list[tuple[str, Path]]) -> bytes:
    chunks: list[bytes] = []
    for name, value in fields.items():
        chunks.extend([
            f"--{boundary}\r\n".encode("utf-8"),
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"),
            value.encode("utf-8"),
            b"\r\n",
        ])
    for field_name, path in files:
        if not path.exists() or not path.is_file():
            raise UsageError(f"{field_name} file does not exist or is not a file: {path}")
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        chunks.extend([
            f"--{boundary}\r\n".encode("utf-8"),
            f'Content-Disposition: form-data; name="{field_name}"; filename="{path.name}"\r\n'.encode("utf-8"),
            f"Content-Type: {mime}\r\n\r\n".encode("utf-8"),
            path.read_bytes(),
            b"\r\n",
        ])
    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks)


def _normalize_base_url(raw: str) -> str:
    return normalize_base_url(raw, label="--base-url", error_cls=UsageError)


def _join_api_url(base: str, path: str) -> str:
    if base.endswith("/v1") and path.startswith("/v1/"):
        path = path[3:]
        return base + path
    if base.endswith("/v1") and path.startswith("/mj/"):
        return base[:-3] + path
    return base + path


def _absolute_url(raw_url: str, base_url: str) -> str:
    if raw_url.startswith(("http://", "https://")):
        return raw_url
    if raw_url.startswith("/"):
        parsed = urllib.parse.urlsplit(base_url)
        root = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, "", "", ""))
        return root.rstrip("/") + raw_url
    return raw_url


def _join_nb_task_url(base_url: str, task_id: str) -> str:
    base = base_url.rstrip("/")
    if base.endswith("/v1"):
        base = base[:-3]
    return f"{base}/task/{task_id}"
