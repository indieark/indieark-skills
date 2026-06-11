"""Six input mode subcommand handlers."""

from __future__ import annotations

import argparse
from pathlib import Path

from seedance2.api import (
    build_create_payload,
    download_video,
    submit_task,
    validate_payload_media_urls,
    wait_for_task,
)
from seedance2.artifacts import (
    create_run_artifacts,
    update_media_manifest,
    write_generation_log,
    write_submit_summary,
    write_task_result,
)
from seedance2.asset_server import maybe_serve_local_assets
from seedance2.constants import DEFAULT_RUN_ROOT, EXIT_USAGE
from seedance2.errors import SeedanceError
from seedance2.media_prepare import prepare_local_media
from seedance2.media_validate import validate_local_media
from seedance2.project_store import (
    ProjectStore,
    storyboard_image_source,
    storyboard_video_prompt,
)
from seedance2.settings import Settings


def _submit_with_optional_wait(
    settings: Settings,
    args: argparse.Namespace,
    *,
    mode: str,
) -> dict:
    _load_prompt_file(args)
    _prepare_project_context(args)
    prepare_local_media(args)
    validate_local_media(args)
    with maybe_serve_local_assets(args) as asset_server:
        payload = build_create_payload(
            settings,
            args,
            mode=mode,
            **_payload_kwargs(mode, args),
        )
        artifacts = create_run_artifacts(args, mode=mode, payload=payload)
        if asset_server:
            artifacts["manifest"]["asset_server"] = asset_server
            update_media_manifest(artifacts, artifacts["manifest"].get("url_checks", []))
        if args.dry_run_payload:
            response = {
                "ok": True,
                "dry_run": True,
                "mode": mode,
                "payload": artifacts["payload_redacted"],
                "run_dir": artifacts["run_dir"],
                "payload_path": artifacts["payload_path"],
                "manifest_path": artifacts["manifest_path"],
                "generation_log_path": artifacts["generation_log_path"],
                "asset_server": asset_server,
            }
            write_generation_log(artifacts, stage="dry_run")
            _write_project_generation_record(args, mode, "dry_run", artifacts, response)
            return response
        settings.require_api_key()
        url_checks = validate_payload_media_urls(payload)
        update_media_manifest(artifacts, url_checks)
        submission = submit_task(settings, args, payload, mode)
        submission["run_dir"] = artifacts["run_dir"]
        submission["payload_path"] = artifacts["payload_path"]
        submission["manifest_path"] = artifacts["manifest_path"]
        submission["generation_log_path"] = artifacts["generation_log_path"]
        write_submit_summary(artifacts, submission)
        write_generation_log(artifacts, stage="submitted", submission=submission)
        if not args.wait:
            _write_project_generation_record(args, mode, "submitted", artifacts, submission)
            return submission
        final = wait_for_task(
            settings, submission["task_id"], interval=args.interval, timeout=args.timeout
        )
        if args.download and final.get("video_url"):
            downloaded = download_video(
                final["video_url"], args.download, submission["task_id"]
            )
            final["downloaded_path"] = str(downloaded)
        final["created"] = submission
        final["mode"] = mode
        final["run_dir"] = artifacts["run_dir"]
        final["payload_path"] = artifacts["payload_path"]
        final["manifest_path"] = artifacts["manifest_path"]
        final["generation_log_path"] = artifacts["generation_log_path"]
        write_task_result(artifacts, final)
        write_generation_log(
            artifacts,
            stage="completed",
            submission=submission,
            result=final,
        )
        _write_project_generation_record(args, mode, "completed", artifacts, final)
        return final


def _load_prompt_file(args: argparse.Namespace) -> None:
    prompt_file = getattr(args, "prompt_file", None)
    if not prompt_file:
        return
    if getattr(args, "prompt", None):
        raise SeedanceError(
            "use either --prompt or --prompt-file, not both",
            code=EXIT_USAGE,
        )
    path = Path(prompt_file).expanduser()
    if not path.is_file():
        raise SeedanceError(f"prompt file not found: {prompt_file}", code=EXIT_USAGE)
    try:
        prompt = path.read_text(encoding="utf-8-sig").rstrip("\r\n")
    except UnicodeDecodeError as exc:
        raise SeedanceError(
            f"prompt file must be UTF-8: {prompt_file}",
            code=EXIT_USAGE,
            payload={"error": str(exc)},
        )
    if not prompt.strip():
        raise SeedanceError("prompt file is empty", code=EXIT_USAGE)
    args.prompt = prompt


def cmd_text_to_video(args: argparse.Namespace) -> dict:
    settings = Settings(args)
    return _submit_with_optional_wait(settings, args, mode="text-to-video")


