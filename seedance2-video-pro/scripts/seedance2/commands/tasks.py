"""Task management subcommand handlers (status, wait, list, delete)."""

from __future__ import annotations

import argparse
import urllib.parse

from seedance2.api import (
    download_video,
    extract_video_url,
    task_url,
    wait_for_task,
)
from seedance2.constants import EXIT_USAGE, MAX_PAGE, MIN_PAGE
from seedance2.errors import SeedanceError
from seedance2.http import request_json
from seedance2.settings import Settings


def cmd_status(args: argparse.Namespace) -> dict:
    settings = Settings(args)
    api_key = settings.require_api_key()
    result = request_json("GET", task_url(settings, args.task_id), api_key)
    return {
        "ok": True,
        "task_id": args.task_id,
        "status": result.get("status"),
        "video_url": extract_video_url(result),
        "response": result,
    }


def cmd_wait(args: argparse.Namespace) -> dict:
    settings = Settings(args)
    final = wait_for_task(
        settings, args.task_id, interval=args.interval, timeout=args.timeout
    )
    if args.download and final.get("video_url"):
        downloaded = download_video(final["video_url"], args.download, args.task_id)
        final["downloaded_path"] = str(downloaded)
    return final


def cmd_list(args: argparse.Namespace) -> dict:
    if not (MIN_PAGE <= args.page <= MAX_PAGE):
        raise SeedanceError(
            f"page must be between {MIN_PAGE} and {MAX_PAGE}",
            code=EXIT_USAGE,
        )
    if not (MIN_PAGE <= args.page_size <= MAX_PAGE):
        raise SeedanceError(
            f"page-size must be between {MIN_PAGE} and {MAX_PAGE}",
            code=EXIT_USAGE,
        )
    settings = Settings(args)
    api_key = settings.require_api_key()
    params: dict[str, str] = {
        "page_num": str(args.page),
        "page_size": str(args.page_size),
    }
    if args.status:
        params["filter.status"] = args.status
    url = task_url(settings) + "?" + urllib.parse.urlencode(params)
    result = request_json("GET", url, api_key)
    return {"ok": True, "page": args.page, "page_size": args.page_size, "response": result}


def cmd_delete(args: argparse.Namespace) -> dict:
    settings = Settings(args)
    api_key = settings.require_api_key()
    result = request_json("DELETE", task_url(settings, args.task_id), api_key)
    return {"ok": True, "task_id": args.task_id, "deleted": True, "response": result}
