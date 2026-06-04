from __future__ import annotations

from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
import hashlib
import json
import re
import threading
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from ..artifacts import read_json, write_json
from ..config import load_config
from ..errors import ImageGenError, RuntimeRouteError, UsageError
from ..output import build_output_preview
from .jobs import now_iso
from .provider_payload import handle_provider_payload


BATCH_SCHEMA = "image-gen-pro.batch-state.v1"
BATCH_REQUEST_SCHEMA = "image-gen-pro.batch-request.v1"
DEFAULT_BATCH_DIR = "_work/image_gen_batches"
DEFAULT_BATCH_CONCURRENCY = 5
MIN_BATCH_CONCURRENCY = 1
MAX_BATCH_CONCURRENCY = 7
MIN_BATCH_ITEMS = 3
SECRET_FIELDS = {"api_key", "base_url"}
DEFAULT_ALLOWED_FIELDS = {
    "command",
    "route",
    "model",
    "size",
    "aspect",
    "quality",
    "n",
    "background",
    "moderation",
    "output_format",
    "output_compression",
    "user",
    "timeout_sec",
    "output_dir",
    "prepare_local_media",
    "dry_run_payload",
}
ITEM_ALLOWED_FIELDS = DEFAULT_ALLOWED_FIELDS | {
    "id",
    "prompt",
    "prompt_file",
    "image",
    "mask",
    "output_file",
    "run_id",
}


def run_batch(args) -> dict[str, Any]:
    request_path = Path(args.file)
    if not request_path.exists() or not request_path.is_file():
        raise UsageError(f"--file must be an existing JSON file: {request_path}")
    request = _read_json_object(request_path, "batch request")
    _reject_secret_fields(request, "batch")
    concurrency = _resolve_concurrency(args, request)
    request_sha256 = _request_sha256(request)
    defaults = _validated_defaults(request.get("defaults", {}))
    raw_items = request.get("items")
    if not isinstance(raw_items, list):
        raise UsageError("batch file must contain an items array")
    if len(raw_items) < MIN_BATCH_ITEMS:
        raise UsageError(f"batch file must contain at least {MIN_BATCH_ITEMS} items")

    batch_id = _safe_id(args.batch_id or request.get("batch_id") or request_path.stem, "batch")
    config = load_config()
    batch_base = Path(config.get("batch_dir", DEFAULT_BATCH_DIR))
    batch_dir = batch_base / batch_id
    state_path = batch_dir / "state.json"
    existing_state = _read_json_object(state_path, "batch state") if state_path.exists() else None
    if existing_state and not args.resume:
        raise UsageError(f"batch already exists: {batch_id}; use --resume to continue it")
    if existing_state and existing_state.get("request_sha256") != request_sha256:
        raise UsageError(f"batch request changed since first run: {batch_id}; use a new --batch-id")

    item_specs = _build_item_specs(raw_items, defaults, request_path.parent, batch_id, bool(args.dry_run_payload))
    state = _initial_state(existing_state, batch_id, batch_dir, request_path, request_sha256, item_specs, args, concurrency)
    write_json(batch_dir / "request.json", {"schema": BATCH_REQUEST_SCHEMA, "request": request})
    state_lock = threading.Lock()
    runnable_specs = []
    for spec in item_specs:
        record = _find_item(state, spec["id"])
        if args.resume and record.get("status") == "succeeded":
            record["skipped_on_resume"] = True
            record["updated_at"] = now_iso()
            continue
        _mark_pending(record)
        runnable_specs.append(spec)
    _persist_state(state_path, state, state_lock)

    stop_requested = False
    next_index = 0
    in_flight: dict[Any, dict[str, Any]] = {}

    def submit_ready(executor: ThreadPoolExecutor) -> None:
        nonlocal next_index
        while not stop_requested and next_index < len(runnable_specs) and len(in_flight) < concurrency:
            spec = runnable_specs[next_index]
            next_index += 1
            _mark_running(_find_item(state, spec["id"]))
            _persist_state(state_path, state, state_lock)
            in_flight[executor.submit(_run_item, spec)] = spec

    if runnable_specs:
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            submit_ready(executor)
            while in_flight:
                done, _pending = wait(in_flight, return_when=FIRST_COMPLETED)
                for future in done:
                    spec = in_flight.pop(future)
                    record = _find_item(state, spec["id"])
                    try:
                        summary = future.result()
                        _mark_succeeded(record, summary)
                    except ImageGenError as exc:
                        _mark_failed(record, _error_record(exc))
                        if args.stop_on_error:
                            stop_requested = True
                    except Exception as exc:
                        _mark_failed(record, {"type": exc.__class__.__name__, "message": str(exc)[:500]})
                        if args.stop_on_error:
                            stop_requested = True
                    _persist_state(state_path, state, state_lock)
                submit_ready(executor)

    _persist_state(state_path, state, state_lock, final=True)
    _attach_batch_preview(state, batch_dir)
    _persist_state(state_path, state, state_lock, final=True)
    if state["status"] != "succeeded":
        if args.allow_failures:
            return state
        raise RuntimeRouteError(f"batch finished with status={state['status']}; see {state_path}")
    return state


