# Interaction Gate

> Load when: 需要判断是否追问用户、给 2-3 个方向选项，或直接进入 CLI / prompt / API 工作。
> Avoid: 用户已经明确只问 CLI 参数、文档入口、或指定了完整生成参数。
> Pairs with: `router.md` 承接任务类型；`director.md` 承接 prompt 收束。

本文件定义图片生成任务的交互门。目标是避免过度追问，同时不在关键结果信息缺失时盲目调用。

## Decision

| Signal | Route |
| --- | --- |
| 只说“生成一张图” | `ask`：问用途、主体、画幅 |
| 有主体但用途不明 | `ask`：问交付场景或输出规格 |
| 有 2-3 个合理方向且成本较高 | `options`：给方向让用户选 |
| 有 prompt、用途、输出规格 | `proceed`：直接规划或调用 |
| 用户明确说“先讨论/先计划” | `proceed` 到 planning，不调用 API |
| 用户明确给素材但没说素材角色 | `ask`：问首图、参考图、mask、编辑对象 |
| 首次真实生成、config preflight 缺失、或目标 route/model 不可用 | `options`：按 `routes.md` 的 Config Preflight Protocol 给配置/切换/跳过选项 |

Ask 时一次最多问 3 个会影响结果的问题。低风险默认可以使用合理默认值，但要在执行前写进 route。

## Ambiguity Budget

不要为了“完美需求”反复追问；只追问会改变路由、成本或不可逆结果的问题。

| Missing / Ambiguous | Ask? | Default When Low Risk |
| --- | --- | --- |
| 输入图是源图、参考图还是 mask | Yes | 无默认；这是路由分叉点 |
| 用户是否要真实生成还是只要 prompt / 方案 | Yes, if unclear and provider call would happen | 先给方案或 dry-run，不真实提交 |
| 模型、route 或 key 保存策略 | Yes, when config preflight is `partially-configured` / `unconfigured`, or the user asks to change config | 使用 config 读取到的 `default_model` / `default_route` |
| 用户已跳过配置但现在要真实执行 | Yes | 重新进入 config preflight，不沿用旧的 skipped 状态直接生成 |
| 输出尺寸 / 比例 | Ask if delivery-specific; otherwise confirm default | `auto / model default` |
| 风格细节不完整 | Usually no | 保留用户已有风格，用 `director.md` 收束 |
| 文件名 / run id | Usually no | 使用可读短名并写入确认卡 |
| 批量并发 | Usually no | manifest 至少 3 个 item；默认 5，最高 7，除非用户指定或成本敏感 |

如果需要追问，问题优先级是：**素材角色 > 交付物/执行模式 > 尺寸/模型/route**。一次最多 3 个问题；能通过确认卡暴露的默认值，不要提前追问。

## Config Preflight Gate

真实生成、真实编辑和真实批量执行前，先按 `routes.md` 读取 `imagen config list` 与 `imagen doctor` / `imagen doctor --model <model>`。

- `configured`：不要再问默认模型、默认 route 或已存在的凭据来源；把它们写进执行确认卡即可。
- `partially-configured`：指出缺口，例如目标模型不支持当前 route、API key/base URL 缺失、Codex CLI 不可用；给用户 2-4 个可执行选项。
- `unconfigured`：进入首次配置，引导用户选择默认模型、route preset 和凭据保存方式。
- `skipped`：用户只想继续 prompt、方案、`plan`、`dry-run` 或 payload dry-run 时可以继续；如果之后要真实生成/编辑/批量执行，必须重新 preflight 并再次提示配置。

- 现在保存配置：运行 `imagen setup --non-interactive ...` 或 `imagen config set ...`。
- 本次临时使用：在本次 `imagen generate/edit ... --route api-key` 命令上追加 `--api-key` / `--base-url`，不写入 config。
- 改用可用 route：例如从 NB/MJ 的 `codex-cli` 切到 `api-key`，或从缺 key 的 `api-key` 切到可用的 `codex-cli`。
- 先跳过配置：继续 prompt/plan/dry-run；真实执行前还会再次进入 config preflight。

不要把 `imagen --help` 当配置检查问题发给用户；如果 preflight 输出显示已配置，就快速进入执行确认。

## Execution Confirmation

