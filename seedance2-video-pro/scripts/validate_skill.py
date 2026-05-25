#!/usr/bin/env python3
"""Self-check for the seedance2-video-pro Skill package.

It does NOT call the Volcengine API. It only verifies that the local Skill
package stays internally consistent so an agent can trust the layered index:

- SKILL.md exists and has Anthropic-compatible frontmatter (name + description only).
- skill.json is valid JSON and exposes name / version / runtime / capabilities.
- skill.json version appears in CHANGELOG.md as the most recent section.
- CHANGELOG.md exists.
- references/README.md links every top-level reference and subdirectory index.
- references/*/README.md links every file inside its own subdirectory.
- Every non-index reference file has `Load when` / `Avoid` / `Pairs with` metadata.
- All markdown links pointing into other Skill files actually resolve.
- examples/payloads/*.json are valid JSON and contain `model` and `content`.
- scripts/seedance2_video.py exists (entrypoint declared in skill.json).

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
ERRORS: list[str] = []
WARNINGS: list[str] = []


def fail(msg: str) -> None:
    ERRORS.append(msg)


def warn(msg: str) -> None:
    WARNINGS.append(msg)


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
    if fm.get("name") and fm["name"] != "seedance2-video-pro":
        fail(f"SKILL.md frontmatter name should be seedance2-video-pro, got {fm['name']!r}")
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
    runtime = data.get("runtime") or {}
    entry = runtime.get("entrypoint") if isinstance(runtime, dict) else None
    if entry:
        entry_path = SKILL_ROOT / entry
        if not entry_path.exists():
            fail(f"skill.json runtime.entrypoint `{entry}` does not exist")
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


SUBDIRECTORY_INDEXES = {
    "methods": "methods/README.md",
    "visual-assets": "visual-assets/README.md",
}


def check_references_index() -> None:
    index_path = SKILL_ROOT / "references" / "README.md"
    if not index_path.exists():
        fail("references/README.md is missing")
        return
    index_text = index_path.read_text(encoding="utf-8")

    for ref in list_reference_files():
        rel = ref.relative_to(SKILL_ROOT / "references").as_posix()
        subdir = rel.split("/", 1)[0]
        sub_index = SUBDIRECTORY_INDEXES.get(subdir)
        if sub_index and rel != sub_index:
            continue
        if rel not in index_text:
            fail(f"references/README.md does not mention `{rel}`")

    refs_dir = SKILL_ROOT / "references"
    for subdir, index_rel in SUBDIRECTORY_INDEXES.items():
        sub_index_path = refs_dir / index_rel
        if not sub_index_path.exists():
            fail(f"references/{index_rel} is missing")
            continue
        sub_index_text = sub_index_path.read_text(encoding="utf-8")
        for ref in sorted((refs_dir / subdir).glob("*.md")):
            if ref.name == "README.md":
                continue
            rel_name = ref.name
            if rel_name not in sub_index_text:
                fail(f"references/{index_rel} does not mention `{rel_name}`")


def check_reference_headers() -> None:
    required = ("Load when:", "Avoid:", "Pairs with:")
    for ref in list_reference_files():
        rel = ref.relative_to(SKILL_ROOT).as_posix()
        text = ref.read_text(encoding="utf-8")
        head = "\n".join(text.splitlines()[:8])
        for marker in required:
            if marker not in head:
                fail(f"{rel} missing reference header marker `{marker}` near top")


def check_storyboard_reference_contract() -> None:
    required_phrases = {
        "references/visual-assets/storyboard-board.md": [
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
        ],
        "references/visual-assets/script-composed-storyboard.md": [
            "Per-CUT Card Binding",
            "character_refs",
            "scene_ref",
        ],
        "references/visual-assets/seedance-handoff.md": [
            "character_refs",
            "scene_ref",
            "首版正式确认开始就是 4K 或等效 4K",
            "低清草稿不得登记、确认或提交给 Seedance",
            "第一张进入登记和用户确认流程的故事板图必须为 4K 或等效 4K",
        ],
        "references/generation-workflow.md": [
            "故事板规格：首版正式故事板即 4K 或更高",
            "不设置低清预览确认门",
            "不是低清图简单放大",
        ],
    }
    for rel, phrases in required_phrases.items():
        text = (SKILL_ROOT / rel).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                fail(f"{rel} must mention {phrase!r}")


def check_guide_mode_contract() -> None:
    required_phrases = {
        "SKILL.md": [
            "references/guide-mode.md",
            "角色卡",
            "场景卡",
            "不调用 CLI",
            "不构造 payload",
            "不要求 API key",
        ],
        "references/guide-mode.md": [
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
        "skill.json": [
            "feature_intro_guide_mode",
            "detailed_feature_intro_guide",
            "no_cli_guide_mode",
            "on_demand_feature_guide",
        ],
        "agents/openai.yaml": [
            "detailed feature introduction",
            "on-demand explanation",
            "without calling the CLI",
        ],
    }
    for rel, phrases in required_phrases.items():
        text = (SKILL_ROOT / rel).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                fail(f"{rel} must mention {phrase!r}")


def check_generation_workflow_contract() -> None:
    required_phrases = {
        "references/generation-workflow.md": [
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
        "references/router.md": [
            "Director Process Gate",
            "director-process-required",
            "natural-language-to-shot-breakdown",
            "scene-card-before-storyboard",
            "任意非抽象镜头缺 `scene_ref`",
        ],
        "references/director.md": [
            "写 Prompt 前置条件",
            "自然语言转剧本、剧本转镜头、镜头转角色/场景/道具资产依赖",
            "没有故事板时，也不能省略这个步骤",
            "不要直接从自然语言创意跳写",
            "是否写清输出规格、声音、说话人声、字幕/标题文字和不需要的输入",
        ],
        "SKILL.md": [
            "复杂生成任务必须先完成自然语言转剧本",
            "不允许直接从一句自然语言跳到最终 prompt 或 API",
            "非抽象镜头缺场景卡时",
            "清晰度/分辨率",
            "字幕/标题文字",
        ],
        "references/visual-storyboard.md": [
            "generation-workflow.md",
            "结构化修改意见",
            "标准文本格式",
            "结构化 JSON",
        ],
        "references/completion.md": [
            "generation-workflow.md",
            "标准文本格式",
            "结构化 JSON",
            "requested_changes",
        ],
        "references/cli.md": [
            "标准文本格式",
            "结构化 JSON",
            "历史 HTML 实验命令",
        ],
        "skill.json": [
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
        "agents/openai.yaml": [
            "convert natural language into script candidates",
            "shot breakdown",
            "character/scene/prop asset dependencies",
        ],
    }
    for rel, phrases in required_phrases.items():
        text = (SKILL_ROOT / rel).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                fail(f"{rel} must mention {phrase!r}")


def check_continuity_reference_contract() -> None:
    required_phrases = {
        "references/visual-assets/multi-segment-continuity.md": [
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
        "references/visual-assets/seedance-handoff.md": [
            "输入负载",
            "continuity_mode",
            "cut_continuity",
        ],
        "references/router.md": [
            "智能编排与拆分门",
            "15 秒是单次生成上限，不是默认目标",
            "Intelligent Orchestration Gate",
            "continuity_mode",
            "镜头边界",
        ],
        "references/README.md": [
            "智能编排、自动拆分或多段连续性",
        ],
        "references/visual-assets.md": [
            "Intelligent Orchestration Gate",
            "15 秒是否只是上限",
            "单段是否可行",
            "智能编排判断",
        ],
        "references/visual-assets/README.md": [
            "智能编排判断",
            "15 秒是否只是上限",
            "单段是否可行",
            "智能编排与多段连续性",
        ],
        "references/generation-workflow.md": [
            "智能编排判断",
            "15 秒是否只是上限",
            "单段是否可行",
        ],
        "references/visual-assets/storyboard-board.md": [
            "15 秒是单次生成上限，不是故事板默认目标",
            "Intelligent Orchestration Gate",
        ],
        "SKILL.md": [
            "智能编排与拆分",
            "15 秒是否只是上限",
            "single storyboard / storyboard + cards / multi-segment rounds by complexity-change-density-load",
        ],
    }
    for rel, phrases in required_phrases.items():
        text = (SKILL_ROOT / rel).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                fail(f"{rel} must mention {phrase!r}")


def check_character_scene_reference_contract() -> None:
    required_phrases = {
        "references/visual-assets/character-sheet.md": [
            "正式角色卡提示词只能使用下面两种之一",
            "第一种：人设描述提示词",
            "第二种：人设三视图提示词",
            "输出尺寸至少 2K，16:9 不低于 2560x1440",
            "细节丰富或主角 master 优先 4K，推荐 3840x2160",
            "第三种：多视图人设提示词",
            "最低 2K，16:9 不低于 2560x1440",
            "多视图 master、主角、系列内容、服饰/饰品拆解复杂或文字标签较多时优先 4K",
            "底部完整展示行占画面高度 22%-28%、画面宽度 100%",
            "左侧角色信息栏占画面宽度 22%-25%",
            "中央三视图区占画面宽度 50%-55%",
            "右侧拆解栏占画面宽度 22%-25%",
            "中央主体三视图组",
            "右侧服饰拆解组",
            "右侧饰品拆解组",
            "底部完整展示行",
            "统一尺寸方框或细线边框承载",
            "方框之间保留 2%-3% 的可见间隙",
            "底部发型展示组",
            "固定 5 张完整头部图",
            "底部表情设定组",
            "固定 6 张完整头部图",
        ],
        "references/visual-assets/scene-sheet.md": [
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
        ],
        "references/visual-assets.md": [
            "场景卡路由判断",
            "不要默认只生成简单场景单图",
        ],
        "references/visual-assets/README.md": [
            "场景卡路由判断",
            "不要默认只生成简单场景单图",
        ],
        "references/generation-workflow.md": [
            "场景卡路由判断",
            "不能默认只生成简单场景单图",
        ],
        "references/router.md": [
            "场景卡只想默认出一张单图",
            "场景卡不能默认简单单图",
        ],
        "SKILL.md": [
            "生成场景卡前必须先做场景卡路由判断",
            "不要默认只生成简单场景单图",
        ],
        "skill.json": [
            "scene_card_routing_gate",
            "scene_asset_density_decision",
            "no_default_simple_scene_card",
        ],
        "agents/openai.yaml": [
            "route each scene by shot angle count",
            "instead of defaulting to a simple single scene image",
        ],
    }
    for rel, phrases in required_phrases.items():
        text = (SKILL_ROOT / rel).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                fail(f"{rel} must mention {phrase!r}")


def check_cross_project_asset_reuse_contract() -> None:
    required_phrases = {
        "SKILL.md": [
            "asset reuse",
            "reused_from",
        ],
        "references/visual-storyboard.md": [
            "Cross-Project Asset Reuse",
            "asset reuse",
            "reused_from",
            "material.stored_path",
        ],
        "references/generation-workflow.md": [
            "asset reuse",
            "reused_from",
        ],
        "references/router.md": [
            "asset reuse",
            "直接使用 `asset show` 返回的素材路径或 source",
        ],
        "references/cli.md": [
            "asset reuse",
            "reused_from",
        ],
        "references/guide-mode.md": [
            "可以复用",
            "asset reuse",
            "reused_from",
        ],
        "skill.json": [
            "asset_reuse",
            "cross_project_asset_reuse",
        ],
        "agents/openai.yaml": [
            "reusable character cards",
            "cross-project asset reuse",
        ],
    }
    for rel, phrases in required_phrases.items():
        text = (SKILL_ROOT / rel).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                fail(f"{rel} must mention {phrase!r}")


def check_prompt_detail_contract() -> None:
    required_phrases = {
        "references/director.md": [
            "prompt-detail-routing",
            "storyboard-concise-prompt",
            "no-storyboard-detailed-per-shot-prompt",
            "audio-track",
            "speech-track",
            "text-track",
        ],
        "references/sound-design.md": [
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
        "references/visual-assets/storyboard-board.md": [
            "storyboard-concise-prompt",
            "no-storyboard-detailed-per-shot-prompt",
            "speech-track",
            "text-track",
            "短不等于省略最终输入控制",
            "清晰度/分辨率",
        ],
        "references/visual-assets/seedance-handoff.md": [
            "storyboard-concise-prompt",
            "no-storyboard-detailed-per-shot-prompt",
            "speech-track",
            "text-track",
            "final-input-lock",
            "storyboard-does-not-replace-final-prompt",
            "output-spec-lock",
            "no-unneeded-generation-inputs",
        ],
    }
    for rel, phrases in required_phrases.items():
        text = (SKILL_ROOT / rel).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                fail(f"{rel} must mention {phrase!r}")


# ---------------------------------------------------------------------------
# Internal markdown link resolution
# ---------------------------------------------------------------------------

LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)#\s]+)(?:#[^)\s]*)?\)")
INLINE_REF_PATTERN = re.compile(r"`([^`]+\.md)`")


def check_markdown_links() -> None:
    md_files = list((SKILL_ROOT).rglob("*.md"))
    for md in md_files:
        if "__pycache__" in md.parts:
            continue
        text = md.read_text(encoding="utf-8")
        # Resolve [text](path) links.
        for match in LINK_PATTERN.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (md.parent / target).resolve()
            if not resolved.exists():
                fail(f"{md.relative_to(SKILL_ROOT).as_posix()} -> broken link `{target}`")
        # Resolve inline `references/xxx.md` mentions for files inside the package.
        for match in INLINE_REF_PATTERN.finditer(text):
            target = match.group(1)
            # Only validate path-like targets, ignore plain filenames such as `notes.md`.
            if "/" not in target:
                continue
            resolved = (SKILL_ROOT / target).resolve()
            if not resolved.exists():
                # Try relative to current file as a second chance.
                resolved_local = (md.parent / target).resolve()
                if not resolved_local.exists():
                    warn(
                        f"{md.relative_to(SKILL_ROOT).as_posix()} mentions `{target}` "
                        "but no file resolves at Skill root or relative path"
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
    check_storyboard_reference_contract()
    check_guide_mode_contract()
    check_generation_workflow_contract()
    check_continuity_reference_contract()
    check_character_scene_reference_contract()
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