def list_batches(args) -> dict[str, Any]:
    config = load_config()
    limit = args.limit
    if limit < 1:
        raise UsageError("--limit must be at least 1")
    batch_base = Path(config.get("batch_dir", DEFAULT_BATCH_DIR))
    batches = []
    if batch_base.exists():
        candidates = [path for path in batch_base.iterdir() if path.is_dir() and (path / "state.json").exists()]
        for batch_dir in sorted(candidates, key=lambda path: (path / "state.json").stat().st_mtime, reverse=True)[:limit]:
            state = _read_json_object(batch_dir / "state.json", "batch state")
            batches.append(_state_summary(state))
    return {
        "schema": "image-gen-pro.batch-list.v1",
        "batch_dir": str(batch_base),
        "count": len(batches),
        "batches": batches,
    }


def show_batch(args) -> dict[str, Any]:
    config = load_config()
    batch_id = _safe_id(args.batch_id, "batch")
    state_path = Path(config.get("batch_dir", DEFAULT_BATCH_DIR)) / batch_id / "state.json"
    if not state_path.exists():
        raise UsageError(f"batch not found: {batch_id}")
    return _read_json_object(state_path, "batch state")


def _validated_defaults(raw: Any) -> dict[str, Any]:
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise UsageError("batch defaults must be an object")
    _reject_secret_fields(raw, "defaults")
    unknown = sorted(set(raw) - DEFAULT_ALLOWED_FIELDS)
    if unknown:
        raise UsageError(f"unknown batch default field(s): {', '.join(unknown)}")
    return dict(raw)


def _resolve_concurrency(args, request: dict[str, Any]) -> int:
    raw = getattr(args, "concurrency", None)
    if raw is None:
        raw = request.get("concurrency", DEFAULT_BATCH_CONCURRENCY)
    return _bounded_int(raw, "batch concurrency", MIN_BATCH_CONCURRENCY, MAX_BATCH_CONCURRENCY)


def _build_item_specs(
    raw_items: list[Any],
    defaults: dict[str, Any],
    base_dir: Path,
    batch_id: str,
    dry_run_payload: bool,
) -> list[dict[str, Any]]:
    specs = []
    seen_ids: set[str] = set()
    seen_run_ids: set[str] = set()
    for index, raw_item in enumerate(raw_items, start=1):
        if not isinstance(raw_item, dict):
            raise UsageError(f"batch item #{index} must be an object")
        _reject_secret_fields(raw_item, f"item #{index}")
        unknown = sorted(set(raw_item) - ITEM_ALLOWED_FIELDS)
        if unknown:
            raise UsageError(f"unknown batch item field(s) in item #{index}: {', '.join(unknown)}")
        item = {**defaults, **raw_item}
        item_id = _safe_id(item.get("id") or f"item-{index:03d}", f"item-{index:03d}")
        if item_id in seen_ids:
            raise UsageError(f"duplicate batch item id: {item_id}")
        seen_ids.add(item_id)
        command = item.get("command", "generate")
        if command not in {"generate", "edit"}:
            raise UsageError(f"batch item {item_id} command must be generate or edit")
        prompt = item.get("prompt")
        prompt_file = _resolve_optional_path(item.get("prompt_file"), base_dir)
        if bool(prompt) == bool(prompt_file):
            raise UsageError(f"batch item {item_id} must use exactly one of prompt or prompt_file")
        run_id = _safe_id(item.get("run_id") or f"{batch_id}-{item_id}", f"{batch_id}-{item_id}")
        if run_id in seen_run_ids:
            raise UsageError(f"duplicate batch run_id: {run_id}")
        seen_run_ids.add(run_id)
        n = _positive_int(item.get("n", 1), f"batch item {item_id} n")
        timeout_sec = _positive_int(item.get("timeout_sec", 300), f"batch item {item_id} timeout_sec")
        spec = {
            "index": index,
            "id": item_id,
            "run_id": run_id,
            "command": command,
            "prompt": str(prompt) if prompt is not None else None,
            "prompt_file": prompt_file,
            "image": _resolve_path_list(item.get("image"), base_dir),
            "mask": _resolve_optional_path(item.get("mask"), base_dir),
            "route": item.get("route"),
            "model": item.get("model"),
            "size": item.get("size", "auto"),
            "aspect": item.get("aspect"),
            "quality": item.get("quality", "auto"),
            "n": n,
            "background": item.get("background"),
            "moderation": item.get("moderation"),
            "output_format": item.get("output_format", "png"),
            "output_compression": item.get("output_compression"),
            "output_file": _resolve_optional_path(item.get("output_file"), base_dir),
            "output_dir": _resolve_optional_path(item.get("output_dir"), base_dir),
            "user": item.get("user"),
            "timeout_sec": timeout_sec,
            "dry_run_payload": bool(dry_run_payload or item.get("dry_run_payload", False)),
            "prepare_local_media": item.get("prepare_local_media", "auto"),
        }
        if command == "edit" and not spec["image"]:
            raise UsageError(f"batch edit item {item_id} requires image")
        if command == "generate" and spec["image"]:
            raise UsageError(f"batch generate item {item_id} must not include image")
        specs.append(spec)
    return specs


