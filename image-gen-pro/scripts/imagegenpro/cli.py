from __future__ import annotations

import json
import os
import shutil
import sys
from importlib import util as importlib_util
from pathlib import Path

from . import SCRIPT_VERSION
from .artifacts import prompt_fingerprint, run_paths, stable_run_id, write_json
from .commands.batches import list_batches, run_batch, show_batch
from .commands.jobs import delete_job, list_jobs, mark_job, new_job, show_job, wait_job, write_job
from .commands.provider_payload import handle_provider_payload
from .commands.runs import list_runs, show_run
from .config import (
    apply_route_preset,
    config_path,
    load_config,
    mask_secret,
    parse_route_list,
    parse_value,
    redact_config,
    save_config,
)
from .errors import ImageGenError
from .parser import build_parser
from .planning import build_neutral_request, resolve_prompt, summarize_request, validate_provider
from .providers.api_key_http import API_KEY_ENV, BASE_URL_ENV, DEFAULT_BASE_URL, MODEL_API_KEY_ENVS, MODEL_BASE_URL_ENVS, resolve_base_url
from .providers.image_models import normalize_image_model
from .transparent import make_transparent


def _print(data: object) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def handle_setup(args) -> int:
    data = load_config()
    data["default_provider"] = validate_provider(args.provider)
    if args.route_preset:
        data = apply_route_preset(data, args.route_preset)
    if args.default_model:
        data["default_model"] = normalize_image_model(args.default_model)
    if args.api_key:
        data["api_key"] = args.api_key
    if args.base_url:
        data["base_url"] = args.base_url
    path = save_config(data)
    data = load_config()
    _print({
        "ok": True,
        "config_path": str(path),
        "config": redact_config(data),
        "wrote_keys": [
            key for key, value in (
                ("default_provider", args.provider),
                ("default_model", args.default_model),
                ("route_preset", args.route_preset),
                ("api_key", args.api_key),
                ("base_url", args.base_url),
            )
            if value
        ],
        "default_provider": data["default_provider"],
        "default_model": data["default_model"],
        "default_route": data["default_route"],
        "enabled_routes": data["enabled_routes"],
        "route_priority": data["route_priority"],
        "next_steps": _setup_next_steps(data),
    })
    return 0


def handle_doctor(args) -> int:
    data = load_config()
    model = normalize_image_model(args.model or data.get("default_model"))
    codex_command = shutil.which("codex")
    api_key_value, api_key_source = _resolve_api_key_for_doctor(args, data, model)
    api_key_available = bool(api_key_value)
    base_url_value, base_url_source = resolve_base_url(args, data, model)
    pillow_available = importlib_util.find_spec("PIL") is not None
    run_dir = Path(data.get("run_dir", "_work/image_gen_runs"))
    output_dir = Path(data.get("output_dir", "outputs"))
    batch_dir = Path(data.get("batch_dir", "_work/image_gen_batches"))
    _print({
        "ok": True,
        "version": SCRIPT_VERSION,
        "python": {
            "executable": sys.executable,
            "version": sys.version.split()[0],
            "major": sys.version_info.major,
            "minor": sys.version_info.minor,
            "supported": sys.version_info >= (3, 9),
        },
        "config_path": str(config_path()),
        "config_exists": config_path().exists(),
        "default_provider": data.get("default_provider"),
        "default_model": data.get("default_model"),
        "model": model,
        "default_route": data.get("default_route"),
        "enabled_routes": data.get("enabled_routes"),
        "route_priority": data.get("route_priority"),
        "directories": {
            "run_dir": str(run_dir),
            "run_dir_exists": run_dir.exists(),
            "output_dir": str(output_dir),
            "output_dir_exists": output_dir.exists(),
            "batch_dir": str(batch_dir),
            "batch_dir_exists": batch_dir.exists(),
        },
        "optional_tools": {
            "pillow": {
                "available": pillow_available,
                "purpose": "automatic local image resize, compression, format normalization, deeper inspection, transparent PNG post-processing, and multi-image preview contact sheets",
                "install_hint": "python -m pip install Pillow" if not pillow_available else None,
            },
        },
        "provider_api_calls_enabled": True,
        "routes": {
            "codex_cli": {
                "available": codex_command is not None,
                "command": codex_command,
                "install_hint": "Install and login to Codex CLI, or choose an API-key route preset." if not codex_command else None,
            },
            "api_key": {
                "available": api_key_available,
                "source": api_key_source,
                "value": mask_secret(api_key_value),
                "model_env": MODEL_API_KEY_ENVS.get(model),
                "shared_env": API_KEY_ENV,
                "env": API_KEY_ENV,
                "config_key": "api_key",
                "install_hint": _api_key_install_hint(model) if not api_key_available else None,
            },
            "base_url": {
                "value": base_url_value,
                "source": base_url_source,
                "model_env": MODEL_BASE_URL_ENVS.get(model),
                "shared_env": BASE_URL_ENV,
                "env": BASE_URL_ENV,
                "config_key": "base_url",
                "default": DEFAULT_BASE_URL,
            },
        },
        "install_hints": _install_hints(codex_command is not None, api_key_available, pillow_available),
    })
    return 0


