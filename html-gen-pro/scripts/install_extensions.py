"""Install / update / check html-gen-pro extension checkouts.

Two physical extensions are registered:

- `ui-ux-pro-max`: serves `landing-page`, `app-frontend`, `style-mockup` —
  single-Skill collection providing 67 styles / 161 palettes / 57 font
  pairings / 161 industry rules / 99 UX guidelines.
- `taste-skill`: serves `style-mockup` only — multi-child-Skill repo with
  brutalist / swiss / luxury(soft) style coverage. Other child Skills
  (redesign-skill / brandkit) remain in boundary.md §6 relay mode.

`existing-project-optimize` is intentionally unbound (no extension).

The EXTENSIONS list below is the single source of truth — mirror any
changes to references/extensions.md.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXTENSIONS_DIR = ROOT / "extensions"
FRESHNESS_DAYS = 90
MIN_PYTHON = (3, 9)


@dataclass(frozen=True)
class Extension:
    install_name: str
    repo: str
    path: Path
    routes: tuple[str, ...]
    skill_entry: str = "SKILL.md"
    required_paths: tuple[str, ...] = ("SKILL.md", "README.md")
    locked_commit: str | None = None
    verified_date: str | None = None


EXTENSIONS = [
    Extension(
        install_name="ui-ux-pro-max",
        repo="https://github.com/nextlevelbuilder/ui-ux-pro-max-skill",
        path=EXTENSIONS_DIR / "ui-ux-pro-max",
        routes=("landing-page", "app-frontend", "style-mockup"),
        # Upstream entry file is CLAUDE.md (multi-skill collection — actual
        # search command lives in src/ui-ux-pro-max/scripts/search.py).
        skill_entry="CLAUDE.md",
        required_paths=("CLAUDE.md", "README.md", "skill.json"),
        locked_commit="b7e3af8",
        verified_date="2026-05-26",
    ),
    Extension(
        install_name="taste-skill",
        repo="https://github.com/Leonxlnx/taste-skill",
        path=EXTENSIONS_DIR / "taste-skill",
        routes=("style-mockup",),
        # Multi-child-Skill repo; README.md is the registry of child Skills.
        # Concrete child entries live under sub-directories — pick by
        # aesthetic direction at S4 (see references/extensions.md Route
        # Roles for the child-Skill picker).
        # Style-mockup route only: brutalist / swiss / luxury(soft) etc.
        # Other taste-skill child Skills (redesign-skill / brandkit)
        # remain in boundary.md §6 relay mode (Agent guides switch),
        # not extension-fused — keeps existing-project-optimize unbound.
        skill_entry="README.md",
        required_paths=("README.md",),
        locked_commit="3c7017d",
        verified_date="2026-05-27",
    ),
]

ALL_ROUTES = sorted({route for ext in EXTENSIONS for route in ext.routes})
UNBOUND_ROUTES = ("existing-project-optimize",)


def run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True)


def freshness_days(verified_date: str | None) -> int | None:
    if not verified_date:
        return None
    try:
        d = datetime.strptime(verified_date, "%Y-%m-%d").date()
    except ValueError:
        return None
    return (date.today() - d).days


def python_doctor() -> dict[str, object]:
    """Warn-only environment check; never blocks extension install itself."""
    info: dict[str, object] = {
        "found": False,
        "version": None,
        "ok": False,
        "message": "",
    }
    exe = shutil.which("python") or shutil.which("python3")
    if not exe:
        info["message"] = "python executable not found on PATH"
        return info
    info["found"] = True
    result = run([exe, "--version"])
    raw = (result.stdout or result.stderr or "").strip()
    info["version"] = raw or None
    parts = raw.replace("Python", "").strip().split(".")
    try:
        major, minor = int(parts[0]), int(parts[1])
    except (ValueError, IndexError):
        info["message"] = f"could not parse python version: {raw!r}"
        return info
    if (major, minor) < MIN_PYTHON:
        info["message"] = (
            f"python {major}.{minor} detected; recommend >= "
            f"{MIN_PYTHON[0]}.{MIN_PYTHON[1]} for downstream scripts"
        )
        return info
    info["ok"] = True
    info["message"] = f"python {major}.{minor} OK"
    return info


def inspect_extension(ext: Extension) -> dict[str, object]:
    missing = [item for item in ext.required_paths if not (ext.path / item).exists()]
    commit = None
    if (ext.path / ".git").exists():
        result = run(["git", "rev-parse", "--short", "HEAD"], cwd=ext.path)
        if result.returncode == 0:
            commit = result.stdout.strip()
    days = freshness_days(ext.verified_date)
    return {
        "install_name": ext.install_name,
        "routes": list(ext.routes),
        "repo": ext.repo,
        "path": str(ext.path),
        "skill_entry": str(ext.path / ext.skill_entry),
        "installed": ext.path.exists(),
        "missing": missing,
        "commit": commit,
        "locked_commit": ext.locked_commit or None,
        "verified_date": ext.verified_date,
        "freshness_days": days,
        "stale": days is not None and days > FRESHNESS_DAYS,
        "ok": ext.path.exists() and not missing,
    }


def install_or_update(
    ext: Extension, *, check_only: bool, locked: bool
) -> dict[str, object]:
    if check_only:
        return inspect_extension(ext)

    if shutil.which("git") is None:
        raise RuntimeError("git is required to install html-gen-pro extensions")

    EXTENSIONS_DIR.mkdir(parents=True, exist_ok=True)

    target_commit = ext.locked_commit if locked else None

    if not ext.path.exists():
        if target_commit:
            result = run(["git", "clone", ext.repo, str(ext.path)])
        else:
            result = run(["git", "clone", "--depth", "1", ext.repo, str(ext.path)])
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    elif not (ext.path / ".git").exists():
        raise RuntimeError(f"{ext.path} exists but is not a git checkout")

    if target_commit:
        unshallow = run(["git", "rev-parse", "--is-shallow-repository"], cwd=ext.path)
        if unshallow.returncode == 0 and unshallow.stdout.strip() == "true":
            run(["git", "fetch", "--unshallow"], cwd=ext.path)
        else:
            run(["git", "fetch", "--all", "--tags"], cwd=ext.path)
        checkout = run(["git", "checkout", target_commit], cwd=ext.path)
        if checkout.returncode != 0:
            raise RuntimeError(checkout.stderr.strip() or checkout.stdout.strip())
    else:
        pull = run(["git", "pull", "--ff-only"], cwd=ext.path)
        if pull.returncode != 0:
            raise RuntimeError(pull.stderr.strip() or pull.stdout.strip())
    return inspect_extension(ext)


def check_freshness(results: list[dict[str, object]]) -> list[dict[str, object]]:
    warnings: list[dict[str, object]] = []
    for item in results:
        if item.get("verified_date") is None:
            warnings.append(
                {
                    "install_name": item["install_name"],
                    "level": "WARN",
                    "reason": "unverified",
                    "message": (
                        f"{item['install_name']} has no verified_date; "
                        f"run end-to-end verification and update EXTENSIONS"
                    ),
                }
            )
            continue
        if item.get("stale"):
            warnings.append(
                {
                    "install_name": item["install_name"],
                    "level": "WARN",
                    "reason": "stale",
                    "message": (
                        f"{item['install_name']} verified_date="
                        f"{item['verified_date']} is {item['freshness_days']} "
                        f"days old (> {FRESHNESS_DAYS}); re-verify before delegating"
                    ),
                }
            )
    return warnings


def select_extensions(route: str | None) -> list[Extension]:
    if route is None:
        return list(EXTENSIONS)
    if route in UNBOUND_ROUTES:
        return []
    return [ext for ext in EXTENSIONS if route in ext.routes]


def main() -> int:
    choices = ALL_ROUTES + list(UNBOUND_ROUTES)
    parser = argparse.ArgumentParser(
        description="Install, update, or check html-gen-pro route extensions."
    )
    parser.add_argument(
        "--route",
        choices=choices,
        help=(
            "Install/check the extension that serves this route. "
            f"existing-project-optimize is intentionally unbound."
        ),
    )
    parser.add_argument(
        "--check-only", action="store_true", help="Only inspect local extension state."
    )
    parser.add_argument(
        "--locked",
        action="store_true",
        help="Install at EXTENSIONS[].locked_commit instead of upstream default branch.",
    )
    parser.add_argument(
        "--update-lock",
        action="store_true",
        help="Pull latest, then print current commit SHA so it can be written back to EXTENSIONS.",
    )
    parser.add_argument(
        "--check-freshness",
        action="store_true",
        help="Report extensions whose verified_date is missing or > 90 days old (stderr WARNING, exit 0).",
    )
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    if args.locked and args.update_lock:
        parser.error("--locked and --update-lock are mutually exclusive")
    if args.update_lock and args.check_only:
        parser.error("--update-lock cannot be combined with --check-only")

    selected = select_extensions(args.route)
    results: list[dict[str, object]] = []
    errors: list[dict[str, str]] = []

    for ext in selected:
        try:
            results.append(
                install_or_update(ext, check_only=args.check_only, locked=args.locked)
            )
        except RuntimeError as exc:
            errors.append({"install_name": ext.install_name, "error": str(exc)})

    warnings = check_freshness(results) if args.check_freshness else []
    doctor = python_doctor()

    payload = {
        "ok": not errors and all(bool(item["ok"]) for item in results),
        "results": results,
        "errors": errors,
        "warnings": warnings,
        "python": doctor,
        "unbound_routes": list(UNBOUND_ROUTES),
    }

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if args.route in UNBOUND_ROUTES:
            print(
                f"SKIP {args.route}: route is intentionally unbound; no extension to install"
            )
        for item in results:
            status = "OK" if item["ok"] else "MISSING"
            routes = ",".join(item["routes"])  # type: ignore[arg-type]
            print(f"{status} {item['install_name']} (routes: {routes}) {item['path']}")
            print(f"  skill_entry: {item['skill_entry']}")
            if item["missing"]:
                print(f"  missing: {', '.join(item['missing'])}")  # type: ignore[arg-type]
            if item["commit"]:
                print(f"  commit: {item['commit']}")
            if item["locked_commit"]:
                print(f"  locked_commit: {item['locked_commit']}")
            if item["verified_date"]:
                age = item["freshness_days"]
                print(f"  verified_date: {item['verified_date']} ({age} days ago)")
        for warn in warnings:
            print(f"WARN {warn['install_name']}: {warn['message']}", file=sys.stderr)
        for error in errors:
            print(f"ERROR {error['install_name']}: {error['error']}", file=sys.stderr)
        if not doctor.get("ok"):
            print(
                f"WARN python doctor: {doctor.get('message')}",
                file=sys.stderr,
            )

    if args.update_lock and not errors:
        print()
        print("Update EXTENSIONS in scripts/install_extensions.py with the following:")
        for item in results:
            if item.get("commit"):
                today = date.today().strftime("%Y-%m-%d")
                print(
                    f"  {item['install_name']}: locked_commit=\"{item['commit']}\", "
                    f"verified_date=\"{today}\""
                )
        print(
            "Then mirror locked_commit + verified_date into "
            "skills/html-gen-pro/references/extensions.md."
        )

    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
