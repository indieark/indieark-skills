"""Argparse parser builder and subcommand wiring."""

from __future__ import annotations

import argparse

from seedance2.commands.callback import cmd_callback_server, cmd_callback_smoke
from seedance2.commands.modes import (
    cmd_edit,
    cmd_extend,
    cmd_first_frame,
    cmd_first_last,
    cmd_generate,
    cmd_omni,
    cmd_text_to_video,
)
from seedance2.commands.projects import (
    cmd_asset_add,
    cmd_asset_list,
    cmd_asset_reuse,
    cmd_asset_search,
    cmd_asset_show,
    cmd_history_list,
    cmd_history_show,
    cmd_project_create,
    cmd_project_list,
    cmd_project_show,
    cmd_script_set,
    cmd_script_show,
    cmd_storyboard_add,
    cmd_storyboard_approve,
    cmd_storyboard_plan,
    cmd_storyboard_show,
    cmd_style_set,
    cmd_style_show,
)
from seedance2.commands.reviews import cmd_review_final_input, cmd_review_result
from seedance2.commands.setup import (
    cmd_config_get,
    cmd_config_list,
    cmd_config_path,
    cmd_config_set,
    cmd_config_unset,
    cmd_doctor,
    cmd_setup,
    parse_bool,
)
from seedance2.commands.tasks import cmd_delete, cmd_list, cmd_status, cmd_wait
from seedance2.constants import (
    ALLOWED_LIST_FILTER_STATUSES,
    ALLOWED_MODELS,
    ALLOWED_RATIOS,
    ALLOWED_RESOLUTIONS,
    ALLOWED_SERVICE_TIERS,
    CONFIG_KEYS,
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
    DEFAULT_PROJECT_ROOT,
    DEFAULT_RUN_ROOT,
)


def add_global_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--api-key", help="Volcengine Ark API key; overrides env and config"
    )
    parser.add_argument(
        "--base-url", help=f"API base URL (default: {DEFAULT_BASE_URL})"
    )
    parser.add_argument(
        "--format",
        dest="format",
        choices=("json", "markdown"),
        default="json",
        help="output format (default: json)",
    )


def add_create_options(
    parser: argparse.ArgumentParser,
    *,
    allow_web_search: bool = False,
    require_prompt: bool = False,
    include_project_tracking: bool = True,
) -> None:
    add_global_options(parser)
    parser.add_argument(
        "--prompt", "-p", required=require_prompt, help="director prompt"
    )
    parser.add_argument(
        "--prompt-file",
        help="UTF-8 text file containing the director prompt; useful for long or non-ASCII prompts",
    )
    parser.add_argument("--model", choices=list(ALLOWED_MODELS))
    parser.add_argument("--resolution", choices=list(ALLOWED_RESOLUTIONS))
    parser.add_argument("--ratio", choices=list(ALLOWED_RATIOS))
    parser.add_argument(
        "--duration", type=int, help="4-15 seconds, or -1 for automatic"
    )
    parser.add_argument("--generate-audio", type=parse_bool)
    parser.add_argument("--watermark", type=parse_bool)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--return-last-frame", action="store_true")
    parser.add_argument("--callback-url", help="HTTP(S) task status callback URL")
    parser.add_argument(
        "--execution-expires-after",
        type=int,
        help="task expiry in seconds, 3600-259200",
    )
    parser.add_argument(
        "--service-tier",
        choices=list(ALLOWED_SERVICE_TIERS),
        help="Seedance 2.0 supports only default online inference; flex is rejected",
    )
    parser.add_argument(
        "--safety-identifier",
        help="stable hashed end-user identifier, max 64 chars",
    )
    parser.add_argument("--wait", action="store_true", help="poll until completion")
    parser.add_argument("--interval", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument(
        "--download", help="directory to download the generated MP4 (only with --wait)"
    )
    parser.add_argument(
        "--dry-run-payload",
        action="store_true",
        help="build and save the redacted payload without calling the API",
    )
    parser.add_argument(
        "--run-dir",
        default=DEFAULT_RUN_ROOT,
        help=f"directory for prompt/payload/media artifacts (default: {DEFAULT_RUN_ROOT})",
    )
    parser.add_argument("--run-id", help="artifact run id; defaults to timestamp")
    parser.add_argument(
        "--serve-local-assets",
        choices=("none", "cloudflare"),
        default="none",
        help=(
            "serve local reference_video files from an isolated run directory; "
            "cloudflare requires the cloudflared binary"
        ),
    )
    parser.add_argument(
        "--prepare-local-media",
        choices=("auto", "off"),
        default="auto",
        help=(
            "prepare local image/audio before Base64 payload encoding; auto may use "
            "Pillow for images and ffmpeg for audio"
        ),
    )
    if include_project_tracking:
        add_project_tracking_options(parser)
    if allow_web_search:
        parser.add_argument(
            "--web-search", action="store_true", help="text-to-video only"
        )
    else:
        parser.set_defaults(web_search=False)


def add_projects_dir_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--projects-dir",
        default=DEFAULT_PROJECT_ROOT,
        help=f"creative project library root (default: {DEFAULT_PROJECT_ROOT})",
    )


