# Batch Generation

Load when the user asks for batch generation, many prompts, many edits, a sprite/item set, or any repeatable multi-image run.

## Runtime Rule

Batch is a manifest-driven system, not an ad hoc script. Do not ask future agents to write one-off loops around `imagen`.

`imagen batches run` reads a JSON manifest, creates persistent batch state, then executes each item through the same existing `generate` / `edit` route handling used by single-image commands. Model normalization, route priority, key resolution, base URL normalization, local media preparation, provider adapters, artifact writing, and error redaction stay owned by the normal command path.

## Commands

```powershell
imagen batches run --file .\batch.json
imagen batches run --file .\batch.json --batch-id product-icons-001
imagen batches run --file .\batch.json --batch-id product-icons-001 --resume
imagen batches run --file .\batch.json --dry-run-payload
imagen batches run --file .\batch.json --concurrency 7
imagen batches run --file .\batch.json --allow-failures
imagen batches list --limit 20
imagen batches show product-icons-001
```

Use `--dry-run-payload` first when checking a new manifest. Use `--resume` only with the same manifest; the CLI stores `request_sha256` and rejects resume if the request file changed.

## Manifest Shape

```json
{
  "batch_id": "product-icons-001",
  "concurrency": 5,
  "defaults": {
    "command": "generate",
    "model": "gpt-image-2",
    "route": "api-key",
    "size": "1024x1024",
    "output_format": "png",
    "output_dir": "outputs/product-icons"
  },
  "items": [
    {
      "id": "sword",
      "prompt": "A clean game item icon of a silver sword on a simple neutral background"
    },
    {
      "id": "shield",
      "prompt": "A clean game item icon of a blue steel shield on a simple neutral background"
    },
    {
      "id": "potion",
      "prompt": "A clean game item icon of a red health potion on a simple neutral background"
    }
  ]
}
```

`defaults` may contain shared command fields. Each item can override allowed fields and must have exactly one of `prompt` or `prompt_file`. A batch manifest must contain at least 3 items.

Top-level `concurrency` is optional. Concurrency is bounded to 1-7 workers and defaults to 5. CLI `--concurrency` overrides the manifest for the current run only; changing only the CLI concurrency does not change `request_sha256`, while changing manifest `concurrency` does.

Item fields:

- `id`
- `command`: `generate` or `edit`
- `prompt` / `prompt_file`
- `image` / `mask` for edit items
- `route`, `model`, `size`, `quality`, `n`, `background`, `moderation`
- `output_format`, `output_compression`, `output_file`, `output_dir`
- `user`, `timeout_sec`, `dry_run_payload`, `prepare_local_media`, `run_id`

## Credential Boundary

Batch manifests must not contain `api_key` or `base_url`. Use environment variables, `imagen setup`, `imagen config set`, or a normal one-command single run when testing temporary credentials.

The batch state records only normal run summaries and credential sources already written by the underlying route. It must not introduce a second credential storage path.

## Reliability Guarantees

- Writes `_work/image_gen_batches/<batch-id>/request.json`.
- Writes `_work/image_gen_batches/<batch-id>/state.json`.
- Writes `_work/image_gen_batches/<batch-id>/summary.json`.
- Writes per-item run artifacts under the configured `run_dir`.
- Uses default `run_id` format `<batch-id>-<item-id>`.
- Rejects manifests with fewer than 3 items.
- Schedules at most 1-7 concurrent workers and defaults to 5 workers.
- Rejects duplicate item ids and duplicate run ids before execution.
- Records item failures in `state.json` instead of losing them in stdout.
- Refuses to overwrite an existing batch unless `--resume` is passed.
- Refuses resume when the manifest hash changed.

## Failure Policy

Default behavior records all item failures, writes final state, then exits non-zero when any item failed. Use `--stop-on-error` to stop scheduling after the first failure; in concurrent mode, already-started items are allowed to finish and only unscheduled items remain pending. Use `--allow-failures` only when partial output is expected; the command exits zero but `state.json` still has `ok: false`.

After any batch run, inspect `batches show <batch-id>` and the per-item runs before reporting success.