正式生成/编辑/批量真实执行前必须先输出执行确认，并等待用户明确确认后才调用 `imagen`。这一步适用于会提交 provider、消耗额度、写真实输出图片、运行 `imagen generate` / `imagen edit` / `imagen batches run`（非 `--dry-run-payload`）的流程。

不需要执行确认的情况：只写 prompt/方案、`plan`、`dry-run`、`generate/edit --dry-run-payload`、`config`、`doctor`、`runs/jobs` 检查，以及用户只要求本地查看已有 artifact。若透明图流程需要先重新生成纯色背景源图，则生成源图前仍要确认；若用户只要求对已给定本地图做 `imagen transparent` 后处理，可在确认输入/输出路径清楚后直接执行。

执行确认必须覆盖这些字段：

- Model：即将使用的模型，以及来源（用户指定、config `default_model`、或默认 `gpt-image-2`）。
- Route：`auto` / `codex-cli` / `api-key`，以及凭据来源摘要；不得显示 API key。
- Config Preflight：`configured` / `partially-configured` / `unconfigured` / `skipped`，以及使用的检查命令（`config list`、`doctor`、`doctor --model <model>`）。
- Deliverable：`real-image`、`transparent-png`、`batch`、`payload-artifact` 等用户会得到的结果类型。
- Input Roles：源图、参考图、mask、batch manifest、prior run 的角色；没有就写 `无`。
- Method：`direct-generation`、`edit`、`reverse-prompting`、`transparent-output`、`batch-generate` 或具体方法论名，并说明关键处理步骤。
- Size / Ratio：待生成图像的 `--size`、输出格式、数量；如果是 MJ，把 prompt 中的 `--ar` 作为尺寸比例；如果是 `auto`，明确写 `auto / model default`。
- Final Prompt：即将提交给 `imagen` 的最终提示词；过长时给摘要并说明将写入 `prompt.txt`。
- Reference Images：参考图、源图、mask、透明后处理输入图及其角色；没有就写 `无`。更细的角色判定写入 Input Roles。
- Output：预期输出路径、batch id 或 manifest 路径；batch 还要列出 item 数、并发数和 prompt 来源。
- Verification：将检查哪些 artifact 或像素属性，如 `job.json`、`result.json`、输出文件、alpha、contact-sheet。

推荐确认文本：

```text
生成确认：
- Model：...
- Route：...
- Config Preflight：...
- Deliverable：...
- Input Roles：...
- Method：...
- Size / Ratio：...
- Final Prompt：...
- Reference Images：...
- Output：...
- Verification：...

请回复“确认生成”继续，或直接指出要改的字段。
```

确认前不要调用 `imagen generate`、`imagen edit` 或真实 `imagen batches run`。用户只说“继续”“确认”“可以”“开始生成”“执行”这类明确同意后，才进入 CLI 执行；如果用户修改任一字段，先更新确认卡，不直接生成。

## Advisor Mode 越界确认

advisor mode（参考模式，见 `../SKILL.md ## Execution Modes`）下交付的是 prompt / 资产 / checklist，不调用真实 provider。常规 advisor 回复无需 Execution Confirmation，但满足以下任一条件时必须升级确认再执行：

- 用户在同一对话内说「开始生成 / 现在出图 / 真实跑 / 执行 / run it」要求切回 executor mode。
- 用户在 advisor 上下文中要求一个本质上需要真实出图的产物（透明 PNG 像素结果、批量真实输出、模型实际渲染）。

升级确认时先复述请求，确认用户确实要切回 executor mode，再按 `## Execution Confirmation` 流程执行；不要默默切换模式直接调用 `imagen generate|edit|batches run`。

## Default Questions

- 用途是什么：封面、商品图、角色、图标、社媒图、UI 素材，还是普通概念图？
- 交付规格是什么：画幅、尺寸、透明/非透明、格式、是否需要多张？
- 素材角色是什么：输入图、参考图、mask、风格参考，还是只作灵感？
- 执行路线偏好是什么：Codex CLI 优先、自定义 API key 优先、只用 Codex CLI，还是只用 API key？

## Proceed Defaults

信息足够时默认：

- 保留用户指定风格，不强行改成通用商业模板。
- 不承诺像素级一致或局部编辑必然精确。
- 真实 API 接入前使用 `plan` / `dry-run`；接入后只有用户确认过的真实生成命令才提交 provider。
