from __future__ import annotations

from pathlib import Path

from ..artifacts import prompt_fingerprint, stable_run_id, write_json
from .jobs import mark_job, new_job, write_job
from ..config import load_config
from ..constants import GPT_IMAGE_2_MODEL
from ..errors import ImageGenError, RuntimeRouteError, UsageError
from ..output import build_output_preview, output_manifest_items, resolve_output_base, write_base64_outputs
from ..planning import resolve_prompt
from ..providers import api_key_http, codex_cli
from ..providers.image_models import build_edit_payload, build_generate_payload, normalize_image_model


def handle_provider_payload(args, print_json) -> int:
    data = load_config()
    if not getattr(args, "model", None):
        args.model = normalize_image_model(data.get("default_model"))
    prompt = resolve_prompt(args.prompt, args.prompt_file)
    run_id = args.run_id or stable_run_id(prompt)
    run_dir = Path(data.get("run_dir", "_work/image_gen_runs")) / run_id
    if args.command == "generate":
        payload, media_manifest = build_generate_payload(args, prompt, run_dir)
    else:
        payload, media_manifest = build_edit_payload(args, prompt, run_dir)

    run_dir.mkdir(parents=True, exist_ok=True)
    job = new_job(run_id, run_dir, args.command, payload["provider"])
    write_job(run_dir, job)
    (run_dir / "prompt.txt").write_text(prompt + "\n", encoding="utf-8")
    write_json(run_dir / "request-payload-redacted.json", payload)
    write_json(run_dir / "media-manifest.json", media_manifest)
    if args.dry_run_payload:
        job = mark_job(job, "succeeded")
        write_job(run_dir, job)
        return _finish_dry_run(args, print_json, run_id, run_dir, payload, prompt, data, job)

    try:
        output_base = resolve_output_base(args, data, prompt, run_id)
        job = mark_job(job, "running")
        write_job(run_dir, job)
        route_result = _submit(args, data, payload, prompt, output_base)
    except ImageGenError as exc:
        job = mark_job(job, "failed", error=_redacted_error(exc))
        write_job(run_dir, job)
        raise
    job = mark_job(job, "succeeded", route=route_result["route"], remote_task=route_result["result"].get("remote_task"))
    write_job(run_dir, job)
    outputs = route_result["outputs"]
    preview = build_output_preview(outputs, run_dir / "preview")
    if preview:
        route_result["result"]["preview"] = preview
    media_manifest["outputs"] = outputs
    if preview:
        media_manifest["preview"] = preview
    write_json(run_dir / "media-manifest.json", media_manifest)
    write_json(run_dir / "result.json", route_result["result"])
    artifacts = [
        "prompt.txt",
        "request-payload-redacted.json",
        "media-manifest.json",
        "result.json",
        "summary.json",
        "generation-log.json",
        "job.json",
    ]
    if preview and preview.get("kind") == "contact_sheet" and preview.get("path"):
        artifacts.append(_artifact_path(preview["path"], run_dir))
    summary = {
        "schema": "image-gen-pro.result-summary.v1",
        "run_id": run_id,
        "run_dir": str(run_dir),
        "command": args.command,
        "provider": payload["provider"],
        "model": payload["request"]["model"],
        "route": route_result["route"],
        "provider_api_call": route_result["route"] == "api-key",
        "dry_run_payload": False,
        "payload_path": str(run_dir / "request-payload-redacted.json"),
        "media_manifest_path": str(run_dir / "media-manifest.json"),
        "result_path": str(run_dir / "result.json"),
        "outputs": outputs,
        "preview": preview,
        "warnings": payload["warnings"],
        "job_status": job["status"],
    }
    write_json(run_dir / "summary.json", summary)
    write_json(run_dir / "generation-log.json", _generation_log(
        args=args,
        config=data,
        run_id=run_id,
        prompt=prompt,
        payload=payload,
        route_result=route_result,
        artifacts=artifacts,
        job=job,
    ))
    print_json(summary)
    return 0


def _finish_dry_run(args, print_json, run_id, run_dir, payload, prompt: str, config, job) -> int:
    artifacts = [
        "prompt.txt",
        "request-payload-redacted.json",
        "media-manifest.json",
        "summary.json",
        "generation-log.json",
        "job.json",
    ]
    summary = {
        "schema": "image-gen-pro.provider-payload-summary.v1",
        "run_id": run_id,
        "run_dir": str(run_dir),
        "command": args.command,
        "provider": payload["provider"],
        "model": payload["request"]["model"],
        "provider_api_call": False,
        "dry_run_payload": True,
        "payload_path": str(run_dir / "request-payload-redacted.json"),
        "media_manifest_path": str(run_dir / "media-manifest.json"),
        "warnings": payload["warnings"],
        "job_status": job["status"],
    }
    write_json(run_dir / "summary.json", summary)
    write_json(run_dir / "generation-log.json", _generation_log(
        args=args,
        config=config,
        run_id=run_id,
        prompt=prompt,
        payload=payload,
        route_result=None,
        artifacts=artifacts,
        job=job,
    ))
    print_json(summary)
    return 0