def _resolve_api_key_for_doctor(args, data: dict, model: str) -> tuple[str | None, str | None]:
    if getattr(args, "api_key", None):
        return args.api_key, "cli_arg"
    model_env = MODEL_API_KEY_ENVS.get(model)
    if model_env:
        model_value = os.environ.get(model_env)
        if model_value:
            return model_value, f"env:{model_env}"
    value = os.environ.get(API_KEY_ENV)
    if value:
        return value, f"env:{API_KEY_ENV}"
    if data.get("api_key"):
        return str(data["api_key"]), "config_file"
    return None, None


def _api_key_install_hint(model: str) -> str:
    model_env = MODEL_API_KEY_ENVS.get(model)
    if model_env:
        return f"Set {model_env} or {API_KEY_ENV}, run `imagen setup --api-key ...`, or pass --api-key for one command."
    return f"Set {API_KEY_ENV}, run `imagen setup --api-key ...`, or pass --api-key for one command."


def _install_hints(codex_available: bool, api_key_available: bool, pillow_available: bool) -> list[str]:
    hints = []
    if not codex_available:
        hints.append("codex-cli route is unavailable until the codex command is installed and logged in.")
    if not api_key_available:
        hints.append(f"api-key route is unavailable until {API_KEY_ENV} is set or --api-key is passed.")
    if not pillow_available:
        hints.append("Pillow is recommended for automatic local image resize, compression, format normalization, transparent PNG post-processing, and multi-image preview contact sheets.")
    return hints


def _setup_next_steps(data: dict) -> list[str]:
    return [
        "Choose or confirm the default model with `imagen setup --non-interactive --default-model gpt-image-2|nano-banana-2|mj` or `imagen config set default_model ...`.",
        "For agent-wide persistent API use, set IMAGE_GEN_PRO_API_KEY and IMAGE_GEN_PRO_API_BASE_URL as user environment variables; for CLI-local persistence, use `imagen setup --non-interactive --api-key ... --base-url ...`.",
        f"Check the active preference and credential sources with `imagen config list` and `imagen doctor --model {data.get('default_model', 'gpt-image-2')}` before the first real generation.",
    ]


def handle_config(args) -> int:
    data = load_config()
    if args.config_command == "path":
        print(config_path())
    elif args.config_command == "list":
        _print(redact_config(data))
    elif args.config_command == "get":
        _print(redact_config({args.key: data.get(args.key)}))
    elif args.config_command == "set":
        value = args.value if args.key in {"api_key", "base_url"} else parse_value(args.value)
        if args.key == "default_provider":
            value = validate_provider(str(value))
        if args.key == "default_model":
            value = normalize_image_model(str(value))
        if args.key in {"enabled_routes", "route_priority"}:
            value = parse_route_list(value)
        data[args.key] = value
        save_config(data)
        data = load_config()
        _print(redact_config({"ok": True, args.key: data.get(args.key)}))
    elif args.config_command == "unset":
        existed = args.key in data
        data.pop(args.key, None)
        save_config(data)
        _print({"ok": True, "removed": existed})
    return 0


