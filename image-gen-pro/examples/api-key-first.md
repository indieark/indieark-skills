# API Key First

Use when the user wants `imagen --route auto` to try API key route before Codex CLI.

## Setup

```powershell
python scripts\imagen.py setup --non-interactive --route-preset api-key-first --api-key "<provider-api-key>" --base-url "https://api.openai.com"
python scripts\imagen.py doctor
```

`doctor` should show `routes.api_key.available = true`, `routes.api_key.source = config_file`, and a masked key. If the user wants a one-command temporary credential instead, pass `--api-key` / `--base-url` on the `generate` or `edit` command; that does not write config.

## Dry-Run Before Spending API Quota

```powershell
python scripts\imagen.py generate --prompt "A clean product hero image of ..." --dry-run-payload --run-id api-key-dry-run
python scripts\imagen.py runs show api-key-dry-run
```

## Real Generate

```powershell
python scripts\imagen.py generate --prompt "A clean product hero image of ..." --route auto --output-file .\outputs\product-hero.png --run-id api-key-product-hero
```

Temporary override:

```powershell
python scripts\imagen.py generate --prompt "A clean product hero image of ..." --route api-key --api-key "<temporary-key>" --base-url "http://host:port/v1" --output-file .\outputs\product-hero.png
```

## Inspect

```powershell
python scripts\imagen.py jobs show api-key-product-hero
python scripts\imagen.py runs show api-key-product-hero
```

## Notes

- API key route uses standard-library HTTP; no provider SDK package is required.
- API key resolution is `--api-key` > `IMAGE_GEN_PRO_API_KEY` > config `api_key`; base URL resolution is `--base-url` > `IMAGE_GEN_PRO_API_BASE_URL` > config `base_url` > `https://api.openai.com`.
- `config list`, `config get api_key`, `doctor`, and artifacts must never print the raw key.
- `job.json` records local state only. Current Image API responses do not provide a persistent remote task id.
