#!/usr/bin/env python3
"""Self-check for the video-gen-pro hub Skill package and its installed family.

It does NOT call the Volcengine API. It only verifies that the hub package and
its sibling satellite skills stay internally consistent so an agent can trust
the layered index:

- SKILL.md exists and has Anthropic-compatible frontmatter (name + description only).
- skill.json is valid JSON, declares role: hub and the 7 satellite names.
- skill.json version appears in CHANGELOG.md as a section.
- references/README.md links every hub reference file (hub references are flat).
- Every non-index hub reference file has `Load when` / `Avoid` / `Pairs with` metadata.
- All 7 satellite skills exist as sibling directories with SKILL.md + skill.json
  (a missing sibling means a partial install and is a hard failure).
- Cross-skill phrase contracts hold across the family (paths relative to the
  family directory, i.e. the parent of this skill root).
- All markdown links inside the hub actually resolve (CHANGELOG.md is history
  and is exempt).
- examples/payloads/*.json are valid JSON and contain `model` and `content`.
- scripts/video_gen_pro.py exists (entrypoint declared in skill.json).
- scripts/seedance2_video.py exists as the legacy shim.

Run from the Skill root:

    python scripts/validate_skill.py

Exit code 0 on success, 1 on any failure. Output is plain text so it can be
piped into CI logs.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
FAMILY_DIR = SKILL_ROOT.parent
HUB_NAME = "video-gen-pro"
SATELLITE_NAMES = [
    "video-gen-script",
    "video-gen-guide",
    "video-gen-advisor",
    "video-gen-director",
    "video-gen-storyboard",
    "video-gen-assets",
    "video-gen-cinematography",
]
ERRORS: list[str] = []
WARNINGS: list[str] = []


def fail(msg: str) -> None:
    ERRORS.append(msg)


def warn(msg: str) -> None:
    WARNINGS.append(msg)


def read_family(rel: str) -> str | None:
    """Read a family-relative file (e.g. video-gen-script/SKILL.md); fail cleanly if absent."""
    path = FAMILY_DIR / rel
    if not path.exists():
        fail(f"missing family file: {rel}")
        return None
    return path.read_text(encoding="utf-8")


def check_phrases(required_phrases: dict[str, list[str]]) -> None:
    for rel, phrases in required_phrases.items():
        text = read_family(rel)
        if text is None:
            continue
        for phrase in phrases:
            if phrase not in text:
                fail(f"{rel} must mention {phrase!r}")


# ---------------------------------------------------------------------------
# SKILL.md
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    block = text[4:end]
    data: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip()
    return data


def check_skill_md() -> dict[str, str]:
    path = SKILL_ROOT / "SKILL.md"
    if not path.exists():
        fail("SKILL.md is missing")
        return {}
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    # Anthropic skill spec only accepts `name` and `description`; the parent
    # repository validator also enforces this. Version lives in skill.json.
    for key in ("name", "description"):
        if key not in fm:
            fail(f"SKILL.md frontmatter missing `{key}`")
    extra = set(fm) - {"name", "description"}
    if extra:
        fail(f"SKILL.md frontmatter has unsupported keys: {sorted(extra)}")
    if fm.get("name") and fm["name"] != HUB_NAME:
        fail(f"SKILL.md frontmatter name should be {HUB_NAME}, got {fm['name']!r}")
    description = fm.get("description", "")
    if len(description) > 1024:
        fail(
            f"SKILL.md description is {len(description)} chars; "
            "loaders silently drop descriptions over 1024"
        )
    return fm


# ---------------------------------------------------------------------------
# skill.json
# ---------------------------------------------------------------------------

def check_skill_json() -> dict | None:
    path = SKILL_ROOT / "skill.json"
    if not path.exists():
        fail("skill.json is missing")
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"skill.json is not valid JSON: {exc}")
        return None
    for key in ("name", "version", "runtime", "capabilities"):
        if key not in data:
            fail(f"skill.json missing top-level key `{key}`")
    if data.get("role") != "hub":
        fail("skill.json must declare role: hub")
    if data.get("satellites") != SATELLITE_NAMES:
        fail("skill.json satellites list must match the 7 satellite skill names")
    runtime = data.get("runtime") or {}
    entry = runtime.get("entrypoint") if isinstance(runtime, dict) else None
    if entry:
        entry_path = SKILL_ROOT / entry
        if not entry_path.exists():
            fail(f"skill.json runtime.entrypoint `{entry}` does not exist")
    legacy_entry = SKILL_ROOT / "scripts" / "seedance2_video.py"
    if not legacy_entry.exists():
        fail("legacy compatibility shim scripts/seedance2_video.py is missing")
    return data


def check_version_in_changelog(skill_json: dict | None) -> None:
    if not skill_json:
        return
    version = skill_json.get("version")
    if not version:
        return
    changelog_path = SKILL_ROOT / "CHANGELOG.md"
    if not changelog_path.exists():
        return
    text = changelog_path.read_text(encoding="utf-8")
    needle = f"## {version}"
    if needle not in text:
        fail(f"CHANGELOG.md missing section `## {version}` for current skill.json version")


# ---------------------------------------------------------------------------
# CHANGELOG.md and references/README.md coverage
# ---------------------------------------------------------------------------

def check_changelog() -> None:
    path = SKILL_ROOT / "CHANGELOG.md"
    if not path.exists():
        fail("CHANGELOG.md is missing")


def list_reference_files() -> list[Path]:
    refs_dir = SKILL_ROOT / "references"
    if not refs_dir.exists():
        return []
    root_index = refs_dir / "README.md"
    return sorted(p for p in refs_dir.rglob("*.md") if p != root_index)


def check_references_index() -> None:
    # Hub references are flat after the hub+spoke split; satellite references
    # are indexed by their own skills.
    index_path = SKILL_ROOT / "references" / "README.md"
    if not index_path.exists():
        fail("references/README.md is missing")
        return
    index_text = index_path.read_text(encoding="utf-8")

    for ref in list_reference_files():
        rel = ref.relative_to(SKILL_ROOT / "references").as_posix()
        if "/" in rel:
            fail(f"hub references must stay flat; unexpected nested file `references/{rel}`")
            continue
        if rel not in index_text:
            fail(f"references/README.md does not mention `{rel}`")


def check_reference_headers() -> None:
    required = ("Load when:", "Avoid:", "Pairs with:")
    for ref in list_reference_files():
        rel = ref.relative_to(SKILL_ROOT).as_posix()
        text = ref.read_text(encoding="utf-8")
        head = "\n".join(text.splitlines()[:8])
        for marker in required:
            if marker not in head:
                fail(f"{rel} missing reference header marker `{marker}` near top")


# ---------------------------------------------------------------------------
# Family siblings (partial-install detection)
# ---------------------------------------------------------------------------

def check_family_siblings() -> None:
    for name in SATELLITE_NAMES:
        sat_dir = FAMILY_DIR / name
        if not sat_dir.is_dir():
            fail(f"satellite skill `{name}` is not installed next to the hub (partial install)")
            continue
        for rel in ("SKILL.md", "skill.json"):
            if not (sat_dir / rel).exists():
                fail(f"satellite skill `{name}` is missing {rel}")
        manifest_path = sat_dir / "skill.json"
        if not manifest_path.exists():
            continue
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"{name}/skill.json is not valid JSON: {exc}")
            continue
        if manifest.get("role") != "satellite":
            fail(f"{name}/skill.json must declare role: satellite")
        if manifest.get("hub") != HUB_NAME:
            fail(f"{name}/skill.json must declare hub: {HUB_NAME}")


# ---------------------------------------------------------------------------
# Cross-skill phrase contracts (paths relative to the family directory)
# ---------------------------------------------------------------------------

def check_storyboard_reference_contract() -> None:
    check_phrases({
        "video-gen-storyboard/references/storyboard-board.md": [
            "角色卡",
            "场景卡",
            "character_refs",
            "scene_ref",
            "no-low-res-storyboard-preview",
            "first-pass-4k-storyboard-required",
            "reconfirm-storyboard-before-handoff",
            "当前工作流不设置低清预览确认门",
            "不要先生成低分辨率故事板给用户确认版式",
            "第一张进入确认和登记流程的故事板图就按 4K 或等效 4K 生成",
            "高能力图像模型可以直接生成包含中文文字、CUT 表、时间码、对白和复杂版式的完整 4K 故事板母图",
            "需要确定性可编辑文字、指定字体/品牌版式、超密集 CUT 表或程序化复盘时",
        ],
        "video-gen-storyboard/references/script-composed-storyboard.md": [
            "Per-CUT Card Binding",
            "character_refs",
            "scene_ref",
            "高能力图像模型可以直接生成包含中文文字、表格和复杂版式的完整 4K 故事板母图",
            "脚本拼版用于需要确定性可编辑文字、指定字体/品牌版式、超密集 CUT 表或程序化复盘的场景",
        ],
        "video-gen-assets/references/seedance-handoff.md": [
            "character_refs",
            "scene_ref",
            "首版正式确认开始就是 4K 或等效 4K",
            "低清草稿不得登记、确认或提交给 Seedance",
            "第一张进入登记和用户确认流程的故事板图必须为 4K 或等效 4K",
        ],
        "video-gen-script/references/generation-workflow.md": [
            "故事板规格：首版正式故事板即 4K 或更高",
            "不设置低清预览确认门",
            "不是低清图简单放大",
        ],
    })
    disallowed_phrases = {
        "video-gen-director/references/director-method.md": [
            "不要依赖图像模型生成大量小字",
        ],
        "video-gen-pro/references/router.md": [
            "优先脚本拼版而不是让图像模型一次生成整张带小字的信息图",
        ],
        "video-gen-storyboard/references/visual-storyboard.md": [
            "这样可避免图像模型生成乱码小字",
        ],
        "video-gen-storyboard/references/script-composed-storyboard.md": [
            "外部图像模型生成整张复杂信息图时容易乱码",
            "图像模型生成的小字乱码",
        ],
        "video-gen-storyboard/references/storyboard-board.md": [
            "不要依赖图像模型画小字",
        ],
    }
    for rel, phrases in disallowed_phrases.items():
        text = read_family(rel)
        if text is None:
            continue
        for phrase in phrases:
            if phrase in text:
                fail(f"{rel} must not keep stale text/layout guidance {phrase!r}")


def check_guide_mode_contract() -> None:
    check_phrases({
        "video-gen-pro/SKILL.md": [
            "../video-gen-guide/SKILL.md",
            "角色卡",
            "场景卡",
            "不调 CLI",
            "不构造 payload",
            "不要求 API key",
        ],
        "video-gen-guide/references/guide-mode.md": [
            "Hard Rules",
            "Required Guide Output",
            "On-Demand Feature Guide",
            "Feature Guide Template",
            "Detailed Content Checklist",
            "Short Guide Template",
            "不调用 CLI",
            "不构造 payload",
            "不要求用户先提供 API Key",
            "这个 Skill 解决什么问题",
            "支持哪些输入模式",
            "复杂任务的标准流程",
            "生成前会让用户确认什么",
            "角色卡",
            "场景卡",
            "故事板",
            "声音",
            "结构化修改意见",
            "CLI / API / Key",
        ],
        "video-gen-guide/skill.json": [
            "feature_intro_guide_mode",
            "detailed_feature_intro_guide",
            "no_cli_guide_mode",
            "on_demand_feature_guide",
        ],
        "video-gen-pro/agents/openai.yaml": [
            "detailed feature introduction",
            "on-demand explanation",
            "without calling the CLI",
        ],
    })


def check_generation_workflow_contract() -> None:
    check_phrases({
        "video-gen-script/references/generation-workflow.md": [
            "Anti-Bypass Director Contract",
            "director-process-required",
            "natural-language-to-shot-breakdown",
            "scene-card-before-storyboard",
            "no-direct-prompt-bypass",
            "Progress Contract",
            "Stage 1: Idea To Script Candidates",
            "Stage 2: Asset Plan Confirmation",
            "Stage 3: Storyboard Edit Contract",
            "Stage 4: Standard Reply And JSON Contract",
            "Stage 5: Final Input Review",
            "Stage 6: Result Review",
            "标准回复流程",
            "标准文本",
            "结构化 JSON",
            "before_video_generation",
            "after_video_generation",
            "dimensions",
            "workflow_stage",
            "requested_changes",
            "Final Input Lock Contract",
            "final-input-lock",
            "audio-text-lock",
            "no-unneeded-generation-inputs",
            "storyboard-does-not-replace-final-prompt",
            "output-spec-lock",
            "声音 / 说话人声 / 字幕与画面文字",
        ],
        "video-gen-pro/references/router.md": [
            "Director Process Gate",
            "director-process-required",
            "natural-language-to-shot-breakdown",
            "scene-card-before-storyboard",
            "任意非抽象镜头缺 `scene_ref`",
        ],
        "video-gen-director/references/director-method.md": [
            "写 Prompt 前置条件",
            "自然语言转剧本、剧本转资产清单、剧本转镜头、镜头引用资产",
            "没有故事板时，也不能省略这个步骤",
            "不要直接从自然语言创意跳写",
            "是否写清输出规格、声音、说话人声、字幕/标题文字和不需要的输入",
        ],
        "video-gen-pro/SKILL.md": [
            "必须先把自然语言整理为剧本候选或选定剧本",
            "不允许直接从一句自然语言跳到最终 prompt 或 API",
            "非抽象镜头缺场景卡时",
            "清晰度/分辨率",
            "字幕/标题文字",
            "阶段提醒义务",
        ],
        "video-gen-storyboard/references/visual-storyboard.md": [
            "generation-workflow.md",
            "结构化修改意见",
            "标准文本格式",
            "结构化 JSON",
        ],
        "video-gen-pro/references/completion.md": [
            "generation-workflow.md",
            "标准文本格式",
            "结构化 JSON",
            "requested_changes",
        ],
        "video-gen-pro/references/cli.md": [
            "标准文本格式",
            "结构化 JSON",
            "历史 HTML 实验命令",
        ],
        "video-gen-pro/skill.json": [
            "archived_capabilities",
            "agent_html_review_gates",
            "agent_html_response_template",
            "final_input_review_gate",
            "result_review_gate",
            "paused",
            "director_process_guard",
            "natural_language_shot_breakdown_gate",
            "scene_card_generation_gate",
        ],
        "video-gen-pro/agents/openai.yaml": [
            "convert natural language into script candidates",
            "shot breakdown",
            "character/scene/prop asset dependencies",
        ],
    })


def check_continuity_reference_contract() -> None:
    check_phrases({
        "video-gen-script/references/multi-segment-continuity.md": [
            "Intelligent Orchestration Gate",
            "intelligent-orchestration-gate",
            "complexity-change-density-gate",
            "max-duration-not-target",
            "per-round-information-budget",
            "15 秒是单次生成上限，不是默认目标",
            "智能编排判断",
            "Automatic Split Route",
            "输入负载",
            "生成轮次",
            "Segment Boundary Rules",
            "continuity_mode",
            "cut_continuity",
            "tail_frame_handoff",
            "first_last_bridge",
            "extend",
        ],
        "video-gen-assets/references/seedance-handoff.md": [
            "输入负载",
            "continuity_mode",
            "cut_continuity",
        ],
        "video-gen-pro/references/router.md": [
            "智能编排与拆分门",
            "15 秒是单次生成上限，不是默认目标",
            "Intelligent Orchestration Gate",
            "continuity_mode",
            "镜头边界",
        ],
        "video-gen-pro/references/README.md": [
            "multi-segment-continuity.md",
        ],
        "video-gen-assets/references/assets.md": [
            "Intelligent Orchestration Gate",
            "15 秒是否只是上限",
            "单段是否可行",
            "智能编排判断",
        ],
        "video-gen-storyboard/references/README.md": [
            "智能编排判断",
            "15 秒是否只是上限",
            "单段是否可行",
            "智能编排与多段连续性",
        ],
        "video-gen-script/references/generation-workflow.md": [
            "智能编排判断",
            "15 秒是否只是上限",
            "单段是否可行",
        ],
        "video-gen-storyboard/references/storyboard-board.md": [
            "15 秒是单次生成上限，不是故事板默认目标",
            "Intelligent Orchestration Gate",
        ],
        "video-gen-pro/SKILL.md": [
            "智能编排与拆分",
            "15 秒是否只是上限",
            "single storyboard / storyboard + cards / multi-segment rounds by complexity-change-density-load",
        ],
    })


def check_character_scene_reference_contract() -> None:
    check_phrases({
        "video-gen-assets/references/character-sheet.md": [
            "正式角色卡提示词只能使用下面两种之一",
            "第一种：人设描述提示词",
            "第二种：人设三视图提示词",
            "输出尺寸至少 2K，16:9 不低于 2560x1440",
            "细节丰富或主角 master 优先 4K，推荐 3840x2160",
            "第三种：多视图人设提示词",
            "最低 2K，16:9 不低于 2560x1440",
            "多视图 master、主角、系列内容或服饰/饰品拆解复杂时优先 4K",
            "纯图像",
            "不写任何标题、字段表、栏目名或文字标签",
            "左 2/3 三视图区和右 1/3 拆解区",
            "右 1/3 上半为表情区，下半为细节特写区",
            "图内文字会被视频模型当成要还原的画面元素",
            "浅灰水平测量参考线",
            "右上表情组",
            "右下细节特写组",
            "4 张或 6 张完整头部图",
            "主角或表情戏重的角色用 6 张，配角或造型简洁用 4 张",
            "服饰配饰复杂用 6 格，简洁用 4 格",
        ],
        "video-gen-assets/references/scene-sheet.md": [
            "主要场景列表",
            "Scene Card Routing Contract",
            "scene-card-routing-required",
            "no-default-simple-scene-card",
            "scene-asset-density-decision",
            "shot-angle-count-gate",
            "reuse-strength-gate",
            "场景卡路由判断",
            "不要默认只生成一张简单场景单图",
            "镜头角度数",
            "复用强度",
            "空间风险",
            "不要把多个空间混在一条提示词里",
            "Basic Scene Card Route",
            "Orthographic Reuse Gate",
            "Multi-View Shot Gate",
            "Quick Indoor / Outdoor Draw",
            "Single Scene Concept Art",
            "Orthographic Scene Sheet",
            "Multi-View Scene Board",
            "场景图提示词格式",
            "场景 DNA",
            "光线方向",
            "关键道具位置",
            "禁止穿帮提醒",
            "场景卡直接作为视频模型的参考图输入，必须纯图像",
        ],
        "video-gen-assets/references/principles.md": [
            "角色卡、场景卡、道具卡直接作视频模型参考输入，必须纯图像零文字",
            "input/image-input.md",
        ],
        "video-gen-cinematography/references/input/image-input.md": [
            "Reference Purity",
            "这张图给谁当输入",
            "纯几何测量线和对齐参考线不算文字",
            "Input Economy",
            "按当前镜头精选最小够用集",
            "全能参考写法",
        ],
        "video-gen-assets/references/assets.md": [
            "场景卡路由判断",
            "不要默认只生成简单场景单图",
        ],
        "video-gen-assets/references/README.md": [
            "场景卡路由判断",
            "不要默认只生成简单场景单图",
        ],
        "video-gen-script/references/generation-workflow.md": [
            "场景卡路由判断",
            "不能默认只生成简单场景单图",
        ],
        "video-gen-pro/references/router.md": [
            "场景卡只想默认出一张单图",
            "场景卡不能默认简单单图",
        ],
        "video-gen-pro/SKILL.md": [
            "生成场景卡前必须先做场景卡路由判断",
            "不要默认只生成简单场景单图",
        ],
        "video-gen-pro/skill.json": [
            "scene_card_routing_gate",
            "scene_asset_density_decision",
            "no_default_simple_scene_card",
        ],
        "video-gen-pro/agents/openai.yaml": [
            "route each scene by shot angle count",
            "instead of defaulting to a simple single scene image",
        ],
    })


def check_core_concepts_contract() -> None:
    check_phrases({
        "video-gen-pro/references/concepts.md": [
            "三个一级概念",
            "能跨剧本复用 = 资产",
            "绑定本剧本、一次性产出 = 方法论产物",
            "可登记、可复用的资产类型共五种",
            "维度 → 形态",
            "两种并列方法",
        ],
        "video-gen-pro/SKILL.md": [
            "剧本 / 资产 / 方法论三分概念",
            "references/concepts.md",
        ],
        "video-gen-pro/references/README.md": [
            "核心概念",
            "concepts.md",
        ],
    })


def check_cross_project_asset_reuse_contract() -> None:
    check_phrases({
        "video-gen-pro/SKILL.md": [
            "asset reuse",
            "reused_from",
        ],
        "video-gen-storyboard/references/visual-storyboard.md": [
            "Cross-Project Asset Reuse",
            "asset reuse",
            "reused_from",
            "material.stored_path",
        ],
        "video-gen-script/references/generation-workflow.md": [
            "asset reuse",
            "reused_from",
        ],
        "video-gen-pro/references/router.md": [
            "asset reuse",
            "直接使用 `asset show` 返回的素材路径或 source",
        ],
        "video-gen-pro/references/cli.md": [
            "asset reuse",
            "reused_from",
        ],
        "video-gen-guide/references/guide-mode.md": [
            "可以复用",
            "asset reuse",
            "reused_from",
        ],
        "video-gen-pro/skill.json": [
            "asset_reuse",
            "cross_project_asset_reuse",
        ],
        "video-gen-pro/agents/openai.yaml": [
            "reusable character cards",
            "cross-project asset reuse",
        ],
    })


def check_prompt_detail_contract() -> None:
    check_phrases({
        "video-gen-director/references/director-method.md": [
            "prompt-detail-routing",
            "storyboard-concise-prompt",
            "no-storyboard-detailed-per-shot-prompt",
            "audio-track",
            "speech-track",
            "text-track",
        ],
        "video-gen-pro/references/sound-design.md": [
            "Speech And Text Track",
            "sound-system-manages",
            "speech-track",
            "subtitle-track",
            "title-text-track",
            "no-random-text",
            "Final Audio/Text Input Lock",
            "final-audio-text-input-lock",
            "no-unneeded-audio-inputs",
            "audio-text-independent-tracks",
        ],
        "video-gen-storyboard/references/storyboard-board.md": [
            "storyboard-concise-prompt",
            "no-storyboard-detailed-per-shot-prompt",
            "speech-track",
            "text-track",
            "短不等于省略最终输入控制",
            "清晰度/分辨率",
        ],
        "video-gen-assets/references/seedance-handoff.md": [
            "storyboard-concise-prompt",
            "no-storyboard-detailed-per-shot-prompt",
            "speech-track",
            "text-track",
            "final-input-lock",
            "storyboard-does-not-replace-final-prompt",
            "output-spec-lock",
            "no-unneeded-generation-inputs",
        ],
    })


# ---------------------------------------------------------------------------
# Internal markdown link resolution
# ---------------------------------------------------------------------------

LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)#\s]+)(?:#[^)\s]*)?\)")
INLINE_REF_PATTERN = re.compile(r"`([^`]+\.md)`")


def check_markdown_links() -> None:
    md_files = list((SKILL_ROOT).rglob("*.md"))
    for md in md_files:
        if "__pycache__" in md.parts or "_work" in md.parts or md.name == "CHANGELOG.md":
            continue
        text = md.read_text(encoding="utf-8")
        # Resolve [text](path) links.
        for match in LINK_PATTERN.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:")) or "..." in target:
                continue
            resolved = (md.parent / target).resolve()
            if not resolved.exists():
                fail(f"{md.relative_to(SKILL_ROOT).as_posix()} -> broken link `{target}`")
        # Resolve inline `references/xxx.md` mentions for files inside the family.
        for match in INLINE_REF_PATTERN.finditer(text):
            target = match.group(1)
            # Only validate path-like targets, ignore plain filenames such as `notes.md`.
            if "/" not in target or "..." in target:
                continue
            candidates = [
                (SKILL_ROOT / target),
                (md.parent / target),
                (FAMILY_DIR / target.lstrip("./")),
            ]
            if not any(c.resolve().exists() for c in candidates):
                warn(
                    f"{md.relative_to(SKILL_ROOT).as_posix()} mentions `{target}` "
                    "but no file resolves at Skill root, relative, or family path"
                )


# ---------------------------------------------------------------------------
# examples/payloads/*.json
# ---------------------------------------------------------------------------

def check_example_payloads() -> None:
    payloads_dir = SKILL_ROOT / "examples" / "payloads"
    if not payloads_dir.exists():
        warn("examples/payloads/ does not exist")
        return
    payloads = sorted(payloads_dir.glob("*.json"))
    if not payloads:
        warn("examples/payloads/ has no JSON files")
        return
    for payload in payloads:
        try:
            data = json.loads(payload.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"{payload.relative_to(SKILL_ROOT).as_posix()} invalid JSON: {exc}")
            continue
        if "model" not in data:
            fail(f"{payload.relative_to(SKILL_ROOT).as_posix()} missing `model`")
        if "content" not in data or not isinstance(data["content"], list):
            fail(f"{payload.relative_to(SKILL_ROOT).as_posix()} missing list `content`")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    check_skill_md()
    skill_json = check_skill_json()
    check_changelog()
    check_version_in_changelog(skill_json)
    check_references_index()
    check_reference_headers()
    check_family_siblings()
    check_storyboard_reference_contract()
    check_guide_mode_contract()
    check_generation_workflow_contract()
    check_continuity_reference_contract()
    check_character_scene_reference_contract()
    check_core_concepts_contract()
    check_cross_project_asset_reuse_contract()
    check_prompt_detail_contract()
    check_markdown_links()
    check_example_payloads()

    if WARNINGS:
        print("Warnings:")
        for w in WARNINGS:
            print(f"  - {w}")
    if ERRORS:
        print("Errors:")
        for e in ERRORS:
            print(f"  - {e}")
        print(f"\nvalidate_skill: FAIL ({len(ERRORS)} error(s), {len(WARNINGS)} warning(s))")
        return 1
    print(f"validate_skill: OK ({len(WARNINGS)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
