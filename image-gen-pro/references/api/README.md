# Provider API References

> Load when: 需要新增或维护 provider-specific API 参数、payload、错误映射或真实调用边界。
> Avoid: 只做 prompt 设计、gallery 迁移或通用 CLI 使用。
> Pairs with: `../api.md` 作为运行时 API 边界；`../provider-adapter.md` 作为 adapter 契约。

本目录用于承载 provider-specific API 参考。先更新这里，再实现 provider adapter。

## Rules

- provider-specific 参数只能放在本目录和 provider adapter 中。
- core workflow 只保留通用输入、artifact、redaction、output writing。
- 能力或参数不确定时，先记录来源和核验日期。
- 不保存 API key、完整 Authorization header、未脱敏 response。

## File Layout

每个 provider 一个文件，文件内同时承载 model defaults、payload、image/mask 规则、response 解析、redaction 规则、error mapping。不拆 `redaction.md` / `errors.md` 这类横切文件 — 它们与 provider 绑定，跨 provider 不可复用。

跨模型比较、尺寸限制和参数路由只放在 `model-capabilities.md`，它是索引层，不替代 provider 文件。

## Files

| File | Status | Contents |
| --- | --- | --- |
| `model-capabilities.md` | active | implemented capability matrix, size and parameter limits, CLI parameter mapping, env override matrix, deferred capabilities |
| `gpt-image-2.md` | active | model defaults, generate/edit payloads, image/mask rules, response parsing, local validation, redaction, error mapping |
| `nano-banana.md` | active | NB proxy-compatible payloads, image field rules, model-specific env names, response parsing, adapter boundary |
| `mj.md` | active | MJ proxy submit/poll contract, prompt parameter boundary, model-specific env names, result URL handling |

新增 provider 时，按 `gpt-image-2.md` 的段落结构建一个同名文件，并在本表登记一行。
