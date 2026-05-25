# First Setup

Trigger: first use, unclear route preference, skipped config, or failed route readiness.

Canonical protocol: `references/routes.md` -> `Config Preflight Protocol`.

## Preflight

Do not use `imagen --help` to determine config/readiness.

```powershell
imagen config list
imagen doctor
imagen config get default_model
imagen config get api_key
```

Model-specific readiness:

```powershell
imagen doctor --model gpt-image-2
imagen doctor --model nano-banana-2
imagen doctor --model mj
```

Report only:

- preflight status
- `default_model`
- `default_route`
- `enabled_routes`
- `route_priority`
- redacted key/base URL source
- target route/model readiness

## States

| State | Action |
| --- | --- |
| Already Configured / `configured` | Use saved model/route/priority; proceed to execution confirmation |
| Partially Configured / `partially-configured` | Offer repair, temporary credential, route switch, or dry-run only |
| Unconfigured / `unconfigured` | Ask default model, route preset, and credential storage |
| Skipped Config / `skipped` | Allow prompt/plan/dry-run only; real output must preflight again |

## Save Defaults

```powershell
imagen setup --non-interactive --default-model gpt-image-2 --route-preset codex-cli-first
imagen setup --non-interactive --default-model nano-banana-2 --route-preset api-key-first
imagen setup --non-interactive --default-model mj --route-preset api-key-first
imagen setup --non-interactive --route-preset codex-cli-only
imagen setup --non-interactive --route-preset api-key-only
```

## Save API Config

```powershell
imagen setup --non-interactive --api-key "<provider-api-key>" --base-url "https://api.openai.com"
imagen config set api_key "<provider-api-key>"
imagen config set base_url "http://host:port/v1"
```

## Temporary API Use

```powershell
imagen generate --prompt "..." --route api-key --api-key "<temporary-key>" --base-url "http://host:port/v1" --output-file .\outputs\image.png
```

## Skipped Config Allowed

```powershell
imagen plan --prompt "..." --provider placeholder
imagen dry-run --prompt "..." --provider placeholder
imagen generate --prompt "..." --dry-run-payload
imagen edit --prompt "..." --image .\input.png --dry-run-payload
```

Not allowed while skipped: real `imagen generate`, real `imagen edit`, or non-dry-run `imagen batches run`.

When the user later asks for real output, run config preflight again.

## Confirm

```powershell
imagen config list
imagen doctor
imagen doctor --model gpt-image-2
```