def handle_runs(args) -> int:
    data = load_config()
    if args.runs_command == "list":
        _print(list_runs(data, args.limit))
    elif args.runs_command == "show":
        _print(show_run(data, args.run_id))
    return 0


def handle_jobs(args) -> int:
    data = load_config()
    if args.jobs_command == "list":
        _print(list_jobs(data, args.limit))
    elif args.jobs_command == "show":
        _print(show_job(data, args.run_id))
    elif args.jobs_command == "wait":
        _print(wait_job(data, args.run_id, args.timeout_sec))
    elif args.jobs_command == "delete":
        _print(delete_job(data, args.run_id))
    return 0


def handle_batches(args) -> int:
    if args.batches_command == "run":
        _print(run_batch(args))
    elif args.batches_command == "list":
        _print(list_batches(args))
    elif args.batches_command == "show":
        _print(show_batch(args))
    return 0


def handle_plan_or_dry_run(args) -> int:
    data = load_config()
    provider = args.provider or data.get("default_provider") or "placeholder"
    prompt = resolve_prompt(args.prompt, args.prompt_file)
    request = build_neutral_request(prompt, provider, args.reference)
    run_id = args.run_id or stable_run_id(prompt)
    run_dir = run_paths(data.get("run_dir", "_work/image_gen_runs"), run_id)
    job = new_job(run_id, run_dir, args.command, request["provider"])
    write_job(run_dir, job)
    (run_dir / "prompt.txt").write_text(prompt + "\n", encoding="utf-8")
    write_json(run_dir / "request.json", request)
    job = mark_job(job, "succeeded")
    write_job(run_dir, job)
    artifacts = ["prompt.txt", "request.json", "manifest.json", "summary.json", "generation-log.json", "job.json"]
    write_json(run_dir / "manifest.json", {
        "schema": "image-gen-pro.run-manifest.v1",
        "run_id": run_id,
        "command": args.command,
        "provider": request["provider"],
        "prompt_chars": len(prompt),
        "reference_count": len(request["references"]),
        "artifacts": artifacts,
    })
    summary = summarize_request(request)
    summary["run_dir"] = str(run_dir)
    write_json(run_dir / "summary.json", summary)
    write_json(run_dir / "generation-log.json", {
        "schema": "image-gen-pro.generation-log.v1",
        "run_id": run_id,
        "command": args.command,
        "provider": request["provider"],
        "prompt": prompt_fingerprint(prompt),
        "references": request["references"],
        "route": {
            "requested_route": None,
            "default_route": data.get("default_route"),
            "enabled_routes": data.get("enabled_routes"),
            "route_priority": data.get("route_priority"),
            "final_route": None,
        },
        "job": {
            "status": job["status"],
            "updated_at": job["updated_at"],
            "remote_task": None,
        },
        "artifacts": artifacts,
        "warnings": [],
    })
    _print(summary)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "setup":
            return handle_setup(args)
        if args.command == "doctor":
            return handle_doctor(args)
        if args.command == "config":
            return handle_config(args)
        if args.command == "runs":
            return handle_runs(args)
        if args.command == "jobs":
            return handle_jobs(args)
        if args.command == "batches":
            return handle_batches(args)
        if args.command == "transparent":
            _print(make_transparent(args))
            return 0
        if args.command in {"plan", "dry-run"}:
            return handle_plan_or_dry_run(args)
        if args.command in {"generate", "edit"}:
            return handle_provider_payload(args, _print)
        if args.command == "version":
            print(SCRIPT_VERSION)
            return 0
        parser.error("unknown command")
    except ImageGenError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return exc.exit_code
    return 0
