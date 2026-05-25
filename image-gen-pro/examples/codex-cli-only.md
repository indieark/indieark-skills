# Codex CLI Only

Use when the user wants to rely only on the local Codex CLI route and avoid API keys.

## Setup

```powershell
python scripts\imagen.py setup --non-interactive --route-preset codex-cli-only
python scripts\imagen.py doctor
```

`doctor` should show `routes.codex_cli.available = true`.

## Real Generate

```powershell
python scripts\imagen.py generate --prompt "A polished app icon, simple geometry, crisp edges" --route auto --output-file .\outputs\app-icon.png --run-id codex-app-icon
```

Because the preset is `codex-cli-only`, `--route auto` resolves to the Codex CLI route.

## Inspect

```powershell
python scripts\imagen.py jobs show codex-app-icon
python scripts\imagen.py runs show codex-app-icon
```

## Cleanup Boundary

`imagen --route codex-cli` must delete newly created Codex session rollout files after extracting the image and keep only redacted summaries in this repository's artifacts.