def _run_item(spec: dict[str, Any]) -> dict[str, Any]:
    captured: list[dict[str, Any]] = []
    namespace = SimpleNamespace(
        command=spec["command"],
        prompt=spec["prompt"],
        prompt_file=spec["prompt_file"],
        route=spec["route"],
        model=spec["model"],
        size=spec["size"],
        aspect=spec["aspect"],
        quality=spec["quality"],
        n=spec["n"],
        background=spec["background"],
        moderation=spec["moderation"],
        output_format=spec["output_format"],
        output_compression=spec["output_compression"],
        output_file=spec["output_file"],
        output_dir=spec["output_dir"],
        user=spec["user"],
        api_key=None,
        base_url=None,
        timeout_sec=spec["timeout_sec"],
        run_id=spec["run_id"],
        dry_run_payload=spec["dry_run_payload"],
        prepare_local_media=spec["prepare_local_media"],
        image=spec["image"] if spec["command"] == "edit" else None,
        mask=spec["mask"],
    )
    handle_provider_payload(namespace, captured.append)
    if not captured:
        raise RuntimeRouteError(f"batch item produced no summary: {spec['id']}")
    return captured[-1]


def _initial_state(
    existing: dict[str, Any] | None,
    batch_id: str,
    batch_dir: Path,
    request_path: Path,
    request_sha256: str,
    specs,
    args,
    concurrency: int,
) -> dict[str, Any]:
    created_at = existing.get("created_at") if existing else now_iso()
    existing_items = {item.get("id"): item for item in (existing or {}).get("items", [])}
    items = []
    for spec in specs:
        previous = existing_items.get(spec["id"])
        if previous:
            item = dict(previous)
            item.update({"index": spec["index"], "run_id": spec["run_id"], "command": spec["command"]})
        else:
            item = {
                "index": spec["index"],
                "id": spec["id"],
                "run_id": spec["run_id"],
                "command": spec["command"],
                "status": "pending",
                "created_at": created_at,
                "updated_at": created_at,
            }
        items.append(item)
    state = {
        "schema": BATCH_SCHEMA,
        "batch_id": batch_id,
        "batch_dir": str(batch_dir),
        "request_file": str(request_path),
        "request_sha256": request_sha256,
        "status": "running",
        "created_at": created_at,
        "updated_at": now_iso(),
        "resume": bool(args.resume),
        "dry_run_payload": bool(args.dry_run_payload),
        "stop_on_error": bool(args.stop_on_error),
        "concurrency": concurrency,
        "items": items,
        "counts": {},
    }
    _refresh_state(state)
    return state


def _refresh_state(state: dict[str, Any], *, final: bool = False) -> None:
    counts = {"total": len(state["items"]), "pending": 0, "running": 0, "succeeded": 0, "failed": 0}
    for item in state["items"]:
        status = item.get("status", "pending")
        if status in counts:
            counts[status] += 1
    state["counts"] = counts
    if final:
        if counts["failed"] > 0:
            state["status"] = "failed"
        elif counts["pending"] > 0 or counts["running"] > 0:
            state["status"] = "partial"
        else:
            state["status"] = "succeeded"
    state["updated_at"] = now_iso()


def _write_state(path: Path, state: dict[str, Any]) -> None:
    write_json(path, state)
    write_json(path.with_name("summary.json"), _state_summary(state))


