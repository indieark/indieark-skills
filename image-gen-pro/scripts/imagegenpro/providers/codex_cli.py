from __future__ import annotations

import base64
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from ..artifacts import sha256_file
from ..errors import RuntimeRouteError


MIN_BLOB_LENGTH = 200
BASE64_BLOB_PATTERN = re.compile(r'"([A-Za-z0-9+/=]{' + str(MIN_BLOB_LENGTH) + r',})"')
IMAGE_MAGIC_PREFIXES = {
    "iVBORw0KGgo": "png",
    "/9j/": "jpeg",
    "UklGR": "webp",
}
SESSIONS_DIR_ENV = "IMAGE_GEN_PRO_CODEX_SESSIONS_DIR"
CODEX_CMD_ENV = "IMAGE_GEN_PRO_CODEX_CMD"
HOST_PATH_ENV = "IMAGE_GEN_PRO_HOST_PATH"
_MSYS_DRIVE_RE = re.compile(r"^/(?:cygdrive/)?([A-Za-z])(/.*)?$")
_CODEX_NAMES = ("codex.cmd", "codex.exe", "codex.bat", "codex")


def submit(payload: dict[str, Any], prompt: str, timeout_sec: int, output_path: Path) -> dict[str, Any]:
    codex = find_codex()
    if not codex:
        raise RuntimeRouteError("codex-cli route unavailable: codex command not found", 3)
    sessions_root = _sessions_root()
    sessions_root.mkdir(parents=True, exist_ok=True)
    before = _rollout_files(sessions_root)
    args = [
        codex,
        "exec",
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
        "--color",
        "never",
        "--enable",
        "image_generation",
    ]
    for item in payload.get("files", []):
        if item["role"] == "image":
            args.extend(["-i", item["path"]])

    instruction = _instruction(prompt, bool(payload.get("files")))
    try:
        result = subprocess.run(
            args,
            input=instruction.encode("utf-8"),
            capture_output=True,
            timeout=timeout_sec,
            check=False,
            env=subprocess_env(),
        )
    except subprocess.TimeoutExpired as exc:
        _cleanup_new_session_files(sessions_root, before)
        raise RuntimeRouteError("codex-cli route timed out") from exc
    if result.returncode != 0:
        stderr = _tail(_decode_stream(result.stderr))
        _cleanup_new_session_files(sessions_root, before)
        raise RuntimeRouteError(f"codex-cli route failed: exit={result.returncode}; {stderr}")

    after = _rollout_files(sessions_root)
    new_sessions = _new_session_files(after, before)
    if not new_sessions:
        raise RuntimeRouteError("codex-cli route failed: no new session rollout file")
    session_items = [_session_item(path) for path in new_sessions]
    image = find_best_image_blob(new_sessions)
    if image is None:
        cleanup = _cleanup_session_files(new_sessions, sessions_root)
        raise RuntimeRouteError("codex-cli route failed: image payload not found")
    blob, image_format = image
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(base64.b64decode(blob))
    finally:
        cleanup = _cleanup_session_files(new_sessions, sessions_root)
    return {
        "provider_response": {
            "route": "codex-cli",
            "session_files": session_items,
            "session_cleanup": cleanup,
            "image_format": image_format,
        },
        "output_paths": [output_path],
    }


def find_best_image_blob(session_paths: list[Path]) -> tuple[str, str] | None:
    best: tuple[str, str, int] | None = None
    for session_path in session_paths:
        try:
            text = session_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for line in text.splitlines():
            try:
                obj = json.loads(line)
            except ValueError:
                continue
            flat = json.dumps(obj)
            for match in BASE64_BLOB_PATTERN.finditer(flat):
                blob = match.group(1)
                for magic, image_format in IMAGE_MAGIC_PREFIXES.items():
                    if blob.startswith(magic):
                        if best is None or len(blob) > best[2]:
                            best = (blob, image_format, len(blob))
                        break
    if best is None:
        return None
    return best[0], best[1]


def _instruction(prompt: str, has_refs: bool) -> str:
    text = "Use the imagegen tool to generate the image for the following request."
    if has_refs:
        text += " Use the attached image(s) as visual reference / input for image-to-image."
    text += "\nRequirements: generate the image directly, return only the image, no explanation.\n\nRequest:\n"
    return text + prompt


