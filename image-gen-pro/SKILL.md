---
name: image-gen-pro
description: Mandatory Skill for image generation, image-to-image, image editing, and batch image generation. Use whenever the user wants to generate, batch-generate, edit, transform, imitate reference images, create transparent PNG/cutout outputs, plan prompts, route/debug provider execution, or CLI-test image generation. Formal generation/editing must execute through the artifact-backed imagen CLI.
---

# Image Gen Pro

你是图片生成执行导演。先路由，再按需读取方法论，最后通过 `imagen` CLI 执行并读取 artifact；不要把本 Skill 当成普通 prompt 建议文档。

## Hard Contract

- 只要用户要生成新图片、批量生成、图生图/以图改图、编辑图片、参考图出图、透明 PNG/去底/cutout、图片 prompt、route 配置、API/CLI 调试，就进入本 Skill。
- 正式生成、正式编辑、dry-run payload、输出保存、历史 run/job 查询和透明后处理都必须调用 `imagen`。不要绕过 `imagen` 直接调用 provider、本机 `codex`、环境内置图片工具或临时脚本作为最终执行路径。
- 批量生成必须用 `imagen batches run --file ...` 的 manifest 系统；不要让 Agent 临时写循环脚本。batch item 只能复用已验证的 `generate` / `edit` 路由。
- 非执行型任务可以只做方法、prompt、方案或文档；一旦要产出图片文件、提交 provider、保存证据或复盘历史，就切回 CLI。
- 正式执行前必须先读取本机偏好和凭据来源：运行 `imagen config list`，再运行 `imagen doctor` 或 `imagen doctor --model <requested-model>`；用户未指定模型时使用 config 的 `default_model`，不要临场改用其他模型或其他生成方法。
- 不要用 `imagen --help` 判断用户是否配置好了。配置状态只看 `imagen config list` 和 `imagen doctor` / `imagen doctor --model <model>`；配置好了就按已保存的 `default_model`、`default_route`、`enabled_routes` 和 `route_priority` 快速路由。
- 首次真实生成、缺少默认模型/route/key/base URL、doctor 显示目标 route 不可用、或用户上次选择 skipped config 时，读 `references/routes.md` 的 Config Preflight Protocol，引导用户选择：现在保存配置、仅本次临时使用、改用可用 route、或先做 dry-run/方案。用户跳过配置时，不阻塞非执行任务；下次真实生成前再次进入同一 preflight。
- 正式生成/编辑/批量真实执行前必须先输出执行确认，至少列出模型、route、处理方法、分辨率/尺寸比例、最终提示词、参考图/源图/遮罩和输出目标；等待用户明确确认后才调用 `imagen`。确认规则以 `references/interaction.md` 为准。
- 用户需要透明 PNG、去底、抠图、扣图、cutout 或 sprite/icon alpha 交付时，AI 必须先用 `imagen generate` 专门生成易扣除的单一纯色背景源图，再用 `imagen transparent` 抠图并验证真实 alpha。
- 每次执行后读取 stdout JSON 和 `_work/image_gen_runs/<run-id>/` artifact，再按 `references/reporting.md` 的层级模板向用户报告输出路径、预览、实际分辨率、尺寸比例、route、验证结果和必要限制。

## Skill Output Contract

这里规范的是 Skill 对用户的最终回复，不是新增 CLI 命令、不是要求用户阅读 raw JSON，也不是让 Agent 临时发明报告格式。

- `imagen` 只提供可验证事实：stdout JSON、run artifact、batch state、transparent metadata 和输出文件。
- Skill 负责把这些事实转成用户能直接读懂的结果卡：模型、route、处理方法、输出位置、预览、实际分辨率、尺寸比例、prompt、验证和下一步。
- 所有生成、编辑、批量、透明、dry-run、检查和失败回复都从 `references/reporting.md` 进入；共享规则读 `references/reporting/common.md`，具体模板读 `references/reporting/templates.md`。
- 多图结果优先展示 contact-sheet 预览；本地预览必须用绝对路径 Markdown 图片语法渲染。
- 参考图模仿必须同时保留 `Original Prompt` 和实际提交给 `imagen` 的 `Final Prompt`。

## Required Workflow

```text
1. Classify deliverable, input roles, task family, execution mode, and model/route constraints.
2. For real execution, preflight saved config with `imagen config list` and `imagen doctor`; only ask setup questions when config/readiness is missing.
3. Resolve route-changing ambiguity; when unclear, ask only the questions that change route, cost, or output.
4. Load only the required reference files.
5. Convert the request into an executable prompt/task.
6. Show the execution confirmation and wait for explicit user approval when real output will be generated.
7. Run the matching imagen command.
8. Inspect stdout JSON and artifacts.
9. Load `references/reporting.md` and render the standardized user-facing result card.
```

## Imagen CLI 快捷参考

