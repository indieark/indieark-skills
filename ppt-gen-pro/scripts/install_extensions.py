from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXTENSIONS_DIR = ROOT / "extensions"
FRESHNESS_DAYS = 90


@dataclass(frozen=True)
class Extension:
    route: str
    name: str
    repo: str
    path: Path
    skill_entry: str = "SKILL.md"
    required_paths: tuple[str, ...] = ("SKILL.md", "README.md", "references")
    locked_commit: str | None = None  # None / "" means follow upstream default branch
    verified_date: str | None = None  # YYYY-MM-DD; None means never verified


EXTENSIONS = [
    Extension(
        route="image-first-ppt",
        name="ppt-image-first",
        repo="https://github.com/NyxTides/ppt-image-first",
        path=EXTENSIONS_DIR / "ppt-image-first",
    ),
    Extension(
        route="web-html-ppt",
        name="guizang-ppt-skill",
        repo="https://github.com/op7418/guizang-ppt-skill",
        path=EXTENSIONS_DIR / "guizang-ppt-skill",
    ),
    Extension(
        route="svg-ppt",
        name="ppt-master",
        repo="https://github.com/hugohe3/ppt-master",
        path=EXTENSIONS_DIR / "ppt-master",
        skill_entry="skills/ppt-master/SKILL.md",
        required_paths=("README.md", "skills/ppt-master/SKILL.md", "skills/ppt-master/references"),
    ),
    Extension(
        route="academic-image-ppt",
        name="literature-report-ppt-builder",
        repo="https://github.com/fangyuanopus/literature-report-ppt-builder",
        path=EXTENSIONS_DIR / "literature-report-ppt-builder",
        skill_entry="academic-slide-minimalist/SKILL.md",
        required_paths=(
            "README.md",
            "academic-slide-minimalist/SKILL.md",
            "academic-slide-minimalist/references",
        ),
        locked_commit="8fe01a4",
        verified_date="2026-05-25",
    ),
    Extension(
        route="design-html-ppt",
        name="huashu-design",
        repo="https://github.com/alchaincyf/huashu-design",
        path=EXTENSIONS_DIR / "huashu-design",
        locked_commit="9100be3",
        verified_date="2026-05-25",
    ),
    Extension(
        route="video-html-ppt",
        name="garden-skills",
        repo="https://github.com/ConardLi/garden-skills",
        path=EXTENSIONS_DIR / "garden-skills",
        skill_entry="skills/web-video-presentation/SKILL.md",
        required_paths=(
            "README.md",
            "skills/web-video-presentation/SKILL.md",
            "skills/web-video-presentation/references",
        ),
        locked_commit="ea0c0c8",
        verified_date="2026-05-25",
    ),
]


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


def inspect_extension(ext: Extension) -> dict[str, object]:
    missing = [item for item in ext.required_paths if not (ext.path / item).exists()]
    commit = None
    if (ext.path / ".git").exists():
        result = run(["git", "rev-parse", "--short", "HEAD"], cwd=ext.path)
        if result.returncode == 0:
            commit = result.stdout.strip()
    days = freshness_days(ext.verified_date)
    return {
        "route": ext.route,
        "name": ext.name,
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


def install_or_update(ext: Extension, *, check_only: bool, locked: bool) -> dict[str, object]:
    if check_only:
        return inspect_extension(ext)

    if shutil.which("git") is None:
        raise RuntimeError("git is required to install ppt-gen-pro extensions")

    EXTENSIONS_DIR.mkdir(parents=True, exist_ok=True)

    target_commit = ext.locked_commit if locked else None

    if not ext.path.exists():
        if target_commit:
            # Full clone so we can checkout an arbitrary historical commit.
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
        # Default behaviour: follow upstream default branch via git pull --ff-only.
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
                    "route": item["route"],
                    "level": "WARN",
                    "reason": "unverified",
                    "message": f"{item['route']} has no verified_date; run end-to-end verification and update EXTENSIONS",
                }
            )
            continue
        if item.get("stale"):
            warnings.append(
                {
                    "route": item["route"],
                    "level": "WARN",
                    "reason": "stale",
                    "message": (
                        f"{item['route']} verified_date={item['verified_date']} is "
                        f"{item['freshness_days']} days old (> {FRESHNESS_DAYS}); re-verify before delegating"
                    ),
                }
            )
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Install, update, or check ppt-gen-pro route extensions.")
    parser.add_argument("--route", choices=[ext.route for ext in EXTENSIONS], help="Install/check one route only.")
    parser.add_argument("--check-only", action="store_true", help="Only inspect local extension state.")
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
        help="Report routes whose verified_date is missing or > 90 days old (stderr WARNING, exit 0).",
    )
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    if args.locked and args.update_lock:
        parser.error("--locked and --update-lock are mutually exclusive")
    if args.update_lock and args.check_only:
        parser.error("--update-lock cannot be combined with --check-only")

    selected = [ext for ext in EXTENSIONS if args.route in (None, ext.route)]
    results: list[dict[str, object]] = []
    errors: list[dict[str, str]] = []

    for ext in selected:
        try:
            results.append(install_or_update(ext, check_only=args.check_only, locked=args.locked))
        except RuntimeError as exc:
            errors.append({"route": ext.route, "error": str(exc)})

    warnings = check_freshness(results) if args.check_freshness else []

    payload = {
        "ok": not errors and all(bool(item["ok"]) for item in results),
        "results": results,
        "errors": errors,
        "warnings": warnings,
    }

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for item in results:
            status = "OK" if item["ok"] else "MISSING"
            print(f"{status} {item['route']} {item['path']}")
            print(f"  skill_entry: {item['skill_entry']}")
            if item["missing"]:
                print(f"  missing: {', '.join(item['missing'])}")
            if item["commit"]:
                print(f"  commit: {item['commit']}")
            if item["locked_commit"]:
                print(f"  locked_commit: {item['locked_commit']}")
            if item["verified_date"]:
                age = item["freshness_days"]
                print(f"  verified_date: {item['verified_date']} ({age} days ago)")
        for warn in warnings:
            print(f"WARN {warn['route']}: {warn['message']}", file=sys.stderr)
        for error in errors:
            print(f"ERROR {error['route']}: {error['error']}", file=sys.stderr)

    if args.update_lock and not errors:
        print()
        print("Update EXTENSIONS in scripts/install_extensions.py with the following:")
        for item in results:
            if item.get("commit"):
                today = date.today().strftime("%Y-%m-%d")
                print(
                    f"  {item['route']}: locked_commit=\"{item['commit']}\", verified_date=\"{today}\""
                )
        print("Then mirror locked_commit + verified_date into "
              "skills/ppt-gen-pro/references/extensions.md.")

    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