def find_codex() -> str | None:
    override = os.environ.get(CODEX_CMD_ENV)
    if override:
        candidate = _msys_to_windows(override.strip().strip('"'))
        if Path(candidate).is_file():
            return candidate
        found_override = shutil.which(candidate)
        if found_override:
            return found_override
    found = shutil.which("codex")
    if found:
        return found
    if os.name != "nt":
        return None
    for directory in _path_dirs():
        for name in _CODEX_NAMES:
            candidate = Path(directory) / name
            if candidate.is_file():
                return str(candidate)
    return None


def subprocess_env() -> dict[str, str]:
    env = dict(os.environ)
    if os.name == "nt":
        path_value = os.pathsep.join(_path_dirs())
        for key in list(env):
            if key.lower() == "path":
                del env[key]
        env["PATH"] = path_value
    return env


def _path_dirs() -> list[str]:
    on_windows = os.name == "nt"
    dirs: list[str] = []
    seen: set[str] = set()

    def _add(entry: str) -> None:
        value = (_msys_to_windows(entry) if on_windows else entry).strip().strip('"')
        key = os.path.normcase(os.path.normpath(value)) if on_windows else value
        if value and key not in seen:
            seen.add(key)
            dirs.append(value)

    # Git Bash/MSYS may pass this as either Windows ';' or POSIX ':' PATH.
    host = os.environ.get(HOST_PATH_ENV, "")
    if on_windows and host:
        for entry in host.split(";" if ";" in host else ":"):
            _add(entry)
    for entry in os.environ.get("PATH", "").split(os.pathsep):
        _add(entry)
    return dirs


def _msys_to_windows(entry: str) -> str:
    match = _MSYS_DRIVE_RE.match(entry)
    if not match:
        return entry
    drive = match.group(1).upper()
    rest = (match.group(2) or "").replace("/", "\\")
    return f"{drive}:{rest}"


def _sessions_root() -> Path:
    override = os.environ.get(SESSIONS_DIR_ENV)
    if override:
        return Path(override)
    return Path.home() / ".codex" / "sessions"


def _rollout_files(root: Path) -> set[Path]:
    return {path.resolve() for path in root.rglob("rollout-*.jsonl") if path.is_file()}


def _new_session_files(after: set[Path], before: set[Path]) -> list[Path]:
    return sorted(path for path in after if path not in before)


def _session_item(path: Path) -> dict[str, Any]:
    return {
        "path": str(path),
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "mtime": path.stat().st_mtime,
    }


def _cleanup_session_files(paths: list[Path], sessions_root: Path) -> list[dict[str, Any]]:
    cleanup: list[dict[str, Any]] = []
    root = sessions_root.resolve()
    for path in paths:
        item: dict[str, Any] = {"path": str(path), "deleted": False}
        try:
            resolved = path.resolve()
            if root != resolved and root not in resolved.parents:
                item["error"] = "outside_sessions_root"
            elif resolved.exists() and resolved.is_file():
                resolved.unlink()
                item["deleted"] = True
                _cleanup_empty_parents(resolved.parent, root)
            else:
                item["deleted"] = True
                item["already_missing"] = True
        except OSError as exc:
            item["error"] = exc.__class__.__name__
        cleanup.append(item)
    return cleanup


def _cleanup_new_session_files(sessions_root: Path, before: set[Path]) -> list[dict[str, Any]]:
    after = _rollout_files(sessions_root)
    return _cleanup_session_files(_new_session_files(after, before), sessions_root)


def _cleanup_empty_parents(start: Path, stop: Path) -> None:
    current = start
    while current != stop and stop in current.parents:
        try:
            current.rmdir()
        except OSError:
            break
        current = current.parent


def _tail(text: str, max_chars: int = 500) -> str:
    clean = (text or "").strip().replace("\r", "")
    if not clean:
        return "no stderr"
    return clean[-max_chars:]


def _decode_stream(data: bytes | str) -> str:
    if isinstance(data, str):
        return data
    return data.decode("utf-8", errors="replace")
