"""Project asset library subcommands."""

from __future__ import annotations

import argparse

from seedance2.constants import EXIT_USAGE
from seedance2.errors import SeedanceError
from seedance2.project_store import ProjectStore, read_text_file


def _text_from_args(args: argparse.Namespace, *, label: str) -> tuple[str, str | None]:
    if getattr(args, "file", None):
        return read_text_file(args.file, label=label), args.file
    text = getattr(args, "text", None)
    if text is None or not text.strip():
        raise SeedanceError(f"{label} text is empty", code=EXIT_USAGE)
    return text.rstrip("\r\n"), None


def cmd_project_create(args: argparse.Namespace) -> dict:
    store = ProjectStore.from_args(args)
    return store.create_project(
        intent=args.intent,
        title=args.title,
        project_id=args.project_id,
        platform=args.platform,
        ratio=args.ratio,
        duration=args.duration,
        notes=args.notes,
    )


def cmd_project_list(args: argparse.Namespace) -> dict:
    return ProjectStore.from_args(args).list_projects()


def cmd_project_show(args: argparse.Namespace) -> dict:
    return ProjectStore.from_args(args).show_project(args.project_id)


def cmd_asset_add(args: argparse.Namespace) -> dict:
    return ProjectStore.from_args(args).add_asset(
        project_id=args.project_id,
        asset_type=args.type,
        name=args.name,
        file_path=args.file,
        source=args.source,
        asset_id=args.asset_id,
        purpose=args.purpose,
        description=args.description,
        role=args.role,
        tags=args.tag,
        aliases=args.alias,
    )


def cmd_asset_list(args: argparse.Namespace) -> dict:
    return ProjectStore.from_args(args).list_assets(
        args.project_id,
        args.type,
        query=args.query,
        tags=args.tag,
        role=args.role,
        source_type=args.source_type,
    )


def cmd_asset_show(args: argparse.Namespace) -> dict:
    return ProjectStore.from_args(args).show_asset(args.project_id, args.asset_id, args.type)


def cmd_asset_search(args: argparse.Namespace) -> dict:
    return ProjectStore.from_args(args).search_assets(
        project_id=args.project,
        asset_type=args.type,
        query=args.query,
        tags=args.tag,
        role=args.role,
        source_type=args.source_type,
    )


def cmd_asset_reuse(args: argparse.Namespace) -> dict:
    return ProjectStore.from_args(args).reuse_asset(
        target_project_id=args.target_project_id,
        source_project_id=args.source_project_id,
        source_asset_id=args.source_asset_id,
        asset_type=args.type,
        new_asset_id=args.asset_id,
        name=args.name,
        purpose=args.purpose,
        description=args.description,
        role=args.role,
        tags=args.tag,
        aliases=args.alias,
    )


def cmd_script_set(args: argparse.Namespace) -> dict:
    text, source_file = _text_from_args(args, label="script")
    return ProjectStore.from_args(args).set_text_artifact(
        project_id=args.project_id,
        kind="script",
        text=text,
        source_file=source_file,
    )


def cmd_script_show(args: argparse.Namespace) -> dict:
    return ProjectStore.from_args(args).show_text_artifact(args.project_id, "script")


def cmd_style_set(args: argparse.Namespace) -> dict:
    text, source_file = _text_from_args(args, label="style")
    return ProjectStore.from_args(args).set_text_artifact(
        project_id=args.project_id,
        kind="style",
        text=text,
        source_file=source_file,
    )


def cmd_style_show(args: argparse.Namespace) -> dict:
    return ProjectStore.from_args(args).show_text_artifact(args.project_id, "style")


def cmd_storyboard_plan(args: argparse.Namespace) -> dict:
    return ProjectStore.from_args(args).plan_storyboard(
        project_id=args.project_id,
        storyboard_id=args.storyboard_id,
        layout=args.layout,
        notes=args.notes,
    )


def cmd_storyboard_add(args: argparse.Namespace) -> dict:
    return ProjectStore.from_args(args).add_storyboard(
        project_id=args.project_id,
        storyboard_id=args.storyboard_id,
        image=args.image,
        prompt_file=args.prompt,
        video_prompt_file=args.video_prompt,
        layout=args.layout,
        notes=args.notes,
    )


def cmd_storyboard_show(args: argparse.Namespace) -> dict:
    storyboard = ProjectStore.from_args(args).load_storyboard(
        args.project_id,
        args.storyboard_id,
    )
    return {"ok": True, "project_id": args.project_id, "storyboard": storyboard}


def cmd_storyboard_approve(args: argparse.Namespace) -> dict:
    return ProjectStore.from_args(args).approve_storyboard(
        project_id=args.project_id,
        storyboard_id=args.storyboard_id,
        approved_by=args.approved_by,
        notes=args.notes,
    )


def cmd_history_list(args: argparse.Namespace) -> dict:
    return ProjectStore.from_args(args).list_generations(args.project_id)


def cmd_history_show(args: argparse.Namespace) -> dict:
    return ProjectStore.from_args(args).show_generation(args.project_id, args.run_id)