def cmd_first_frame(args: argparse.Namespace) -> dict:
    settings = Settings(args)
    return _submit_with_optional_wait(settings, args, mode="first-frame")


def cmd_first_last(args: argparse.Namespace) -> dict:
    settings = Settings(args)
    return _submit_with_optional_wait(settings, args, mode="first-last")


def cmd_omni(args: argparse.Namespace) -> dict:
    settings = Settings(args)
    return _submit_with_optional_wait(settings, args, mode="omni")


def cmd_edit(args: argparse.Namespace) -> dict:
    settings = Settings(args)
    return _submit_with_optional_wait(settings, args, mode="edit")


def cmd_extend(args: argparse.Namespace) -> dict:
    settings = Settings(args)
    return _submit_with_optional_wait(settings, args, mode="extend")


def cmd_generate(args: argparse.Namespace) -> dict:
    settings = Settings(args)
    mode = _prepare_generate_from_storyboard(args)
    return _submit_with_optional_wait(settings, args, mode=mode)


def _payload_kwargs(mode: str, args: argparse.Namespace) -> dict:
    if mode == "text-to-video":
        return {"web_search": args.web_search}
    if mode == "first-frame":
        return {"first_frame": args.first_frame}
    if mode == "first-last":
        return {"first_frame": args.first_frame, "last_frame": args.last_frame}
    if mode == "omni":
        return {
            "reference_images": args.reference_image or [],
            "reference_videos": args.reference_video or [],
            "reference_audios": args.reference_audio or [],
        }
    if mode == "edit":
        return {
            "reference_images": args.reference_image or [],
            "reference_videos": args.reference_video,
        }
    if mode == "extend":
        return {"reference_videos": args.reference_video}
    return {}


def _prepare_project_context(args: argparse.Namespace) -> dict | None:
    if getattr(args, "project_context", None):
        return args.project_context
    project_id = getattr(args, "project", None)
    storyboard_id = getattr(args, "storyboard", None)
    if storyboard_id and not project_id:
        raise SeedanceError("--storyboard requires --project", code=EXIT_USAGE)
    if not project_id:
        return None
    store = ProjectStore.from_args(args)
    context = store.project_context(
        project_id,
        storyboard_id,
        allow_unapproved=getattr(args, "allow_unapproved_storyboard", False),
    )
    args.project_context = _context_summary(context)
    args.project_store = store
    if getattr(args, "run_dir", None) == DEFAULT_RUN_ROOT:
        args.run_dir = str(store.generations_root(project_id))
    return args.project_context


def _prepare_generate_from_storyboard(args: argparse.Namespace) -> str:
    context = _prepare_project_context(args)
    if not context or not context.get("storyboard_id"):
        raise SeedanceError("generate requires --project and --storyboard", code=EXIT_USAGE)
    storyboard = context["storyboard"]
    image_source = storyboard_image_source(storyboard)
    if not image_source:
        raise SeedanceError(
            "storyboard has no image source; run storyboard add first",
            code=EXIT_USAGE,
        )
    if not getattr(args, "prompt", None) and not getattr(args, "prompt_file", None):
        prompt = storyboard_video_prompt(storyboard)
        if not prompt:
            raise SeedanceError(
                "storyboard has no video prompt; run storyboard add with --video-prompt",
                code=EXIT_USAGE,
            )
        args.prompt = prompt
    if args.storyboard_mode == "first-frame":
        args.first_frame = image_source
        return "first-frame"
    args.reference_image = [image_source, *(getattr(args, "reference_image", None) or [])]
    return "omni"


def _context_summary(context: dict) -> dict:
    storyboard = context.get("storyboard")
    return {
        "project_id": context.get("project_id"),
        "project_title": context.get("project_title"),
        "project_path": context.get("project_path"),
        "storyboard_id": context.get("storyboard_id"),
        "storyboard": {
            "storyboard_id": storyboard.get("storyboard_id"),
            "status": storyboard.get("status"),
            "approved": storyboard.get("approved"),
            "image": storyboard.get("image"),
            "storyboard_prompt": storyboard.get("storyboard_prompt"),
            "video_prompt": storyboard.get("video_prompt"),
            "storyboard_path": storyboard.get("storyboard_path"),
        } if isinstance(storyboard, dict) else None,
    }


def _write_project_generation_record(
    args: argparse.Namespace,
    mode: str,
    stage: str,
    artifacts: dict,
    result: dict,
) -> None:
    context = getattr(args, "project_context", None)
    store = getattr(args, "project_store", None)
    if not context or not store:
        return
    store.write_generation_record(
        context=context,
        run_id=args.run_id,
        mode=mode,
        stage=stage,
        artifacts=artifacts,
        result=result,
    )
