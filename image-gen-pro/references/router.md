# Routing Reference

> Load when: 需要选择任务类型、输入素材角色、方法论、CLI 操作或验证路径。
> Avoid: 用户已经明确只要某个单一 reference 的局部规则。
> Pairs with: `interaction.md` 先判断是否追问；`director.md` 承接 prompt；`cli.md` 承接命令。

本文件定义运行时路由。核心约束：**执行型图片任务必须落到 `imagen` CLI**；本 Skill 不直接调用 provider、本机 `codex` 或环境内置图片工具作为最终生成/编辑路径。

## Pipeline

```text
用户请求
-> 模式判定（executor / advisor，见 ../SKILL.md `## Execution Modes`）
-> 交付物类型
-> 输入角色
-> 任务类型 / 子路线
-> 执行模式
-> 模型与 route 约束
-> 必读 reference
-> 方法选择
-> 执行确认（真实生成/编辑/批量执行前；advisor 模式越界时同样需要）
-> imagen CLI operation（advisor 模式仅允许 plan / dry-run / payload-dry-run / inspect 类命令）
-> artifact / 输出验证
-> reporting.md 用户回复（advisor 用 Advisor Reference Pack 模板）
```

## Routing Dimensions

路由不要只按一句“生成/编辑”判断。每次执行前先在内部收束以下维度；真实执行时把关键字段写进确认卡。

| Dimension | Values | Why It Matters |
| --- | --- | --- |
| Deliverable | `prompt-only`, `plan`, `dry-run-artifact`, `payload-artifact`, `real-image`, `transparent-png`, `batch`, `inspect/config` | 决定是否需要 CLI、是否需要用户确认、以及回复模板 |
| Input role | `none`, `source-image`, `mask`, `style-reference`, `composition-reference`, `identity-reference`, `batch-manifest`, `prior-run` | 决定走 `generate`、`edit`、反推、batch 还是 run/job 检查 |
| Task family | `direct-generate`, `image-edit`, `reference-imitation`, `multi-reference-synthesis`, `transparent-output`, `batch-generate`, `iteration`, `route-config`, `runtime-inspect` | 决定必读 reference 和 CLI operation |
| Execution mode | `discuss`, `plan`, `dry-run`, `payload-dry-run`, `real-run`, `post-process`, `inspect` | 防止把 dry-run 说成已生成，或在确认前提交 provider |
| Model/route constraint | `gpt-image-2`, `nano-banana-2`, `mj`, `auto`, `codex-cli`, `api-key` | 决定 provider payload、能力边界、凭据来源和 fallback |

### Routing Snapshot

执行型任务在确认前至少形成这份快照；不需要逐字展示给用户，但最终确认卡和报告必须能追溯到这些字段。

```text
Deliverable:
Input roles:
Task family / subroute:
Execution mode:
Model / route:
Required references:
Method:
CLI operation:
Verification target:
Ambiguity resolved:
```

## Task Route

| User Need | Route | Required Reference | Required CLI |
| --- | --- | --- | --- |
| 文本生成图片 | `generate` | `director.md`; complex scenes also `scenes.md` or one method file | `imagen generate ...` |
| 图生图、以图改图、基于图片生成/编辑、PS、修图、局部替换、保留原图结构 | `edit` | `media.md` + `director.md`; optional `methods/edit.md` | `imagen edit ... --image ...` |
| 模仿参考图片、照着参考图、提取风格/构图/色彩/光照/材质后生成新图 | `reference-reverse-prompt` | `reverse-prompting.md` + `director.md` | reverse first, then `imagen generate ...` |
| 多参考图融合生成新图 | `reference-reverse-prompt` | `reverse-prompting.md`; optional `methods/selection.md` | assign roles, reverse first, then `imagen generate ...` |
| 批量生成、多 prompt、多素材集合 | `batch-generate` | `batches.md` + `cli.md` | `imagen batches run --file ...`; start with `--dry-run-payload` for new manifests |
| 透明 PNG、去底、抠图、扣图、cutout、sprite/icon alpha 输出 | `transparent-output` | `transparent-output.md` + `cli.md` | `imagen generate ...` for cutout-ready chroma source, then `imagen transparent ...` |
| 只要生成方案 | `plan` | `director.md` + `workflow.md` | optional `imagen plan ...` when artifact is useful |
| 只要中立 request 证据 | `dry-run` | `api.md` + `cli.md` | `imagen dry-run ...` |
| 只要 provider payload 证据 | `payload-dry-run` | `api.md` + `cli.md` | `imagen generate/edit --dry-run-payload ...` |
| provider 接入 | `provider-work` | `provider-adapter.md` + `api.md` | tests/validator; do not perform ad-hoc provider calls |
| 结果不满意 | `iteration` | `iteration.md` | usually inspect `imagen runs show <run-id>` before re-running |
| 切换执行路线 | `route-config` | `routes.md` + `cli.md` | `imagen setup ...` or `imagen config set ...` |
| 查看历史 run/job | `runtime-inspect` | `jobs.md` or `cli.md` | `imagen runs ...` / `imagen jobs ...` |

After any CLI operation, read `reporting.md` before replying to the user.

## Fine-Grained Subroutes

这些子路线用于处理当前最容易误判的复合意图。它们不新增 CLI 命令，只让 Agent 更稳定地选择已有命令。

| Situation | Subroute | Decision |
| --- | --- | --- |
| 用户给一张图并说“改一下 / 修一下 / 换背景 / 加文字 / 去掉某物” | `edit-source-image` | 源图是待改对象，走 `media.md` + `imagen edit --image ...` |
| 用户给一张图并说“照这个风格生成新的 / 像这张 / 参考这个感觉” | `reference-style-imitation` | 图是风格/构图参考，走 `reverse-prompting.md` 后 `imagen generate ...` |
| 用户给一张图并说“保持这个角色/商品/Logo 一致，再出新场景” | `identity-reference` | 优先读 `reverse-prompting.md` + `methods/consistency.md`；如果要求直接改原图才切 `edit` |
| 用户给多张图但没分角色 | `multi-input-disambiguation` | 先问每张图角色；不得平均混成模糊风格词 |
| 用户要求透明 PNG / sprite / icon / product cutout | `transparent-two-stage` | 先生成可抠除纯色背景源图，再 `imagen transparent`；已给本地图时可只做后处理 |
| 用户要求“一组 / 批量 / 每个 prompt 一张 / 多素材组合” | `manifest-batch` | 先把需求转成 batch manifest 并 dry-run；真实执行只用 `imagen batches run` |
| 用户说“继续上一张 / 改刚才结果 / 换一种” | `prior-run-iteration` | 先 `runs show` 或 `jobs show` 找证据，再按 `iteration.md` 修改 |
| 用户只要“提示词 / 方案 / prompt 模板” | `non-output-craft` | 不提交 provider；可按需用 `imagen plan` 写 artifact |
| 用户说“参考模式 / 我自己去 MJ\|Sora\|... 跑 / 只要素材包 / 给我提示词” | `advisor-reference-pack` | 进入 advisor mode；按 `reporting/templates.md` 的 Advisor Reference Pack 输出；只允许 plan / dry-run / payload-dry-run / inspect 类 CLI |
| 用户要检查路由、key、模型、为什么失败 | `diagnostic-route` | 先 `config list` / `doctor` / `runs show`，不要重新生成 |

## Conflict Priority

同一句话里有多个信号时，按以下优先级决定路线：

1. 明确要改原图、保留结构、局部替换、mask 或 PS：优先 `edit`。
2. 明确要透明 PNG / 去底 / cutout：优先 `transparent-output`，并判断是否需要先重新生成纯色背景源图。
3. 明确是批量、多 prompt、多素材集合：优先 `batch-generate`。
4. 明确是模仿、参考、提取风格但生成新图：优先 `reference-reverse-prompt`。
5. 明确只要 prompt、方案、评价或调试：不要真实生成。
6. 仍不确定输入图角色时先问，不要猜。

## Input Role

| Input | Role Decision |
| --- | --- |
| prompt only | 文生图、方案、dry-run 或 payload dry-run |
| one image | 先判断是图生图/edit source、style/composition reference，还是透明后处理输入 |
| image + mask | 局部编辑，优先 `edit` |
| multiple images | 参考图模仿/融合时走 `reverse-prompting.md`；编辑多源时走 `edit` |
| JSON batch manifest | 批量生成，走 `batches.md` 和 `imagen batches run --file ...` |
| prior output + feedback | 先 inspect run/job，再按 `iteration.md` 定向修正 |
| existing local cutout source | 如果只是对已有纯色背景图去底，可直接 `imagen transparent`; 如果源图背景复杂，先说明可靠性限制 |
| provider/API error output | `diagnostic-route`; 先定位 route、model、base URL、artifact，不重新生成 |

Guardrails:

- 输入图角色不明时先问；不要默认当作 edit source 或风格参考。
- 用户要“模仿/参考/照着/像这张图再生成”时，必须读 `reverse-prompting.md`；用户要“改这张图/PS/修图/局部替换/保留原图结构”时，走 `edit`。
- 用户说“图生图、以图改图、基于这张图生成/改一版”且源图是待改对象、结构依据或像素输入时，走 `edit` 和 `imagen edit --image ...`，不要转成 `generate --reference`。
- 参考图模仿当前执行形态是先由 Agent 反推成文本 prompt，再通过 `imagen generate` 生成；不要绕过 CLI 直接用外部图片工具。
- 透明图/抠图不是 prompt-only 约束。必须先生成专门用于抠图的可控纯色背景图，再后处理并验证 alpha；不要先生成复杂背景再尝试硬抠。
- 批量生成不是让 Agent 临时写循环脚本；必须用 `imagen batches run`，每个 item 复用现有 `generate` / `edit` 路由。
- 多参考图必须说明每张图的用途，不要把多图平均成模糊风格词。
- 真实生成/编辑/批量执行前必须按 `interaction.md` 展示执行确认，列明模型、route、处理方法、尺寸比例、最终提示词和参考图/源图角色；用户确认前不要调用 `imagen`。

## Method Route

先读 `methods/README.md`，只选一个主方法；复杂任务最多再选一个辅助方法。

| Need | Method |
| --- | --- |
| 构图、视觉层次、画面焦点复杂 | composition |
| 同一角色、同一商品、同一风格要延续 | consistency |
| 商品图、商店封面、商业视觉 | product |
| 风格迁移或风格约束强 | style |
| 图生图、局部修改、保留原图结构 | edit |
| 海报、UI、信息图、科研图、摄影 | typography / ui-mockups / infographics / research-figures / photography |
| 简单 prompt | none |

方法论选择只影响 prompt 和执行约束，不替代 CLI。

## CLI Operation Route

| Need | CLI Operation |
| --- | --- |
| 写方案证据 | `imagen plan ...` |
| 写中立请求证据 | `imagen dry-run ...` |
| 写 provider payload 但不提交 | `imagen generate --dry-run-payload ...` / `imagen edit --dry-run-payload ...` |
| 文生图真实调用 | `imagen generate ... --route auto|codex-cli|api-key --output-file ...` |
| 图生图 / 图像编辑真实调用 | `imagen edit ... --image ... --route auto|codex-cli|api-key --output-file ...` |
| 透明 PNG 后处理 | `imagen transparent --input ... --output ...` |
| 查看历史 run | `imagen runs list|show ...` |
| 查看本地 job | `imagen jobs list|show|wait|delete ...` |

## Verification Route

| Output Type | Verify |
| --- | --- |
| real generate/edit | stdout JSON, `job.json`, `result.json`, output file exists |
| dry-run/payload | `summary.json`, `request.json` or `request-payload-redacted.json` |
| local media edit / image-to-image | `media-manifest.json`, prepared-media entries when auto-preprocess is on |
| transparent output | PNG mode has alpha, metadata `transparent_output=true`, alpha bbox is not null for visible subject |
| codex-cli route | `result.json` records cleanup; no raw session rollout remains |
| api-key route | no API key, Authorization header, or raw long b64 payload in artifacts |
