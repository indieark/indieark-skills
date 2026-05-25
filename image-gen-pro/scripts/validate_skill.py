from __future__ import annotations

import json
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]


def fail(message: str) -> int:
    print(f"validate_skill: {message}", file=sys.stderr)
    return 1


def main() -> int:
    skill = SKILL_DIR / "SKILL.md"
    if not skill.exists():
        return fail("missing SKILL.md")
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\nname: image-gen-pro\n"):
        return fail("invalid frontmatter")
    if "description:" not in text.split("---", 2)[1]:
        return fail("missing description")

    metadata = json.loads((SKILL_DIR / "skill.json").read_text(encoding="utf-8"))
    if metadata.get("version") != "0.1.0-beta.29":
        return fail("skill.json version must be 0.1.0-beta.29")

    required_skill_phrases = [
        "正式生成、正式编辑、dry-run payload、输出保存、历史 run/job 查询和透明后处理都必须调用 `imagen`",
        "不要绕过 `imagen` 直接调用 provider、本机 `codex`、环境内置图片工具或临时脚本作为最终执行路径",
        "正式执行前必须先读取本机偏好和凭据来源",
        "不要用 `imagen --help` 判断用户是否配置好了",
        "Config Preflight Protocol",
        "用户上次选择 skipped config",
        "下次真实生成前再次进入同一 preflight",
        "正式生成/编辑/批量真实执行前必须先输出执行确认",
        "等待用户明确确认后才调用 `imagen`",
        "CLI 命令速查、凭证解析优先级和执行前路由快照均在 `references/cli.md`",
        "批量生成必须用 `imagen batches run --file ...` 的 manifest 系统",
        "AI 必须先用 `imagen generate` 专门生成易扣除的单一纯色背景源图",
        "图生图不是单独的 provider shortcut",
        "棋盘格背景、看起来透明的像素、白底/黑底假透明都不是合格结果",
        "先反推成干净 prompt，再 `imagen generate",
        "最终回复必须包含 `Original Prompt`、`Final Prompt`、`Method`、输出路径、预览、实际分辨率、尺寸比例和实际验证结果",
        "这里规范的是 Skill 对用户的最终回复，不是新增 CLI 命令",
        "Classify deliverable, input roles, task family, execution mode, and model/route constraints",
        "Resolve route-changing ambiguity",
    ]
    for phrase in required_skill_phrases:
        if phrase not in text:
            return fail(f"SKILL.md missing hard routing phrase: {phrase}")

    transparent = (SKILL_DIR / "references/transparent-output.md").read_text(encoding="utf-8")
    for phrase in [
        "Checkerboard pattern inside the generated image is fake transparency",
        "Generate a cutout-ready source image",
        "do not first generate a normal complex-background image",
        "Run imagen transparent on that generated chroma image",
        "Verify the result is a PNG with real alpha",
        "RGB-only 去污染",
        "连通域小岛清理",
        "不默认改 alpha feather",
    ]:
        if phrase not in transparent:
            return fail(f"transparent-output.md missing hard protocol phrase: {phrase}")

    router = (SKILL_DIR / "references/router.md").read_text(encoding="utf-8")
    for phrase in [
        "执行型图片任务必须落到 `imagen` CLI",
        "图生图、以图改图、基于图片生成/编辑",
        "imagen edit --image",
        "批量生成不是让 Agent 临时写循环脚本",
        "不要绕过 CLI 直接用外部图片工具",
        "透明图/抠图不是 prompt-only 约束",
        "真实生成/编辑/批量执行前必须按 `interaction.md` 展示执行确认",
        "## Routing Dimensions",
        "### Routing Snapshot",
        "## Fine-Grained Subroutes",
        "## Conflict Priority",
        "`diagnostic-route`",
    ]:
        if phrase not in router:
            return fail(f"router.md missing hard routing phrase: {phrase}")

    reporting = (SKILL_DIR / "references/reporting.md").read_text(encoding="utf-8")
    for phrase in [
        "Report only facts supported by `imagen` stdout JSON",
        "For reference-image imitation, include both the user's original prompt/request and the final prompt submitted through `imagen`",
        "图生图 / image-to-image",
        "Original Prompt",
        "Final Prompt",
        "Method",
        "reporting/common.md",
        "reporting/templates.md",
        "Skill must render the user-facing reply from these reporting templates",
    ]:
        if phrase not in reporting:
            return fail(f"reporting.md missing required reporting phrase: {phrase}")

    interaction = (SKILL_DIR / "references/interaction.md").read_text(encoding="utf-8")
    for phrase in [
        "## Config Preflight Gate",
        "`configured`：不要再问默认模型",
        "`partially-configured`：指出缺口",
        "`unconfigured`：进入首次配置",
        "`skipped`：用户只想继续 prompt",
        "真实执行前还会再次进入 config preflight",
        "## Execution Confirmation",
        "正式生成/编辑/批量真实执行前必须先输出执行确认",
        "等待用户明确确认后才调用 `imagen`",
        "Model：即将使用的模型",
        "Route：`auto` / `codex-cli` / `api-key`",
        "Size / Ratio",
        "Final Prompt",
        "Reference Images",
        "## Ambiguity Budget",
        "只追问会改变路由、成本或不可逆结果的问题",
        "Input Roles",
        "Verification",
        "请回复“确认生成”继续",
    ]:
        if phrase not in interaction:
            return fail(f"interaction.md missing execution confirmation phrase: {phrase}")

    reverse_prompting = (SKILL_DIR / "references/reverse-prompting.md").read_text(encoding="utf-8")
    for phrase in [
        "Style Template Mode",
        "`style-template`",
        "[在此处替换为您想要生成的主体内容]",
        "Do the 15-part analysis internally",
        "If the user only asks for a prompt/template, output the prompt draft and do not run `imagen`",
        "If the user asks to generate a new image from the template, keep the existing execution route",
    ]:
        if phrase not in reverse_prompting:
            return fail(f"reverse-prompting.md missing style-template rule: {phrase}")

    media = (SKILL_DIR / "references/media.md").read_text(encoding="utf-8")
    for phrase in [
        "图生图、以图改图、基于这张图生成/改一版",
        "执行路线是 `edit`",
        "imagen edit --prompt",
        "same format and dimensions as the first `--image`, each submitted file less than 50MB, alpha channel required",
        "Masking with GPT Image is prompt-based guidance",
        "GPT masks with a different format from the first image, 50MB or larger submitted files, missing alpha, or mismatched dimensions are rejected",
    ]:
        if phrase not in media:
            return fail(f"media.md missing image-to-image route phrase: {phrase}")

    routes = (SKILL_DIR / "references/routes.md").read_text(encoding="utf-8")
    for phrase in [
        "## Config Preflight Protocol",
        "Do not use `imagen --help` to determine config/readiness",
        "`configured`",
        "`partially-configured`",
        "`unconfigured`",
        "`skipped`",
        "Fast route when configured",
        "Skip：标记 `skipped`",
        "真实生成/编辑/批量执行前再次 preflight",
        "imagen config get default_model",
        "imagen config get api_key",
        "API key 解析顺序：`--api-key` > 模型专属环境变量 > `IMAGE_GEN_PRO_API_KEY` > CLI config `api_key`",
        "Base URL 解析顺序：`--base-url` > 模型专属环境变量 > `IMAGE_GEN_PRO_API_BASE_URL` > CLI config `base_url` > `https://api.openai.com`",
        "IMAGE_GEN_PRO_NANO_BANANA_API_KEY",
        "IMAGE_GEN_PRO_MJ_API_KEY",
        "模型限制和参数路由先看 `api/model-capabilities.md`",
        "不要把 MJ 当成 Images API 字段集合",
        "default_model",
        "首次闭环",
        "`imagen setup --non-interactive --api-key ... --base-url ...`",
        "单次临时使用",
        "不会写入 artifact",
    ]:
        if phrase not in routes:
            return fail(f"routes.md missing api-key route credential phrase: {phrase}")

    cli = (SKILL_DIR / "references/cli.md").read_text(encoding="utf-8")
    for phrase in [
        "Do not run `imagen --help` for normal generation/editing",
        "Do not use `imagen --help` to determine config/readiness",
        "`config list` plus `doctor` / `doctor --model <model>` are the authoritative readiness checks",
        "`batches run|list|show` is the stable batch generation system",
        "Batch manifests must contain at least 3 items",
        "Batch concurrency is bounded to 1-7 workers and defaults to 5",
        "Batch manifests must not contain `api_key` or `base_url`",
        "request_sha256",
        "config `default_model`",
        "API key resolution: `--api-key` > model-specific env > `IMAGE_GEN_PRO_API_KEY` > config `api_key`",
        "Base URL resolution: `--base-url` > model-specific env > `IMAGE_GEN_PRO_API_BASE_URL` > config `base_url` > `https://api.openai.com`",
        "`imagen config list`, `imagen config get api_key`, and `imagen doctor` mask API keys",
        "`mj` uses `/mj/submit/imagine` plus `/mj/task/<task-id>/fetch`",
        "Base URL prefixes are explicit",
        "`--min-island-area`",
        "`--edge-decontaminate-strength`",
        "output records in `summary.json`, `result.json`, `media-manifest.json`, and `generation-log.json` include actual `width`, `height`, `resolution`, and `aspect_ratio`",
        "multi-output runs write `preview/contact-sheet.png`",
        "GPT `--mask` follows the official Images Edit rule",
        "mask guidance is prompt-based",
    ]:
        if phrase not in cli:
            return fail(f"cli.md missing command contract phrase: {phrase}")

    reporting_common = (SKILL_DIR / "references/reporting/common.md").read_text(encoding="utf-8")
    for phrase in ["Use a compact result card", "Markdown image syntax", "实际分辨率", "预览"]:
        if phrase not in reporting_common:
            return fail(f"reporting/common.md missing output standardization phrase: {phrase}")

    reporting_templates = (SKILL_DIR / "references/reporting/templates.md").read_text(encoding="utf-8")
    for phrase in ["## Real Generate / Edit", "## Batch", "## Transparent Output", "## Dry-Run / Payload Dry-Run", "## Failure"]:
        if phrase not in reporting_templates:
            return fail(f"reporting/templates.md missing template section: {phrase}")

    first_setup = (SKILL_DIR / "examples/first-setup.md").read_text(encoding="utf-8")
    for phrase in [
        "Canonical protocol: `references/routes.md` -> `Config Preflight Protocol`",
        "Do not use `imagen --help` to determine config/readiness",
        "Already Configured",
        "Partially Configured",
        "Skipped Config",
        "real `imagen generate`, real `imagen edit`, or non-dry-run `imagen batches run`",
        "When the user later asks for real output, run config preflight again",
    ]:
        if phrase not in first_setup:
            return fail(f"examples/first-setup.md missing config preflight phrase: {phrase}")

    batches = (SKILL_DIR / "references/batches.md").read_text(encoding="utf-8")
    for phrase in [
        "Batch is a manifest-driven system, not an ad hoc script",
        "same existing `generate` / `edit` route handling",
        "A batch manifest must contain at least 3 items",
        "Concurrency is bounded to 1-7 workers and defaults to 5",
        "Batch manifests must not contain `api_key` or `base_url`",
        "request_sha256",
        "`--resume`",
    ]:
        if phrase not in batches:
            return fail(f"batches.md missing required batch rule: {phrase}")

    api_index = (SKILL_DIR / "references/api/README.md").read_text(encoding="utf-8")
    for phrase in ["model-capabilities.md", "size and parameter limits", "nano-banana.md", "mj.md"]:
        if phrase not in api_index:
            return fail(f"api/README.md missing provider reference: {phrase}")

    capabilities = (SKILL_DIR / "references/api/model-capabilities.md").read_text(encoding="utf-8")
    for phrase in [
        "## Current Adapter Matrix",
        "## Size And Parameter Limits",
        "shared CLI size validator",
        "each edge <= `3840`",
        "multiple of `16`",
        "total pixels `655360..8294400`",
        "same format and dimensions as first image; each submitted file less than 50MB; alpha required; prompt-based guidance",
        "gpt-image-2 sends normalized size",
        "nano-banana-2 sends reduced aspect_ratio",
        "mj appends --ar W:H",
        "## CLI Parameter Mapping",
        "only `auto`; native V8 `--sd` / `--hd` or older `--q` belongs in prompt",
        "Optional `remote_task` when an async proxy returns `taskId/PENDING`",
        "under configured base URL or prefix",
        "The adapter does not probe project-specific fallback paths",
        "Config `default_model` controls the model used when `--model` is omitted",
        "`OPENAI_API_KEY` is not a credential source",
    ]:
        if phrase not in capabilities:
            return fail(f"model-capabilities.md missing required phrase: {phrase}")

    gpt = (SKILL_DIR / "references/api/gpt-image-2.md").read_text(encoding="utf-8")
    for phrase in [
        "## Parameter Limits",
        "Shared CLI size validator runs before payload construction",
        "gpt-image-2 sends normalized size",
        "The shared CLI size validator enforces these rules before the GPT payload is built",
        "Official mask rule is enforced locally",
        "Masking with GPT Image is prompt-based guidance",
    ]:
        if phrase not in gpt:
            return fail(f"gpt-image-2.md missing model limit phrase: {phrase}")

    mj = (SKILL_DIR / "references/api/mj.md").read_text(encoding="utf-8")
    for phrase in [
        "## Capability Matrix",
        "## CLI Parameter Mapping",
        "## Size / Parameter Limits",
        "shared CLI size validator",
        "mj appends --ar W:H",
        "Existing prompt ratio wins",
        "native quality belongs in prompt as V8 `--sd` / `--hd` or older `--q ...`",
        "does not retry hardcoded fallback prefixes",
        "Do not add MJ prompt parameters as generic CLI flags",
    ]:
        if phrase not in mj:
            return fail(f"mj.md missing required capability phrase: {phrase}")

    nb = (SKILL_DIR / "references/api/nano-banana.md").read_text(encoding="utf-8")
    for phrase in [
        "## Capability Matrix",
        "## CLI Parameter Mapping",
        "## Size / Parameter Limits",
        "shared CLI size validator",
        "nano-banana-2 sends reduced aspect_ratio",
        "repeated multipart `image` fields",
        "configured-base-without-/v1",
        "does not retry hardcoded fallback prefixes",
    ]:
        if phrase not in nb:
            return fail(f"nano-banana.md missing required capability phrase: {phrase}")

    for rel in [
        "references/interaction.md",
        "references/router.md",
        "references/routes.md",
        "references/scenes.md",
        "references/director.md",
        "references/reverse-prompting.md",
        "references/api.md",
        "references/api/README.md",
        "references/api/model-capabilities.md",
        "references/api/gpt-image-2.md",
        "references/api/nano-banana.md",
        "references/api/mj.md",
        "references/cli.md",
        "references/media.md",
        "references/transparent-output.md",
        "references/batches.md",
        "references/jobs.md",
        "references/reporting.md",
        "references/reporting/README.md",
        "references/reporting/common.md",
        "references/reporting/templates.md",
        "references/workflow.md",
        "references/provider-adapter.md",
        "references/safety.md",
        "references/iteration.md",
        "references/gallery.md",
        "references/gallery/README.md",
        "references/gallery/anime-and-manga.md",
        "references/gallery/gaming.md",
        "references/gallery/retro-and-cyberpunk.md",
        "references/gallery/cinematic-and-animation.md",
        "references/gallery/character-design.md",
        "references/gallery/illustration.md",
        "references/gallery/watercolor.md",
        "references/gallery/ink-and-chinese.md",
        "references/gallery/pixel-art.md",
        "references/gallery/isometric.md",
        "references/gallery/product-and-food.md",
        "references/gallery/brand-systems-and-identity.md",
        "references/gallery/photography.md",
        "references/gallery/typography-and-posters.md",
        "references/gallery/infographics-and-field-guides.md",
        "references/gallery/research-paper-figures.md",
        "references/gallery/official-cookbook-examples.md",
        "references/gallery/data-visualization.md",
        "references/gallery/technical-illustration.md",
        "references/gallery/architecture-and-interior.md",
        "references/gallery/scientific-and-educational.md",
        "references/gallery/fashion-editorial.md",
        "references/gallery/fine-art-painting.md",
        "references/gallery/more-illustration-styles.md",
        "references/gallery/cinematic-film-references.md",
        "references/gallery/beauty-and-lifestyle.md",
        "references/gallery/events-and-experience.md",
        "references/gallery/tattoo-design.md",
        "references/gallery/screen-photography.md",
        "references/gallery/ui-ux-mockups.md",
        "references/gallery/edit-endpoint-showcase.md",
        "references/methods/README.md",
        "references/methods/selection.md",
        "references/methods/prompt-patterns.md",
        "references/methods/composition.md",
        "references/methods/consistency.md",
        "references/methods/product.md",
        "references/methods/style.md",
        "references/methods/edit.md",
        "references/methods/typography.md",
        "references/methods/structured-prompts.md",
        "references/methods/infographics.md",
        "references/methods/research-figures.md",
        "references/methods/ui-mockups.md",
        "references/methods/photography.md",
        "references/methods/posters.md",
        "examples/README.md",
        "examples/first-setup.md",
        "examples/api-key-first.md",
        "examples/codex-cli-only.md",
        "examples/edit-with-local-media.md",
        "examples/inspect-prior-run.md",
        "scripts/imagen.py",
        "scripts/imagegenpro/commands/batches.py",
        "scripts/imagegenpro/commands/provider_payload.py",
        "scripts/imagegenpro/commands/jobs.py",
        "scripts/imagegenpro/commands/runs.py",
        "scripts/imagegenpro/media.py",
        "scripts/imagegenpro/transparent.py",
        "scripts/imagegenpro/providers/gpt_image_2.py",
        "scripts/imagegenpro/providers/image_models.py",
    ]:
        if not (SKILL_DIR / rel).exists():
            return fail(f"missing {rel}")

    print("validate_skill: OK (0 warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
