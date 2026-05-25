from __future__ import annotations

import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..artifacts import read_json, write_json
from ..errors import UsageError


TERMINAL_STATUSES = {"succeeded", "failed", "cancelled"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def new_job(run_id: str, run_dir: Path, command: str, provider: str | None = None) -> dict[str, Any]:
    created_at = now_iso()
    return {
        "schema": "image-gen-pro.job.v1",
        "run_id": run_id,
        "run_dir": str(run_dir),
        "command": command,
        "provider": provider,
        "status": "created",
        "created_at": created_at,
        "updated_at": created_at,
        "remote_task": None,
        "history": [
            {"status": "created", "at": created_at},
        ],
    }


def mark_job(job: dict[str, Any], status: str, **extra: Any) -> dict[str, Any]:
    if status not in {"created", "running", "succeeded", "failed", "cancelled"}:
        raise UsageError(f"invalid job status: {status}")
    updated = dict(job)
    updated["status"] = status
    updated["updated_at"] = now_iso()
    updated.update(extra)
    history = list(updated.get("history", []))
    entry = {"status": status, "at": updated["updated_at"]}
    if "route" in extra and extra["route"] is not None:
        entry["route"] = extra["route"]
    if "error" in extra and extra["error"] is not None:
        entry["error"] = extra["error"]
    history.append(entry)
    updated["history"] = history
    return updated


def write_job(run_dir: Path, job: dict[str, Any]) -> None:
    write_json(run_dir / "job.json", job)


def list_jobs(config: dict, limit: int) -> dict[str, Any]:
    if limit < 1:
        raise UsageError("--limit must be at least 1")
    base = Path(config.get("run_dir", "_work/image_gen_runs"))
    jobs = []
    if base.exists():
        candidates = [path for path in base.iterdir() if path.is_dir() and (path / "job.json").exists()]
        for run_dir in sorted(candidates, key=lambda path: (path / "job.json").stat().st_mtime, reverse=True)[:limit]:
            jobs.append(read_json(run_dir / "job.json"))
    return {
        "schema": "image-gen-pro.jobs-list.v1",
        "run_dir": str(base),
        "count": len(jobs),
        "jobs": jobs,
    }


def show_job(config: dict, run_id: str) -> dict[str, Any]:
    job_path = _job_path(config, run_id)
    if not job_path.exists():
        raise UsageError(f"job not found: {run_id}")
    return read_json(job_path)


def wait_job(config: dict, run_id: str, timeout_sec: int) -> dict[str, Any]:
    if timeout_sec < 0:
        raise UsageError("--timeout-sec must be >= 0")
    deadline = time.monotonic() + timeout_sec
    while True:
        job = show_job(config, run_id)
        if job.get("status") in TERMINAL_STATUSES:
            return job
        if time.monotonic() >= deadline:
            return {
                "schema": "image-gen-pro.job-wait.v1",
                "run_id": run_id,
                "status": job.get("status"),
                "timed_out": True,
                "job": job,
            }
        time.sleep(1)


def delete_job(config: dict, run_id: str) -> dict[str, Any]:
    base = Path(config.get("run_dir", "_work/image_gen_runs"))
    run_dir = base / run_id
    if not run_dir.exists() or not run_dir.is_dir() or not (run_dir / "job.json").exists():
        raise UsageError(f"job not found: {run_id}")
    resolved_base = base.resolve()
    resolved_run = run_dir.resolve()
    if resolved_base != resolved_run and resolved_base not in resolved_run.parents:
        raise UsageError(f"refusing to delete job outside run_dir: {run_id}")
    shutil.rmtree(resolved_run)
    return {
        "schema": "image-gen-pro.job-delete.v1",
        "run_id": run_id,
        "deleted": True,
        "run_dir": str(resolved_run),
    }


def _job_path(config: dict, run_id: str) -> Path:
    return Path(config.get("run_dir", "_work/image_gen_runs")) / run_id / "job.json"
