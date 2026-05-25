from __future__ import annotations

from pathlib import Path

from ..artifacts import read_json, run_summary
from ..errors import UsageError


def list_runs(config: dict, limit: int) -> dict:
    if limit < 1:
        raise UsageError("--limit must be at least 1")
    base = Path(config.get("run_dir", "_work/image_gen_runs"))
    runs = []
    if base.exists():
        candidates = [path for path in base.iterdir() if path.is_dir()]
        for run_dir in sorted(candidates, key=lambda path: path.stat().st_mtime, reverse=True)[:limit]:
            runs.append(run_summary(run_dir))
    return {
        "schema": "image-gen-pro.runs-list.v1",
        "run_dir": str(base),
        "count": len(runs),
        "runs": runs,
    }


def show_run(config: dict, run_id: str) -> dict:
    base = Path(config.get("run_dir", "_work/image_gen_runs"))
    run_dir = base / run_id
    if not run_dir.exists() or not run_dir.is_dir():
        raise UsageError(f"run not found: {run_id}")
    files = {}
    for name in [
        "summary.json",
        "generation-log.json",
        "manifest.json",
        "request.json",
        "media-manifest.json",
        "request-payload-redacted.json",
        "result.json",
        "job.json",
    ]:
        path = run_dir / name
        if path.exists():
            files[name] = read_json(path)
    return {
        "schema": "image-gen-pro.run-detail.v1",
        "run_id": run_id,
        "run_dir": str(run_dir),
        "files": files,
    }
