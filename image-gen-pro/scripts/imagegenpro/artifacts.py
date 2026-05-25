from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any


def stable_run_id(prompt: str) -> str:
    stamp = time.strftime("%Y%m%d-%H%M%S")
    digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:8]
    return f"{stamp}-{digest}"


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON file must contain an object: {path}")
    return data


def run_paths(base_dir: str, run_id: str) -> Path:
    path = Path(base_dir) / run_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prompt_fingerprint(prompt: str) -> dict[str, Any]:
    return {
        "chars": len(prompt),
        "sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
    }


def run_summary(run_dir: Path) -> dict[str, Any]:
    summary_path = run_dir / "summary.json"
    summary = read_json(summary_path) if summary_path.exists() else {}
    log_path = run_dir / "generation-log.json"
    log = read_json(log_path) if log_path.exists() else {}
    job_path = run_dir / "job.json"
    job = read_json(job_path) if job_path.exists() else {}
    stat = run_dir.stat()
    return {
        "run_id": run_dir.name,
        "run_dir": str(run_dir),
        "command": summary.get("command") or log.get("command"),
        "route": summary.get("route") or log.get("route", {}).get("final_route"),
        "provider": summary.get("provider"),
        "model": summary.get("model"),
        "dry_run_payload": summary.get("dry_run_payload"),
        "outputs": summary.get("outputs", []),
        "job_status": job.get("status"),
        "mtime": stat.st_mtime,
        "has_generation_log": log_path.exists(),
        "has_job": job_path.exists(),
    }
