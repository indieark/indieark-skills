# Local Jobs

Load when inspecting, waiting for, or deleting local image generation run state.

## Boundary

`jobs` is a local artifact layer. It does not represent a remote provider task id, remote progress, or remote cancellation.

Current Image API and Codex CLI routes are synchronous from this CLI's point of view. `job.json` records local state transitions so the Skill can inspect what happened after a run:

- `created`
- `running`
- `succeeded`
- `failed`
- `cancelled` reserved for future local-only use

`remote_task` is currently always `null`.

## Commands

```powershell
python scripts\imagen.py jobs list --limit 20
python scripts\imagen.py jobs show <run-id>
python scripts\imagen.py jobs wait <run-id> --timeout-sec 0
python scripts\imagen.py jobs delete <run-id>
```

## Files

Every implemented run-producing command writes `_work/image_gen_runs/<run-id>/job.json`:

- `plan`
- `dry-run`
- `generate --dry-run-payload`
- `edit --dry-run-payload`
- real `generate`
- real `edit`

`runs show <run-id>` also includes `job.json` when present.

## Delete Semantics

`jobs delete <run-id>` deletes only the local run directory under the configured `run_dir`. It performs a path boundary check and does not contact provider APIs, Codex sessions, or remote services.