def _persist_state(path: Path, state: dict[str, Any], lock: threading.Lock, *, final: bool = False) -> None:
    with lock:
        _refresh_state(state, final=final)
        if final:
            state["ok"] = state["status"] == "succeeded"
        _write_state(path, state)


def _state_summary(state: dict[str, Any]) -> dict[str, Any]:
    summary = {
        "schema": "image-gen-pro.batch-summary.v1",
        "batch_id": state.get("batch_id"),
        "batch_dir": state.get("batch_dir"),
        "status": state.get("status"),
        "concurrency": state.get("concurrency"),
        "counts": state.get("counts"),
        "created_at": state.get("created_at"),
        "updated_at": state.get("updated_at"),
    }
    if state.get("preview"):
        summary["preview"] = state.get("preview")
    return summary


def _find_item(state: dict[str, Any], item_id: str) -> dict[str, Any]:
    for item in state["items"]:
        if item.get("id") == item_id:
            return item
    raise UsageError(f"batch item missing from state: {item_id}")


def _safe_id(raw: Any, fallback: str) -> str:
    value = str(raw or fallback).strip()
    value = re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-._")
    return value[:96] or fallback


def _resolve_optional_path(raw: Any, base_dir: Path) -> str | None:
    if raw in {None, ""}:
        return None
    path = Path(str(raw))
    if not path.is_absolute():
        path = base_dir / path
    return str(path)


def _resolve_path_list(raw: Any, base_dir: Path) -> list[str]:
    if raw in {None, ""}:
        return []
    values = raw if isinstance(raw, list) else [raw]
    paths = []
    for value in values:
        resolved = _resolve_optional_path(value, base_dir)
        if not resolved:
            raise UsageError("batch image list must not contain empty paths")
        paths.append(resolved)
    return paths


def _positive_int(raw: Any, label: str) -> int:
    try:
        value = int(raw)
    except (TypeError, ValueError) as exc:
        raise UsageError(f"{label} must be an integer") from exc
    if value < 1:
        raise UsageError(f"{label} must be at least 1")
    return value


def _bounded_int(raw: Any, label: str, minimum: int, maximum: int) -> int:
    value = _positive_int(raw, label)
    if value < minimum:
        raise UsageError(f"{label} must be at least {minimum}")
    if value > maximum:
        raise UsageError(f"{label} must be at most {maximum}")
    return value


def _clear_item_attempt(record: dict[str, Any]) -> None:
    for key in ("error", "summary", "outputs", "preview", "run_dir", "job_status", "started_at", "skipped_on_resume"):
        record.pop(key, None)


def _mark_pending(record: dict[str, Any]) -> None:
    _clear_item_attempt(record)
    record["status"] = "pending"
    record["updated_at"] = now_iso()


def _mark_running(record: dict[str, Any]) -> None:
    _clear_item_attempt(record)
    record.update({
        "status": "running",
        "started_at": now_iso(),
        "updated_at": now_iso(),
    })


def _mark_succeeded(record: dict[str, Any], summary: dict[str, Any]) -> None:
    record.pop("error", None)
    record.update({
        "status": "succeeded",
        "summary": summary,
        "outputs": summary.get("outputs", []),
        "run_dir": summary.get("run_dir"),
        "job_status": summary.get("job_status"),
        "updated_at": now_iso(),
    })
    if summary.get("preview"):
        record["preview"] = summary["preview"]


def _mark_failed(record: dict[str, Any], error: dict[str, Any]) -> None:
    record.update({
        "status": "failed",
        "error": error,
        "updated_at": now_iso(),
    })


def _reject_secret_fields(data: dict[str, Any], label: str) -> None:
    present = sorted(SECRET_FIELDS & set(data))
    if present:
        raise UsageError(f"{label} must not contain credential field(s): {', '.join(present)}; use env or CLI config")


def _read_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        return read_json(path)
    except Exception as exc:
        raise UsageError(f"invalid {label} JSON: {path}: {exc}") from exc


def _request_sha256(request: dict[str, Any]) -> str:
    canonical = json.dumps(request, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _error_record(exc: ImageGenError) -> dict[str, Any]:
    return {
        "type": exc.__class__.__name__,
        "exit_code": exc.exit_code,
        "message": str(exc)[:500],
    }


def _attach_batch_preview(state: dict[str, Any], batch_dir: Path) -> None:
    outputs: list[dict[str, Any]] = []
    for item in state.get("items", []):
        raw_outputs = item.get("outputs")
        if isinstance(raw_outputs, list):
            outputs.extend(output for output in raw_outputs if isinstance(output, dict))
    if not outputs:
        state.pop("preview", None)
        return
    state["preview"] = build_output_preview(outputs, batch_dir / "preview")
