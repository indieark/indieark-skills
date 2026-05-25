# Route Preference Reference

> Load when: 首次真实生成、config preflight、用户跳过/恢复配置、检查默认模型或 route readiness、用户要切换 Codex CLI/API key 优先级、或需要解释 `--route auto`。
> Avoid: 只做 prompt 方案、gallery 选择或 dry-run payload。
> Pairs with: `interaction.md` 做首次引导；`cli.md` 给可复制命令；`api.md` 确认额度和凭证边界。

本文件记录执行路线偏好。Skill 负责引导用户选择，CLI 负责保存和执行。

## Route Presets

| Preset | Meaning | CLI Setup |
| --- | --- | --- |
| `codex-cli-first` | `auto` 先用本机 Codex CLI，失败再尝试 API key | `python scripts\imagen.py setup --non-interactive --route-preset codex-cli-first` |
| `api-key-first` | `auto` 先用自定义 API key，失败再尝试 Codex CLI | `python scripts\imagen.py setup --non-interactive --route-preset api-key-first` |
| `codex-cli-only` | 只允许 Codex CLI | `python scripts\imagen.py setup --non-interactive --route-preset codex-cli-only` |
| `api-key-only` | 只允许 API key | `python scripts\imagen.py setup --non-interactive --route-preset api-key-only` |

默认 preset 是 `codex-cli-first`，但首次真实生成前应让用户确认默认模型和 route 偏好。不要假设所有用户都想优先消耗 Codex 订阅额度。

## Config Keys

- `default_route`: `auto`、`codex-cli` 或 `api-key`。
- `default_model`: 未传 `--model` 时使用的默认图片模型，初始值是 `gpt-image-2`，可设为 `gpt-image-2`、`nano-banana-2` 或 `mj`。
- `enabled_routes`: 允许使用的 route 列表。
- `route_priority`: `auto` 模式下的尝试顺序。
- `api_key`: 可选，本机持久 API key；所有 CLI 读路径都必须脱敏显示。
- `base_url`: 可选，本机持久 API base URL；允许 `http://host:port` 或 `http://host:port/v1`，保存时统一为 provider root/prefix。

`imagen config` 可以保存 route 偏好、目录、API key 和 base URL。API key 只允许进入本机 config 文件和请求 Authorization header；不得进入文档、artifact、日志或用户回复明文。

后续变更用 CLI，不手改 JSON：

```powershell
python scripts\imagen.py config set default_route auto
python scripts\imagen.py config set default_model nano-banana-2
python scripts\imagen.py config set enabled_routes api-key,codex-cli
python scripts\imagen.py config set route_priority api-key,codex-cli
python scripts\imagen.py config set api_key "<provider-api-key>"
python scripts\imagen.py config set base_url "http://127.0.0.1:8080/v1"
```

## Config Preflight Protocol

Do not use `imagen --help` to determine config/readiness. `--help` 只用于确认命令参数面；配置状态只看 `imagen config list` 与 `imagen doctor`。

真实生成、真实编辑和真实批量执行前，按固定顺序检查：

```powershell
imagen config list
imagen doctor
imagen doctor --model gpt-image-2
imagen doctor --model nano-banana-2
imagen doctor --model mj
imagen config get default_model
imagen config get api_key
```

用户指定模型时，只跑对应的 `imagen doctor --model <model>`。未指定模型时，用 `config list` 里的 `default_model`，再跑对应 `doctor --model`。`config get api_key` 只确认脱敏 key 状态。

Preflight status:

| Status | Meaning | Skill action |
| --- | --- | --- |
| `configured` | `default_model`、`default_route`、`enabled_routes`、`route_priority` 可读，目标模型/route 在 `doctor` 中可用，key/base URL 来源已脱敏显示或不需要 | Fast route：按已保存偏好进入执行确认，不重新问安装，不重看 `--help` |
| `partially-configured` | 有默认模型或 route 偏好，但目标 route/model 不可用，例如 NB/MJ 选了 `codex-cli`、API key/base URL 缺失、Codex CLI 不可用 | 给 2-4 个配置/切换选项；真实执行前必须修复或切到可用 route |
| `unconfigured` | 缺默认偏好、route 不明确、没有可用 route，或从未运行过 setup/config | 进入首次配置引导：选择默认模型、route preset、凭据保存方式 |
| `skipped` | 用户明确暂时不配置或不想提供 key/route | 只允许继续 prompt、方案、`plan`、`dry-run` 或 `generate/edit --dry-run-payload`；下次真实执行前必须重新进入 config preflight |