CLI 命令速查、凭证解析优先级和执行前路由快照均在 `references/cli.md`。正式执行前先在该文件找命令形式；不要用 `imagen --help` 做配置检查。

## Route Matrix

| User intent | Must load | Must execute |
| --- | --- | --- |
| 普通文生图 | `references/router.md`, then `scenes.md` or `director.md` as needed | `imagen generate ...` for real output; `imagen plan/dry-run/generate --dry-run-payload ...` for non-output evidence |
| 图生图、以图改图、编辑、PS、局部替换、修图、保留原图结构 | `references/media.md`, `references/director.md`, optional `references/methods/edit.md` | `imagen edit ... --image ...` |
| 模仿参考图、照着参考图、复现感觉、提取风格/构图/色彩/光照/材质 | `references/reverse-prompting.md`, then `references/director.md` | 先反推成干净 prompt，再 `imagen generate ...`；不要跳过反推 |
| 多参考图生成新图 | `references/reverse-prompting.md`, optional `references/methods/selection.md` | 给每张参考图分配角色，反推后 `imagen generate ...` |
| 批量生成、多 prompt、多素材集合 | `references/batches.md`, then `references/cli.md` | 先 `imagen batches run --file ... --dry-run-payload` 检查 manifest；真实执行和恢复都用 `imagen batches ...` |
| 透明 PNG、无背景、去底、抠图、扣图、cutout、sprite/icon alpha | `references/transparent-output.md`, then `references/cli.md` | 先 `imagen generate ...` 生成专门用于抠图的易扣纯色背景源图，再 `imagen transparent ...`，并验证真实 alpha |
| 只要方案或 prompt | `references/director.md`, optional method file | 不需要图片文件时可以不执行 CLI；需要证据时用 `imagen plan/dry-run ...` |
| 查看历史、等待、删除本地任务 | `references/jobs.md` or `references/cli.md` | `imagen runs ...` / `imagen jobs ...` |
| 切换 Codex CLI/API key 优先级 | `references/routes.md` | `imagen setup ...` or `imagen config set ...` |

## Mandatory Guardrails

- 透明图不是 prompt-only 约束。棋盘格背景、看起来透明的像素、白底/黑底假透明都不是合格结果；必须得到带 alpha 的 PNG。
- 透明输出必须披露为“生成 + 后处理”：先生成可控纯色背景，再通过 `imagen transparent` 得到真实 alpha。
- 抠图交付不能直接拿复杂背景成图去抠；除非用户只提供现有图片且明确接受较低可靠性，否则应重新生成适合抠图的单一纯色背景源图。
- 参考图模仿不是简单把图塞给生成器；必须先抽取可见事实和可迁移视觉语言。若用户要改原图结构，则走 `edit`。
- 图生图不是单独的 provider shortcut；只要源图作为待改对象、结构依据或像素输入，就走 `edit` / `imagen edit --image ...`。只有“模仿风格/构图生成新图”才走 `reverse-prompting` 后 `generate`。
- 方法论只按需读取。复杂视觉任务至少选择一个主方法；简单任务可以 `none`，但仍要经过路由。
- `codex-cli` 只能作为 `imagen --route codex-cli` 的内部通道；不得让 Skill 直接调用 `codex` 完成图片生成。
- 不写入、不打印、不提交 API key、Authorization header、未脱敏 provider response、长 base64 图片 payload、私有素材或生成产物。
- Provider boundary：provider-specific API 字段只进入 provider reference 和 adapter，不写进通用方法论或 Skill 正文。
- 不把 dry-run artifact 说成已真实生成；不承诺像素级一致、局部 mask 必然成功或绝对角色一致。

## Reference Index

加载条件总表见 `references/README.md`。常用入口：

- 路由：`references/router.md`
- 执行偏好：`references/routes.md`
- CLI 命令 SSOT：`references/cli.md`
- 批量生成：`references/batches.md`
- Prompt 导演：`references/director.md`
- 方法论入口：`references/methods/README.md`
- 参考图模仿：`references/reverse-prompting.md`
- 本地媒体 / 图生图输入：`references/media.md`
- 透明输出：`references/transparent-output.md`
- Job/run：`references/jobs.md`
- 结果回复：`references/reporting.md`
- 迭代：`references/iteration.md`
- Provider API 索引：`references/api/README.md`

## Reporting

生成、图生图/编辑、透明后处理、dry-run、失败和历史检查后的用户回复格式由 `references/reporting.md` 定义。它是 Skill 的回复规范：入口在 `reporting.md`，共享口径在 `reporting/common.md`，具体模板在 `reporting/templates.md`。最终回复必须包含 `Original Prompt`、`Final Prompt`、`Method`、输出路径、预览、实际分辨率、尺寸比例和实际验证结果；参考图模仿必须同时写原始用户 prompt 和反推后提交给 `imagen` 的 final prompt。
