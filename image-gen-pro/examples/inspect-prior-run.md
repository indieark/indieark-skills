# Inspect Prior Run

Use when the user asks what happened in a previous generation, wants to continue from a run, or asks whether the job is done.

## List Recent Runs

```powershell
python scripts\imagen.py runs list --limit 20
```

## Show Artifacts

```powershell
python scripts\imagen.py runs show <run-id>
```

## Show Local Job State

```powershell
python scripts\imagen.py jobs show <run-id>
```

## Wait For Local Completion

```powershell
python scripts\imagen.py jobs wait <run-id> --timeout-sec 0
```

Current routes are synchronous, so `wait` normally returns the current local terminal state immediately.

## Delete Local Artifacts

```powershell
python scripts\imagen.py jobs delete <run-id>
```

This deletes only the local run directory under the configured `run_dir`. It does not delete provider-side resources or Codex sessions.
