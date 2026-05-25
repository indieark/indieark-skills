# Safety

Load when handling assets, credentials, logs, or repository hygiene.

## Rules

- Never commit API keys, `.env`, private images, generated outputs, or customer assets.
- Use `_work/` or `outputs/` for local run artifacts; both are ignored.
- Redact provider credentials before writing payloads.
- Prefer local file hashes and metadata over copying raw images into logs.
- When adding a provider, document credential names in provider-specific references, not in core unless stable.
- When migrating external craft or gallery material, rewrite into local methodology and keep attribution; do not paste long upstream prose.
- Avoid prompts that request living artists' exact style; describe visible medium, palette, lighting, line work, and composition instead.
