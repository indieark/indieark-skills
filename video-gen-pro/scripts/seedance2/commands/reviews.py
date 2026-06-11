"""Review page subcommands."""

from __future__ import annotations

import argparse

from seedance2.project_store import ProjectStore
from seedance2.review_pages import (
    build_final_input_review_state,
    build_result_review_state,
    review_stem,
    write_review_bundle,
)


def cmd_review_final_input(args: argparse.Namespace) -> dict:
    store = ProjectStore.from_args(args)
    state = build_final_input_review_state(store, args)
    default_dir = store.project_dir(args.project) / "reviews"
    return write_review_bundle(
        state,
        output=args.output,
        default_dir=default_dir,
        stem=review_stem("final-input", state["output"]["run_id"]),
        title="Seedance Final Input Review",
    )


def cmd_review_result(args: argparse.Namespace) -> dict:
    store = ProjectStore.from_args(args)
    state = build_result_review_state(store, args)
    default_dir = store.project_dir(args.project) / "reviews"
    return write_review_bundle(
        state,
        output=args.output,
        default_dir=default_dir,
        stem=review_stem("result", args.run_id),
        title="Seedance Result Review",
    )