Fast route when configured:

1. 使用 `default_model`，除非用户本轮显式指定 `--model`。
2. 使用 `default_route`；当它是 `auto` 时按 `route_priority`。
3. 如果 `api-key` route 被选中，只报告 `api_key_source` / `base_url_source`，不显示 key。
4. 如果 `codex-cli` route 被选中，确认目标模型是 `gpt-image-2`；NB/MJ 真实执行应切到 `api-key` 或提示配置。
5. 直接进入 `interaction.md` 的执行确认卡；不要再次询问已配置字段。

Setup / repair commands:

```powershell
imagen setup --non-interactive --default-model gpt-image-2 --route-preset codex-cli-first
imagen setup --non-interactive --default-model nano-banana-2 --route-preset api-key-first
imagen setup --non-interactive --default-model mj --route-preset api-key-first
imagen setup --non-interactive --route-preset codex-cli-only
imagen setup --non-interactive --route-preset api-key-only
imagen config set default_model gpt-image-2
imagen config set route_priority api-key,codex-cli
imagen config set api_key "<provider-api-key>"
imagen config set base_url "http://host:port/v1"
```

Credential placement:

- User environment variables：写入 `IMAGE_GEN_PRO_API_KEY` / `IMAGE_GEN_PRO_API_BASE_URL` 或模型专属变量。
- CLI config：运行 `imagen setup --non-interactive --api-key ... --base-url ...` 或 `imagen config set ...`。
- One-command temporary override：运行 `imagen generate/edit ... --route api-key --api-key ... --base-url ...`；不写入 config。
- Skip：标记 `skipped`；继续非输出任务；真实生成/编辑/批量执行前再次 preflight。

## API Key Route Credentials

`api-key` route 支持本机持久配置，也支持单次临时覆盖。解析顺序必须和 `video-gen-pro` 的设置层一致，并允许模型专属环境变量覆盖共享值。

| Item | Supported Source | Stored In Config |
| --- | --- | --- |
| API key | API key 解析顺序：`--api-key` > 模型专属环境变量 > `IMAGE_GEN_PRO_API_KEY` > CLI config `api_key` | Optional |
| Provider base URL | Base URL 解析顺序：`--base-url` > 模型专属环境变量 > `IMAGE_GEN_PRO_API_BASE_URL` > CLI config `base_url` > `https://api.openai.com` | Optional |

模型专属环境变量：

```text
IMAGE_GEN_PRO_GPT_IMAGE_2_API_KEY
IMAGE_GEN_PRO_GPT_IMAGE_2_API_BASE_URL
IMAGE_GEN_PRO_NANO_BANANA_API_KEY
IMAGE_GEN_PRO_NANO_BANANA_API_BASE_URL
IMAGE_GEN_PRO_MJ_API_KEY
IMAGE_GEN_PRO_MJ_API_BASE_URL
```

Rules:

- 首次闭环：按 `Config Preflight Protocol` 运行 `imagen config list` 和 `imagen doctor` / `imagen doctor --model <model>`，读取已配置的 `default_model`、route 偏好、key/base URL 来源；不要跳过本机偏好去使用环境内置图片工具或其他 provider 方法。
- 用户未指定模型时，使用 config 的 `default_model`；要长期切换默认模型，运行 `imagen setup --non-interactive --default-model ...` 或 `imagen config set default_model ...`。
- 只改默认模型时不会重置 route；只有显式传 `--route-preset` 时才更新 `default_route`、`enabled_routes` 和 `route_priority`。
- 持久保存：`imagen setup --non-interactive --api-key ... --base-url ...`，或分别用 `imagen config set api_key ...` / `imagen config set base_url ...`。
- 单次临时使用：在 `imagen generate/edit ... --route api-key` 后追加 `--api-key ...` / `--base-url ...`；这不会写入 config。
- 环境变量适合 agent-wide / shell-wide 持久偏好：模型专属变量覆盖共享 `IMAGE_GEN_PRO_API_KEY` 和 `IMAGE_GEN_PRO_API_BASE_URL`；共享变量覆盖 config。用户要“机器上一直可用”时，优先提醒写入用户环境变量。
- 不读取 `OPENAI_API_KEY`，避免和其他工具的通用配置互相覆盖。
- `IMAGE_GEN_PRO_API_BASE_URL` / `base_url` 可省略。设置时，`http://host:port` 和 `http://host:port/v1` 都被接受；config 保存会去掉末尾 `/` 和末尾 `/v1`，运行时再自动追加正确 endpoint。如果兼容 API 挂在额外前缀下，必须把前缀显式写进 base URL，CLI 不自动猜测项目专属前缀。
- `config list`、`config get api_key` 和 `doctor` 只显示脱敏 key；artifact 只记录 `api_key_source` / `base_url_source`，不会写入 artifact 的 key 值。
- Use `imagen doctor --model gpt-image-2|nano-banana-2|mj` to check whether `api-key` route is available for a specific model; it reports availability and source without printing the key.
- If a user asks to make API preferred, configure route priority, not credentials: `imagen setup --non-interactive --route-preset api-key-first`.

## Model Route Notes

- 模型限制和参数路由先看 `api/model-capabilities.md`；需要具体 payload、响应或错误边界时再看 `api/gpt-image-2.md`、`api/nano-banana.md` 或 `api/mj.md`。
- 默认模型初始是 `gpt-image-2`，但应以 config `default_model` 为准。
- `nano-banana`、`nano-banana-2` 和 `nb` 归一为 `nano-banana-2`，走 `/v1/images/*` 兼容代理，细节见 `api/nano-banana.md`。
- 兼容 NB API 若挂在额外前缀下，可把共享或模型专属 base URL 指到该前缀，例如 `/nbapi` 或 `/nbapi/v1`；异步代理返回 `taskId/PENDING` 时，CLI 会在配置的前缀下轮询 `/task/<task-id>`。
- `mj` 是单独的代理契约，走 `/mj/submit/imagine` + `/mj/task/<id>/fetch`，细节见 `api/mj.md`；不要把 MJ 当成 Images API 字段集合。
- 兼容 MJ API 若挂在额外前缀下，可把共享或模型专属 base URL 指到该前缀，例如 `/mjapi`；CLI 会在该前缀下请求 `/mj/submit/imagine` 和 `/mj/task/<id>/fetch`。
- 需要 MJ V8.1 或 V8 画质时，把 `--v 8.1 --sd` 或 `--v 8.1 --hd` 放进 prompt；不要用通用 `--quality high` 试图映射 MJ V8 画质。
- `codex-cli` route 当前只支持 `gpt-image-2`；NB/MJ 真实执行应显式用 `--route api-key` 或配置 `api-key-first`。

## Skill Guidance

首次真实生成或配置缺失时，给用户 2-4 个选择：

- `codex-cli-first`: 已登录 Codex，想优先用订阅能力。
- `api-key-first`: 有自定义 API key，想优先用自己的 provider 额度。
- `codex-cli-only`: 不想配置 API key。
- `api-key-only`: 不想通过本机 Codex CLI 生成。

如果用户提供 key/base URL，先确认保存策略：永久保存到本机 config，或只用于本次命令。用户选择永久保存时运行 `setup/config set`；用户选择临时使用时只在本次 `generate/edit` 命令上带 `--api-key` / `--base-url`。

用户之后说“换成 API 优先”“不要走 Codex”“只用 Codex”时，Skill 应先改 CLI config，再执行生成。执行链仍是：

```text
Skill -> imagen CLI -> configured route selection -> codex-cli or api-key
```

## Execution Rules

- 显式 `--route codex-cli` 或 `--route api-key` 必须受 `enabled_routes` 约束；禁用的 route 应直接拒绝。
- 未传 `--route` 时使用 `default_route`。
- `default_route=auto` 时按 `route_priority` 顺序尝试。
- fallback 信息只记录失败 route 和脱敏错误摘要。
