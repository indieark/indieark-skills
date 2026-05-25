"""Local creative project store for Video Gen Pro workflows."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from seedance2.constants import DEFAULT_PROJECT_ROOT, EXIT_CONFIG, EXIT_USAGE
from seedance2.errors import SeedanceError
from seedance2.http import is_http_url


SCHEMA_VERSION = 1
ASSET_TYPES = ("character", "scene")
ASSET_CONTAINERS = {"character": "characters", "scene": "scenes"}


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def projects_root(args: argparse.Namespace | None = None) -> Path:
    configured = getattr(args, "projects_dir", None) if args else None
    return Path(configured or DEFAULT_PROJECT_ROOT).expanduser()


def clean_id(value: str, *, prefix: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip()).strip("-._").lower()
    if not value:
        value = prefix
    if not value.startswith(f"{prefix}-"):
        value = f"{prefix}-{value}"
    return value[:80]


def new_id(prefix: str, label: str | None = None) -> str:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    if label:
        suffix = clean_id(label, prefix=prefix).removeprefix(f"{prefix}-")
        return clean_id(f"{timestamp}-{suffix}", prefix=prefix)
    return f"{prefix}-{timestamp}"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SeedanceError(
            f"invalid project JSON: {path}",
            code=EXIT_CONFIG,
            payload={"error": str(exc)},
        )


def read_text_file(path_text: str, *, label: str) -> str:
    path = Path(path_text).expanduser()
    if not path.is_file():
        raise SeedanceError(f"{label} file not found: {path_text}", code=EXIT_USAGE)
    try:
        text = path.read_text(encoding="utf-8-sig").rstrip("\r\n")
    except UnicodeDecodeError as exc:
        raise SeedanceError(
            f"{label} file must be UTF-8: {path_text}",
            code=EXIT_USAGE,
            payload={"error": str(exc)},
        )
    if not text.strip():
        raise SeedanceError(f"{label} file is empty: {path_text}", code=EXIT_USAGE)
    return text


def normalized_list(values: list[str] | tuple[str, ...] | None) -> list[str]:
    if not values:
        return []
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = value.strip()
        key = text.casefold()
        if text and key not in seen:
            result.append(text)
            seen.add(key)
    return result


def text_matches(value: Any, needle: str) -> bool:
    if value is None:
        return False
    if isinstance(value, dict):
        return any(text_matches(item, needle) for item in value.values())
    if isinstance(value, list):
        return any(text_matches(item, needle) for item in value)
    return needle in str(value).casefold()


class ProjectStore:
    def __init__(self, root: Path):
        self.root = root

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "ProjectStore":
        return cls(projects_root(args))

    def project_dir(self, project_id: str) -> Path:
        return self.root / project_id

    def project_file(self, project_id: str) -> Path:
        return self.project_dir(project_id) / "project.json"

    def require_project(self, project_id: str) -> dict[str, Any]:
        path = self.project_file(project_id)
        if not path.is_file():
            raise SeedanceError(
                f"project not found: {project_id}",
                code=EXIT_USAGE,
                payload={"projects_dir": str(self.root)},
            )
        return read_json(path)

    def save_project(self, data: dict[str, Any]) -> None:
        data["updated_at"] = now_iso()
        write_json(self.project_file(data["project_id"]), data)

    def create_project(
        self,
        *,
        intent: str,
        title: str | None,
        project_id: str | None,
        platform: str | None,
        ratio: str | None,
        duration: int | None,
        notes: str | None,
    ) -> dict[str, Any]:
        pid = clean_id(project_id, prefix="proj") if project_id else new_id("proj", title or intent)
        path = self.project_file(pid)
        if path.exists():
            raise SeedanceError(f"project already exists: {pid}", code=EXIT_USAGE)
        now = now_iso()
        data: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "project_id": pid,
            "title": title or intent[:60],
            "intent": intent,
            "platform": platform,
            "ratio": ratio,
            "duration": duration,
            "notes": notes,
            "created_at": now,
            "updated_at": now,
            "assets": {"characters": [], "scenes": []},
            "script": None,
            "style": None,
            "storyboards": [],
            "generations": [],
        }
        write_json(path, data)
        return {"ok": True, "project": data, "project_path": str(path)}

    def list_projects(self) -> dict[str, Any]:
        projects = []
        if self.root.exists():
            for path in sorted(self.root.glob("*/project.json")):
                data = read_json(path)
                projects.append({
                    "project_id": data.get("project_id"),
                    "title": data.get("title"),
                    "intent": data.get("intent"),
                    "updated_at": data.get("updated_at"),
                    "path": str(path.parent),
                    "storyboards": len(data.get("storyboards") or []),
                    "generations": len(data.get("generations") or []),
                })
        return {"ok": True, "projects_dir": str(self.root), "projects": projects}

    def show_project(self, project_id: str) -> dict[str, Any]:
        data = self.require_project(project_id)
        return {
            "ok": True,
            "project": data,
            "project_path": str(self.project_file(project_id)),
        }

    def add_asset(
        self,
        *,
        project_id: str,
        asset_type: str,
        name: str,
        file_path: str | None,
        source: str | None,
        asset_id: str | None,
        purpose: str | None,
        description: str | None,
        role: str | None,
        tags: list[str] | None,
        aliases: list[str] | None,
    ) -> dict[str, Any]:
        if asset_type not in ASSET_TYPES:
            raise SeedanceError(
                f"asset type must be one of: {', '.join(ASSET_TYPES)}",
                code=EXIT_USAGE,
            )
        if bool(file_path) == bool(source):
            raise SeedanceError(
                "provide exactly one of --file or --source",
                code=EXIT_USAGE,
            )
        project = self.require_project(project_id)
        prefix = "char" if asset_type == "character" else "scene"
        aid = clean_id(asset_id, prefix=prefix) if asset_id else new_id(prefix, name)
        container = ASSET_CONTAINERS[asset_type]
        asset_dir = self.project_dir(project_id) / container / aid
        image_dir = asset_dir / "images"
        if (asset_dir / "asset.json").exists():
            raise SeedanceError(f"asset already exists: {aid}", code=EXIT_USAGE)
        material = self._material_record(
            file_path=file_path,
            source=source,
            target_dir=image_dir,
            label="asset",
        )
        now = now_iso()
        data = {
            "schema_version": SCHEMA_VERSION,
            "project_id": project_id,
            "asset_id": aid,
            "type": asset_type,
            "name": name,
            "purpose": purpose,
            "description": description,
            "role": role,
            "tags": normalized_list(tags),
            "aliases": normalized_list(aliases),
            "material": material,
            "created_at": now,
            "updated_at": now,
        }
        write_json(asset_dir / "asset.json", data)
        project["assets"].setdefault(container, [])
        if aid not in project["assets"][container]:
            project["assets"][container].append(aid)
        self.save_project(project)
        return {
            "ok": True,
            "project_id": project_id,
            "asset": data,
            "asset_path": str(asset_dir / "asset.json"),
        }

    def list_assets(
        self,
        project_id: str,
        asset_type: str | None = None,
        *,
        query: str | None = None,
        tags: list[str] | None = None,
        role: str | None = None,
        source_type: str | None = None,
    ) -> dict[str, Any]:
        self.require_project(project_id)
        assets = [
            data
            for _, data, _ in self._iter_assets(project_id=project_id, asset_type=asset_type)
            if self._asset_matches(
                data,
                query=query,
                tags=tags,
                role=role,
                source_type=source_type,
            )
        ]
        return {
            "ok": True,
            "project_id": project_id,
            "filters": self._asset_filters(
                asset_type=asset_type,
                query=query,
                tags=tags,
                role=role,
                source_type=source_type,
            ),
            "assets": assets,
        }

    def show_asset(
        self,
        project_id: str,
        asset_id: str,
        asset_type: str | None = None,
    ) -> dict[str, Any]:
        self.require_project(project_id)
        for _, data, path in self._iter_assets(project_id=project_id, asset_type=asset_type):
            if data.get("asset_id") == asset_id:
                return {
                    "ok": True,
                    "project_id": project_id,
                    "asset": data,
                    "asset_path": str(path),
                }
        raise SeedanceError(
            f"asset not found: {asset_id}",
            code=EXIT_USAGE,
            payload={"project_id": project_id},
        )

    def search_assets(
        self,
        *,
        project_id: str | None = None,
        asset_type: str | None = None,
        query: str | None = None,
        tags: list[str] | None = None,
        role: str | None = None,
        source_type: str | None = None,
    ) -> dict[str, Any]:
        assets = [
            data
            for _, data, _ in self._iter_assets(project_id=project_id, asset_type=asset_type)
            if self._asset_matches(
                data,
                query=query,
                tags=tags,
                role=role,
                source_type=source_type,
            )
        ]
        return {
            "ok": True,
            "projects_dir": str(self.root),
            "filters": self._asset_filters(
                project_id=project_id,
                asset_type=asset_type,
                query=query,
                tags=tags,
                role=role,
                source_type=source_type,
            ),
            "assets": assets,
        }

    def reuse_asset(
        self,
        *,
        target_project_id: str,
        source_project_id: str,
        source_asset_id: str,
        asset_type: str | None,
        new_asset_id: str | None,
        name: str | None,
        purpose: str | None,
        description: str | None,
        role: str | None,
        tags: list[str] | None,
        aliases: list[str] | None,
    ) -> dict[str, Any]:
        source_result = self.show_asset(source_project_id, source_asset_id, asset_type)
        source_asset = source_result["asset"]
        resolved_type = source_asset.get("type") or asset_type
        if resolved_type not in ASSET_TYPES:
            raise SeedanceError(
                f"source asset has unknown type: {resolved_type}",
                code=EXIT_USAGE,
            )

        material = source_asset.get("material") or {}
        file_path: str | None = None
        source: str | None = None
        if material.get("source_type") == "local_file":
            candidate = material.get("stored_path") or material.get("original_path")
            if not candidate or not Path(candidate).expanduser().is_file():
                raise SeedanceError(
                    "source local asset file is missing; cannot reuse it safely",
                    code=EXIT_USAGE,
                    payload={
                        "source_project_id": source_project_id,
                        "source_asset_id": source_asset_id,
                        "candidate": candidate,
                    },
                )
            file_path = candidate
        else:
            source = material.get("source")
            if not source:
                raise SeedanceError(
                    "source asset does not contain a reusable material source",
                    code=EXIT_USAGE,
                    payload={
                        "source_project_id": source_project_id,
                        "source_asset_id": source_asset_id,
                    },
                )

        combined_tags = normalized_list(
            [str(tag) for tag in source_asset.get("tags", [])] + normalized_list(tags)
        )
        combined_aliases = normalized_list(
            [str(alias) for alias in source_asset.get("aliases", [])]
            + normalized_list(aliases)
        )
        result = self.add_asset(
            project_id=target_project_id,
            asset_type=resolved_type,
            name=name or source_asset.get("name") or source_asset_id,
            file_path=file_path,
            source=source,
            asset_id=new_asset_id or source_asset_id,
            purpose=purpose if purpose is not None else source_asset.get("purpose"),
            description=(
                description if description is not None else source_asset.get("description")
            ),
            role=role if role is not None else source_asset.get("role"),
            tags=combined_tags,
            aliases=combined_aliases,
        )
        reused_from = {
            "source_project_id": source_project_id,
            "source_project_title": source_asset.get("project_title"),
            "source_asset_id": source_asset_id,
            "source_asset_name": source_asset.get("name"),
            "source_asset_path": source_result.get("asset_path"),
            "source_material_type": material.get("source_type"),
            "source_material_sha256": material.get("sha256"),
            "reused_at": now_iso(),
        }
        asset = result["asset"]
        asset["reused_from"] = reused_from
        asset["updated_at"] = reused_from["reused_at"]
        write_json(Path(result["asset_path"]), asset)
        result["asset"] = asset
        result["reused_from"] = reused_from
        return result

    def _iter_assets(
        self,
        *,
        project_id: str | None = None,
        asset_type: str | None = None,
    ) -> list[tuple[dict[str, Any], dict[str, Any], Path]]:
        project_paths: list[Path]
        if project_id:
            project = self.require_project(project_id)
            project_paths = [self.project_file(project["project_id"])]
        elif self.root.exists():
            project_paths = sorted(self.root.glob("*/project.json"))
        else:
            project_paths = []
        types = ASSET_TYPES if asset_type is None else (asset_type,)
        for kind in types:
            if kind not in ASSET_TYPES:
                raise SeedanceError(f"unknown asset type: {kind}", code=EXIT_USAGE)
        assets = []
        for project_path in project_paths:
            project = read_json(project_path)
            pid = project.get("project_id") or project_path.parent.name
            for kind in types:
                container = ASSET_CONTAINERS[kind]
                for path in sorted((self.project_dir(pid) / container).glob("*/asset.json")):
                    assets.append((project, self._asset_with_context(path, project, kind), path))
        return assets

    def _asset_with_context(
        self,
        path: Path,
        project: dict[str, Any],
        fallback_type: str,
    ) -> dict[str, Any]:
        data = read_json(path)
        data.setdefault("schema_version", SCHEMA_VERSION)
        data.setdefault("project_id", project.get("project_id") or path.parents[2].name)
        data.setdefault("type", fallback_type)
        data.setdefault("tags", [])
        data.setdefault("aliases", [])
        data.setdefault("role", None)
        data["project_title"] = project.get("title")
        data["asset_path"] = str(path)
        return data

    def _asset_matches(
        self,
        data: dict[str, Any],
        *,
        query: str | None,
        tags: list[str] | None,
        role: str | None,
        source_type: str | None,
    ) -> bool:
        if source_type and (data.get("material") or {}).get("source_type") != source_type:
            return False
        if role and (data.get("role") or "").casefold() != role.casefold():
            return False
        wanted_tags = {tag.casefold() for tag in normalized_list(tags)}
        if wanted_tags:
            actual_tags = {str(tag).casefold() for tag in data.get("tags", [])}
            if not wanted_tags.issubset(actual_tags):
                return False
        if query:
            searchable = {
                "project_id": data.get("project_id"),
                "project_title": data.get("project_title"),
                "asset_id": data.get("asset_id"),
                "type": data.get("type"),
                "name": data.get("name"),
                "purpose": data.get("purpose"),
                "description": data.get("description"),
                "role": data.get("role"),
                "tags": data.get("tags"),
                "aliases": data.get("aliases"),
                "material": data.get("material"),
            }
            if not text_matches(searchable, query.casefold()):
                return False
        return True

    def _asset_filters(
        self,
        *,
        project_id: str | None = None,
        asset_type: str | None = None,
        query: str | None = None,
        tags: list[str] | None = None,
        role: str | None = None,
        source_type: str | None = None,
    ) -> dict[str, Any]:
        return {
            "project_id": project_id,
            "type": asset_type,
            "query": query,
            "tags": normalized_list(tags),
            "role": role,
            "source_type": source_type,
        }

    def set_text_artifact(
        self,
        *,
        project_id: str,
        kind: str,
        text: str,
        source_file: str | None,
    ) -> dict[str, Any]:
        if kind not in {"script", "style"}:
            raise SeedanceError(f"unknown text artifact kind: {kind}", code=EXIT_USAGE)
        project = self.require_project(project_id)
        path = self.project_dir(project_id) / f"{kind}.md"
        path.write_text(text.rstrip("\r\n") + "\n", encoding="utf-8")
        record = {
            "path": str(path),
            "sha256": sha256_text(text.rstrip("\r\n")),
            "source_file": source_file,
            "updated_at": now_iso(),
        }
        project[kind] = record
        self.save_project(project)
        return {"ok": True, "project_id": project_id, kind: record}

    def show_text_artifact(self, project_id: str, kind: str) -> dict[str, Any]:
        self.require_project(project_id)
        path = self.project_dir(project_id) / f"{kind}.md"
        if not path.is_file():
            raise SeedanceError(f"{kind} not found for project: {project_id}", code=EXIT_USAGE)
        return {
            "ok": True,
            "project_id": project_id,
            kind: path.read_text(encoding="utf-8"),
            "path": str(path),
        }

    def plan_storyboard(
        self,
        *,
        project_id: str,
        storyboard_id: str | None,
        layout: str,
        notes: str | None,
    ) -> dict[str, Any]:
        project = self.require_project(project_id)
        sid = clean_id(storyboard_id, prefix="sb") if storyboard_id else new_id("sb", project.get("title"))
        storyboard_dir = self.storyboard_dir(project_id, sid)
        if storyboard_dir.exists():
            raise SeedanceError(f"storyboard already exists: {sid}", code=EXIT_USAGE)
        storyboard_dir.mkdir(parents=True, exist_ok=True)
        plan = {
            "schema_version": SCHEMA_VERSION,
            "storyboard_id": sid,
            "project_id": project_id,
            "layout": layout,
            "status": "planned",
            "notes": notes,
            "created_at": now_iso(),
            "inputs": self._project_snapshot(project_id, project),
            "next_actions": [
                "write storyboard-prompt.txt",
                "create or provide storyboard-image",
                "write video-prompt.txt",
                "run storyboard add, then storyboard approve",
            ],
        }
        write_json(storyboard_dir / "storyboard-plan.json", plan)
        prompt_text = self._storyboard_prompt_scaffold(project, layout, notes)
        (storyboard_dir / "storyboard-prompt.txt").write_text(prompt_text, encoding="utf-8")
        if sid not in project.get("storyboards", []):
            project.setdefault("storyboards", []).append(sid)
            self.save_project(project)
        return {
            "ok": True,
            "project_id": project_id,
            "storyboard_id": sid,
            "storyboard_dir": str(storyboard_dir),
            "plan_path": str(storyboard_dir / "storyboard-plan.json"),
            "storyboard_prompt_path": str(storyboard_dir / "storyboard-prompt.txt"),
            "status": "planned",
        }

    def add_storyboard(
        self,
        *,
        project_id: str,
        storyboard_id: str | None,
        image: str,
        prompt_file: str,
        video_prompt_file: str,
        layout: str | None,
        notes: str | None,
    ) -> dict[str, Any]:
        project = self.require_project(project_id)
        sid = clean_id(storyboard_id, prefix="sb") if storyboard_id else new_id("sb", project.get("title"))
        storyboard_dir = self.storyboard_dir(project_id, sid)
        storyboard_dir.mkdir(parents=True, exist_ok=True)
        storyboard_prompt = read_text_file(prompt_file, label="storyboard prompt")
        video_prompt = read_text_file(video_prompt_file, label="video prompt")
        (storyboard_dir / "storyboard-prompt.txt").write_text(storyboard_prompt + "\n", encoding="utf-8")
        (storyboard_dir / "video-prompt.txt").write_text(video_prompt + "\n", encoding="utf-8")
        material = self._material_record(
            file_path=None if is_external_source(image) else image,
            source=image if is_external_source(image) else None,
            target_dir=storyboard_dir,
            label="storyboard-image",
        )
        now = now_iso()
        data = {
            "schema_version": SCHEMA_VERSION,
            "storyboard_id": sid,
            "project_id": project_id,
            "layout": layout,
            "status": "ready",
            "approved": False,
            "notes": notes,
            "image": material,
            "storyboard_prompt": {
                "path": str(storyboard_dir / "storyboard-prompt.txt"),
                "sha256": sha256_text(storyboard_prompt),
            },
            "video_prompt": {
                "path": str(storyboard_dir / "video-prompt.txt"),
                "sha256": sha256_text(video_prompt),
            },
            "created_at": now,
            "updated_at": now,
        }
        write_json(storyboard_dir / "storyboard.json", data)
        if sid not in project.get("storyboards", []):
            project.setdefault("storyboards", []).append(sid)
            self.save_project(project)
        return {
            "ok": True,
            "project_id": project_id,
            "storyboard": data,
            "storyboard_path": str(storyboard_dir / "storyboard.json"),
        }

    def storyboard_dir(self, project_id: str, storyboard_id: str) -> Path:
        return self.project_dir(project_id) / "storyboards" / storyboard_id

    def storyboard_file(self, project_id: str, storyboard_id: str) -> Path:
        return self.storyboard_dir(project_id, storyboard_id) / "storyboard.json"

    def load_storyboard(self, project_id: str, storyboard_id: str) -> dict[str, Any]:
        self.require_project(project_id)
        path = self.storyboard_file(project_id, storyboard_id)
        if not path.is_file():
            plan = self.storyboard_dir(project_id, storyboard_id) / "storyboard-plan.json"
            if plan.is_file():
                data = read_json(plan)
                data["storyboard_path"] = str(plan)
                return data
            raise SeedanceError(
                f"storyboard not found: {storyboard_id}",
                code=EXIT_USAGE,
                payload={"project_id": project_id},
            )
        data = read_json(path)
        data["storyboard_path"] = str(path)
        return data

    def approve_storyboard(
        self,
        *,
        project_id: str,
        storyboard_id: str,
        approved_by: str | None,
        notes: str | None,
    ) -> dict[str, Any]:
        data = self.load_storyboard(project_id, storyboard_id)
        if data.get("status") == "planned":
            raise SeedanceError(
                "storyboard plan has no image/video prompt yet; run storyboard add first",
                code=EXIT_USAGE,
            )
        approval = {
            "approved": True,
            "approved_at": now_iso(),
            "approved_by": approved_by,
            "notes": notes,
        }
        data["approved"] = True
        data["status"] = "approved"
        data["approval"] = approval
        data["updated_at"] = approval["approved_at"]
        write_json(self.storyboard_file(project_id, storyboard_id), data)
        write_json(self.storyboard_dir(project_id, storyboard_id) / "approval.json", approval)
        return {"ok": True, "project_id": project_id, "storyboard": data}

    def generation_dir(self, project_id: str, run_id: str) -> Path:
        return self.project_dir(project_id) / "generations" / run_id

    def generations_root(self, project_id: str) -> Path:
        return self.project_dir(project_id) / "generations"

    def project_context(
        self,
        project_id: str,
        storyboard_id: str | None,
        *,
        allow_unapproved: bool = False,
    ) -> dict[str, Any]:
        project = self.require_project(project_id)
        storyboard = None
        if storyboard_id:
            storyboard = self.load_storyboard(project_id, storyboard_id)
            if storyboard.get("status") == "planned":
                raise SeedanceError(
                    "storyboard is only planned; add image and prompts before generation",
                    code=EXIT_USAGE,
                )
            if not storyboard.get("approved") and not allow_unapproved:
                raise SeedanceError(
                    "storyboard is not approved; run storyboard approve or pass --allow-unapproved-storyboard",
                    code=EXIT_CONFIG,
                )
        return {
            "project_id": project_id,
            "project_title": project.get("title"),
            "project_path": str(self.project_file(project_id)),
            "storyboard_id": storyboard_id,
            "storyboard": storyboard,
        }

    def write_generation_record(
        self,
        *,
        context: dict[str, Any],
        run_id: str,
        mode: str,
        stage: str,
        artifacts: dict[str, Any],
        result: dict[str, Any],
    ) -> dict[str, Any]:
        project_id = context["project_id"]
        project = self.require_project(project_id)
        record = {
            "schema_version": SCHEMA_VERSION,
            "project_id": project_id,
            "storyboard_id": context.get("storyboard_id"),
            "run_id": run_id,
            "mode": mode,
            "stage": stage,
            "updated_at": now_iso(),
            "run_dir": artifacts.get("run_dir"),
            "artifacts": {
                "prompt_path": artifacts.get("manifest", {}).get("prompt", {}).get("path"),
                "payload_path": artifacts.get("payload_path"),
                "manifest_path": artifacts.get("manifest_path"),
                "generation_log_path": artifacts.get("generation_log_path"),
                "project_generation_path": str(Path(artifacts["run_dir"]) / "project-generation.json"),
                "submit_summary_path": str(Path(artifacts["run_dir"]) / "submit-summary.json"),
                "task_result_path": str(Path(artifacts["run_dir"]) / "task-result.json"),
            },
            "task_id": result.get("task_id") or result.get("created", {}).get("task_id"),
            "status": result.get("status"),
            "dry_run": bool(result.get("dry_run")),
        }
        target_dir = self.generation_dir(project_id, run_id)
        target_dir.mkdir(parents=True, exist_ok=True)
        write_json(target_dir / "generation-record.json", record)
        write_json(Path(artifacts["run_dir"]) / "project-generation.json", record)
        generations = project.setdefault("generations", [])
        if run_id not in generations:
            generations.append(run_id)
            self.save_project(project)
        return record

    def list_generations(self, project_id: str) -> dict[str, Any]:
        self.require_project(project_id)
        records = []
        root = self.generations_root(project_id)
        if root.exists():
            for path in sorted(root.glob("*/generation-record.json")):
                data = read_json(path)
                data["record_path"] = str(path)
                records.append(data)
        return {"ok": True, "project_id": project_id, "generations": records}

    def show_generation(self, project_id: str, run_id: str) -> dict[str, Any]:
        self.require_project(project_id)
        path = self.generation_dir(project_id, run_id) / "generation-record.json"
        if not path.is_file():
            raise SeedanceError(f"generation not found: {run_id}", code=EXIT_USAGE)
        return {
            "ok": True,
            "project_id": project_id,
            "generation": read_json(path),
            "record_path": str(path),
        }

    def _material_record(
        self,
        *,
        file_path: str | None,
        source: str | None,
        target_dir: Path,
        label: str,
    ) -> dict[str, Any]:
        if file_path:
            path = Path(file_path).expanduser()
            if not path.is_file():
                raise SeedanceError(f"{label} file not found: {file_path}", code=EXIT_USAGE)
            target_dir.mkdir(parents=True, exist_ok=True)
            dest = target_dir / path.name
            if dest.exists():
                dest = target_dir / f"{dest.stem}-{datetime.now().strftime('%H%M%S')}{dest.suffix}"
            shutil.copy2(path, dest)
            return {
                "source_type": "local_file",
                "original_path": str(path.resolve()),
                "stored_path": str(dest.resolve()),
                "sha256": sha256_file(dest),
                "size_bytes": dest.stat().st_size,
            }
        if not source:
            raise SeedanceError(f"{label} source is required", code=EXIT_USAGE)
        if not is_http_url(source) and not source.startswith(("asset://", "data:")):
            raise SeedanceError(
                f"{label} source must be a local file, HTTP(S), asset://, or data URI",
                code=EXIT_USAGE,
            )
        return {"source_type": "external", "source": source}

    def _project_snapshot(self, project_id: str, project: dict[str, Any]) -> dict[str, Any]:
        return {
            "project_id": project_id,
            "title": project.get("title"),
            "intent": project.get("intent"),
            "ratio": project.get("ratio"),
            "duration": project.get("duration"),
            "script": project.get("script"),
            "style": project.get("style"),
            "characters": project.get("assets", {}).get("characters", []),
            "scenes": project.get("assets", {}).get("scenes", []),
        }

    def _storyboard_prompt_scaffold(
        self,
        project: dict[str, Any],
        layout: str,
        notes: str | None,
    ) -> str:
        return (
            f"项目：{project.get('title')}\n"
            f"原始意图：{project.get('intent')}\n"
            f"故事板布局：{layout}\n"
            f"画幅：{project.get('ratio') or '待定'}；时长：{project.get('duration') or '待定'}\n"
            f"补充说明：{notes or '无'}\n\n"
            "请生成视觉故事板母图提示词：明确角色外观、场景空间、镜头顺序、"
            "关键动作、光线色彩、连续性约束和每格用途。\n"
        )


def storyboard_image_source(storyboard: dict[str, Any]) -> str:
    image = storyboard.get("image") or {}
    return image.get("stored_path") or image.get("source") or ""


def is_external_source(value: str) -> bool:
    return is_http_url(value) or value.startswith(("asset://", "data:"))


def storyboard_video_prompt(storyboard: dict[str, Any]) -> str:
    prompt = storyboard.get("video_prompt") or {}
    path = prompt.get("path")
    if not path:
        return ""
    return Path(path).read_text(encoding="utf-8").rstrip("\r\n")
