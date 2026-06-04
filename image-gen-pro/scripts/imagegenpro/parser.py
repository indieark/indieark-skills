from __future__ import annotations

import argparse

from .constants import CONFIG_KEYS, GPT_IMAGE_2_MODEL, IMAGE_MODEL_CHOICES, ROUTE_CHOICES, ROUTE_PRESETS


def add_prompt_args(parser: argparse.ArgumentParser) -> None:
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt")
    prompt_group.add_argument("--prompt-file")


def add_gpt_image_2_args(parser: argparse.ArgumentParser) -> None:
    add_prompt_args(parser)
    parser.add_argument("--route", choices=ROUTE_CHOICES)
    parser.add_argument("--model", choices=IMAGE_MODEL_CHOICES)
    parser.add_argument("--size", default="auto")
    parser.add_argument("--aspect")
    parser.add_argument("--quality", default="auto")
    parser.add_argument("-n", "--n", type=int, default=1)
    parser.add_argument("--background")
    parser.add_argument("--moderation")
    parser.add_argument("--output-format", default="png")
    parser.add_argument("--output-compression", type=int)
    parser.add_argument("--output-file")
    parser.add_argument("--user")
    parser.add_argument("--api-key")
    parser.add_argument("--base-url")
    parser.add_argument("--timeout-sec", type=int, default=300)
    parser.add_argument("--output-dir")
    parser.add_argument("--run-id")
    parser.add_argument("--dry-run-payload", action="store_true")
    parser.add_argument("--prepare-local-media", choices=("auto", "off"), default="auto")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="imagen",
        description="Provider-neutral image generation workflow CLI.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    setup = sub.add_parser("setup", help="write default configuration")
    setup.add_argument("--provider", default="placeholder")
    setup.add_argument("--route-preset", choices=list(ROUTE_PRESETS))
    setup.add_argument("--default-model", choices=IMAGE_MODEL_CHOICES)
    setup.add_argument("--non-interactive", action="store_true")
    setup.add_argument("--api-key")
    setup.add_argument("--base-url")

    doctor = sub.add_parser("doctor", help="inspect config and local readiness")
    doctor.add_argument("--model", choices=IMAGE_MODEL_CHOICES)
    doctor.add_argument("--api-key")
    doctor.add_argument("--base-url")

    config = sub.add_parser("config", help="inspect or edit config")
    config_sub = config.add_subparsers(dest="config_command", required=True)
    config_sub.add_parser("path")
    config_sub.add_parser("list")
    get = config_sub.add_parser("get")
    get.add_argument("key", choices=list(CONFIG_KEYS))
    set_cmd = config_sub.add_parser("set")
    set_cmd.add_argument("key", choices=list(CONFIG_KEYS))
    set_cmd.add_argument("value")
    unset = config_sub.add_parser("unset")
    unset.add_argument("key", choices=list(CONFIG_KEYS))

    runs = sub.add_parser("runs", help="inspect saved run artifacts")
    runs_sub = runs.add_subparsers(dest="runs_command", required=True)
    runs_list = runs_sub.add_parser("list")
    runs_list.add_argument("--limit", type=int, default=20)
    runs_show = runs_sub.add_parser("show")
    runs_show.add_argument("run_id")

    jobs = sub.add_parser("jobs", help="inspect local job state")
    jobs_sub = jobs.add_subparsers(dest="jobs_command", required=True)
    jobs_list = jobs_sub.add_parser("list")
    jobs_list.add_argument("--limit", type=int, default=20)
    jobs_show = jobs_sub.add_parser("show")
    jobs_show.add_argument("run_id")
    jobs_wait = jobs_sub.add_parser("wait")
    jobs_wait.add_argument("run_id")
    jobs_wait.add_argument("--timeout-sec", type=int, default=0)
    jobs_delete = jobs_sub.add_parser("delete")
    jobs_delete.add_argument("run_id")

    batches = sub.add_parser("batches", help="run or inspect batch generation manifests")
    batches_sub = batches.add_subparsers(dest="batches_command", required=True)
    batches_run = batches_sub.add_parser("run")
    batches_run.add_argument("--file", required=True)
    batches_run.add_argument("--batch-id")
    batches_run.add_argument("--resume", action="store_true")
    batches_run.add_argument("--dry-run-payload", action="store_true")
    batches_run.add_argument("--concurrency", type=int)
    batches_run.add_argument("--stop-on-error", action="store_true")
    batches_run.add_argument("--allow-failures", action="store_true")
    batches_list = batches_sub.add_parser("list")
    batches_list.add_argument("--limit", type=int, default=20)
    batches_show = batches_sub.add_parser("show")
    batches_show.add_argument("batch_id")

    transparent = sub.add_parser("transparent", help="post-process a chroma-background image into transparent PNG")
    transparent.add_argument("--input", required=True)
    transparent.add_argument("--output", required=True)
    transparent.add_argument("--background", default="auto")
    transparent.add_argument("--tolerance", type=int, default=36)
    transparent.add_argument("--soft-range", type=int, default=18)
    transparent.add_argument("--edge-cleanup", choices=("rgb-unmix-despill", "none"), default="rgb-unmix-despill")
    transparent.add_argument("--min-island-area", type=int, default=0)
    transparent.add_argument("--edge-decontaminate-strength", type=float, default=0.78)
    transparent.add_argument("--metadata-file")
    transparent.add_argument("--preview-file")

    for name in ("plan", "dry-run"):
        cmd = sub.add_parser(name, help=f"{name} a provider-neutral image request")
        add_prompt_args(cmd)
        cmd.add_argument("--provider")
        cmd.add_argument("--reference", action="append", default=[])
        cmd.add_argument("--run-id")

    generate = sub.add_parser("generate", help="build an image generation payload")
    add_gpt_image_2_args(generate)

    edit = sub.add_parser("edit", help="build an image edit payload")
    add_gpt_image_2_args(edit)
    edit.add_argument("--image", action="append", required=True)
    edit.add_argument("--mask")

    sub.add_parser("version", help="print CLI version")
    return parser
