# Workflow

Load when defining image generation task lifecycle, artifacts, or logs.

## Core Stages

1. Intake: capture user prompt, references, target use, constraints, and provider hint.
2. Normalize: record inputs without changing creative intent.
3. Plan: create a provider-neutral request object.
4. Provider payload dry-run: build redacted provider payload without reading keys or using the network.
5. Prepare media: for local edit inputs, inspect and optionally copy accepted media into the run directory.
6. Track local job state: write `job.json` for local created/running/succeeded/failed transitions.
7. Execute: adapter owns credential resolution, submission, result handling and output writing after explicit implementation.
8. Iterate: future adapter-specific feedback loop updates request and artifacts.
9. Inspect: use `runs list|show` and `jobs list|show|wait` to recover prior artifacts and state.

Stages 1-7 and 9 are implemented for synchronous `generate` / `edit` routes. Remote async provider task management remains future work.

## Artifact Rules

- Every run gets `_work/image_gen_runs/<run-id>/`.
- Store prompt as `prompt.txt` and the neutral request as `request.json`.
- Store hashes, sizes, and paths for local assets, not raw private content in Git.
- Store HTTP(S) references without query strings or fragments.
- Store provider dry-run payloads as `request-payload-redacted.json`.
- Store provider input media metadata as `media-manifest.json`.
- Store prepared local edit inputs under `prepared-media/`; do not overwrite user originals.
- Store local job state as `job.json`; keep `remote_task` null unless a real provider task id exists.
- Store `generation-log.json` for prompt fingerprint, route config, selected route, outputs, artifact list, and warnings.
- Keep provider response logs redacted.
- Do not save secrets.