def _submit(args, config, payload, prompt: str, output_base):
    requested_route = args.route or config.get("default_route", "auto")
    enabled_routes = list(config.get("enabled_routes", ["codex-cli", "api-key"]))
    if requested_route != "auto":
        if requested_route not in enabled_routes:
            raise UsageError(f"route is disabled by config: {requested_route}")
        return _submit_one(requested_route, args, config, payload, prompt, output_base)

    failures = []
    for route in config.get("route_priority", enabled_routes):
        if route not in enabled_routes:
            continue
        try:
            result = _submit_one(route, args, config, payload, prompt, output_base)
            if failures:
                result["result"]["fallback_from"] = failures
            return result
        except Exception as exc:
            failures.append({"route": route, "error": str(exc)})
    raise RuntimeRouteError(f"auto route failed: {failures}")


def _submit_one(route: str, args, config, payload, prompt: str, output_base):
    if route == "codex-cli":
        return _submit_codex(args, payload, prompt, output_base)
    if route == "api-key":
        return _submit_api_key(args, config, payload, output_base)
    raise UsageError(f"unknown route: {route}")


def _generation_log(args, config, run_id: str, prompt: str, payload, route_result, artifacts: list[str], job) -> dict:
    final_route = route_result["route"] if route_result else None
    return {
        "schema": "image-gen-pro.generation-log.v1",
        "run_id": run_id,
        "command": args.command,
        "provider": payload["provider"],
        "model": payload["request"]["model"],
        "method": payload["method"],
        "prompt": prompt_fingerprint(prompt),
        "route": {
            "requested_route": args.route,
            "default_route": config.get("default_route"),
            "enabled_routes": config.get("enabled_routes"),
            "route_priority": config.get("route_priority"),
            "final_route": final_route,
            "fallback_from": route_result["result"].get("fallback_from") if route_result else None,
            "api_key_source": route_result["result"].get("api_key_source") if route_result else None,
            "base_url_source": route_result["result"].get("base_url_source") if route_result else None,
        },
        "request": {
            "size": payload["request"].get("size"),
            "quality": payload["request"].get("quality"),
            "output_format": payload["request"].get("output_format"),
            "output_compression": payload["request"].get("output_compression"),
            "n": payload["request"].get("n"),
        },
        "inputs": payload.get("files", []),
        "outputs": route_result["outputs"] if route_result else [],
        "preview": route_result["result"].get("preview") if route_result else None,
        "job": {
            "status": job["status"],
            "updated_at": job["updated_at"],
            "remote_task": route_result["result"].get("remote_task") if route_result else None,
        },
        "artifacts": artifacts,
        "warnings": payload["warnings"],
    }


def _redacted_error(exc: ImageGenError) -> dict:
    return {
        "type": exc.__class__.__name__,
        "exit_code": exc.exit_code,
        "message": str(exc)[:500],
    }


def _artifact_path(path: str, run_dir: Path) -> str:
    try:
        return str(Path(path).relative_to(run_dir))
    except ValueError:
        return path


def _submit_codex(args, payload, prompt: str, output_base):
    if payload["provider"] != GPT_IMAGE_2_MODEL:
        raise UsageError("codex-cli route currently supports only gpt-image-2")
    if args.n != 1:
        raise UsageError("codex-cli route currently supports only --n 1")
    if args.output_format.lower() != "png" and not args.output_file:
        output_base = output_base.with_suffix(".png")
    data = codex_cli.submit(payload, prompt, args.timeout_sec, output_base)
    image_format = data["provider_response"].get("image_format") or args.output_format.lower()
    outputs = output_manifest_items(data["output_paths"], image_format)
    return {
        "route": "codex-cli",
        "outputs": outputs,
        "result": {
            "schema": "image-gen-pro.route-result.v1",
            "route": "codex-cli",
            "provider_response_redacted": data["provider_response"],
            "outputs": outputs,
        },
    }


def _submit_api_key(args, config, payload, output_base):
    model = payload["provider"]
    api_key, key_source = api_key_http.resolve_api_key(args, config, model)
    base_url, base_url_source = api_key_http.resolve_base_url(args, config, model)
    if args.command == "generate":
        response = api_key_http.submit_generate(payload, api_key, args.timeout_sec, base_url)
    else:
        response = api_key_http.submit_edit(payload, api_key, args.timeout_sec, base_url)
    image_items = api_key_http.extract_image_data(response, api_key, args.timeout_sec, base_url)
    outputs = write_base64_outputs(image_items, output_base, args.output_format.lower())
    return {
        "route": "api-key",
        "outputs": outputs,
        "result": {
            "schema": "image-gen-pro.route-result.v1",
            "route": "api-key",
            "api_key_source": key_source,
            "base_url_source": base_url_source,
            "provider_response_redacted": api_key_http.redact_response(response),
            "remote_task": response.get("remote_task"),
            "outputs": outputs,
        },
    }