def add_project_tracking_options(parser: argparse.ArgumentParser) -> None:
    add_projects_dir_option(parser)
    parser.add_argument("--project", help="creative project id for traceable runs")
    parser.add_argument("--storyboard", help="storyboard id to associate with this run")
    parser.add_argument(
        "--allow-unapproved-storyboard",
        action="store_true",
        help="allow generation with an unapproved storyboard; default requires approval",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="seedance2",
        description=(
            "Seedance 2.0 director-grade video API CLI. "
            "Run `seedance2 setup` first to save your Volcengine Ark API key."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # --- setup ---
    setup_p = sub.add_parser("setup", help="configure API key and defaults")
    setup_p.add_argument("--non-interactive", action="store_true")
    setup_p.add_argument(
        "--reset", action="store_true", help="discard existing config before writing"
    )
    setup_p.add_argument("--api-key")
    setup_p.add_argument("--base-url")
    setup_p.add_argument("--model", choices=list(ALLOWED_MODELS))
    setup_p.add_argument("--default-resolution", choices=list(ALLOWED_RESOLUTIONS))
    setup_p.add_argument("--default-ratio", choices=list(ALLOWED_RATIOS))
    setup_p.add_argument("--default-duration", type=int)
    setup_p.add_argument("--default-generate-audio", type=parse_bool)
    setup_p.add_argument("--default-watermark", type=parse_bool)
    setup_p.add_argument("--format", choices=("json", "markdown"), default="json")
    setup_p.set_defaults(func=cmd_setup)

    # --- doctor ---
    doctor_p = sub.add_parser("doctor", help="health check for config and connectivity")
    add_global_options(doctor_p)
    doctor_p.add_argument("--skip-connectivity", action="store_true")
    doctor_p.add_argument(
        "--skip-update-check",
        action="store_true",
        help="skip GitHub Releases version check",
    )
    doctor_p.set_defaults(func=cmd_doctor)

    # --- config ---
    config_p = sub.add_parser("config", help="inspect or edit saved config")
    config_sub = config_p.add_subparsers(dest="config_command", required=True)

    cp_path = config_sub.add_parser("path", help="print config file path")
    cp_path.add_argument("--format", choices=("json", "markdown"), default="json")
    cp_path.set_defaults(func=cmd_config_path)

    cp_list = config_sub.add_parser("list", help="list saved config (secret keys masked)")
    cp_list.add_argument("--format", choices=("json", "markdown"), default="json")
    cp_list.set_defaults(func=cmd_config_list)

    cp_get = config_sub.add_parser("get", help="get one config value")
    cp_get.add_argument("key", choices=list(CONFIG_KEYS))
    cp_get.add_argument("--format", choices=("json", "markdown"), default="json")
    cp_get.set_defaults(func=cmd_config_get)

    cp_set = config_sub.add_parser("set", help="set one config value")
    cp_set.add_argument("key", choices=list(CONFIG_KEYS))
    cp_set.add_argument("value")
    cp_set.add_argument("--format", choices=("json", "markdown"), default="json")
    cp_set.set_defaults(func=cmd_config_set)

    cp_unset = config_sub.add_parser("unset", help="remove one config value")
    cp_unset.add_argument("key", choices=list(CONFIG_KEYS))
    cp_unset.add_argument("--format", choices=("json", "markdown"), default="json")
    cp_unset.set_defaults(func=cmd_config_unset)

    # --- project asset library ---
    project_p = sub.add_parser("project", help="create, list, and inspect creative projects")
    project_sub = project_p.add_subparsers(dest="project_command", required=True)

    project_create = project_sub.add_parser("create", help="create a creative project")
    project_create.add_argument("intent", help="original user idea or brief")
    project_create.add_argument("--title")
    project_create.add_argument("--project-id")
    project_create.add_argument("--platform")
    project_create.add_argument("--ratio")
    project_create.add_argument("--duration", type=int)
    project_create.add_argument("--notes")
    add_projects_dir_option(project_create)
    project_create.add_argument("--format", choices=("json", "markdown"), default="json")
    project_create.set_defaults(func=cmd_project_create)

    project_list = project_sub.add_parser("list", help="list creative projects")
    add_projects_dir_option(project_list)
    project_list.add_argument("--format", choices=("json", "markdown"), default="json")
    project_list.set_defaults(func=cmd_project_list)

    project_show = project_sub.add_parser("show", help="show one creative project")
    project_show.add_argument("project_id")
    add_projects_dir_option(project_show)
    project_show.add_argument("--format", choices=("json", "markdown"), default="json")
    project_show.set_defaults(func=cmd_project_show)

    asset_p = sub.add_parser("asset", help="add, list, show, search, and reuse project character/scene images")
    asset_sub = asset_p.add_subparsers(dest="asset_command", required=True)

    asset_add = asset_sub.add_parser("add", help="add a character or scene asset")
    asset_add.add_argument("project_id")
    asset_add.add_argument("--type", choices=("character", "scene"), required=True)
    asset_add.add_argument("--name", required=True)
    asset_add.add_argument("--file", help="local image file copied into the project")
    asset_add.add_argument("--source", help="HTTP(S), asset://, or data URI source")
    asset_add.add_argument("--asset-id")
    asset_add.add_argument("--purpose")
    asset_add.add_argument("--description")
    asset_add.add_argument("--role", help="stable creative role, e.g. protagonist or location")
    asset_add.add_argument("--tag", action="append", help="repeatable search tag")
    asset_add.add_argument("--alias", action="append", help="repeatable alias or alternate name")
    add_projects_dir_option(asset_add)
    asset_add.add_argument("--format", choices=("json", "markdown"), default="json")
    asset_add.set_defaults(func=cmd_asset_add)

    asset_list = asset_sub.add_parser("list", help="list project assets")
    asset_list.add_argument("project_id")
    asset_list.add_argument("--type", choices=("character", "scene"))
    asset_list.add_argument("--query", help="case-insensitive text search within project assets")
    asset_list.add_argument("--tag", action="append", help="repeatable tag filter; all tags must match")
    asset_list.add_argument("--role", help="exact role filter")
    asset_list.add_argument("--source-type", choices=("local_file", "external"))
    add_projects_dir_option(asset_list)
    asset_list.add_argument("--format", choices=("json", "markdown"), default="json")
    asset_list.set_defaults(func=cmd_asset_list)

    asset_show = asset_sub.add_parser("show", help="show one project asset")
    asset_show.add_argument("project_id")
    asset_show.add_argument("asset_id")
    asset_show.add_argument("--type", choices=("character", "scene"))
    add_projects_dir_option(asset_show)
    asset_show.add_argument("--format", choices=("json", "markdown"), default="json")
    asset_show.set_defaults(func=cmd_asset_show)

    asset_search = asset_sub.add_parser("search", help="search assets across projects")
    asset_search.add_argument("--project", help="optional project id scope")
    asset_search.add_argument("--type", choices=("character", "scene"))
    asset_search.add_argument("--query", help="case-insensitive text search")
    asset_search.add_argument("--tag", action="append", help="repeatable tag filter; all tags must match")
    asset_search.add_argument("--role", help="exact role filter")
    asset_search.add_argument("--source-type", choices=("local_file", "external"))
    add_projects_dir_option(asset_search)
    asset_search.add_argument("--format", choices=("json", "markdown"), default="json")
    asset_search.set_defaults(func=cmd_asset_search)

    asset_reuse = asset_sub.add_parser("reuse", help="reuse an asset in another project")
    asset_reuse.add_argument("target_project_id")
    asset_reuse.add_argument("source_project_id")
    asset_reuse.add_argument("source_asset_id")
    asset_reuse.add_argument("--type", choices=("character", "scene"))
    asset_reuse.add_argument("--asset-id", help="new asset id in the target project")
    asset_reuse.add_argument("--name", help="new display name; defaults to source name")
    asset_reuse.add_argument("--purpose", help="new purpose; defaults to source purpose")
    asset_reuse.add_argument("--description", help="new description; defaults to source description")
    asset_reuse.add_argument("--role", help="new role; defaults to source role")
    asset_reuse.add_argument("--tag", action="append", help="extra tag; source tags are preserved")
    asset_reuse.add_argument("--alias", action="append", help="extra alias; source aliases are preserved")
    add_projects_dir_option(asset_reuse)
    asset_reuse.add_argument("--format", choices=("json", "markdown"), default="json")
    asset_reuse.set_defaults(func=cmd_asset_reuse)

    script_p = sub.add_parser("script", help="set or show a project script")
    script_sub = script_p.add_subparsers(dest="script_command", required=True)

    script_set = script_sub.add_parser("set", help="save project script.md")
    script_set.add_argument("project_id")
    source_group = script_set.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--file")
    source_group.add_argument("--text")
    add_projects_dir_option(script_set)
    script_set.add_argument("--format", choices=("json", "markdown"), default="json")
    script_set.set_defaults(func=cmd_script_set)

    script_show = script_sub.add_parser("show", help="show project script.md")
    script_show.add_argument("project_id")
    add_projects_dir_option(script_show)
    script_show.add_argument("--format", choices=("json", "markdown"), default="json")
    script_show.set_defaults(func=cmd_script_show)

    style_p = sub.add_parser("style", help="set or show project visual style rules")
    style_sub = style_p.add_subparsers(dest="style_command", required=True)

    style_set = style_sub.add_parser("set", help="save project style.md")
    style_set.add_argument("project_id")
    style_group = style_set.add_mutually_exclusive_group(required=True)
    style_group.add_argument("--file")
    style_group.add_argument("--text")
    add_projects_dir_option(style_set)
    style_set.add_argument("--format", choices=("json", "markdown"), default="json")
    style_set.set_defaults(func=cmd_style_set)

    style_show = style_sub.add_parser("show", help="show project style.md")
    style_show.add_argument("project_id")
    add_projects_dir_option(style_show)
    style_show.add_argument("--format", choices=("json", "markdown"), default="json")
    style_show.set_defaults(func=cmd_style_show)

    storyboard_p = sub.add_parser("storyboard", help="plan, add, approve, and inspect storyboards")
    storyboard_sub = storyboard_p.add_subparsers(dest="storyboard_command", required=True)

    storyboard_plan = storyboard_sub.add_parser("plan", help="create a storyboard planning scaffold")
    storyboard_plan.add_argument("project_id")
    storyboard_plan.add_argument("--storyboard-id")
    storyboard_plan.add_argument(
        "--layout",
        choices=("3x3", "four-column", "single-reference"),
        default="3x3",
    )
    storyboard_plan.add_argument("--notes")
    add_projects_dir_option(storyboard_plan)
    storyboard_plan.add_argument("--format", choices=("json", "markdown"), default="json")
    storyboard_plan.set_defaults(func=cmd_storyboard_plan)

    storyboard_add = storyboard_sub.add_parser("add", help="register a storyboard image and prompts")
    storyboard_add.add_argument("project_id")
    storyboard_add.add_argument("--storyboard-id")
    storyboard_add.add_argument("--image", required=True)
    storyboard_add.add_argument("--prompt", required=True, help="UTF-8 storyboard prompt file")
    storyboard_add.add_argument("--video-prompt", required=True, help="UTF-8 Seedance prompt file")
    storyboard_add.add_argument("--layout", choices=("3x3", "four-column", "single-reference"))
    storyboard_add.add_argument("--notes")
    add_projects_dir_option(storyboard_add)
    storyboard_add.add_argument("--format", choices=("json", "markdown"), default="json")
    storyboard_add.set_defaults(func=cmd_storyboard_add)

    storyboard_show = storyboard_sub.add_parser("show", help="show storyboard metadata")
    storyboard_show.add_argument("project_id")
    storyboard_show.add_argument("storyboard_id")
    add_projects_dir_option(storyboard_show)
    storyboard_show.add_argument("--format", choices=("json", "markdown"), default="json")
    storyboard_show.set_defaults(func=cmd_storyboard_show)

    storyboard_approve = storyboard_sub.add_parser("approve", help="approve a storyboard for generation")
    storyboard_approve.add_argument("project_id")
    storyboard_approve.add_argument("storyboard_id")
    storyboard_approve.add_argument("--approved-by")
    storyboard_approve.add_argument("--notes")
    add_projects_dir_option(storyboard_approve)
    storyboard_approve.add_argument("--format", choices=("json", "markdown"), default="json")
    storyboard_approve.set_defaults(func=cmd_storyboard_approve)

    # --- input modes ---
    t2v = sub.add_parser("text-to-video", help="pure text prompt -> video")
    add_create_options(t2v, allow_web_search=True)
    t2v.set_defaults(func=cmd_text_to_video)

    ff = sub.add_parser("first-frame", help="prompt + first frame image -> video")
    add_create_options(ff)
    ff.add_argument(
        "--first-frame",
        required=True,
        help="URL, data URI, asset URI, or local image file",
    )
    ff.set_defaults(func=cmd_first_frame)

    fl = sub.add_parser(
        "first-last", help="prompt + first frame + last frame -> video"
    )
    add_create_options(fl)
    fl.add_argument("--first-frame", required=True)
    fl.add_argument("--last-frame", required=True)
    fl.set_defaults(func=cmd_first_last)

    omni = sub.add_parser(
        "omni", help="omnireference: prompt + reference image/video/audio -> video"
    )
    add_create_options(omni)
    omni.add_argument(
        "--reference-image", action="append", help="reference image; repeat up to 9"
    )
    omni.add_argument(
        "--reference-video", action="append", help="reference video; repeat up to 3"
    )
    omni.add_argument(
        "--reference-audio",
        action="append",
        help="reference audio; must pair with image/video",
    )
    omni.set_defaults(func=cmd_omni)

    edit_p = sub.add_parser(
        "edit",
        help=(
            "edit-intent prompt + reference video(s); not mask/inpaint or "
            "guaranteed subject replacement"
        ),
    )
    add_create_options(edit_p)
    edit_p.add_argument("--reference-video", action="append", required=True)
    edit_p.add_argument("--reference-image", action="append")
    edit_p.set_defaults(func=cmd_edit)

    ext_p = sub.add_parser(
        "extend", help="prompt + reference video(s) -> extended video"
    )
    add_create_options(ext_p)
    ext_p.add_argument("--reference-video", action="append", required=True)
    ext_p.set_defaults(func=cmd_extend)

    gen_p = sub.add_parser(
        "generate",
        help="generate from an approved project storyboard and save traceable history",
    )
    add_create_options(gen_p, include_project_tracking=False)
    gen_p.add_argument("--project", required=True)
    gen_p.add_argument("--storyboard", required=True)
    gen_p.add_argument(
        "--storyboard-mode",
        choices=("omni", "first-frame"),
        default="omni",
        help="how to feed the storyboard image into Seedance 2.0 (default: omni)",
    )
    gen_p.add_argument("--reference-image", action="append", help="extra reference image")
    gen_p.add_argument("--reference-video", action="append", help="extra reference video")
    gen_p.add_argument("--reference-audio", action="append", help="extra reference audio")
    add_projects_dir_option(gen_p)
    gen_p.add_argument(
        "--allow-unapproved-storyboard",
        action="store_true",
        help="allow generation with an unapproved storyboard",
    )
    gen_p.set_defaults(func=cmd_generate)

    review_p = sub.add_parser(
        "review",
        help="archived Agent-HTML final-input and result review gates",
    )
    review_sub = review_p.add_subparsers(dest="review_command", required=True)

    review_final = review_sub.add_parser(
        "final-input",
        help="create the archived before-video-generation Agent-HTML approval gate",
    )
    review_final.add_argument("--project", required=True)
    review_final.add_argument("--storyboard", required=True)
    review_final.add_argument(
        "--storyboard-mode",
        choices=("omni", "first-frame"),
        default="omni",
    )
    review_final.add_argument("--model", choices=list(ALLOWED_MODELS))
    review_final.add_argument("--resolution", choices=list(ALLOWED_RESOLUTIONS))
    review_final.add_argument("--ratio", choices=list(ALLOWED_RATIOS))
    review_final.add_argument("--duration", type=int)
    review_final.add_argument("--generate-audio", type=parse_bool)
    review_final.add_argument("--watermark", type=parse_bool)
    review_final.add_argument("--reference-image", action="append")
    review_final.add_argument("--reference-video", action="append")
    review_final.add_argument("--reference-audio", action="append")
    review_final.add_argument("--run-id")
    review_final.add_argument("--wait", action="store_true")
    review_final.add_argument("--download")
    review_final.add_argument("--output", help="HTML output path")
    add_projects_dir_option(review_final)
    review_final.add_argument("--format", choices=("json", "markdown"), default="json")
    review_final.set_defaults(func=cmd_review_final_input)

    review_result = review_sub.add_parser(
        "result",
        help="create the archived after-video-generation Agent-HTML recap gate",
    )
    review_result.add_argument("--project", required=True)
    review_result.add_argument("--run-id", required=True)
    review_result.add_argument("--output", help="HTML output path")
    add_projects_dir_option(review_result)
    review_result.add_argument("--format", choices=("json", "markdown"), default="json")
    review_result.set_defaults(func=cmd_review_result)

    # --- task management ---
    status_p = sub.add_parser("status", help="query a task")
    add_global_options(status_p)
    status_p.add_argument("task_id")
    status_p.set_defaults(func=cmd_status)

    wait_p = sub.add_parser("wait", help="poll a task until completion")
    add_global_options(wait_p)
    wait_p.add_argument("task_id")
    wait_p.add_argument("--interval", type=int, default=10)
    wait_p.add_argument("--timeout", type=int, default=1800)
    wait_p.add_argument("--download")
    wait_p.set_defaults(func=cmd_wait)

    list_p = sub.add_parser("list", help="list tasks")
    add_global_options(list_p)
    list_p.add_argument("--page", type=int, default=1)
    list_p.add_argument("--page-size", type=int, default=10)
    list_p.add_argument("--status", choices=list(ALLOWED_LIST_FILTER_STATUSES))
    list_p.set_defaults(func=cmd_list)

    del_p = sub.add_parser("delete", help="cancel or delete a task")
    add_global_options(del_p)
    del_p.add_argument("task_id")
    del_p.set_defaults(func=cmd_delete)

    history_p = sub.add_parser("history", help="list or inspect project generation records")
    history_sub = history_p.add_subparsers(dest="history_command", required=True)

    history_list = history_sub.add_parser("list", help="list project generation records")
    history_list.add_argument("project_id")
    add_projects_dir_option(history_list)
    history_list.add_argument("--format", choices=("json", "markdown"), default="json")
    history_list.set_defaults(func=cmd_history_list)

    history_show = history_sub.add_parser("show", help="show one project generation record")
    history_show.add_argument("project_id")
    history_show.add_argument("run_id")
    add_projects_dir_option(history_show)
    history_show.add_argument("--format", choices=("json", "markdown"), default="json")
    history_show.set_defaults(func=cmd_history_show)

    # --- optional callback helpers ---
    callback_server = sub.add_parser(
        "callback-server",
        help="optional local webhook receiver for testing callback_url integrations",
    )
    callback_server.add_argument("--host", default="127.0.0.1")
    callback_server.add_argument("--port", type=int, default=8787)
    callback_server.add_argument("--path", default="/callback")
    callback_server.add_argument("--out-dir", default="_work/seedance_callbacks")
    callback_server.add_argument(
        "--max-events",
        type=int,
        default=0,
        help="stop after N callbacks; 0 means run until interrupted",
    )
    callback_server.add_argument("--format", choices=("json", "markdown"), default="json")
    callback_server.set_defaults(func=cmd_callback_server)

    callback_smoke = sub.add_parser(
        "callback-smoke",
        help="send a local simulated callback POST to a callback receiver",
    )
    callback_smoke.add_argument("url")
    callback_smoke.add_argument("--task-id", default="seedance2-callback-smoke")
    callback_smoke.add_argument(
        "--status",
        choices=("queued", "running", "succeeded", "failed", "expired"),
        default="succeeded",
    )
    callback_smoke.add_argument("--timeout", type=int, default=10)
    callback_smoke.add_argument("--format", choices=("json", "markdown"), default="json")
    callback_smoke.set_defaults(func=cmd_callback_smoke)

    return parser
